import numpy as np, json
from vc import *
from lin import qosh_elem
rng=np.random.default_rng(11); R={}
x=np.arange(256)
def ddt(F,nout):
    D=np.zeros((256,nout),dtype=np.int64)
    for d in range(256): D[d]=np.bincount(F^F[x^d],minlength=nout)
    return D
DS=ddt(S,256); DZ=ddt(Z,16)
R['S_ddt_max']=int(DS[1:].max()); v,c=np.unique(DS[1:],return_counts=True); R['S_ddt_dist']={int(a):int(b) for a,b in zip(v,c)}
R['Z_ddt_max']=int(DZ[1:].max()); R['Z_ddt_argmax']=[hex(int(i)) for i in np.unravel_index(DZ[1:].argmax(),DZ[1:].shape)]
R['Z_ddt_argmax'][0]=hex(int(R['Z_ddt_argmax'][0],16)+1)
v,c=np.unique(DZ[1:],return_counts=True); R['Z_ddt_dist']={int(a):int(b) for a,b in zip(v,c)}
R['Z_row_80']=DZ[0x80].tolist(); R['Z_row_08']=DZ[0x08].tolist(); R['Z_row_01']=DZ[0x01].tolist(); R['Z_row_96']=DZ[0x96].tolist()
R['Z_vanish_count']=int((DZ[1:,0]>0).sum()); R['Z_vanish_max']=int(DZ[1:,0].max())
# SBZ: (dh=0, dn=0x80) va (dh=0x80,dn=0) taqsimotining maksimumi
def sbz_dist(dh,dn):
    tot=np.zeros(256)
    for d in range(256):
        if DS[dn,d]: tot+=DS[dn,d]*DS[dh^d] if dn else 0
    if dn==0: tot=DS[dh]*256.0
    return tot/65536
R['SBZ_dn80_max']=float(sbz_dist(0,0x80).max()); R['SBZ_dh80_max']=float(sbz_dist(0x80,0).max())
R['SBZ_dn80_vanish']=float(sbz_dist(0,0x80)[0]); R['SBZ_both80_vanish']=float(sbz_dist(0x80,0x80)[0])
# Qo'sh element DDT (belgilangan parametrlar)
mx=[];p80=[];pj={j:[] for j in range(8)}; tri=[]
for t in range(200):
    A1,B1,A2,B2=[int(rng.integers(0,128))*2+1 for _ in range(4)]; Rv=int(rng.integers(0,128))*2
    f=qosh_elem(A1,B1,A2,B2,Rv); D=ddt(f,256)
    mx.append(int(D[1:].max())); p80.append(D[0x80,0x80]/256)
    for j in range(8): pj[j].append(D[1<<j].max()/256)
    # T-funksiya: 2^j farq quyi bitlarga o'tmaydimi
    tri.append(all(((f^f[x^(1<<j)]) & ((1<<j)-1)).max()==0 for j in range(8)))
R['Qosh_ddt_max_median']=float(np.median(mx)); R['Qosh_ddt_max_max']=int(max(mx))
R['Qosh_p80_mean']=float(np.mean(p80)); R['Qosh_p80_min']=float(np.min(p80))
R['Qosh_pj_best_mean']=[round(float(np.mean(pj[j])),4) for j in range(8)]
R['Qosh_Tfunc_all']=bool(all(tri))
json.dump(R,open('dif1.json','w'),indent=1); print(json.dumps({k:v for k,v in R.items() if not k.startswith('Z_row')},indent=0)); print('Z80',R['Z_row_80']); print('Z96',R['Z_row_96']); print('Z01',R['Z_row_01'])
