from builder import setup_cell
C = []
md = lambda s: C.append(('markdown', s.strip('\n')))
code = lambda s: C.append(('code', s.strip('\n')))

md("""
# O‘zMSt 285:2024, 1-algoritm: 2- va 3-tavsiyalarni amalga oshirish va tekshirish

**2-tavsiya.** Aralash va TuzilmaKalit: diamatritsa 2 moduli bo‘yicha har doim teskarilanuvchi bo‘lishi uchun
raund kaliti kₑ ning barcha elementlari toq qilinadi (kₑ ← kₑ ∨ 1).

**3-tavsiya.** Raund funksiyasiga yuqori bitlarni quyi bitlarga o‘tkazuvchi element qo‘shiladi
(SurHolat dan keyin, ikkinchi Qo‘sh dan oldin): davriy aylantirish, XOR-surish yoki S-box qatlami.

Daftar mustaqil: kerakli modullar 0-hujayrada yuklanadi. Faqat `numpy` kerak.
`TEZ = True` qilinsa, tanlanmalar kichraytiriladi (tez sinov uchun).
""")
C.append(setup_cell(['algoritm', 'komponentlar', 'differensial', 'variant']))
code(r'''
import numpy as np, itertools, json, time
from algoritm import *
from komponentlar import *
from variant import xesh_v, iteration_v, PRESENT
TEZ = False                      # True — tez sinov (kichik tanlanmalar)
K_ = (lambda n: max(1, n // 5)) if TEZ else (lambda n: n)
R = {}
print("Nazorat qiymatlari (standart va SBZ):", "hammasi mos" if nazorat() else "XATO")
# Tavsiyalar bo‘yicha variantlarning nazorat qiymatlari (A ilova kaliti va xabari)
VAR = [('std', False, False), ('sbz', False, False), ('std', True, False), ('std', False, True), ('sbz', True, False), ('sbz', True, True)]
R['KAT'] = {}
for p in (256, 16):
    for bz, toq, sq in VAR:
        h = xesh_v(KAT_XABAR, KAT_KALIT, p, bz, toq, sq).hex()
        R['KAT'][f"{p}_{bz}_{int(toq)}_{int(sq)}"] = h
        print(f"p={p:3d}  bz={bz}  toq kₑ={int(toq)}  S-qatlam={int(sq)}:  {h}")
''')

md("""
## 1. 2-tavsiya: kₑ ning juft/toqlik naqshi

Aralash 2 moduli bo‘yicha faqat kₑ elementlarining juft/toqligiga bog‘liq chiziqli akslantirish M(k₀).
Har bir 4×4 yarim uchun barcha 2¹⁶ naqsh tekshiriladi: qaysilarida yarim matritsa teskarilanuvchi va
ularning tarmoqlanish soni (min wt(x) + wt(Mx)) qancha.
""")
code(r'''
from algoritm import dia
def M_yarim(bitlar):
    K = np.array(bitlar, dtype=np.int64).reshape(4, 4)
    E = np.eye(16, dtype=np.int64).reshape(16, 4, 4)
    return (dia(E, np.tile(K, (16, 1, 1)), 2).reshape(16, 16).T) % 2
asos = [M_yarim([1 if i == b else 0 for i in range(16)]) for b in range(16)]   # M(K) K ga nisbatan chiziqli
def M_of(p_):
    M = np.zeros((16, 16), dtype=np.int64)
    for b in range(16):
        if (p_ >> b) & 1: M ^= asos[b]
    return M
w2 = 1 << np.arange(16)
def rang_bit(rows):
    rows = list(rows); r = 0
    for b in range(16):
        piv = next((i for i in range(r, len(rows)) if (rows[i] >> b) & 1), None)
        if piv is None: continue
        rows[r], rows[piv] = rows[piv], rows[r]
        for i in range(len(rows)):
            if i != r and (rows[i] >> b) & 1: rows[i] ^= rows[r]
        r += 1
    return r
invs = [p_ for p_ in range(65536) if rang_bit((M_of(p_) * w2).sum(1)) == 16]
pc = np.array([bin(i).count('1') for i in range(65536)])
def tarmoqlanish(p_):
    cols = (M_of(p_) * w2[:, None]).sum(0); lo = np.zeros(256, dtype=np.int64); hi = np.zeros(256, dtype=np.int64)
    for x in range(1, 256):
        b = (x & -x).bit_length() - 1; lo[x] = lo[x & (x - 1)] ^ cols[b]; hi[x] = hi[x & (x - 1)] ^ cols[b + 8]
    img = (hi[:, None] ^ lo[None, :]).reshape(-1); return int((pc + pc[img])[1:].min())
br = {p_: tarmoqlanish(p_) for p_ in invs}
from collections import Counter
taq = dict(sorted(Counter(br.values()).items())); eng = [p_ for p_, b in br.items() if b == max(taq)]
print(f"Teskarilanuvchi naqshlar: {len(invs)} / 65536 = {len(invs)/65536:.3f}")
print("Tarmoqlanish soni bo‘yicha taqsimot:", taq)
print("Eng katta tarmoqlanishli naqsh(lar):", [hex(p_) for p_ in eng], "— 0xffff = barcha elementlar toq")
R['naqsh'] = dict(teskarilanuvchi=len(invs), taqsimot={str(k): v for k, v in taq.items()}, eng=[hex(p_) for p_ in eng])
''')

