import numpy as np, json, itertools
from vc import *
rng=np.random.default_rng(7)
def rand_keys(N,p):
    if p==256: k=rng.integers(0,256,(N,32)); k[:,0]&=0xFE; k[:,1]&=0xFE
    else: k=rng.integers(0,16,(N,32)); k[:,0]&=0xE; k[:,1]&=0xE
    return k
c2=Cfg(2,'std')
idx=np.arange(32)[None,:]
Pperm=surholat(idx.copy())[0]   # yangi[i]=eski[Pperm[i]]
Pm=np.zeros((32,32),dtype=np.int64); Pm[np.arange(32),Pperm]=1
def Mmat(k):  # LSB qatlam matritsasi: h0' = M h0 (mod 2)
    E=np.eye(32,dtype=np.int64); K=np.tile(k%2,(32,1))
    return (aralash(E,K,c2).T)%2
def rank2(A):
    A=A.copy()%2; r=0
    for col in range(A.shape[1]):
        piv=[i for i in range(r,A.shape[0]) if A[i,col]]
        if not piv: continue
        A[[r,piv[0]]]=A[[piv[0],r]]
        for i in range(A.shape[0]):
            if i!=r and A[i,col]: A[i]^=A[r]
        r+=1
    return r
Res={}
# 1) LSB-qatlam bashoratining aniqligi (1..10 raund), 4 variant
for p,bz in [(256,'std'),(256,'sbz'),(16,'std'),(16,'sbz')]:
    c=Cfg(p,bz); N=1500
    k=rand_keys(N,p); holat=rng.integers(0,p,(N,32)); blok=rng.integers(0,p,(N,32))
    tr=[]; iteration(holat,blok,k.copy(),k,c,trace=tr)
    # boshlang'ich nuqta: BZ0 dan keyin
    h0=[t for t in tr if t[0]=='BZ0'][0][2]%2
    pred=h0.copy(); agree=[]
    Ms=[ (Pm@Mmat(k[n]))%2 for n in range(N)]
    cur=pred
    for j in range(1,11):
        cur=np.array([(Ms[n]@cur[n])%2 for n in range(N)])
        if j in (8,9) and bz=='std' and p==16: cur=cur^(blok%2)
        act=[t for t in tr if t[1]==j][-1][2]%2
        agree.append(float((cur==act).mean()))
    Res[f'lsb_pred_{p}_{bz}']=[round(2*a-1,4) for a in agree]
    print(p,bz,Res[f'lsb_pred_{p}_{bz}'])
# 2) Rang, nol satrlar, aktiv baytlar (L = P*M)
ranks=[];zr=[];br1=[];br8=[];kerdim=[]
for t in range(200):
    k=rand_keys(1,256)[0]; L=(Pm@Mmat(k))%2; L8=np.linalg.matrix_power(L,8)%2
    ranks.append(rank2(L)); zr.append(int((L.sum(1)==0).sum()))
    for Lm,store in [(L,br1),(L8,br8)]:
        LT=Lm.T%2; best=99
        for w in range(1,4):
            for comb in itertools.combinations(range(32),w):
                v=LT[:,list(comb)].sum(1)%2; wv=int(v.sum())
                if wv>0: best=min(best,w+wv)
            if best<=w+1: break
        store.append(best)
Res['rank_L']={'mean':float(np.mean(ranks)),'min':int(min(ranks)),'max':int(max(ranks)),'full':float(np.mean(np.array(ranks)==32))}
Res['zero_rows']={'mean':float(np.mean(zr)),'share_keys_with_zero_row':float(np.mean(np.array(zr)>0)),'max':int(max(zr))}
Res['branch_L1']={str(v):int(c) for v,c in zip(*np.unique(br1,return_counts=True))}
Res['branch_L8']={str(v):int(c) for v,c in zip(*np.unique(br8,return_counts=True))}
print(Res['rank_L'],Res['zero_rows'],Res['branch_L1'],Res['branch_L8'])
json.dump(Res,open('lin2.json','w'),indent=1)
