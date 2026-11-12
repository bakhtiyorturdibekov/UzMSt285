import json, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, numpy as np
plt.rcParams.update({'font.family':'DejaVu Serif','font.size':11})
K='/home/claude/ka/'; Ch=json.load(open(K+'chegaralar.json')); T=json.load(open(K+'yagona_tezlik.json'))
fig,ax=plt.subplots(1,2,figsize=(7.6,3.4)); rs=np.arange(1,7)
ax[0].plot(rs,-96*rs,'-o',ms=4,label='differensial (≥16 S/raund)')
ax[0].plot(rs,[-3*Ch['lin_256'][str(r)] for r in rs],'-s',ms=4,label='chiziqli, 256 bit')
ax[0].plot(rs,[-3*Ch['lin_128_yagona'][str(r)] for r in rs],'-^',ms=4,label='chiziqli, 128 bit')
ax[0].axhline(-128,color='r',ls='--',lw=.8); ax[0].axhline(-64,color='r',ls=':',lw=.8); ax[0].text(4.6,-122,'2⁻¹²⁸',color='r',fontsize=8); ax[0].text(4.6,-58,'2⁻⁶⁴',color='r',fontsize=8)
ax[0].set_ylim(-420,5); ax[0].set_xlabel('Raundlar soni'); ax[0].set_ylabel('log₂ (iz chegarasi)'); ax[0].legend(fontsize=7); ax[0].grid(alpha=.3)
labs=['Standart','Yakuniy\n(R=10)','Yagona\nR=10','R=6','R=5','R=4']
for i,(bl,c) in enumerate(((32,'#2e6db5'),(16,'#2e9d5b'))):
    v=[T[f'{bl}_standart']['MBs'],T[f'{bl}_yakuniy']['MBs']]+[T[f'{bl}_yagona{R}']['MBs'] for R in (10,6,5,4)]
    ax[1].bar(np.arange(6)+(i-0.5)*0.38,v,0.38,color=c,label='256 bit' if bl==32 else '128 bit')
ax[1].set_xticks(range(6)); ax[1].set_xticklabels(labs,fontsize=7); ax[1].set_ylabel('MB/s (C, -O2)'); ax[1].legend(fontsize=8); ax[1].grid(alpha=.3,axis='y')
fig.tight_layout(); fig.savefig('ch1.png',dpi=200); print('ok')
