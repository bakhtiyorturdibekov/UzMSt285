import json, math
R=json.load(open('/home/claude/nb/misollar_natijalari.json'))
B=[]
H1=lambda t:B.append(['h1',t]); H2=lambda t:B.append(['h2',t]); H3=lambda t:B.append(['h3',t])
P=lambda t:B.append(['p',t]); F=lambda t:B.append(['f',t]); BL=lambda t:B.append(['b',t])
def XUL(t): B.append(['xul',t])
def T(w,rows,cap,mono=()): B.append(['cap',cap]); B.append(['t',w,rows,list(mono)])
PB=lambda:B.append(['pb'])
fz=lambda x,d=2:(f'{x:.{d}f}').replace('.',',')
nl='\n'.join
tc=[0]
def cap(t): tc[0]+=1; return f"{tc[0]}-jadval. {t}"
opn={'Aralash':'Aralash(holat, kₑ)','Qosh1':'Qo‘sh(holat, kₑ)','Sur':'SurHolat, SurKalit','Qosh2':'Qo‘sh(holat, kₑ)','Tuz':'TuzilmaKalit(kₑ, k)'}

B.append(['title','SBZ O‘ZGARTIRISHI KRIPTOTAHLILI XULOSALARINING AKSLANTIRISHLAR KETMA-KETLIGIDA KUZATILGAN MISOLLAR BILAN ASOSLANISHI'])
B.append(['sub','«O‘zMSt 285:2024 1-algoritmida BaytZichlash o‘rniga SBZ o‘zgartirishini qo‘llashning chiziqli, differensial va algebraik kriptotahlilga ta’siri» hisobotiga ilova'])
H1('Kirish')
P("Ushbu hujjatda asosiy hisobotdagi 13 ta xulosaning (chiziqli kriptotahlil bo‘yicha 5 ta, differensial va algebraik kriptotahlil bo‘yicha 4 tadan) har biri aniq misolda tekshiriladi. Har bir misolda algoritm akslantirishlari ketma-ket bajarilib, har bir qadamdan keyingi qiymatlar (holat massivi, uning 0-qatlami, ayirmalar, approksimatsiya va tenglamalar) ko‘rsatiladi va qadamning xulosaga qanday hissa qo‘shishi izohlanadi.")
P("Barcha misollar ilova qilingan *xulosalar_misollar.ipynb* Jupyter daftarida hisoblangan. Daftar bajarilgan holda topshirilgan, ya’ni barcha natijalar uning ichida ko‘rinib turadi; uni qayta ishga tushirish orqali har bir raqamni takrorlash mumkin. Dastlabki ma’lumotlar sifatida O‘zMSt 285:2024 standartining A ilovasidagi xeshlash kaliti va xabari olingan:")
F("k = c86ed4b2 756df1cd 6b6eca81 d4418092 21ab81bb a0c7c150 44be8feb 934f95a2,")
F("M = «funksiyaxeshirovaniyainformasionnayatexnologiyakriptograficheska» (64 bayt).")
P("128 bitli rejimda kalit sifatida k ning birinchi 16 bayti olinadi. Daftardagi realizatsiya standartning nazorat misolini va SBZ materialidagi barcha nazorat qiymatlarini takrorlaydi (daftarning 1-hujayrasi). Jadvallarda 4×8 massivlar o‘n oltilik sanoq tizimida, 0-qatlamlar esa har bir elementning eng kichik biti sifatida beriladi; holat[s,u] — s-satr, u-ustundagi element.")

# ======================= CHIZIQLI =======================
PB(); H1('1. Chiziqli kriptotahlil xulosalari')
H2('1.1. Birinchi xulosa: yutishsiz raundlar 0- va 1-bit qatlamlarni c ≈ 1 bilan o‘tkazadi')
XUL("Yutish nuqtasi bo‘lmagan raundlar (1–7, 10) 0- va 1-bit qatlamlarda c ≈ 1 bilan o‘tadi, ya’ni chiziqli bardoshlilikka hissa qo‘shmaydi; bu barcha variantlar uchun umumiy xossa.")
L1=R['L1']
P("*Misol.* SBZ-256 varianti, A ilova kaliti va xabari, 1-iteratsiya (holat = 1-blok, holatn = 2-blok). 0-nuqtadagi Qo‘sh va SBZ bajarilgandan keyingi holat va uning 0-qatlami h₀ quyidagicha:")
T([4677,4677],[["0-nuqtadagi yutishdan keyingi holat","0-qatlam h₀"],[nl(L1['h_bz0']),nl(L1['h0'])]],cap("Kuzatish boshlanadigan holat (SBZ-256, A ilova ma’lumotlari)"),mono=(0,1))
P("Endi 1-raundning har bir akslantirishidan keyin 0-qatlam nazariy qoida bo‘yicha bashorat qilinadi va haqiqiy qiymat bilan solishtiriladi. Qoida: Aralash da h₀ ← M(k₀)·h₀, Qo‘sh da h₀ o‘zgarmaydi, SurHolat da h₀ ← P·h₀, TuzilmaKalit holatga ta’sir qilmaydi.")
rows=[["Akslantirish","Holat (haqiqiy)","0-qatlam (haqiqiy)","Bashorat bilan mos bitlar"]]
for q in L1['qadamlar']: rows.append([opn[q['amal']],nl(q['holat']),nl(q['qatlam0']),f"{q['mos']}/32"])
T([2100,3150,2350,1754],rows,cap("1-raund akslantirishlari bo‘yicha 0-qatlamni kuzatish"),mono=(1,2))
P("Har bir qadamning izohi:")
BL("*Aralash.* Holat baytlari to‘liq o‘zgaradi (masalan, holat[0,0] = bf → c0), lekin 0-qatlam M(k₀)·h₀ ga aniq teng chiqdi. Sababi: 2ⁿ moduli bo‘yicha ko‘paytma va yig‘indining eng kichik biti faqat qo‘shiluvchilarning eng kichik bitlariga bog‘liq. A ilova kaliti uchun, masalan, h′[0,0]₀ = h[1,1]₀ ⊕ h[2,2]₀ tenglamasi bajariladi (3.1-bo‘limga qarang).")
BL("*Qo‘sh(holat, kₑ).* Baytlar yana to‘liq o‘zgaradi (c0 → 40), ammo 0-qatlam bitma-bit saqlanadi: x⁻¹ ≡ −A·x·(B + R·x)⁻¹ va A toq, R juft bo‘lgani uchun x⁻¹ ≡ x (mod 2).")
BL("*SurHolat, SurKalit.* 0-qatlam bitlari pozitsiyalar bo‘yicha joyini o‘zgartiradi, bu P o‘rin almashtirish matritsasi bilan aniq tasvirlanadi.")
BL("*Ikkinchi Qo‘sh va TuzilmaKalit.* 0-qatlam yana o‘zgarmaydi. TuzilmaKalit dan keyin kₑ ning 0-qatlami kalitning 0-qatlamiga teng: tekshiruv natijasi — " + ("ha" if L1['ke_ok'] else "yo‘q") + ". Demak, keyingi raundlarda ham Aralash matritsasi o‘sha M(k₀) bo‘lib qoladi.")
rm=L1['raund_mos']
T([2600]+[675]*10,[["Raund j"]+[str(j) for j in range(1,11)],["Mos bitlar (32 dan)"]+[str(v) for v in rm]],cap("h₀⁽ʲ⁾ = Lʲ·h₀ bashoratining raundlar oxiridagi aniqligi"))
P(f"1–7-raundlarda bashorat 32/32 aniqlikda bajariladi: 7 raund davomida holat 0-qatlami bitta chiziqli tenglama h₀⁽⁷⁾ = L⁷·h₀ bilan to‘liq aniqlanadi (L = P·M(k₀), bu kalit uchun rang L = {L1['rangL']}). 8-raundda yutish nuqtasi (SBZ) ishlaydi va moslik tasodifiy darajaga ({rm[7]}/32) tushadi.")
p=L1['param']
P(f"*1-bit qatlam.* 0-nuqtadagi Qo‘sh o‘zgartirishining holat[0,0] elementi uchun haqiqiy parametrlar hisoblandi: R = {p['R']}, A₁ = {p['A1']}, B₁ = {p['B1']}, A₂ = {p['A2']}, B₂ = {p['B2']}. Shu parametrlar bilan x → x⁻³ akslantirishi barcha 256 ta kirishda tekshirildi: y₀ = x₀ tengligi {L1['y0_ok']}/256 kirishda, y₁ = x₁ ⊕ {L1['y1'][0]}·x₀ tengligi {L1['y1'][1]}/256 kirishda bajariladi. Har bir chiqish biti uchun eng yaxshi korrelyatsiya: " + ", ".join(fz(v,3) for v in L1['bitc']) + ".")
P("*Natija.* Misolda yutishsiz raundlar 0-qatlamni c = 1, 1-bit qatlamni ham c = 1 bilan o‘tkazishi akslantirishma-akslantirish ko‘rsatildi. Bu xossa yutish o‘zgartirishiga bog‘liq emas (BaytZichlash yoki SBZ faqat 0-, 8-, 9-nuqtalarda ishlaydi), shuning uchun barcha variantlar uchun umumiydir.")

