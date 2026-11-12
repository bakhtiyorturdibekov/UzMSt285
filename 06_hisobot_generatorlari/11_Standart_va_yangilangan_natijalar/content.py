import json, re as _re
K='/home/claude/ka/'; J=lambda f: json.load(open(K+f+'.json'))
XS=J('izlar_std'); XY=J('izlar_yag'); IZ=J('std_iz'); L1=J('lin1'); D3=J('dif3'); A2=J('alg2'); A3=J('alg3'); CH=J('chegaralar'); YT=J('yakuniy_tahlil'); YR=J('yagona_raund'); YD=J('yakuniy_det'); D1=J('dif1'); A1=J('alg1')
MR=json.load(open('/home/claude/nb/misollar_natijalari.json'))
B=[]; tc=[0]
H1=lambda t:B.append(['h1',t]); H2=lambda t:B.append(['h2',t]); H3=lambda t:B.append(['h3',t])
P=lambda t:B.append(['p',t]); F=lambda t:B.append(['f',t]); BL=lambda t:B.append(['b',t]); PB=lambda:B.append(['pb'])
def T(w,rows,cap,mono=()): tc[0]+=1; B.append(['cap',f"{tc[0]}-jadval. {cap}"]); B.append(['t',w,rows,list(mono)])
fz=lambda x,d=2:(f'{x:.{d}f}').replace('.',','); nl='\n'.join; sp=lambda n:f"{n:,}".replace(',',' ')
xor=lambda ps,v='h₀': ' ⊕ '.join(f"{v}{p}" for p in ps) if ps else '0'
opn={'Qosh0':'Qo‘sh(holat, blok)','BZ0':'BaytZichlash (0-nuqta)','Aralash':'Aralash(holat, kₑ)','Qosh1':'Qo‘sh(holat, kₑ) — 1','Sur':'SurHolat, SurKalit','Qosh2':'Qo‘sh(holat, kₑ) — 2','Tuz':'TuzilmaKalit','Qosh_inj8':'Qo‘sh(holat, blok)','BZ8':'BaytZichlash (8-nuqta)','BZ9':'BaytZichlash (9-nuqta)','Qosh_inj9':'Qo‘sh(holat, blok)'}

B.append(['title','STANDART VA YANGILANGAN ALGORITMNING CHIZIQLI, DIFFERENSIAL, ALGEBRAIK VA INTEGRAL KRIPTOTAHLILI: BOSHLANG‘ICH, ORALIQ VA YAKUNIY NATIJALAR'])
B.append(['sub','Akslantirishlar va raundlar bo‘yicha tenglamalar, orttirmalar va to‘plamlarning ko‘rinishi (A ilova ma’lumotlari misolida)'])
H1('Kirish')
P("Ushbu hujjatda ikki algoritm uchun to‘rtta kriptotahlil usulining boshlang‘ich, oraliq va yakuniy natijalari to‘liq ko‘rinishda keltiriladi: chiziqli tahlilda — approksimatsiya tenglamalarining har bir akslantirish va raunddan keyingi ko‘rinishi; differensial tahlilda — optimal orttirmalarning akslantirishlar va raundlardan o‘tgandagi ko‘rinishi; algebraik tahlilda — tenglamalarning akslantirishlar va raundlardagi ko‘rinishi; integral tahlilda — tanlangan to‘plamlarning akslantirishlar va raundlardan keyingi ko‘rinishi.")
BL("*Standart algoritm* — O‘zMSt 285:2024, 1-algoritm (Qo‘sh, Aralash, SurHolat, SurKalit, TuzilmaKalit, BaytZichlash; 10 raund).")
BL("*Yangilangan algoritm* — «6.2-band yangi tahriri» loyihasidagi yagona variant: Qo‘sh o‘rniga Bog‘lash, BaytZichlash o‘rniga SBZ, toq kₑ va holatdan mustaqil kalit jadvali (RCⱼ — √2), oldinga uzatish va chiqish o‘zgartirishi P(H) ⊕ H (C₁, C₂ — √3), R = 6 raund (yutish nuqtalari 0, 4, 5).")
P("Barcha misollar standartning A ilovasidagi kalit (k = c86ed4b2 756df1cd 6b6eca81 d4418092 21ab81bb a0c7c150 44be8feb 934f95a2) va 64 baytli xabar («funksiyaxeshirovaniya…») bilan 256 bitli rejimda hisoblangan; 128 bitli rejim uchun asosiy natijalar alohida keltiriladi. Belgilashlar: [s,u] — massivning s-satr, u-ustundagi elementi; h₀[s,u] — uning 0-biti (eng kichik biti); x₀ … x₇ — baytning bitlari (x₀ — eng kichigi); Δ — XOR ayirma; o‘n oltilik qiymatlar 4×8 massiv ko‘rinishida satrma-satr yoziladi.")

