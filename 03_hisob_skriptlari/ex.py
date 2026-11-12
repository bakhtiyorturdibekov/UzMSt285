import numpy as np, json
from vc import *
from lin import lat, qosh_elem, rng
WS=lat(S,8,8); WZ=lat(Z,8,4)
x=np.arange(256)
DS=np.array([np.bincount(S^S[x^d],minlength=256) for d in range(256)])
E={}
E['S_lat_block']=[[int(WS[b,a]) for a in range(1,9)] for b in range(1,9)]   # qator: chiqish niqobi b, ustun: kirish niqobi a
E['Z_lat_block']=[[int(WZ[b,a]) for a in [1,2,4,8,0x10,0x20,0x40,0x80,0xC5]] for b in range(1,16)]
E['S_ddt_block']=[[int(DS[d,y]) for y in range(8)] for d in range(1,9)]
v,c=np.unique(DS[1:],return_counts=True); E['S_ddt_dist']={int(a):int(b) for a,b in zip(v,c)}
E['SBZ_sign']=(int(WS[1,45]),int(WS[45,26]))
# Qo'sh daraja medianasi
def anf_deg(fb):
    a=fb.astype(np.uint8).copy(); h=1
    while h<256:
        a=a.reshape(-1,2,h); a[:,1]^=a[:,0]; a=a.reshape(-1); h*=2
    wt=np.array([bin(i).count('1') for i in range(256)]); nz=wt[a==1]; return int(nz.max()) if len(nz) else -1
D=[]
for t in range(100):
    A1,B1,A2,B2=[int(rng.integers(0,128))*2+1 for _ in range(4)]; Rv=int(rng.integers(0,128))*2
    f=qosh_elem(A1,B1,A2,B2,Rv); D.append([anf_deg((f>>j)&1) for j in range(8)])
E['Qosh_deg_median']=np.median(np.array(D),0).tolist()
json.dump(E,open('ex.json','w'),indent=0); print(E['S_lat_block'][:3],E['S_ddt_dist'],E['SBZ_sign'],E['Qosh_deg_median'])
