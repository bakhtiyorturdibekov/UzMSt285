from run2 import *
import itertools, full
c=list((512).to_bytes(32,'big'))
for bump,kc,a2lit in itertools.product([0,1],[0,1],[0,1]):
    full.V.update(bump=bump,kc=kc,a2lit=a2lit)
    a,b=Q(h1,to2(c))
    sc=sum(x==y for x,y in zip(hx(b).split()+hx(a).split(),exp_hn.split()+exp_h.split()))
    print(bump,kc,a2lit,sc)
