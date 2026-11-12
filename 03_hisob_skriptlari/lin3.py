import numpy as np, itertools, json
from lin2 import Pm, Mmat, rand_keys, rng
import lin2
seq_maps=['L8','L1','L1']*3   # 0->8 (L^8), 8->9 (L), 9->0' (L)
res={k:[] for k in range(1,7)}
for t in range(120):
    k=rand_keys(1,256)[0]; L=(Pm@Mmat(k))%2; L8=np.linalg.matrix_power(L,8)%2
    # qatlamlar ketma-ketligi: 0,8,9,0',8',9'  ; xaritalar: 0->8:L8, 8->9:L, 9->0':L
    maps=[L8,L,L,L8,L]   # i-qatlamdan (i+1)-qatlamga
    best={kk:99 for kk in range(1,7)}
    cands=[np.eye(32,dtype=np.int64)[list(c)].sum(0)%2 for w in (1,2) for c in itertools.combinations(range(32),w)]
    for end in range(1,6):   # oxirgi qatlam indeksi (1..5), zanjir orqaga
        for u in cands:
            tot=int(u.sum()); cur=u; n=1
            best[1]=min(best[1],tot)
            for m in range(end-1,-1,-1):
                cur=(maps[m].T@cur)%2
                if cur.sum()==0: break
                tot+=int(cur.sum()); n+=1
                best[n]=min(best[n],tot)
    for kk in best: 
        if best[kk]<99: res[kk].append(best[kk])
out={str(kk):{'min':int(min(v)),'median':float(np.median(v)),'mean':round(float(np.mean(v)),2)} for kk,v in res.items() if v}
print(out); json.dump(out,open('lin3.json','w'),indent=1)
