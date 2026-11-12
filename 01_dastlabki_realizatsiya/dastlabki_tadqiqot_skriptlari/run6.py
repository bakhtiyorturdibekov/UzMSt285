from run2 import *
res=[];best=(0,None)
for v1 in range(256):
    for v2 in range(256):
        c=[0]*32; c[16]=v1; c[30]=v2
        a,b=Q(h1,to2(c))
        sc=sum(x==y for x,y in zip(hx(b).split()+hx(a).split(),exp_hn.split()+exp_h.split()))
        if sc>best[0]: best=(sc,(v1,v2))
print(best)
