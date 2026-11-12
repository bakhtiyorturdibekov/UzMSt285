import json, math, numpy as np, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.family':'DejaVu Serif','font.size':11})
K='/home/claude/ka/'; I=json.load(open('/home/claude/pkg/uzmst285_tahlil/natijalar/integral.json'))
L2=json.load(open(K+'lin2.json')); L3=json.load(open(K+'lin3.json')); D3=json.load(open(K+'dif3.json'))
# 1 chiziqli: raundlar bo'yicha 0-qatlam korrelyatsiyasi va qatlamlar bo'yicha chegara
fig,ax=plt.subplots(1,2,figsize=(7.6,3.4))
js=list(range(1,11))
ax[0].plot(js,L2['lsb_pred_256_std'],'-o',ms=4,label='Standart-256'); ax[0].plot(js,L2['lsb_pred_16_std'],'-s',ms=4,label='Standart-128')
ax[0].axvspan(7.5,9.5,color='orange',alpha=0.12); ax[0].set_xlabel('Raund j'); ax[0].set_ylabel('0-qatlam tenglamasi korrelyatsiyasi'); ax[0].legend(fontsize=8); ax[0].grid(alpha=.3)
ks=list(range(1,7)); med=[L3[str(k)]['median'] for k in ks]; mn=[L3[str(k)]['min'] for k in ks]
ax[1].plot(ks,[-2*m for m in med],'-o',ms=4,label='Standart-256, mediana kalit'); ax[1].plot(ks,[-2*m for m in mn],'--o',ms=4,label='Standart-256, eng yomon kalit')
ax[1].plot(ks,[0]*6,'-^',ms=4,label='Standart-128 (c = 1)'); ax[1].axhline(-64,color='gray',ls=':'); ax[1].text(1,-60,'2⁻⁶⁴',color='gray')
ax[1].set_xlabel('Yutish qatlamlari soni'); ax[1].set_ylabel('log₂|c| chegarasi'); ax[1].legend(fontsize=7.5); ax[1].grid(alpha=.3)
fig.tight_layout(); fig.savefig('ch1.png',dpi=200)
# 2 differensial
fig,ax=plt.subplots(1,2,figsize=(7.6,3.4))
for key,lab in [('256_std_D0a','Standart-256'),('16_std_D0a','Standart-128')]:
    rows=[r for r in D3[key] if r['op']=='Tuz']
    ax[0].semilogy([r['j'] for r in rows],[max(r['msb'],1e-3) for r in rows],'-o',ms=4,label=lab)
    ax[1].plot([r['j'] for r in rows],[r['act'] for r in rows],'-o',ms=4,label=lab)
for a in ax: a.axvspan(7.5,9.5,color='orange',alpha=.12); a.grid(alpha=.3); a.set_xlabel('Raund j')
ax[0].set_ylabel('MSB izining saqlanish ehtimolligi'); ax[1].set_ylabel('holatdagi faol elementlar'); ax[1].legend(fontsize=8)
fig.tight_layout(); fig.savefig('ch2.png',dpi=200)
# 3 algebraik
fig,ax=plt.subplots(figsize=(7,3.3)); ds=list(range(1,21))
for nv in (128,256): ax.plot(ds,[2.8*math.log2(sum(math.comb(nv,i) for i in range(d+1))) for d in ds],'-o',ms=3,label=f'{nv} ta noma’lum bit')
for d,lab in [(1,'XOR (1)'),(6,'Z (6)')]: ax.axvline(d,color='gray',ls=':'); ax.text(d+.2,15,lab,rotation=90,color='gray',fontsize=9)
for y in (64,128): ax.axhline(y,color='red',ls='--',lw=.8); ax.text(16,y+5,f'2^{y}',color='red',fontsize=9)
ax.set_xlabel('Tenglamalar darajasi d'); ax.set_ylabel('log₂ (linearizatsiya mehnati)'); ax.legend(fontsize=9); ax.grid(alpha=.3)
fig.tight_layout(); fig.savefig('ch3.png',dpi=200)
# 4 integral
fig,ax=plt.subplots(1,2,figsize=(7.6,3.4))
for key,lab,a in [('raund_256_holat','Standart-256',0),('raund_16_holat','Standart-128',1)]:
    rows=[r for r in I[key] if r['amal']=='Tuz']; nb=len(rows[0]['qatlam_doim_nol'])
    for b in range(nb): ax[a].plot([r['raund'] for r in rows],[r['qatlam_doim_nol'][b] for r in rows],'-o',ms=3,label=f'{b}-qatlam')
    ax[a].set_title(lab,fontsize=10); ax[a].set_xlabel('Raund j'); ax[a].axvspan(7.5,9.5,color='orange',alpha=.12); ax[a].grid(alpha=.3)
ax[0].set_ylabel('doim balanslangan bitlar (32 dan)'); ax[0].legend(fontsize=7,ncol=2); ax[1].legend(fontsize=7)
fig.tight_layout(); fig.savefig('ch4.png',dpi=200); print('ok')
