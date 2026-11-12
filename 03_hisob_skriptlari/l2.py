import numpy as np
from lin import qosh_elem, lat, rng
for t in range(3):
    A1,B1,A2,B2=[int(rng.integers(0,128))*2+1 for _ in range(4)]; Rv=int(rng.integers(0,128))*2
    f=qosh_elem(A1,B1,A2,B2,Rv); W=lat(f,8,8)
    idx=np.argwhere(np.abs(W)>=128); print([(int(b),int(a),int(W[b,a])) for b,a in idx if b>0][:20])
    print("bijektiv:",len(set(f.tolist())))
