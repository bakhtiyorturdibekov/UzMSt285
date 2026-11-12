import itertools, functools
from a import M
msg=b"funksiyaxeshirovaniyainformasionnayatexnologiyakriptograficheska"
b1=list(msg[:32]); b2=list(msg[32:64])
exp_h=[int(x,16) for x in "8a ff 7e 0d b7 8b 49 25 f8 25 a1 68 43 12 91 be 9d be a9 d1 bf 37 d2 f6 8f d2 73 a1 5d 9f c5 5e".split()]
exp_hn=[int(x,16) for x in "8a 17 b1 fb 24 c3 f8 86 df ec 11 07 17 e9 b3 af 4a 01 70 d4 0d 35 46 b9 e6 b9 49 68 4f 11 c5 29".split()]
r=256; R=0x6e
def inv(x):
    try: return pow(x%r,-1,r)
    except ValueError: return None
def prododd(a):
    p=1
    for x in a: p=p*(x+1 if x%2==0 else x)%r
    return p
def J(a): return sum(a)%r
def step(x, A, B):
    d=(B+R*x)%r; i=inv(d)
    if i is None: return None
    return (-A*x*i)%r
def qosh(h, hn, V):
    Jh, Jhn = J(h), J(hn)
    Ph, Phn = prododd(h), prododd(hn)
    # Delta for A
    dA_h = 0 if Jhn%2==1 else 1
    dA_hn= 0 if Jh%2==1 else 1
    # Delta for K
    def dK(P,Jo):
        c=[(Jo+1)%r, (-(Jo+1))%r]
        return 10 if P in c else 0
    K1h=(Ph+dK(Ph, Jhn if V['kc'] else Jh))%r
    K1hn=(Phn+dK(Phn, Jh if V['kc'] else Jhn))%r
    o1h=[];o1hn=[]
    for x,y in zip(h,hn):
        A1h=(Jhn+2*y+dA_h)%r; A1hn=(Jh+2*x+dA_hn)%r
        xx = x+1 if (V['bump'] and x%2==0) else x
        yy = y+1 if (V['bump'] and y%2==0) else y
        B1h=(K1h-2*xx)%r; B1hn=(K1hn-2*yy)%r
        o1h.append((step(xx,A1h,B1h),A1h,B1h)); o1hn.append((step(yy,A1hn,B1hn),A1hn,B1hn))
    if any(t[0] is None for t in o1h+o1hn): return None
    h1=[t[0] for t in o1h]; hn1=[t[0] for t in o1hn]
    if V['stop1']: return h1,hn1
    J2h,J2hn=J(h1),J(hn1); P2h,P2hn=prododd(h1),prododd(hn1)
    K2h=(P2h+dK(P2h, J2hn if V['kc'] else J2h))%r
    K2hn=(P2hn+dK(P2hn, J2h if V['kc'] else J2hn))%r
    if V['a2lit']:
        dA2h = 0 if (Jh+J2h)%2==1 else 1; dA2hn = 0 if (Jhn+J2hn)%2==1 else 1
    else:
        dA2h = 0 if (Jhn+J2hn)%2==1 else 1; dA2hn = 0 if (Jh+J2h)%2==1 else 1
    oh=[];ohn=[]
    for x,y in zip(h1,hn1):
        A2h=(Jhn+J2hn+2*y+dA2h)%r or 1; A2hn=(Jh+J2h+2*x+dA2hn)%r or 1
        xx = x+1 if (V['bump'] and x%2==0) else x
        yy = y+1 if (V['bump'] and y%2==0) else y
        B2h=(K1h*K2h-2*xx)%r; B2hn=(K1hn*K2hn-2*yy)%r
        x2=step(xx,A2h,B2h); y2=step(yy,A2hn,B2hn)
        if x2 is None or y2 is None: return None
        if x2==0: x2=(A2h+B2h)%r
        if y2==0: y2=(A2hn+B2hn)%r
        x3=step(x2,A2h,B2h); y3=step(y2,A2hn,B2hn)
        if x3 is None or y3 is None: return None
        oh.append(x3); ohn.append(y3)
    return oh,ohn
best=[]
for bump,kc,a2lit,stop1 in itertools.product([0,1],[0,1],[0,1],[0,1]):
    V=dict(bump=bump,kc=kc,a2lit=a2lit,stop1=stop1)
    res=qosh(b1,b2,V)
    if res is None: print(V,"teskari mavjud emas"); continue
    sh=sum(a==b for a,b in zip(res[0],exp_h)); shn=sum(a==b for a,b in zip(res[1],exp_hn))
    print(V, sh, shn)
