import sys, itertools; sys.path.insert(0,'/mnt/user-data/outputs')
import uzmst285_alg1 as U
from loc import S
U.P=16
k=bytes.fromhex("c86ed4b2756df1cd6b6eca81d441809221ab81bba0c7c15044be8feb934f95a2")[:16]
def nib(b): return [x for y in b for x in (y>>4, y&15)]
def unnib(a): return bytes(a[2*i]<<4|a[2*i+1] for i in range(16))
def bz_xor(h,hn): return [a^b for a,b in zip(h,hn)]
def bz_sbz(h,hn):
    out=[]
    for j in range(16):
        H=16*h[2*j]+h[2*j+1]; N=16*hn[2*j]+hn[2*j+1]; Q=int(S[H^S[N]]); out+= [Q>>4, Q&15]
    return out
def xesh128(M,k,bz,lenbytes=16,ny_mod=128):
    bits=len(M)*8
    M = M + b"\x00"*(-len(M)%16) if M else b"\x00"*16
    bl=[M[i:i+16] for i in range(0,len(M),16)]
    ny=sum(int.from_bytes(b,'big') for b in bl)%2**ny_mod
    kir=[nib(b) for b in bl]+[nib(bits.to_bytes(16,'big')), nib(ny.to_bytes(16,'big'))]
    kk=nib(k); R=kk[0]; ke=kk[:]; holat=kir[0]
    for i in range(1,len(kir)):
        blok=kir[i]
        holat,hn=U.qosh(holat,blok,R); holat=bz(holat,hn)
        for j in range(1,11):
            holat=U.aralash(holat,ke); holat,ke=U.qosh(holat,ke,R)
            holat,ke=U.sur_holat(holat),U.sur_kalit(ke)
            if j==8: holat,hn=U.qosh(holat,blok,R); holat=bz(holat,hn)
            else: holat,ke=U.qosh(holat,ke,R)
            ke=U.tuzilma_kalit(ke,kk)
            if j==9: holat,hn=U.qosh(holat,blok,R); holat=bz(holat,hn)
    return unnib(holat)
if __name__=="__main__":
    exp={("std",b""):"86882acce4e8a2e8a42e48288eca28e2",("std","A"):"e9eaccdd4ccce2d229228c864989eb9f",("std",b"abc"):"bea2c2d7133fc1c4a9446e66ea88adf3",
         ("sbz",b""):"8524b2987285223cb2c2886bb73a3dd7",("sbz","A"):"bd745e2ed572ea4246ed68482ef46c5e",("sbz",b"abc"):"5696f8e9e74cc9e8b6b3c4ab356a1b72"}
    A=b"funksiyaxeshirovaniyainformasionnayatexnologiyakriptograficheska"
    for (v,m),e in exp.items():
        mm=A if m=="A" else m
        r=xesh128(mm,k,bz_xor if v=="std" else bz_sbz).hex()
        print(v, repr(mm[:6]), r, "MOS" if r==e else "farq")