# =================== I. CHIZIQLI ===================
PB(); H1('1. Chiziqli kriptotahlil')
H2('1.1. Standart algoritm')
H3('1.1.1. Akslantirishlarning approksimatsiya tenglamalari')
pm=MR['L1']['param']
P(f"*Qo‘sh.* Bitta element uchun (A, B toq, R juft) quyidagi tenglamalar aniq bajariladi. A ilova ma’lumotlarida 0-nuqtadagi holat[0,0] elementi uchun (R = {pm['R']}, A₁ = {pm['A1']}, B₁ = {pm['B1']}, A₂ = {pm['A2']}, B₂ = {pm['B2']}) barcha 256 kirishda tekshirildi:")
F(f"y₀ = x₀   (c = 1; 256/256),      y₁ = x₁ ⊕ x₀   (c = 1; {MR['L1']['y1'][1]}/256).")
P("Yuqori bitlar uchun eng yaxshi korrelyatsiyalar (shu element): " + ", ".join(f"y{j}: {fz(v,3)}" for j,v in enumerate(MR['L1']['bitc'])) + ".")
zb=XS['Z_bit0']
P("*BaytZichlash (Z jadvali).* Chiqishning 0-biti uchun eng yaxshi tenglama va umumiy eng yaxshi tenglama:")
a_=zb[0]; F(f"z₀ = {' ⊕ '.join(f'x{b}' for b in range(8) if (a_>>b)&1)}   (c = {zb[1]}/256 = {fz(zb[1]/256,3)}),      z₀ ⊕ z₂ = x₀ ⊕ x₂ ⊕ x₆ ⊕ x₇   (c = 0,25).")
P("Standart-128 dagi XOR uchun yᵢ = hᵢ ⊕ nᵢ (c = 1).")
P("*Aralash.* A ilova kalitining 0-qatlami bilan 0-qatlam bo‘yicha 32 ta tenglama (har biri c = 1) — 1-jadval. Masalan, 1-qator h′₀[0,0] = h₀[1,1] ⊕ h₀[2,2] ni bildiradi.")
rows=[["Chiqish","Tenglama: chiqishning 0-biti = kirish 0-bitlarining XOR yig‘indisi"]]+[[e[0],xor(e[1:])] for e in XS['aralash_tengl']]
T([1300,8054],rows,"Standart algoritm, A ilova kaliti: Aralash ning 0-qatlam tenglamalari",mono=(1,))
P("*SurHolat* — o‘rin almashtirish: chiqish [s,u] ← kirish [s′,u′] (2-jadval). *TuzilmaKalit* kₑ ning 0-qatlamini k ning 0-qatlamiga tenglashtiradi, shuning uchun Aralash tenglamalari barcha raundlarda bir xil.")
sur=XS['sur']; rows=[["Chiqish ← kirish"]*4]+[[f"{sur[r*4+i][0]} ← {sur[r*4+i][1]}" for i in range(4)] for r in range(8)]
T([2338,2338,2338,2340],rows,"SurHolat: pozitsiyalar almashinuvi",mono=(0,1,2,3))
H3('1.1.2. Raund tenglamasi')
P("Akslantirishlar tenglamalari birlashtirilib, yutishsiz raund uchun h₀⁽ʲ⁾ = L·h₀⁽ʲ⁻¹⁾ (L = P·M) tenglamasi hosil bo‘ladi (c = 1). A ilova kaliti uchun L ning barcha 32 ta qatori:")
rows=[["Chiqish","h₀⁽ʲ⁾[s,u] = … (j-raund kirishining 0-bitlari)"]]+[[e[0],xor(e[1:])] for e in XS['L_tengl']]
T([1300,8054],rows,"Standart algoritm, A ilova kaliti: raund tenglamasi (L matritsasi qatorlari)",mono=(1,))
P("L ning [0,3] qatorida yagona birlik bor: h₀⁽ʲ⁾[0,3] = h₀⁽ʲ⁻¹⁾[0,3] — bu bit har raundda o‘zgarmay o‘tadi (A ilova kaliti «eng yomon» kalit).")
H3('1.1.3. Tenglamaning raundlar bo‘yicha ko‘rinishi')
P("Raund tenglamalarini ketma-ket qo‘llab, 7-raunddan keyingi bitning 0-nuqtadagi yutishdan keyingi holat bitlari orqali ifodasi olinadi (c = 1). [0,0] va [0,3] bitlari uchun natija:")
for st in ('[0,0]','[0,3]'):
    rows=[["Raund","h₀⁽⁷⁾" + st + " ning ifodasi: shu raund kirishidagi 0-bitlar"]]
    for j,ps in XS['L_iz'][st]: rows.append([f"{j}-raund kirishi",xor(ps)])
    T([1700,7654],rows,f"h₀⁽⁷⁾{st} ning raundlar bo‘yicha orqaga ifodasi",mono=(1,))
