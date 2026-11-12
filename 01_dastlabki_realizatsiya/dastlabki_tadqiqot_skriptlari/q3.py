import itertools, q
from q2 import h,hn,eh,ehn
q.R=0xc8
for bump,kc,a2lit,stop1 in itertools.product([0,1],[0,1],[0,1],[0,1]):
    V=dict(bump=bump,kc=kc,a2lit=a2lit,stop1=stop1); res=q.qosh(h,hn,V)
    if res: print(V, sum(a==b for a,b in zip(res[0]+res[1],eh+ehn)))
# birinchi Qo'sh: xabar bloklari
msg=q.msg; b1=list(msg[:32]); b2=list(msg[32:])
V=dict(bump=0,kc=0,a2lit=0,stop1=0)
for name,(x,y) in {"satr":(b1,b2), "ustun":([b1[4*u+s] for s in range(4) for u in range(8)],[b2[4*u+s] for s in range(4) for u in range(8)])}.items():
    res=q.qosh(x,y,V); print("1-Qo'sh, xabar",name,"bo'yicha:", sum(a==b for a,b in zip(res[0]+res[1],q.exp_h+q.exp_hn)),"/64")
