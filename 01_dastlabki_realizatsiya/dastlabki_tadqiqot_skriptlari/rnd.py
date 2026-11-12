import numpy as np
from scipy.stats import chi2
rng=np.random.default_rng(3); x=np.arange(256)
H=np.array([[(-1)**bin(a&b).count('1') for b in range(256)] for a in range(256)])
def met(T):
    d=max(np.bincount(T^T[x^dd],minlength=16).max() for dd in range(1,256))
    par=np.array([[bin(v&b).count('1')&1 for v in T] for b in range(1,16)])
    w=np.abs((1-2*par)@H).max()
    return d,w
import sys; sys.path.insert(0,'/mnt/user-data/outputs'); from uzmst285_alg1 import ZICHLASH
Z=np.array(list(ZICHLASH))
print("Z:",met(Z>>0 & 15))
R=[met(rng.permutation(np.repeat(np.arange(16),16))) for _ in range(300)]
R=np.array(R); print("tasodifiy 300 ta mediana DDT, Walsh:",np.median(R[:,0]),np.median(R[:,1]))
print("chi2 kritik (alfa=0.01, Bonferroni): 128 bit:",round(chi2.isf(0.01/128,1),1),"256 bit:",round(chi2.isf(0.01/256,1),1))
for v in [16.0,19.4,13.5,21.7]: print(v,"p =",chi2.sf(v,1))
