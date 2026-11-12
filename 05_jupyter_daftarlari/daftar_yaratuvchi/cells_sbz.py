from builder import setup_cell
C = []
md = lambda s: C.append(('markdown', s.strip('\n')))
code = lambda s: C.append(('code', s.strip('\n')))

md("""
# BaytZichlash o‘rniga SBZ qo‘llanilgan 1-algoritmning kriptotahlili

To‘rtta usul: chiziqli, differensial, algebraik va integral. Variantlar: SBZ-256 va SBZ-128
(Aralash, TuzilmaKalit va raund funksiyasi standartdagidek).

Daftar mustaqil ishlaydi: modullar 0-hujayrada yuklanadi, faqat `numpy` kerak.
`HAJM` koeffitsiyenti tanlanmalar hajmini boshqaradi (1 — tez, 4–5 — hisobotdagi hajmga yaqin).
`OGIR = True` qilinsa, to‘liq xesh uchun 2¹⁶ to‘plamli integral sinov ham bajariladi (har bir tajriba bir necha daqiqa).
""")
C.append(setup_cell(['algoritm', 'komponentlar', 'differensial', 'algebraik', 'integral']))
code(r'''
import numpy as np, itertools, math, json, collections
from algoritm import *
from komponentlar import *
import algebraik, integral
from differensial import raundlar_yutishsiz
HAJM = 1          # 1 — tez; kattaroq qiymat tanlanmalarni oshiradi
OGIR = False      # True — to‘liq xesh uchun 2^16 to‘plamli integral sinov
R = {}
print("Nazorat qiymatlari:", "hammasi mos" if nazorat() else "XATO")
''')

md("""
## 1. Chiziqli kriptotahlil
### 1.1. S va SBZ korrelyatsion matritsalari

SBZ uchun c_SBZ((α, β) → γ) = c_S(α → γ) · c_S(β → α). To‘liq taqsimot 255 × 65536 element bo‘yicha hisoblanadi.
""")
code(r'''
WS = lat(S, 8); A = np.abs(WS)
v, c = np.unique(A[1:, :], return_counts=True)
R['S_lat'] = {int(a): int(b) for a, b in zip(v, c)}
print("S: |W| taqsimoti:", R['S_lat'], " maks |c| =", A[1:, :].max() / 256)
cnt = collections.Counter()
for g in range(1, 256):
    for a in range(1, 256):
        if A[g, a]:
            vv, cc = np.unique(A[g, a] * A[a, :], return_counts=True)
            for x, y in zip(vv, cc): cnt[int(x)] += int(y)
cnt[0] = 255 * 65536 - sum(cnt.values())
R['SBZ_lat'] = dict(sorted(cnt.items()))
print("SBZ: maks |c| =", max(k for k in cnt if cnt[k]) / 65536, "= 2^-6;  bunday elementlar soni:", cnt[1024])
print("γ = 01 uchun eng yaxshi approksimatsiyalar (α, β, c):")
for a in np.argsort(-A[1])[:6]:
    b = int(np.argmax(A[a])); print(f"   α = {a:02X}, β = {b:02X}, c = {WS[1, a] * WS[a, b] / 65536:+.6f}")
hh = np.arange(65536) >> 8; nn = np.arange(65536) & 255; y = S[hh ^ S[nn]]
rel = (y & 1) ^ PAR8[hh & 0x2D] ^ PAR8[nn & 0x1A]
print("Tekshiruv: y0 ⊕ <2D,h> ⊕ <1A,n> = 1 ifodasi", int(rel.sum()), "/ 65536 juftlikda 1 ga teng, c =", 1 - 2 * rel.sum() / 65536)
''')

