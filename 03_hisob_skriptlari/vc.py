"""Vektorlashtirilgan O'zMSt 285:2024 1-algoritm (standart va SBZ), p=256 va p=16."""
import numpy as np, sys
sys.path.insert(0,'/mnt/user-data/outputs')
from uzmst285_alg1 import ZICHLASH
Z=np.array(list(ZICHLASH),dtype=np.int64)
def aes_sbox():
    s=[0]*256; p=q=1
    while True:
        p ^= (p<<1) ^ (0x1b if p&0x80 else 0); p&=0xff
        q ^= q<<1; q ^= q<<2; q ^= q<<4; q&=0xff
        if q&0x80: q^=0x09
        x=q ^ ((q<<1|q>>7)&0xff) ^ ((q<<2|q>>6)&0xff) ^ ((q<<3|q>>5)&0xff) ^ ((q<<4|q>>4)&0xff)
        s[p]=x^0x63
        if p==1: break
    s[0]=0x63; return np.array(s,dtype=np.int64)
S=aes_sbox()
class Cfg:
    def __init__(s,p=256,bz='sbz'):
        s.p=p; s.bz=bz
        s.INV=np.zeros(p,dtype=np.int64)
        for x in range(1,p,2): s.INV[x]=pow(x,-1,p)
def prododd(a,p):
    b=np.where(a%2==0,a+1,a)%p; r=np.ones(a.shape[0],dtype=np.int64)
    for i in range(a.shape[1]): r=(r*b[:,i])%p
    return r
def dK(P,Jo,p): return np.where((P==(Jo+1)%p)|(P==(-(Jo+1))%p),10,0)
def step(x,A,B,R,c):
    d=(B+R*x)%c.p; return (-A*x*c.INV[d])%c.p
def qosh(h,hn,R,c):
    p=c.p; R=R[:,None]
    J1h=h.sum(1)%p; J1hn=hn.sum(1)%p
    Ph=prododd(h,p); Phn=prododd(hn,p)
    K1h=(Ph+dK(Ph,J1hn,p))%p; K1hn=(Phn+dK(Phn,J1h,p))%p
    dAh=np.where(J1hn%2==1,0,1); dAhn=np.where(J1h%2==1,0,1)
    A1h=(J1hn[:,None]+2*hn+dAh[:,None])%p; A1hn=(J1h[:,None]+2*h+dAhn[:,None])%p
    h1=step(h,A1h,(K1h[:,None]-2*h)%p,R,c); hn1=step(hn,A1hn,(K1hn[:,None]-2*hn)%p,R,c)
    J2h=h1.sum(1)%p; J2hn=hn1.sum(1)%p
    P2h=prododd(h1,p); P2hn=prododd(hn1,p)
    K2h=(P2h+dK(P2h,J2hn,p))%p; K2hn=(P2hn+dK(P2hn,J2h,p))%p
    dA2h=np.where((J1hn+J2hn)%2==1,0,1); dA2hn=np.where((J1h+J2h)%2==1,0,1)
    A2h=(J1hn[:,None]+J2hn[:,None]+2*hn1+dA2h[:,None])%p; A2h=np.where(A2h==0,1,A2h)
    A2hn=(J1h[:,None]+J2h[:,None]+2*h1+dA2hn[:,None])%p; A2hn=np.where(A2hn==0,1,A2hn)
    B2h=((K1h*K2h)[:,None]-2*h1)%p; B2hn=((K1hn*K2hn)[:,None]-2*hn1)%p
    h2=step(h1,A2h,B2h,R,c); h2=np.where(h2==0,(A2h+B2h)%p,h2)
    hn2=step(hn1,A2hn,B2hn,R,c); hn2=np.where(hn2==0,(A2hn+B2hn)%p,hn2)
    return step(h2,A2h,B2h,R,c), step(hn2,A2hn,B2hn,R,c)
def bzf(h,hn,c):
    if c.p==256:
        if c.bz=='std': return (Z[h]<<4)|Z[hn]
        return S[h^S[hn]]
    if c.bz=='std': return h^hn
    H=16*h[:,0::2]+h[:,1::2]; N=16*hn[:,0::2]+hn[:,1::2]; Q=S[H^S[N]]
    out=np.empty_like(h); out[:,0::2]=Q>>4; out[:,1::2]=Q&15; return out
