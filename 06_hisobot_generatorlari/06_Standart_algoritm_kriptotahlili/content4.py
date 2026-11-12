import json, math
K='/home/claude/ka/'; J=lambda f: json.load(open(K+f+'.json'))
L1,L2,L3,D1,A1,A2,A3,EX,AB,IZ=[J(x) for x in ['lin1','lin2','lin3','dif1','alg1','alg2','alg3','ex','aralash_bit1','std_iz']]
D2=J('dif2'); XE=J('extra'); MR=json.load(open('/home/claude/nb/misollar_natijalari.json')); D3=J('dif3'); I=json.load(open('/home/claude/pkg/uzmst285_tahlil/natijalar/integral.json'))
B=[]; tc=[0]; fc=[0]
H1=lambda t:B.append(['h1',t]); H2=lambda t:B.append(['h2',t]); H3=lambda t:B.append(['h3',t])
P=lambda t:B.append(['p',t]); F=lambda t:B.append(['f',t]); BL=lambda t:B.append(['b',t]); PB=lambda:B.append(['pb'])
TK={}
def T(w,rows,cap,mono=(),key=None):
    tc[0]+=1; B.append(['cap',f"{tc[0]}-jadval. {cap}"]); B.append(['t',w,rows,list(mono)])
    if key: TK[key]=tc[0]
def IMG(p,w,h,cap): fc[0]+=1; B.append(['img',p,w,h]); B.append(['fcap',f"{fc[0]}-rasm. {cap}"])
fz=lambda x,d=2:(f'{x:.{d}f}').replace('.',','); nl='\n'.join
sp=lambda n:f"{n:,}".replace(',',' ')
opn={'Aralash':'Aralash(holat, kₑ)','Qosh1':'Qo‘sh(holat, kₑ)','Sur':'SurHolat, SurKalit','Qosh2':'Qo‘sh(holat, kₑ)','Tuz':'TuzilmaKalit(kₑ, k)','Qosh0':'Qo‘sh(holat, blok)','BZ0':'BaytZichlash (0-nuqta)','BZ8':'BaytZichlash (8-nuqta)','BZ9':'BaytZichlash (9-nuqta)','Qosh_inj8':'Qo‘sh(holat, blok)','Qosh_inj9':'Qo‘sh(holat, blok)'}

B.append(['title','O‘zMSt 285:2024 XESH FUNKSIYASI 1-ALGORITMINING CHIZIQLI, DIFFERENSIAL, ALGEBRAIK VA INTEGRAL KRIPTOTAHLILI'])
B.append(['sub','Standart algoritm (BaytZichlash bilan) bo‘yicha hisobot'])
H1('Kirish')
P("Ushbu hisobotda O‘zMSt 285:2024 standartining 1-algoritmi uning standartdagi ko‘rinishida, ya’ni yutish nuqtasida *BaytZichlash* o‘zgartirishi bilan, to‘rtta kriptotahlil usuli bo‘yicha buzg‘unchi nuqtai nazaridan baholanadi: chiziqli, differensial, algebraik va integral (square) kriptotahlil. Har bir usul bo‘yicha avval algoritmning har bir akslantirishi alohida o‘rganiladi, so‘ngra natijalar raund darajasida birlashtiriladi va algoritm qaysi raunddan keyin tegishli hujumga bardoshli bo‘lishi (yoki bardoshli emasligi) aniqlanadi.")
P("Algoritmning ikkala rejimi ko‘rib chiqiladi: *Standart-256* (p = 256, kirish bloki va kalit 256 bit, yutish nuqtasida B ilovadagi 1×256 chiziqli zichlash massivi) va *Standart-128* (p = 16, 128 bit, yutish nuqtasida yarim baytlarni XOR qilish). Hisob-kitoblar mustaqil dasturiy realizatsiyada bajarildi; u standartning A ilovasidagi nazorat misolini bayt-ma-bayt takrorlaydi (masalan, A ilovadagi birinchi «BaytZichlash(holat, holatn)» natijasi 44 a6 2b c4 3c 65 d7 7a … bilan aynan mos keladi). Akslantirishlar ko‘rsatkichlari barcha kirishlar bo‘yicha to‘liq, raund darajasidagi ko‘rsatkichlar esa tasodifiy kalit, holat va xabarlarda tanlanma asosida o‘lchandi.")
H2('Algoritm tuzilishi va belgilashlar')
P("Ichki holat — 4×8 massiv (holat), raund kaliti — 4×8 massiv (kₑ). Xabar bloklarga ajratiladi, ularga uzunlik va NY bloklari qo‘shiladi; birinchi blok boshlang‘ich holat bo‘ladi, qolgan har bir blok uchun bitta tashqi iteratsiya (10 raund) bajariladi. ⟦struct⟧-jadvalda bitta iteratsiyadagi akslantirishlar ketma-ketligi keltirilgan.")
T([1700,7650],[["Qadam","Akslantirishlar"],["0-nuqta","Qo‘sh(holat, blok), BaytZichlash(holat, holatn) — yutish"],["1–7-raundlar","Aralash(holat, kₑ) → Qo‘sh(holat, kₑ) → SurHolat, SurKalit → Qo‘sh(holat, kₑ) → TuzilmaKalit(kₑ, k)"],["8-raund","Aralash → Qo‘sh(holat, kₑ) → SurHolat, SurKalit → Qo‘sh(holat, blok), BaytZichlash — yutish → TuzilmaKalit"],["9-raund","1–7-raundlar kabi; oxirida Qo‘sh(holat, blok), BaytZichlash — yutish"],["10-raund","1–7-raundlar kabi"]],"Bitta tashqi iteratsiyadagi akslantirishlar",key='struct')
P("Hisobotda quyidagi belgilashlar ishlatiladi. *Bit-qatlam j* — holatning barcha 32 ta elementidagi j-bitlar to‘plami; *0-qatlam* — elementlarning eng kichik bitlari (juft/toqlik). *Yutish nuqtasi* — kirish bloki holatga qo‘shiladigan va BaytZichlash bajariladigan nuqta. *Faol bayt* — niqobi (chiziqli tahlil) yoki ayirmasi (differensial tahlil) noldan farqli bayt. *T-funksiya* — natijaning j-biti kirishlarning faqat 0…j-bitlariga bog‘liq bo‘lgan akslantirish; 2ⁿ moduli bo‘yicha qo‘shish, ko‘paytirish va teskarilash T-funksiyalardir. Integral tahlil uchun to‘plam xossalari: A (barcha qiymatlarni bir martadan qabul qiladi), C (doimiy), B (XOR-yig‘indisi nol, balanslangan), U (noma’lum).")
P("Asosiy strukturaviy kuzatish: 1–7- va 10-raundlardagi barcha akslantirishlar (Aralash, Qo‘sh, SurHolat, SurKalit, TuzilmaKalit) 2ⁿ moduli bo‘yicha arifmetika va o‘rin almashtirishlardan iborat. Shuning uchun 0-qatlam bu raundlarda boshqa bitlar bilan aralashmaydi. Yuqori bitlardagi axborotni quyi bitlarga o‘tkazuvchi yagona element — yutish nuqtasidagi BaytZichlash. Bu kuzatish to‘rttala usulning natijalarini ham belgilaydi.")

