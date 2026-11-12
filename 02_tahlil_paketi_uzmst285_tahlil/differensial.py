"""
2-bo‘lim. Differensial kriptotahlil.
  1) ayirmalar matritsalari: S, Z, SBZ, Qo‘sh elementi;
  2) orttirmalarni raundlar va har bir akslantirish bo‘yicha kuzatish:
       D0a/D0b — yutishdan keyingi holatdagi 1 / 2 baytli MSB ayirmasi,
       D1 — iteratsiya boshidagi holatdagi 1 baytli MSB ayirmasi,
       D2 — kirish blokidagi 2 baytli MSB ayirmasi, D3 — kirish blokidagi 1 baytli MSB ayirmasi;
  3) Aralash yadrosi: nol va teng ustunli kalitlar ulushi.
Natija: natijalar/differensial.json
"""
import argparse, collections, json, os
import numpy as np
from algoritm import S, Z, Cfg, iteration, aralash, qosh, surholat, surkalit, tuz, bzf
from komponentlar import ddt, qosh_elem, tasodifiy_param, kalitlar, M_aralash

def komponentlar_tahlili(rng, trials=200):
    R = {}; DS = ddt(S, 256); DZ = ddt(Z, 16); x = np.arange(256)
    dist = lambda D: {int(a): int(b) for a, b in zip(*np.unique(D[1:], return_counts=True))}
    R['S_max'] = int(DS[1:].max()); R['S_taqsimot'] = dist(DS)
    R['S_bolagi'] = [[int(DS[d, y]) for y in range(8)] for d in range(1, 9)]
    R['Z_max'] = int(DZ[1:].max()); i = np.unravel_index(DZ[1:].argmax(), DZ[1:].shape)
    R['Z_max_joyi'] = (hex(int(i[0]) + 1), hex(int(i[1]))); R['Z_taqsimot'] = dist(DZ)
    R['Z_sonishi_mumkin_ayirmalar'] = int((DZ[1:, 0] > 0).sum())
    for d in (0x80, 0x01, 0x96): R[f'Z_satr_{d:02x}'] = DZ[d].tolist()
    def sbz(dh, dn):
        if dn == 0: return DS[dh] / 256.0
        return sum(DS[dn, d] * DS[dh ^ d] for d in range(256) if DS[dn, d]) / 65536.0
    R['SBZ_dh0_dn80_max'] = float(sbz(0, 0x80).max()); R['SBZ_dh80_dn0_max'] = float(sbz(0x80, 0).max())
    R['SBZ_dh0_dn80_sonish'] = float(sbz(0, 0x80)[0]); R['SBZ_dh80_dn80_sonish'] = float(sbz(0x80, 0x80)[0])
    R['SBZ_80dan80ga'] = float((DS[0x80] * DS[:, 0x80]).sum() / 65536)
    mx, p80, pj = [], [], {j: [] for j in range(8)}
    for _ in range(trials):
        f = qosh_elem(*tasodifiy_param(rng)); D = ddt(f, 256)
        mx.append(int(D[1:].max())); p80.append(D[0x80, 0x80] / 256)
        for j in range(8): pj[j].append(D[1 << j].max() / 256)
    R['Qosh_max'] = int(max(mx)); R['Qosh_p(80->80)'] = float(np.mean(p80))
    R['Qosh_2^j_eng_ehtimolli'] = [round(float(np.mean(pj[j])), 4) for j in range(8)]
    return R

def raundlar_yutishsiz(holat, blok, ke, k, c, trace):
    """Yutishdan keyingi holatdan boshlab 1–10-raundlar (0-nuqtadagi yutishsiz)."""
    R = k[:, 0]
    def T(nm, j): trace.append((nm, j, holat.copy(), ke.copy()))
    for j in range(1, 11):
        holat = aralash(holat, ke, c); T('Aralash', j)
        holat, ke = qosh(holat, ke, R, c); T('Qosh1', j)
        holat = surholat(holat); ke = surkalit(ke); T('Sur', j)
        if j == 8:
            holat, hn = qosh(holat, blok, R, c); T('Qosh_inj8', j); holat = bzf(holat, hn, c); T('BZ8', j)
        else:
            holat, ke = qosh(holat, ke, R, c); T('Qosh2', j)
        ke = tuz(ke, k, c); T('Tuz', j)
        if j == 9:
            holat, hn = qosh(holat, blok, R, c); T('Qosh_inj9', j); holat = bzf(holat, hn, c); T('BZ9', j)

