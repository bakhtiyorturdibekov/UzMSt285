"""
1-bo‘lim. Chiziqli kriptotahlil.
  1) akslantirishlarning korrelyatsion matritsalari (S, Z, SBZ, Qo‘sh elementi);
  2) 0-qatlam bo‘yicha raund tenglamasining korrelyatsiyasi (haqiqiy algoritmda);
  3) L = P·M(k0) matritsasi: rang, nol satrlar, tarmoqlanish soni;
  4) ketma-ket yutish qatlamlari bo‘yicha minimal faol baytlar.
Natija: natijalar/chiziqli.json
"""
import argparse, itertools, json, os
import numpy as np
from algoritm import S, Z, Cfg, iteration
from komponentlar import lat, qosh_elem, tasodifiy_param, kalitlar, L_raund, rank2

def komponentlar_tahlili(rng, trials=200):
    R = {}
    WS = lat(S, 8); WZ = lat(Z, 4); CS = WS / 256.0
    dist = lambda W: {int(a): int(b) for a, b in zip(*np.unique(np.abs(W[1:, :]), return_counts=True))}
    R['S_W_max'] = int(np.abs(WS[1:, :]).max()); R['S_W_taqsimot'] = dist(WS)
    R['S_eng_yaxshi_soni'] = int((np.abs(WS[1:, 1:]) == 32).sum())
    R['S_W_bolagi'] = [[int(WS[b, a]) for a in range(1, 9)] for b in range(1, 9)]
    R['Z_W_max'] = int(np.abs(WZ[1:, :]).max()); R['Z_W_taqsimot'] = dist(WZ)
    R['Z_bit0_eng_yaxshi_c'] = float(np.abs(WZ[1]).max() / 256)
    # SBZ: c((α,β)→γ) = c_S(α→γ)·c_S(β→α)
    best, ex, cnt = 0.0, None, 0
    M32 = (np.abs(WS) == 32)
    for g in range(1, 256):
        for a in range(1, 256):
            v = abs(CS[g, a]) * np.abs(CS[a]).max()
            if v > best + 1e-12: best, ex = v, (a, int(np.argmax(np.abs(CS[a]))), g)
        for a in np.nonzero(M32[g, 1:])[0] + 1: cnt += int(M32[a, 1:].sum())
    R['SBZ_c_max'] = best; R['SBZ_misol_alfa_beta_gamma'] = ex; R['SBZ_max_uchliklar_soni'] = cnt
    R['SBZ_gamma1_alfa_quyi'] = float(max(abs(CS[1, a]) * np.abs(CS[a]).max() for a in (1, 2, 3)))
    # Qo‘sh elementi
    layer, layer_min, same = np.zeros(8), np.ones(8), np.zeros(8)
    for _ in range(trials):
        f = qosh_elem(*tasodifiy_param(rng)); W = lat(f, 8)
        for j in range(8):
            v = np.abs(W[1 << j]).max() / 256; layer[j] += v; layer_min[j] = min(layer_min[j], v)
            same[j] += abs(W[1 << j, 1 << j]) / 256
    R['Qosh_bitj_eng_yaxshi_c_ortacha'] = (layer / trials).round(4).tolist()
    R['Qosh_bitj_eng_yaxshi_c_min'] = layer_min.round(4).tolist()
    R['Qosh_bitj_c(xj->yj)_ortacha'] = (same / trials).round(4).tolist()
    return R

def raund_tahlili(rng, N=1500):
    """0-qatlam bashorati h0 ← L·h0 (Standart-128 da yutishda ⊕ blok0) ning raundlar bo‘yicha korrelyatsiyasi."""
    R = {}
    for p, bz in [(256, 'std'), (256, 'sbz'), (16, 'std'), (16, 'sbz')]:
        c = Cfg(p, bz); k = kalitlar(rng, N, p)
        holat = rng.integers(0, p, (N, 32)); blok = rng.integers(0, p, (N, 32))
        tr = []; iteration(holat, blok, k.copy(), k, c, trace=tr)
        cur = [t for t in tr if t[0] == 'BZ0'][0][2] % 2
        Ls = [L_raund(k[n]) for n in range(N)]; corr = []
        for j in range(1, 11):
            cur = np.array([(Ls[n] @ cur[n]) % 2 for n in range(N)])
            if j in (8, 9) and bz == 'std' and p == 16: cur = cur ^ (blok % 2)
            act = [t for t in tr if t[1] == j][-1][2] % 2
            corr.append(round(2 * float((cur == act).mean()) - 1, 4))
        R[f'{p}_{bz}'] = corr; print(f"  0-qatlam bashorati p={p}, {bz}: {corr}")
    return R