H2('1.2. Ikkinchi xulosa: Standart-128 da 0-qatlam butun xesh davomida c = 1 bilan kuzatiladi')
XUL("Standart-128 da XOR tufayli 0-qatlam butun xesh davomida c = 1 bilan kuzatiladi; bu variant raundlar sonidan qat’i nazar chiziqli kriptotahlilga bardoshli emas.")
L2=R['L2']
P("*Misol.* Standart-128 varianti, kalit — k ning birinchi 16 bayti, xabar — 64 baytli A ilova xabari. 128 bitli rejimda u 4 ta blokka bo‘linadi; ularga uzunlik va NY bloklari qo‘shiladi, shuning uchun 1-blok boshlang‘ich holat bo‘ladi va 5 ta iteratsiya bajariladi. Bashorat qoidasi 1.1-bo‘limdagiga yutish nuqtalari uchun bitta qoida qo‘shish bilan olinadi:")
F("raundda: h₀ ← L·h₀;     yutish nuqtasida (0, 8, 9): h₀ ← h₀ ⊕ blok₀.")
P("Yutish qoidasi quyidagicha asoslanadi: Qo‘sh(holat, blok) holat va blokning 0-qatlamini o‘zgartirmaydi, BaytZichlash esa XOR, ya’ni yangi holatning 0-qatlami eski holat va blok 0-qatlamlarining yig‘indisi.")
rows=[["Iteratsiya","Kirish bloki","Kuzatilgan akslantirishlar soni","Bashorat bilan moslik (minimum)"]]
names={1:'2-blok',2:'3-blok',3:'4-blok',4:'uzunlik bloki',5:'NY bloki'}
for j in L2['jurnal']: rows.append([str(j['iteratsiya']),names[j['iteratsiya']],str(j['amallar']),f"{j['min_mos']}/32"])
T([1700,2400,2750,2504],rows,cap("Standart-128: 0-qatlam bashoratining barcha iteratsiyalar bo‘yicha aniqligi"))
T([4677,4677],[["Xesh qiymatning haqiqiy 0-qatlami","Bashorat qilingan 0-qatlam"],[nl(L2['haqiqiy']),nl(L2['bashorat'])]],cap(f"Yakuniy xesh qiymat {L2['xesh']} ning 0-qatlami"),mono=(0,1))
P("Har bir qadamning izohi: 0-nuqtadagi Qo‘sh(holat, blok) juftlikni saqlaydi; XOR blokning 0-qatlamini qo‘shadi; 1–7-raundlarda 1.1-bo‘limdagi qoidalar ishlaydi; 8- va 9-raunddagi yutishlar yana XOR bo‘lgani uchun bashorat buzilmaydi; 10-raund ham chiziqli. Natijada har bir iteratsiyaning 55 ta akslantirishidan keyin moslik 32/32 bo‘lib qoladi.")
P(f"*Natija.* Xesh qiymatning 32 bitli 0-qatlami xabar bloklarining 0-qatlamlari orqali korrelyatsiya 1 bilan hisoblandi ({L2['mos']}/32). Bu munosabat raundlar sonini oshirish bilan buzilmaydi, chunki har bir raund 0-qatlamga chiziqli L akslantirish sifatida ta’sir qiladi. 3.3-bo‘limda bu xossa amaliy hujumga aylantiriladi.")

H2('1.3. Uchinchi xulosa: Standart-256 da faol bayt boshiga c ≤ 2⁻²')
XUL("Standart-256 da har bir faol bayt ≤ 2⁻² hissa qo‘shadi; 2⁻⁶⁴ chegarasiga mediana kalitlarda 5–6 yutish qatlamidan keyin (≈19-raund) erishiladi, eng yomon kalitlarda amalda erishilmaydi.")
L3=R['L3']
P(f"*Misol, 1-qadam: yutish o‘zgartirishi uchun approksimatsiya.* B ilovadagi Z jadvali uchun eng yaxshi approksimatsiyalardan biri barcha 256 kirishda tekshirildi:")
F("z₀ ⊕ z₂ = x₀ ⊕ x₂ ⊕ x₆ ⊕ x₇")
P(f"Tenglik {L3['agree']}/256 kirishda bajariladi: c = 2·{L3['agree']}/256 − 1 = {fz(L3['cZ'])}, chetlanish ε = {fz(L3['cZ']/2,3)}. Standart-256 da yangi holat baytining quyi yarim bayti Z(holatn bayti) ga teng, shuning uchun bu tenglama yutish nuqtasida bevosita ishlaydi. Haqiqiy algoritmda (20000 ta tasodifiy holat, 0-bayt) Qo‘sh dan keyingi holatn bayti va yangi holat bayti orasida o‘lchangan korrelyatsiya {fz(L3['c_meas'],3)} ga teng, ya’ni nazariy qiymat bilan mos keladi.")
P("*2-qadam: iz o‘tadigan yutish qatlamlari.* Yutish qatlamlari 0, 8, 9, 0′, 8′, 9′ tartibida keladi; ular orasidagi 0-qatlam akslantirishlari L⁸, L, L, L⁸, L. Iz oxirgi qatlamdagi niqobdan orqaga Lᵀ bilan tarqatiladi va har bir qatlamda niqobi noldan farqli baytlar soni (faol baytlar) sanaladi.")
z=L3['zanjir']
rows=[["Qatlamlar soni","Faol baytlar a","Faol pozitsiyalar (oxirgi qatlamdan orqaga)","log₂|c| ≤ −2·a"]]
for kk in map(str,range(1,7)):
    a,path=z[kk]; rows.append([kk,str(a),"; ".join("{"+",".join(f"[{i//8},{i%8}]" for i in pth)+"}" for pth in path),str(-2*a)])
