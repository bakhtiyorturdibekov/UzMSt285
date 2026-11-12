import numpy as np, json, time
from vc import *
rng=np.random.default_rng(21); R={}
def rk(p):
    if p==256: k=rng.integers(0,256,32); k[0]&=0xFE; k[1]&=0xFE
    else: k=rng.integers(0,16,32); k[0]&=0xE; k[1]&=0xE
    return k
def cube_test(p,bz,r,d,ncubes=4):
    c=Cfg(p,bz); ub=8 if p==256 else 4
    k=rk(p); h=rng.integers(0,p,32); bl=rng.integers(0,p,32)
    lowmask=None; allzero=None
    for cc in range(ncubes):
        pos=rng.choice(2*8 if p==256 else 4*4,d,replace=False)   # birinchi 16 bit
        base=bl.copy(); base[:16//ub]=rng.integers(0,p,16//ub)
        N=1<<d; B=np.tile(base,(N,1))
        for t,q in enumerate(pos):
            unit=q//ub; bit=q%ub; B[:,unit]&=~(1<<bit)
            B[:,unit]|=((np.arange(N)>>t)&1)<<bit
        K=np.tile(k,(N,1)); H=np.tile(h,(N,1))
        out,_=iteration(H,B,K.copy(),K,c,rounds=r)
        s=np.bitwise_xor.reduce(out,axis=0)
        zb=np.array([(s>>j)&1 for j in range(ub)]).T==0   # (32,ub)
        allzero=zb if allzero is None else (allzero&zb)
    return float(allzero.mean()), allzero.mean(0).round(3).tolist()
for p,bz in [(256,'std'),(256,'sbz'),(16,'std'),(16,'sbz')]:
    for r in [0,1,2,3]:
        row={}
        for d in [2,4,6,8,10,12]:
            fr,lay=cube_test(p,bz,r,d); row[d]=(round(fr,3),lay)
        R[f'{p}_{bz}_r{r}']=row
        print(p,bz,r,{d:v[0] for d,v in row.items()}, 'qatlam0:',{d:v[1][0] for d,v in row.items()})
json.dump(R,open('alg2.json','w'),indent=0)
