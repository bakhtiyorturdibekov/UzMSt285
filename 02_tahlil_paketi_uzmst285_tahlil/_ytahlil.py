import numpy as np, json, collections, math
from algoritm import Cfg, S, to_units, aralash, surholat
from komponentlar import kalitlar, lat, ddt, rank2, L_raund
from boglash import boglash, juftlash, INV
from yakuniy_variant import iteration_y, xesh_y, kirish
from algebraik import gf2_solve
rng=np.random.default_rng(2026); R={}
x=np.arange(256)
# ---------------- A1: element akslantirishi g(x)=S(f_{a,b}(x) ^ t)
lm=[];dm=[];lq=[]
for t_ in range(200):
    a=int(rng.integers(0,128))*2+1; b=int(rng.integers(0,128))*2+1; Rv=int(rng.integers(0,128))*2; t=int(rng.integers(0,256))
    f=(-a*x*INV[(b+Rv*x)%256])%256; g=S[f^t]
    W=lat(g,8); lm.append(int(np.abs(W[1:]).max())); D=ddt(g,256); dm.append(int(D[1:].max()))
    lq.append(int(np.abs(W[1:,1]).max()))
R['g_lat_max']={str(k):v for k,v in sorted(collections.Counter(lm).items())}; R['g_ddt_max']={str(k):v for k,v in sorted(collections.Counter(dm).items())}
print('element g: LAT maks taqsimoti',R['g_lat_max'],' DDT maks taqsimoti',R['g_ddt_max'])
# ---------------- A2: massiv darajasida bitta chaqiruv
def bitsu(a,p):
    nb=8 if p==256 else 4; return ((a[:,:,None]>>np.arange(nb))&1).reshape(len(a),-1)
