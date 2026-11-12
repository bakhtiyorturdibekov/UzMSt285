"""
Tavsiyalar bo‘yicha o‘zgartirilgan 1-algoritm variantlari (vektorlashtirilgan).
  bz    : 'std' (BaytZichlash) yoki 'sbz' (S(h ⊕ S(n)))      — 1-tavsiya
  toq   : True — kₑ elementlari doim toq (kₑ ← kₑ ∨ 1)         — 2-tavsiya
  sqatlam: True — raund ichida S-box qatlami (SurHolat dan keyin) — 3-tavsiya
"""
import numpy as np
from algoritm import Cfg, aralash, qosh, surholat, surkalit, tuz, bzf, S, to_units

PRESENT = np.array([0xC, 5, 6, 0xB, 9, 0, 0xA, 0xD, 3, 0xE, 0xF, 8, 4, 7, 1, 2])

def s_qatlam(h, p):
    return S[h] if p == 256 else PRESENT[h]

def iteration_v(holat, blok, ke, k, c, toq=False, sqatlam=False, trace=None, rounds=10):
    R = k[:, 0]
    def T(nm, j):
        if trace is not None: trace.append((nm, j, holat.copy(), ke.copy()))
    if toq: ke = ke | 1
    holat, hn = qosh(holat, blok, R, c); T('Qosh0', 0)
    holat = bzf(holat, hn, c); T('BZ0', 0)
    for j in range(1, rounds + 1):
        holat = aralash(holat, ke, c); T('Aralash', j)
        holat, ke = qosh(holat, ke, R, c); T('Qosh1', j)
        holat = surholat(holat); ke = surkalit(ke); T('Sur', j)
        if sqatlam: holat = s_qatlam(holat, c.p); T('Sqatlam', j)
        if j == 8:
            holat, hn = qosh(holat, blok, R, c); holat = bzf(holat, hn, c); T('BZ8', j)
        else:
            holat, ke = qosh(holat, ke, R, c); T('Qosh2', j)
        ke = (ke | 1) if toq else tuz(ke, k, c); T('Tuz', j)
        if j == 9:
            holat, hn = qosh(holat, blok, R, c); holat = bzf(holat, hn, c); T('BZ9', j)
    return holat, ke

def xesh_v(xabar: bytes, kalit: bytes, p=256, bz='sbz', toq=False, sqatlam=False) -> bytes:
    c = Cfg(p, bz); bl = 32 if p == 256 else 16
    bits = len(xabar) * 8
    m = xabar + b"\x00" * (-len(xabar) % bl) if xabar else b"\x00" * bl
    bloks = [np.array(list(m[i:i + bl])) for i in range(0, len(m), bl)]
    ny = sum(int.from_bytes(bytes(b.tolist()), 'big') for b in bloks) % 2 ** (8 * bl)
    kir = [to_units(b, p) for b in bloks] + [to_units(np.array(list(bits.to_bytes(bl, 'big'))), p),
                                             to_units(np.array(list(ny.to_bytes(bl, 'big'))), p)]
    k = to_units(np.array(list(kalit[:bl])), p)[None]; ke = k.copy(); h = kir[0][None]
    for i in range(1, len(kir)):
        h, ke = iteration_v(h, kir[i][None], ke, k, c, toq, sqatlam)
    h = h[0]
    if p == 16: h = [h[2 * i] << 4 | h[2 * i + 1] for i in range(16)]
    return bytes(int(v) for v in h)

def xesh_v4(msgs, keys, p=256, bz='sbz', toq=True, sqatlam=True, dm=True, omega=True):
    """4-tavsiya bilan: har bir blokdan keyin oldinga uzatish (dm) va chiqish o‘zgartirishi P(H) ⊕ H (omega).
    msgs: (N,L) bayt, keys: (N,32 yoki 16) bayt."""
    from yakuniy import P_perm
    c = Cfg(p, bz); N, L = msgs.shape; bl = 32 if p == 256 else 16; nb = L // bl
    blocks = [msgs[:, i * bl:(i + 1) * bl] for i in range(nb)]
    ny = np.zeros((N, bl), dtype=np.int64)
    for n in range(N): ny[n] = list((sum(int.from_bytes(bytes(b[n].tolist()), 'big') for b in blocks) % 2 ** (8 * bl)).to_bytes(bl, 'big'))
    lb = np.tile(np.array(list((L * 8).to_bytes(bl, 'big'))), (N, 1))
    kir = [to_units(b, p) for b in blocks] + [to_units(lb, p), to_units(ny, p)]
    k = to_units(keys, p); ke = k.copy(); h = kir[0]
    for i in range(1, len(kir)):
        h0 = h; h, ke = iteration_v(h, kir[i], ke, k, c, toq, sqatlam)
        if dm: h = h ^ h0
    return P_perm(h, p) ^ h if omega else h