iz=IZ
rows=[["Akslantirish (1-raund)","Holat","0-qatlam","Bashorat bilan mos"]]+[[opn.get(s['amal'],s['amal']),nl(s['holat']),nl(s['q0']),f"{s['mos']}/32"] for s in iz['steps']]
T([2300,3300,2300,1454],rows,"Standart-256, A ilova: 1-raund akslantirishlaridan keyingi holat va 0-qatlam tenglamasining bajarilishi",mono=(1,2))
T([2600]+[675]*10,[["Raund j"]+[str(j) for j in range(1,11)],["Mos bitlar (32 dan)"]+[str(v) for v in iz['raund']]],"Standart-256, A ilova: raund tenglamasining raundlar bo‘yicha bajarilishi")
H3('1.1.4. To‘liq approksimatsiya tenglamasi (xabar bitlaridan)')
P("[0,3] izi bo‘yicha xabar bitlaridan 7-raund chiqishigacha bo‘lgan to‘liq tenglama: 0-nuqtadagi BaytZichlash da holat[0,3] ning 0-biti Z(holatn[0,3]) ning 0-biti, holatn esa Qo‘sh(blok) natijasi (0-biti blok[0,3] ning 0-biti bilan aniq teng, yuqori bitlari ≈0,99–0,27 korrelyatsiya bilan):")
F(f"h₀⁽⁷⁾[0,3] = h₀⁽⁰⁾[0,3] = z₀(holatn[0,3]) ≈ n₀ ⊕ n₄ ⊕ n₆ ⊕ n₇   (n = holatn[0,3];  c ≤ {fz(zb[1]/256,3)}),")
P("ya’ni ichki holatning bitta biti 7 raund davomida xabarning bitta baytiga bog‘liq bitta tenglama bilan, korrelyatsiyasi ≤ 0,219 bilan ifodalanadi. Uchta yutish qatlamidan (0, 8, 9) o‘tuvchi to‘liq iz uchun |c| ≤ 0,219³ ≈ 2⁻⁶·⁶; 10-raund (c = 1) va chiqish munosabatlari qo‘shiladi.")
H3('1.1.5. Yakuniy natija: chiqishdagi c = 1 munosabatlar')
P("10-raund oxirgi yutishdan keyin bajarilgani uchun xesh qiymatning 0-qatlami L obrazida yotadi. A ilova kaliti uchun L ning chap yadrosidan quyidagi 8 ta munosabat olinadi; ularning har biri har qanday xabar uchun aniq bajariladi (c = 1):")
rows=[["№","Xesh qiymat 0-bitlari orasidagi munosabat"]]+[[str(i+1),xor(m)+" = 0"] for i,m in enumerate(XS['chiqish_munosabat'])]
T([800,8554],rows,"Standart-256, A ilova kaliti: xesh qiymatdagi chiziqli munosabatlar",mono=(1,))
af=XS['std128_affin']
P(f"*Standart-128.* Bu rejimda 0-qatlam butun xesh bo‘yicha chiziqli. A ilova kalitining birinchi 16 bayti bilan chiqish 0-bitlari xabar 0-bitlarining affin funksiyasi sifatida topildi (120 xabar bo‘yicha); 500 ta yangi xabarda tekshiruv aniqligi {fz(af['aniqlik'],3)}. Dastlabki oltita chiqish biti uchun to‘liq tenglamalar (mᵢ — xabarning i-yarim bayti 0-biti, oᵢ — xeshning i-yarim bayti 0-biti):")
rows=[["Chiqish","Tenglama (c = 1)"]]+[[o,(" ⊕ ".join(ms) if ms else "0")+(" ⊕ 1" if cst else "")] for o,ms,cst in af['tengl']]
T([1300,8054],rows,"Standart-128, A ilova kaliti: xesh qiymat 0-bitlarining to‘liq tenglamalari",mono=(1,))
H2('1.2. Yangilangan algoritm')
H3('1.2.1. Akslantirishlarning approksimatsiya tenglamalari')
P("*Aralash (toq kₑ).* kₑ ning barcha elementlari toq bo‘lgani uchun σᵤ = 4 ≡ 0 (mod 2) va 0-qatlam tenglamalari kalitga bog‘liq emas:")
F("h′₀[u,u] = ⊕_{i≠u} h₀[i,i],      h′₀[s,u] = ⊕ᵢ h₀[i,u] ⊕ ⊕_{i≠s,u} h₀[s,i]   (s ≠ u),")
P("bu matritsa teskarilanuvchi (rang 32) va 4×4 yarim uchun tarmoqlanish soni 6. Barcha 32 tenglama 9-jadvalda.")
rows=[["Chiqish","0-qatlam tenglamasi (har qanday kalit uchun)"]]+[[e[0],xor(e[1:])] for e in XY['aralash_tengl']]
T([1300,8054],rows,"Yangilangan algoritm: Aralash ning 0-qatlam tenglamalari (toq kₑ)",mono=(1,))
be=XY['bog_element']
P(f"*Bog‘lash elementi.* A ilova ma’lumotlarida 0-nuqtadagi Bog‘lash(holat, blok) ning 1-yarim qadamidagi o‘ng yarimning birinchi elementi (holat[0,4]) uchun parametrlar: J = {be['J']}, K = {be['K']}, a = 2·S({be['U0']} ⊕ {be['XU0']} ⊕ {be['J']}) + 1 = {be['a']}, b = 2·S({be['U1']} ⊕ {be['XT0']} ⊕ {be['K']}) + 1 = {be['b']}, R = {be['R']}, t = X_T[0] = {be['XT0']}. Shu parametrlardagi g(x) = S(−a·x·(b + R·x)⁻¹ ⊕ t) ning eng yaxshi approksimatsiya tenglamasi:")
F(f"⟨{be['beta']:02X}, g(x)⟩ = ⟨{be['alfa']:02X}, x⟩,   c = {be['W']}/256 = {fz(be['W']/256,3)}   (parametrlar bo‘yicha o‘rtacha: |c| ≤ {fz(YD['g_ortacha_c_max'],4)} ≈ 2⁻⁶).")
P("Parametrlar har chaqiruvda boshqa yarimning S-box chiqishlaridan olinadi, shuning uchun buzg‘unchi uchun samarali korrelyatsiya ≈2⁻⁶. 0-bit endi chiziqli emas: y₀ = x₀ tengligi faqat ≈50% hollarda bajariladi.")
P("*SBZ* uchun eng yaxshi tenglamalardan biri (barcha 65 536 juftlikda tekshirilgan):")
F("y₀ ⊕ (h₀ ⊕ h₂ ⊕ h₃ ⊕ h₅) ⊕ (n₁ ⊕ n₃ ⊕ n₄) = 1,   c = 2⁻⁶   (y = S(h ⊕ S(n))).")
P("*SurHolat* — standartdagidek o‘rin almashtirish (2-jadval). *Kalit jadvali* kₑ ← (SurKalit(kₑ) ⊕ RCⱼ) ∨ 1 chiziqli (konstanta bilan XOR va 0-bitni 1 ga tenglash). *Oldinga uzatish* — chiziqli XOR, *P(H) ⊕ H* — ikkita Bog‘lash.")
H3('1.2.2. Raundlar bo‘yicha minimal chiziqli izlar')
P("Bog‘lash orqali niqob buzg‘unchi uchun eng arzon yo‘l bilan — faqat o‘zgartiriladigan element orqali — o‘tkaziladi: chap yarimdagi niqobli bayt 1 ta, o‘ng yarimdagi 2 ta faol S-box beradi; Aralash orqali niqob 0-qatlamda Mᵀ bilan tarqaladi. Quyida 1, 2 va 3 raund uchun topilgan minimal izlar (niqob pozitsiyalari oxiridan boshlab orqaga) keltirilgan.")
for r in ('1','2','3'):
    d=XY['chiziqli_iz'][r]; rows=[["Qadam (orqaga)","Niqobli baytlar (0-bit)","Faol S"]]+[[q[0]," ".join(q[1]),str(q[2])] for q in d['qadamlar']]
    T([4300,3654,1400],rows,f"{r} raundli minimal chiziqli iz: jami {d['jami']} ta faol S-box, |c| ≤ 2" + "⁻" + str(3*d['jami']).translate(str.maketrans("0123456789","⁰¹²³⁴⁵⁶⁷⁸⁹")),mono=(1,))