for p in (256,16):
    r={}; nb=8 if p==256 else 4; msb=p//2
    N=6000; H=rng.integers(0,p,(N,32)); X=rng.integers(0,p,(N,32)); Rv=rng.integers(0,128,N)*2; Y=boglash(H,X,Rv,p)
    r['y0=x0']=round(float(((Y&1)==(H&1)).mean()),3)
    Xb=1-2*bitsu(H,p).astype(float); Yb=1-2*bitsu(Y,p).astype(float); r['bit_bit']=round(float((np.abs(Yb.T@Xb)/N).max()),3); r['shovqin']=round(4.5/math.sqrt(N),3)
    H2=H.copy(); H2[:,0]^=msb; D=Y^boglash(H2,X,Rv,p); r['msb_faqat']=round(float(((D==0)|(D==msb)).all(1).mean()),3); r['faol']=round(float((D!=0).sum(1).mean()),1)
    N=200; H=rng.integers(0,p,(N,32)); X=rng.integers(0,p,(N,32)); Rv=rng.integers(0,128,N)*2; Yb=bitsu(boglash(H,X,Rv,p),p); SAC=np.zeros((32*nb,32*nb))
    for i in range(32*nb):
        H2=H.copy(); H2[:,i//nb]^=1<<(i%nb); SAC[i]=(Yb^bitsu(boglash(H2,X,Rv,p),p)).mean(0)
    r['sac']=[round(float(SAC.mean()),3),round(float((SAC==0).mean()),3),round(float(SAC.min()),3)]
    # integral: bitta faol bayt (256) / juftlangan bayt (128)
    cnt=collections.Counter(); zb=[]
    for t in range(40):
        h=rng.integers(0,p,32); xx=rng.integers(0,p,32); Rv=np.full(256,int(rng.integers(0,128))*2)
        HH=np.tile(h,(256,1))
        if p==256: HH[:,0]=np.arange(256)
        else: HH[:,0]=np.arange(256)>>4; HH[:,1]=np.arange(256)&15
        YY=boglash(HH,np.tile(xx,(256,1)),Rv,p); s_=np.bitwise_xor.reduce(YY,axis=0)
        for i in range(32):
            nd=len(np.unique(YY[:,i])); cnt['C' if nd==1 else ('A' if nd==p and p==256 else ('B' if s_[i]==0 else 'U'))]+=1
        zb.append(((s_&1)==0).mean())
    r['integral']={k:round(v/40,2) for k,v in cnt.items()}; r['integral_0qatlam']=round(float(np.mean(zb)),3)
    R[f'bog_{p}']=r; print('Bog‘lash',p,r,flush=True)
# ---------------- B: raundlar
def keys(N,p):
    if p==256: return kalitlar(rng,N,256)
    k=rng.integers(0,16,(N,32)); k[:,0]&=0xE; k[:,1]&=0xE; return k
for p in (256,16):
    c=Cfg(p,'sbz'); msb=p//2; r={}
    # B1: bit->bit korrelyatsiya, 1 va 2 raunddan keyin (raund kirishidan)
    for nr in (1,2):
        N=6000; k=keys(N,p); h=rng.integers(0,p,(N,32)); bl=rng.integers(0,p,(N,32)); tr=[]
        iteration_y(h,bl,k.copy(),k,c,trace=tr,rounds=nr)
        h0=[t[2] for t in tr if t[0]=='SBZ0'][0]; hr=tr[-1][2]
        Xb=1-2*bitsu(h0,p).astype(float); Yb=1-2*bitsu(hr,p).astype(float); r[f'bit_bit_{nr}']=round(float((np.abs(Yb.T@Xb)/N).max()),3)
    # 0-qatlam tenglamasi L bilan
    N=600; k=keys(N,p); h=rng.integers(0,p,(N,32)); bl=rng.integers(0,p,(N,32)); tr=[]
    iteration_y(h,bl,k.copy(),k,c,trace=tr); cur=[t[2] for t in tr if t[0]=='SBZ0'][0]%2; Ls=[L_raund(k[n]|1) for n in range(N)]; cl=[]
    for j in range(1,11):
        cur=np.array([(Ls[n]@cur[n])%2 for n in range(N)]); act=[t for t in tr if t[1]==j][-1][2]%2; cl.append(round(2*float((cur==act).mean())-1,3))
    r['qatlam0_c']=cl
    # B2: differensial — yutishdan keyingi holatda MSB ayirmasi (raund kirishi), akslantirishlar bo'yicha
    N=2000; k=keys(N,p); h=rng.integers(0,p,(N,32)); bl=rng.integers(0,p,(N,32)); t1=[];t2=[]
    iteration_y(h,bl,k.copy(),k,c,trace=t1)
    h0=[t[2] for t in t1 if t[0]=='SBZ0'][0]
    # ikkinchi ishga tushirish: holatni SBZ0 dan keyin almashtirish uchun 0-raunddan boshlash qiyin; shuning uchun boshlang'ich holat ayirmasi (D1) ishlatiladi
    h2=h.copy(); h2[:,0]^=msb; iteration_y(h2,bl,k.copy(),k,c,trace=t2)
    r['D1']=[(nm,j,round(float(((a^b)!=0).sum(1).mean()),1),round(float(((((a^b)==0)|((a^b)==msb)).all(1)).mean()),3),round(float(((a==b).all(1)).mean()),4)) for (nm,j,a,ka),(_,_,b,kb) in zip(t1,t2) if j<=2 or nm in ('SBZ8','SBZ9') or (nm=='Bog2' and j in (7,10))]
    # D2: blokdagi ikki elementli MSB ayirmasi
    bl2=bl.copy(); bl2[:,0]^=msb; bl2[:,9]^=msb; t3=[]; iteration_y(h,bl2,k.copy(),k,c,trace=t3)
    r['D2']=[(nm,j,round(float(((a^b)!=0).sum(1).mean()),1),round(float(((a==b).all(1)).mean()),4)) for (nm,j,a,ka),(_,_,b,kb) in zip(t1,t3) if j<=1 or nm in ('SBZ8','SBZ9')]
    # B3: kub testlari
    kub={}
    for rr_ in (0,1):
        for d in (4,8,10):
            allz=None
            for cc in range(4):
                kk=keys(1,p)[0]; hh=rng.integers(0,p,32); b0=rng.integers(0,p,32); ub=8 if p==256 else 4
                pos=rng.choice(16,d,replace=False); Nn=1<<d; Bm=np.tile(b0,(Nn,1))
                for t_,q in enumerate(pos):
                    u_,bb=q//ub,q%ub; Bm[:,u_]&=~(1<<bb); Bm[:,u_]|=((np.arange(Nn)>>t_)&1)<<bb
                K=np.tile(kk,(Nn,1)); o,_=iteration_y(np.tile(hh,(Nn,1)),Bm,K.copy(),K,c,rounds=rr_)
                s_=np.bitwise_xor.reduce(o,axis=0); zb=np.array([(s_>>j)&1 for j in range(ub)]).T==0
                allz=zb if allz is None else allz&zb
            kub[f'r{rr_}_d{d}']=[round(float(allz.mean()),3),round(float(allz[:,0].mean()),3)]
    r['kub']=kub
    # B4: integral raundlar bo'yicha (holat faol, boshlang'ich holat) va blok faol
    for joy in ('holat','blok'):
        recs={}
        for t in range(20):
            kk=keys(1,p)[0]; hh=rng.integers(0,p,32); b0=rng.integers(0,p,32); Nn=256
            HH=np.tile(hh,(Nn,1)); BB=np.tile(b0,(Nn,1)); T_=HH if joy=='holat' else BB
            if p==256: T_[:,0]=np.arange(256)
            else: T_[:,0]=np.arange(256)>>4; T_[:,1]=np.arange(256)&15
            K=np.tile(kk,(Nn,1)); tr=[]; iteration_y(HH,BB,K.copy(),K,c,trace=tr,rounds=3)
            for nm,j,a,kk2 in tr:
                s_=np.bitwise_xor.reduce(a,axis=0); recs.setdefault(f'{j}:{nm}',[]).append(np.array([((s_>>b)&1)==0 for b in range(8 if p==256 else 4)]))
        r[f'integral_{joy}']={k_:np.array(v).all(0).sum(1).tolist() for k_,v in recs.items()}
    R[f'raund_{p}']=r; print('raund',p,{kk:r[kk] for kk in ('bit_bit_1','bit_bit_2','qatlam0_c','kub')},flush=True)
# ---------------- C: chiqish darajasi
for p in (256,16):
    bl=32 if p==256 else 16; r={}
    ranks=[];cmin=1
    for t in range(3):
        k=kalitlar(rng,1,256)[0][:bl] if p==256 else rng.integers(0,256,16)
        if p==16: k[0]&=0xEE
        m=rng.integers(0,256,(300,64)); o=xesh_y(m,np.tile(k,(300,1)),p)%2; ranks.append(rank2((o[1:]^o[0]).T.copy())); cmin=min(cmin,float(o.mean(0).min()))
    r['rang']=ranks; r['min_chastota']=round(cmin,3)
    feat=lambda mm: np.concatenate([to_units(mm,p)%2,np.ones((len(mm),1),dtype=np.int64)],1)
    tr=rng.integers(0,256,(80,bl)); te=rng.integers(0,256,(200,bl)); KK=lambda n:np.tile(k,(n,1))
    W=gf2_solve(feat(tr),xesh_y(tr,KK(80),p)%2); r['affin_0']=round(float(((feat(te)@W)%2==xesh_y(te,KK(200),p)%2).mean()),3)
    z=[]
    for t in range(10):
        mm=rng.integers(0,256,bl); M=np.tile(mm,(256,1)); M[:,0]=np.arange(256); s_=np.bitwise_xor.reduce(xesh_y(M,KK(256),p),axis=0); z.append(np.array([((s_>>b)&1)==0 for b in range(8 if p==256 else 4)]))
    r['integral_toliq']=np.array(z).all(0).sum(1).tolist()
    N=300; m=rng.integers(0,256,(N,2*bl)); kk=np.tile(k,(N,1)); o=xesh_y(m,kk,p); m2=m.copy(); pos=rng.integers(0,2*bl*8,N); m2[np.arange(N),pos//8]^=(1<<(pos%8)); o2=xesh_y(m2,kk,p)
    hd=bitsu(o^o2,p).sum(1); r['HD']=[round(float(hd.mean()),1),int(hd.min()),int(hd.max())]; fl=bitsu(o^o2,p).mean(0); r['bit_ehtimol']=[round(float(fl.min()),2),round(float(fl.max()),2)]
    R[f'chiqish_{p}']=r; print('chiqish',p,r,flush=True)
json.dump(R,open('/home/claude/ka/yakuniy_tahlil.json','w'),default=lambda o: o.tolist() if hasattr(o,'tolist') else int(o))
