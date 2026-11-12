import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle, Circle
plt.rcParams.update({'font.family':'STIXGeneral','mathtext.fontset':'stix'})
KE=r'$k_e$'
def box(ax,x,y,w,h,txt,fs=10,style='round,pad=0.02,rounding_size=0.05',fc='white',ls='-',bold=False,it=True,lw=1.0):
    ax.add_patch(FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle=style,fc=fc,ec='black',lw=lw,ls=ls))
    if txt: ax.text(x,y,txt,ha='center',va='center',fontsize=fs,style='italic' if it else 'normal',weight='bold' if bold else 'normal',linespacing=1.3)
def diamond(ax,x,y,w,h,txt,fs=10):
    ax.add_patch(Polygon([(x-w/2,y),(x,y+h/2),(x+w/2,y),(x,y-h/2)],fc='white',ec='black',lw=1))
    ax.text(x,y,txt,ha='center',va='center',fontsize=fs,style='italic')
def para(ax,x,y,w,h,txt,fs=10):
    s=0.15; ax.add_patch(Polygon([(x-w/2+s,y+h/2),(x+w/2+s,y+h/2),(x+w/2-s,y-h/2),(x-w/2-s,y-h/2)],fc='white',ec='black',lw=1))
    ax.text(x,y,txt,ha='center',va='center',fontsize=fs,style='italic')
def term(ax,x,y,w,h,txt,fs=10):
    ax.add_patch(FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle=f'round,pad=0,rounding_size={h/2}',fc='white',ec='black',lw=1))
    ax.text(x,y,txt,ha='center',va='center',fontsize=fs,style='italic')
def line(ax,pts,arrow=True,lw=1.0,color='black'):
    xs,ys=zip(*pts); ax.plot(xs[:-1]+(xs[-1],),ys,color=color,lw=lw) if not arrow else None
    if arrow:
        ax.plot(xs[:-1],ys[:-1],color=color,lw=lw) if len(pts)>2 else None
        ax.annotate('',xy=pts[-1],xytext=pts[-2],arrowprops=dict(arrowstyle='-|>',color=color,lw=lw,mutation_scale=10,shrinkA=0,shrinkB=0))
def lab(ax,x,y,t,fs=9,ha='center'): ax.text(x,y,t,ha=ha,va='center',fontsize=fs,style='italic')

# ---------- 1) SBZ sxemasi ----------
fig,ax=plt.subplots(figsize=(9.2,4.6)); ax.set_xlim(0,18.4); ax.set_ylim(0,9.2); ax.axis('off')
def sbz_panel(x0,title,ltxt,rtxt,out,note,lx,s_lbl):
    ax.text(x0+4.4,8.75,title,ha='center',fontsize=11.5)
    box(ax,x0+2.1,7.6,4.0,0.8,ltxt,fs=9.5,fc='#EEF3FA'); box(ax,x0+6.75,7.6,4.0,0.8,rtxt,fs=9.5,fc='#FCF0EC')
    box(ax,x0+6.75,5.9,1.3,0.75,'S',fs=12,it=False,bold=True,fc='#EAF6F0')
    line(ax,[(x0+6.75,7.2),(x0+6.75,6.28)])
    cx=x0+2.1
    ax.add_patch(Circle((cx,4.5),0.27,fc='white',ec='black',lw=1)); ax.plot([cx-0.27,cx+0.27],[4.5,4.5],'k',lw=1); ax.plot([cx,cx],[4.23,4.77],'k',lw=1)
    line(ax,[(cx,7.2),(cx,4.77)]); line(ax,[(x0+6.75,5.52),(x0+6.75,4.5),(cx+0.27,4.5)])
    lab(ax,x0+4.5,4.85,s_lbl,fs=10.5)
    box(ax,cx,3.0,1.3,0.75,'S',fs=12,it=False,bold=True,fc='#EAF6F0'); line(ax,[(cx,4.23),(cx,3.38)])
    box(ax,x0+4.4,1.2,8.2,1.0 if '\n' in out else 0.8,out,fs=10); line(ax,[(cx,2.62),(cx,1.7 if '\n' in out else 1.6)])
    ax.text(x0+6.2,3.0,note,ha='center',va='center',fontsize=9.5,color='#333333',linespacing=1.3)