P(f"Raundlar bo‘yicha minimal faol S-box lar soni: 256 bitli rejimda {', '.join(str(CH['lin_256'][str(r)]) for r in range(1,7))}; 128 bitli rejimda {', '.join(str(CH['lin_128_yagona'][str(r)]) for r in range(1,7))} (1…6 raund). 2⁻⁶⁴ va 2⁻³² chegaralariga 3 raundda erishiladi.")
H3('1.2.3. Akslantirishlar bo‘yicha holat (A ilova)')
rows=[["Akslantirish","Holat","0-qatlam"]]+[[f"{e['amal']} ({e['raund']})",nl(e['holat']),nl(e['q0'])] for e in XY['holat_iz']]
T([2900,3900,2554],rows,"Yangilangan algoritm, A ilova: 0-nuqta va 1-raund akslantirishlaridan keyingi holat",mono=(1,2))
P("Standart algoritmdan farqli o‘laroq, Bog‘lash dan keyingi 0-qatlam oldingi 0-qatlamning chiziqli funksiyasi emas; shuning uchun c = 1 bilan bajariladigan raund tenglamasi mavjud emas.")
r6=YR['32_6']; r6b=YR['16_6']
H3('1.2.4. Yakuniy natija')
P(f"Xesh qiymatning 0-qatlami to‘liq rangli (256 bitli rejimda {r6['rang']}, 128 bitli rejimda {r6b['rang']}), doimiy bitlar yo‘q (minimal chastota {fz(r6['minf'],3)}), 0-qatlamning affin modeli aniqligi {fz(r6['affin'],3)} va {fz(r6b['affin'],3)} — tasodifiy taxmin darajasi. Standart algoritmdagi 8 ta c = 1 munosabat va Standart-128 dagi to‘liq affin tenglamalar mavjud emas.")

