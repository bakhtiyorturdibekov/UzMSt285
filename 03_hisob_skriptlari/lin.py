import numpy as np, json, itertools
from vc import *
rng=np.random.default_rng(2025)
R={}
def wht(f):  # f: +-1 vector length 2^n
    a=f.astype(np.int64).copy(); h=1; n=len(a)
    while h<n:
        a=a.reshape(-1,2,h); a=np.stack([a[:,0]+a[:,1],a[:,0]-a[:,1]],1).reshape(-1); h*=2
    return a
par8=np.array([bin(i).count('1')&1 for i in range(256)])
def lat(F,nin,nout):  # W[b][a]
    W=np.zeros((1<<nout,1<<nin),dtype=np.int64)
    for b in range(1<<nout):
        W[b]=wht(1-2*par8[F & b] if nout<=8 else None)
    return W
WS=lat(S,8,8); WZ=lat(Z,8,4)
def dist(W):
    v,cn=np.unique(np.abs(W[1:,:]),return_counts=True); return {int(a):int(b) for a,b in zip(v,cn)}
R['S_lat_max']=int(np.abs(WS[1:,:]).max()); R['S_lat_dist']=dist(WS)
R['Z_lat_max']=int(np.abs(WZ[1:,:]).max()); R['Z_lat_dist']=dist(WZ)
# eng yaxshi S approksimatsiyalari soni
R['S_best_count']=int((np.abs(WS[1:,1:])==32).sum())
# misol: S uchun eng yaxshi niqob
b,a=np.argwhere(np.abs(WS[1:,1:])==32)[0]; R['S_example']=(int(a+1),int(b+1),int(WS[b+1,a+1]))
# Z eng yaxshi
b,a=np.argwhere(np.abs(WZ[1:,:])==R['Z_lat_max'])[0]; R['Z_example']=(int(a),int(b+1),int(WZ[b+1,a]))
# SBZ: c((alfa,beta)->gamma)=cS(alfa->gamma)*cS(beta->alfa)
CS=WS/256.0
best=0; cnt=0; ex=None
for g in range(1,256):
    row=np.abs(CS[g])  # over alfa
    for al in range(1,256):
        v=row[al]*np.abs(CS[al]).max()
        if v>best+1e-12: best=v; ex=(al,int(np.argmax(np.abs(CS[al]))),g)
R['SBZ_corr_max']=best; R['SBZ_example']=ex
# max |c| uchun (alfa,beta,gamma) uchliklar soni
m=(np.abs(WS)==16).astype(np.int64)
R['SBZ_best_triples']=int((m[1:,1:].T @ m[1:,:]).sum()) if False else int(sum(m[g,1:].dot(m[1:,1:].sum(0)*0+0) for g in range(0)) )
cntb=0
M16=(np.abs(WS)==32)
for g in range(1,256):
    al=np.nonzero(M16[g,1:])[0]+1
    for a_ in al: cntb+=int(M16[a_,1:].sum())
R['SBZ_best_triples']=cntb
# Qo'sh bitta element: tasodifiy parametrlar bilan LAT
def qosh_elem(A1,B1,A2,B2,Rv,p=256):
    x=np.arange(p); INV=np.zeros(p,dtype=np.int64)
    for t in range(1,p,2): INV[t]=pow(t,-1,p)
    s=lambda x,A,B: (-A*x*INV[(B+Rv*x)%p])%p
    y1=s(x,A1,B1); y2=s(y1,A2,B2); y2=np.where(y2==0,(A2+B2)%p,y2); return s(y2,A2,B2)
qmax=[]; bitc=np.zeros(8); trials=200; lsb_ok=0
for t in range(trials):
    A1,B1,A2,B2=[int(rng.integers(0,128))*2+1 for _ in range(4)]; Rv=int(rng.integers(0,128))*2
    f=qosh_elem(A1,B1,A2,B2,Rv); W=lat(f,8,8)
    Wn=np.abs(W.copy()); Wn[1,1]=0; Wn[0,:]=0
    qmax.append(int(Wn.max()))
    for j in range(8): bitc[j]+=abs(W[1<<j,1<<j])/256
    lsb_ok+= (W[1,1]==256)
R['Qosh_lsb_corr1_frac']=lsb_ok/trials
R['Qosh_lat_max_nontriv_median']=float(np.median(qmax)); R['Qosh_lat_max_nontriv_max']=int(max(qmax)); R['Qosh_lat_max_nontriv_min']=int(min(qmax))
R['Qosh_bitj_corr_avg']=(bitc/trials).round(4).tolist()
json.dump(R,open('lin1.json','w'),indent=1,default=float); print(json.dumps(R,indent=1,default=float))
# bit-qatlam bo'yicha Qo'sh: chiqish bit j uchun max|c| (istalgan kirish niqobi)
layer=np.zeros(8); layer_min=np.ones(8)
for t in range(trials):
    A1,B1,A2,B2=[int(rng.integers(0,128))*2+1 for _ in range(4)]; Rv=int(rng.integers(0,128))*2
    f=qosh_elem(A1,B1,A2,B2,Rv); W=lat(f,8,8)
    for j in range(8):
        v=np.abs(W[1<<j]).max()/256; layer[j]+=v; layer_min[j]=min(layer_min[j],v)
R['Qosh_bitj_bestcorr_avg']=(layer/trials).round(4).tolist(); R['Qosh_bitj_bestcorr_min']=layer_min.round(4).tolist()
# Z va SBZ uchun chiqishning 0-biti (gamma=1) bo'yicha eng yaxshi korrelyatsiya
R['Z_out_bit0_best']=float(np.abs(WZ[1]).max()/256)
R['SBZ_gamma1_best']=float(max(abs(CS[1,a])*np.abs(CS[a]).max() for a in range(1,256)))
R['SBZ_gamma1_alpha_low']=float(max(abs(CS[1,a])*np.abs(CS[a]).max() for a in [1,2,3]))
json.dump(R,open('lin1.json','w'),indent=1,default=float)
print({k:R[k] for k in ['S_best_count','S_example','SBZ_best_triples','Qosh_bitj_bestcorr_avg','Qosh_bitj_bestcorr_min','Z_out_bit0_best','SBZ_gamma1_best','SBZ_gamma1_alpha_low']})
