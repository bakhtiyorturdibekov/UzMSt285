from full import *
msg=q.msg; b1=list(msg[:32]); b2=list(msg[32:])
log=[]
# faqat 1-iteratsiya natijasini tekshirish: blocks=[b1,b2]
out=hesh([b1,b2],k,log)
print("i=1 oxiri:", hx(out))
print("kutilgan : 29 14 b4 73 ca cb a4 a4 69 f7 aa ec 1b c4 ea 80 32 22 1f 26 3c da d4 73 25 a4 a2 69 a0 4f 32 a1")
