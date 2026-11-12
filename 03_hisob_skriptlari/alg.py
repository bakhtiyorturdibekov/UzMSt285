import numpy as np, itertools, json, time
from vc import *
from lin import qosh_elem
rng=np.random.default_rng(13); R={}
def monomials(nv,deg):
    out=[()]
    for d in range(1,deg+1): out+=list(itertools.combinations(range(nv),d))
    return out
def implicit_count(points_bits,deg):
    """points_bits: (npts, nv) 0/1. Qaytaradi: deg darajali bog'liqsiz implitsit tenglamalar soni."""
    npts,nv=points_bits.shape; mons=monomials(nv,deg)
    words=(npts+63)//64
    cols=[]
    for m in mons:
        v=np.ones(npts,dtype=np.uint8)
        for i in m: v&=points_bits[:,i].astype(np.uint8)
        pad=np.zeros(words*64,dtype=np.uint8); pad[:npts]=v
        cols.append(np.packbits(pad.reshape(-1,8)[:,::-1],axis=1).reshape(-1).view(np.uint64) if False else np.packbits(pad).view(np.uint64))
    A=np.array(cols)  # (nmon, words)
    rank=0; n=A.shape[0]
    for w in range(A.shape[1]):
        for b in range(64):
            if rank>=n: break
            mask=np.uint64(1)<<np.uint64(b)
            col=(A[rank:,w]&mask)!=0
            idx=np.nonzero(col)[0]
            if len(idx)==0: continue
            piv=rank+idx[0]
            if piv!=rank: A[[rank,piv]]=A[[piv,rank]]
            rows=np.nonzero((A[:,w]&mask)!=0)[0]; rows=rows[rows!=rank]
            A[rows]^=A[rank]; rank+=1
    return len(mons)-rank, len(mons)
def bits(v,n): return ((v[:,None]>>np.arange(n))&1)
x=np.arange(256)
pts=np.concatenate([bits(x,8),bits(S[x],8)],1); R['S_quad']=implicit_count(pts,2)
pts=np.concatenate([bits(x,8),bits(Z[x],4)],1); R['Z_quad']=implicit_count(pts,2); R['Z_cubic']=implicit_count(pts,3)
A1,B1,A2,B2=[int(rng.integers(0,128))*2+1 for _ in range(4)]; Rv=int(rng.integers(0,128))*2
f=qosh_elem(A1,B1,A2,B2,Rv)
pts=np.concatenate([bits(x,8),bits(f,8)],1); R['Qosh_quad']=implicit_count(pts,2); R['Qosh_cubic']=implicit_count(pts,3)
t=time.time()
hh=np.arange(65536)>>8; nn=np.arange(65536)&255; y=S[hh^S[nn]]
pts=np.concatenate([bits(hh,8),bits(nn,8),bits(y,8)],1); R['SBZ_quad']=implicit_count(pts,2)
yb=(Z[hh]<<4)|Z[nn]; pts=np.concatenate([bits(hh,8),bits(nn,8),bits(yb,8)],1); R['BZ256_quad']=implicit_count(pts,2)
print('t',time.time()-t)
# ANF darajalari
def anf_deg(fbits,nv):
    a=fbits.astype(np.uint8).copy(); h=1; N=1<<nv
    while h<N:
        a=a.reshape(-1,2,h); a[:,1]^=a[:,0]; a=a.reshape(-1); h*=2
    wt=np.array([bin(i).count('1') for i in range(N)]); nz=wt[a==1]; return int(nz.max()) if len(nz) else -1
R['S_deg']=[anf_deg((S>>j)&1,8) for j in range(8)]
R['Z_deg']=[anf_deg((Z>>j)&1,8) for j in range(4)]
R['SBZ_deg']=[anf_deg((y>>j)&1,16) for j in range(8)]
R['BZ256_deg']=[anf_deg((yb>>j)&1,16) for j in range(8)]
degs=np.zeros((50,8),dtype=int)
for t_ in range(50):
    A1,B1,A2,B2=[int(rng.integers(0,128))*2+1 for _ in range(4)]; Rv=int(rng.integers(0,128))*2
    f=qosh_elem(A1,B1,A2,B2,Rv); degs[t_]=[anf_deg((f>>j)&1,8) for j in range(8)]
R['Qosh_deg_min']=degs.min(0).tolist(); R['Qosh_deg_max']=degs.max(0).tolist()
json.dump(R,open('alg1.json','w'),indent=1); print(R)