T([1500,1500,4554,1800],rows,cap("A ilova kaliti uchun yutish qatlamlari bo‘yicha minimal faol baytlar (Standart-256)"))
P("Jadvaldan muhim xulosa kelib chiqadi: A ilova kaliti *eng yomon kalitlar* sinfiga kiradi. L matritsasining [0,3] satrida faqat bitta birlik bor (o‘sha [0,3] ustunda), ya’ni holat[0,3] ning 0-biti har raundda o‘zgarmay o‘tadi. Shuning uchun faqat shu pozitsiyadan o‘tuvchi iz har bir yutish qatlamida atigi bitta faol bayt hosil qiladi va 6 ta qatlamdan keyin ham chegara faqat 2⁻¹² ni tashkil qiladi.")
P("*Natija.* Standart-256 da faol bayt boshiga hissa 2⁻² ga teng (o‘lchangan 0,254). Odatiy kalitlarda faol baytlar soni 4-qatlamdan boshlab keskin oshadi (hisobotdagi mediana: 15, 31,5, 46). A ilova kaliti kabi kalitlarda esa 2⁻⁶⁴ ga erishish uchun 32 ta qatlam (≈11 ta iteratsiya) kerak bo‘ladi, bu amalda erishib bo‘lmaydigan chegara.")

H2('1.4. To‘rtinchi xulosa: SBZ da faol bayt boshiga c ≤ 2⁻⁶')
XUL("SBZ-256 da har bir faol bayt ≤ 2⁻⁶ hissa qo‘shadi; 2⁻⁶⁴ chegarasiga mediana kalitlarda 4 ta yutish qatlamidan keyin (≈11-raund) erishiladi; eng yomon kalitlarda 11 ta qatlam (≈4 ta iteratsiya) kerak; SBZ-128 uchun 2⁻³² ga mediana bo‘yicha 4 ta, eng yomon holatda 6 ta qatlamdan keyin erishiladi.")
L4=R['L4']
P("*Misol, 1-qadam: SBZ uchun approksimatsiya.* SBZ korrelyatsiyasi c_SBZ((α, β) → γ) = c_S(α → γ)·c_S(β → α) formulasi bilan aniqlanadi. α = 2D, β = 1A, γ = 01 uchun approksimatsiya tenglamasi:")
F("y₀ ⊕ (h₀ ⊕ h₂ ⊕ h₃ ⊕ h₅) ⊕ (n₁ ⊕ n₃ ⊕ n₄) = 1,     y = S(h ⊕ S(n)).")
P(f"Barcha 65536 ta (h, n) juftlik tekshirildi: chap tomon {L4['ones']} ta juftlikda 1 ga teng, ya’ni korrelyatsiya {L4['c']} = −2⁻⁶. Bu qiymat formulaga to‘liq mos keladi: c_S(2D → 01) = −2⁻³ va c_S(1A → 2D) = +2⁻³, ularning ko‘paytmasi −2⁻⁶. Shu bilan formulaning to‘g‘riligi va SBZ uchun maksimal korrelyatsiya 2⁻⁶ ekani misolda tasdiqlandi.")
P("*2-qadam: yutish qatlamlari.* 1.3-bo‘limdagi faol baytlar zanjiri yutish o‘zgartirishiga bog‘liq emas, chunki u faqat L matritsasi bilan aniqlanadi. Shuning uchun chegara SBZ uchun log₂|c| ≤ −6·a bo‘ladi. Taqqoslash uchun A ilova kaliti (eng yomon) va tasodifiy tanlangan odatiy kalit olindi:")
za=L4['zanjir_A']; zy=L4['yomon']
rows=[["Qatlamlar soni","A ilova kaliti: a","SBZ: log₂|c| ≤","Odatiy kalit: a","SBZ: log₂|c| ≤"]]
for kk in map(str,range(1,7)):
    ay=zy[kk][0] if zy else None
    rows.append([kk,str(za[kk]),str(-6*za[kk]),str(ay),str(-6*ay)])
T([1700,1900,1900,1900,1954],rows,cap("SBZ-256: yutish qatlamlari bo‘yicha chegaralar"))
P(f"Odatiy kalit ({L4['yomon_kalit'][:16]}…) uchun 4-qatlamda faol baytlar soni {zy['4'][0]} ga yetadi va chegara 2^{-6*zy['4'][0]} bo‘ladi, ya’ni 2⁻⁶⁴ dan ancha kichik. Iz yo‘lida faol pozitsiyalar qanday tarqalishi ham kuzatildi: 4-qatlam uchun oxirgidan orqaga " + " → ".join(str(len(pth)) for pth in zy['4'][1]) + " ta faol bayt. A ilova kaliti uchun esa 4-qatlamda chegara faqat 2⁻²⁴; 2⁻⁶⁴ ga erishish uchun 11 ta qatlam kerak bo‘ladi.")
P("*Natija.* SBZ bir faol bayt uchun to‘lovni 2⁻² dan 2⁻⁶ ga oshiradi, ya’ni bir xil iz uchun chegara 3 baravar (log shkalada) kuchliroq bo‘ladi. Odatiy kalitlarda 2⁻⁶⁴ chegarasiga 4-qatlamda, ya’ni 2-iteratsiyaning 0-nuqtasida (≈11-raund) erishiladi. Eng yomon kalitlarda zarur qatlamlar soni keskin ortadi; bu SBZ ga emas, Aralash matritsasining tuzilishiga bog‘liq.")

H2('1.5. Beshinchi xulosa: chiqishdagi c = 1 munosabatlar SBZ ga bog‘liq emas')
XUL("Chiqish 0-qatlamidagi c = 1 munosabatlar (o‘rtacha ≈6 ta) SBZ ga bog‘liq emas va Aralash o‘zgartirishining 2 moduli bo‘yicha degeneratsiyasidan kelib chiqadi.")
L5=R['L5']
P(f"*Misol.* Oxirgi, 10-raund 9-nuqtadagi yutishdan keyin bajariladi: Aralash, Qo‘sh, SurHolat, Qo‘sh, TuzilmaKalit. Demak, xesh qiymatning 0-qatlami h₀ = L·x₀ ko‘rinishida, bu yerda x₀ — 10-raund kirishidagi 0-qatlam. Agar wᵀ·L = 0 bo‘lsa, istalgan x₀ uchun w·h₀ = 0 bo‘ladi. A ilova kaliti uchun rang L = {L5['rang']}, shuning uchun 32 − {L5['rang']} = {len(L5['munosabatlar'])} ta bog‘liq bo‘lmagan munosabat mavjud:")
rows=[["№","Munosabat (xesh qiymat 0-qatlamida)","Standart-256","SBZ-256"]]
for i,m in enumerate(L5['munosabatlar']):
    rows.append([str(i+1)," ⊕ ".join(m)+" = 0",fz(L5['tekshiruv']['std'][i],3),fz(L5['tekshiruv']['sbz'][i],3)])
