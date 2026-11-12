import numpy as np, json, time
from yagona import *
from algoritm import KAT_XABAR, KAT_KALIT
from komponentlar import rank2
from algebraik import gf2_solve
rng=np.random.default_rng(31); Rz={}
print('RC1:',bytes(RC[1][:8].tolist()).hex(),' C1:',bytes(C1[:8].tolist()).hex())
Rz['KAT']={f'{bl}_{R}':xesh_bayt_g(KAT_XABAR,KAT_KALIT,bl,R).hex() for bl in (32,16) for R in (10,6,5,4)}
for k,v in Rz['KAT'].items(): print('KAT',k,v)
# Aralash 4x4 teskarilanuvchimi (toq kₑ)?
from komponentlar import rank2 as r2
def M44():
    E=np.eye(16,dtype=np.int64).reshape(16,4,4); K=np.ones((16,4,4),dtype=np.int64)
    return (dia(E,K,2).reshape(16,16).T)%2
Rz['aralash44_rang']=int(r2(M44())); print('4×4 Aralash (toq kₑ) rangi mod 2:',Rz['aralash44_rang'])
def bitsb(a): return ((a[:,:,None]>>np.arange(8))&1).reshape(len(a),-1)
def keys(N,bl):
    k=rng.integers(0,256,(N,bl)); k[:,0]&=0xFE; return k
for bl in (32,16):
    for R in (3,4,5,6,8,10):
        r={}
        N=300; m=rng.integers(0,256,(N,2*bl)); k=keys(N,bl); o=xesh_g(m,k,R)
        m2=m.copy(); pos=rng.integers(0,2*bl*8,N); m2[np.arange(N),pos//8]^=(1<<(pos%8)); o2=xesh_g(m2,k,R)
        hd=bitsb(o^o2).sum(1); fl=bitsb(o^o2).mean(0); r['HD']=[round(float(hd.mean()),1),int(hd.min()),int(hd.max())]; r['bit']=[round(float(fl.min()),2),round(float(fl.max()),2)]
        kk=keys(1,bl)[0]; KK=lambda n:np.tile(kk,(n,1))
        mm=rng.integers(0,256,(300,2*bl)); oo=xesh_g(mm,KK(300),R)%2; r['rang']=int(rank2((oo[1:]^oo[0]).T.copy())); r['minf']=round(float(oo.mean(0).min()),3)
        feat=lambda x_: np.concatenate([x_%2,np.ones((len(x_),1),dtype=np.int64)],1)
        tr=rng.integers(0,256,(80,bl)); te=rng.integers(0,256,(200,bl))
        W=gf2_solve(feat(tr),xesh_g(tr,KK(80),R)%2); r['affin']=round(float(((feat(te)@W)%2==xesh_g(te,KK(200),R)%2).mean()),3)
        z=[]
        for t in range(8):
            mm=rng.integers(0,256,bl); M=np.tile(mm,(256,1)); M[:,0]=np.arange(256); s_=np.bitwise_xor.reduce(xesh_g(M,KK(256),R),axis=0); z.append(np.array([((s_>>b)&1)==0 for b in range(8)]))
        r['integral']=int(np.array(z).all(0).sum())
        # bitta iteratsiya: ichki ko'chki (holat biti -> chiqish), R raund
        N=150; h=rng.integers(0,256,(N,bl)); b_=rng.integers(0,256,(N,bl)); k=keys(N,bl); y,_=iteration_g(h,b_,k.copy(),k,R); yb=bitsb(y); SAC=np.zeros((8*bl,8*bl))
        for i in range(8*bl):
            h2=h.copy(); h2[:,i//8]^=1<<(i%8); y2,_=iteration_g(h2,b_,k.copy(),k,R); SAC[i]=(yb^bitsb(y2)).mean(0)
        r['sac_iter']=[round(float(SAC.mean()),3),round(float(SAC.min()),3),round(float(SAC.max()),3)]
        Rz[f'{bl}_{R}']=r; print(bl,R,r,flush=True)
json.dump(Rz,open('/home/claude/ka/yagona_raund.json','w'))
