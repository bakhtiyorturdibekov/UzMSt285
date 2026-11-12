import json, numpy as np, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.family':'DejaVu Serif','font.size':11})
L3=json.load(open('lin3.json')); D3=json.load(open('dif3.json'))
# 1) chiziqli: log2|c| chegarasi yutish qatlamlari soni bo'yicha (mediana faol baytlar)
ks=[1,2,3,4,5,6]; med=[L3[str(k)]['median'] for k in ks]; mn=[L3[str(k)]['min'] for k in ks]
fig,ax=plt.subplots(figsize=(7,3.6))
for lab,per,st in [('SBZ (≤2⁻⁶ / faol bayt)',6,'-o'),('BaytZichlash p=256 (≤2⁻² / faol bayt)',2,'-s')]:
    ax.plot(ks,[-per*m for m in med],st,label=lab+', mediana')
    ax.plot(ks,[-per*m for m in mn],st.replace('-','--'),alpha=0.6,label=lab+', eng yomon kalit')
ax.plot(ks,[0]*6,'-^',label='BaytZichlash p=16 (XOR), c = 1')
ax.axhline(-64,color='gray',ls=':'); ax.text(1.05,-60,'2⁻⁶⁴ (256 bitli rejim chegarasi)',fontsize=9,color='gray')
ax.axhline(-32,color='gray',ls=':'); ax.text(1.05,-28,'2⁻³² (128 bitli rejim chegarasi)',fontsize=9,color='gray')
ax.set_xlabel('Iz o‘tadigan yutish qatlamlari soni'); ax.set_ylabel('log₂|c| yuqori chegarasi'); ax.set_ylim(-300,10)
ax.legend(fontsize=8,loc='lower left'); ax.grid(alpha=0.3); fig.tight_layout(); fig.savefig('ch_lin.png',dpi=200)
# 2) differensial: MSB izining saqlanish ehtimolligi raundlar bo'yicha
fig,ax=plt.subplots(1,2,figsize=(7.4,3.4))
for key,lab in [('256_std_D0a','Standart, p=256'),('256_sbz_D0a','SBZ, p=256'),('16_std_D0a','Standart, p=16'),('16_sbz_D0a','SBZ, p=16')]:
    rows=[r for r in D3[key] if r['op']=='Tuz']
    js=[r['j'] for r in rows]; pr=[max(r['msb'],1e-3) for r in rows]; act=[r['act'] for r in rows]
    ax[0].semilogy(js,pr,'-o',ms=3,label=lab); ax[1].plot(js,act,'-o',ms=3,label=lab)
ax[0].set_xlabel('Raund j'); ax[0].set_ylabel('MSB izining saqlanish ehtimolligi'); ax[0].grid(alpha=0.3)
ax[1].set_xlabel('Raund j'); ax[1].set_ylabel('holat dagi faol elementlar'); ax[1].grid(alpha=0.3); ax[1].legend(fontsize=8)
for a in ax: a.axvspan(7.5,9.5,color='orange',alpha=0.12)
fig.tight_layout(); fig.savefig('ch_dif.png',dpi=200)
# 3) algebraik: linearizatsiya murakkabligi daraja bo'yicha
import math
fig,ax=plt.subplots(figsize=(7,3.4)); ds=list(range(1,21))
for nv in (128,256):
    ax.plot(ds,[2.8*math.log2(sum(math.comb(nv,i) for i in range(d+1))) for d in ds],'-o',ms=3,label=f'{nv} ta o‘zgaruvchi')
for d,lab in [(1,'XOR (1)'),(6,'BaytZichlash (6)'),(13,'SBZ (13)')]:
    ax.axvline(d,color='gray',ls=':'); ax.text(d+0.2,10,lab,fontsize=9,rotation=90,color='gray')
ax.axhline(128,color='red',ls='--',lw=0.8); ax.text(14.2,133,'2¹²⁸',color='red',fontsize=9)
ax.axhline(64,color='red',ls='--',lw=0.8); ax.text(14.2,69,'2⁶⁴',color='red',fontsize=9)
ax.set_xlabel('Tenglamalar darajasi d'); ax.set_ylabel('log₂ (linearizatsiya murakkabligi)'); ax.legend(fontsize=9); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig('ch_alg.png',dpi=200)
print('ok')
