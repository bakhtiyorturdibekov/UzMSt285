import numpy as np
from vc import *
from dif3 import rounds_from
from dif2 import rand_keys
rng=np.random.default_rng(3)
for p in (256,16):
    c=Cfg(p,'sbz'); N=4000; msb=p//2
    k=rand_keys(N,p); h=rng.integers(0,p,(N,32)); bl=rng.integers(0,p,(N,32)); h2=h.copy(); h2[:,0]^=msb
    t1=[];t2=[]; rounds_from(h,bl,k.copy(),k,c,t1); rounds_from(h2,bl,k.copy(),k,c,t2)
    out=[]
    for (nm,j,a,ka),(_,_,b,kb) in zip(t1,t2):
        if j<=2 or nm in('BZ8','BZ9'): out.append((nm,j,round(float(((a==b).all(1)&(ka==kb).all(1)).mean()),4)))
    print(p,out)
