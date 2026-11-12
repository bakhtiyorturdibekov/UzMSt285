import numpy as np, sys
sys.path.insert(0,'/mnt/user-data/outputs')
from uzmst285_alg1 import ZICHLASH
Z=np.array(list(ZICHLASH))
# AES S-box
def aes_sbox():
    s=[0]*256; p=q=1
    while True:
        p ^= (p<<1) ^ (0x1b if p&0x80 else 0); p&=0xff
        q ^= q<<1; q ^= q<<2; q ^= q<<4; q&=0xff
        if q&0x80: q^=0x09
        x=q ^ ((q<<1|q>>7)&0xff) ^ ((q<<2|q>>6)&0xff) ^ ((q<<3|q>>5)&0xff) ^ ((q<<4|q>>4)&0xff)
        s[p]=x^0x63
        if p==1: break
    s[0]=0x63; return np.array(s)
S=aes_sbox(); assert S[0]==0x63 and S[1]==0x7c and S[0x53]==0xed
h=np.arange(65536)>>8; n=np.arange(65536)&255
F={"BZ256":(Z[h]<<4)|Z[n], "XOR16":( ( (h>>4)^(n>>4) )<<4 ) | ((h&15)^(n&15)), "SBZ":S[h^S[n]]}
def bits(v,k): return ((v[:,None]>>np.arange(k))&1)
def walsh_max(f,ob):
    # max |W| over in-mask (16 bit) and nonzero out-mask
    best=0
    for b in range(1,1<<ob):
        g=np.array([bin(x).count('1')&1 for x in range(256)])[f & b] if False else None
        par=np.zeros(65536,dtype=np.int64)
        v=f&b
        while v.any(): par^=v&1; v=v>>1
        w=1-2*par.astype(np.int64)
        # fast WHT
        a=w.copy(); hh=1
        while hh<65536:
            a=a.reshape(-1,2,hh); a=np.stack([a[:,0]+a[:,1],a[:,0]-a[:,1]],1).reshape(-1); hh*=2
        best=max(best,np.abs(a).max())
    return best/65536
def ddt_max(f):
    best=(0,None); vanish_h=0; vanish_n=0
    x=np.arange(65536)
    for d in range(1,65536):
        dy=f^f[x^d]; c=np.bincount(dy,minlength=256)
        m=c.max()
        if m>best[0]: best=(m,(hex(d),hex(c.argmax())))
        if d<256: vanish_n=max(vanish_n,c[0])
        if d&255==0: vanish_h=max(vanish_h,c[0])
    return best[0]/65536,best[1],vanish_h/65536,vanish_n/65536
def anf_deg(f,ob):
    deg=0; wt=np.array([bin(i).count('1') for i in range(65536)])
    for j in range(ob):
        a=((f>>j)&1).astype(np.uint8).copy(); hh=1
        while hh<65536:
            a=a.reshape(-1,2,hh); a[:,1]^=a[:,0]; a=a.reshape(-1); hh*=2
        deg=max(deg,wt[a==1].max())
    return deg
def sac_bic(f,ob):
    x=np.arange(65536); O=bits(f,ob)
    M=np.zeros((16,ob)); bic=0
    for i in range(16):
        D=bits(f^f[x^(1<<i)],ob); M[i]=D.mean(0)
        C=np.corrcoef(D.T)
        C=np.nan_to_num(C); np.fill_diagonal(C,0); bic=max(bic,np.abs(C).max())
    return M.min(),M.max(),M.mean(),bic,(M>0).sum()
for nm,f in F.items():
    ob=8
    print(nm,"DDT/so'nish:",ddt_max(f),"| maks corr:",walsh_max(f,ob),"| daraja:",anf_deg(f,ob),"| SAC/BIC/bog'liq:",sac_bic(f,ob))
# 8->4 local table
x=np.arange(256); best=(0,None)
for d in range(1,256):
    c=np.bincount(Z^Z[x^d],minlength=16); 
    if c.max()>best[0]: best=(c.max(),(hex(d),c.argmax()))
print("Z 8->4 DDT max:",best)
