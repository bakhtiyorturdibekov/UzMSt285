import itertools
from a import M,k,krow,kcol,eq
def dia(H,K,p=256):
    R=[[0]*4 for _ in range(4)]
    for s in range(4):
        for u in range(4):
            sk=sum(K[i][u] for i in range(4))
            if s==u:
                v=H[u][u]*sk - sum(H[i][i]*K[i][u] for i in range(4) if i!=u)
            else:
                v=H[s][u]*sk + K[s][u]*sum(H[i][u] for i in range(4)) - sum(H[s][i]*K[i][u] for i in range(4) if i not in (s,u))
            R[s][u]=v%p
    return R
def aralash(h,ke):
    L=dia([r[:4] for r in h],[r[:4] for r in ke]); Rr=dia([r[4:] for r in h],[r[4:] for r in ke])
    return [L[s]+Rr[s] for s in range(4)]
h=M("44 a6 2b c4 3c 65 d7 7a 79 7d c7 b8 26 2a 8d c7 df cd 8b 5b 5c 4d 49 cf 24 4f 1d cb f6 17 88 d9")
exp=M("4a 9f 4a b9 0d 04 84 65 91 f6 ca 1b 13 e6 82 5b 4d fa 23 1e 6f cc f6 b9 9e 36 96 45 78 23 7b d9")
r=aralash(h,krow); eq(r,exp,"Aralash (ke=k satr bo'yicha):")
for row in r: print(' '.join(f'{x:02x}' for x in row))
# j=8 for i=1 : need ke before; use TuzilmaKalit output of j=7 not given. Check i=1 j=9: holat after BZ (a2 c6..) and ke = TuzilmaKalit j=8 (dc 66 ...)
h=M("a2 c6 bb e8 21 4e f3 44 78 4b 6f 61 13 a5 dc ac 26 70 30 b2 49 bd 30 b1 2e a7 59 52 40 3b 2d da")
ke=M("dc 66 44 b6 fb 25 5d 59 b1 62 88 49 16 73 fe 80 09 d5 2b 17 d6 27 a7 16 4e b2 dd c5 c7 21 8b dc")
eq(aralash(h,ke),M("c1 23 f0 f3 aa 6e 83 cd 79 a5 67 a7 8c 31 89 61 0a f0 16 3d c7 cf 5f 0c e4 f8 4b 47 bb d0 e3 c5"),"Aralash i=1 j=9:")
