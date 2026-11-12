import numpy as np, random, sys
sys.path.insert(0,'/mnt/user-data/outputs'); import uzmst285_alg1 as U
U.P=2
def rank2(A):
    A=A.copy()%2; r=0; rows,cols=A.shape
    for c in range(cols):
        p=[i for i in range(r,rows) if A[i,c]]
        if not p: continue
        A[[r,p[0]]]=A[[p[0],r]]
        for i in range(rows):
            if i!=r and A[i,c]: A[i]^=A[r]
        r+=1
    return r
random.seed(7); ranks=[]; zr=0; N=2000
for t in range(N):
    kp=[random.getrandbits(1) for _ in range(32)]; kp[0]=0; kp[1]=0
    Mx=np.array([U.aralash([1 if j==i else 0 for j in range(32)],kp) for i in range(32)]).T  # ustun = e_i obrazi
    ranks.append(rank2(Mx)); zr+= any(not Mx[i].any() for i in range(32))
ranks=np.array(ranks)
print("o'rtacha rang:",ranks.mean(),"min-max:",ranks.min(),ranks.max(),"to'liq rang ulushi:",(ranks==32).mean(),"nol satrli kalitlar:",zr/N)