# ======================= 1. CHIZIQLI =======================
PB(); H1('1. Chiziqli kriptotahlil')
H2('1.1. Usulning mohiyati va bardoshlilik mezoni')
P("Chiziqli kriptotahlilda buzg‘unchi kirish va chiqish bitlarining XOR yig‘indilari orasidagi, ehtimolligi 1/2 dan farq qiladigan tengliklarni (chiziqli approksimatsiyalarni) qidiradi. F akslantirish uchun kirish niqobi α va chiqish niqobi β bo‘lgan approksimatsiyaning korrelyatsiyasi va chetlanishi:")
F("c_F(α → β) = 2⁻ⁿ · Σₓ (−1)^(β·F(x) ⊕ α·x),      ε = c/2.")
P("Barcha (β, α) juftliklari uchun c qiymatlaridan tuzilgan matritsa *korrelyatsion matritsa* deyiladi. Raundlar bo‘yicha chiziqli iz korrelyatsiyasi oraliq korrelyatsiyalar ko‘paytmasiga teng (c_iz = Π cᵢ), hujum uchun zarur ma’lumotlar hajmi N ≈ c⁻². Shuning uchun 256 bitli xesh uchun chiziqli farqlovchi umumiy hujumdan (2¹²⁸) samaraliroq bo‘lmasligi uchun |c| ≤ 2⁻⁶⁴, 128 bitli rejim uchun |c| ≤ 2⁻³² talab qilinadi.")
H2('1.2. Akslantirishlarning korrelyatsion matritsalari va approksimatsiya tenglamalari')
H3('1.2.1. BaytZichlash: zichlash massivi Z (Standart-256)')
dz=L1['Z_lat_dist']
P("Standart-256 da yangi holat bayti Z(h) ‖ Z(n) ko‘rinishida hosil bo‘ladi: yuqori yarim bayt holat baytidan, quyi yarim bayt Qo‘sh dan keyingi holatn baytidan olinadi. Z — 8 bitni 4 bitga siquvchi jadval, uning korrelyatsion matritsasi 15×256 o‘lchamli (noldan farqli chiqish niqoblari). Matritsa to‘liq hisoblandi, elementlar taqsimoti ⟦zdist⟧-jadvalda keltirilgan.")
T([2900]+[717]*9,[["|W| = 256·|c|","0","8","16","24","32","40","48","56","64"],["Elementlar soni"]+[str(dz[str(v)]) for v in (0,8,16,24,32,40,48,56,64)]],"Z korrelyatsion matritsasi elementlarining taqsimoti",key='zdist')
P("Korrelyatsion matritsa quyidagi tartibda qurildi: har bir chiqish niqobi β (1…15) uchun β·Z(x) bitining ±1 ko‘rinishidagi qiymatlari vektori tuzildi va unga Uolsh–Adamar o‘zgartirishi qo‘llanildi; natijada bir yo‘la barcha 256 ta kirish niqobi α uchun W(α → β) = Σₓ (−1)^(β·Z(x) ⊕ α·x) qiymatlari olinadi. Matritsaning bir qismi ⟦zlat⟧-jadvalda keltirilgan (oxirgi ustun — eng yaxshi approksimatsiyaga mos α = C5).")
zb=EX['Z_lat_block']
T([1100]+[917]*9,[["β \\ α","01","02","04","08","10","20","40","80","C5"]]+[[f"{b:X}"]+[str(v) for v in zb[b-1]] for b in range(1,16)],"Z korrelyatsion matritsasining bo‘lagi: W(α → β) = 256·c",key='zlat')
P(f"Maksimal |c| = 64/256 = 0,25 (chetlanish 2⁻³) bitta approksimatsiyada erishiladi; chiqishning 0-biti uchun eng yaxshi korrelyatsiya {fz(L1['Z_out_bit0_best'],3)}. Eng yaxshi approksimatsiya tenglamasi:")
F("z₀ ⊕ z₂ = x₀ ⊕ x₂ ⊕ x₆ ⊕ x₇,     c = 0,25   (z = Z(x)).")
P("Bu tenglama 256 ta kirishdan 160 tasida bajariladi. Taqqoslash uchun: 300 ta tasodifiy muvozanatli 8 → 4 jadvalning medianasi |W| = 60, ya’ni Z tasodifiy jadval darajasida, lekin kriptografik jihatdan optimallashtirilmagan (AES S-box da maksimal |c| = 2⁻³). Bundan tashqari, BaytZichlash tuzilishi tufayli holat baytining axboroti faqat yuqori yarim baytga, holatn baytining axboroti faqat quyi yarim baytga tushadi; 16 bitli kirish va 8 bitli chiqish orasidagi 128 ta bog‘liqlikdan faqat 64 tasi mavjud. Butun 16 → 8 akslantirish uchun maksimal |c| = 0,25, algebraik daraja 6.")
H3('1.2.2. BaytZichlash: XOR (Standart-128)')
P("128 bitli rejimda yutish yarim baytlarni bitma-bit qo‘shish bilan bajariladi: y = h ⊕ n. Har bir bit uchun approksimatsiya tenglamasi aniq bajariladi:")
F("yᵢ = hᵢ ⊕ nᵢ,     c = 1   (i = 0, 1, 2, 3).")
P("Ya’ni yutish nuqtasi chiziqli tahlil nuqtai nazaridan hech qanday qarshilik ko‘rsatmaydi.")
H3('1.2.3. Qo‘sh o‘zgartirishi')
qa,qm,qs=L1['Qosh_bitj_bestcorr_avg'],L1['Qosh_bitj_bestcorr_min'],L1['Qosh_bitj_corr_avg']
P("Qo‘sh har bir elementni (A, B, R) parametrli −3 darajaga ko‘taradi: x → x⁻¹ → x⁻² → x⁻³, bunda x⁻¹ ≡ −A·x·(B + R·x)⁻¹ (mod p). A va B parametrlari massivlarning yig‘indilari (J) va ko‘paytmalari (K) orqali aniqlanadi va doim toq; R kalitning birinchi elementi, juft. Shuning uchun (B + R·x) toq va x⁻¹ ≡ x (mod 2):")
F("y₀ = x₀,     c = 1.")
P("Bitta element uchun (parametrlar belgilangan) 256×256 korrelyatsion matritsa 200 ta tasodifiy parametrlar to‘plamida hisoblandi (⟦qoshlat⟧-jadval).")
T([2880]+[808]*8,[["Chiqish biti j","0","1","2","3","4","5","6","7"],["Eng yaxshi |c| (o‘rtacha)"]+[fz(v,3) for v in qa],["Eng yaxshi |c| (minimum)"]+[fz(v,3) for v in qm],["|c(xⱼ → yⱼ)| (o‘rtacha)"]+[fz(v,3) for v in qs]],"Qo‘sh elementining bit-qatlamlar bo‘yicha korrelyatsiyalari",key='qoshlat')
pm=MR['L1']['param']
P(f"Misol sifatida A ilova ma’lumotlaridagi 0-nuqta Qo‘sh o‘zgartirishining holat[0,0] elementi olindi: R = {pm['R']}, A₁ = {pm['A1']}, B₁ = {pm['B1']}, A₂ = {pm['A2']}, B₂ = {pm['B2']}. Shu parametrlar bilan barcha 256 kirish tekshirildi: y₀ = x₀ tengligi {MR['L1']['y0_ok']}/256 kirishda, y₁ = x₁ ⊕ x₀ tengligi {MR['L1']['y1'][1]}/256 kirishda bajariladi; chiqish bitlari uchun eng yaxshi korrelyatsiyalar: " + ", ".join(fz(v,3) for v in MR['L1']['bitc']) + ".")
P("0-bit doim chiziqli (c = 1), 1-bit deyarli doim chiziqli: y₁ = x₁ ⊕ δ·x₀, δ ∈ {0, 1} parametrlarga bog‘liq, c ≥ 0,992. 2- va 3-bitlar uchun o‘rtacha 0,77 va 0,69 korrelyatsiyali chiziqli tenglamalar mavjud, yuqori bitlarda korrelyatsiya kamayadi (7-bit uchun 0,27). Elementlar orasidagi bog‘lanish (J va K) 0-qatlamga ta’sir qilmaydi, chunki Δ = 10 tuzatmasi va nolni A₂ + B₂ ga almashtirish qoidasi juft qiymatlar qo‘shadi.")
H3('1.2.4. Aralash o‘zgartirishi')
P("Aralash holat va raund kaliti massivlarining chap va o‘ng 4×4 yarimlarini diamatritsa qoidasi bo‘yicha 2ⁿ moduli bo‘yicha ko‘paytiradi. Belgilangan kₑ uchun u h ga nisbatan Z/2ⁿ ustida chiziqli, shuning uchun 0-qatlam bo‘yicha aniq chiziqli tenglamalar o‘rinli (σᵤ = Σᵢ kₑ[i,u]₀):")
F("h′[u,u]₀ = σᵤ·h[u,u]₀ ⊕ Σ_{i≠u} kₑ[i,u]₀·h[i,i]₀,")
F("h′[s,u]₀ = σᵤ·h[s,u]₀ ⊕ kₑ[s,u]₀·Σᵢ h[i,u]₀ ⊕ Σ_{i≠s,u} kₑ[i,u]₀·h[s,i]₀   (s ≠ u).")
P(f"Bu tenglamalar c = 1 bilan bajariladi va h′₀ = M(k₀)·h₀ ko‘rinishida yoziladi; M(k₀) — 32×32 o‘lchamli GF(2) matritsa, u faqat kalitning 0-qatlamiga bog‘liq. A ilova kaliti uchun, masalan, h′[0,0]₀ = h[1,1]₀ ⊕ h[2,2]₀. 1-bit qatlamda ko‘chirishlar paydo bo‘ladi: holat′[0,0] ning 1-biti 8 ta kirish bitining funksiyasi bo‘lib, 300 ta kalit bo‘yicha uning eng yaxshi chiziqli approksimatsiyasining korrelyatsiyasi o‘rtacha {fz(AB['aralash_bit1_ortacha'],2)} (minimum {fz(AB['min'],2)}), kalitlarning {fz(100*AB['c1_ulushi'],1)} foizida esa 1 ga teng.")
H3('1.2.5. SurHolat, SurKalit, TuzilmaKalit')
P("SurHolat va SurKalit elementlarni pozitsiyalar bo‘yicha davriy suradi; chiziqli izdagi niqob ham shunchaki boshqa pozitsiyalarga ko‘chadi, korrelyatsiya 1. SurHolat ni 32×32 o‘rin almashtirish matritsasi P bilan ifodalaymiz. TuzilmaKalit kₑ ni o‘zgartiradi va har raundda kₑ₀ = k₀ tengligini ta’minlaydi: kₑ ning 0-qatlami har doim kalitning 0-qatlamiga teng (nol kirish niqobli, c = ±1 bo‘lgan tenglamalar). Shu sababli Aralash dagi M(k₀) matritsasi barcha raundlarda bir xil.")
T([3700,2800,2854],[["Akslantirish","Standart-256","Standart-128"],["BaytZichlash, maks. |c|","0,25 (0-bit: 0,219)","1 (XOR)"],["Qo‘sh: 0-bit / 1-bit","1 / ≥ 0,99","1 / ≥ 0,99"],["Aralash: 0-qatlam / 1-bit","1 / o‘rtacha 0,53","1 / o‘rtacha 0,53"],["SurHolat, SurKalit","1","1"],["TuzilmaKalit (kₑ₀ = k₀)","1","1"]],"Akslantirishlar bo‘yicha eng yaxshi korrelyatsiyalar")
H2('1.3. Raund approksimatsiya tenglamasi va uning raundlar bo‘yicha o‘tishi')
P("Akslantirishlar tenglamalarini birlashtirib, yutish nuqtasi bo‘lmagan raund uchun 0-qatlam bo‘yicha raund tenglamasi hosil qilinadi: Qo‘sh juft/toqlikni saqlaydi, SurHolat pozitsiyalarni almashtiradi, Aralash M(k₀) bilan ko‘paytiradi, TuzilmaKalit holatga ta’sir qilmaydi:")
F("h₀⁽ʲ⁾ = P · M(k₀) · h₀⁽ʲ⁻¹⁾ = L · h₀⁽ʲ⁻¹⁾,     c = 1    (j = 1, …, 7, 10).")
P("Standart-128 da yutish nuqtasi ham chiziqli: Qo‘sh(holat, blok) juft/toqlikni saqlaydi, XOR esa blokning 0-qatlamini qo‘shadi. Shuning uchun 8- va 9-raund uchun ham tenglama o‘rinli: h₀⁽ʲ⁾ = L·h₀⁽ʲ⁻¹⁾ ⊕ blok₀. Standart-256 da esa 8- va 9-raunddagi yutishda yangi holatning 0-biti Z(holatn bayti) ning 0-biti bo‘ladi va tenglama 0,219 dan oshmaydigan korrelyatsiyali approksimatsiyaga aylanadi.")
P("Har bir akslantirishdan keyin tenglamaning bajarilishi A ilova kaliti va xabarida Standart-256 da kuzatildi (⟦izop⟧-jadval): kuzatish 0-nuqtadagi BaytZichlash natijasidan boshlanadi.")
rows=[["Akslantirish (1-raund)","Holat","0-qatlam","Mos bitlar"]]
for s in IZ['steps']: rows.append([opn[s['amal']],nl(s['holat']),nl(s['q0']),f"{s['mos']}/32"])
T([2200,3200,2300,1654],rows,"Standart-256, A ilova ma’lumotlari: 1-raund akslantirishlari bo‘yicha 0-qatlam tenglamasining bajarilishi",mono=(1,2),key='izop')
P("Har bir qadamda baytlar to‘liq o‘zgarsa ham (masalan, holat[0,0]: 44 → 27 → …), 0-qatlam nazariy bashorat bilan 32 bitning hammasida mos keladi. Raundlar bo‘yicha natija (A ilova kaliti uchun) va 1500 ta tasodifiy kalit bo‘yicha o‘lchangan korrelyatsiya ⟦raundc⟧-jadvalda keltirilgan.")
T([2600]+[675]*10,[["Raund j"]+[str(j) for j in range(1,11)],["A ilova: mos bitlar (256)"]+[str(v) for v in IZ['raund']],["c, Standart-256"]+[fz(v,2) for v in L2['lsb_pred_256_std']],["c, Standart-128"]+[fz(v,2) for v in L2['lsb_pred_16_std']]],"0-qatlam raund tenglamasining raundlar bo‘yicha korrelyatsiyasi",key='raundc')
IMG('ch1.png',15.5,6.9,"0-qatlam tenglamasining raundlar bo‘yicha korrelyatsiyasi (chapda) va Standart-256 da yutish qatlamlari bo‘yicha iz korrelyatsiyasi chegarasi (o‘ngda)")
P("Raundlar bo‘yicha eng yaxshi iz korrelyatsiyasining chegarasini (1-raund kirishidan boshlab) quyidagicha jamlash mumkin: 1–7-raundlarda iz bepul (c = 1), har bir yutish qatlami esa faol baytlar soniga qarab 2⁻²·ᵃ ko‘paytuvchi qo‘shadi (1.4-bo‘limdagi faol baytlar zanjiri bo‘yicha).")
rr=[["Raund (umumiy hisob)","1–7","8","9–10","11 (2-iter. 0-nuqta)","12–18","19 (8′)","20 (9′)"],
    ["O‘tilgan yutish qatlamlari","0","1","2","3","3","4","5"],
    ["Std-256, mediana kalit: log₂|c| ≤","0",str(-2*int(L3['1']['median'])),str(-2*int(L3['2']['median'])),str(-2*int(L3['3']['median'])),str(-2*int(L3['3']['median'])),str(-2*int(L3['4']['median'])),fz(-2*L3['5']['median'],0)],
    ["Std-256, eng yomon kalit: log₂|c| ≤","0","−2","−4","−6","−6","−8","−10"],
    ["Std-128: log₂|c|","0","0","0","0","0","0","0"]]
T([2800,800,750,800,1300,900,900,1104],rr,"Raundlar bo‘yicha iz korrelyatsiyasi chegarasi (1-raund kirishidan boshlab)")
P("Standart-256 da 1–7-raundlarda korrelyatsiya aniq 1, 8-raunddagi yutishdan keyin tasodifiy darajaga tushadi (A ilova kaliti uchun 8–10-raundlarda 25, 14, 10 bit mos keldi; ko‘p kalit bo‘yicha o‘rtacha c ≈ 0). Standart-128 da korrelyatsiya butun iteratsiya davomida, yutish nuqtalarini ham qo‘shgan holda, 1 ga teng; bu xossa keyingi iteratsiyalarda ham saqlanadi, demak xesh qiymatning 32 bitli 0-qatlami xabar bloklari 0-qatlamlarining affin funksiyasi.")
H2('1.4. Yutish qatlamlari, faol baytlar va iz korrelyatsiyasi')
P("1.3-bo‘limga ko‘ra Standart-256 da chiziqli bardoshlilikni faqat yutish nuqtalari ta’minlaydi. Iz korrelyatsiyasini baholash uchun iz qancha yutish qatlamidan va ularning har birida nechta faol bayt bilan o‘tishini aniqlash kerak. Qatlamlar ketma-ketligi: 1-iteratsiyaning 0-, 8-, 9-nuqtalari, so‘ng 2-iteratsiyaning 0-, 8-, 9-nuqtalari; ular orasidagi 0-qatlam akslantirishlari L⁸, L, L, L⁸, L. Iz oxirgi qatlamdagi niqobdan orqaga Lᵀ bilan tarqatiladi. Har bir faol bayt Z orqali o‘tganda korrelyatsiyani kamida 4 marta kamaytiradi (|c| ≤ 2⁻²).")
b1=L2['branch_L1']; b8=L2['branch_L8']
P(f"Avval ikki ketma-ket qatlamdagi faol baytlarning minimal yig‘indisi (chiziqli tarmoqlanish soni) hisoblandi: L uchun 2 ({b1['2']} ta kalitda) yoki 3 ({b1.get('3',0)} ta kalitda); L⁸ uchun minimum 2, mediana 7–8. So‘ngra 1 dan 6 tagacha qatlamdan o‘tuvchi izlar uchun minimal faol baytlar soni 120 ta kalitda qidirildi (⟦chain⟧-jadval).")
rows=[["Qatlamlar","Faol baytlar: min / mediana","log₂|c| (mediana kalit)","log₂|c| (eng yomon kalit)","Standart-128"]]
for k_ in range(1,7):
    v=L3[str(k_)]; rows.append([str(k_),f"{v['min']} / {fz(v['median'],1)}",f"≤ −{fz(2*v['median'],0)}",f"≤ −{2*v['min']}","0 (c = 1)"])
