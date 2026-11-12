"""natijalar/*.json asosida hisobotdagi uchta grafikni chizadi (matplotlib kerak)."""
import json, math, os
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.family': 'DejaVu Serif', 'font.size': 11})
L = json.load(open('natijalar/chiziqli.json')); D = json.load(open('natijalar/differensial.json'))
os.makedirs('natijalar', exist_ok=True)
# 1) chiziqli
FB = L['faol_baytlar']; ks = sorted(int(k) for k in FB)
fig, ax = plt.subplots(figsize=(7, 3.6))
for lab, per, st in [('SBZ (≤2⁻⁶ / faol bayt)', 6, '-o'), ('BaytZichlash p=256 (≤2⁻² / faol bayt)', 2, '-s')]:
    ax.plot(ks, [-per * FB[str(k)]['mediana'] for k in ks], st, label=lab + ', mediana')
    ax.plot(ks, [-per * FB[str(k)]['min'] for k in ks], st.replace('-', '--'), alpha=0.6, label=lab + ', eng yomon kalit')
ax.plot(ks, [0] * len(ks), '-^', label='BaytZichlash p=16 (XOR), c = 1')
for y, t in [(-64, '2⁻⁶⁴ (256 bitli rejim)'), (-32, '2⁻³² (128 bitli rejim)')]:
    ax.axhline(y, color='gray', ls=':'); ax.text(ks[0] + 0.05, y + 4, t, fontsize=9, color='gray')
ax.set_xlabel('Iz o‘tadigan yutish qatlamlari soni'); ax.set_ylabel('log₂|c| yuqori chegarasi')
ax.legend(fontsize=8, loc='lower left'); ax.grid(alpha=0.3); fig.tight_layout(); fig.savefig('natijalar/1_chiziqli.png', dpi=200)
# 2) differensial
K = D['kuzatish']; fig, ax = plt.subplots(1, 2, figsize=(7.4, 3.4))
for key, lab in [('256_std_D0a', 'Standart, p=256'), ('256_sbz_D0a', 'SBZ, p=256'), ('16_std_D0a', 'Standart, p=16'), ('16_sbz_D0a', 'SBZ, p=16')]:
    rows = [r for r in K[key] if r['amal'] == 'Tuz']; js = [r['raund'] for r in rows]
    ax[0].semilogy(js, [max(r['P_MSB_izi'], 1e-3) for r in rows], '-o', ms=3, label=lab)
    ax[1].plot(js, [r['faol_holat'] for r in rows], '-o', ms=3, label=lab)
ax[0].set_xlabel('Raund j'); ax[0].set_ylabel('MSB izining saqlanish ehtimolligi')
ax[1].set_xlabel('Raund j'); ax[1].set_ylabel('holat dagi faol elementlar'); ax[1].legend(fontsize=8)
for a in ax: a.grid(alpha=0.3); a.axvspan(7.5, 9.5, color='orange', alpha=0.12)
fig.tight_layout(); fig.savefig('natijalar/2_differensial.png', dpi=200)
# 3) algebraik
fig, ax = plt.subplots(figsize=(7, 3.4)); ds = list(range(1, 21))
for nv in (128, 256):
    ax.plot(ds, [2.8 * math.log2(sum(math.comb(nv, i) for i in range(d + 1))) for d in ds], '-o', ms=3, label=f'{nv} ta o‘zgaruvchi')
for d, lab in [(1, 'XOR (1)'), (6, 'BaytZichlash (6)'), (13, 'SBZ (13)')]:
    ax.axvline(d, color='gray', ls=':'); ax.text(d + 0.2, 10, lab, fontsize=9, rotation=90, color='gray')
for y in (64, 128): ax.axhline(y, color='red', ls='--', lw=0.8); ax.text(14.2, y + 5, f'2^{y}', color='red', fontsize=9)
ax.set_xlabel('Tenglamalar darajasi d'); ax.set_ylabel('log₂ (linearizatsiya murakkabligi)'); ax.legend(fontsize=9); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig('natijalar/3_algebraik.png', dpi=200)
print("Grafiklar natijalar/ papkasida saqlandi.")
