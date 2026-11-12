import json, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, numpy as np
plt.rcParams.update({'font.family':'DejaVu Serif','font.size':11})
K='/home/claude/ka/'; C=json.load(open(K+'yakuniy_tezlik_c.json')); Pq=json.load(open(K+'yakuniy_tezlik_py.json')); R=json.load(open(K+'yakuniy_tahlil.json'))
L2=json.load(open(K+'lin2.json')); D3=json.load(open(K+'dif3.json'))
fig,ax=plt.subplots(1,2,figsize=(7.6,3.3)); noms=['standart','sbz','yakuniy']; lab=['Standart','SBZ','Yakuniy variant']
for i,p in enumerate(('256','16')):
    v=[C[f'{p}_{n}']['MBs'] for n in noms]; ax[i].bar(range(3),v,color=['#888','#4a7ab5','#2e9d5b'])
    for j,x in enumerate(v): ax[i].text(j,x+0.05,f'{x:.2f}',ha='center',fontsize=9)
    ax[i].set_xticks(range(3)); ax[i].set_xticklabels(lab,fontsize=8); ax[i].set_title(f'{p if p=="256" else "128"} bitli rejim',fontsize=10); ax[i].set_ylabel('MB/s (C, -O2)'); ax[i].grid(alpha=.3,axis='y')
fig.tight_layout(); fig.savefig('ch_tezlik.png',dpi=200)
fig,ax=plt.subplots(1,2,figsize=(7.6,3.3)); js=list(range(1,11))
ax[0].plot(js,L2['lsb_pred_256_std'],'-o',ms=3,label='Standart-256'); ax[0].plot(js,L2['lsb_pred_256_sbz'],'-s',ms=3,label='SBZ-256'); ax[0].plot(js,R['raund_256']['qatlam0_c'],'-^',ms=3,label='Yakuniy-256')
ax[0].set_xlabel('Raund j'); ax[0].set_ylabel('0-qatlam tenglamasi c'); ax[0].legend(fontsize=7); ax[0].grid(alpha=.3)
for key,lab_ in [('256_std_D0a','Standart-256'),('256_sbz_D0a','SBZ-256')]:
    rows=[r for r in D3[key] if r['op']=='Tuz']; ax[1].semilogy([r['j'] for r in rows],[max(r['msb'],1e-3) for r in rows],'-o',ms=3,label=lab_)
d1=[x for x in R['raund_256']['D1'] if x[0] in ('Bog2','SBZ8','SBZ9')]
ax[1].semilogy([1,2],[1e-3,1e-3],'-^',ms=3,label='Yakuniy-256 (0,000)')
ax[1].set_xlabel('Raund j'); ax[1].set_ylabel('MSB izining saqlanishi'); ax[1].legend(fontsize=7); ax[1].grid(alpha=.3)
fig.tight_layout(); fig.savefig('ch_tahlil.png',dpi=200); print('ok')