T([1500,2300,1900,2000,1654],rows,"Standart-256: yutish qatlamlari bo‘yicha faol baytlar va iz korrelyatsiyasi chegarasi",key='chain')
P("Mediana kalitlarda 2⁻⁶⁴ chegarasiga 5-qatlamda (−63) amalda, 6-qatlamda (−92) aniq erishiladi; bu 2-iteratsiyaning 8–9-raundlariga, ya’ni umumiy hisobda taxminan 18–19-raundga to‘g‘ri keladi. Eng yomon kalitlarda har bir qatlamda faqat bitta faol bayt qoladi va 2⁻⁶⁴ ga erishish uchun 32 ta qatlam (≈11 ta iteratsiya, ≈107 raund) kerak bo‘ladi. A ilova kaliti aynan shunday kalit: L ning [0,3] satrida faqat bitta birlik bor, ya’ni holat[0,3] ning 0-biti har raundda o‘zgarmay o‘tadi.")
P("A ilova kaliti uchun topilgan eng yaxshi izlar barcha qatlamlarda faqat holat[0,3] pozitsiyasidan o‘tadi: 1 qatlam — {[0,3]}, 2 qatlam — {[0,3]}; {[0,3]}, …, 6 qatlam — oltita qatlamning har birida {[0,3]}. Shu iz uchun approksimatsiya tenglamasi har bir yutish qatlamida Z ning 0-chiqish biti bo‘yicha eng yaxshi tenglamasi (c = 0,219) bilan, qatlamlar orasida esa h₀[0,3] ← h₀[0,3] tengligi bilan (c = 1) quriladi; 6 qatlam uchun |c| ≈ 0,219⁶ ≈ 2⁻¹³·².")
H2('1.5. Yutishdan keyingi raunddagi qoldiq munosabatlar')
P(f"10-raund oxirgi yutish nuqtasidan keyin bajariladi, shuning uchun xesh qiymatning 0-qatlami L matritsasining obrazi (aksi) ichida yotadi. 200 ta kalit bo‘yicha L ning o‘rtacha rangi {fz(L2['rank_L']['mean'],1)} (min {L2['rank_L']['min']}, max {L2['rank_L']['max']}); demak chiqishning 0-qatlamida o‘rtacha ≈{fz(32-L2['rank_L']['mean'],1)} ta chiziqli munosabat korrelyatsiya 1 bilan bajariladi. Kalitlarning {fz(100*L2['zero_rows']['share_keys_with_zero_row'],1)} foizida L da nol satrlar bor (o‘rtacha {fz(L2['zero_rows']['mean'],2)} ta) va ular xesh qiymatda doimiy nol bitlarni beradi. A ilova kaliti uchun rang 24, ya’ni 8 ta munosabat; ular 1000 ta tasodifiy xabarning barchasida bajarildi. Kalitsiz rejimda kalit ochiq bo‘lgani uchun bu munosabatlar bitta xesh qiymat bo‘yicha farqlovchini beradi.")
H2('1.6. Chiziqli kriptotahlil bo‘yicha xulosalar')
BL("Yutish nuqtasi bo‘lmagan raundlar (1–7, 10) 0-qatlamda c = 1, 1-bit qatlamda c ≥ 0,99 (Qo‘sh) bilan o‘tadi; bu raundlar chiziqli bardoshlilikka hissa qo‘shmaydi.")
BL("Standart-128 da yutish nuqtasidagi XOR ham chiziqli, shuning uchun xesh qiymatning 32 bitli 0-qatlami raundlar sonidan qat’i nazar c = 1 bilan kuzatiladi. Standart-128 chiziqli kriptotahlilga bardoshli emas.")
BL("Standart-256 da har bir faol bayt yutish nuqtasida ≤ 2⁻² hissa qo‘shadi. 2⁻⁶⁴ chegarasiga mediana kalitlarda 5–6 ta yutish qatlamidan keyin (≈18–19-raund, ya’ni kamida 2 ta iteratsiya, 3 blokli xabar) erishiladi; eng yomon kalitlarda amalda erishilmaydi.")
BL("Xesh qiymatning 0-qatlamida o‘rtacha ≈6 ta c = 1 munosabat (va kalitlarning yarmidan ko‘pida doimiy bitlar) mavjud; ular Aralash ning 2 moduli bo‘yicha degeneratsiyasidan kelib chiqadi va raundlar soniga bog‘liq emas.")

# ======================= 2. DIFFERENSIAL =======================
PB(); H1('2. Differensial kriptotahlil')
H2('2.1. Usulning mohiyati va bardoshlilik mezoni')
P("Differensial kriptotahlilda buzg‘unchi kirish ayirmasi (orttirmasi) Δx = x ⊕ x′ ning akslantirishlar orqali ma’lum chiqish ayirmasiga Δy o‘tish ehtimolligidan foydalanadi. F akslantirish uchun ayirmalar matritsasi (DDT) elementlari va o‘tish ehtimolligi:")
F("DDT_F(Δx, Δy) = #{ x : F(x) ⊕ F(x ⊕ Δx) = Δy },     p(Δx → Δy) = DDT_F(Δx, Δy) / 2ⁿ.")
P("Iz ehtimolligi oraliq ehtimolliklar ko‘paytmasiga teng. Xesh funksiyaning kolliziyaga bardoshliligi uchun iz ehtimolligi 256 bitli rejimda 2⁻¹²⁸ dan, 128 bitli rejimda 2⁻⁶⁴ dan kichik bo‘lishi talab qilinadi. Algoritmda 2ⁿ moduli bo‘yicha amallar ishlatilgani uchun eng katta bit (MSB) ayirmasi alohida ahamiyatga ega: x + 2ⁿ⁻¹ ≡ x ⊕ 2ⁿ⁻¹ (mod 2ⁿ), ya’ni MSB ayirmasi qo‘shish va ko‘paytirishda ko‘chirish hosil qilmaydi.")
H2('2.2. Akslantirishlarning ayirmalar matritsalari')
H3('2.2.1. BaytZichlash: Z jadvali (Standart-256)')
dd=D1['Z_ddt_dist']
P(f"Z ning 256×16 ayirmalar matritsasi to‘liq hisoblandi. Maksimal qiymat {D1['Z_ddt_max']}/256 = 0,156 bo‘lib, u Δx = 96 → Δy = 0 da erishiladi, ya’ni ayirma butunlay so‘nadi. 255 ta noldan farqli ayirmaning {D1['Z_vanish_count']} tasi musbat ehtimollik bilan so‘nishi mumkin. Z lotin kvadrati (har bir satr va ustun 0…15 ning o‘rin almashtirishi) bo‘lgani uchun faqat bitta yarim baytdagi ayirma hech qachon so‘nmaydi: DDT(80, 0) = DDT(01, 0) = 0. ⟦zddt⟧-jadvalda tipik satrlar keltirilgan.")
T([1100]+[515]*16,[["Δx \\ Δy"]+[f"{y:X}" for y in range(16)],["80"]+[str(v) for v in D1['Z_row_80']],["01"]+[str(v) for v in D1['Z_row_01']],["96"]+[str(v) for v in D1['Z_row_96']]],"Z ayirmalar matritsasining satrlari (×1/256)",key='zddt')
T([1100]+[515]*16,[["Δx \\ Δy"]+[f"{y:X}" for y in range(16)]]+[[f"{d:02X}"]+[str(v) for v in XE[f'Z_ddt_{d:02x}']] for d in (0x08,0x10,0x88,0x0f,0xf0,0x11)],"Z ayirmalar matritsasining qo‘shimcha satrlari")
T([2900]+[600]*10,[["DDT qiymati","0","2","4–8","10–14","16–20","22–26","28–32","34–36","38","40"],["Elementlar soni"]+[str(sum(dd.get(str(v),0) for v in rng_)) for rng_ in ([0],[2],[4,6,8],[10,12,14],[16,18,20],[22,24,26],[28,30,32],[34,36],[38],[40])]],"Z ayirmalar matritsasi elementlarining taqsimoti (Δx ≠ 0)")
P("Taqsimotdan ko‘rinadiki, Z da ehtimolligi 0,1 dan katta (DDT ≥ 26) o‘tishlar ko‘p: ular buzg‘unchiga yutish nuqtasidan yuqori ehtimollik bilan o‘tadigan izlar qurish imkonini beradi. Tasodifiy 8 → 4 jadval medianasi 38 bo‘lgani uchun Z tasodifiy jadvaldan yaxshi emas; optimal 8 → 8 S-box larda maksimal qiymat 4.")
P("BaytZichlash da ayirmalar quyidagicha o‘tadi: holat baytidagi ayirma faqat yuqori yarim baytga (Z(h)), holatn baytidagi ayirma faqat quyi yarim baytga (Z(n)) tushadi. Holat va xabar ayirmalari bir-biriga aralashmaydi va bir-birini kompensatsiya qila olmaydi.")
H3('2.2.2. BaytZichlash: XOR (Standart-128)')
P("XOR uchun Δy = Δh ⊕ Δn ehtimollik 1 bilan bajariladi. Agar Δh = Δn bo‘lsa, ayirma ehtimollik 1 bilan so‘nadi: holatdagi farqni xabar blokidagi xuddi shunday farq bilan to‘liq «o‘chirish» mumkin.")
H3('2.2.3. Qo‘sh o‘zgartirishi')
pj=D1['Qosh_pj_best_mean']
P(f"Qo‘sh elementining (parametrlar belgilangan) ayirmalar matritsasida maksimal qiymat {D1['Qosh_ddt_max_max']}/256 bo‘lib, u 80 → 80 o‘tishda erishiladi. Haqiqatan, toq y uchun (y + 2ⁿ⁻¹)⁻¹ ≡ y⁻¹ + 2ⁿ⁻¹ (mod 2ⁿ), R juft bo‘lgani uchun R·2ⁿ⁻¹ ≡ 0, shuning uchun MSB ayirmasi har bir bosqichdan o‘zgarmay o‘tadi; faqat x⁻² ≡ 0 almashtirish nuqtasi istisno. ⟦qoshddt⟧-jadvalda 2ʲ ko‘rinishidagi kirish ayirmalari uchun eng ehtimolli chiqish ayirmasining ehtimolligi keltirilgan.")
T([3100]+[780]*8,[["Kirish ayirmasi Δx = 2ʲ, j","0","1","2","3","4","5","6","7"],["Eng ehtimolli Δy ehtimolligi"]+[fz(v,3) for v in pj]],"Qo‘sh elementining ayirmalar o‘tkazish ehtimolliklari (200 ta parametrlar to‘plami)",key='qoshddt')
P("T-funksiya xossasi tufayli j-bitdagi ayirma faqat j va undan yuqori bitlarga ta’sir qiladi; quyi bitdagi ayirma esa ko‘chirishlar orqali barcha yuqori bitlarga tarqaladi (Δx = 01 uchun eng ehtimolli chiqish atigi 0,12 ehtimollik bilan). Massiv darajasida bitta elementdagi MSB ayirmasi J yig‘indisini 2ⁿ⁻¹ ga o‘zgartiradi, bu ikkinchi massivning barcha A parametrlarini siljitadi va uning toq elementlarida MSB ayirmasini paydo qiladi; juft sondagi MSB ayirmalari esa yig‘indini o‘zgartirmaydi. 128 bitli rejimda Δ = 10 tuzatmasi va nol almashtirish shartlari mod 16 da tez-tez ishlaydi va ayirmalarni MSB dan quyi bitlarga ham o‘tkazadi.")
H3('2.2.4. Aralash, SurHolat, SurKalit, TuzilmaKalit')
P(f"Aralash belgilangan kₑ uchun Z/2ⁿ ustida chiziqli, shuning uchun modul ayirmalari uchun aniq chiziqli: Δh′ = Aralash(Δh, kₑ). MSB ayirmasi uchun 2ⁿ⁻¹·kₑ ≡ 2ⁿ⁻¹·(kₑ mod 2), ya’ni MSB ayirmalari 0-qatlamdagi bilan bir xil M(k₀) matritsasi orqali ehtimollik 1 bilan tarqaladi: Δh′_MSB = M(k₀)·Δh_MSB. Agar ayirma M(k₀) ning yadrosida bo‘lsa, u ehtimollik 1 bilan so‘nadi; tasodifiy kalitlarning {fz(100*A3['keys_zero_col'],0)} foizida M da nol ustun, {fz(100*A3['keys_equal_cols'],0)} foizida teng ustunlar juftligi bor. SurHolat va SurKalit ayirmani pozitsiyalar bo‘yicha ko‘chiradi (ehtimollik 1), TuzilmaKalit faqat kₑ ga ta’sir qiladi va undagi MSB ayirmasini o‘zgartirmaydi.")
H2('2.3. Orttirmalarning akslantirishlar va raundlar orqali o‘tishi')
P("Ayirmalarning o‘tishi haqiqiy algoritmda kuzatildi. Birinchi tajribada (D0) 0-nuqtadagi yutishdan keyingi holatning bitta baytiga MSB ayirmasi kiritildi va har bir akslantirishdan keyin holat va kₑ dagi faol elementlar soni hamda MSB izining saqlanish ehtimolligi (barcha ayirmalar faqat MSB da) o‘lchandi (har bir rejimda 3000 juftlik). ⟦d0op⟧-jadvalda 1- va 2-raund akslantirishlari bo‘yicha natijalar keltirilgan.")
def opsRow(key,j,lab):
    rs=[r for r in D3[key] if r['j']==j]
    return [lab]+[f"{fz(r['act'],1)} / {fz(r['actk'],1)}; {fz(r['msb'],2)}" for r in rs]
