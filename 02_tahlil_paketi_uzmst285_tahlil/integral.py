"""
4-bo‘lim. Integral (square) kriptotahlil — standart algoritm (BaytZichlash) va SBZ varianti.
To‘plam xossalari: A (barcha qiymatlar bir martadan), C (doimiy), B (XOR-yig‘indi = 0),
B7 (XOR-yig‘indining 0–6-bitlari = 0, ya’ni yig‘indi ∈ {00, 80}), U (noma’lum).
  1) akslantirishlarning tanlangan to‘plamlarga ta’siri (Qo‘sh elementi va massivi, Aralash, Z, XOR);
  2) raundlar va akslantirishlar bo‘yicha integral xossalarni kuzatish;
  3) to‘liq xesh uchun integral farqlovchi;
  4) Standart-128 da T-funksiya xossasi: yuqori bit-qatlam o‘zgarganda quyi qatlamlar saqlanishi.
Natija: natijalar/integral.json
"""
import argparse, json, os
import numpy as np
from algoritm import S, Z, Cfg, iteration, qosh, aralash, surholat, surkalit, tuz, bzf, hash_msgs, to_units
from komponentlar import qosh_elem, tasodifiy_param, kalitlar

def xossa(V, p):
    """V: (N, 32) — to‘plam bo‘yicha qiymatlar. Har pozitsiya uchun: 'A','C','B','B7','U'."""
    msb = p // 2; out = []
    s = np.bitwise_xor.reduce(V, axis=0)
    for i in range(V.shape[1]):
        col = V[:, i]; nd = len(np.unique(col))
        if nd == 1: out.append('C')
        elif nd == V.shape[0] and V.shape[0] == p: out.append('A')
        elif s[i] == 0: out.append('B')
        elif s[i] == msb: out.append('B7')
        else: out.append('U')
    return out

def sana(xs):
    return {t: xs.count(t) for t in ('A', 'C', 'B', 'B7', 'U')}

