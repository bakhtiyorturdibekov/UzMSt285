"""
Bog‘lash orqali faol S-box larning minimal sonini hisoblash (differensial va chiziqli chegaralar).
Differensial model (bayt darajasidagi qisqartirilgan ayirmalar, bitta kalit — X da ayirma yo‘q):
  yarim qadam T ← f(U): aᵢ uchun S faol, agar (i ∈ A_U) yoki ΔJ ≠ 0; bᵢ uchun S faol, agar (i+1) ∈ A_U (ΔK = 0 tanlanadi);
  |A_U| = 1 bo‘lsa ΔJ ≠ 0 majburiy (bitta baytning modul ayirmasi nol emas), |A_U| ≥ 2 da ΔJ = 0 tanlanishi mumkin;
  parametrlari o‘zgarmagan element: chiqish S faol ⇔ T[i] faol; parametrlari o‘zgargan element: chiqish faol yoki nofaol (buzg‘unchi tanlaydi).
  Har bir faol S-box: p ≤ 2⁻⁶. Chiziqli model: niqob faqat T elementlari orqali o‘tkaziladi (eng arzon yo‘l), har bir faol S-box: |c| ≤ 2⁻³.
"""
import numpy as np, itertools, json

def yarim_qadam(AU, AT, m):
    """AU, AT: bitmaskalar (m bit). Natija: [(narx, yangi_AT), ...] — buzg‘unchi tanlashi mumkin bo‘lgan barcha variantlar."""
    k = bin(AU).count('1'); full = (1 << m) - 1
    rot = lambda x: ((x >> 1) | ((x & 1) << (m - 1)))          # b_i U[i+1] ga bog‘liq: i+1 ∈ A_U ⇔ i ∈ rot(AU)
    variantlar = []
    for dJ in ([True] if k == 1 else ([False, True] if k >= 2 else [False])):
        Pa = full if dJ else AU                                   # a parametri o‘zgargan elementlar
        Pb = rot(AU)
        nS = bin(Pa).count('1') + bin(Pb).count('1')
        P = Pa | Pb
        majburiy = AT & ~P                                        # parametr o‘zgarmagan, T faol -> chiqish faol
        ixtiyoriy = P                                             # parametr o‘zgargan -> buzg‘unchi tanlaydi
        variantlar.append((nS, majburiy, ixtiyoriy))
    return variantlar

def min_chaqiruv(m, maxw=None, maxsub=None):
    """Bitta Bog‘lash chaqiruvidagi faol S-box larning minimal soni (barcha noldan farqli kirishlar bo‘yicha).
    Dinamik dasturlash: holat = (A_L, A_R) bitmaskalar; uchta yarim qadam."""
    full = (1 << m) - 1; INF = 10 ** 9
    def qadam(dist, nishon_ong):
        new = {}
        for (AL, AR), c in dist.items():
            AU, AT = (AL, AR) if nishon_ong else (AR, AL)
            for nS, maj, ixt in yarim_qadam(AU, AT, m):
                if maxsub is None:
                    subs = []; sub = ixt
                    while True:
                        subs.append(sub)
                        if sub == 0: break
                        sub = (sub - 1) & ixt
                else:                                             # faqat kichik qism to‘plamlar (≤ maxsub element)
                    bits = [1 << i for i in range(m) if (ixt >> i) & 1]
                    subs = [sum(c_) for w in range(maxsub + 1) for c_ in itertools.combinations(bits, w)]
                for sub in subs:                                  # ixtiyoriy elementlarning qism to‘plamlari
                    nAT = maj | sub
                    cost = c + nS + bin(nAT).count('1')
                    key = (AL, nAT) if nishon_ong else (nAT, AR)
                    if cost < new.get(key, INF): new[key] = cost
        return new
    start = {}
    if maxw is None:
        for AL in range(1 << m):
            for AR in range(1 << m):
                if AL or AR: start[(AL, AR)] = 0
    else:
        for w in range(1, maxw + 1):
            for pos in itertools.combinations(range(2 * m), w):
                AL = sum(1 << q for q in pos if q < m); AR = sum(1 << (q - m) for q in pos if q >= m); start[(AL, AR)] = 0
    d = qadam(start, True); d = qadam(d, False); d = qadam(d, True)
    d = {k: v for k, v in d.items() if k != (0, 0)}
    return min(d.values())