# =================== II. DIFFERENSIAL ===================
PB(); H1('2. Differensial kriptotahlil')
H2('2.1. Standart algoritm')
H3('2.1.1. Akslantirishlarning optimal orttirmalari')
T([2600,3400,3354],[["Akslantirish","Optimal o‘tish","Ehtimollik"],["Qo‘sh elementi","80 → 80 (MSB ayirmasi)",f"≥ 254/256 (eng yaxshisi {D1['Qosh_ddt_max_max']}/256)"],["Z (BaytZichlash)",f"{XS['Z_ddt_best'][1]:02x} → 0 (ayirma so‘nadi)",f"{XS['Z_ddt_best'][0]}/256 = 0,156"],["XOR (128 bit)","Δh = Δn → 0 (kompensatsiya)","1"],["Aralash","MSB ayirmasi M(k₀) ustuni bo‘yicha tarqaladi; yadrodagi ayirma so‘nadi","1"],["SurHolat, SurKalit, TuzilmaKalit","pozitsiyalar almashinuvi","1"]],"Standart algoritm akslantirishlarining optimal orttirmalari")
H3('2.1.2. Optimal orttirmaning akslantirishlar va raundlar orqali o‘tishi')
P("Boshlang‘ich orttirma: 0-nuqtadagi yutishdan keyingi holatning [0,0] baytida MSB ayirmasi (Δ = 80). A ilova ma’lumotlarida har bir akslantirishdan keyingi ayirma (Δholat) va kₑ dagi faol baytlar:")
rows=[["Akslantirish (raund)","Δholat","Faol: holat / kₑ"]]+[[f"{opn.get(e['amal'],e['amal'])} ({e['raund']})",nl(e['d']),f"{e['faol']} / {e['faolk']}"] for e in XS['juft']]
T([3000,4300,2054],rows,"Standart-256, A ilova: MSB orttirmasining 1–3-raundlarda o‘tishi",mono=(1,))
P("1–2-raundlarda ayirma faqat MSB ko‘rinishida (80) saqlanadi va Aralash orqali M(k₀) ustuni bo‘yicha tarqaladi (1 → 2 → 4 bayt); 3-raundda J juftligi o‘zgarib, ayirma kₑ ga va quyi bitlarga tarqaladi.")
rows=[["Raund j"]+[str(j) for j in range(1,11)],["P(MSB izi), 3000 juftlik"]+[fz(r['msb'],3) for r in D3['256_std_D0a'] if r['op']=='Tuz'],["Faol baytlar"]+[fz(r['act'],1) for r in D3['256_std_D0a'] if r['op']=='Tuz']]
T([2850]+[650]*10,rows,"Standart-256: MSB orttirmasining raundlar bo‘yicha saqlanish ehtimolligi")
H3('2.1.3. Xabar blokidagi orttirma')
P("Blokning [0,0] va [1,1] baytlarida MSB ayirmasi (J yig‘indisini o‘zgartirmaydi):")
rows=[["Akslantirish (raund)","Δholat","Faol baytlar"]]+[[f"{opn.get(e['amal'],e['amal'])} ({e['raund']})",nl(e['d']),str(e['faol'])] for e in XS['D2']]
T([3000,4300,2054],rows,"Standart-256, A ilova: blok orttirmasining 0-nuqta va 1-raunddan o‘tishi",mono=(1,))
P("Qo‘sh(holat, blok) dan keyin holatda ayirma yo‘q (blok ayirmasi holatn da qoladi), BaytZichlash dan keyin u faqat quyi yarim baytlarga tushadi.")
H3('2.1.4. Yakuniy natija')
BL("256 bitli rejimda iz ehtimolligining yuqori chegarasi 8-nuqtadan keyin ≤ 2⁻⁷², 8- va 9-nuqtalardan keyin ≤ 2⁻¹⁵⁶ (talab 2⁻¹²⁸ — 9-raunddan keyin bajariladi).")
BL("128 bitli rejimda XOR ayirmani o‘zgarishsiz o‘tkazadi va kompensatsiya qilinadi; faqat yuqori bit-qatlam o‘zgartirilganda 0-qatlam ehtimollik 1 bilan saqlanadi — 2⁴⁸ murakkablikdagi kolliziya hujumi.")
BL("Aralash yadrosi orqali ≈3% juftliklarda ayirma 1-raunddayoq butunlay so‘nadi (ichki kolliziya).")
H2('2.2. Yangilangan algoritm')
H3('2.2.1. Bog‘lash orqali optimal (minimal faol S-box li) orttirma')
P("Bitta Bog‘lash chaqiruvi uchun kamida 8 ta faol S-box isbotlangan. Minimumga erishadigan qisqartirilgan orttirma: chap yarim nofaol, o‘ng yarimning ikkita baytida ayirma (masalan, [0,4] va [0,5]), buzg‘unchi ΔJ = ΔK = 0 ni tanlaydi (masalan, ayirmalar 256 moduli bo‘yicha qarama-qarshi va faqat yuqori bitlarda).")
T([2600,2500,2300,1954],[["Yarim qadam","Faol baytlar (kirish)","Faol S-box lar","Chiqishdagi faol baytlar"],["1: o‘ng ← f(chap)","chap: —; o‘ng: [0,4], [0,5]","2 ta chiqish S ([0,4], [0,5])","o‘ng: [0,4], [0,5]"],["2: chap ← f(o‘ng)","U = o‘ng: 2 ta bayt (ΔJ = ΔK = 0)","2 ta aᵢ (i = [0,4], [0,5] ga mos) + 2 ta bᵢ (i + 1 ∈ A_U) = 4","chap: — (chiqishlar bekor qilinadi)"],["3: o‘ng ← f(chap)","chap: —; o‘ng: [0,4], [0,5]","2 ta chiqish S","o‘ng: 2 ta bayt"],["Jami","","8 ta (p ≤ 2⁻⁴⁸)",""]],"Bog‘lash orqali minimal faol S-box li orttirma (o‘lchamlar modeli)")
P("Agar o‘ng yarimda faqat bitta bayt faol bo‘lsa, ΔJ ≠ 0 majburiy va 2-yarim qadamda 16 ta aᵢ S-box faollashadi (jami 18). Raund funksiyasi holat bo‘yicha bijeksiya bo‘lgani uchun ayirma nolga aylanmaydi: har raundda ≥ 16 ta faol S-box, p ≤ 2⁻⁹⁶.")
H3('2.2.2. Orttirmaning akslantirishlar, yarim qadamlar va raundlar orqali o‘tishi (A ilova)')
P("Boshlang‘ich holatning [0,0] baytida MSB ayirmasi. Har bir yarim qadam va akslantirishdan keyingi ayirma:")
rows=[["Qadam (raund)","Δholat","Faol baytlar"]]+[[f"{e['amal']} ({e['raund']})",nl(e['d']),str(e['faol'])] for e in XY['juft'] if e['raund']<=1]
T([3300,4300,1754],rows,"Yangilangan algoritm, A ilova: holat orttirmasining 0-nuqta va 1-raunddan o‘tishi",mono=(1,))
P("Chap yarimdagi bitta bayt ayirmasi 1-yarim qadamdayoq J va K orqali butun o‘ng yarimga (17 bayt), 2-yarim qadamdan keyin esa butun holatga (32 bayt) tarqaladi; keyingi barcha akslantirishlarda holat to‘liq faol. Standart algoritmda xuddi shu ayirma 2 raund davomida 1–4 baytda, faqat MSB ko‘rinishida qolar edi.")
H3('2.2.3. Xabar blokidagi orttirma')
rows=[["Qadam (raund)","Δholat","Faol baytlar"]]+[[f"{e['amal']} ({e['raund']})",nl(e['d']),str(e['faol'])] for e in XY['blok_juft'] if e['raund']==0]
T([3300,4300,1754],rows,"Yangilangan algoritm, A ilova: blok[0,0] dagi MSB orttirmasining yutish nuqtasidan o‘tishi",mono=(1,))
P("Blok ayirmasi Bog‘lash(holat, blok) ning parametrlari orqali holatga kiradi va yutish nuqtasidan keyin holat to‘liq faol. Kolliziya izi uchun buzg‘unchi holat ayirmasini yutishda nolga keltirishi kerak, bu esa har bir yutish nuqtasida kamida 5 ta faol S-box talab qiladi (Bog‘lash da 3 ta parametr S, SBZ da ichki S va Bog‘lash chiqishidagi S): bir blok uchun ≥ 15, NY bloki bilan ≥ 30 ta, p ≤ 2⁻¹⁸⁰.")
H3('2.2.4. Yakuniy natija')
T([3600,2877,2877],[["Ko‘rsatkich","Standart","Yangilangan"],["Bitta akslantirishning maks. ehtimolligi","Qo‘sh: ≥ 254/256; Z: 0,156","S-box: 2⁻⁶ (har bir faol S)"],["Raund boshiga minimal faol S-box","0 (yutishsiz raund)","16"],["Raund boshiga iz ehtimolligi","≈0,9 (MSB izi)","≤ 2⁻⁹⁶"],["Holat orttirmasi: talabga erishish (256)","9-raund","2-raund"],["Kolliziya izi (blok orttirmasi)","yutish nuqtasida so‘nish 0,156","≤ 2⁻¹⁸⁰"],["Ichki kolliziya (ayirma so‘nishi)","≈3%","0 (bijeksiya)"]],"Differensial tahlil: yakuniy natijalar")

