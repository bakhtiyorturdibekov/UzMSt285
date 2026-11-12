from run2 import *
import itertools
res=[]
for p in [30,15,16]:
    for v1 in range(256):
        for v2 in range(256):
            c=[0]*32; c[p]=v1; c[p+1]=v2
            a,b=Q(h1,to2(c))
            if hx(b)==exp_hn and hx(a)==exp_h: res.append((p,v1,v2))
print(res)