md("""
### 1.1. Toq kₑ bilan L = P·M matritsasi va faol baytlar zanjiri
""")
code(r'''
Lf = (P_SUR @ M_aralash(np.ones(32, dtype=np.int64))) % 2
print(f"rang L = {rank2(Lf)},  nol satrlar = {int((Lf.sum(1)==0).sum())},  nol ustunlar = {int((Lf.sum(0)==0).sum())}")
def zanjir(Lm, wmax=2):
    L8 = np.linalg.matrix_power(Lm, 8) % 2; maps = [L8, Lm, Lm, L8, Lm]; best = {k: 99 for k in range(1, 7)}
    cands = [np.eye(32, dtype=np.int64)[list(c)].sum(0) % 2 for w in range(1, wmax + 1) for c in itertools.combinations(range(32), w)]
    for end in range(1, 6):
        for u in cands:
            tot = int(u.sum()); cur = u; n = 1; best[1] = min(best[1], tot)
            for m in range(end - 1, -1, -1):
                cur = (maps[m].T @ cur) % 2
                if cur.sum() == 0: break
                tot += int(cur.sum()); n += 1; best[n] = min(best[n], tot)
    return best
zf = zanjir(Lf)
rng = np.random.default_rng(9); zs = {k: [] for k in range(1, 7)}
for t in range(K_(60)):
    zz = zanjir(L_raund(kalitlar(rng, 1, 256)[0]))
    for k_ in zz:
        if zz[k_] < 99: zs[k_].append(zz[k_])
print("Yutish qatlamlari:      ", list(range(1, 7)))
print("Hozirgi: minimum        ", [min(zs[k_]) for k_ in range(1, 7)])
print("Hozirgi: mediana        ", [float(np.median(zs[k_])) for k_ in range(1, 7)])
print("Toq kₑ (har qanday kalit)", [zf[k_] for k_ in range(1, 7)])
R['L_toq'] = dict(rang=rank2(Lf), zanjir_toq=[zf[k_] for k_ in range(1, 7)],
                  zanjir_hozirgi_min=[min(zs[k_]) for k_ in range(1, 7)], zanjir_hozirgi_med=[float(np.median(zs[k_])) for k_ in range(1, 7)])
''')

