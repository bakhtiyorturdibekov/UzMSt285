"""
Bog‘lash(holat, X) — Qo‘sh o‘rniga taklif etilayotgan yagona akslantirish (256 va 128 bitli rejimlar uchun bir xil).
Ikkala rejimda ham bayt darajasida ishlaydi: 128 bitli rejimda qo‘shni yarim baytlar juftlab baytga birlashtiriladi
(SBZ dagi kabi), so‘ng natija yana yarim baytlarga ajratiladi.
  Yarim qadam (T ← f(U)):  J = Σ U,  K = Π (U ∨ 1)  (mod 256)
      aᵢ = 2·S(U[i] ⊕ X_U[i] ⊕ J) + 1,   bᵢ = 2·S(U[i+1] ⊕ X_T[i] ⊕ K) + 1
      T[i] ← S( −aᵢ·T[i]·(bᵢ + R·T[i])⁻¹ ⊕ X_T[i] )        (R — kalitning birinchi bayti, juft)
  Bog‘lash: o‘ng ← f(chap), chap ← f(o‘ng), o‘ng ← f(chap).
"""
import numpy as np
from algoritm import S, Cfg, aralash, surholat, surkalit, bzf, to_units

INV = np.zeros(256, dtype=np.int64)
for _x in range(1, 256, 2): INV[_x] = pow(_x, -1, 256)
SI = np.zeros(256, dtype=np.int64); SI[S] = np.arange(256)

def juftlash(u, p):      # birliklar -> baytlar
    return u if p == 256 else 16 * u[:, 0::2] + u[:, 1::2]
def ajratish(b, p):      # baytlar -> birliklar
    if p == 256: return b
    u = np.empty((b.shape[0], 32), dtype=np.int64); u[:, 0::2] = b >> 4; u[:, 1::2] = b & 15; return u
def yarimlar(m):         # m = 32 yoki 16 bayt; satrda w bayt; chap yarim — satrning birinchi yarmi
    w = 8 if m == 32 else 4
    i = np.arange(m); return i[(i % w) < w // 2], i[(i % w) >= w // 2]

def _param(U, XT, XU):
    J = U.sum(1) % 256; K = np.ones(U.shape[0], dtype=np.int64)
    for i in range(U.shape[1]): K = (K * (U[:, i] | 1)) % 256
    sig = np.roll(np.arange(U.shape[1]), -1)
    a = (2 * S[U ^ XU ^ J[:, None]] + 1) % 256
    b = (2 * S[U[:, sig] ^ XT ^ K[:, None]] + 1) % 256
    return a, b
def _yarim(T, U, XT, XU, R):
    a, b = _param(U, XT, XU)
    return S[((-a * T * INV[(b + R[:, None] * T) % 256]) % 256) ^ XT]
def _yarim_inv(Y, U, XT, XU, R):
    a, b = _param(U, XT, XU); f = SI[Y] ^ XT
    return (-b * f * INV[(a + R[:, None] * f) % 256]) % 256

def boglash(holat, X, R, p):
    """holat, X: (N,32) birliklar; R: (N,) juft bayt. Natija: (N,32) birliklar."""
    H = juftlash(holat, p).copy(); Xb = juftlash(X, p); L, Rt = yarimlar(H.shape[1])
    H[:, Rt] = _yarim(H[:, Rt], H[:, L], Xb[:, Rt], Xb[:, L], R)
    H[:, L] = _yarim(H[:, L], H[:, Rt], Xb[:, L], Xb[:, Rt], R)
    H[:, Rt] = _yarim(H[:, Rt], H[:, L], Xb[:, Rt], Xb[:, L], R)
    return ajratish(H, p)
def boglash_inv(Y, X, R, p):
    H = juftlash(Y, p).copy(); Xb = juftlash(X, p); L, Rt = yarimlar(H.shape[1])
    H[:, Rt] = _yarim_inv(H[:, Rt], H[:, L], Xb[:, Rt], Xb[:, L], R)
    H[:, L] = _yarim_inv(H[:, L], H[:, Rt], Xb[:, L], Xb[:, Rt], R)
    H[:, Rt] = _yarim_inv(H[:, Rt], H[:, L], Xb[:, Rt], Xb[:, L], R)
    return ajratish(H, p)

RC = np.array([[int(S[(16 * j + i) % 256]) for i in range(32)] for j in range(11)])   # raund konstantalari

def iteration_b(holat, blok, ke, k, c, sbz=True, rounds=10, trace=None):
    """Yangi variant: Qo‘sh -> Bog‘lash; yutish: Bog‘lash(holat, blok) [-> SBZ(holat, blok)];
    kalit jadvali holatdan mustaqil: kₑ ← (SurKalit(kₑ) ⊕ RC_j) ∨ 1."""
    p = c.p; R = juftlash(k, p)[:, 0] & 0xFE; m = p - 1
    def yut(h):
        h = boglash(h, blok, R, p)
        return bzf(h, blok, c) if sbz else h
    ke = ke | 1
    holat = yut(holat)
    for j in range(1, rounds + 1):
        holat = aralash(holat, ke, c)
        holat = boglash(holat, ke, R, p)
        holat = surholat(holat); ke = (surkalit(ke) ^ (RC[j] & m)) | 1
        holat = yut(holat) if j == 8 else boglash(holat, ke, R, p)
        if j == 9: holat = yut(holat)
        if trace is not None: trace.append((j, holat.copy(), ke.copy()))
    return holat, ke

def xesh_b(msgs, keys, p, sbz=True):
    """msgs: (N,L) bayt (L blok uzunligiga karrali), keys: (N,32 yoki 16) bayt."""
    c = Cfg(p, 'sbz'); N, L = msgs.shape; bl = 32 if p == 256 else 16; nb = L // bl
    blocks = [msgs[:, i * bl:(i + 1) * bl] for i in range(nb)]
    ny = np.zeros((N, bl), dtype=np.int64)
    for n in range(N):
        v = sum(int.from_bytes(bytes(b[n].tolist()), 'big') for b in blocks) % 2 ** (8 * bl); ny[n] = list(v.to_bytes(bl, 'big'))
    lb = np.tile(np.array(list((L * 8).to_bytes(bl, 'big'))), (N, 1))
    kir = [to_units(b, p) for b in blocks] + [to_units(lb, p), to_units(ny, p)]
    k = to_units(keys, p); ke = k.copy(); holat = kir[0]
    for i in range(1, len(kir)): holat, ke = iteration_b(holat, kir[i], ke, k, c, sbz)
    return holat
