from run2 import *
best=(0,None)
for p in range(32):
    for v in range(256):
        c=[0]*32; c[p]=v
        a,b=Q(h1,to2(c))
        sc=sum(x==y for x,y in zip(hx(b).split(),exp_hn.split()))+sum(x==y for x,y in zip(hx(a).split(),exp_h.split()))
        if sc>best[0]: best=(sc,(p,v))
print(best)
