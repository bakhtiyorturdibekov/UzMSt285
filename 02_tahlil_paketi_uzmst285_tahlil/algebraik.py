"""
3-bo‘lim. Algebraik kriptotahlil.
  1) implitsit tenglamalar soni va ANF darajalari: S, Z, SBZ, BaytZichlash-256, Qo‘sh elementi;
  2) kub testlari: r = 0…3 raunddan keyin daraja o‘sishi;
  3) hujum namoyishi: chiqish 0-qatlamini xabar 0-qatlamining affin funksiyasi sifatida tiklash;
  4) bit darajasidagi tenglamalar soni (baho modeli) va linearizatsiya murakkabligi.
Natija: natijalar/algebraik.json
"""
import argparse, json, math, os
import numpy as np
from algoritm import S, Z, Cfg, iteration, hash_msgs, to_units
from komponentlar import implicit_count, anf_deg, bits, qosh_elem, tasodifiy_param, kalitlar

def tenglamalar_va_daraja(rng, trials=50):
    R = {}; x = np.arange(256)
    R['S_kvadrat'] = implicit_count(np.concatenate([bits(x, 8), bits(S[x], 8)], 1), 2)
    R['Z_kvadrat'] = implicit_count(np.concatenate([bits(x, 8), bits(Z[x], 4)], 1), 2)
    R['Z_kub'] = implicit_count(np.concatenate([bits(x, 8), bits(Z[x], 4)], 1), 3)
    f = qosh_elem(*tasodifiy_param(rng))
    R['Qosh_kvadrat'] = implicit_count(np.concatenate([bits(x, 8), bits(f, 8)], 1), 2)
    R['Qosh_kub'] = implicit_count(np.concatenate([bits(x, 8), bits(f, 8)], 1), 3)
    hh = np.arange(65536) >> 8; nn = np.arange(65536) & 255
    y = S[hh ^ S[nn]]; yb = (Z[hh] << 4) | Z[nn]
    R['SBZ_kvadrat'] = implicit_count(np.concatenate([bits(hh, 8), bits(nn, 8), bits(y, 8)], 1), 2)
    R['BZ256_kvadrat'] = implicit_count(np.concatenate([bits(hh, 8), bits(nn, 8), bits(yb, 8)], 1), 2)
    R['S_daraja'] = [anf_deg((S >> j) & 1, 8) for j in range(8)]
    R['Z_daraja'] = [anf_deg((Z >> j) & 1, 8) for j in range(4)]
    R['SBZ_daraja'] = [anf_deg((y >> j) & 1, 16) for j in range(8)]
    R['BZ256_daraja'] = [anf_deg((yb >> j) & 1, 16) for j in range(8)]
    D = np.array([[anf_deg((qosh_elem(*tasodifiy_param(rng)) >> j) & 1, 8) for j in range(8)] for _ in range(trials)])
    R['Qosh_daraja_min'] = D.min(0).tolist(); R['Qosh_daraja_mediana'] = np.median(D, 0).tolist(); R['Qosh_daraja_max'] = D.max(0).tolist()
    return R