rr=[["Rejim, raund","Aralash","Qo‘sh(holat, kₑ)","SurHolat, SurKalit","Qo‘sh(holat, kₑ)","TuzilmaKalit"]]
for key,lab in [('256_std_D0a','Standart-256'),('16_std_D0a','Standart-128')]:
    for j in (1,2): rr.append(opsRow(key,j,f"{lab}, j = {j}"))
T([1750,1520,1520,1520,1520,1520],rr,"Akslantirishlardan keyingi faol elementlar (holat / kₑ) va MSB izining saqlanish ehtimolligi",key='d0op')
rr=[["Raund, akslantirish","Δholat","Faol (holat / kₑ)","Faqat MSB"]]
for r in XE['juft']:
    if r['raund']<=3 and r['amal'] in ('Aralash','Qosh1','Qosh2'): rr.append([f"{r['raund']}: {opn[r['amal']]}",nl(r['d']),f"{r['faol']} / {r['faol_ke']}","ha" if r['msb'] else "yo‘q"])
T([2700,3300,1800,1554],rr,"Standart-256, A ilova ma’lumotlari: holat[0,0] dagi MSB ayirmasining 1–3-raundlarda o‘tishi",mono=(1,))
P("A ilova misolida MSB izi 1- va 2-raundlarda saqlanadi (2 va 4 ta faol bayt), 3-raundda Aralash ayirmani 13 baytga tarqatadi, keyingi Qo‘sh da J yig‘indisi juftligi o‘zgarib, ayirma kₑ ga o‘tadi va quyi bitlarga tarqaladi (32 ta faol bayt).")
P("Aralash bitta MSB ayirmasini M(k₀) ustunidagi birlar soniga teng (o‘rtacha 3 ta) baytga ehtimollik 1 bilan tarqatadi. Birinchi Qo‘sh(holat, kₑ) toq sondagi faol elementlar J yig‘indisini o‘zgartirgani uchun ayirmani kₑ massiviga ham o‘tkazadi; ikkinchi Qo‘sh da ayirmalarning bir qismi juft sonli bo‘lib qoladi. SurHolat, SurKalit va TuzilmaKalit faol elementlar sonini o‘zgartirmaydi. 128 bitli rejimda iz birinchi raunddayoq yarmidan ko‘p hollarda buziladi (0,47). Raundlar bo‘yicha natija ⟦d0r⟧-jadvalda keltirilgan.")
def r0(key,f): return [ (fz(r[f],3) if f=='msb' else fz(r[f],1)) for r in D3[key] if r['op']=='Tuz']
T([2850]+[650]*10,[["Raund j"]+[str(j) for j in range(1,11)],["Standart-256: P(MSB izi)"]+r0('256_std_D0a','msb'),["Standart-256: faol baytlar"]+r0('256_std_D0a','act'),["Standart-128: P(MSB izi)"]+r0('16_std_D0a','msb'),["Standart-128: faol el."]+r0('16_std_D0a','act')],"Bitta MSB ayirmasining raundlar orqali o‘tishi (8- va 9-raundlarda yutish)",key='d0r')
IMG('ch2.png',15.5,6.9,"MSB izining saqlanish ehtimolligi va faol elementlar soni (Standart-256 va Standart-128)")
P("Standart-256 da MSB izi har raundda ≈0,85–0,94 ehtimollik bilan saqlanadi, 7 raunddan keyingi umumiy ehtimollik ≈0,34 ≈ 2⁻¹·⁶. 8-raunddagi yutishda iz buziladi; qolgan ≈3,3% juftliklarda ayirma 1-raundning Aralash o‘zgartirishida butunlay so‘ngan (ichki kolliziya). Standart-128 da iz tezroq buziladi, lekin ≈3,6% juftlikda ayirma xuddi shu tarzda butunlay yo‘qoladi va keyingi barcha raundlarda nol bo‘lib qoladi.")
H3('2.3.1. Kirish blokidagi ayirmalar')
P("Ikkinchi tajribada (D2) kirish blokining ikkita elementiga MSB ayirmasi kiritildi — bu J yig‘indisini o‘zgartirmaydi va kolliziya hujumlari uchun eng qulay boshlang‘ich ayirma hisoblanadi. Uchinchi tajribada (D1) ayirma iteratsiya boshidagi holatga kiritildi (oldingi blokni qayta ishlashdan qolgan farqqa mos keladi). Natijalar ⟦d2⟧-jadvalda (2000 juftlik).")
def d2(key,op,j=None):
    for r in D2[key]:
        if r['op']==op and (j is None or r['j']==j): return r
rr=[["Tajriba, rejim","Qo‘sh(0): faol / p","Yutish(0): faol / p","1-raund","2-raund","7-raund","8-nuqta","9-nuqta","10-raund: Xemming"]]
for case in ('D2','D1'):
    for key,lab in [('256_std','Std-256'),('16_std','Std-128')]:
        k_=f'{key}_{case}'; q=d2(k_,'Qosh0'); b=d2(k_,'BZ0')
        rr.append([f"{case}, {lab}",f"{fz(q['act'],1)} / {fz(q['top'],2)}",f"{fz(b['act'],1)} / {fz(b['top'],3)}",fz(d2(k_,'Tuz',1)['act'],1),fz(d2(k_,'Tuz',2)['act'],1),fz(d2(k_,'Tuz',7)['act'],1),fz(d2(k_,'BZ8')['act'],1),fz(d2(k_,'BZ9')['act'],1),fz(d2(k_,'Tuz',10)['hd'],1)])
T([1350,1150,1200,800,800,800,850,850,1550],rr,"Kirish bloki va holatdagi ayirmalarning tarqalishi (faol elementlar, eng ehtimolli ayirma ehtimolligi p, Xemming masofasi)",key='d2')
rr=[["Rejim","Aralash","Qo‘sh(holat, kₑ)","SurHolat, SurKalit","Qo‘sh(holat, kₑ)","TuzilmaKalit"]]
for key,lab in [('256_std_D2','Std-256'),('16_std_D2','Std-128')]:
    rs=[r for r in D2[key] if r['j']==1]
    rr.append([lab]+[f"{fz(r['act'],1)}; HD {fz(r['hd'],0)}" for r in rs])
