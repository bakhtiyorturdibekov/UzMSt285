from run2 import *
c=[0]*32; c[16]=64; c[30]=194
a,b=Q(h1,to2(c))
for i,(x,y) in enumerate(zip(hx(a).split(),exp_h.split())):
    if x!=y: print("holat",i,x,y)
for i,(x,y) in enumerate(zip(hx(b).split(),exp_hn.split())):
    if x!=y: print("holatn",i,x,y)