md("""
### 1.2. 0-qatlam raund tenglamasi h₀ ← L·h₀ va yutish qatlamlari bo‘yicha chegara
""")
code(r'''
rng = np.random.default_rng(7); R['lsb'] = {}
for p in (256, 16):
    c = Cfg(p, 'sbz'); N = 300 * HAJM; k = kalitlar(rng, N, p)
    h = rng.integers(0, p, (N, 32)); bl = rng.integers(0, p, (N, 32)); tr = []
    iteration(h, bl, k.copy(), k, c, trace=tr)
    cur = [t for t in tr if t[0] == 'BZ0'][0][2] % 2; Ls = [L_raund(k[n]) for n in range(N)]; cl = []
    for j in range(1, 11):
        cur = np.array([(Ls[n] @ cur[n]) % 2 for n in range(N)]); act = [t for t in tr if t[1] == j][-1][2] % 2
        cl.append(round(2 * float((cur == act).mean()) - 1, 3))
    R['lsb'][p] = cl; print(f"SBZ-{p if p == 256 else 128}: 0-qatlam tenglamasi korrelyatsiyasi (raund 1..10): {cl}")
def zanjir(Lm):
    L8 = np.linalg.matrix_power(Lm, 8) % 2; maps = [L8, Lm, Lm, L8, Lm]; best = {k: 99 for k in range(1, 7)}
    cands = [np.eye(32, dtype=np.int64)[list(c)].sum(0) % 2 for w in (1, 2) for c in itertools.combinations(range(32), w)]
    for end in range(1, 6):
        for u in cands:
            tot = int(u.sum()); cur = u; n = 1; best[1] = min(best[1], tot)
            for m in range(end - 1, -1, -1):
                cur = (maps[m].T @ cur) % 2
                if cur.sum() == 0: break
                tot += int(cur.sum()); n += 1; best[n] = min(best[n], tot)
    return best
zs = {k: [] for k in range(1, 7)}
for t in range(15 * HAJM):
    zz = zanjir(L_raund(kalitlar(rng, 1, 256)[0]))
    for k_ in zz:
        if zz[k_] < 99: zs[k_].append(zz[k_])
R['zanjir'] = {k_: (min(v), float(np.median(v))) for k_, v in zs.items()}
print("Qatlamlar | faol baytlar min / mediana | SBZ chegarasi log2|c| (mediana / eng yomon)")
for k_, (mn, md_) in R['zanjir'].items(): print(f"   {k_}   |   {mn} / {md_}   |   ≤ {-6*md_:.0f} / ≤ {-6*mn}")
''')

md("""
## 2. Differensial kriptotahlil
### 2.1. SBZ ayirmalar matritsasi (65536 × 256, to‘liq)
""")
code(r'''
DS = ddt(S, 256).astype(np.float64); idx = np.arange(256); dist = collections.Counter(); mx = (0, None); son = 0
for dn in range(256):
    Rm = (DS[dn][idx[:, None] ^ idx[None, :]] @ DS).astype(np.int64) if dn else DS.astype(np.int64) * 256
    v, c = np.unique(Rm, return_counts=True); dist.update({int(a): int(b) for a, b in zip(v, c)})
    sub = Rm.copy()
    if dn == 0: sub[0, :] = 0
    if sub.max() > mx[0]: mx = (int(sub.max()), (dn,) + tuple(int(t) for t in np.unravel_index(sub.argmax(), sub.shape)))
    if dn: son += int(Rm[0, 0])
R['SBZ_ddt_max'] = mx[0]
print("Maks. ehtimollik:", mx[0], "/ 65536 =", mx[0] / 65536, " (Δn, Δh, Δy) =", mx[1])
print("Δn ≠ 0 dagi qiymatlar oralig‘i:", min(k for k in dist if 0 < k < 512), "…", max(k for k in dist if 0 < k < 512), "(×2^-16)")
print("Δh = 0, Δn ≠ 0 da so‘nishlar soni:", son)
''')

md("""
### 2.2. Orttirmalarning raundlar orqali o‘tishi (yutishdan keyingi holatda bitta MSB ayirmasi)
""")
code(r'''
rng = np.random.default_rng(9); R['msb'] = {}
for p in (256, 16):
    c = Cfg(p, 'sbz'); N = 500 * HAJM; msb = p // 2; k = kalitlar(rng, N, p)
    h = rng.integers(0, p, (N, 32)); bl = rng.integers(0, p, (N, 32)); h2 = h.copy(); h2[:, 0] ^= msb
    t1, t2 = [], []; raundlar_yutishsiz(h, bl, k.copy(), k, c, t1); raundlar_yutishsiz(h2, bl, k.copy(), k, c, t2)
    rows = [(a[1], round(float((((a[2] ^ b[2]) == 0) | ((a[2] ^ b[2]) == msb)).all(1).mean()), 3), round(float(((a[2] ^ b[2]) != 0).sum(1).mean()), 1))
            for a, b in zip(t1, t2) if a[0] == 'Tuz']
    R['msb'][p] = rows; print(f"SBZ-{p if p == 256 else 128}: (raund, P(MSB izi), faol elementlar):", rows)
''')

md("""
## 3. Algebraik kriptotahlil
""")
code(r'''
x = np.arange(256)
print("S: kvadrat implitsit tenglamalar:", implicit_count(np.concatenate([bits(x, 8), bits(S[x], 8)], 1), 2))
hh = np.arange(65536) >> 8; nn = np.arange(65536) & 255; y = S[hh ^ S[nn]]
print("SBZ: kvadrat implitsit tenglamalar (24 o‘zgaruvchi):", implicit_count(np.concatenate([bits(hh, 8), bits(nn, 8), bits(y, 8)], 1), 2))
print("SBZ: chiqish bitlari darajalari:", [anf_deg((y >> j) & 1, 16) for j in range(8)])
R['kub'] = algebraik.kub_testlari(np.random.default_rng(21), dlar=(4, 8, 10), raundlar=(0, 1)) if HAJM >= 2 else None
rng = np.random.default_rng(31); R['lin'] = algebraik.linearizatsiya_hujumi(rng, 80, 100 * HAJM)
''')

