exec(open('t.py').read().split("import re")[0]) if False else None
import t  # loads D
D=t.D
def M(s): 
    v=[int(x,16) for x in s.split()]; return [v[8*r:8*r+8] for r in range(4)]
def eq(a,b,name): print(name, "MOS ✓" if a==b else "MOS EMAS ✗")
k=[int(x,16) for x in "c8 6e d4 b2 75 6d f1 cd 6b 6e ca 81 d4 41 80 92 21 ab 81 bb a0 c7 c1 50 44 be 8f eb 93 4f 95 a2".split()]
# BaytZichlash 256
def BZ(h,hn): return [[(D[h[s][u]]<<4)|D[hn[s][u]] for u in range(8)] for s in range(4)]
h=M("8a ff 7e 0d b7 8b 49 25 f8 25 a1 68 43 12 91 be 9d be a9 d1 bf 37 d2 f6 8f d2 73 a1 5d 9f c5 5e")
hn=M("8a 17 b1 fb 24 c3 f8 86 df ec 11 07 17 e9 b3 af 4a 01 70 d4 0d 35 46 b9 e6 b9 49 68 4f 11 c5 29")
eq(BZ(h,hn),M("44 a6 2b c4 3c 65 d7 7a 79 7d c7 b8 26 2a 8d c7 df cd 8b 5b 5c 4d 49 cf 24 4f 1d cb f6 17 88 d9"),"BaytZichlash i=1 boshi:")
h=M("86 24 03 bc 50 8a 4a d2 b4 09 e3 5a 52 3e 5e ba e8 36 34 d4 61 59 82 eb e8 ba 3a f2 d2 15 d5 f0")
hn=M("96 e3 59 53 04 13 78 e6 a9 d4 9b a5 b7 bf 87 19 02 1f 30 a4 df d7 2a c1 a6 c7 71 e8 a3 03 ab 1b")
eq(BZ(h,hn),M("a2 c6 bb e8 21 4e f3 44 78 4b 6f 61 13 a5 dc ac 26 70 30 b2 49 bd 30 b1 2e a7 59 52 40 3b 2d da"),"BaytZichlash i=1 j=8:")
# SurHolat
def surholat(h):
    a=[row[:] for row in h]
    for s in range(4):
        n=s+1; a[s]=a[s][-n:]+a[s][:-n]   # o'ngga
    b=[row[:] for row in a]
    sh={0:1,4:1,1:2,5:2,2:3,6:3}
    for u,n in sh.items():
        col=[a[s][u] for s in range(4)]
        col=col[-n:]+col[:-n]  # pastga
        for s in range(4): b[s][u]=col[s]
    return b
eq(surholat(M("56 eb 86 59 d3 84 24 1b ab c2 fe c9 c3 fe 5e 87 5b da f1 4e 3f 3c 8e ed 82 42 96 ff d8 fd 91 d9")),
   M("d8 8e ab 86 82 f1 c3 24 1b fd ed c2 59 42 4e fe 5e 56 91 5b fe d3 96 3f 3c 87 eb d9 da c9 84 ff"),"SurHolat i=1 j=1:")
def surkalit(h):
    a=[row[:] for row in h]
    for s in range(4):
        n=4-s; a[s]=a[s][-n:]+a[s][:-n]
    b=[row[:] for row in a]
    sh={1:3,5:3,2:2,6:2,3:1,7:1}
    for u,n in sh.items():
        col=[a[s][u] for s in range(4)]
        col=col[n:]+col[:n]  # yuqoriga
        for s in range(4): b[s][u]=col[s]
    return b
eq(surkalit(M("a8 9a 64 2e dd 37 cb 35 a7 ae 6a fd cc 6f 80 e6 f1 49 8d d1 60 21 0f f0 f4 be d5 ff e5 7f 79 fe")),
   M("dd f4 f1 a7 a8 e5 60 cc 6f 37 be 49 ae 9a 7f 21 0f 80 cb d5 8d 6a 64 79 fe f0 e6 35 ff d1 fd 2e"),"SurKalit i=1 j=1:")
def tuz(ke,kk):
    out=[]
    for s in range(4):
        r=[]
        for u in range(8):
            x=ke[s][u]; kv=kk[s][u]
            if x==0 and kv%2==0: x=2
            elif x!=0 and x%2==kv%2: pass
            else: x=(x-1)%256
            r.append(x)
        out.append(r)
    return out
krow=[k[8*r:8*r+8] for r in range(4)]
kcol=[[k[4*u+s] for u in range(8)] for s in range(4)]
ke=M("27 34 59 55 28 89 a0 9c 1b f7 62 2f c2 b2 1d ef 0d 80 6b 45 2b 1e 64 49 ae 90 02 29 95 8d 8f 6a")
exp=M("26 34 58 54 27 89 9f 9b 1b f6 62 2f c2 b1 1c ee 0d 7f 6b 45 2a 1d 63 48 ae 90 01 29 95 8d 8f 6a")
eq(tuz(ke,krow),exp,"TuzilmaKalit (k satr bo'yicha joylashgan):")
eq(tuz(ke,kcol),exp,"TuzilmaKalit (k ustun bo'yicha joylashgan):")
