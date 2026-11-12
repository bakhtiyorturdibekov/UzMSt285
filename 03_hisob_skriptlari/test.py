from vc import *
A=b"funksiyaxeshirovaniyainformasionnayatexnologiyakriptograficheska"
k=bytes.fromhex("c86ed4b2756df1cd6b6eca81d441809221ab81bba0c7c15044be8feb934f95a2")
M=np.array([list(A)]); K=np.array([list(k)])
def hx(u,p):
    u=u[0]; 
    if p==16: u=[u[2*i]<<4|u[2*i+1] for i in range(16)]
    return bytes(int(x) for x in u).hex()
for p in [256,16]:
    for bz in ['std','sbz']:
        c=Cfg(p,bz); print(p,bz,hx(hash_msgs(M,K if p==256 else K[:,:16],c),p))