def hw(a, p): return sum(((a >> i) & 1) for i in range(8 if p == 256 else 4)).sum(1)

def kuzatish(rng, N=2000, holatlar=('D1', 'D2', 'D3')):
    R = {}
    for p, bz in [(256, 'std'), (256, 'sbz'), (16, 'std'), (16, 'sbz')]:
        c = Cfg(p, bz); msb = p // 2
        for case in holatlar:
            k = kalitlar(rng, N, p); h = rng.integers(0, p, (N, 32)); bl = rng.integers(0, p, (N, 32))
            h2, bl2 = h.copy(), bl.copy()
            if case in ('D0a', 'D1'): h2[:, 0] ^= msb
            elif case == 'D0b': h2[:, 0] ^= msb; h2[:, 9] ^= msb
            elif case == 'D2': bl2[:, 0] ^= msb; bl2[:, 9] ^= msb
            else: bl2[:, 0] ^= msb
            t1, t2 = [], []
            if case.startswith('D0'):
                raundlar_yutishsiz(h, bl, k.copy(), k, c, t1); raundlar_yutishsiz(h2, bl, k.copy(), k, c, t2)
            else:
                iteration(h, bl, k.copy(), k, c, trace=t1); iteration(h2, bl2, k.copy(), k, c, trace=t2)
            rows = []
            for (nm, j, a, ka), (_, _, b, kb) in zip(t1, t2):
                d, dk = a ^ b, ka ^ kb; act = (d != 0).sum(1)
                msbonly = (((d == 0) | (d == msb)).all(1) & ((dk == 0) | (dk == msb)).all(1)).mean()
                top = collections.Counter(map(bytes, np.concatenate([d, dk], 1).astype(np.uint8))).most_common(1)[0][1] / N
                rows.append(dict(amal=nm, raund=j, faol_holat=round(float(act.mean()), 2), faol_holat_min=int(act.min()),
                                 faol_ke=round(float((dk != 0).sum(1).mean()), 2), P_MSB_izi=round(float(msbonly), 4),
                                 eng_ehtimolli_ayirma=round(top, 4), xemming=round(float(hw(d, p).mean()), 1),
                                 nol_ayirma=round(float(((act == 0) & ((dk != 0).sum(1) == 0)).mean()), 4)))
            R[f'{p}_{bz}_{case}'] = rows
        print(f"  p={p}, {bz}: tayyor")
    return R

def yadro(rng, nkeys=300):
    zc = eq = 0
    for _ in range(nkeys):
        M = M_aralash(kalitlar(rng, 1, 256)[0]); cols = [tuple(M[:, i]) for i in range(32)]
        zc += any(sum(cc) == 0 for cc in cols); eq += len(set(cols)) < 32
    return {'nol_ustunli_kalitlar': zc / nkeys, 'teng_ustunli_kalitlar': eq / nkeys}

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument('--tez', action='store_true')
    a = ap.parse_args(); s = 0.15 if a.tez else 1.0
    os.makedirs('natijalar', exist_ok=True); out = {}
    print("1. Ayirmalar matritsalari..."); out['komponentlar'] = komponentlar_tahlili(np.random.default_rng(11), int(200 * s))
    print("2. Orttirmalarni kuzatish...")
    out['kuzatish'] = kuzatish(np.random.default_rng(5), int(2000 * s), ('D1', 'D2', 'D3'))
    out['kuzatish'].update(kuzatish(np.random.default_rng(9), int(3000 * s), ('D0a', 'D0b')))
    print("3. Aralash yadrosi..."); out['yadro'] = yadro(np.random.default_rng(31), int(300 * s))
    json.dump(out, open('natijalar/differensial.json', 'w'), indent=1, ensure_ascii=False)
    print("Saqlandi: natijalar/differensial.json")
