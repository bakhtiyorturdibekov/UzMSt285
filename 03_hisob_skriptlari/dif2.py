import numpy as np, json, collections
from vc import *
rng=np.random.default_rng(5)
def rand_keys(N,p):
    if p==256: k=rng.integers(0,256,(N,32)); k[:,0]&=0xFE; k[:,1]&=0xFE
    else: k=rng.integers(0,16,(N,32)); k[:,0]&=0xE; k[:,1]&=0xE
    return k
def hw(a,p): 
    b=8 if p==256 else 4
    return sum(((a>>i)&1) for i in range(b)).sum(1)
Res={}
order=None
for p,bz in [(256,'std'),(256,'sbz'),(16,'std'),(16,'sbz')]:
    c=Cfg(p,bz); msb=p//2; N=2000
    for case in ['D1','D2','D3']:
        k=rand_keys(N,p); h=rng.integers(0,p,(N,32)); bl=rng.integers(0,p,(N,32))
        h2=h.copy(); bl2=bl.copy()
        if case=='D1': h2[:,0]^=msb
        elif case=='D2': bl2[:,0]^=msb; bl2[:,9]^=msb
        else: bl2[:,0]^=msb
        t1=[];t2=[]
        iteration(h,bl,k.copy(),k,c,trace=t1); iteration(h2,bl2,k.copy(),k,c,trace=t2)
        rows=[]
        for (nm,j,a,ka),(_,_,b,kb) in zip(t1,t2):
            d=a^b; act=(d!=0).sum(1)
            msbonly=float(((d==0)|(d==msb)).all(1).mean())
            cnt=collections.Counter(map(bytes,d.astype(np.uint8))); top=cnt.most_common(1)[0][1]/N
            rows.append(dict(op=nm,j=j,act=round(float(act.mean()),2),act_min=int(act.min()),msb=round(msbonly,3),top=round(top,4),hd=round(float(hw(d,p).mean()),1),zero=round(float((act==0).mean()),4)))
        Res[f'{p}_{bz}_{case}']=rows
        print(p,bz,case,[(r['op'],r['j'],r['act'],r['msb'],r['top'],r['hd']) for r in rows if r['op'] in ('Qosh0','BZ0','Tuz','BZ8','BZ9')][:14])
json.dump(Res,open('dif2.json','w'),indent=0)
