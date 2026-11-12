import os, random, numpy as np
from k128 import *
random.seed(1)
def L0(b): return [x&1 for x in nib(b)]
def rk():  # R (1-nibble) juft
    while True:
        k=bytearray(os.urandom(16)); k[0]&=0xEF  # yuqori nibble juft
        return bytes(k)
def flip_hi(b):  # har nibble ning 1-3 bitlarini tasodifiy o'zgartirish
    return bytes(x ^ (random.getrandbits(8)&0xEE) for x in b)
ok=[0,0,0,0]; N=30
for t in range(N):
    k=rk(); m=os.urandom(16)
    ok[0]+= L0(xesh128(m,k,bz_xor))==L0(xesh128(flip_hi(m),k,bz_xor))      # T1, 1 blok
    k2=bytes([k[0]^ (random.getrandbits(8)&0x6E)])+flip_hi(k[1:])            # R juftligi saqlanadi
    ok[1]+= L0(xesh128(m,k,bz_xor))==L0(xesh128(m,k2,bz_xor))                # T2
    m2=os.urandom(32)
    ok[2]+= L0(xesh128(m2,k,bz_xor))==L0(xesh128(flip_hi(m2),k,bz_xor))    # 2 blok, NY o'zgaradi
    ok[3]+= L0(xesh128(m,k,bz_sbz))==L0(xesh128(flip_hi(m),k,bz_sbz))
print("T1 (1 blok) std:",ok[0],"/",N," | T2 kalit std:",ok[1],"/",N," | 2 blok, NY ko'chirishli std:",ok[2],"/",N," | T1 SBZ:",ok[3],"/",N)
# R toq bo'lsa
fail=0
for t in range(20):
    k=bytearray(os.urandom(16)); k[0]|=0x10
    try: xesh128(os.urandom(16),bytes(k),bz_xor)
    except ValueError: fail+=1
print("R toq: teskari mavjud bo'lmagan holatlar:",fail,"/ 20")
fail=0
import uzmst285_alg1 as U2
