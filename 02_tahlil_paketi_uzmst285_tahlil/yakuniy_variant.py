"""
Taklif etilgan yakuniy variant (barcha tavsiyalar birgalikda):
  - yutish: Bog‘lash(holat, blok) → SBZ(holat, blok)                         (1-tavsiya + Qo‘sh o‘rniga Bog‘lash)
  - raund: Aralash(holat, kₑ) → Bog‘lash(holat, kₑ) → SurHolat → Bog‘lash(holat, kₑ)   (Qo‘sh o‘rniga Bog‘lash)
  - kalit jadvali: kₑ ← (SurKalit(kₑ) ⊕ RCⱼ) ∨ 1, boshida kₑ ← k ∨ 1         (2-tavsiya: toq kₑ, holatdan mustaqil)
  - 3-tavsiya (T-funksiya xossasini yo‘qotish) Bog‘lash ichidagi S-box orqali bajariladi
  - har bir blokdan keyin oldinga uzatish: holatᵢ = F(holatᵢ₋₁, blokᵢ) ⊕ holatᵢ₋₁   (4-tavsiya)
  - chiqish o‘zgartirishi: h(M) = P(H) ⊕ H, P = Bog‘lash(Bog‘lash(H, C₁), C₂)   (4-tavsiya)
"""
import numpy as np
from algoritm import Cfg, aralash, surholat, surkalit, bzf, to_units, S
from boglash import boglash, juftlash, RC
from yakuniy import P_perm

def iteration_y(holat, blok, ke, k, c, trace=None, rounds=10):
    p = c.p; m = p - 1; R = juftlash(k, p)[:, 0] & 0xFE
    def T(nm, j):
        if trace is not None: trace.append((nm, j, holat.copy(), ke.copy()))
    ke = ke | 1
    holat = boglash(holat, blok, R, p); T('Bog0', 0)
    holat = bzf(holat, blok, c); T('SBZ0', 0)
    for j in range(1, rounds + 1):
        holat = aralash(holat, ke, c); T('Aralash', j)
        holat = boglash(holat, ke, R, p); T('Bog1', j)
        holat = surholat(holat); ke = (surkalit(ke) ^ (RC[j] & m)) | 1; T('Sur', j)
        if j == 8:
            holat = boglash(holat, blok, R, p); T('Bog8', j); holat = bzf(holat, blok, c); T('SBZ8', j)
        else:
            holat = boglash(holat, ke, R, p); T('Bog2', j)
        if j == 9:
            holat = boglash(holat, blok, R, p); T('Bog9', j); holat = bzf(holat, blok, c); T('SBZ9', j)
    return holat, ke

def kirish(msgs, p):
    N, L = msgs.shape; bl = 32 if p == 256 else 16; nb = L // bl
    blocks = [msgs[:, i * bl:(i + 1) * bl] for i in range(nb)]
    ny = np.zeros((N, bl), dtype=np.int64)
    for n in range(N): ny[n] = list((sum(int.from_bytes(bytes(b[n].tolist()), 'big') for b in blocks) % 2 ** (8 * bl)).to_bytes(bl, 'big'))
    lb = np.tile(np.array(list((L * 8).to_bytes(bl, 'big'))), (N, 1))
    return [to_units(b, p) for b in blocks] + [to_units(lb, p), to_units(ny, p)]

def xesh_y(msgs, keys, p=256):
    """msgs: (N,L) bayt (L blok uzunligiga karrali); keys: (N,32 yoki 16) bayt. Natija: (N,32) birliklar."""
    c = Cfg(p, 'sbz'); kir = kirish(msgs, p); k = to_units(keys, p); ke = k.copy(); h = kir[0]
    for i in range(1, len(kir)):
        h0 = h; h, ke = iteration_y(h, kir[i], ke, k, c); h = h ^ h0
    return P_perm(h, p) ^ h

def xesh_bayt(xabar: bytes, kalit: bytes, p=256) -> bytes:
    bl = 32 if p == 256 else 16
    m = xabar + b"\x00" * (-len(xabar) % bl) if xabar else b"\x00" * bl
    h = xesh_y(np.array([list(m)]), np.array([list(kalit[:bl])]), p)[0]
    if p == 16: h = [h[2 * i] << 4 | h[2 * i + 1] for i in range(16)]
    return bytes(int(v) for v in h)