T([700,5254,1700,1700],rows,cap("A ilova kaliti uchun chiqishdagi chiziqli munosabatlar va ularning 1000 ta tasodifiy xabarda bajarilish ulushi"))
P("Har bir munosabat ikkala variantda ham 1000 ta xabarning barchasida bajarildi. Masalan, 1-munosabat xesh qiymatning [0,4] va [1,5] elementlarining eng kichik bitlari doim teng ekanini bildiradi. Munosabatlar yutish o‘zgartirishidan mustaqil, chunki ular faqat oxirgi raunddagi Aralash matritsasi orqali hosil bo‘ladi. Bu kalitda L da nol satr yo‘q, shuning uchun doimiy bitlar kuzatilmadi; tasodifiy kalitlarning taxminan yarmida esa doimiy bitlar ham paydo bo‘ladi (asosiy hisobot, 1.5-bo‘lim).")
P("*Natija.* Kalitsiz rejimda k ochiq bo‘lgani uchun bu 8 ta munosabat hamma uchun ma’lum. Ular to‘liq xesh funksiyani tasodifiy funksiyadan bitta xesh qiymat bo‘yicha ajratishga imkon beradi: tasodifiy funksiya uchun 8 ta munosabatning hammasi bajarilishi ehtimolligi 2⁻⁸. SBZ bu xossani o‘zgartirmaydi.")

# ======================= DIFFERENSIAL =======================
PB(); H1('2. Differensial kriptotahlil xulosalari')
H2('2.1. Birinchi xulosa: yutishsiz raundlar MSB izlarini yuqori ehtimollik bilan o‘tkazadi')
XUL("1–7- va 10-raundlar MSB izlarini ≈0,85–0,94 ehtimollik bilan o‘tkazadi; differensial bardoshlilik faqat yutish nuqtalarida hosil bo‘ladi.")
D1=R['D1']
P("*Misol.* SBZ-256, A ilova kaliti; 1.1-bo‘limdagi yutishdan keyingi holat va undan holat[0,0] ning MSB biti bilan farq qiladigan ikkinchi holat (Δ = 80) olinadi. Ikkala holat bir xil kalit va blok bilan 1–10-raundlardan o‘tkaziladi va har bir akslantirishdan keyin ayirma kuzatiladi.")
rows=[["Raund, akslantirish","Δholat","Faol bayt (holat / kₑ)","Faqat MSB"]]
for q in D1['qadam']: rows.append([f"{q['raund']}: {opn[q['amal']]}",nl(q['dh']),f"{q['faol']} / {q['faol_ke']}","ha" if q['msb'] else "yo‘q"])
T([2600,3300,1900,1554],rows,cap("1- va 2-raundlar akslantirishlari bo‘yicha ayirmani kuzatish (SBZ-256)"),mono=(1,))
BL("*Aralash (1-raund).* Bitta MSB ayirmasi M(k₀) ning [0,0] ustunidagi birlar soniga teng, ya’ni 2 ta baytga tarqaldi: [1,0] va [2,0]. Bu ehtimollik 1 bilan sodir bo‘ladi, chunki 128·kₑ ≡ 128·(kₑ mod 2) (mod 256) va ko‘chirishlar yuzaga kelmaydi.")
BL("*Qo‘sh(holat, kₑ).* Faol baytlar juft (2 ta) bo‘lgani uchun J yig‘indisi o‘zgarmaydi (2·128 ≡ 0) va ayirma kₑ massiviga o‘tmaydi; har bir faol element uchun (x + 128)⁻¹ ≡ x⁻¹ + 128 bo‘lgani uchun MSB ayirmasi saqlanadi.")
BL("*SurHolat.* Faol baytlar [0,2] va [2,3] pozitsiyalariga ko‘chdi; ikkinchi Qo‘sh va TuzilmaKalit ayirmani o‘zgartirmadi.")
BL("*2-raund.* Aralash ayirmani 4 ta baytga tarqatdi, qolgan akslantirishlar uni yana MSB ko‘rinishida saqladi.")
xs=D1['xulosa']
T([2600]+[675]*10,[["Raund j"]+[str(r_['raund']) for r_ in xs],["Faol baytlar (holat)"]+[str(r_['faol']) for r_ in xs],["Faol baytlar (kₑ)"]+[str(r_['faol_ke']) for r_ in xs],["Faqat MSB"]+["ha" if r_['msb'] else "yo‘q" for r_ in xs]],cap("Misoldagi juftlik uchun raundlar oxiridagi holat"))
P("Ushbu juftlikda MSB izi ikki raund saqlandi va 3-raundda buzildi: ayirma kₑ massiviga o‘tdi (32 ta faol bayt) va quyi bitlarga tarqaldi. Bunga Qo‘sh o‘zgartirishidagi J, K yig‘indi va ko‘paytmalari hamda Δ tuzatmalari orqali massivlarning o‘zaro bog‘lanishi sabab bo‘ladi. Izning qancha saqlanishini statistik baholash uchun 3000 ta tasodifiy juftlikda xuddi shu tajriba takrorlandi:")
st=D1['stat']
T([2600]+[675]*10,[["Raund j"]+[str(j) for j in range(1,11)],["P(MSB izi saqlanadi)"]+[fz(v,3) for v in st]],cap("MSB izining saqlanish ehtimolligi (3000 juftlik, SBZ-256)"))
P(f"*Natija.* Har raundda iz ≈{fz(st[0],2)}–{fz(st[6]/st[5],2)} ehtimollik bilan saqlanadi, 7 raunddan keyin umumiy ehtimollik {fz(st[6],3)} ≈ 2^{math.log2(st[6]):.1f}. 8-raunddagi yutishda (SBZ) iz to‘liq buziladi; qolgan {fz(st[7],3)} ulush ayirmasi butunlay yo‘qolgan juftliklardir (2.4-bo‘lim). Demak, yutishsiz raundlar differensial bardoshlilikka deyarli hissa qo‘shmaydi.")

H2('2.2. Ikkinchi xulosa: SBZ yutish nuqtasidagi ehtimollikni 2⁻⁶ gacha kamaytiradi')
XUL("SBZ yutish nuqtasidagi maksimal ehtimollikni 0,156 (Standart-256) va 1 (Standart-128) dan 2⁻⁶ gacha kamaytiradi va bitta argumentdagi ayirmaning so‘nishini imkonsiz qiladi.")
D2=R['D2']
P(f"*Misol, 1-qadam: bitta argumentdagi ayirma.* A ilova ma’lumotlaridan h = {D2['h']:#04x} (yutishdan keyingi holat[0,0]) va n = {D2['n']:#04x} (2-blokning 0-bayti) olinadi va n ga MSB ayirmasi kiritiladi: n′ = {D2['n']^0x80:#04x}.")
T([3000,3177,3177],[["Variant","n uchun natija","n′ uchun natija / Δ"],
   ["Standart-256: Z(h) ‖ Z(n)",f"{D2['std'][0]:#04x}",f"{D2['std'][1]:#04x} / Δ = {D2['std'][0]^D2['std'][1]:#04x}"],
   ["SBZ: S(h ⊕ S(n))",f"{D2['sbz'][0]:#04x}",f"{D2['sbz'][1]:#04x} / Δ = {D2['sbz'][0]^D2['sbz'][1]:#04x}"]],cap("Yutish nuqtasida bitta argumentdagi ayirmaning o‘tishi"))
