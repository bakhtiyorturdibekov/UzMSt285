"""
Yagona (unifikatsiyalangan) yakuniy variant: ikkala rejim bayt darajasida, bir xil tuzilish.
  256 bitli rejim: holat va kalit — 4×8 bayt; 128 bitli rejim: holat va kalit — 4×4 bayt (yarim baytlar yo‘q).
  Aralash — diamatritsa ko‘paytmasi (mod 256): 4×8 da ikki 4×4 yarim, 4×4 da bitta matritsa.
  Bog‘lash, SBZ, kalit jadvali, oldinga uzatish va P(H) ⊕ H — ikkala rejimda bir xil.
  Raundlar soni R (standartda 10); yutish nuqtalari: 0, R−2, R−1 (R = 10 da 0, 8, 9).
  Konstantalar: RCⱼ — √2 ning kasr qismi baytlari (j = 1…10, har biri 32 bayt), C₁, C₂ — √3 ning kasr qismi baytlari.
"""
import numpy as np
from math import isqrt
from algoritm import S, dia, surholat as _surholat8, surkalit as _surkalit8
from boglash import _yarim, yarimlar

def kasr_baytlar(n, N):
    v = isqrt(n * 256 ** (2 * N)); butun = isqrt(n) * 256 ** N
    return list((v - butun).to_bytes(N, 'big'))
_RC = kasr_baytlar(2, 320)
RC = np.array([[0] * 32] + [_RC[32 * (j - 1):32 * j] for j in range(1, 11)])
_C = kasr_baytlar(3, 64); C1 = np.array(_C[:32]) | 1; C2 = np.array(_C[32:]) | 1

def aralash_y(h, ke, w):
    N = h.shape[0]; H = h.reshape(N, 4, w); K = ke.reshape(N, 4, w)
    if w == 8:
        out = np.concatenate([dia(H[:, :, :4], K[:, :, :4], 256), dia(H[:, :, 4:], K[:, :, 4:], 256)], axis=2)
    else:
        out = dia(H, K, 256)
    return out.reshape(N, 4 * w) % 256

def _sur4(a, rows, cols):
    N = a.shape[0]; m = a.reshape(N, 4, 4).copy()
    for s_ in range(4): m[:, s_, :] = np.roll(m[:, s_, :], rows[s_], axis=1)
    for u, n in cols.items(): m[:, :, u] = np.roll(m[:, :, u], n, axis=1)
    return m.reshape(N, 16)
def surholat_y(h, w): return _surholat8(h) if w == 8 else _sur4(h, [1, 2, 3, 0], {0: 1, 1: 2, 2: 3, 3: 0})
def surkalit_y(k, w): return _surkalit8(k) if w == 8 else _sur4(k, [0, 3, 2, 1], {1: -3, 2: -2, 3: -1})

def boglash_y(H, X, R):
    H = H.copy(); L, Rt = yarimlar(H.shape[1])
    H[:, Rt] = _yarim(H[:, Rt], H[:, L], X[:, Rt], X[:, L], R)
    H[:, L] = _yarim(H[:, L], H[:, Rt], X[:, L], X[:, Rt], R)
    H[:, Rt] = _yarim(H[:, Rt], H[:, L], X[:, Rt], X[:, L], R)
    return H
def sbz_y(h, n): return S[h ^ S[n]]

def iteration_g(holat, blok, ke, k, R_raund=10, trace=None):
    w = holat.shape[1] // 4; Rp = k[:, 0] & 0xFE; mm = 4 * w
    def T(nm, j):
        if trace is not None: trace.append((nm, j, holat.copy(), ke.copy()))
    ke = ke | 1
    holat = sbz_y(boglash_y(holat, blok, Rp), blok); T('yutish0', 0)
    for j in range(1, R_raund + 1):
        holat = aralash_y(holat, ke, w)
        holat = boglash_y(holat, ke, Rp)
        holat = surholat_y(holat, w); ke = (surkalit_y(ke, w) ^ RC[j][:mm]) | 1
        if j == R_raund - 2: holat = sbz_y(boglash_y(holat, blok, Rp), blok)
        else: holat = boglash_y(holat, ke, Rp)
        if j == R_raund - 1: holat = sbz_y(boglash_y(holat, blok, Rp), blok)
        T('raund', j)
    return holat, ke

def xesh_g(msgs, keys, R_raund=10):
    """msgs: (N, L) bayt, L — blok uzunligiga (32 yoki 16) karrali; keys: (N, 32 yoki 16) bayt; natija (N, bl) bayt."""
    bl = keys.shape[1]; N, L = msgs.shape; nb = L // bl
    blocks = [msgs[:, i * bl:(i + 1) * bl] for i in range(nb)]
    ny = np.zeros((N, bl), dtype=np.int64)
    for n in range(N): ny[n] = list((sum(int.from_bytes(bytes(b[n].tolist()), 'big') for b in blocks) % 2 ** (8 * bl)).to_bytes(bl, 'big'))
    lb = np.tile(np.array(list((L * 8).to_bytes(bl, 'big'))), (N, 1))
    kir = blocks + [lb, ny]; ke = keys.copy(); h = kir[0].copy()
    for i in range(1, len(kir)):
        h0 = h; h, ke = iteration_g(h, kir[i], ke, keys, R_raund); h = h ^ h0
    Rc = np.full(N, 0xC8)
    P = boglash_y(boglash_y(h, np.tile(C1[:bl], (N, 1)), Rc), np.tile(C2[:bl], (N, 1)), Rc)
    return P ^ h

def xesh_bayt_g(xabar: bytes, kalit: bytes, bl=32, R_raund=10) -> bytes:
    m = xabar + b"\x00" * (-len(xabar) % bl) if xabar else b"\x00" * bl
    return bytes(int(v) for v in xesh_g(np.array([list(m)]), np.array([list(kalit[:bl])]), R_raund)[0])
