import q, t
from b import aralash
from a import surholat, surkalit, tuz
D=t.D; q.R=0xc8
V=dict(bump=0,kc=0,a2lit=0,stop1=0)
def to2(a): return [a[8*s:8*s+8] for s in range(4)]
def fl(m): return [x for r in m for x in r]
def Q(h,hn):
    a,b=q.qosh(fl(h),fl(hn),V); return to2(a),to2(b)
def BZ(h,hn): return [[(D[h[s][u]]<<4)|D[hn[s][u]] for u in range(8)] for s in range(4)]
def hx(m): return ' '.join(f'{x:02x}' for x in fl(m))
def hesh(blocks,k,log=None):
    K=to2(k); ke=to2(k); holat=to2(blocks[0])
    for i in range(1,len(blocks)):
        nb=to2(blocks[i])
        holat,holatn=Q(holat,nb)
        if log is not None: log.append((i,'Qosh0',hx(holat),hx(holatn)))
        holat=BZ(holat,holatn)
        for j in range(1,11):
            holat=aralash(holat,ke)
            holat,ke=Q(holat,ke)
            holat=surholat(holat); ke=surkalit(ke)
            if j==8:
                holat,holatn=Q(holat,nb); holat=BZ(holat,holatn)
            else:
                holat,ke=Q(holat,ke)
            ke=tuz(ke,K)
            if j==9:
                holat,holatn=Q(holat,nb); holat=BZ(holat,holatn)
    return holat
k=t.__dict__.get('k') or __import__('a').k