sbz_panel(0.1,'a) 256 bitli rejim (p = 256), i = 0…31',r'holat$[i]$ (Qo‘sh natijasi)',r'holatn$[i]$ (Qo‘sh natijasi)',r'holat$[i] \leftarrow S(\,h[i] \oplus S(n[i])\,)$','8 bit + 8 bit → 8 bit,\nhar bir argument bo‘yicha\nbijektiv',0,r'$S(n[i])$')
sbz_panel(9.3,'b) 128 bitli rejim (p = 16), j = 0…15',r'$H_j = 16\cdot h[2j] + h[2j{+}1]$',r'$N_j = 16\cdot n[2j] + n[2j{+}1]$',r'$Q_j = S(H_j \oplus S(N_j))$'+'\n'+r'$h[2j]=Q_j \gg 4,\;\; h[2j{+}1]=Q_j \wedge 15$','qo‘shni ikki yarim bayt\nbitta baytga juftlanadi',0,r'$S(N_j)$')
fig.savefig('sbz.png',dpi=220,bbox_inches='tight',pad_inches=0.05); plt.close(fig)

# ---------- 2) Blok-sxema ----------
fig,ax=plt.subplots(figsize=(7.2,11.4)); ax.set_xlim(0,10); ax.set_ylim(0,16.2); ax.axis('off')
X=5
term(ax,X,15.8,2.2,0.55,'Boshlash'); line(ax,[(X,15.52),(X,15.12)])
para(ax,X,14.85,2.0,0.55,'M, k'); line(ax,[(X,14.57),(X,14.4)])
box(ax,X,13.95,7.2,0.9,KE+r'$[4,8]$, holat$[4,8]$, holatn$[4,8]$, uzunlik$[4,8]$, NY$[4,8]$'+'\n'+r'$R=k[1]$, holat = kirish{1-blok}, '+KE+r'$\,=k$, $i=1$',fs=10,style='square,pad=0')
line(ax,[(X,13.5),(X,13.0)])
diamond(ax,X,12.55,2.6,0.9,r'$i \leq b+1$')
lab(ax,X+0.15,12.0,'HA',fs=8.5,ha='left'); lab(ax,7.0,12.78,'YO‘Q')
line(ax,[(X,12.1),(X,11.85)])
box(ax,X,11.35,4.6,1.0,'holatn = kirish{(i+1)-blok},\nQo‘sh(holat, holatn),\nSBZ(holat, holatn), j = 0',fs=10,style='square,pad=0')
line(ax,[(X,10.85),(X,10.4)])
box(ax,X,10.15,1.6,0.5,'j = j + 1',fs=10,style='square,pad=0'); line(ax,[(X,9.9),(X,9.8)])
diamond(ax,X,9.35,2.4,0.9,r'$j \leq 10$')
lab(ax,3.4,9.58,'YO‘Q'); lab(ax,X+0.15,8.8,'HA',fs=8.5,ha='left')
# i = i + 1 qaytish (chap)
line(ax,[(X-1.2,9.35),(0.9,9.35),(0.9,11.1)])
box(ax,0.9,11.35,1.4,0.5,'i = i + 1',fs=10,style='square,pad=0')
line(ax,[(0.9,11.6),(0.9,13.2),(X,13.2)],arrow=False); line(ax,[(X-0.6,13.2),(X,13.2)])
line(ax,[(X,8.9),(X,8.72)])
box(ax,X,8.1,5.8,1.25,'Aralash(holat, '+KE+'), holatn = '+KE+',\nQo‘sh(holat, holatn), '+KE+' = holatn,\nSurHolat(holat), SurKalit('+KE+')',fs=10,style='square,pad=0')
line(ax,[(X,7.47),(X,7.4)])
diamond(ax,X,6.95,2.0,0.9,r'$j = 8$')
lab(ax,3.55,7.17,'HA'); lab(ax,6.5,7.17,'YO‘Q')
line(ax,[(X-1.0,6.95),(2.3,6.95),(2.3,6.25)])
box(ax,2.3,5.75,3.9,1.0,'holatn = kirish{(i+1)-blok},\nQo‘sh(holat, holatn),\nSBZ(holat, holatn)',fs=10,style='square,pad=0')
line(ax,[(X+1.0,6.95),(7.5,6.95),(7.5,6.25)])
box(ax,7.5,5.75,2.6,1.0,'holatn = '+KE+',\nQo‘sh(holat, holatn),\n'+KE+' = holatn',fs=10,style='square,pad=0')
line(ax,[(2.3,5.25),(2.3,4.95),(7.5,4.95),(7.5,5.25)],arrow=False); line(ax,[(X,4.95),(X,4.8)])
box(ax,X,4.55,3.0,0.5,'TuzilmaKalit('+KE+', k)',fs=10,style='square,pad=0'); line(ax,[(X,4.3),(X,4.2)])
diamond(ax,X,3.75,2.0,0.9,r'$j = 9$')
lab(ax,3.55,3.97,'HA'); lab(ax,6.5,3.97,'YO‘Q')
line(ax,[(X-1.0,3.75),(2.3,3.75),(2.3,3.25)])
box(ax,2.3,2.75,3.9,1.0,'holatn = kirish{(i+1)-blok},\nQo‘sh(holat, holatn),\nSBZ(holat, holatn)',fs=10,style='square,pad=0')
# j halqasi qaytishi (o'ng)
line(ax,[(2.3,2.25),(2.3,2.0),(9.0,2.0),(9.0,10.6),(X,10.6),(X,10.4)])
line(ax,[(X+1.0,3.75),(9.0,3.75)],arrow=False)
# chiqish
line(ax,[(X+1.3,12.55),(9.6,12.55),(9.6,1.55),(X,1.55),(X,1.33)])
para(ax,X,1.05,2.0,0.55,'holat'); line(ax,[(X,0.77),(X,0.62)])
term(ax,X,0.35,2.0,0.55,'Tamom')
fig.savefig('blok.png',dpi=220,bbox_inches='tight',pad_inches=0.05); plt.close(fig)