P("Standart-256 da ayirma faqat quyi yarim baytda qoladi (Δ = 06), yuqori yarim bayt h ga bog‘liq bo‘lgani uchun o‘zgarmaydi. Z jadvali lotin kvadrati ekani tekshirildi (har bir satr va ustun 0…15 ning o‘rin almashtirishi), shuning uchun faqat bitta yarim baytdagi ayirma bu yerda so‘nmaydi. SBZ da ayirma butun baytga tarqaldi (Δ = 3f).")
P(f"*2-qadam: so‘nish.* Z jadvali uchun ikkala yarim baytdagi ayirma so‘nishi mumkin: Z(x) = Z(x ⊕ 96) tengligi {D2['v96']}/256 kirishda bajariladi (masalan, x = {D2['v96_misol'][0]:#04x}: Z(x) = Z(x ⊕ 96) = {D2['v96_misol'][1]:#x}), ya’ni so‘nish ehtimolligi {D2['v96']}/256 = 0,156. SBZ uchun Δh = 0, Δn ≠ 0 bo‘lgan barcha 255·65536 juftlik tekshirildi: so‘nishlar soni {D2['sbz_sonish_bir']}. Ikkala argumentda ham ayirma bo‘lganda (Δh = Δn = 80) so‘nish {D2['sbz_sonish_80']}/65536 = 2⁻⁷ ehtimollik bilan sodir bo‘ladi. 128 bitli rejimdagi XOR da esa Δh = Δn bo‘lsa, ayirma ehtimollik 1 bilan so‘nadi.")
P(f"*Natija.* Yutish nuqtasidagi maksimal ehtimollik: XOR — 1, Z — {D2['Zmax']}/256 = 0,156, SBZ — 4/256 = 2⁻⁶. SBZ da holatdagi ayirmani (Δn = 0) yoki kirish blokidagi ayirmani (Δh = 0) yutish nuqtasida so‘ndirib bo‘lmaydi, bu kolliziya izlari uchun eng muhim cheklovdir.")

H2('2.3. Uchinchi xulosa: SBZ variantlari 8-raunddan keyin differensial chegaraga erishadi')
XUL("SBZ-256 va SBZ-128 birinchi iteratsiyaning 8-raundidan keyin differensial chegaraga (mos ravishda 2⁻¹²⁸ va 2⁻⁶⁴) erishadi; Standart-256 — 9-raunddan keyin; Standart-128 esa raundlar sonidan qat’i nazar bardoshli emas.")
D3=R['D3']
P("*Misol.* A ilova kaliti va xabari; 2-blokning 0- va 9-elementlariga MSB ayirmasi kiritiladi (256 bitli rejimda 80, 128 bitli rejimda 8). Juft sondagi MSB ayirmasi J yig‘indisini o‘zgartirmaydi, shuning uchun bu kolliziya hujumlari uchun eng qulay boshlang‘ich ayirma hisoblanadi. Ayirma to‘rttala variantda 9-raunddagi yutishgacha kuzatildi.")
lab={'256_std':'Standart-256','256_sbz':'SBZ-256','16_std':'Standart-128','16_sbz':'SBZ-128'}
rows=[["Variant","Qo‘sh (0-nuqta): faol","Yutishdan keyingi Δholat","1-raund: faol","8-nuqtada faol","9-nuqtada faol"]]
for k_,v in D3.items(): rows.append([lab[k_],str(v['faol_q0']),nl(v['dbz0']),str(v['r1']),str(v['a8']),str(v['a9'])])
T([1700,1350,2700,1100,1250,1254],rows,cap("Kirish blokidagi ikki elementli MSB ayirmasining yutish nuqtalarigacha o‘tishi"),mono=(2,))
P("Qadamlarning izohi:")
BL("*Qo‘sh (0-nuqta).* Barcha variantlarda holatda faol bayt yo‘q: ayirma faqat holatn ning ikki elementida 80 (8) ko‘rinishida qoladi; bu ehtimollik 1 bilan sodir bo‘ladi.")
BL("*Yutish (0-nuqta).* Standart-128 da XOR ayirmani o‘zgarishsiz holatga o‘tkazdi (8 va 8). Standart-256 da Z faqat quyi yarim baytda kichik ayirmalar berdi (3 va 1). SBZ-256 da ayirma butun baytlarga tarqaldi (ea va 74). SBZ-128 da juftlangan baytlar orqali 4 ta yarim baytga tarqaldi.")
BL("*1–7-raundlar.* Birinchi raunddayoq ayirma holatning 28–32 ta elementiga tarqaldi va 8-nuqtaga 28–32 ta faol element bilan yetib keldi.")
rows=[["Variant","Faol bayt boshiga maks. p","8-nuqtadan keyin log₂p ≤","8- va 9-nuqtalardan keyin log₂p ≤","Talab"]]
treb={'256_std':'−128','256_sbz':'−128','16_std':'−64','16_sbz':'−64'}
per={'256_std':'2⁻²·⁶⁸','256_sbz':'2⁻⁶','16_std':'1','16_sbz':'2⁻⁶ (bayt = 2 yarim bayt)'}
for k_,v in D3.items(): rows.append([lab[k_],per[k_],fz(v['chegara8'],1),fz(v['chegara89'],1),treb[k_]])
T([1800,2300,1800,2154,1300],rows,cap("Misoldagi faol elementlar asosida iz ehtimolligi chegaralari"))
P("*Natija.* Misoldagi faol elementlar bilan SBZ-256 da 8-nuqtadan keyingi chegara 2⁻¹⁸⁶, SBZ-128 da 2⁻⁸⁴ bo‘lib, ular talab qilingan 2⁻¹²⁸ va 2⁻⁶⁴ dan kichik; demak, SBZ variantlari 8-raunddan keyin bardoshli. Standart-256 da 8-nuqtadan keyin 2⁻⁸⁶ (talabdan katta), 9-nuqtadan keyin 2⁻¹⁷¹ — bardoshlilikka 9-raunddan keyin erishiladi. Standart-128 da XOR har bir faol yarim bayt uchun ehtimollik 1 beradi va chegara 0 bo‘lib qoladi.")

