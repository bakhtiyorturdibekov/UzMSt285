import sys; sys.path.insert(0,'/mnt/user-data/outputs')
import uzmst285_alg1 as U
from loc import S
k=bytes.fromhex("c86ed4b2756df1cd6b6eca81d441809221ab81bba0c7c15044be8feb934f95a2")
std=U.bayt_zichlash
def sbz(h,hn): return [int(S[a^S[b]]) for a,b in zip(h,hn)]
for nm,bz in [("Standart",std),("SBZ",sbz)]:
    U.bayt_zichlash=bz
    for m in [b"", b"funksiyaxeshirovaniyainformasionnayatexnologiyakriptograficheska", b"abc"]:
        print(nm, repr(m[:10]), U.xesh(m,k).hex())