T([1750,1520,1520,1520,1520,1524],rr,"D2 tajribasi: 1-raund akslantirishlaridan keyingi faol elementlar va Xemming masofasi")
P("D2 tajribasida Qo‘sh(0-nuqta) ayirmani ehtimollik 1 bilan holatga ta’sir qilmasdan o‘tkazadi va u yutish nuqtasiga holatn ning ikki elementidagi MSB ayirmasi sifatida yetib keladi. Standart-128 da XOR uni deyarli o‘zgarishsiz holatga kiritadi (p ≈ 0,79). Standart-256 da Z ikkala baytda quyi yarim bayt ayirmasini beradi (o‘lchangan p ≈ 0,0135, nazariy (26/256)² ≈ 2⁻⁶·⁶). Bir raunddan keyin ikkala rejimda ayirma deyarli butun holatga tarqaladi. Standart-128 da 10-raunddan keyingi Xemming masofasi (≈47 bit) ideal 64 bitdan sezilarli kichik: bu 0-qatlam ayirmasi chiziqli qoidaga bo‘ysunishining natijasi.")
H2('2.4. Optimal orttirmalar')
P("Buzg‘unchi uchun eng foydali (optimal) izlar quyidagi bo‘g‘inlardan quriladi:")
BL("*Yutishsiz raundlardagi MSB izlari.* 1–7-raundlarda MSB ayirmalari M(k₀) orqali chiziqli tarqaladi va har raundda ≈0,85–0,94 ehtimollik bilan saqlanadi (Standart-256). Bu bo‘g‘inlar 7 raund davomida iz ehtimolligini atigi ≈2⁻¹·⁶ ga kamaytiradi.")
BL("*Z da so‘nish.* Ikkala yarim baytda farq qiladigan ayirma (optimali 96) Z da 40/256 = 2⁻²·⁶⁸ ehtimollik bilan so‘nadi; tasodifiy ayirma uchun o‘rtacha so‘nish ehtimolligi 1/16 = 2⁻⁴. Holat baytidagi ayirma Δn = 0 bo‘lganda ham Z(h) da so‘nishi mumkin, ya’ni holatdagi farqni yutish nuqtasida yo‘qotish mumkin.")
BL("*XOR da kompensatsiya (Standart-128).* Holatdagi ayirma Δh ni xabar blokidagi Δn = Δh bilan ehtimollik 1 bilan so‘ndirish mumkin.")
BL("*Aralash yadrosi.* Agar yutishdan keyingi ayirma M(k₀) ning yadrosidagi MSB ayirmasi bo‘lsa, u keyingi Aralash da ehtimollik 1 bilan so‘nadi. Tajribada bitta tasodifiy pozitsiyadagi MSB ayirmasi 3,1% (p = 256) va 3,3% (p = 16) hollarda 1-raunddayoq butunlay yo‘qoldi.")
P("*Kolliziya izining tuzilishi.* Bitta blokdagi ayirma o‘sha blok uchun uch marta (0-, 8- va 9-nuqtalarda) holatga kiritiladi. Kolliziya uchun 1–7-raundlardan keyin holatdagi ayirma shunday bo‘lishi kerakki, u 8- va 9-nuqtalardagi blok ayirmasi bilan birgalikda so‘nsin, so‘ng uzunlik va NY bloklari ham bir xil bo‘lsin. Standart-256 da holat ayirmasi Z(h) da Δn ga bog‘liq bo‘lmagan holda 0,156 gacha (tasodifiy ayirma uchun o‘rtacha 2⁻⁴) ehtimollik bilan so‘nishi mumkin: 32 bayt uchun 2⁻¹²⁸ tartibida, ya’ni umumiy hujum darajasida. Standart-128 da esa XOR kompensatsiyasi va 0-qatlamning chiziqliligi bu qadamlarni ancha osonlashtiradi.")
P("Standart-128 uchun qo‘shimcha ravishda T-funksiya xossasi tekshirildi: bir blokli xabarda faqat yuqori (3-) bit-qatlamdagi w ta bit o‘zgartirilib, chiqishning quyi qatlamlari kuzatildi (⟦tfunc⟧-jadval, 2000 juftlik).")
tf=I['tfunksiya_128']
T([2800]+[1310]*5,[["O‘zgartirilgan bitlar soni w","1","2","4","8","32"],["0-qatlam saqlandi"]+[fz(tf[w]['0_qatlam_saqlandi'],3) for w in ('1','2','4','8','32')],["0–2-qatlamlar to‘liq saqlandi"]+[fz(tf[w]['quyi_3_qatlam_saqlandi'],4) for w in ('1','2','4','8','32')],["Yarim baytlarning quyi 3 biti saqlandi (ulush)"]+[fz(tf[w]['quyi_qatlam_bitlari_saqlandi'],3) for w in ('1','2','4','8','32')]],"Standart-128: yuqori bit-qatlam o‘zgarganda chiqish quyi qatlamlarining saqlanishi",key='tfunc')
P("0-qatlam har doim saqlanadi (ehtimollik 1), lekin 1- va 2-qatlamlar amalda tasodifiy o‘zgaradi (yarim baytning quyi 3 biti saqlanish ulushi ≈0,26, bu 0-bit doim saqlanganda tasodifiy holat uchun kutilgan 0,25 ga yaqin). Sababi: Qo‘sh dagi Δ = 10 = 1010₂ tuzatmasi va boshqa tenglik shartlari yuqori bitlarga bog‘liq bo‘lib, quyi bitlarga juft (0-bitni o‘zgartirmaydigan) qiymatlar qo‘shadi. Demak, Standart-128 da faqat 0-qatlam T-funksiya kabi ajralgan; bu 2⁴⁸ murakkablikdagi kolliziya hujumiga asos bo‘ladi (96 bitlik qism uchun tug‘ilgan kunlar paradoksi).")
H2('2.5. Bardoshlilik bahosi')
P("Iz ehtimolligining yuqori chegarasi har bir faol bayt uchun eng yaxshi ehtimollikni olish orqali baholandi. 1–7-raundlardan keyin MSB izi ham holatning 25–27 ta baytiga tarqalgan bo‘ladi, shuning uchun 8-raunddagi yutishda faol baytlar soni amalda 27–32 ni tashkil qiladi.")
T([1900,1800,2000,2000,1654],[["Rejim","Faol bayt boshiga maks. p","8-nuqtadan keyin (≈27 bayt)","8- va 9-nuqtalardan keyin (≈27 + 31)","Talab"],["Standart-256","2⁻²·⁶⁸","≤ 2⁻⁷²","≤ 2⁻¹⁵⁶","2⁻¹²⁸"],["Standart-128","1 (XOR)","≈ 1","≈ 1","2⁻⁶⁴"]],"Birinchi iteratsiyadagi differensial iz ehtimolligining yuqori chegaralari")
P("Standart-256 da 8-raunddagi birinchi «ichki» yutishdan keyin chegara (2⁻⁷²) hali talabdan katta, 9-raunddagi yutishdan keyin esa 2⁻¹⁵⁶ — talabdan kichik. Standart-128 da yutish qatlami ayirmani jazolamaydi, bardoshlilik faqat yutishsiz raundlarga tayanadi, ular esa MSB izlariga kuchsiz qarshilik ko‘rsatadi va 0-qatlam ayirmasini umuman o‘zgartirmaydi.")
H2('2.6. Differensial kriptotahlil bo‘yicha xulosalar')
BL("Yutishsiz raundlar (1–7, 10) MSB izlarini ≈0,85–0,94 ehtimollik bilan o‘tkazadi; differensial bardoshlilik faqat yutish nuqtalarida hosil bo‘ladi.")
BL("Standart-256 da Z ning maksimal o‘tish ehtimolligi 0,156 (96 → 0), holatdagi ayirma Z(h) da so‘nishi mumkin; differensial chegaraga (2⁻¹²⁸) birinchi iteratsiyaning 9-raundidan keyin erishiladi.")
BL("Standart-128 da XOR ayirmani o‘zgarishsiz o‘tkazadi va xabar ayirmasi bilan kompensatsiya qilinadi; 0-qatlam ayirmasi butun xesh davomida chiziqli. Standart-128 raundlar sonidan qat’i nazar differensial kriptotahlilga bardoshli emas.")
BL("Aralash yadrosi orqali ayirmaning ehtimollik 1 bilan so‘nishi (≈3% juftliklar) ikkala rejimda ichki kolliziyalarni keltirib chiqaradi.")

# ======================= 3. ALGEBRAIK =======================
PB(); H1('3. Algebraik kriptotahlil')
H2('3.1. Usulning mohiyati va bardoshlilik mezoni')
P("Algebraik kriptotahlilda algoritm noma’lum bitlar (kalit yoki xabar) ga nisbatan GF(2) maydoni yoki Z/2ⁿ halqasi ustidagi tenglamalar tizimi ko‘rinishida yoziladi va tizim yechiladi. Murakkablik tenglamalar darajasi, o‘zgaruvchilar soni va tizim tuzilishiga bog‘liq. Linearizatsiya usulida d-darajali tizimdagi har bir monom yangi o‘zgaruvchi deb olinadi; murakkablik taxminan:")
F("C(n, d) ≈ ( Σ_{i=0..d} binom(n, i) )^ω,     ω ≈ 2,8,")
P("bu yerda n — noma’lum bitlar soni. 128 bitli rejim uchun (n = 128) 2⁶⁴ dan oshish uchun d ≥ 4, 256 bitli rejim uchun (n = 256) 2¹²⁸ dan oshish uchun d ≥ 8 talab qilinadi. Har bir akslantirish uchun oshkor (y = f(x)) va implitsit (g(x, y) = 0) tenglamalar ko‘riladi; implitsit tenglamalar soni monomlar matritsasining rangi orqali aniq hisoblandi.")
H2('3.2. Akslantirishlar uchun algebraik tenglamalar')
H3('3.2.1. BaytZichlash')
P(f"Z jadvali (8 → 4) uchun 12 ta o‘zgaruvchiga nisbatan kvadrat implitsit tenglamalar yo‘q ({A1['Z_quad'][0]} / {A1['Z_quad'][1]} monom), kub darajali implitsit tenglamalar {A1['Z_cubic'][0]} ta ({A1['Z_cubic'][1]} ta monomdan). Har bir chiqish bitining oshkor ANF darajasi {A1['Z_deg'][0]}. Standart-256 dagi butun BaytZichlash (16 → 8) uchun ham kvadrat implitsit tenglamalar yo‘q, chiqish bitlari darajasi 6. Har bir bayt uchun tenglamalar:")
F("y_hi = Z(h),   y_lo = Z(n),     har bir Z uchun 4 ta oshkor 6-darajali yoki 43 ta kub implitsit tenglama.")
rr=[["Z chiqish biti","Monomlar soni"]+[f"d = {d}" for d in range(7)]]
for j,a in enumerate(XE['Z_anf']): rr.append([f"z{j}",str(a['monomlar'])]+[str(v) for v in a['daraja_boyicha'][:7]])
T([1700,1700]+[850]*7,rr,"Z jadvali oshkor tenglamalarining (ANF) tarkibi: darajalar bo‘yicha monomlar soni")
P("Har bir Z bitining ANF ida 97–120 ta monom bor, ularning ko‘pchiligi 3–5-darajali. Oshkor tenglamalar zich va yuqori darajali bo‘lgani uchun algebraik tizimda implitsit kub tenglamalar (43 ta) qulayroq.")
P("Standart-128 dagi XOR uchun yᵢ = hᵢ ⊕ nᵢ chiziqli tenglamalari (daraja 1) o‘rinli; ular yangi o‘zgaruvchi talab qilmaydi.")
H3('3.2.2. Qo‘sh')
P("Z/2ⁿ halqasi ustida Qo‘sh ning har bir bosqichi (t = 1, 2, 3) bitta element uchun quyidagicha yoziladi (x⁽⁰⁾ = x):")
F("x⁽ᵗ⁾ · (B_t + R · x⁽ᵗ⁻¹⁾) + A_t · x⁽ᵗ⁻¹⁾ ≡ 0 (mod 2ⁿ),")
F("A₁ = J₁′ + 2·x′ + Δ,   B₁ = K₁ − 2·x,   J₁ = Σ x,   K₁ = Π (x | 1) + Δ′,")
P("bu yerda shtrixli kattaliklar ikkinchi massivga tegishli, (x | 1) — elementning 0-bitini 1 ga tenglashtirish, Δ va Δ′ — J juftligi va K ning ±(J′ + 1) bilan tengligiga bog‘liq tuzatmalar. 2- va 3-bosqichlarda A₂ = J₁′ + J₂′ + 2·x′⁽¹⁾ + Δ, B₂ = K₁·K₂ − 2·x⁽¹⁾. A ilova ma’lumotlarida holat[0,0] uchun bu tenglamalar tekshirildi: J₁h = 72, J₁hn = 42, K₁h = 1, A₁ = 123, B₁ = 51, uchala bosqichda chap tomon aynan 0 ga teng.")
qd=EX['Qosh_deg_median']
P(f"Bitta element (parametrlar belgilangan) algebraik jihatdan juda zaif: 16 ta o‘zgaruvchiga nisbatan {A1['Qosh_quad'][0]} ta kvadrat implitsit tenglama mavjud (taqqoslash uchun AES S-box da 39 ta). Chiqish bitlarining ANF darajalari (mediana) j = 0…7 uchun: {', '.join(str(int(v)) for v in qd)}; 0-bit chiziqli, j ≥ 2 bitlar uchun daraja j ga yaqin (T-funksiya). 1-bit darajasining 8 ga yetishi nolni almashtirish nuqtasi bilan bog‘liq: bu qoida bitta kirishda ishlaydi va ANF ga to‘liq darajali «nuqtali» had qo‘shadi.")
H3('3.2.3. Aralash, SurHolat, SurKalit, TuzilmaKalit')
F("h′[u,u] = h[u,u]·Σᵢ kₑ[i,u] − Σ_{i≠u} h[i,i]·kₑ[i,u],")
F("h′[s,u] = h[s,u]·Σᵢ kₑ[i,u] + kₑ[s,u]·Σᵢ h[i,u] − Σ_{i≠s,u} h[s,i]·kₑ[i,u]   (s ≠ u).")
P("Aralash uchun har bir chiqish elementiga bitta bichiziqli tenglama yoziladi; ma’lum kₑ da u h ga nisbatan chiziqli, kalit noma’lum bo‘lganda (h, kₑ) ga nisbatan kvadrat. Bit darajasida j-bitning darajasi j + 1 dan oshmaydi, 0-qatlam chiziqli. SurHolat va SurKalit — o‘zgaruvchilarni qayta nomlash. TuzilmaKalit uchun: kₑ ≠ 0 bo‘lganda kₑ′ = kₑ − (kₑ₀ ⊕ k₀) (mod 2ⁿ), kₑ = 0 va k₀ = 0 bo‘lganda kₑ′ = 2.")
T([3200,3077,3077],[["Akslantirish","0-qatlam darajasi","j-bit darajasi (kirish bitlariga nisbatan)"],["Aralash (kₑ ma’lum)","1","≤ j + 1 (ko‘chirishlar)"],["Aralash (kₑ noma’lum)","2 (h·kₑ)","≤ 2(j + 1)"],["Qo‘sh","1","≈ j (mediana); nuqtali istisno — 8"],["SurHolat, SurKalit","1","1"],["TuzilmaKalit","1 (kₑ₀ = k₀)","≤ j + 1"],["BaytZichlash (Std-256)","6","6"],["BaytZichlash (Std-128)","1","1"]],"Akslantirishlar bo‘yicha algebraik darajalar (bit darajasi)")
H3('3.2.4. Bit darajasidagi tenglamalar soni')
P("Hisoblash modeli: n bitli modul qo‘shish — 2n − 1 o‘zgaruvchi va tenglama (n − 1 tasi ko‘chirish uchun kvadrat); n bitli modul ko‘paytirish — n(n+1)/2 qisman ko‘paytma va n − 1 ta qo‘shish (n = 8 da 141 o‘zgaruvchi, 85 kvadrat tenglama); modul bo‘yicha teskarilash y·d = 1 ko‘paytirish tenglamasi bilan.")
E=A3['eq']; es=E['256_std']; e1=E['128_std']
rr=[["Akslantirish","256: o‘zg. / tengl. / nochiziqli","128: o‘zg. / tengl. / nochiziqli"]]
for lab,k_ in [("Qo‘sh (ikki massiv, 3 bosqich)",'qosh'),("Aralash",'aralash'),("TuzilmaKalit",'tuzilma'),("BaytZichlash",'bz'),("Raund (yutishsiz)",'raund')]:
    rr.append([lab," / ".join(sp(v) for v in es[k_])," / ".join(sp(v) for v in e1[k_])])
