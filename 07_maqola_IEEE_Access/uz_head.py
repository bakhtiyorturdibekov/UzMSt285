import json, re
K='/home/claude/ka/'; J=lambda f: json.load(open(K+f+'.json'))
L2=J('lin2'); A2=J('alg2'); CH=J('chegaralar'); YR=J('yagona_raund'); QB=J('qb_tezlik'); MR=json.load(open('/home/claude/nb/misollar_natijalari.json'))
EX=json.load(open('/home/claude/paper/extra.json')); KAT=YR['KAT']
B=[]; tc=[0]; fc=[0]; eq=[0]
ROM=['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII','XIII','XIV','XV','XVI','XVII','XVIII']
H1=lambda t:B.append(['h1',t]); H2=lambda t:B.append(['h2',t]); P=lambda t:B.append(['p',t]); BL=lambda t:B.append(['b',t])
def F(t): eq[0]+=1; B.append(['f',t,f'({eq[0]})'])
TK={}; FK={}
def T(w,rows,cap,key,mono=()): tc[0]+=1; TK[key]=str(tc[0]); B.append(['cap',f"{tc[0]}-jadval — {cap}"]); B.append(['t',w,rows,list(mono)])
def IMG(p,w,h,cap,key): fc[0]+=1; FK[key]=str(fc[0]); B.append(['img',p,w,h]); B.append(['fcap',f"{fc[0]}-rasm. {cap}"])
fz=lambda x,d=2:f'{x:.{d}f}'.replace('.',',')
rh=EX['rank_hist']; nk=sum(rh.values()); mean_rank=sum(int(k)*v for k,v in rh.items())/nk; full=rh.get('32',0)/nk*100; rmin=min(int(k) for k in rh)