def komponentlar(rng, trials=200, bz='std'):
    R = {}; x = np.arange(256)
    # Qo'sh elementi: 256 kirish -> chiqish to'plami
    nd, sm = [], []
    for _ in range(trials):
        f = qosh_elem(*tasodifiy_param(rng)); nd.append(len(np.unique(f))); sm.append(int(np.bitwise_xor.reduce(f)))
    R['Qosh_element_turli_qiymatlar'] = {str(k): nd.count(k) for k in sorted(set(nd))}
    R['Qosh_element_xor_yigindi'] = {'00': sm.count(0), '80': sm.count(0x80), 'boshqa': trials - sm.count(0) - sm.count(0x80)}
    # Z: faol kirish -> chiqish
    R['Z_xor_yigindi'] = int(np.bitwise_xor.reduce(Z)); R['Z_har_qiymat_soni'] = sorted(set(np.bincount(Z, minlength=16).tolist()))
    # SBZ: S(h ⊕ S(n)) — n faol (h doimiy), h faol (n doimiy), ikkalasi bir xil faol (h = n = x)
    R['SBZ_n_faol_turli'] = int(len(np.unique(S[0x3c ^ S[x]]))); R['SBZ_h_faol_turli'] = int(len(np.unique(S[x ^ S[0x5a]])))
    R['SBZ_ikkalasi_faol_turli'] = int(len(np.unique(S[x ^ S[x]]))); R['SBZ_ikkalasi_xor'] = int(np.bitwise_xor.reduce(S[x ^ S[x]]))
    # Massiv darajasida: bitta faol bayt (holat[0,0]) — Qo'sh, Aralash, BZ ning ta'siri
    for p in (256, 16):
        c = Cfg(p, bz); N = p; acc = {'Qosh_holat': [], 'Qosh_holatn': [], 'Aralash': [], 'BZ_n_faol': [], 'XOR_n_faol': [], 'BZ_h_faol': []}
        for _ in range(trials // 4):
            k = kalitlar(rng, 1, p)[0]; h = rng.integers(0, p, 32); hn = rng.integers(0, p, 32)
            H = np.tile(h, (N, 1)); H[:, 0] = np.arange(N); HN = np.tile(hn, (N, 1)); K = np.tile(k, (N, 1))
            a, b = qosh(H, HN, K[:, 0], c); acc['Qosh_holat'].append(sana(xossa(a, p))); acc['Qosh_holatn'].append(sana(xossa(b, p)))
            acc['Aralash'].append(sana(xossa(aralash(H, K, c), p)))
            HN2 = HN.copy(); HN2[:, 0] = np.arange(N)
            if p == 256 or bz == 'sbz': acc['BZ_n_faol'].append(sana(xossa(bzf(np.tile(h, (N, 1)), HN2, c), p)))
            else: acc['XOR_n_faol'].append(sana(xossa(bzf(np.tile(h, (N, 1)), HN2, c), p)))
            acc['BZ_h_faol'].append(sana(xossa(bzf(H, np.tile(hn, (N, 1)), c), p)))
            cs = Cfg(p, 'sbz'); acc.setdefault('SBZ_n_faol', []).append(sana(xossa(bzf(np.tile(h, (N, 1)), HN2, cs), p)))
        R[f'massiv_{p}'] = {k_: {t: round(float(np.mean([d[t] for d in v])), 2) for t in ('A', 'C', 'B', 'B7', 'U')} for k_, v in acc.items() if v}
    return R

def raund_kuzatish(rng, p, joy, T=40, bz='std'):
    """joy='holat': 1-raund kirishidagi holat[0,0] faol; joy='blok': kirish blokining 0-elementi faol (0-nuqtadan boshlab).
    Natija: har akslantirishdan keyin har pozitsiyaning xossasi; T ta tajriba bo‘yicha 'barcha tajribalarda B yoki A' ulushi."""
    c = Cfg(p, bz); N = p; rec = {}; sums = {}
    nb = 8 if p == 256 else 4
    for _ in range(T):
        k = kalitlar(rng, 1, p)[0]; h = rng.integers(0, p, 32); bl = rng.integers(0, p, 32)
        H = np.tile(h, (N, 1)); BL = np.tile(bl, (N, 1)); K = np.tile(k, (N, 1))
        if joy == 'holat': H[:, 0] = np.arange(N)
        else: BL[:, 0] = np.arange(N)
        tr = []
        if joy == 'holat':
            from differensial import raundlar_yutishsiz
            raundlar_yutishsiz(H, BL, K.copy(), K, c, tr)
        else:
            iteration(H, BL, K.copy(), K, c, trace=tr)
        for nm, j, hh, kk in tr:
            key = f'{j}:{nm}'; rec.setdefault(key, []).append(xossa(hh, p))
            sums.setdefault(key, []).append(np.bitwise_xor.reduce(hh, axis=0))
    out = []
    for key, lst in rec.items():
        j, nm = key.split(':'); arr = np.array(lst)          # (T, 32)
        bal_all = ((arr == 'A') | (arr == 'B') | (arr == 'C')).all(0)   # doim balanslangan (XOR-yig‘indi 0)
        b7_all = ((arr == 'A') | (arr == 'B') | (arr == 'C') | (arr == 'B7')).all(0)
        SS = np.array(sums[key])                              # (T, 32)
        qatlam = [int((((SS >> b) & 1) == 0).all(0).sum()) for b in range(nb)]
        out.append(dict(raund=int(j), amal=nm, doim_B=int(bal_all.sum()), doim_B7=int(b7_all.sum()), qatlam_doim_nol=qatlam,
                        ortacha=sana([t for row in lst for t in row]), T=T))
        out[-1]['ortacha'] = {t: round(v / T, 2) for t, v in out[-1]['ortacha'].items()}
    return out

def toliq_xesh(rng, T=40, bz='std'):
    """Standart-128: bir blokli xabar, 0-bayt faol (256 xabar). Standart-256: 2 blokli xabar, 2-blokning 0-bayti faol."""
    R = {}
    for p, L in ((16, 16), (256, 64)):
        c = Cfg(p, bz); zer = np.zeros((T, 32, 8 if p == 256 else 4), dtype=bool)
        for t in range(T):
            k = kalitlar(rng, 1, 256)[0] if p == 256 else rng.integers(0, 256, 16)
            if p == 16: k[0] &= 0xEE
            m = rng.integers(0, 256, L); Mm = np.tile(m, (256, 1)); pos = 0 if p == 16 else 32
            Mm[:, pos] = np.arange(256)
            out = hash_msgs(Mm, np.tile(k, (256, 1)), c); s = np.bitwise_xor.reduce(out, axis=0)
            zer[t] = np.array([(s >> j) & 1 for j in range(zer.shape[2])]).T == 0
        R[f'{p}'] = {'qatlam_boyicha_doim_nol_bitlar': [int(zer[:, :, j].all(0).sum()) for j in range(zer.shape[2])],
                     'qatlam_boyicha_nol_ulushi': [round(float(zer[:, :, j].mean()), 3) for j in range(zer.shape[2])]}
    return R

def tfunksiya_128(rng, N=2000, bz='std'):
    """Standart-128, bir blokli xabar: faqat yuqori (3-) bit-qatlamdagi w ta bit o‘zgartirilganda
    chiqishning 0–2-qatlamlari (96 bit) saqlanish ehtimolligi."""
    c = Cfg(16, bz); R = {}
    for w in (1, 2, 4, 8, 32):
        k = rng.integers(0, 256, (N, 16)); k[:, 0] &= 0xEE
        m = rng.integers(0, 256, (N, 16)); u = to_units(m, 16); u2 = u.copy()
        for n in range(N):
            pos = rng.choice(32, w, replace=False); u2[n, pos] ^= 8
        m2 = np.array([[u2[n, 2*i] << 4 | u2[n, 2*i+1] for i in range(16)] for n in range(N)])
        o1 = hash_msgs(m, k, c); o2 = hash_msgs(m2, k, c)
        low = ((o1 ^ o2) & 7) == 0
        R[str(w)] = {'quyi_3_qatlam_saqlandi': round(float(low.all(1).mean()), 4), 'quyi_qatlam_bitlari_saqlandi': round(float(low.mean()), 4),
                     '0_qatlam_saqlandi': round(float((((o1 ^ o2) & 1) == 0).all(1).mean()), 4)}
    return R

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument('--tez', action='store_true')
    ap.add_argument('--bz', default='std', choices=['std', 'sbz'], help="yutish o‘zgartirishi: std (BaytZichlash) yoki sbz")
    a = ap.parse_args(); s = 0.25 if a.tez else 1.0
    os.makedirs('natijalar', exist_ok=True); out = {}
    print("1. Akslantirishlarning to‘plamlarga ta’siri..."); out['komponentlar'] = komponentlar(np.random.default_rng(41), int(200 * s), a.bz)
    print("2. Raundlar bo‘yicha kuzatish...")
    for p in (256, 16):
        for joy in ('holat', 'blok'):
            out[f'raund_{p}_{joy}'] = raund_kuzatish(np.random.default_rng(42), p, joy, int(40 * s), a.bz); print(f"   p={p}, {joy}: tayyor")
    print("3. To‘liq xesh..."); out['toliq_xesh'] = toliq_xesh(np.random.default_rng(43), int(40 * s), a.bz)
    print("4. 128 bitli rejimda yuqori bit-qatlam o‘zgarishi..."); out['tfunksiya_128'] = tfunksiya_128(np.random.default_rng(44), int(2000 * s), a.bz)
    fn = 'natijalar/integral.json' if a.bz == 'std' else 'natijalar/integral_sbz.json'
    json.dump(out, open(fn, 'w'), indent=1, ensure_ascii=False)
    print('Saqlandi:', fn)