T([3200,3077,3077],rr,"Standart algoritm akslantirishlari uchun bit darajasidagi tenglamalar soni (baho)")
P("Raund tizimining 91 foizdan ortig‘i Qo‘sh o‘zgartirishiga to‘g‘ri keladi; BaytZichlash 256 bitli rejimda 256 ta o‘zgaruvchi va 2752 ta kub tenglama, 128 bitli rejimda faqat 128 ta chiziqli tenglama qo‘shadi.")
H2('3.3. Raund tenglamalari va 2–3 raund uchun tizimlar')
P("j-raund kirishidagi (h⁽ʲ⁻¹⁾, kₑ⁽ʲ⁻¹⁾) va chiqishidagi (h⁽ʲ⁾, kₑ⁽ʲ⁾) massivlari orqali raund tenglamalari akslantirishlar tenglamalarini ketma-ket birlashtirish bilan yoziladi:")
F("a = Aralash(h⁽ʲ⁻¹⁾, kₑ⁽ʲ⁻¹⁾);   (b, c) = Qo‘sh(a, kₑ⁽ʲ⁻¹⁾);   b′ = P·b,  c′ = Q·c;")
F("(h⁽ʲ⁾, d) = Qo‘sh(b′, c′);   kₑ⁽ʲ⁾ = TuzilmaKalit(d, k),")
P("P va Q — SurHolat va SurKalit o‘rin almashtirishlari. 8- va 9-raundlarda yutish tenglamalari qo‘shiladi: (h̃, ñ) = Qo‘sh(h, blok), h = BaytZichlash(h̃, ñ). 2 va 3 raund uchun tizimlar raund tenglamalarini h⁽ʲ⁾ va kₑ⁽ʲ⁾ umumiy o‘zgaruvchilari orqali zanjirlash bilan olinadi (⟦eqsys⟧-jadval; «1 raund» — 0-nuqtadagi yutish va bitta raund).")
rr=[["Rejim","1 raund: o‘zg. / tengl.","2 raund: o‘zg. / tengl.","3 raund: o‘zg. / tengl."]]
for key,lab in [('256_std','Standart-256'),('128_std','Standart-128')]: rr.append([lab]+[f"{sp(E[key][r][0])} / {sp(E[key][r][1])}" for r in ('r1','r2','r3')])
T([2050,2450,2450,2400],rr,"1, 2 va 3 raund uchun bit darajasidagi tenglamalar tizimlari hajmi",key='eqsys')
rr=[["Tizim qismi (Standart-256, 2 raund)","O‘zgaruvchilar","Tenglamalar"]]
rr.append(["0-nuqta: Qo‘sh(holat, blok)",sp(es['qosh'][0]),sp(es['qosh'][1])]); rr.append(["0-nuqta: BaytZichlash",sp(es['bz'][0]),sp(es['bz'][1])])
for j in (1,2):
    rr.append([f"{j}-raund: Aralash",sp(es['aralash'][0]),sp(es['aralash'][1])]); rr.append([f"{j}-raund: 2 × Qo‘sh",sp(2*es['qosh'][0]),sp(2*es['qosh'][1])]); rr.append([f"{j}-raund: TuzilmaKalit",sp(es['tuzilma'][0]),sp(es['tuzilma'][1])])
rr.append(["Jami",sp(es['r2'][0]),sp(es['r2'][1])])
T([4554,2400,2400],rr,"Standart-256 uchun 2 raundli tenglamalar tizimining tarkibi")
P("Tizim hajmi katta bo‘lsa ham, uning tuzilishi buzg‘unchi uchun qulay: 0-qatlam tenglamalari barcha yutishsiz raundlarda chiziqli. Standart-128 da 0-nuqtadagi va 8-, 9-nuqtalardagi yutish ham chiziqli bo‘lgani uchun 0-qatlam tenglamalari istalgan sondagi raundlar uchun h₀⁽ʲ⁾ = L·h₀⁽ʲ⁻¹⁾ ⊕ blok₀ ko‘rinishidagi chiziqli tizimni tashkil qiladi. Standart-256 da esa har bir yutishda 0-qatlam Z orqali 6-darajali bog‘lanishga ega bo‘ladi.")
H2('3.4. Raundlar bo‘yicha algebraik darajaning o‘sishi')
P("Daraja o‘sishi kub testlari bilan tekshirildi: xabarning dastlabki 16 bitidan tasodifiy d ta bit tanlanadi, qolganlari belgilanadi va 2ᵈ ta qiymat bo‘yicha r raunddan keyingi holat bitlarining XOR yig‘indisi hisoblanadi. Agar bitning darajasi d dan kichik bo‘lsa, yig‘indi doim nol. 4 ta tasodifiy kub uchun yig‘indisi doim nol bo‘lgan bitlar ulushi o‘lchandi (yuqori darajali funksiya uchun kutilgan qiymat 1/16 ≈ 0,06).")
def cr(key,lay=None):
    row=A2[key]; return [fz((row[str(d)][1][lay] if lay is not None else row[str(d)][0]),2) for d in (2,4,6,8,10,12)]
rr=[["Rejim, raund r","d = 2","d = 4","d = 6","d = 8","d = 10","d = 12"]]
for r in (0,1,2,3): rr.append([f"Standart-256, r = {r}"]+cr(f'256_std_r{r}'))
for r in (0,1,2,3): rr.append([f"Standart-128, r = {r} (0-qatlam)"]+cr(f'16_std_r{r}',0))
for r in (1,3): rr.append([f"Standart-128, r = {r} (barcha bitlar)"]+cr(f'16_std_r{r}'))
T([3150,1030,1030,1030,1030,1030,1030],rr,"Kub testlari: yig‘indisi doim nol bo‘lgan chiqish bitlari ulushi")
lay1=A2['256_std_r1']
rr=[["Bit-qatlam j (Standart-256, r = 1)"]+[str(j) for j in range(8)]]
for d in (4,8,12): rr.append([f"d = {d}"]+[fz(v,2) for v in lay1[str(d)][1]])
T([3354]+[750]*8,rr,"Standart-256, 1 raunddan keyin: bit-qatlamlar bo‘yicha nol yig‘indilar ulushi")
lay16=A2['16_std_r1']
rr=[["Bit-qatlam j (Standart-128, r = 1)"]+[str(j) for j in range(4)]]
for d in (4,8,12): rr.append([f"d = {d}"]+[fz(v,2) for v in lay16[str(d)][1]])
T([4554,1200,1200,1200,1200],rr,"Standart-128, 1 raunddan keyin: bit-qatlamlar bo‘yicha nol yig‘indilar ulushi")
P("Standart-256 da r = 0 (faqat 0-nuqtadagi yutish) va d = 12 da ulush 0,84 ga yetadi: bu Z ning 6-darajasi va bayt bo‘yicha lokalligi bilan bog‘liq. r ≥ 1 da ulush tasodifiy funksiya darajasiga (0,05–0,14) tushadi, ya’ni xabarning 16 biti bo‘yicha daraja 12 dan oshadi; bunga Qo‘sh dagi J, K bog‘lanishlari va yuqori bitlarning T-funksiya darajasi o‘sishi sabab bo‘ladi. Standart-128 da esa 0-qatlam barcha d va r uchun 1,00: bu qatlam xabar bitlariga nisbatan chiziqli (daraja 1) bo‘lib qoladi.")
H2('3.5. Hujum namoyishi: Standart-128 da 0-qatlamni linearizatsiya qilish')
P("Buzg‘unchi modeli: kalitli rejim, kalit noma’lum, buzg‘unchi bir blokli xabarlar uchun xesh qiymatlarni oladi. U chiqish 0-qatlamini xabar 0-qatlamining affin funksiyasi deb faraz qiladi: o₀ = A·m₀ ⊕ c (32 × 33 noma’lum koeffitsiyent) va ularni 80 ta xabar bo‘yicha Gauss usulida topadi, so‘ngra 300 ta yangi xabar uchun bashorat qiladi.")
T([3000,3200,3154],[["Rejim","32 bitning hammasi to‘g‘ri","Bitlar bo‘yicha to‘g‘ri"],["Standart-128",fz(A3['16_std']['full_vec'],3),fz(A3['16_std']['per_bit'],3)],["Standart-256",fz(A3['256_std']['full_vec'],3),fz(A3['256_std']['per_bit'],3)]],"Chiqish 0-qatlamining affin modelini qurish natijasi")
rr=[["Sinov xabari","Haqiqiy 0-qatlam","Bashorat"]]
for m_,a_,p_ in MR['A3']['std']['misollar']: rr.append([m_,a_,p_])
T([3154,3100,3100],rr,"Standart-128: sinov xabarlari uchun bashorat misollari",mono=(0,1,2))
P("Standart-128 da 80 ta so‘rovdan keyin buzg‘unchi istalgan xabar uchun kalitli xesh qiymatining 32 bitini xatosiz bashorat qiladi. A va c faqat kalitning 0-qatlamiga bog‘liq bo‘lgani uchun kalitning 0-qatlami (30 ta noma’lum bit) qolganlaridan alohida 2³⁰ ta sinov bilan tiklanadi, so‘ng qolgan 96 bit qidiriladi; umumiy murakkablik ≈2⁹⁶ (kalit fazosi 2¹²⁶). Standart-256 da affin model ishlamaydi.")
P("*Taxmin qilish va aniqlash (guess-and-determine) strategiyasi.* Buzg‘unchi kalitning 0-qatlamini (2³⁰ variant) taxmin qilsa, M(k₀) va L matritsalari ma’lum bo‘ladi va barcha raundlarning 0-qatlam tenglamalari to‘liq chiziqli tizimga aylanadi. Shundan so‘ng 1-bit qatlam tenglamalari ham chiziqli bo‘lib qoladi (Qo‘sh da y₁ = x₁ ⊕ δ·x₀, Aralash da 1-bit faqat 0- va 1-bitlarga bog‘liq), ko‘chirishlar esa 0-qatlam qiymatlari orqali aniqlanadi. Bu qatlamma-qatlam yechish g‘oyasi T-funksiyali raundlar uchun tipik bo‘lib, uning to‘liq baholanishi keyingi tadqiqot mavzusi; Standart-256 da u yutish nuqtasidagi Z tufayli faqat bitta iteratsiya ichida qo‘llaniladi.")
H2('3.6. Bardoshlilik bahosi')
IMG('ch3.png',15.5,7.3,"Linearizatsiya mehnatining tenglamalar darajasiga bog‘liqligi")
T([2600,2000,2000,2754],[["Rejim","Yutishdagi daraja","Talab qilinadigan","Bardoshlilikka erishiladigan raund"],["Standart-128","1 (XOR)","≥ 4","erishilmaydi (0-qatlam doim chiziqli)"],["Standart-256","6","≥ 8","1-raunddan keyin (yuqori bitlar darajasi o‘sishi hisobiga)"]],"Algebraik bardoshlilik bahosi")
H2('3.7. Algebraik kriptotahlil bo‘yicha xulosalar')
BL("Daraja 1 dan yuqori bo‘lgan yagona element — yutish nuqtasidagi o‘zgartirish: XOR — 1, Z — 6. Qo‘sh va Aralash bit darajasida T-funksiyalar, ularning 0-qatlami chiziqli.")
BL("Raund tenglamalari tizimining hajmini Qo‘sh belgilaydi (256 bitli rejimda bir raundda ≈2,4·10⁵ ta o‘zgaruvchi, 3 raund uchun ≈8,4·10⁵).")
BL("Standart-128 da 0-qatlam butun xesh davomida chiziqli: 80 ta so‘rov bilan 32 bitli bashorat 100% aniqlikda ishlaydi, kalitning 0-qatlami alohida tiklanadi. Standart-128 algebraik kriptotahlilga bardoshli emas.")
BL("Standart-256 da Z ning 6-darajasi 0-nuqtada talabga (8) yetmaydi; bardoshlilik 1-raunddan keyin, yuqori bitlar darajasi o‘sgani hisobiga paydo bo‘ladi.")