md("""
## 4. Integral kriptotahlil
""")
code(r'''
R['int_komp'] = integral.komponentlar(np.random.default_rng(41), 40 * HAJM, 'sbz')
print("SBZ: n faol — turli qiymatlar", R['int_komp'].get('SBZ_n_faol_turli'), "; h faol —", R['int_komp'].get('SBZ_h_faol_turli'))
R['int_raund'] = {}
for p in (256, 16):
    for joy in ('holat', 'blok'):
        rr = integral.raund_kuzatish(np.random.default_rng(42), p, joy, 8 * HAJM, 'sbz'); R['int_raund'][f'{p}_{joy}'] = rr
        print(f"SBZ-{p if p == 256 else 128}, faol {joy}: raundlar oxirida 0-qatlamda doim balanslangan bitlar:",
              [r['qatlam_doim_nol'][0] for r in rr if r['amal'] == 'Tuz'])
R['int_toliq'] = integral.toliq_xesh(np.random.default_rng(43), 8 * HAJM, 'sbz')
print("To‘liq xesh (bitta faol bayt), bit-qatlamlar bo‘yicha doim nol bitlar:", {k: v['qatlam_boyicha_doim_nol_bitlar'] for k, v in R['int_toliq'].items()})
''')

md("""
### 4.1. Yuqori tartibli integral: 2¹⁶ elementli to‘plam (blokning ikki bayti faol)
""")
code(r'''
def ikki_bayt_iteratsiya(p, T):
    c = Cfg(p, 'sbz'); rng = np.random.default_rng(5); nb = 8 if p == 256 else 4; acc = []
    for t in range(T):
        k = kalitlar(rng, 1, p)[0]; h = rng.integers(0, p, 32); bl = rng.integers(0, p, 32); N = 65536
        H = np.tile(h, (N, 1)); BL = np.tile(bl, (N, 1))
        if p == 256: BL[:, 0] = np.arange(N) >> 8; BL[:, 1] = np.arange(N) & 255
        else:
            for i in range(4): BL[:, i] = (np.arange(N) >> (12 - 4 * i)) & 15
        K = np.tile(k, (N, 1)); tr = []; iteration(H, BL, K.copy(), K, c, trace=tr, rounds=3)
        acc.append([np.array([((np.bitwise_xor.reduce(hh_, axis=0) >> b) & 1) == 0 for b in range(nb)]) for nm, j, hh_, kk in tr if nm in ('BZ0', 'Tuz')])
    return [np.array([a[i] for a in acc]).all(0).sum(1).tolist() for i in range(len(acc[0]))]
for p in (256, 16):
    r = ikki_bayt_iteratsiya(p, 2 * HAJM); R[f'ikki_bayt_{p}'] = r
    print(f"SBZ-{p if p == 256 else 128}: SBZ(0) dan keyin va 1–3-raundlar oxirida doim nol bitlar (qatlamlar bo‘yicha):", r)
if OGIR:
    def toliq_ikki_bayt(p, L, act, T):
        c = Cfg(p, 'sbz'); rng = np.random.default_rng(11); nb = 8 if p == 256 else 4; z = []
        for t in range(T):
            k = kalitlar(rng, 1, 256)[0] if p == 256 else rng.integers(0, 256, 16)
            if p == 16: k[0] &= 0xEE
            m = rng.integers(0, 256, L); N = 65536; M = np.tile(m, (N, 1)); M[:, act[0]] = np.arange(N) >> 8; M[:, act[1]] = np.arange(N) & 255
            sm = np.zeros(32, dtype=np.int64)
            for s0 in range(0, N, 16384): sm ^= np.bitwise_xor.reduce(hash_msgs(M[s0:s0 + 16384], np.tile(k, (min(16384, N - s0), 1)), c), axis=0)
            z.append(np.array([((sm >> b) & 1) == 0 for b in range(nb)]))
        return np.array(z).all(0).sum(1).tolist()
    R['toliq_ikki_bayt_128'] = toliq_ikki_bayt(16, 16, (0, 1), 2); print("SBZ-128 to‘liq xesh, 2^16 to‘plam:", R['toliq_ikki_bayt_128'])
json.dump(R, open('sbz_natijalari.json', 'w'), ensure_ascii=False, indent=1, default=lambda o: o.tolist() if hasattr(o, 'tolist') else str(o))
print("Natijalar sbz_natijalari.json ga yozildi.")
''')