def matritsa_tahlili(rng, nkeys=200):
    ranks, zr, br1, br8 = [], [], [], []
    for _ in range(nkeys):
        k = kalitlar(rng, 1, 256)[0]; L = L_raund(k); L8 = np.linalg.matrix_power(L, 8) % 2
        ranks.append(rank2(L)); zr.append(int((L.sum(1) == 0).sum()))
        for Lm, store in [(L, br1), (L8, br8)]:
            LT = Lm.T % 2; best = 99
            for w in range(1, 4):
                for comb in itertools.combinations(range(32), w):
                    wv = int((LT[:, list(comb)].sum(1) % 2).sum())
                    if wv > 0: best = min(best, w + wv)
                if best <= w + 1: break
            store.append(best)
    cnt = lambda a: {str(v): int(c) for v, c in zip(*np.unique(a, return_counts=True))}
    return {'rang': {'ortacha': float(np.mean(ranks)), 'min': int(min(ranks)), 'max': int(max(ranks))},
            'nol_satrlar': {'ortacha': float(np.mean(zr)), 'kalitlar_ulushi': float(np.mean(np.array(zr) > 0))},
            'tarmoqlanish_L': cnt(br1), 'tarmoqlanish_L8': cnt(br8)}

def faol_baytlar(rng, nkeys=120):
    """Qatlamlar: 0, 8, 9, 0', 8', 9'; o‘tishlar: L^8, L, L, L^8, L. Izni oxirgi qatlamdan orqaga tarqatish."""
    res = {k: [] for k in range(1, 7)}
    cands = [np.eye(32, dtype=np.int64)[list(c)].sum(0) % 2 for w in (1, 2) for c in itertools.combinations(range(32), w)]
    for _ in range(nkeys):
        k = kalitlar(rng, 1, 256)[0]; L = L_raund(k); L8 = np.linalg.matrix_power(L, 8) % 2
        maps = [L8, L, L, L8, L]; best = {kk: 99 for kk in range(1, 7)}
        for end in range(1, 6):
            for u in cands:
                tot = int(u.sum()); cur = u; n = 1; best[1] = min(best[1], tot)
                for m in range(end - 1, -1, -1):
                    cur = (maps[m].T @ cur) % 2
                    if cur.sum() == 0: break
                    tot += int(cur.sum()); n += 1; best[n] = min(best[n], tot)
        for kk in best:
            if best[kk] < 99: res[kk].append(best[kk])
    return {str(kk): {'min': int(min(v)), 'mediana': float(np.median(v)), 'ortacha': round(float(np.mean(v)), 2)} for kk, v in res.items() if v}

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument('--tez', action='store_true', help="kichik tanlanmalar bilan tez sinov")
    a = ap.parse_args(); s = 0.2 if a.tez else 1.0
    os.makedirs('natijalar', exist_ok=True)
    out = {}
    print("1. Akslantirishlar..."); out['komponentlar'] = komponentlar_tahlili(np.random.default_rng(2025), int(200 * s))
    rng = np.random.default_rng(7)   # 2–4-bosqichlar bitta generatordan ketma-ket foydalanadi (hisobotdagi tanlanma)
    print("2. Raund tenglamasi..."); out['raund_0qatlam'] = raund_tahlili(rng, int(1500 * s))
    print("3. L matritsasi..."); out['L_matritsa'] = matritsa_tahlili(rng, int(200 * s))
    print("4. Faol baytlar..."); out['faol_baytlar'] = faol_baytlar(rng, int(120 * s))
    json.dump(out, open('natijalar/chiziqli.json', 'w'), indent=1, ensure_ascii=False, default=float)
    print("Saqlandi: natijalar/chiziqli.json")