# ======================= 4. INTEGRAL =======================
PB(); H1('4. Integral (square) kriptotahlil')
H2('4.1. Usulning mohiyati va bardoshlilik mezoni')
P("Integral kriptotahlilda buzg‘unchi kirishlar to‘plamini maxsus tanlaydi: masalan, bitta bayt barcha 256 qiymatni qabul qiladi (A — faol), qolganlari doimiy (C). So‘ngra bu to‘plam akslantirishlardan o‘tganda har bir pozitsiyada qanday xossa saqlanishi kuzatiladi: A (barcha qiymatlar bir martadan), C (doimiy), B (balanslangan: barcha qiymatlarning XOR yig‘indisi nol) yoki U (noma’lum). Agar r raunddan keyin biror bayt yoki bit ehtimollik 1 bilan balanslangan bo‘lsa, bu r raund uchun integral farqlovchi hisoblanadi: tasodifiy funksiyada bunday bayt 2⁻⁸, bit esa 1/2 ehtimollik bilan balanslangan bo‘ladi.")
P("Hisobotda byte darajasidagi xossalar bilan birga bit darajasidagi balans ham kuzatiladi: har bir bit-qatlam j uchun to‘plam bo‘yicha XOR yig‘indining j-biti doim nol bo‘lgan pozitsiyalar soni. B7 xossasi — XOR yig‘indisi {00, 80} dan biri (0–6-bitlar balanslangan, MSB noma’lum).")
H2('4.2. Akslantirishlarning tanlangan to‘plamlarga ta’siri')
H3('4.2.1. BaytZichlash')
P(f"Z jadvalida har bir 4 bitli qiymat aynan 16 marta uchraydi, shuning uchun faol kirish (A) Z dan keyin balanslangan (B) to‘plamga aylanadi: XOR yig‘indisi {I['komponentlar']['Z_xor_yigindi']}, lekin qiymatlar takrorlanadi. Standart-256 da holatn baytidagi faol to‘plam yangi holat baytining quyi yarim baytida B, yuqori yarim baytida C beradi; holat baytidagi faol to‘plam esa yuqori yarim baytda B beradi. XOR (Standart-128) A ⊕ C = A, ya’ni faol to‘plamni o‘zgarishsiz o‘tkazadi.")
H3('4.2.2. Qo‘sh')
qe=I['komponentlar']['Qosh_element_turli_qiymatlar']; qx=I['komponentlar']['Qosh_element_xor_yigindi']
P(f"Bitta element (parametrlar belgilangan) uchun 256 ta kirishning obrazlari 200 ta parametrlar to‘plamining {qe.get('255',0)} tasida 255 xil, {qe.get('256',0)} tasida 256 xil qiymatdan iborat: nolni A₂ + B₂ ga almashtirish qoidasi tufayli element akslantirishi odatda bijeksiya emas va A to‘plamni A ga o‘tkazmaydi. Obrazlarning XOR yig‘indisi {qx['00']} holatda 00, {qx['80']} holatda 80, qolgan {qx['boshqa']} holatda boshqa qiymat; demak bitta element darajasida ham balans kafolatlanmaydi.")
mk=I['komponentlar']
rr=[["Akslantirish (holat[0,0] faol)","A","C","B","B7","U"]]
for p,lab in [(256,'256'),(16,'128')]:
    d_=mk[f'massiv_{p}']
    for k_,lb in [('Qosh_holat',"Qo‘sh: holat"),('Qosh_holatn',"Qo‘sh: holatn"),('Aralash','Aralash'),('BZ_n_faol','BaytZichlash (holatn[0] faol)'),('XOR_n_faol','XOR (holatn[0] faol)')]:
        if k_ in d_: rr.append([f"{lab}: {lb}"]+[fz(d_[k_][t],2) for t in ('A','C','B','B7','U')])
T([3554,1160,1160,1160,1160,1160],rr,"Bitta faol elementli to‘plamning massiv akslantirishlaridan keyingi xossalari (32 pozitsiya bo‘yicha o‘rtacha soni)",key='intarr')
P("Qo‘sh massiv darajasida faol to‘plamni deyarli butun massivga tarqatadi: J yig‘indi va K ko‘paytma faol elementga bog‘liq bo‘lgani uchun boshqa barcha elementlarning A, B parametrlari o‘zgaradi va doimiy elementlar ham U ga aylanadi. 256 bitli rejimda Qo‘sh dan keyin pozitsiyalarning ≈83 foizi U, 128 bitli rejimda esa ≈70 foizi B yoki B7 bo‘lib qoladi (mod 16 da T-funksiya xossasi ko‘proq saqlanadi).")
H3('4.2.3. Aralash')
P("Aralash belgilangan kₑ uchun h ga nisbatan Z/2ⁿ ustida chiziqli: har bir chiqish elementi c·x + const ko‘rinishida (x — faol element). Agar c toq bo‘lsa, x → c·x + const o‘rin almashtirish, natija A; agar c = 2ᵗ·toq (t ≥ 1) bo‘lsa, har bir qiymat 2ᵗ marta (juft marta) uchraydi va XOR yig‘indisi nol, natija B; agar c ≡ 0 bo‘lsa, natija C. Shunday qilib, Aralash A to‘plamni A, B yoki C ga o‘tkazadi va hech qachon U hosil qilmaydi (⟦intarr⟧-jadvalda: o‘rtacha 3,1 ta A, 3,9 ta B, 25 ta C, 0 ta U).")
H3('4.2.4. SurHolat, SurKalit, TuzilmaKalit')
P("SurHolat xossalarni pozitsiyalar bo‘yicha ko‘chiradi; SurKalit va TuzilmaKalit faqat kₑ ga ta’sir qiladi va holat to‘plamining xossalarini o‘zgartirmaydi.")
H3('4.2.5. Bit darajasidagi balans')
P("T-funksiya xossasi integral tahlil uchun muhim natija beradi. 0-qatlam barcha yutishsiz akslantirishlarda chiziqli: chiqishning har bir 0-biti kirish 0-bitlarining chiziqli funksiyasi. Faol bayt 256 qiymatni qabul qilganda uning 0-biti 128 marta 0 va 128 marta 1 bo‘ladi, shuning uchun har qanday chiziqli funksiyaning to‘plam bo‘yicha yig‘indisi nol. Demak, yutishsiz raundlarda holatning barcha 32 ta 0-biti ehtimollik 1 bilan balanslangan bo‘lib qolishi kerak. Yuqori qatlamlarda bunday kafolat yo‘q: Qo‘sh dagi tenglik shartlari (Δ = 10, nolni almashtirish) T-funksiya xossasini buzadi.")
H2('4.3. Integral xossalarning akslantirishlar va raundlar orqali o‘tishi')
P("Birinchi tajribada 1-raund kirishidagi (0-nuqtadagi yutishdan keyingi) holatning holat[0,0] elementi faol qilindi (256 bitli rejimda 256, 128 bitli rejimda 16 qiymat), qolgan elementlar va kalit tasodifiy. Tajriba 40 ta tasodifiy kalit va holatda takrorlandi; jadvallarda barcha 40 tajribada balanslangan pozitsiyalar soni keltirilgan. ⟦intop⟧-jadvalda 1-raund akslantirishlari bo‘yicha natijalar.")
def irow(key,j):
    out=[]
    for r in I[key]:
        if r['raund']==j: out.append(r)
    return out
rr=[["Rejim, akslantirish","Bayt: doim B","Bit-qatlamlar bo‘yicha doim nol bitlar (0, 1, 2, …)","O‘rtacha: B / U"]]
for key,lab in [('raund_256_holat','256'),('raund_16_holat','128')]:
    for r in irow(key,1):
        rr.append([f"{lab}: {opn[r['amal']]}",str(r['doim_B']),", ".join(map(str,r['qatlam_doim_nol'])),f"{fz(r['ortacha']['B'],1)} / {fz(r['ortacha']['U'],1)}"])
T([2900,1300,3300,1854],rr,"1-raund akslantirishlari bo‘yicha integral xossalar (holat[0,0] faol, 40 tajriba)",key='intop')
rr=[["1-raund akslantirishi","To‘plam bo‘yicha XOR-yig‘indi (A ilova ma’lumotlari)"]]
for r in XE['integral_misol']:
    if r['raund']==1 and r['amal'] in ('Aralash','Qosh1','Qosh2'): rr.append([opn[r['amal']],nl(r['yigindi'])])
T([3354,6000],rr,"Standart-256, A ilova misoli: holat[0,0] faol, 256 ta holat bo‘yicha XOR-yig‘indilar",mono=(1,))
P("Aralash dan keyin barcha yig‘indilar 00; Qo‘sh dan keyin yig‘indilar noldan farq qiladi, lekin ularning hammasi juft (eng kichik bit 0), ya’ni 0-qatlam balansi saqlanadi.")
P("Aralash dan keyin barcha 32 pozitsiya balanslangan (A, B yoki C) va barcha bit-qatlamlar balanslangan — 4.2.3-banddagi nazariya tasdiqlandi. Birinchi Qo‘sh dan keyin bayt darajasidagi balans yo‘qoladi, 1–3-qatlamlarda qisman saqlanadi, ikkinchi Qo‘sh dan keyin esa faqat 0-qatlam (32 bit) qoladi. Raundlar bo‘yicha natijalar ⟦intr⟧-jadvalda.")
rr=[["Raund j"]+[str(j) for j in range(1,11)]]
for key,lab in [('raund_256_holat','Std-256: 0-qatlam'),('raund_256_holat#','Std-256: 1–7-qatlamlar'),('raund_16_holat','Std-128: 0-qatlam'),('raund_16_holat#','Std-128: 1–3-qatlamlar')]:
    rows_=[r for r in I[key.rstrip('#')] if r['amal']=='Tuz']
    if key.endswith('#'): rr.append([lab]+[str(sum(r['qatlam_doim_nol'][1:])) for r in rows_])
    else: rr.append([lab]+[str(r['qatlam_doim_nol'][0]) for r in rows_])
T([2850]+[650]*10,rr,"Raundlar oxirida doim balanslangan bitlar soni (holat[0,0] faol)",key='intr')
IMG('ch4.png',15.5,6.9,"Raundlar bo‘yicha doim balanslangan bitlar soni bit-qatlamlar kesimida")
P("Yuqori tartibli integral xossa ham tekshirildi: ikkita bayt (holat[0,0] va holat[1,1]) faol, ya’ni 2¹⁶ = 65536 ta holatdan iborat to‘plam olindi (Standart-256, 8 ta tajriba). Bunday to‘plamda yuqori qatlamlar ham balanslangan bo‘lib qolishi kutilishi mumkin edi.")
ib=XE['ikki_bayt']
T([3354]+[750]*8,[["Raund (2 ta faol bayt)"]+[f"{b}-qatlam" for b in range(8)]]+[[f"{j}-raund"]+[str(v) for v in ib[str(j)]] for j in (1,2,3,4)],"Ikki faol baytli to‘plam: doim balanslangan bitlar soni (8 tajriba)")
P("Natija bir faol baytli to‘plam bilan deyarli bir xil: 0-qatlam doim balanslangan, 1-raunddan keyin 1- va 2-qatlamlarning bir necha biti ham balanslangan, 2-raunddan boshlab esa faqat 0-qatlam qoladi. Demak, yuqori qatlamlarda integral xossalarni yuqori tartibli to‘plamlar bilan ham saqlab bo‘lmaydi; buning sababi — Qo‘sh dagi tenglik shartlari va massivlararo bog‘lanish.")
P("Standart-256 da 0-qatlamning 32 biti 1–7-raundlarda ehtimollik 1 bilan balanslangan, 8-raunddagi yutishdan keyin balans yo‘qoladi. Standart-128 da esa 0-qatlam yutish nuqtalarini ham qo‘shgan holda butun iteratsiya davomida balanslangan qoladi. Yuqori bit-qatlamlarda birinchi raunddan keyin doim balanslangan bitlar qolmaydi.")
H3('4.3.1. Kirish blokidagi faol to‘plam')
P("Ikkinchi tajribada kirish blokining 0-elementi faol qilindi (to‘plam 0-nuqtadan boshlab kuzatiladi). ⟦intblok⟧-jadvalda natijalar keltirilgan.")
rr=[["Rejim, qadam","Bayt: doim B","Bit-qatlamlar bo‘yicha doim nol bitlar","O‘rtacha: B / U"]]
for key,lab in [('raund_256_blok','256'),('raund_16_blok','128')]:
    for r in I[key]:
        if r['raund']==0 or (r['amal']=='Tuz' and r['raund'] in (1,7,10)) or r['amal'] in ('BZ8','BZ9'):
            nm=opn[r['amal']] if r['raund']==0 or r['amal'] in ('BZ8','BZ9') else f"{r['raund']}-raund oxiri"
            rr.append([f"{lab}: {nm}",str(r['doim_B']),", ".join(map(str,r['qatlam_doim_nol'])),f"{fz(r['ortacha']['B'],1)} / {fz(r['ortacha']['U'],1)}"])