H2('2.4. To‘rtinchi xulosa: Aralash yadrosi orqali ayirma ehtimollik 1 bilan so‘nadi')
XUL("Aralash yadrosi orqali ayirmaning ehtimollik 1 bilan so‘nishi SBZ ga bog‘liq bo‘lmagan qoldiq xavf hisoblanadi; uni bartaraf etish uchun Aralash/TuzilmaKalit o‘zgartirishlarini qayta ko‘rib chiqish talab qilinadi.")
D4=R['D4']
s_,u_=D4['pozitsiya']
P(f"*Misol.* Tasodifiy kalitlar orasidan M(k₀) matritsasida nol ustun bo‘lgani topildi: k = {D4['kalit'][:32]}…; nol ustunlar: {', '.join(D4['nol_ustunlar'])}. Tanlangan pozitsiya holat[{s_},{u_}]. Shu ustunga mos kₑ[i,{u_}] qiymatlari: {', '.join(hex(v) for v in D4['kcol'])}; ularning hammasi juft.")
P(f"Aralash ning ta’rifiga ko‘ra holat[{s_},{u_}] elementi faqat kₑ ning {u_}-ustunidagi qiymatlarga ko‘paytiriladi. Ular juft bo‘lgani uchun 128·kₑ ≡ 0 (mod 256), ya’ni holat[{s_},{u_}] dagi MSB ayirmasi Aralash ning hech bir chiqishiga yetib bormaydi. Tasodifiy holat va undan holat[{s_},{u_}] ning MSB biti bilan farq qiladigan holat olinib, SBZ-256 da raundlardan o‘tkazildi:")
T([4677,4677],[["Kirish ayirmasi (Aralash dan oldin)","1-raund Aralash dan keyingi ayirma"],[nl([' '.join('80' if (i==s_ and j==u_) else '00' for j in range(8)) for i in range(4)]),nl(D4['d_aralash'])]],cap("Aralash yadrosidagi ayirmaning so‘nishi"),mono=(0,1))
P("10-raunddan keyingi holat va kₑ ayirmasi ham nolga teng: " + ("ha." if D4['oxir_nol'] else "yo‘q.") + " Shunday qilib, ikki xil holat bitta Aralash dan keyin bir xil holatga o‘tdi va keyingi barcha hisoblar bir xil bo‘ldi; bu ichki kolliziyadir. Asosiy hisobotdagi statistikaga ko‘ra tasodifiy kalitlarning taxminan yarmida M(k₀) da nol ustun bor, tasodifiy pozitsiyadagi bitta MSB ayirmasi 3,1% hollarda shu tarzda so‘nadi.")
P("*Natija.* So‘nish SBZ dan oldin, Aralash bosqichida ro‘y beradi, shuning uchun yutish o‘zgartirishini almashtirish bu hodisaga ta’sir qilmaydi. Buzg‘unchi uchun asosiy qiyinchilik yutish chiqishida aynan kerakli MSB ayirmasini hosil qilish (SBZ da bir bayt uchun ≈2⁻⁷·⁹); yadroning o‘zi esa ehtimollik 1 bilan ishlaydi. Shuning uchun Aralash/TuzilmaKalit ni diamatritsa 2 moduli bo‘yicha doim teskarilanuvchi bo‘ladigan qilib qayta loyihalash tavsiya etiladi.")

# ======================= ALGEBRAIK =======================
PB(); H1('3. Algebraik kriptotahlil xulosalari')
H2('3.1. Birinchi xulosa: yagona yuqori darajali element — yutish o‘zgartirishi')
XUL("Akslantirishlar ichida yagona yuqori darajali element — yutish nuqtasidagi o‘zgartirish: XOR — 1-daraja, Z — 6-daraja, SBZ — 13-daraja. Qo‘sh va Aralash bit darajasida T-funksiyalar bo‘lib, ularning 0-qatlami chiziqli.")
A1=R['A1']; dg=A1['deg']
P("*Misol, 1-qadam: yutish o‘zgartirishlarining darajalari.* Har bir akslantirishning chiqish bitlari uchun ANF (algebraik normal shakl) Möbius o‘zgartirishi orqali to‘liq hisoblandi:")
rows=[["Akslantirish","Kirish bitlari","Chiqish bitlarining darajalari"]]
for nm,lab_,nv in [('XOR','XOR (Standart-128)','8'),('Z','Z jadvali (8 → 4)','8'),('BaytZichlash_256','BaytZichlash (Standart-256, 16 → 8)','16'),('S','AES S-box','8'),('SBZ','SBZ (16 → 8)','16'),('Qosh_element','Qo‘sh elementi (holat[0,0], A ilova)','8')]:
    rows.append([lab_,nv,", ".join(str(v) for v in dg[nm])])
T([3800,1500,4054],rows,cap("Akslantirishlar chiqish bitlarining algebraik darajalari"))
P("*2-qadam: Qo‘sh elementi.* A ilova ma’lumotlaridagi holat[0,0] elementi uchun (1.1-bo‘limdagi parametrlar) 0- va 1-bitlar chiziqli (daraja 1): y₀ = x₀, y₁ = x₁ ⊕ x₀. 3- va 5-bitlar darajasi T-funksiya kutilganidek bit raqamiga teng. 2-, 4-, 6-, 7-bitlarda daraja 8 ga yetgan; bunga x⁻² ≡ 0 bo‘lganda A₂ + B₂ ga almashtirish qoidasi sabab bo‘ladi. Bu qoida 256 ta kirishdan bittasida ishlaydi va ANF ga to‘liq darajali «nuqtali» had qo‘shadi. Bu yuqori daraja kriptografik kuch bermaydi: funksiya qolgan 255 nuqtada past darajali funksiya bilan ustma-ust tushadi.")
P("*3-qadam: Aralash.* A ilova kaliti uchun holat′[0,0] ning 0-biti quyidagi chiziqli tenglama bilan aniqlanadi:")
F("h′[0,0]₀ = " + " ⊕ ".join(t_+"₀" for t_ in A1['aralash_tengl']) + ".")
P("Bu tenglama M(k₀) matritsasining birinchi satridan olindi va 1.1-bo‘limda 1-raund Aralash qadamida bajarilishi tekshirildi (32/32).")
P("*Natija.* Daraja 1 dan yuqori bo‘lgan yagona element yutish o‘zgartirishidir. SBZ bu elementning darajasini 6 (Z) va 1 (XOR) dan 13 gacha oshiradi; algoritmning qolgan qismi 0-qatlamda chiziqli bo‘lib qoladi.")