def dia(H,K,p):  # H,K: (N,4,4)
    sk=K.sum(1)            # sum_i K[i,u]  -> (N,4)
    sh=H.sum(1)            # sum_i H[i,u]
    R=np.empty_like(H)
    for s in range(4):
        for u in range(4):
            if s==u:
                v=H[:,u,u]*sk[:,u]-sum(H[:,i,i]*K[:,i,u] for i in range(4) if i!=u)
            else:
                v=H[:,s,u]*sk[:,u]+K[:,s,u]*sh[:,u]-sum(H[:,s,i]*K[:,i,u] for i in range(4) if i not in (s,u))
            R[:,s,u]=v%p
    return R
def aralash(h,ke,c):
    H=h.reshape(-1,4,8); K=ke.reshape(-1,4,8)
    L=dia(H[:,:,:4],K[:,:,:4],c.p); Rr=dia(H[:,:,4:],K[:,:,4:],c.p)
    return np.concatenate([L,Rr],axis=2).reshape(-1,32)
def _shift(h,rows,cols):
    m=h.reshape(-1,4,8).copy()
    for s in range(4): m[:,s,:]=np.roll(m[:,s,:],rows[s],axis=1)
    for u,n in cols.items(): m[:,:,u]=np.roll(m[:,:,u],n,axis=1)
    return m.reshape(-1,32)
def surholat(h): return _shift(h,[1,2,3,4],{0:1,4:1,1:2,5:2,2:3,6:3})
def surkalit(ke): return _shift(ke,[4,3,2,1],{1:-3,5:-3,2:-2,6:-2,3:-1,7:-1})
def tuz(ke,k,c):
    p=c.p
    return np.where((ke==0)&(k%2==0),2,np.where((ke!=0)&(ke%2==k%2),ke,(ke-1)%p))
def iteration(holat,blok,ke,k,c,trace=None,rounds=10):
    """Bitta tashqi iteratsiya (i): Qo'sh+BZ, so'ng 'rounds' ta bosqich."""
    R=k[:,0]
    def T(name,j,h,kk):
        if trace is not None: trace.append((name,j,h.copy(),kk.copy()))
    holat,hn=qosh(holat,blok,R,c); T('Qosh0',0,holat,ke)
    holat=bzf(holat,hn,c); T('BZ0',0,holat,ke)
    for j in range(1,rounds+1):
        holat=aralash(holat,ke,c); T('Aralash',j,holat,ke)
        holat,ke=qosh(holat,ke,R,c); T('Qosh1',j,holat,ke)
        holat=surholat(holat); ke=surkalit(ke); T('Sur',j,holat,ke)
        if j==8:
            holat,hn=qosh(holat,blok,R,c); T('Qosh_inj8',j,holat,ke); holat=bzf(holat,hn,c); T('BZ8',j,holat,ke)
        else:
            holat,ke=qosh(holat,ke,R,c); T('Qosh2',j,holat,ke)
        ke=tuz(ke,k,c); T('Tuz',j,holat,ke)
        if j==9:
            holat,hn=qosh(holat,blok,R,c); T('Qosh_inj9',j,holat,ke); holat=bzf(holat,hn,c); T('BZ9',j,holat,ke)
    return holat,ke
def to_units(b,p):
    b=np.asarray(b,dtype=np.int64)
    if p==256: return b
    out=np.empty(b.shape[:-1]+(b.shape[-1]*2,),dtype=np.int64); out[...,0::2]=b>>4; out[...,1::2]=b&15; return out
def hash_msgs(msgs,keys,c):
    """msgs: (N,L) bayt, L - blok uzunligiga karrali; keys: (N,32 yoki 16)."""
    N,L=msgs.shape; bl=32 if c.p==256 else 16
    nb=L//bl; bits=L*8
    blocks=[msgs[:,i*bl:(i+1)*bl] for i in range(nb)]
    ny=[0]*N
    nyb=np.zeros((N,bl),dtype=np.int64)
    for n in range(N):
        v=sum(int.from_bytes(bytes(b[n].tolist()),'big') for b in blocks)%(2**(8*bl))
        nyb[n]=list(v.to_bytes(bl,'big'))
    lb=np.tile(np.array(list(bits.to_bytes(bl,'big'))),(N,1))
    kir=[to_units(b,c.p) for b in blocks]+[to_units(lb,c.p),to_units(nyb,c.p)]
    k=to_units(keys,c.p); ke=k.copy(); holat=kir[0]
    for i in range(1,len(kir)): holat,ke=iteration(holat,kir[i],ke,k,c)
    return holat
