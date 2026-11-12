"""Kriptotahlil uchun umumiy yordamchi funksiyalar."""
import itertools
import numpy as np
from algoritm import Cfg, aralash, surholat

PAR8 = np.array([bin(i).count('1') & 1 for i in range(256)])
X256 = np.arange(256)

def kalitlar(rng, N, p):
    """Tasodifiy kalitlar: R (1-element) va 2-element juft (5.1.2-band talabi)."""
    if p == 256:
        k = rng.integers(0, 256, (N, 32)); k[:, 0] &= 0xFE; k[:, 1] &= 0xFE
    else:
        k = rng.integers(0, 16, (N, 32)); k[:, 0] &= 0xE; k[:, 1] &= 0xE
    return k

def wht(f):
    """Walsh–Adamar o‘zgartirishi (f — ±1 vektor)."""
    a = f.astype(np.int64).copy(); h = 1; n = len(a)
    while h < n:
        a = a.reshape(-1, 2, h); a = np.stack([a[:, 0] + a[:, 1], a[:, 0] - a[:, 1]], 1).reshape(-1); h *= 2
    return a

def lat(F, nout):
    """8 bitli kirishli F uchun W[β][α] = Σ (−1)^(β·F(x) ⊕ α·x); korrelyatsiya c = W/256."""
    W = np.zeros((1 << nout, 256), dtype=np.int64)
    for b in range(1 << nout):
        W[b] = wht(1 - 2 * PAR8[F & b])
    return W

def ddt(F, nout):
    """Ayirmalar matritsasi DDT[Δx][Δy] (8 bitli kirish)."""
    return np.array([np.bincount(F ^ F[X256 ^ d], minlength=nout) for d in range(256)])

def anf_deg(fbits, nv):
    """Boolean funksiyaning ANF darajasi (Möbius o‘zgartirishi)."""
    a = fbits.astype(np.uint8).copy(); h = 1; N = 1 << nv
    while h < N:
        a = a.reshape(-1, 2, h); a[:, 1] ^= a[:, 0]; a = a.reshape(-1); h *= 2
    wt = np.array([bin(i).count('1') for i in range(N)]); nz = wt[a == 1]
    return int(nz.max()) if len(nz) else -1

def bits(v, n): return (v[:, None] >> np.arange(n)) & 1

def implicit_count(points, deg):
    """deg darajali chiziqli bog‘liq bo‘lmagan implitsit tenglamalar soni (monomlar matritsasi rangi orqali)."""
    npts, nv = points.shape
    mons = [()] + [m for d in range(1, deg + 1) for m in itertools.combinations(range(nv), d)]
    words = (npts + 63) // 64; cols = []
    for m in mons:
        v = np.ones(npts, dtype=np.uint8)
        for i in m: v &= points[:, i].astype(np.uint8)
        pad = np.zeros(words * 64, dtype=np.uint8); pad[:npts] = v
        cols.append(np.packbits(pad).view(np.uint64))
    A = np.array(cols); rank = 0; n = A.shape[0]
    for w in range(A.shape[1]):
        for b in range(64):
            if rank >= n: break
            mask = np.uint64(1) << np.uint64(b)
            idx = np.nonzero((A[rank:, w] & mask) != 0)[0]
            if len(idx) == 0: continue
            piv = rank + idx[0]
            if piv != rank: A[[rank, piv]] = A[[piv, rank]]
            rows = np.nonzero((A[:, w] & mask) != 0)[0]; rows = rows[rows != rank]
            A[rows] ^= A[rank]; rank += 1
    return len(mons) - rank, len(mons)

def qosh_elem(A1, B1, A2, B2, R, p=256):
    """Qo‘sh o‘zgartirishining bitta elementi (parametrlar belgilangan): x → x^(−3)."""
    x = np.arange(p); INV = np.zeros(p, dtype=np.int64)
    for t in range(1, p, 2): INV[t] = pow(t, -1, p)
    s = lambda x, A, B: (-A * x * INV[(B + R * x) % p]) % p
    y1 = s(x, A1, B1); y2 = s(y1, A2, B2); y2 = np.where(y2 == 0, (A2 + B2) % p, y2)
    return s(y2, A2, B2)

def tasodifiy_param(rng):
    A1, B1, A2, B2 = [int(rng.integers(0, 128)) * 2 + 1 for _ in range(4)]
    return A1, B1, A2, B2, int(rng.integers(0, 128)) * 2

def rank2(A):
    A = A.copy() % 2; r = 0
    for col in range(A.shape[1]):
        piv = [i for i in range(r, A.shape[0]) if A[i, col]]
        if not piv: continue
        A[[r, piv[0]]] = A[[piv[0], r]]
        for i in range(A.shape[0]):
            if i != r and A[i, col]: A[i] ^= A[r]
        r += 1
    return r

# 0-qatlam matritsalari: SurHolat (P) va Aralash (M(k0))
_C2 = Cfg(2, 'std')
_perm = surholat(np.arange(32)[None, :].copy())[0]
P_SUR = np.zeros((32, 32), dtype=np.int64); P_SUR[np.arange(32), _perm] = 1

def M_aralash(k):
    """h0' = M(k0)·h0 (mod 2) matritsasi."""
    E = np.eye(32, dtype=np.int64); K = np.tile(np.asarray(k) % 2, (32, 1))
    return (aralash(E, K, _C2).T) % 2

def L_raund(k):
    """Yutishsiz raundning 0-qatlam matritsasi L = P·M(k0)."""
    return (P_SUR @ M_aralash(k)) % 2
