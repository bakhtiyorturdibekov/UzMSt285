import json, numpy as np, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
plt.rcParams.update({'font.family':'DejaVu Serif','font.size':9})
X=json.load(open('extra.json')); I=json.load(open('/home/claude/pkg/uzmst285_tahlil/natijalar/integral.json'))
# fig3: rank histogram
h=X['rank_hist']; ks=[int(k) for k in h]; vs=[h[str(k)] for k in ks]
fig,ax=plt.subplots(figsize=(3.4,2.4)); ax.bar(ks,vs,color=['#c0392b' if k==32 else '#2e6db5' for k in ks])
ax.set_xlabel('rank of L over GF(2)'); ax.set_ylabel('number of keys (of 1000)'); ax.grid(alpha=.3,axis='y'); fig.tight_layout(); fig.savefig('fig3.png',dpi=300)
# fig4: SAC heatmaps
fig,ax=plt.subplots(1,2,figsize=(7.0,3.2))
for a,nm,t in ((ax[0],'std','(a) standard round'),(ax[1],'new','(b) redesigned round')):
    S=np.load(f'sac_{nm}.npy'); im=a.imshow(S,cmap='viridis',vmin=0,vmax=1,interpolation='nearest'); a.set_title(t,fontsize=9)
    a.set_xlabel('output bit'); a.set_ylabel('input bit')
fig.colorbar(im,ax=ax,shrink=0.8,label='flip probability'); fig.savefig('fig4.png',dpi=300,bbox_inches='tight')
# fig5: LSB balance per round
rows=[r for r in I['raund_256_holat'] if r['amal']=='Tuz']; js=[r['raund'] for r in rows]
std=[32 if r['qatlam_doim_nol'][0]==32 else 16 for r in rows]
fig,ax=plt.subplots(figsize=(3.4,2.4))
ax.plot(js,[r['qatlam_doim_nol'][0] for r in rows],'-o',ms=3,label='standard (balanced in all 40 trials)')
ax.plot(range(1,7),X['int_new_mean'],'-^',ms=3,label='redesign, R = 6 (mean per trial)')
ax.axhline(16,color='gray',ls=':',lw=.8); ax.text(6.3,17,'random ≈ 16',color='gray',fontsize=7)
ax.set_xlabel('round'); ax.set_ylabel('balanced LSBs (of 32)'); ax.set_ylim(-1,34); ax.legend(fontsize=6.5); ax.grid(alpha=.3); fig.tight_layout(); fig.savefig('fig5.png',dpi=300)
# fig6: Bog'lash diagram
fig,ax=plt.subplots(figsize=(7.2,2.9)); ax.axis('off'); ax.set_xlim(0,16.4); ax.set_ylim(-0.9,5)
def box(x,y,w,h,t,fc='#eaf1fb',fs=7.5):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.05',fc=fc,ec='k',lw=.8)); ax.text(x+w/2,y+h/2,t,ha='center',va='center',fontsize=fs)
def arr(x1,y1,x2,y2): ax.annotate('',xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle='->',lw=.8))
box(0.1,3.3,1.9,1.0,'left half'); box(0.1,0.7,1.9,1.0,'right half')
xs=[2.8,7.4,12.0]; names=['half-step 1\nright ← f(right; left)','half-step 2\nleft ← f(left; right)','half-step 3\nright ← f(right; left)']
for i,x in enumerate(xs):
    tgt_y=0.7 if i!=1 else 3.3; src_y=3.3 if i!=1 else 0.7
    box(x,tgt_y,3.6,1.0,names[i],fc='#fdf2e9'); box(x,src_y,3.6,1.0,'J = ΣU,  K = Π(U ∨ 1)\naᵢ, bᵢ = 2·S(·) + 1',fc='#eef7ee',fs=7)
    arr(x+1.8,src_y+(0 if src_y>tgt_y else 1.0),x+1.8,tgt_y+(1.0 if src_y>tgt_y else 0))
for (x1,x2) in ((2.0,2.8),(6.4,7.4),(11.0,12.0)):
    arr(x1,3.8,x2,3.8); arr(x1,1.2,x2,1.2)
ax.text(8.2,-0.5,'f(T; U):  T[i] ← S( −aᵢ · T[i] · (bᵢ + R·T[i])⁻¹ ⊕ X_T[i] ),  parameters from the unchanged half U',ha='center',fontsize=7.5)
fig.savefig('fig6.png',dpi=300,bbox_inches='tight'); print('ok')