H2('3.2. Ikkinchi xulosa: tizim hajmini Qo‘sh belgilaydi, SBZ esa darajani oshiradi')
XUL("Raund tenglamalari tizimining hajmini Qo‘sh o‘zgartirishi belgilaydi (bir raundda ≈2,4·10⁵ ta o‘zgaruvchi, 256 bitli rejim); SBZ tizim hajmini amalda o‘zgartirmaydi, lekin uning darajasini oshiradi.")
A2=R['A2']; x=A2['x']
P(f"*Misol, 1-qadam: Qo‘sh tenglamalarini haqiqiy qiymatlarda tekshirish.* A ilova ma’lumotlari bo‘yicha 0-nuqtadagi Qo‘sh(holat, blok) uchun yig‘indilar va ko‘paytmalar hisoblandi: J₁h = Σ holat = {A2['J1h']}, J₁hn = Σ holatn = {A2['J1hn']}, K₁h = {A2['K1h']}. holat[0,0] = {x[0]:#04x} elementi uchun parametrlar: A₁ = J₁hn + 2·hn[0,0] + Δ = {A2['A1']}, B₁ = K₁h − 2·h[0,0] = {A2['B1']}, A₂ = {A2['A2']}, B₂ = {A2['B2']}, R = 200.")
rows=[["Bosqich","O‘zgaruvchilar","Tenglama","Qiymat (mod 256)"]]
rows.append(["1",f"x = {x[0]:#04x}, x⁻¹ = {x[1]:#04x}","x⁻¹·(B₁ + R·x) + A₁·x ≡ 0",str(A2['tekshiruv'][0])])
rows.append(["2",f"x⁻¹ = {x[1]:#04x}, x⁻² = {x[2]:#04x}","x⁻²·(B₂ + R·x⁻¹) + A₂·x⁻¹ ≡ 0",str(A2['tekshiruv'][1])])
rows.append(["3",f"x⁻² = {x[2]:#04x}, x⁻³ = {x[3]:#04x}","x⁻³·(B₂ + R·x⁻²) + A₂·x⁻² ≡ 0",str(A2['tekshiruv'][2])])
T([1100,3100,3500,1654],rows,cap("Qo‘sh o‘zgartirishining halqa tenglamalari (holat[0,0], A ilova ma’lumotlari)"))
P("Uchala tenglama ham aniq bajariladi; bular algebraik tizimdagi Qo‘sh ning element tenglamalaridir. Har bir tenglama kvadrat, lekin A va B parametrlari massivning barcha elementlari yig‘indisi va ko‘paytmasiga bog‘liq. Shuning uchun bitta element uchun tenglama J, K ni hisoblovchi 31 qo‘shish va 31 ko‘paytirish zanjiri bilan birga yoziladi; bu Qo‘sh ning tizimdagi ulushini katta qiladi.")
rows=[["Tizim qismi (256 bitli rejim)","O‘zgaruvchilar","Raunddagi ulushi"]]
tot=A2['raund']
for lab_,v in [("2 × Qo‘sh(holat, kₑ)",A2['qosh2']),("Aralash",A2['aralash']),("TuzilmaKalit",A2['tuz'])]:
    rows.append([lab_,f"{v:,}".replace(',',' '),fz(100*v/tot,1)+" %"])
rows.append(["Jami (bitta raund)",f"{tot:,}".replace(',',' '),"100 %"])
rows.append(["SBZ qatlami (32 bayt): o‘zg. / tengl.",f"{A2['sbz'][0]} / {A2['sbz'][1]}","—"])
rows.append(["Z qatlami (Standart-256): o‘zg. / tengl.",f"{A2['bz_std'][0]} / {A2['bz_std'][1]}","—"])
T([4554,2400,2400],rows,cap("Bitta raund tenglamalar tizimining tarkibi (bit darajasi, baho)"))
P("*Natija.* Raund tizimining 91,4 foizi Qo‘sh o‘zgartirishiga to‘g‘ri keladi. SBZ qatlami tizimga 512 ta o‘zgaruvchi va 2496 ta kvadrat tenglama qo‘shadi (Z qatlami uchun 256 ta o‘zgaruvchi va 3008 ta tenglama), ya’ni tizim hajmi deyarli o‘zgarmaydi. O‘zgaradigani — darajasi: SBZ qatlami 3.1-bo‘limda ko‘rsatilgan 13-darajali bog‘lanishni hosil qiladi.")

H2('3.3. Uchinchi xulosa: Standart-128 da 0-qatlam linearizatsiya hujumiga ochiq')
XUL("Standart-128 da 0-qatlam butun xesh davomida chiziqli: 80 ta so‘rov bilan 32 bitli bashorat 100% aniqlikda ishlaydi. SBZ bu hujumni to‘liq bartaraf etadi.")
A3=R['A3']
P("*Misol.* Buzg‘unchi kalitni bilmaydi (kalit — k ning birinchi 16 bayti), lekin bir blokli (16 baytli) xabarlar uchun kalitli xesh qiymatlarni oladi. 1.2-bo‘limga ko‘ra chiqish 0-qatlami xabar 0-qatlamining affin funksiyasi bo‘lishi kerak:")
F("o₀ = A·m₀ ⊕ c,     A — 32×32 noma’lum matritsa,  c — 32 bitli noma’lum vektor.")
P("Buzg‘unchi 80 ta tasodifiy xabar uchun (m₀, o₀) juftliklarini to‘playdi va har bir chiqish biti uchun 33 noma’lumli chiziqli tizimni Gauss usulida yechadi. Shundan keyin u 300 ta yangi xabar uchun chiqish 0-qatlamini bashorat qiladi.")
rows=[["Variant","32 bitning hammasi to‘g‘ri","Bitlar bo‘yicha to‘g‘ri","rang A"]]
for bz,lab_ in [('std','Standart-128'),('sbz','SBZ-128')]: rows.append([lab_,fz(A3[bz]['toliq'],3),fz(A3[bz]['bit'],3),str(A3[bz]['rangA'])])
T([2800,2400,2400,1754],rows,cap("Linearizatsiya hujumi natijasi (80 ta o‘quv, 300 ta sinov xabari)"))
rows=[["Variant","Xabar","Haqiqiy 0-qatlam","Bashorat"]]
for bz,lab_ in [('std','Standart-128'),('sbz','SBZ-128')]:
    for m_,a_,p_ in A3[bz]['misollar'][:2]: rows.append([lab_,m_,a_,p_])
T([1500,2850,2500,2504],rows,cap("Sinov xabarlari uchun bashorat misollari (32 bitli 0-qatlam)"),mono=(1,2,3))
P("Standart-128 da 300 ta sinov xabarining barchasida 32 bit xatosiz bashorat qilindi. SBZ-128 da xuddi shu tartibda tuzilgan affin model hech bir xabarda to‘liq to‘g‘ri chiqmadi: bitlar bo‘yicha aniqlik " + fz(A3['sbz']['bit'],3) + ". Bu qiymatning 0,5 dan biroz yuqori bo‘lishiga 1.5-bo‘limda ko‘rsatilgan chiqishdagi chiziqli munosabatlar sabab bo‘ladi.")
P("*Natija.* Standart-128 kalitli rejimda 80 ta so‘rovdan keyin buzg‘unchi istalgan xabar uchun autentifikatsiya kodining 32 bitini soxtalashtira oladi. A va c faqat kalitning 0-qatlamiga bog‘liq bo‘lgani uchun, kalitning 0-qatlami (30 bit) ham qolgan bitlardan alohida tiklanadi. SBZ 0-qatlamni 13-darajali bo‘g‘in orqali o‘tkazgani uchun bu hujumni to‘liq bartaraf etadi.")

