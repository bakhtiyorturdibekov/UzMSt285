from full import *
msg=q.msg; b1=list(msg[:32]); b2=list(msg[32:])
h1=hesh([b1,b2],k)
exp_hn="08 86 c6 2c 12 1c a6 a6 88 14 d2 b6 3c e6 52 9e 62 42 24 8a 56 32 06 2c 20 a6 42 88 de 04 a2 38"
exp_h ="7b a4 c4 0d 3a 65 f4 f4 bb b1 9a 1c b5 94 da 80 42 f2 59 26 2c 8a 64 0d f7 f4 72 bb 20 89 0a b3"
cands={}
for val,nm in [(512,'bit'),(64,'bayt'),(2,'blok')]:
    cands[nm+' BE']=list(val.to_bytes(32,'big'))
    cands[nm+' LE']=list(val.to_bytes(32,'little'))
    s=str(val).encode(); cands[nm+' ASCII-o\'nlik chapda']=list(s)+[0]*(32-len(s)); cands[nm+" ASCII-o'nlik o'ngda"]=[0]*(32-len(s))+list(s)
for nm,c in cands.items():
    a,b=Q(h1,to2(c)); ok=(hx(b)==exp_hn, hx(a)==exp_h)
    print(f"{nm:28s}", ok)
