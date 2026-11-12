from run2 import *
r=256; R=q.R
h=fl(h1); eh=[int(x,16) for x in exp_h.split()]
Jh=sum(h)%r; Ph=q.prododd(h)
inv=q.inv
sols=[]
for Jhn in range(256):
    dA=0 if Jhn%2 else 1
    K1h=(Ph+(10 if Ph in [(Jh+1)%r,(-(Jh+1))%r] else 0))%r
    h1v=[q.step(x,(Jhn+dA)%r,(K1h-2*x)%r) for x in h]  # hn=0 assumed for all positions
    if None in h1v: continue
    J2h=sum(h1v)%r; P2=q.prododd(h1v); K2h=(P2+(10 if P2 in [(J2h+1)%r,(-(J2h+1))%r] else 0))%r
    for J2hn in range(256):
        dA2=0 if (Jhn+J2hn)%2 else 1
        good=[]
        for idx,x in enumerate(h):
            if idx in (16,30): continue
            A2=(Jhn+J2hn+0+dA2)%r or 1  # hn^-1=0 at zero positions
            B2=(K1h*K2h-2*h1v[idx])%r
            x2=q.step(h1v[idx],A2,B2)
            if x2 is None: break
            if x2==0: x2=(A2+B2)%r
            x3=q.step(x2,A2,B2)
            if x3!=eh[idx]: break
        else: sols.append((Jhn,J2hn))
print(sols)