md("""
### 1.2. Chiqishdagi munosabatlar, doimiy bitlar va ayirmalarning so‘nishi

Hozirgi va toq kₑ li algoritm solishtiriladi: (a) 1000 ta xesh qiymatning 0-qatlami vektorlari fazosining rangi
(32 bo‘lsa, doimiy munosabatlar yo‘q) va har bir bitning chastotasi; (b) yutishdan keyingi holatdagi bitta MSB
ayirmasining raundlarda butunlay so‘nish ulushi va MSB izining saqlanishi.
""")
code(r'''
def raundlar(h, bl, ke, k, c, toq=False, E=None, nr=10, trace=None):
    """0-nuqtadagi yutishsiz 1..nr raundlar; E — raund ichidagi qo‘shimcha element (SurHolat dan keyin)."""
    Rr = k[:, 0]
    if toq: ke = ke | 1
    for j in range(1, nr + 1):
        h = aralash(h, ke, c); h, ke = qosh(h, ke, Rr, c); h = surholat(h); ke = surkalit(ke)
        if E is not None: h = E(h)
        if j == 8: h, hn = qosh(h, bl, Rr, c); h = bzf(h, hn, c)
        else: h, ke = qosh(h, ke, Rr, c)
        ke = (ke | 1) if toq else tuz(ke, k, c)
        if j == 9: h, hn = qosh(h, bl, Rr, c); h = bzf(h, hn, c)
        if trace is not None: trace.append((j, h.copy(), ke.copy()))
    return h, ke
R['chiqish'] = {}; R['sonish'] = {}
rng = np.random.default_rng(71)
for p in (256, 16):
    for toq in (False, True):
        ranks, fmin, fmax = [], 1, 0
        for t in range(3):
            if p == 256: k = kalitlar(rng, 1, 256)[0]
            else: k = rng.integers(0, 256, 16); k[0] &= 0xEE
            m = rng.integers(0, 256, (K_(1000), 64)); o = np.array([list(xesh_v(bytes(mm.tolist()), bytes(k.tolist()), p, 'std', toq, False)) for mm in m[:K_(400)]])
            ob = (to_units(o, p) % 2); ranks.append(rank2((ob[1:] ^ ob[0]).T.copy())); f = ob.mean(0); fmin = min(fmin, f.min()); fmax = max(fmax, f.max())
        R['chiqish'][f'{p}_{int(toq)}'] = dict(rang=ranks, chastota=[round(float(fmin), 3), round(float(fmax), 3)])
        print(f"p={p:3d}, toq kₑ={int(toq)}: 0-qatlam rangi {ranks},  bit chastotalari {fmin:.3f}…{fmax:.3f}")
for p in (256, 16):
    for toq in (False, True):
        c = Cfg(p, 'std'); N = K_(3000); msb = p // 2; k = kalitlar(rng, N, p)
        h = rng.integers(0, p, (N, 32)); bl = rng.integers(0, p, (N, 32)); h2 = h.copy(); h2[:, 0] ^= msb
        t1, t2 = [], []; raundlar(h, bl, k.copy(), k, c, toq, trace=t1); raundlar(h2, bl, k.copy(), k, c, toq, trace=t2)
        z = [round(float(((a[1] == b[1]).all(1) & (a[2] == b[2]).all(1)).mean()), 4) for a, b in zip(t1, t2)]
        mi = [round(float((((a[1] ^ b[1]) == 0) | ((a[1] ^ b[1]) == msb)).all(1).mean()), 3) for a, b in zip(t1, t2)]
        R['sonish'][f'{p}_{int(toq)}'] = dict(nol=z, msb=mi)
        print(f"p={p:3d}, toq kₑ={int(toq)}: so‘nish ulushi {z[:3]} …;  MSB izi {mi[:7]}")
''')

