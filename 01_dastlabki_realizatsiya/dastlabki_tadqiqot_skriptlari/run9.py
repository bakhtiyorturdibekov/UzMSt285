import itertools, full
from full import *
msg=q.msg; b1=list(msg[:32]); b2=list(msg[32:])
L=list((512).to_bytes(32,'big'))
I=lambda b:int.from_bytes(bytes(b),'big')
cands={
 "BE yig'indi (b1+b2)": list(((I(b1)+I(b2))%2**256).to_bytes(32,'big')),
 "LE yig'indi": list(((int.from_bytes(bytes(b1),'little')+int.from_bytes(bytes(b2),'little'))%2**256).to_bytes(32,'little')),
 "baytma-bayt mod 256": [(x+y)%256 for x,y in zip(b1,b2)],
 "XOR": [x^y for x,y in zip(b1,b2)],
 "BE yig'indi (b1+b2+L)": list(((I(b1)+I(b2)+I(L))%2**256).to_bytes(32,'big')),
}
exp="55 39 4f 2d 84 fc cd 4d 8d 01 d8 fe f7 56 cd 65 7e be cc 3f 96 f8 1e 52 07 76 74 47 de 66 e2 b6"
exp_i3_hn="7c de 69 84 23 e2 35 e9 c9 d9 26 07 aa a7 70 df b1 cb 91 d3 f0 d0 a0 47 f7 db 10 73 98 7c 92 fb"
for a2lit in [0,1]:
    full.V.update(bump=0,kc=1,a2lit=a2lit)
    for nm,ny in cands.items():
        log=[]
        out=hesh([b1,b2,L,ny],k,log)
        print(a2lit, f"{nm:24s}", "i=2 Qosh holatn:", log[1][3].startswith("08 86 c6 2c"), "| i=3 Qosh holatn:", log[2][3]==exp_i3_hn, "| YAKUNIY:", hx(out)==exp)
print("Hisoblangan xesh:", hx(hesh([b1,b2,L,cands["BE yig'indi (b1+b2)"]],k)))