def kub_testlari(rng, dlar=(2, 4, 6, 8, 10, 12), raundlar=(0, 1, 2, 3), ncubes=4):
    """Xabarning dastlabki 16 bitidan d ta bit; 4 ta kub bo‘yicha yig‘indisi doim nol bo‘lgan bitlar ulushi."""
    R = {}
    for p, bz in [(256, 'std'), (256, 'sbz'), (16, 'std'), (16, 'sbz')]:
        c = Cfg(p, bz); ub = 8 if p == 256 else 4
        for r in raundlar:
            row = {}
            for d in dlar:
                k = kalitlar(rng, 1, p)[0]; h = rng.integers(0, p, 32); bl = rng.integers(0, p, 32); allz = None
                for _ in range(ncubes):
                    pos = rng.choice(16, d, replace=False); base = bl.copy(); base[:16 // ub] = rng.integers(0, p, 16 // ub)
                    N = 1 << d; Bm = np.tile(base, (N, 1))
                    for t, q in enumerate(pos):
                        u, b = q // ub, q % ub; Bm[:, u] &= ~(1 << b); Bm[:, u] |= ((np.arange(N) >> t) & 1) << b
                    K = np.tile(k, (N, 1)); out, _ = iteration(np.tile(h, (N, 1)), Bm, K.copy(), K, c, rounds=r)
                    s = np.bitwise_xor.reduce(out, axis=0); zb = np.array([(s >> j) & 1 for j in range(ub)]).T == 0
                    allz = zb if allz is None else (allz & zb)
                row[str(d)] = {'barcha_bitlar': round(float(allz.mean()), 3), '0-qatlam': round(float(allz[:, 0].mean()), 3)}
            R[f'{p}_{bz}_r{r}'] = row
            print(f"  p={p}, {bz}, r={r}: " + ", ".join(f"d={d}:{v['barcha_bitlar']}" for d, v in row.items()))
    return R

def gf2_solve(X, Y):
    A = np.concatenate([X, Y], 1).astype(np.uint8) % 2; m, n = X.shape; r = 0; piv = []
    for col in range(n):
        idx = [i for i in range(r, m) if A[i, col]]
        if not idx: continue
        A[[r, idx[0]]] = A[[idx[0], r]]
        for i in range(m):
            if i != r and A[i, col]: A[i] ^= A[r]
        piv.append(col); r += 1
    W = np.zeros((n, Y.shape[1]), dtype=np.uint8)
    for i, col in enumerate(piv): W[col] = A[i, n:]
    return W

def linearizatsiya_hujumi(rng, n_oquv=80, n_sinov=300):
    R = {}
    for p, bz in [(16, 'std'), (16, 'sbz'), (256, 'std'), (256, 'sbz')]:
        c = Cfg(p, bz); bl = 32 if p == 256 else 16
        if p == 256: k = rng.integers(0, 256, 32); k[0] &= 0xFE; k[1] &= 0xFE
        else: k = rng.integers(0, 256, 16); k[0] &= 0xEE
        H = lambda m: hash_msgs(m, np.tile(k, (len(m), 1)), c)
        feats = lambda m: np.concatenate([to_units(m, p) % 2, np.ones((len(m), 1), dtype=np.int64)], 1)
        tr = rng.integers(0, 256, (n_oquv, bl)); te = rng.integers(0, 256, (n_sinov, bl))
        W = gf2_solve(feats(tr), H(tr) % 2); pred = (feats(te) @ W) % 2; act = H(te) % 2
        R[f'{p}_{bz}'] = {'toliq_32_bit': float((pred == act).all(1).mean()), 'bitlar_boyicha': round(float((pred == act).mean()), 4)}
        print(f"  p={p}, {bz}: {R[f'{p}_{bz}']}")
    return R

def tenglamalar_soni():
    """Bit darajasidagi baho modeli: (o‘zgaruvchilar, tenglamalar, nochiziqli tenglamalar)."""
    def counts(n, mode):
        w = 32; ADD = (2*n-1, 2*n-1, n-1); MUL = (n*(n+1)//2 + (n-1)*(2*n-1),) * 2 + (n*(n+1)//2 + (n-1)*(n-1),)
        add = lambda a, b, f=1: tuple(x + f*y for x, y in zip(a, b)); z = (0, 0, 0); q = z
        for _ in range(2):
            q = add(q, ADD, (w-1)*2); q = add(q, MUL, (w-1)*2); q = add(q, (2*n,)*3, 4); q = add(q, MUL, 1)
            q = add(q, ADD, w*4); q = add(q, MUL, w*9); q = add(q, ADD, w*6); q = add(q, (n,)*3, w)
        ar = add(add(z, MUL, 128), ADD, 144); tz = add(add(z, ADD, w), (n,)*3, w)
        if mode == 'sbz': nb = w if n == 8 else w // 2; bz = (16*nb, 78*nb, 78*nb)
        elif n == 8: bz = (8*w, 43*2*w + 8*w, 43*2*w)
        else: bz = (0, n*w, 0)
        rnd = add(add(ar, q, 2), tz); r0 = add(q, bz)
        out = dict(qosh=q, aralash=ar, tuzilma=tz, yutish=bz, raund=rnd, r1=add(r0, rnd))
        out['r2'] = add(out['r1'], rnd); out['r3'] = add(out['r2'], rnd); return out
    E = {f'{lab}_{m}': counts(n, m) for n, lab in [(8, '256'), (4, '128')] for m in ('std', 'sbz')}
    lc = lambda nv, d: round(2.8 * math.log2(sum(math.comb(nv, i) for i in range(d + 1))), 1)
    return E, {f'{nv}_ozg_d{d}': lc(nv, d) for nv in (128, 256) for d in (1, 4, 6, 7, 8, 13)}

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument('--tez', action='store_true')
    a = ap.parse_args(); os.makedirs('natijalar', exist_ok=True); out = {}
    print("1. Implitsit tenglamalar va darajalar..."); out['tenglamalar_daraja'] = tenglamalar_va_daraja(np.random.default_rng(13), 10 if a.tez else 50)
    print("2. Kub testlari..."); out['kub'] = kub_testlari(np.random.default_rng(21), dlar=(2, 4, 6, 8) if a.tez else (2, 4, 6, 8, 10, 12), raundlar=(0, 1) if a.tez else (0, 1, 2, 3))
    print("3. Linearizatsiya hujumi..."); out['linearizatsiya'] = linearizatsiya_hujumi(np.random.default_rng(31), 80, 100 if a.tez else 300)
    E, LC = tenglamalar_soni(); out['tenglamalar_soni'] = E; out['linearizatsiya_murakkabligi_log2'] = LC
    json.dump(out, open('natijalar/algebraik.json', 'w'), indent=1, ensure_ascii=False, default=list)
    print("Saqlandi: natijalar/algebraik.json")