md("""
## 2. 3-tavsiya: raund ichidagi T-funksiyani buzuvchi element

Uchta element SurHolat dan keyin holatning har bir elementiga qo‘llanadi va hozirgi algoritm bilan solishtiriladi:
- 0-qatlam raund tenglamasi h₀ ← L·h₀ ning korrelyatsiyasi (raundlar bo‘yicha);
- 1 raund: eng yaxshi «bitta bit → bitta bit» korrelyatsiyasi (shovqin chegarasi bilan);
- MSB izining saqlanishi;
- ko‘chki (SAC): 1 va 2 raunddan keyin o‘rtacha qiymat va bog‘liqligi yo‘q (kirish, chiqish) bit juftliklari ulushi;
- MSB ning 0-bitga ta’siri (1 va 2 raund);
- integral: bitta faol bayt bo‘yicha 0-qatlam yig‘indisi nol bo‘lish ulushi (1–3-raund);
- hisoblash vaqti.
""")
code(r'''
def element(nom, p):
    if nom == 'yoq': return None
    if p == 256:
        return {'aylantirish': lambda h: ((h << 3) | (h >> 5)) & 255, 'xor_surish': lambda h: h ^ (h >> 4), 'sbox': lambda h: S[h]}[nom]
    return {'aylantirish': lambda h: ((h << 1) | (h >> 3)) & 15, 'xor_surish': lambda h: h ^ (h >> 2), 'sbox': lambda h: PRESENT[h]}[nom]
def bitlar(a, p):
    nb = 8 if p == 256 else 4
    return ((a[:, :, None] >> np.arange(nb)) & 1).reshape(len(a), -1)
R['element'] = {}
rng = np.random.default_rng(81)
for p in (256, 16):
    c = Cfg(p, 'std'); msb = p // 2; nb = 8 if p == 256 else 4
    for nom in ('yoq', 'aylantirish', 'xor_surish', 'sbox'):
        E = element(nom, p); r = {}
        N = K_(600); k = kalitlar(rng, N, p); h = rng.integers(0, p, (N, 32)); bl = rng.integers(0, p, (N, 32)); tr = []
        raundlar(h, bl, k.copy(), k, c, False, E, trace=tr)
        Ls = [L_raund(k[n]) for n in range(N)]; cur = h % 2; cl = []
        for j, hh, kk in tr:
            cur = np.array([(Ls[n] @ cur[n]) % 2 for n in range(N)]); cl.append(round(2 * float((cur == hh % 2).mean()) - 1, 3))
        r['qatlam0_c'] = cl
        N = K_(6000); k = kalitlar(rng, N, p); h = rng.integers(0, p, (N, 32)); bl = rng.integers(0, p, (N, 32))
        o, _ = raundlar(h, bl, k.copy(), k, c, False, E, nr=1)
        X = 1 - 2 * bitlar(h, p).astype(float); Y = 1 - 2 * bitlar(o, p).astype(float)
        r['bit_bit'] = round(float((np.abs(Y.T @ X) / N).max()), 3); r['shovqin'] = round(4.5 / np.sqrt(N), 3)
        N = K_(2000); k = kalitlar(rng, N, p); h = rng.integers(0, p, (N, 32)); bl = rng.integers(0, p, (N, 32)); h2 = h.copy(); h2[:, 0] ^= msb
        t1, t2 = [], []; raundlar(h, bl, k.copy(), k, c, False, E, trace=t1); raundlar(h2, bl, k.copy(), k, c, False, E, trace=t2)
        r['msb_izi'] = [round(float(((((a[1] ^ b[1]) == 0) | ((a[1] ^ b[1]) == msb)).all(1) & (((a[2] ^ b[2]) == 0) | ((a[2] ^ b[2]) == msb)).all(1)).mean()), 3) for a, b in zip(t1, t2)]
        for nr in (1, 2):
            N = K_(300); k = kalitlar(rng, N, p); h = rng.integers(0, p, (N, 32)); bl = rng.integers(0, p, (N, 32))
            o, _ = raundlar(h, bl, k.copy(), k, c, False, E, nr=nr); ob = bitlar(o, p); SAC = np.zeros((32 * nb, 32 * nb))
            for i in range(32 * nb):
                h2 = h.copy(); h2[:, i // nb] ^= (1 << (i % nb)); o2, _ = raundlar(h2, bl, k.copy(), k, c, False, E, nr=nr)
                SAC[i] = (ob ^ bitlar(o2, p)).mean(0)
            hi = [i for i in range(32 * nb) if i % nb == nb - 1]; lo = [i for i in range(32 * nb) if i % nb == 0]
            r[f'sac{nr}'] = dict(ortacha=round(float(SAC.mean()), 3), nol=round(float((SAC == 0).mean()), 3), min=round(float(SAC.min()), 3))
            r[f'msb_0bit{nr}'] = round(float(SAC[np.ix_(hi, lo)].mean()), 3)
        zf_ = []
        for t in range(K_(60)):
            k = kalitlar(rng, 1, p)[0]; h = rng.integers(0, p, 32); bl = rng.integers(0, p, 32)
            H = np.tile(h, (p, 1)); H[:, 0] = np.arange(p); Kk = np.tile(k, (p, 1)); tr = []
            raundlar(H, np.tile(bl, (p, 1)), Kk.copy(), Kk, c, False, E, nr=3, trace=tr)
            zf_.append([float(((np.bitwise_xor.reduce(hh, axis=0) & 1) == 0).mean()) for j, hh, kk in tr])
        r['integral0'] = [round(float(v), 2) for v in np.mean(zf_, 0)]
        N = K_(2000); k = kalitlar(rng, N, p); h = rng.integers(0, p, (N, 32)); bl = rng.integers(0, p, (N, 32))
        t0 = time.perf_counter(); raundlar(h, bl, k.copy(), k, c, False, E); r['vaqt'] = round(time.perf_counter() - t0, 3)
        R['element'][f'{p}_{nom}'] = r
        print(f"p={p:3d} {nom:12s} 0-qatlam c: {cl[:3]}  bit→bit: {r['bit_bit']} (shovqin {r['shovqin']})  MSB izi: {r['msb_izi'][:2]}"
              f"  SAC1: {r['sac1']}  SAC2 nol: {r['sac2']['nol']}  MSB→0: {r['msb_0bit1']}/{r['msb_0bit2']}  integral: {r['integral0']}  vaqt: {r['vaqt']}")
''')

