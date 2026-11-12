import numpy as np, json, collections
from vc import *
from dif2 import rand_keys, hw
rng=np.random.default_rng(9)
def rounds_from(holat,blok,ke,k,c,trace,j0=1):
    R=k[:,0]
    for j in range(j0,11):
        holat=aralash(holat,ke,c); trace.append(('Aralash',j,holat.copy(),ke.copy()))
        holat,ke=qosh(holat,ke,R,c); trace.append(('Qosh1',j,holat.copy(),ke.copy()))
        holat=surholat(holat); ke=surkalit(ke); trace.append(('Sur',j,holat.copy(),ke.copy()))
        if j==8:
            holat,hn=qosh(holat,blok,R,c); trace.append(('Qosh_inj8',j,holat.copy(),ke.copy()))
            holat=bzf(holat,hn,c); trace.append(('BZ8',j,holat.copy(),ke.copy()))
        else:
            holat,ke=qosh(holat,ke,R,c); trace.append(('Qosh2',j,holat.copy(),ke.copy()))
        ke=tuz(ke,k,c); trace.append(('Tuz',j,holat.copy(),ke.copy()))
        if j==9:
            holat,hn=qosh(holat,blok,R,c); trace.append(('Qosh_inj9',j,holat.copy(),ke.copy()))
            holat=bzf(holat,hn,c); trace.append(('BZ9',j,holat.copy(),ke.copy()))
    return holat
Res={}
for p,bz in [(256,'std'),(256,'sbz'),(16,'std'),(16,'sbz')]:
    c=Cfg(p,bz); msb=p//2; N=3000
    for case in ['D0a','D0b']:
        k=rand_keys(N,p); h=rng.integers(0,p,(N,32)); bl=rng.integers(0,p,(N,32))
        h2=h.copy()
        if case=='D0a': h2[:,0]^=msb
        else: h2[:,0]^=msb; h2[:,9]^=msb
        t1=[];t2=[]
        rounds_from(h,bl,k.copy(),k,c,t1); rounds_from(h2,bl,k.copy(),k,c,t2)
        rows=[]
        for (nm,j,a,ka),(_,_,b,kb) in zip(t1,t2):
            d=a^b; dk=ka^kb; act=(d!=0).sum(1)
            msbonly=float((((d==0)|(d==msb)).all(1)&((dk==0)|(dk==msb)).all(1)).mean())
            cnt=collections.Counter(map(bytes,np.concatenate([d,dk],1).astype(np.uint8))); top=cnt.most_common(1)[0][1]/N
            rows.append(dict(op=nm,j=j,act=round(float(act.mean()),2),actk=round(float((dk!=0).sum(1).mean()),2),msb=round(msbonly,4),top=round(top,4),hd=round(float(hw(d,p).mean()),1)))
        Res[f'{p}_{bz}_{case}']=rows
        print(p,bz,case,[(r['op'][:4],r['j'],r['act'],r['actk'],r['msb']) for r in rows if r['op'] in ('Tuz','BZ8','BZ9')])
json.dump(Res,open('dif3.json','w'),indent=0)