# ---------- 3) SP tarmoq ----------
fig,ax=plt.subplots(figsize=(7.8,8.5)); ax.set_xlim(0,15.6); ax.set_ylim(4.0,21.0); ax.axis('off')
QK='Qo‘sh(holat, '+KE+')'
L1='Aralash(holat, '+KE+'), '+QK+','; L2='SurHolat(holat), SurKalit('+KE+'),'; L3=QK+', TuzilmaKalit('+KE+', k)'
cols=[(2.55,'2','i = 1'),(7.8,'3','i = 2'),(13.05,'b+2','i = b+1')]
for ci,(x,blk,il) in enumerate(cols):
    inj='Qo‘sh(holat, kirish{'+blk+'}), SBZ'
    box(ax,x,19.2,4.8,1.1,'holatn = kirish{'+blk+'-blok}'+('  (NY)' if ci==2 else '')+'\nQo‘sh(holat, holatn)\nSBZ(holat, holatn)',fs=8.3,style='square,pad=0',bold=True)
    ax.add_patch(Rectangle((x-2.55,7.15),5.1,11.3,fill=False,ls=(0,(5,3)),lw=1.3))
    rounds=[(17.35,'1-bosqich',L1+'\n'+L2+'\n'+L3,1.05,False),(15.55,'2-bosqich',L1+'\n'+L2+'\n'+L3,1.05,False),
            (14.2,None,'3, 4, 5, 6, 7-bosqichlar',0.5,False),
            (12.55,'8-bosqich',L1+'\n'+L2+'\n'+inj+',\nTuzilmaKalit('+KE+', k)',1.35,True),
            (10.45,'9-bosqich',L1+'\n'+L2+'\n'+L3+',\n'+inj,1.35,True),
            (8.5,'10-bosqich',L1+'\n'+L2+'\n'+L3,1.05,False)]
    prev=18.65
    for y,t,txt,h,hl in rounds:
        if t: ax.text(x-2.4,y+h/2+0.27,t,fontsize=8.3,color='#1F4E9A',weight='bold',ha='left',va='center')
        line(ax,[(x,prev),(x,y+h/2)])
        box(ax,x,y,4.85,h,txt,fs=7.7,style='square,pad=0',bold=(t is None),it=(t is not None),fc=('#FFF6E5' if hl else ('#F5F8FC' if t is None else 'white')))
        prev=y-h/2
    ax.text(x-1.3,7.5,il,ha='center',va='center',fontsize=10,style='italic',weight='bold')
    if ci<2:
        line(ax,[(x,prev),(x,6.85),(x+2.62,6.85),(x+2.62,20.1),(cols[ci+1][0],20.1),(cols[ci+1][0],19.75)],lw=1.5,color='#1F6FB5')
    else:
        line(ax,[(x,prev),(x,6.55)]); box(ax,x,6.2,3.0,0.65,'chiqish = holat',fs=9.5,bold=True)
ax.text(11.85,20.38,'…',fontsize=20,ha='center',va='center',color='#1F6FB5')
box(ax,2.55,20.45,4.8,0.55,'R = k[1], holat = kirish{1-blok}, '+KE+' = k',fs=8.3,style='square,pad=0',bold=True)
line(ax,[(2.55,20.17),(2.55,19.75)])
ax.text(0.05,5.25,'Belgilashlar:  '+QK+' — holatn = '+KE+', Qo‘sh(holat, holatn), '+KE+' = holatn;',fontsize=8.5,style='italic',ha='left')
ax.text(0.05,4.6,'Qo‘sh(holat, kirish{m}), SBZ — holatn = kirish{m-blok}, Qo‘sh(holat, holatn), SBZ(holat, holatn).',fontsize=8.5,style='italic',ha='left')
ax.text(0.05,3.95,'Kirish bloki holatga yutiladigan bosqichlar (8 va 9) rang bilan ajratilgan.',fontsize=8.5,style='italic',ha='left')
fig.savefig('sp.png',dpi=220,bbox_inches='tight',pad_inches=0.05); plt.close(fig)