md("""
## 3. Uchala tavsiya birgalikda (SBZ + toq kₑ + S-box qatlami)
""")
code(r'''
rng = np.random.default_rng(9); R['birlashgan'] = {}
for p in (256, 16):
    c = Cfg(p, 'sbz'); N = K_(3000); msb = p // 2; k = kalitlar(rng, N, p)
    h = rng.integers(0, p, (N, 32)); bl = rng.integers(0, p, (N, 32)); h2 = h.copy(); h2[:, 0] ^= msb
    E = element('sbox', p); t1, t2 = [], []
    raundlar(h, bl, k.copy(), k, c, True, E, nr=7, trace=t1); raundlar(h2, bl, k.copy(), k, c, True, E, nr=7, trace=t2)
    mi = [round(float((((a[1] ^ b[1]) == 0) | ((a[1] ^ b[1]) == msb)).all(1).mean()), 4) for a, b in zip(t1, t2)]
    z = [round(float(((a[1] == b[1]).all(1) & (a[2] == b[2]).all(1)).mean()), 4) for a, b in zip(t1, t2)]
    R['birlashgan'][str(p)] = dict(msb=mi, nol=z)
    print(f"p={p}: MSB izi (1–7-raund) {mi};  ayirma so‘ngan juftliklar {z}")
json.dump(R, open('tavsiyalar_natijalari.json', 'w'), ensure_ascii=False, indent=1, default=lambda o: o.tolist() if hasattr(o, 'tolist') else int(o))
print("Natijalar tavsiyalar_natijalari.json ga yozildi.")
''')