# =================== III. ALGEBRAIK ===================
PB(); H1('3. Algebraik kriptotahlil')
H2('3.1. Standart algoritm')
H3('3.1.1. Akslantirishlar tenglamalari (A ilova qiymatlari bilan)')
a2=MR['A2']; x_=a2['x']
P(f"*Qo‘sh* — halqa ustidagi uch bosqichli tenglamalar; A ilova ma’lumotlarida holat[0,0] uchun: J₁h = {a2['J1h']}, J₁hn = {a2['J1hn']}, K₁h = {a2['K1h']}, A₁ = {a2['A1']}, B₁ = {a2['B1']}.")
T([1100,3100,3500,1654],[["Bosqich","O‘zgaruvchilar","Tenglama","Qiymat (mod 256)"],["1",f"x = {x_[0]:#04x}, x⁻¹ = {x_[1]:#04x}","x⁻¹·(B₁ + R·x) + A₁·x ≡ 0",str(a2['tekshiruv'][0])],["2",f"x⁻¹ = {x_[1]:#04x}, x⁻² = {x_[2]:#04x}","x⁻²·(B₂ + R·x⁻¹) + A₂·x⁻¹ ≡ 0",str(a2['tekshiruv'][1])],["3",f"x⁻² = {x_[2]:#04x}, x⁻³ = {x_[3]:#04x}","x⁻³·(B₂ + R·x⁻²) + A₂·x⁻² ≡ 0",str(a2['tekshiruv'][2])]],"Qo‘sh tenglamalarining A ilova qiymatlari bilan ko‘rinishi")
am=XS['aralash_misol']
P(f"*Aralash* — bichiziqli tenglamalar; 1-raunddagi h′[0,0] uchun A ilova qiymatlari bilan (σ₀ = Σᵢ kₑ[i,0] = {am['ke'][0]} + {am['ke'][1]} + {am['ke'][2]} + {am['ke'][3]} ≡ {am['sigma']}):")
F(f"h′[0,0] = h[0,0]·σ₀ − h[1,1]·kₑ[1,0] − h[2,2]·kₑ[2,0] − h[3,3]·kₑ[3,0] = {am['h'][0]}·{am['sigma']} − {am['h'][1]}·{am['ke'][1]} − {am['h'][2]}·{am['ke'][2]} − {am['h'][3]}·{am['ke'][3]} ≡ {am['qiymat']}   (haqiqiy qiymat {am['haqiqiy']}).")
za=XS['z0_anf']
P(f"*BaytZichlash (Z)*: har bir chiqish biti 8 o‘zgaruvchili {za['daraja']}-darajali ko‘phad; z₀ ning ANF ida {za['jami']} ta monom, ulardan darajasi ≤ 2 bo‘lganlari: " + " ⊕ ".join(za['past']) + " ⊕ … (yuqori darajali hadlar). Implitsit ko‘rinishda har bir Z uchun 43 ta kub tenglama, kvadrat tenglamalar yo‘q. *XOR* (128 bit): yᵢ = hᵢ ⊕ nᵢ.")
H3('3.1.2. Raund tenglamalari va tizimlar')
F("a = Aralash(h⁽ʲ⁻¹⁾, kₑ⁽ʲ⁻¹⁾);  (b, c) = Qo‘sh(a, kₑ⁽ʲ⁻¹⁾);  b′ = P·b, c′ = Q·c;  (h⁽ʲ⁾, d) = Qo‘sh(b′, c′);  kₑ⁽ʲ⁾ = TuzilmaKalit(d, k).")
E=A3['eq']
rows=[["Rejim","1 raund: o‘zg. / tengl.","2 raund: o‘zg. / tengl.","3 raund: o‘zg. / tengl."]]
for key,lab in (('256_std','Standart-256'),('128_std','Standart-128')): rows.append([lab]+[f"{sp(E[key][r][0])} / {sp(E[key][r][1])}" for r in ('r1','r2','r3')])
T([2050,2450,2450,2400],rows,"Standart algoritm: bit darajasidagi tenglamalar tizimlari")
P("0-qatlam qismi barcha yutishsiz raundlarda chiziqli tizim (1.1.2-band): h₀⁽ʲ⁾ = L·h₀⁽ʲ⁻¹⁾; Standart-128 da yutish ham chiziqli, shuning uchun bu tizim butun xesh bo‘yicha chiziqli va 1.1.5-banddagi to‘liq affin tenglamalarga keladi.")
H3('3.1.3. Darajaning raundlar bo‘yicha o‘sishi')
def cr(key,lay=None):
    row=A2[key]; return [fz((row[str(d_)][1][lay] if lay is not None else row[str(d_)][0]),2) for d_ in (2,4,6,8,10,12)]