H2('3.4. To‘rtinchi xulosa: SBZ variantlari algebraik chegaraga 0-nuqtadan keyinoq erishadi')
XUL("SBZ variantlari algebraik bardoshlilik chegarasiga 0-nuqtadagi yutishdan keyinoq erishadi, Standart-256 esa 1-raunddan keyin erishadi.")
A4=R['A4']; lc=A4['lc']
P(f"*Misol, 1-qadam: talab qilinadigan daraja.* Linearizatsiya murakkabligi (Σ_{{i≤d}} C(n, i))^2,8 formulasi bilan baholanadi. 128 bitli rejim uchun (n = 128) 2⁶⁴ dan oshish uchun d ≥ {A4['dmin128']} (2^{fz(lc['128_4'],1)}), 256 bitli rejim uchun (n = 256) 2¹²⁸ dan oshish uchun d ≥ {A4['dmin256']} (2^{fz(lc['256_8'],1)}) kerak.")
T([3500,1950,1950,1954],[["Yutish o‘zgartirishi","Daraja d","n = 128: log₂ murakkablik","n = 256: log₂ murakkablik"],
   ["XOR (Standart-128)","1",fz(lc['128_1'],1),fz(lc['256_1'],1)],["Z (Standart-256)","6",fz(lc['128_6'],1),fz(lc['256_6'],1)],["SBZ","13",fz(lc['128_13'],1),fz(lc['256_13'],1)]],cap("Yutish o‘zgartirishi darajasi bo‘yicha linearizatsiya murakkabligi"))
P("Jadvaldan: SBZ (13 ≥ 8 va 13 ≥ 4) ikkala rejimda 0-nuqtadagi yutishning o‘zidayoq talabni qanoatlantiradi; Z (6 < 8) 256 bitli rejimda yetarli emas va bardoshlilik keyingi raundlarda darajaning o‘sishiga tayanadi; XOR (1 < 4) talabni hech qachon qanoatlantirmaydi.")
P("*2-qadam: kub testi bilan tekshirish.* Xabarning 0-baytidagi 7 ta bit (d = 7) o‘zgaruvchi qilib olindi, qolgan bitlar A ilova qiymatlarida qoldirildi. 2⁷ = 128 ta xabar uchun 0-nuqtadan keyingi r raunddan so‘ng holat bitlarining XOR yig‘indisi hisoblandi. Agar bit darajasi 7 dan kichik bo‘lsa, yig‘indi albatta nol bo‘ladi.")
k_=A4['kub']
rows=[["Variant","r = 0: nol / jami (0-qatlam)","r = 1: nol / jami (0-qatlam)","r = 3: nol / jami (0-qatlam)"]]
for p_,lab_ in [('256_std','Standart-256'),('256_sbz','SBZ-256'),('16_std','Standart-128'),('16_sbz','SBZ-128')]:
    rows.append([lab_]+[f"{k_[f'{p_}_r{r}']['nol']}/{k_[f'{p_}_r{r}']['jami']} ({k_[f'{p_}_r{r}']['qatlam0_nol']}/32)" for r in (0,1,3)])
T([2350,2335,2335,2334],rows,cap("Kub testi (d = 7): yig‘indisi nol bo‘lgan chiqish bitlari"))
P("Standart-128 da 0-qatlamning 32 bitining hammasi barcha r da nol yig‘indi beradi: bu qatlam xabar bitlariga nisbatan chiziqli (daraja 1). SBZ-128 da esa 0-qatlamda nol bo‘lmagan yig‘indilar paydo bo‘ladi (r = 0 da 1 ta, r = 3 da 6 ta bit), ya’ni darajasi 7 dan kichik bo‘lmagan bitlar bor. 256 bitli rejimda ikkala variantda ham yig‘indisi nol bo‘lgan bitlar ulushi taxminan yarmini tashkil qiladi, bu tasodifiy funksiyadan kutilgan qiymat.")
P("*Natija.* SBZ yutish nuqtasidayoq kerakli darajani beradi. Standart-256 da Z ning 6-darajasi 256 bitli rejim uchun yetarli emas va bardoshlilik yuqori bitlar darajasining 1-raunddan keyin o‘sishiga tayanadi. Standart-128 ning 0-qatlami esa raundlar sonidan qat’i nazar chiziqli qoladi.")

PB(); H1('Xulosalar va misollar jamlanmasi')
rows=[["№","Xulosa (qisqa)","Asosiy dalil (misol)"]]
rows+= [["Ch-1","Yutishsiz raundlarda 0-qatlam c = 1","1–7-raundlarda Lʲ·h₀ bashorati 32/32; y₀ = x₀, y₁ = x₁ ⊕ x₀ — 256/256"],
 ["Ch-2","Standart-128 da 0-qatlam butun xesh bo‘yicha c = 1","5 iteratsiyaning 275 ta akslantirishida moslik 32/32; xesh 0-qatlami to‘liq bashorat qilindi"],
 ["Ch-3","Standart-256: c ≤ 2⁻² / faol bayt","Z approksimatsiyasi 160/256 (c = 0,25), algoritmda 0,254; A ilova kaliti — eng yomon kalit"],
 ["Ch-4","SBZ: c ≤ 2⁻⁶ / faol bayt","SBZ approksimatsiyasi 65536 juftlikda c = −2⁻⁶; odatiy kalitda 4-qatlamda 2⁻¹⁰⁸"],
 ["Ch-5","Chiqishdagi munosabatlar SBZ ga bog‘liq emas","8 ta munosabat ikkala variantda 1000/1000 xabarda bajarildi"],
 ["D-1","Yutishsiz raundlarda MSB izi ≈0,9 / raund","Misolda 2 raund saqlandi; 3000 juftlikda 7 raunddan keyin 0,335"],
 ["D-2","SBZ: maks. p = 2⁻⁶, bitta argument ayirmasi so‘nmaydi","255·65536 juftlikda so‘nishlar soni 0; Z da 0,156"],
 ["D-3","SBZ 8-raunddan keyin bardoshli","Misolda 8-nuqtadan keyin SBZ-256: 2⁻¹⁸⁶, SBZ-128: 2⁻⁸⁴, Standart-256: 2⁻⁸⁶"],
 ["D-4","Aralash yadrosi orqali so‘nish","Nol ustundagi MSB ayirmasi Aralash dan keyin 0; 10-raundgacha holatlar bir xil"],
 ["A-1","Yagona yuqori darajali element — yutish","Darajalar: XOR 1, Z 6, SBZ 13; Aralash tenglamasi h′[0,0]₀ = h[1,1]₀ ⊕ h[2,2]₀"],
 ["A-2","Tizim hajmini Qo‘sh belgilaydi","Qo‘sh tenglamalari A ilovada ≡ 0; raund tizimining 91,4 % i Qo‘sh"],
 ["A-3","Standart-128 linearizatsiyaga ochiq","80 so‘rovdan keyin 300/300 xabarda 32 bit to‘g‘ri; SBZ-128 da 0/300"],
 ["A-4","SBZ algebraik chegaraga 0-nuqtada erishadi","d = 13 ≥ 8; kub testida Standart-128 0-qatlami 32/32 nol, SBZ-128 da nol bo‘lmagan yig‘indilar"]]
T([900,3500,4954],rows,cap("Har bir xulosa va uni tasdiqlovchi misol"))
P("Barcha misollar *xulosalar_misollar.ipynb* daftarida bajarilgan va natijalari *misollar_natijalari.json* fayliga yozilgan. Daftar ilgari topshirilgan *uzmst285_tahlil* dastur paketining modullari (algoritm.py, komponentlar.py, differensial.py, algebraik.py) bilan bir papkada ishga tushiriladi.")
json.dump(B,open('blocks.json','w'),ensure_ascii=False); print(len(B), tc[0])
