import itertools, q
from a import k
h=[int(x,16) for x in "4a 9f 4a b9 0d 04 84 65 91 f6 ca 1b 13 e6 82 5b 4d fa 23 1e 6f cc f6 b9 9e 36 96 45 78 23 7b d9".split()]
hn=k[:]  # ke = k (satr bo'yicha)
eh=[int(x,16) for x in "56 eb 86 59 d3 84 24 1b ab c2 fe c9 c3 fe 5e 87 5b da f1 4e 3f 3c 8e ed 82 42 96 ff d8 fd 91 d9".split()]
ehn=[int(x,16) for x in "a8 9a 64 2e dd 37 cb 35 a7 ae 6a fd cc 6f 80 e6 f1 49 8d d1 60 21 0f f0 f4 be d5 ff e5 7f 79 fe".split()]
best=(0,None)
for Rv in range(256):
    q.R=Rv
    for bump,kc,a2lit,stop1 in itertools.product([0,1],[0,1],[0,1],[0,1]):
        V=dict(bump=bump,kc=kc,a2lit=a2lit,stop1=stop1)
        res=q.qosh(h,hn,V)
        if res is None: continue
        sc=sum(a==b for a,b in zip(res[0],eh))+sum(a==b for a,b in zip(res[1],ehn))
        if sc>best[0]: best=(sc,(Rv,V))
print("eng yaxshi moslik (64 dan):",best)