rows=[["Rejim, raund r","d = 2","d = 4","d = 6","d = 8","d = 10","d = 12"]]
for r in (0,1,2): rows.append([f"Standart-256, r = {r}"]+cr(f'256_std_r{r}'))
for r in (0,1,3): rows.append([f"Standart-128, r = {r} (0-qatlam)"]+cr(f'16_std_r{r}',0))
T([3150,1030,1030,1030,1030,1030,1030],rows,"Standart algoritm: kub testlari (yig‘indisi doim nol bitlar ulushi)")
H2('3.2. Yangilangan algoritm')
H3('3.2.1. Akslantirishlar tenglamalari (A ilova qiymatlari bilan)')
P("*Bog‘lash elementi* — oraliq o‘zgaruvchilar u, v, w bilan (1.2.1-banddagi element, A ilova qiymatlari):")
T([3000,4000,2354],[["Tenglama","Qiymatlar bilan","Natija"],["J = Σ U,  K = Π (U ∨ 1)","chap yarim bo‘yicha",f"J = {be['J']}, K = {be['K']}"],["u = S(U[0] ⊕ X_U[0] ⊕ J),  a = 2u + 1",f"u = S({be['U0']} ⊕ {be['XU0']} ⊕ {be['J']})",f"u = {be['u']}, a = {be['a']}"],["v = S(U[1] ⊕ X_T[0] ⊕ K),  b = 2v + 1",f"v = S({be['U1']} ⊕ {be['XT0']} ⊕ {be['K']})",f"v = {be['v']}, b = {be['b']}"],["w·(b + R·T) + a·T ≡ 0 (mod 256)",f"{be['w']}·({be['b']} + {be['R']}·{be['T']}) + {be['a']}·{be['T']}",f"≡ {be['tekshiruv']}  (w = {be['w']})"],["T′ = S(w ⊕ X_T[0])",f"S({be['w']} ⊕ {be['XT0']})",f"T′ = {be['yangi']}"]],"Bog‘lash elementi tenglamalarining A ilova qiymatlari bilan ko‘rinishi")
P("Har bir S tenglamasi bit darajasida 39 ta kvadrat tenglama (x·y = 1 munosabatidan: 23 ta bi-affin va 16 ta to‘liq kvadrat) bilan yoziladi; Möbius tenglamasi — halqa ustidagi kvadrat tenglama; J, K — qo‘shish va ko‘paytirish zanjirlari. Bitta element uchun 3 ta S-box, 4 ta modul ko‘paytirish va 2 ta qo‘shish.")
P("*SBZ*: u = S(n), v = h ⊕ u, y = S(v) — har bir bayt uchun 16 ta yangi o‘zgaruvchi, 8 ta chiziqli va 78 ta kvadrat tenglama. *Aralash* — standartdagidek bichiziqli (kₑ toq). *Kalit jadvali, SurHolat, oldinga uzatish* — chiziqli.")
H3('3.2.2. Raund tenglamalari va tizimlar')
F("a = Aralash(h⁽ʲ⁻¹⁾, kₑ⁽ʲ⁻¹⁾);  b = Bog‘lash(a, kₑ⁽ʲ⁻¹⁾);  b′ = P·b;  kₑ⁽ʲ⁾ = (Q·kₑ⁽ʲ⁻¹⁾ ⊕ RCⱼ) ∨ 1;  h⁽ʲ⁾ = Bog‘lash(b′, kₑ⁽ʲ⁾).")
def cnt(n):
    ADD=(2*n-1,2*n-1,n-1); MUL=(n*(n+1)//2+(n-1)*(2*n-1),)*2+(n*(n+1)//2+(n-1)*(n-1),); Sx=(8,39,39)
    add=lambda a,b,f=1: tuple(x+f*y for x,y in zip(a,b)); return ADD,MUL,Sx,add
def bog(m):
    ADD,MUL,Sx,add=cnt(8); h=(0,0,0)
    h=add(h,ADD,m-1); h=add(h,MUL,m-1); h=add(h,Sx,3*m); h=add(h,MUL,3*m); h=add(h,ADD,2*m); return add((0,0,0),h,3)
def aral(n,cnt_=128): ADD,MUL,Sx,add=cnt(n); return add(add((0,0,0),MUL,cnt_),ADD,cnt_+16)
tot=lambda *xs: tuple(sum(v) for v in zip(*xs))
b2_=bog(16); b1_=bog(8); s2=(512,2496,2496); s1=(256,1248,1248)
rn2=tot(aral(8),b2_,b2_); rn1=tot(aral(8,64),b1_,b1_); r02=tot(b2_,s2); r01=tot(b1_,s1)
rows=[["Rejim","Bitta Bog‘lash: o‘zg. / tengl.","1 raund","2 raund","3 raund"]]
rows.append(["256",f"{sp(b2_[0])} / {sp(b2_[1])}"]+[f"{sp(r02[0]+k*rn2[0])} / {sp(r02[1]+k*rn2[1])}" for k in (1,2,3)])
rows.append(["128",f"{sp(b1_[0])} / {sp(b1_[1])}"]+[f"{sp(r01[0]+k*rn1[0])} / {sp(r01[1]+k*rn1[1])}" for k in (1,2,3)])
T([900,2300,2050,2050,2054],rows,"Yangilangan algoritm: bit darajasidagi tenglamalar tizimlari (yutish nuqtasi bilan, baho)")
H3('3.2.3. Darajalar')
dg=YD['bog_daraja']
P(f"Bitta Bog‘lash chaqiruvidan keyin barcha 256 ta chiqish biti bitta kirish baytiga nisbatan 7 yoki 8-darajali ({', '.join(f'{k}-daraja: {v} ta' for k,v in dg.items())}); SBZ chiqishi 16 kirish bitiga nisbatan 13-darajali. Kub testlarida (Bog‘lash asosidagi variant) yutish nuqtasidan keyinoq yig‘indisi nol bitlar ulushi tasodifiy funksiya darajasida: 256 bitli rejimda r = 0 da d = 4, 8, 10 uchun {', '.join(fz(YT['raund_256']['kub'][f'r0_d{d}'][0],3) for d in (4,8,10))}.")
H3('3.2.4. Yakuniy natija')
T([3600,2877,2877],[["Ko‘rsatkich","Standart","Yangilangan"],["Eng yuqori darajali element","Z: 6 (128 bitda XOR: 1)","S-box: 7; SBZ: 13; Bog‘lash: 7–8"],["0-qatlam tizimi","chiziqli (yutishsiz raundlarda; 128 bitda butun xesh)","chiziqli qism yo‘q"],["Linearizatsiya (0-qatlam, 128 bit)","80 so‘rov, aniqlik 1,00","aniqlik ≈0,50"],["Kub testi, r = 0, d = 12 (256)","0,84","tasodifiy daraja"]],"Algebraik tahlil: yakuniy natijalar")

# =================== IV. INTEGRAL ===================
PB(); H1('4. Integral kriptotahlil')
P("To‘plam xossalari: A — barcha 256 qiymat bir martadan; C — doimiy; B — XOR yig‘indisi 00; B₇ — XOR yig‘indisi 80 (0–6-bitlar balanslangan); U — noma’lum. Har bir jadvalda 4×8 massivning har bir pozitsiyasi uchun xossa va to‘plam bo‘yicha XOR yig‘indisining 0-biti (0 — 0-bit balanslangan) ko‘rsatiladi.")
H2('4.1. Standart algoritm')
H3('4.1.1. Holatdagi faol bayt (0-nuqtadagi yutishdan keyin holat[0,0] faol)')
rows=[["Akslantirish (raund)","Pozitsiyalar xossasi","XOR yig‘indisining 0-biti"]]+[[f"{opn.get(e['amal'],e['amal'])} ({e['raund']})",nl(e['klass']),nl(e['q0'])] for e in XS['int_holat']]
T([2700,4000,2654],rows,"Standart-256, A ilova: holatdagi faol to‘plamning akslantirishlar va raundlardan keyingi ko‘rinishi",mono=(1,2))
P("Aralash faol to‘plamni A, B va C pozitsiyalariga o‘tkazadi; Qo‘sh dan keyin pozitsiyalar U ga aylanadi, lekin XOR yig‘indisining 0-biti barcha 32 pozitsiyada 0 bo‘lib qoladi (0-qatlam balansi) va bu 7 raund davomida saqlanadi; 8-raunddagi BaytZichlash dan keyin balans yo‘qoladi.")
H3('4.1.2. Blokdagi faol bayt (blok[0,0] faol)')
rows=[["Akslantirish (raund)","Pozitsiyalar xossasi","XOR yig‘indisining 0-biti"]]+[[f"{opn.get(e['amal'],e['amal'])} ({e['raund']})",nl(e['klass']),nl(e['q0'])] for e in XS['int_blok']]
T([2700,4000,2654],rows,"Standart-256, A ilova: blokdagi faol to‘plamning ko‘rinishi",mono=(1,2))
P("Standart-128 da 0-qatlam balansi butun xesh bo‘yicha saqlanadi: xesh qiymatning 32 ta 0-biti to‘plam bo‘yicha doim balanslangan (to‘liq xesh uchun integral farqlovchi).")
H2('4.2. Yangilangan algoritm')
H3('4.2.1. Holatdagi faol bayt (boshlang‘ich holat[0,0] faol)')
rows=[["Qadam (raund)","Pozitsiyalar xossasi","XOR yig‘indisining 0-biti"]]+[[f"{e['amal']} ({e['raund']})",nl(e['klass']),nl(e['q0'])] for e in XY['int_holat'] if e['raund']<=1]
T([3000,3900,2454],rows,"Yangilangan algoritm, A ilova: holatdagi faol to‘plamning yarim qadamlar va akslantirishlardan keyingi ko‘rinishi",mono=(1,2))
P("1-yarim qadamda faol bayt chap yarimda o‘zgarmay qoladi (A), uning ta’siri J va K orqali o‘ng yarimning barcha elementlariga U sifatida tarqaladi; 2-yarim qadamdan keyin barcha pozitsiyalar U, 0-qatlam balansi ham yo‘qoladi.")
H3('4.2.2. Blokdagi faol bayt (blok[0,0] faol)')
rows=[["Qadam (raund)","Pozitsiyalar xossasi","XOR yig‘indisining 0-biti"]]+[[f"{e['amal']} ({e['raund']})",nl(e['klass']),nl(e['q0'])] for e in XY['int_blok'] if e['raund']<=1]
T([3000,3900,2454],rows,"Yangilangan algoritm, A ilova: blokdagi faol to‘plamning ko‘rinishi",mono=(1,2))
H3('4.2.3. Yakuniy natija')
T([3600,2877,2877],[["Ko‘rsatkich","Standart","Yangilangan"],["Holat bo‘yicha integral farqlovchi","7 raund (0-qatlam, 32 bit)","yo‘q (1-chaqiruvdan keyin)"],["Blok bo‘yicha faol to‘plam","BaytZichlash gacha 0-qatlam balansi","1-raund Bog‘lash dan keyin yo‘qoladi"],["To‘liq xesh, 256 bit","farqlovchi yo‘q","farqlovchi yo‘q"],["To‘liq xesh, 128 bit","32 bitli farqlovchi","farqlovchi yo‘q (R = 6 da 0–1 bit, tasodifiy daraja)"]],"Integral tahlil: yakuniy natijalar")

PB(); H1('Umumiy yakuniy natijalar')
T([2200,3577,3577],[["Usul","Standart algoritm","Yangilangan algoritm (R = 6)"],
 ["Chiziqli","yutishsiz raundlarda c = 1 (L tenglamasi); chiqishda 8 ta c = 1 munosabat (A ilova kaliti); 128 bitda to‘liq affin tenglamalar","raund boshiga ≥ 2 faol S, 3 raundda ≥ 26 (256) / 20 (128) — |c| ≤ 2⁻⁷⁸ / 2⁻⁶⁰; chiqishda munosabat yo‘q"],
 ["Differensial","MSB izi raundga ≈0,9; Z da 0,156 bilan so‘nish; ≈3% ichki kolliziya","raund boshiga ≥ 16 faol S (p ≤ 2⁻⁹⁶); kolliziya izi ≤ 2⁻¹⁸⁰; ichki kolliziya yo‘q"],
 ["Algebraik","0-qatlam chiziqli; Z — 6, XOR — 1; 128 bitda linearizatsiya 100%","Bog‘lash — 7–8, SBZ — 13; 0-qatlamda ham chiziqli qism yo‘q"],
 ["Integral","0-qatlam 7 raund balanslangan; 128 bitda to‘liq xesh farqlovchisi","balans birinchi Bog‘lash chaqiruvida yo‘qoladi; farqlovchi yo‘q"]],"Standart va yangilangan algoritmni to‘rtta usul bo‘yicha solishtirish")
P("Barcha qiymatlar uzmst285_tahlil paketidagi dasturlar bilan A ilova ma’lumotlarida hisoblangan; statistik ko‘rsatkichlar oldingi hisobotlardagi tanlanmalardan olingan.")
json.dump(B,open('blocks.json','w'),ensure_ascii=False); print(len(B),tc[0])