T([2900,1300,3300,1854],rr,"Kirish blokidagi faol element: integral xossalarning o‘tishi (40 tajriba)",key='intblok')
P("Standart-256 da 0-nuqtadagi Qo‘sh dan keyin holatning 0- va 1-qatlamlari balanslangan, lekin BaytZichlash dan keyin barcha balans yo‘qoladi: yangi holat baytining yuqori yarim bayti Z(h), quyi yarim bayti Z(hn), Z esa barcha 8 bitni aralashtiradi va T-funksiya tuzilishini buzadi. Standart-128 da XOR 0-qatlam balansini saqlaydi va u butun iteratsiya davomida 32/32 bo‘lib qoladi.")
H2('4.4. To‘liq xesh uchun integral farqlovchi')
tx=I['toliq_xesh']
P("Integral xossa to‘liq xesh funksiya uchun ham tekshirildi. Standart-128: bir blokli (16 baytli) xabarning 0-bayti 256 qiymatni qabul qiladi, qolgan baytlar va kalit tasodifiy. Standart-256: ikki blokli (64 baytli) xabarning ikkinchi blokidagi 0-bayt faol. 40 ta tajribada xesh qiymatlar to‘plamining XOR yig‘indisi hisoblandi (⟦intfull⟧-jadval).")
rr=[["Rejim","Bit-qatlam j"]+[str(j) for j in range(8)]]
rr.append(["Standart-128","doim nol bitlar"]+[str(v) for v in tx['16']['qatlam_boyicha_doim_nol_bitlar']]+["—"]*4)
rr.append(["Standart-128","nol ulushi"]+[fz(v,2) for v in tx['16']['qatlam_boyicha_nol_ulushi']]+["—"]*4)
rr.append(["Standart-256","doim nol bitlar"]+[str(v) for v in tx['256']['qatlam_boyicha_doim_nol_bitlar']])
rr.append(["Standart-256","nol ulushi"]+[fz(v,2) for v in tx['256']['qatlam_boyicha_nol_ulushi']])
T([1750,1700]+[738]*8,rr,"To‘liq xesh: to‘plam bo‘yicha XOR yig‘indisi nol bo‘lgan bitlar (40 tajriba)",key='intfull')
P("Standart-128 da xesh qiymatning 0-qatlamidagi 32 bitning hammasi 40 tajribaning barchasida balanslangan: bu 256 ta (aslida 16 ta yetarli) tanlangan xabar bilan to‘liq xesh funksiyani tasodifiy funksiyadan ajratish imkonini beradi. Tasodifiy funksiyada 32 bitning hammasi nol bo‘lish ehtimolligi 2⁻³². Standart-256 da yig‘indilar tasodifiy (nol ulushi ≈0,5) va to‘liq xesh uchun integral farqlovchi topilmadi.")
P("*Buzg‘unchi uchun foydalanish.* Standart-128 kalitli rejimida integral farqlovchi kalitni bilmasdan algoritmni aniqlash va xesh qiymatning 32 biti haqida ishonchli ma’lumot olish imkonini beradi; 3.5-bo‘limdagi linearizatsiya hujumi bilan birgalikda u kalitning 0-qatlamini tiklashga olib keladi. Standart-256 da ichki holat bo‘yicha 7 raundli farqlovchi mavjud, lekin buzg‘unchi ichki holatni bevosita boshqara olmaydi: xabar orqali kiritilgan to‘plam 0-nuqtadagi BaytZichlash da balansini yo‘qotadi. Shuning uchun Standart-256 da integral xossa faqat bitta blok ichida, oldingi yutishdan keyingi raundlar uchun ahamiyatga ega.")
H2('4.5. Bardoshlilik bahosi')
T([2200,2500,2400,2254],[["Rejim","Bayt darajasidagi integral xossa","Bit darajasidagi (0-qatlam) xossa","Xulosa"],["Standart-256","1 ta Qo‘sh dan keyin yo‘qoladi","1–7-raundlarda saqlanadi, 8-raunddagi yutishda yo‘qoladi","xabar orqali — 0-nuqtadan keyin bardoshli; holat orqali — 8-raunddan keyin"],["Standart-128","1 ta Qo‘sh dan keyin yo‘qoladi","butun xesh davomida saqlanadi","bardoshli emas (to‘liq xesh uchun farqlovchi)"]],"Integral bardoshlilik bahosi")
H2('4.6. Integral kriptotahlil bo‘yicha xulosalar')
BL("Bayt darajasidagi integral xossalar (A, B) Qo‘sh o‘zgartirishining massivlararo bog‘lanishi (J, K) tufayli bitta Qo‘sh dan keyin yo‘qoladi; Aralash A ni A, B yoki C ga o‘tkazadi, BaytZichlash (Z) A ni B ga aylantiradi, XOR A ni saqlaydi.")
BL("0-qatlam T-funksiya xossasi tufayli yutishsiz raundlarda ehtimollik 1 bilan balanslangan: Standart-256 da 1–7-raundlar uchun (yutish ichki holatdan keyin) 32 bitli integral farqlovchi mavjud; 8-raunddagi yutishdan keyin u yo‘qoladi.")
BL("Standart-256 da xabar orqali kiritilgan faol to‘plam 0-nuqtadagi BaytZichlash dan keyinoq balansini yo‘qotadi; to‘liq xesh uchun integral farqlovchi topilmadi.")
BL("Standart-128 da 0-qatlam balansi butun xesh davomida saqlanadi: 16–256 ta tanlangan xabar bilan to‘liq xesh uchun 32 bitli integral farqlovchi quriladi. Standart-128 integral kriptotahlilga bardoshli emas.")

# ======================= UMUMIY =======================
PB(); H1('Umumiy xulosa')
T([2400,3500,3454],[["Usul","Standart-256","Standart-128"],
 ["Chiziqli","2⁻⁶⁴ chegarasiga mediana kalitlarda 5–6 ta yutish qatlamidan keyin (≈18–19-raund, kamida 3 blokli xabar); eng yomon kalitlarda erishilmaydi","bardoshli emas: xesh qiymatning 32 biti c = 1 bilan kuzatiladi"],
 ["Differensial","2⁻¹²⁸ chegarasiga 1-iteratsiyaning 9-raundidan keyin","bardoshli emas: XOR ayirmani o‘tkazadi va kompensatsiya qilinadi"],
 ["Algebraik","1-raunddan keyin (Z ning 6-darajasi 0-nuqtada yetarli emas)","bardoshli emas: 80 so‘rov bilan 32 bit bashorat, kalit qatlamlarga ajraladi"],
 ["Integral","xabar orqali — 0-nuqtadan keyin; ichki holat orqali — 8-raunddan keyin (1–7-raundlarda 32 bitli farqlovchi)","bardoshli emas: to‘liq xesh uchun 32 bitli farqlovchi"],
 ["Umumiy qoldiq xossalar","Aralash degeneratsiyasi: chiqishda ≈6 ta c = 1 munosabat, doimiy bitlar, ayirmalarning ≈3% so‘nishi","xuddi shunday"]],"Standart algoritmning to‘rtta kriptotahlil usuliga bardoshliligi")
P("Tahlil quyidagi asosiy xulosalarga olib keladi. Birinchidan, 1-algoritmning raund funksiyasi (Aralash, Qo‘sh, SurHolat, SurKalit, TuzilmaKalit) 2ⁿ moduli bo‘yicha arifmetika va o‘rin almashtirishlardan iborat bo‘lgani uchun T-funksiya xossasiga ega. Natijada 0-qatlam barcha yutishsiz raundlarda chiziqli tenglama bilan aniq kuzatiladi (chiziqli tahlil), MSB ayirmalari har raundda ≈0,9 ehtimollik bilan saqlanadi (differensial tahlil), 0-qatlam darajasi 1 bo‘lib qoladi (algebraik tahlil) va ehtimollik 1 bilan balanslanadi (integral tahlil). Shuning uchun algoritmning barcha to‘rtta usulga bardoshliligi to‘liq yutish nuqtasidagi BaytZichlash o‘zgartirishiga bog‘liq.")
P("Ikkinchidan, Standart-128 dagi XOR chiziqli, differensial jihatdan shaffof, algebraik darajasi 1 va integral xossalarni saqlaydi. Shu sababli Standart-128 to‘rttala usulning hech biriga bardoshli emas: xesh qiymatning 32 bitli 0-qatlami xabar 0-qatlamining affin funksiyasi, u kalitni bilmasdan bashorat qilinadi, kalitning 0-qatlami alohida tiklanadi, kolliziya murakkabligi 2⁴⁸ gacha kamayadi.")
P("Uchinchidan, Standart-256 dagi Z jadvali chiziqli bo‘lmagan, lekin kriptografik jihatdan zaif: maksimal korrelyatsiya 0,25, maksimal differensial ehtimollik 0,156 (ayirma so‘nishi bilan), algebraik daraja 6, holat va xabar axboroti chiqish baytida aralashmaydi. Natijada Standart-256 bardoshlilikka faqat bir necha yutish nuqtasidan keyin erishadi; chiziqli tahlil bo‘yicha bu kamida 3 blokli xabarni talab qiladi, eng yomon kalitlarda esa erishilmaydi.")
P("To‘rtinchidan, Aralash o‘zgartirishining 2 moduli bo‘yicha degeneratsiyasi (L matritsasi rangi o‘rtacha ≈26, nol satrlar va ustunlar) ikkala rejimda ham chiqishda c = 1 chiziqli munosabatlarni, doimiy bitlarni va ayirmalarning ehtimollik 1 bilan so‘nishini keltirib chiqaradi.")
H2('Tavsiyalar')
BL("Yutish nuqtasidagi BaytZichlash o‘zgartirishini optimal kriptografik ko‘rsatkichlarga ega chiziqli bo‘lmagan o‘zgartirish bilan almashtirish (masalan, S(h ⊕ S(n)) ko‘rinishidagi SBZ, bunda S — differensial bir xilligi 4 va nochiziqliligi 112 bo‘lgan S-box).")
BL("Aralash va TuzilmaKalit o‘zgartirishlarini diamatritsa 2 moduli bo‘yicha har doim teskarilanuvchi bo‘ladigan qilib qayta loyihalash; bu chiqishdagi c = 1 munosabatlarni, doimiy bitlarni va ichki kolliziyalarni bartaraf etadi.")
BL("Raund funksiyasining o‘ziga yuqori bitlarni quyi bitlarga o‘tkazuvchi element (masalan, bit bo‘yicha davriy surish yoki S-box qatlami) qo‘shish; bu yutishsiz raundlarning T-funksiya xossasini yo‘qotadi va ularni to‘rttala usul bo‘yicha bardoshlilikka hissa qo‘shadigan qiladi.")
BL("Oxirgi raunddan keyin chiziqli bo‘lmagan yakuniy qatlam qo‘shishni ko‘rib chiqish.")
H2('Tahlil usuli va cheklovlari')
P("Akslantirishlarning korrelyatsion va ayirmalar matritsalari, ANF darajalari, implitsit tenglamalar soni va to‘plam xossalari barcha kirishlar bo‘yicha aniq hisoblandi. Raund darajasidagi ko‘rsatkichlar tanlanma asosida o‘lchandi: chiziqli tenglama — 1500 kalit, ayirmalar — 2000–3000 juftlik, integral — 40 ta tajriba (har birida 16 yoki 256 element), kub testlari — har bir holatda 4 ta kub, faol baytlar — 120–200 ta kalit. Chiziqli izlar 0-qatlam modeli doirasida, differensial chegaralar har bir faol bayt uchun eng yaxshi ehtimollik bilan baholandi; tenglamalar soni 3.2.4-banddagi modelga asoslangan. Barcha hisoblar uchun dasturlar (uzmst285_tahlil paketi, shu jumladan yangi integral.py moduli) hisobotga ilova qilingan.")
import re as _re
def _fix(x):
    if isinstance(x,str): return _re.sub(r'⟦(\w+)⟧',lambda m:str(TK[m.group(1)]),x)
    if isinstance(x,list): return [_fix(y) for y in x]
    return x
B=[_fix(b) for b in B]
json.dump(B,open('blocks.json','w'),ensure_ascii=False); print(len(B),tc[0],fc[0])