# ---------------- Chiziqli: niqoblar zanjiri (0-qatlam modeli, Aralash toq kₑ bilan, raundlar bo‘yicha) ----------------
def chiziqli_zanjir(rejim=256, raundlar=4, maxw=2):
    """Niqob bayt to‘plami sifatida. Bog‘lash narxi: o‘ng yarim bayti 2 ta (3- va 1-yarim qadam), chap yarim bayti 1 ta faol S.
    Aralash: 0-qatlam bo‘yicha M(1)ᵀ, SurHolat — o‘rin almashtirish. 128 bitli rejimda Aralash yarim baytlarda, Bog‘lash baytlarda."""
    from komponentlar import M_aralash, P_SUR
    M = M_aralash(np.ones(32, dtype=np.int64)) % 2; P = P_SUR % 2
    if rejim == 256:
        bayt = lambda e: e; nb = 32; chap = lambda j: (j % 8) < 4
    else:
        bayt = lambda e: e // 2; nb = 16; chap = lambda j: (j % 4) < 2
    def narx(v):          # v: 32 ta element bo‘yicha niqob (0/1)
        B = set(bayt(e) for e in np.nonzero(v)[0]); return sum(1 if chap(j) else 2 for j in B)
    best = {r: 10 ** 9 for r in range(1, raundlar + 1)}
    for w in range(1, maxw + 1):
        for pos in itertools.combinations(range(32), w):
            v = np.zeros(32, dtype=np.int64); v[list(pos)] = 1; tot = 0
            for r in range(1, raundlar + 1):           # oxiridan orqaga: Bog2, SurHolat⁻¹, Bog1, Aralashᵀ
                tot += narx(v); v = (P.T @ v) % 2; tot += narx(v); best[r] = min(best[r], tot); v = (M.T @ v) % 2
    return best

def min_chaqiruv_olcham(m):
    """O‘lchamlar bo‘yicha (ruxsat etilgan barcha variantlarning ustki to‘plami) — har qanday m uchun isbotlangan quyi chegara.
    U yarmida k ta faol bayt: parametrlar S-boxlari ≥ s(k) (s(0)=0, s(1)=m, s(k≥2)=2k), o‘zgargan parametrli elementlar ≤ |P|
    (|P| ≤ m agar k=1, aks holda ≤ 2k); yangi T o‘lchami [max(0, t−|P|), min(m, t+|P|)] oralig‘ida (buzg‘unchi tanlaydi)."""
    INF = 10 ** 9
    s = lambda k: 0 if k == 0 else (m if k == 1 else 2 * k)
    Pm = lambda k: 0 if k == 0 else (m if k == 1 else min(m, 2 * k))
    def qadam(dist, ong):
        new = {}
        for (l, r), c in dist.items():
            k, t = (l, r) if ong else (r, l)
            lo, hi = max(0, t - Pm(k)), min(m, t + Pm(k))
            for nt in range(lo, hi + 1):
                cost = c + s(k) + nt; key = (l, nt) if ong else (nt, r)
                if cost < new.get(key, INF): new[key] = cost
        return new
    d = {(l, r): 0 for l in range(m + 1) for r in range(m + 1) if l or r}
    d = qadam(d, True); d = qadam(d, False); d = qadam(d, True)
    return min(v for k, v in d.items() if k != (0, 0))

def chiziqli_zanjir_yagona(bl=32, raundlar=6, maxw=2):
    """Yagona variant uchun chiziqli zanjir (bayt darajasi): bl = 32 — 4×8 (ikki 4×4 Aralash), bl = 16 — 4×4."""
    from algoritm import dia
    if bl == 32:
        from komponentlar import M_aralash, P_SUR
        M = M_aralash(np.ones(32, dtype=np.int64)) % 2; P = P_SUR % 2; chap = lambda j: (j % 8) < 4
    else:
        from yagona import _sur4
        E = np.eye(16, dtype=np.int64).reshape(16, 4, 4); M = (dia(E, np.ones((16, 4, 4), dtype=np.int64), 2).reshape(16, 16).T) % 2
        P = np.zeros((16, 16), dtype=np.int64)
        for i in range(16):
            v = np.zeros((1, 16), dtype=np.int64); v[0, i] = 1; P[:, i] = _sur4(v, [1, 2, 3, 0], {0: 1, 1: 2, 2: 3, 3: 0})[0]
        chap = lambda j: (j % 4) < 2
    narx = lambda v: sum(1 if chap(j) else 2 for j in np.nonzero(v)[0])
    best = {r: 10 ** 9 for r in range(1, raundlar + 1)}
    for w in range(1, maxw + 1):
        for pos in itertools.combinations(range(bl), w):
            v = np.zeros(bl, dtype=np.int64); v[list(pos)] = 1; tot = 0
            for r in range(1, raundlar + 1):
                tot += narx(v); v = (P.T @ v) % 2; tot += narx(v); best[r] = min(best[r], tot); v = (M.T @ v) % 2
    return best
