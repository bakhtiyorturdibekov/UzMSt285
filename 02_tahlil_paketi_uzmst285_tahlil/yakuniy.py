"""
4-tavsiya: yakuniy qatlam.
  DM    — har bir blokdan keyin oldingi holat bilan XOR (Davies–Meyer tarzidagi oldinga uzatish):
          holat_i = Iteratsiya(holat_{i-1}, blok_i) ⊕ holat_{i-1}
  Omega — chiqish o‘zgartirishi: h(M) = P(H) ⊕ H, P = Bog‘lash(Bog‘lash(H, C1), C2), R = C8 (doimiy)
"""
import numpy as np
from algoritm import Cfg, iteration, to_units, S
from boglash import boglash
C1 = np.array([int(S[(7 * i + 1) % 256]) | 1 for i in range(32)])
C2 = np.array([int(S[(11 * i + 3) % 256]) | 1 for i in range(32)])
def P_perm(H, p):
    m = p - 1; R = np.full(len(H), 0xC8)
    return boglash(boglash(H, np.tile(C1 & m, (len(H), 1)), R, p), np.tile(C2 & m, (len(H), 1)), R, p)
def xesh_yakuniy(msgs, keys, p=256, bz='sbz', dm=True, omega=True):
    c = Cfg(p, bz); N, L = msgs.shape; bl = 32 if p == 256 else 16; nb = L // bl
    blocks = [msgs[:, i * bl:(i + 1) * bl] for i in range(nb)]
    ny = np.zeros((N, bl), dtype=np.int64)
    for n in range(N): ny[n] = list((sum(int.from_bytes(bytes(b[n].tolist()), 'big') for b in blocks) % 2 ** (8 * bl)).to_bytes(bl, 'big'))
    lb = np.tile(np.array(list((L * 8).to_bytes(bl, 'big'))), (N, 1))
    kir = [to_units(b, p) for b in blocks] + [to_units(lb, p), to_units(ny, p)]
    k = to_units(keys, p); ke = k.copy(); h = kir[0]
    for i in range(1, len(kir)):
        h0 = h; h, ke = iteration(h, kir[i], ke, k, c)
        if dm: h = h ^ h0
    return P_perm(h, p) ^ h if omega else h
