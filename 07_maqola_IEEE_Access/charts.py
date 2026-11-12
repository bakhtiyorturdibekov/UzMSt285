import json, numpy as np, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.family':'DejaVu Serif','font.size':9})
K='/home/claude/ka/'; L2=json.load(open(K+'lin2.json')); D3=json.load(open(K+'dif3.json')); CH=json.load(open(K+'chegaralar.json')); YT=json.load(open(K+'yagona_tezlik.json')); QB=json.load(open(K+'qb_tezlik.json')); YK=json.load(open(K+'yakuniy_tahlil.json'))
js=list(range(1,11))
fig,ax=plt.subplots(1,2,figsize=(7.0,2.6))
ax[0].plot(js,L2['lsb_pred_256_std'],'-o',ms=3,label='Standard, 256-bit'); ax[0].plot(js,L2['lsb_pred_16_std'],'-s',ms=3,label='Standard, 128-bit')
ax[0].plot(js,YK['raund_256']['qatlam0_c'],'-^',ms=3,label='Modified, 256-bit'); ax[0].axvspan(7.5,9.5,color='orange',alpha=.12)
ax[0].set_xlabel('Round'); ax[0].set_ylabel('Correlation of LSB-layer relation'); ax[0].legend(fontsize=7); ax[0].grid(alpha=.3); ax[0].set_title('(a)',fontsize=9)
for key,lab in [('256_std_D0a','Standard, 256-bit'),('16_std_D0a','Standard, 128-bit')]:
    rows=[r for r in D3[key] if r['op']=='Tuz']; ax[1].semilogy([r['j'] for r in rows],[max(r['msb'],1e-3) for r in rows],'-o',ms=3,label=lab)
ax[1].semilogy(js,[1e-3]*10,'-^',ms=3,label='Modified (0 observed)'); ax[1].axvspan(7.5,9.5,color='orange',alpha=.12)
ax[1].set_xlabel('Round'); ax[1].set_ylabel('Pr[MSB-only difference]'); ax[1].legend(fontsize=7); ax[1].grid(alpha=.3); ax[1].set_title('(b)',fontsize=9)
fig.tight_layout(); fig.savefig('fig1.png',dpi=300)
fig,ax=plt.subplots(1,2,figsize=(7.0,2.6)); rs=np.arange(1,7)
ax[0].plot(rs,-96*rs,'-o',ms=3,label='differential (≥16 active S-boxes/round)')
ax[0].plot(rs,[-3*CH['lin_256'][str(r)] for r in rs],'-s',ms=3,label='linear, 256-bit')
ax[0].plot(rs,[-3*CH['lin_128_yagona'][str(r)] for r in rs],'-^',ms=3,label='linear, 128-bit')
ax[0].axhline(-128,color='r',ls='--',lw=.8); ax[0].axhline(-64,color='r',ls=':',lw=.8); ax[0].text(5.2,-122,'$2^{-128}$',color='r',fontsize=7); ax[0].text(5.2,-58,'$2^{-64}$',color='r',fontsize=7)
ax[0].set_ylim(-420,5); ax[0].set_xlabel('Rounds'); ax[0].set_ylabel('log$_2$ of trail bound'); ax[0].legend(fontsize=6.5); ax[0].grid(alpha=.3); ax[0].set_title('(a)',fontsize=9)
labs=['Standard','R=10','R=6','R=5','R=4']
for i,(bl,c) in enumerate(((32,'#2e6db5'),(16,'#2e9d5b'))):
    v=[YT[f'{bl}_standart']['MBs']]+[YT[f'{bl}_yagona{R}']['MBs'] for R in (10,6,5,4)]
    ax[1].bar(np.arange(5)+(i-0.5)*0.38,v,0.38,color=c,label='256-bit' if bl==32 else '128-bit')
ax[1].set_xticks(range(5)); ax[1].set_xticklabels(labs,fontsize=8); ax[1].set_ylabel('Throughput, MB/s (C, -O2)'); ax[1].legend(fontsize=7); ax[1].grid(alpha=.3,axis='y'); ax[1].set_title('(b)',fontsize=9)
fig.tight_layout(); fig.savefig('fig2.png',dpi=300); print('ok')
