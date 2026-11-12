import sys; sys.path.insert(0,'/home/claude/pkg/uzmst285_tahlil')
import numpy as np, json
from algoritm import Cfg, aralash, qosh, surholat, surkalit, tuz
from komponentlar import kalitlar, L_raund, rank2
from yagona import aralash_y, boglash_y, surholat_y, surkalit_y, RC, iteration_g
rng=np.random.default_rng(11); X={}
ranks=[rank2(L_raund(kalitlar(rng,1,256)[0])) for _ in range(1000)]
X['rank_hist']={str(r):ranks.count(r) for r in range(min(ranks),33)}
def bits(a): return ((a[:,:,None]>>np.arange(8))&1).reshape(len(a),-1)
c=Cfg(256,'std')
def round_std(h,k):
    ke=k.copy(); R=k[:,0]
    h=aralash(h,ke,c); h,ke=qosh(h,ke,R,c); h=surholat(h); ke=surkalit(ke); h,ke=qosh(h,ke,R,c); return h
def round_new(h,k):
    ke=k|1; Rp=k[:,0]&0xFE
    h=aralash_y(h,ke,8); h=boglash_y(h,ke,Rp); h=surholat_y(h,8); ke=(surkalit_y(ke,8)^RC[1])|1; h=boglash_y(h,ke,Rp); return h
for nm,f in (('std',round_std),('new',round_new)):
    N=150; k=kalitlar(rng,N,256); h=rng.integers(0,256,(N,32)); yb=bits(f(h,k)); S=np.zeros((256,256))
    for i in range(256):
        h2=h.copy(); h2[:,i//8]^=1<<(i%8); S[i]=(yb^bits(f(h2,k))).mean(0)
    np.save(f'/home/claude/paper/sac_{nm}.npy',S); X[f'sac_{nm}']=[float(S.mean()),float((S==0).mean())]
# integral: holat[0,0] faol, raundlar bo'yicha LSB balansi (yangilangan, R=6, 20 tajriba)
bal=[]
for t in range(20):
    k=rng.integers(0,256,32); k[0]&=0xFE; h=rng.integers(0,256,32); b=rng.integers(0,256,32)
    H=np.tile(h,(256,1)); H[:,0]=np.arange(256); K=np.tile(k,(256,1)); tr=[]
    iteration_g(H,np.tile(b,(256,1)),K.copy(),K,6,trace=tr)
    bal.append([int(((np.bitwise_xor.reduce(hh,axis=0)&1)==0).sum()) for nm,j,hh,kk in tr if nm=='raund'])
X['int_new_min']=np.array(bal).min(0).tolist(); X['int_new_mean']=np.array(bal).mean(0).round(1).tolist()
json.dump(X,open('/home/claude/paper/extra.json','w')); print(X['rank_hist'],X['sac_std'],X['sac_new'],X['int_new_min'],X['int_new_mean'])
