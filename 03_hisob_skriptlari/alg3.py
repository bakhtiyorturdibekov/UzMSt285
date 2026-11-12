import numpy as np, json, math
from vc import *
from lin2 import Pm, Mmat, rank2
rng=np.random.default_rng(31); R={}
def gf2_solve(X,Y):
    """X:(m,n) 0/1, Y:(m,k). Eng kichik kvadratlar emas - aniq yechim (Gauss)."""
    A=np.concatenate([X,Y],1).astype(np.uint8)%2; m,n=X.shape; r=0; piv=[]
    for col in range(n):
        idx=[i for i in range(r,m) if A[i,col]]
        if not idx: continue
        A[[r,idx[0]]]=A[[idx[0],r]]
        for i in range(m):
            if i!=r and A[i,col]: A[i]^=A[r]
        piv.append(col); r+=1
    W=np.zeros((n,Y.shape[1]),dtype=np.uint8)
    for i,col in enumerate(piv): W[col]=A[i,n:]
    return W
for p,bz in [(16,'std'),(16,'sbz'),(256,'std'),(256,'sbz')]:
    c=Cfg(p,bz); bl=32 if p==256 else 16
    if p==256: k=rng.integers(0,256,32); k[0]&=0xFE; k[1]&=0xFE
    else: k=rng.integers(0,256,16); k[0]&=0xEE
    def H(msgs): return hash_msgs(msgs,np.tile(k,(len(msgs),1)),c)
    def feats(msgs):
        u=to_units(msgs,p)%2; return np.concatenate([u,np.ones((len(msgs),1),dtype=np.int64)],1)
    tr=rng.integers(0,256,(80,bl)); te=rng.integers(0,256,(300,bl))
    Wt=gf2_solve(feats(tr),H(tr)%2)
    pred=(feats(te)@Wt)%2; act=H(te)%2
    R[f'{p}_{bz}']={'full_vec':float((pred==act).all(1).mean()),'per_bit':round(float((pred==act).mean()),4)}
    print(p,bz,R[f'{p}_{bz}'])
# Aralash yadrosi: nol ustunlar va teng ustun juftlari
zc=0;eq=0;N=300
for t in range(N):
    k=rng.integers(0,256,32); k[0]&=0xFE; k[1]&=0xFE
    M=Mmat(k); cols=[tuple(M[:,i]) for i in range(32)]
    zc+= any(sum(cc)==0 for cc in cols); eq+= len(set(cols))<32
R['keys_zero_col']=zc/N; R['keys_equal_cols']=eq/N
# SBZ: P(dy=0x80 | dn=0x80, dh=0)
x=np.arange(256)
DS=np.zeros((256,256),dtype=np.int64)
for d in range(256): DS[d]=np.bincount(S^S[x^d],minlength=256)
R['SBZ_80to80']=float((DS[0x80]*DS[:,0x80]).sum()/65536)
print(R)
# Tenglamalar soni (bit darajasida)
def counts(n,mode):
    w=32
    ADD=(2*n-1,2*n-1,n-1); MUL=(n*(n+1)//2+(n-1)*(2*n-1),)*2+(n*(n+1)//2+(n-1)*(n-1),)
    def add(a,b,f=1): return tuple(x+f*y for x,y in zip(a,b))
    z=(0,0,0)
    # Qo'sh: 2 massiv x 3 bosqich
    q=z
    for arr in range(2):
        q=add(q,ADD,(w-1)*2)            # J1,J2
        q=add(q,MUL,(w-1)*2)            # K1,K2 ko'paytmalar zanjiri
        q=add(q,(2*n,2*n,2*n),4)        # Δ=10 taqqoslashlari
        q=add(q,MUL,1)                  # K1*K2
        q=add(q,ADD,w*2*2)              # A1,B1 ; A2,B2 har element
        q=add(q,MUL,w*3*3)              # har bosqich: R*x, A*x, y*d
        q=add(q,ADD,w*3*2)              # B+Rx, manfiy
        q=add(q,(n,n,n),w)              # nol holat tekshiruvi
    ar=add(add(z,MUL,128),ADD,144)
    tz=add(add(z,ADD,w),(n,n,n),w)
    if mode=='sbz':
        nb=w if n==8 else w//2; bz=(16*nb,78*nb,78*nb)
    elif mode=='std' and n==8: bz=(8*w,43*2*w+8*w,43*2*w)    # Z: kubik implitsit
    else: bz=(0,n*w,0)
    rnd=add(add(add(ar,q,2),tz),z)
    return dict(qosh=q,aralash=ar,tuzilma=tz,bz=bz,raund=rnd)
EQ={}
for n,lab in [(8,'256'),(4,'128')]:
    for mode in ['std','sbz']:
        cc=counts(n,mode)
        r0=tuple(a+b for a,b in zip(cc['qosh'],cc['bz']))
        r1=tuple(a+b for a,b in zip(r0,cc['raund'])); r2=tuple(a+b for a,b in zip(r1,cc['raund'])); r3=tuple(a+b for a,b in zip(r2,cc['raund']))
        cc.update(r0=r0,r1=r1,r2=r2,r3=r3); EQ[f'{lab}_{mode}']=cc
print(EQ)
# Linearizatsiya murakkabligi
def lg2C(nv,d): return math.log2(sum(math.comb(nv,i) for i in range(d+1)))
LC={f'{nv}_{d}':round(lg2C(nv,d)*2.8,1) for nv in (128,256) for d in (1,6,7,8,13,20)}
R['lin_cost']=LC; R['eq']=EQ
json.dump(R,open('alg3.json','w'),indent=1,default=list); print(LC)
