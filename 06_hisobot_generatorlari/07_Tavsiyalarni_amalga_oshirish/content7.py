import json
T=json.load(open('/home/claude/ka/tavsiyalar_natijalari.json')); T4=json.load(open('/home/claude/ka/tavsiya4.json')); YK=json.load(open('/home/claude/ka/yakuniy.json')); Z=json.load(open('/home/claude/ka/tezlik_natijalari.json'))
B=[]; tc=[0]; fc=[0]
H1=lambda t:B.append(['h1',t]); H2=lambda t:B.append(['h2',t]); H3=lambda t:B.append(['h3',t])
P=lambda t:B.append(['p',t]); F=lambda t:B.append(['f',t]); BL=lambda t:B.append(['b',t]); PB=lambda:B.append(['pb'])
def Tb(w,rows,cap,mono=()): tc[0]+=1; B.append(['cap',f"{tc[0]}-jadval. {cap}"]); B.append(['t',w,rows,list(mono)])
def IMG(p,w,h,cap): fc[0]+=1; B.append(['img',p,w,h]); B.append(['fcap',f"{fc[0]}-rasm. {cap}"])
fz=lambda x,d=2:(f'{x:.{d}f}').replace('.',','); sg=lambda x:(('+' if x>0 else '')+fz(x,1)) if x!=0 else '0,0'
E=T['element']

B.append(['title','O‘zMSt 285:2024 1-ALGORITMINI TAKOMILLASHTIRISH BO‘YICHA TAVSIYALARNI AMALGA OSHIRISH VA ULARNING TEZLIKKA TA’SIRI'])
B.append(['sub','To‘rtta tavsiya: SBZ, Aralash/TuzilmaKalit, raund funksiyasining T-funksiya xossasi va yakuniy qatlam'])
H1('Kirish')
P("Standart algoritmning kriptotahlili natijasida to‘rtta tavsiya berilgan edi: (1) yutish nuqtasidagi BaytZichlash ni SBZ = S(h ⊕ S(n)) bilan almashtirish; (2) Aralash va TuzilmaKalit o‘zgartirishlarini diamatritsa 2 moduli bo‘yicha har doim teskarilanuvchi bo‘ladigan qilib qayta loyihalash; (3) raund funksiyasiga yuqori bitlarni quyi bitlarga o‘tkazuvchi element qo‘shib, T-funksiya xossasini yo‘qotish; (4) oxirgi raunddan keyin chiziqli bo‘lmagan yakuniy qatlam qo‘shish. Ushbu hujjatda har bir tavsiyani amalda qanday bajarish mumkinligi, uning kriptografik samarasi va cheklovlari, to‘rtta tavsiyaning birgalikdagi varianti hamda o‘zgarishlarning tezlikka ta’siri bayon etiladi. Birinchi tavsiyaning to‘rtta kriptotahlil usuli bo‘yicha batafsil tahlili «SBZ varianti kriptotahlili» hisobotida berilgan; bu yerda uning asosiy natijalari keltiriladi.")
P("Barcha natijalar ilova qilingan ikkita Jupyter daftarida olingan: *tavsiyalar_tahlili.ipynb* (kriptografik tekshiruvlar) va *tezlik_tahlili.ipynb* (tezlik o‘lchovlari, C va Python realizatsiyalari, amallar modeli). Daftarlar mustaqil ishlaydi va bajarilgan holda topshirilgan. Algoritmning barcha 12 ta varianti (ikki rejim × olti variant) uchun C va Python realizatsiyalari bir xil nazorat qiymatlarini beradi; standart va SBZ variantlari uchun ular standartning A ilovasidagi va SBZ materialidagi qiymatlar bilan mos keladi.")


# ===================== 1. 1-TAVSIYA =====================
PB(); H1('1. Birinchi tavsiya: BaytZichlash o‘rniga SBZ')
H2('1.1. Muammoning mohiyati')
P("Yutish nuqtasidagi BaytZichlash algoritmning yuqori bitlardagi axborotni quyi bitlarga o‘tkazuvchi yagona elementi, ya’ni yutishsiz raundlar T-funksiya bo‘lgani uchun butun algoritmning bardoshliligi aynan unga bog‘liq. Standartdagi ko‘rinishida u ikkala rejimda ham zaif:")
BL("256 bitli rejimda yangi bayt Z(h) ‖ Z(n) ko‘rinishida hosil bo‘ladi (Z — 8 → 4 jadval). Holat baytining axboroti faqat yuqori yarim baytga, holatn baytining axboroti faqat quyi yarim baytga tushadi (128 ta mumkin bo‘lgan bog‘liqlikdan 64 tasi); maksimal korrelyatsiya 0,25, maksimal differensial ehtimollik 40/256 = 0,156 va bu holatda ayirma butunlay so‘nadi; algebraik daraja 6.")
BL("128 bitli rejimda yutish oddiy XOR: chiziqli (c = 1), ayirmani o‘zgarishsiz o‘tkazadi va xabar ayirmasi bilan to‘liq kompensatsiya qilinadi, darajasi 1. Natijada Standart-128 to‘rttala kriptotahlil usulining hech biriga bardoshli emas: xesh qiymatning 32 bitli 0-qatlami xabar 0-qatlamining affin funksiyasi.")
H2('1.2. Taklif etilayotgan o‘zgartirish')
P("BaytZichlash AES (FIPS 197) S-boxiga asoslangan SBZ o‘zgartirishi bilan almashtiriladi:")
F("holat[i] ← S( h[i] ⊕ S( n[i] ) ),   i = 0, …, 31   (256 bitli rejim),")
P("bu yerda h — Qo‘sh dan keyingi holat bayti, n — holatn bayti. 128 bitli rejimda qo‘shni yarim baytlar juftlanadi: H = 16·h[2j] + h[2j+1], N = 16·n[2j] + n[2j+1], Q = S(H ⊕ S(N)), h[2j] = Q ≫ 4, h[2j+1] = Q ∧ 15. SBZ faqat uchta yutish nuqtasida (0-nuqta, 8- va 9-raund) qo‘llanadi, algoritmning qolgan qismi o‘zgarmaydi.")
H2('1.3. Akslantirish ko‘rsatkichlari')
Tb([3300,2000,2000,2054],[["Ko‘rsatkich (barcha 2¹⁶ kirish bo‘yicha)","BaytZichlash (256)","XOR (128)","SBZ"],["Maks. differensial ehtimollik","40/256 = 0,156","1","4/256 = 2⁻⁶"],["Bitta argument ayirmasining so‘nishi","0,156","0 (lekin kompensatsiya — 1)","0"],["Maks. |korrelyatsiya|","0,25","1","2⁻⁶"],["Algebraik daraja","6","1","13"],["Qat’iy ko‘chki mezoni (o‘rtacha)","0,266","0,125","0,503"],["Kirish–chiqish bog‘liqliklari","64/128","16/128","128/128"]],"Yutish o‘zgartirishlarining kriptografik ko‘rsatkichlari")
P("SBZ uchun korrelyatsiya va ayirmalar ehtimolligi S-box ko‘rsatkichlari orqali aniq ifodalanadi: c_SBZ((α, β) → γ) = c_S(α → γ)·c_S(β → α), DDT_SBZ((Δh, Δn), Δy) = Σ_d DDT_S(Δn, d)·DDT_S(Δh ⊕ d, Δy). Maksimal korrelyatsiya 2⁻⁶ atigi 6375 ta holatda (0,04%), maksimal ehtimollik 2⁻⁶ faqat Δn = 0 da erishiladi; Δn ≠ 0 da ehtimolliklar 2⁻⁸·⁶ … 2⁻⁷·⁶, ya’ni tekis taqsimotga yaqin. Faqat holatn orqali o‘tuvchi approksimatsiya mavjud emas va bitta argumentdagi ayirma hech qachon so‘nmaydi.")
H2('1.4. Algoritm bardoshliligiga ta’siri')
Tb([1900,1850,1850,1850,1904],[["Usul","Standart-256","SBZ-256","Standart-128","SBZ-128"],["Chiziqli (2⁻⁶⁴ / 2⁻³²)","≈18–19-raund","≈11-raund (4 qatlam)","bardoshli emas","4–6 qatlam"],["Differensial (2⁻¹²⁸ / 2⁻⁶⁴)","9-raunddan keyin","8-raunddan keyin","bardoshli emas","8-raunddan keyin"],["Algebraik","1-raunddan keyin","0-nuqtadan keyin","bardoshli emas","0-nuqtadan keyin"],["Integral (to‘liq xesh)","farqlovchi yo‘q","farqlovchi yo‘q","32 bitli farqlovchi","farqlovchi yo‘q (2¹⁶ to‘plam bilan ham)"]],"SBZ ning algoritm bardoshliligiga ta’siri (SBZ varianti kriptotahlili hisobotidan)")
P("SBZ eng katta samarani 128 bitli rejimda beradi: Standart-128 dagi barcha asosiy zaifliklar — 0-qatlamning butun xesh bo‘yicha chiziqliligi, 80 so‘rovli linearizatsiya hujumi (100% aniqlik), bit-qatlamlar bo‘yicha ajralish (2⁴⁸ kolliziya) va to‘liq xesh integral farqlovchisi — SBZ-128 da kuzatilmaydi. Tezlikka ta’siri sezilmaydi: SBZ Z jadvali bilan bir xil sondagi jadval murojaatini talab qiladi (C da farq ±1% atrofida, o‘lchov shovqini doirasida).")
Tb([2200,7154],[["Variant","Nazorat qiymati (A ilova kaliti va xabari)"],["SBZ-256","42f97daaa8e7010bc629ca695eaa77df7ae7443a0c3ae78d205c2e025d256c96"],["SBZ-128","bd745e2ed572ea4246ed68482ef46c5e"]],"SBZ variantining nazorat qiymatlari",mono=(1,))
H2('1.5. Cheklovlar')
BL("SBZ yutishsiz raundlarning T-funksiya xossasiga ta’sir qilmaydi: 1–7-raundlarda 0-qatlam chiziqli, MSB izlari ≈0,9 ehtimollik bilan saqlanadi — buni 3-tavsiya bartaraf etadi.")
BL("Aralash degeneratsiyasidan kelib chiqadigan xossalar (chiqishdagi ≈6 ta doimiy munosabat, doimiy bitlar, ≈3% ichki kolliziya, «eng yomon» kalitlar) SBZ bilan saqlanadi — buni 2-tavsiya bartaraf etadi.")

# ===================== 1. 2-TAVSIYA =====================
PB(); H1('2. Ikkinchi tavsiya: Aralash va TuzilmaKalit')
H2('2.1. Muammoning mohiyati')
P("Aralash holatning har bir 4×4 yarmini raund kaliti kₑ ning mos yarmiga diamatritsa qoidasi bo‘yicha 2ⁿ moduli bo‘yicha ko‘paytiradi. Belgilangan kₑ da bu Z/2ⁿ halqasi ustidagi chiziqli akslantirish. Halqa ustidagi chiziqli akslantirish faqat uning aniqlovchisi toq, ya’ni 2 moduli bo‘yicha ko‘rinishi teskarilanuvchi bo‘lgandagina teskarilanuvchi bo‘ladi. 2 moduli bo‘yicha ko‘rinish M(k₀) esa faqat kₑ elementlarining juft/toqligiga bog‘liq.")
P("Hozirgi TuzilmaKalit kₑ ning juft/toqligini kalit k ning juft/toqligiga tenglashtiradi, shuning uchun M(k₀) kalitga bog‘liq va kalitlarning ≈99 foizida teskarilanmaydi. Bundan uchta kamchilik kelib chiqadi: xesh qiymatning 0-qatlamida korrelyatsiyasi 1 bo‘lgan chiziqli munosabatlar (o‘rtacha ≈6 ta) va doimiy bitlar; M(k₀) yadrosidagi ayirmalarning ehtimollik 1 bilan so‘nishi (ichki kolliziyalar); chiziqli izlar uchun «eng yomon» kalitlar. Standartning 5.1.2-bandi ham kₑ ning kvadrat qismlari teskarilanuvchi bo‘lishini talab qiladi, lekin shartni «aniqlovchi noldan farqli» deb ifodalaydi; 2ⁿ moduli uchun to‘g‘ri shart — aniqlovchining toq bo‘lishi.")
H2('2.2. Juft/toqlik naqshlarini tahlil qilish')
P("M(K) matritsasi K ning juft/toqlik bitlariga nisbatan chiziqli (diamatritsa ko‘paytmasi bichiziqli), shuning uchun har bir 4×4 yarim uchun barcha 2¹⁶ = 65536 ta juft/toqlik naqshi uchun 16×16 matritsa tez quriladi. Har bir naqsh uchun GF(2) dagi rang va teskarilanuvchi naqshlar uchun tarmoqlanish soni — min (wt(x) + wt(M·x)), x ≠ 0 — barcha 2¹⁶ vektor bo‘yicha hisoblandi.")
nq=T['naqsh']
Tb([4677,4677],[["Ko‘rsatkich","Qiymat"],["Teskarilanuvchi naqshlar",f"{nq['teskarilanuvchi']} / 65536 ({fz(100*nq['teskarilanuvchi']/65536,1)}%)"]]+[[f"Tarmoqlanish soni {k}",f"{v} ta naqsh"] for k,v in nq['taqsimot'].items()]+[["Eng katta tarmoqlanishli naqsh","0xFFFF — barcha elementlar toq"]],"4×4 yarim uchun juft/toqlik naqshlari tahlili")
P("Natija juda aniq: tarmoqlanish soni 6 bo‘lgan yagona naqsh — kₑ ning barcha elementlari toq bo‘lgan holat. Qolgan teskarilanuvchi naqshlarning tarmoqlanish soni 2–4 ga teng. Toq son 2ⁿ moduli bo‘yicha doim teskarilanuvchi bo‘lgani uchun bu tanlov algebraik jihatdan ham tabiiy.")
H2('2.3. Taklif etilayotgan o‘zgartirish')
P("TuzilmaKalit o‘zgartirishi quyidagi qoida bilan almashtiriladi:")
F("kₑ[s,u] ← kₑ[s,u] ∨ 1   (0 ≤ s < 4, 0 ≤ u < 8),")
P("ya’ni juft element 1 ga oshiriladi, toq element o‘zgarmaydi. Hozirgi «k bilan bir xil juftlik» sharti va «kₑ ≡ 0 bo‘lsa 2» qoidasi kerak bo‘lmay qoladi, chunki toq son nolga teng bo‘lmaydi. Birinchi raunddagi Aralash TuzilmaKalit dan oldin bajarilgani uchun iteratsiyalardan oldin ham kₑ ← k ∨ 1 qo‘llanadi. Qo‘sh o‘zgartirishidagi R = k[0] parametri o‘zgarmaydi va avvalgidek juft bo‘lishi kerak (u kₑ dan emas, k dan olinadi). Aralash ning formulasi o‘zgarmaydi.")
H2('2.4. Tekshiruv natijalari')
L=T['L_toq']; ch=T['chiqish']; so=T['sonish']
Tb([3600,2877,2877],[["Ko‘rsatkich","Hozirgi algoritm","Toq kₑ"],
 ["L = P·M matritsasi rangi","kalitga bog‘liq, o‘rtacha ≈26",f"{L['rang']} (barcha kalitlar uchun)"],
 ["Xesh 0-qatlami vektorlari rangi (256), 3 kalit",", ".join(map(str,ch['256_0']['rang'])),", ".join(map(str,ch['256_1']['rang']))],
 ["Xesh 0-qatlami vektorlari rangi (128), 3 kalit",", ".join(map(str,ch['16_0']['rang'])),", ".join(map(str,ch['16_1']['rang']))],
 ["Chiqish bitlari chastotasi (256)",f"{fz(ch['256_0']['chastota'][0],3)} … {fz(ch['256_0']['chastota'][1],3)}",f"{fz(ch['256_1']['chastota'][0],3)} … {fz(ch['256_1']['chastota'][1],3)}"],
 ["MSB ayirmasining so‘nishi (256 / 128)",f"{fz(100*so['256_0']['nol'][0],1)}% / {fz(100*so['16_0']['nol'][0],1)}%","0% / 0%"],
 ["Faol baytlar, 1–6 yutish qatlami (mediana)",", ".join(fz(v,1).replace(',0','') for v in L['zanjir_hozirgi_med']),", ".join(map(str,L['zanjir_toq']))],
 ["Faol baytlar, 1–6 yutish qatlami (eng yomon kalit)",", ".join(map(str,L['zanjir_hozirgi_min'])),", ".join(map(str,L['zanjir_toq']))]],
 "Ikkinchi tavsiya: hozirgi va o‘zgartirilgan algoritmni taqqoslash")
P("Hozirgi algoritmda xesh 0-qatlami vektorlari 22–30 o‘lchamli fazoda yotadi (ya’ni 2–10 ta doimiy chiziqli munosabat bor), ayrim bitlar doim nolga teng (chastota 0,000). Toq kₑ bilan rang barcha kalitlarda 32 ga teng, doimiy bitlar yo‘q. MSB ayirmasining Aralash yadrosi orqali so‘nishi butunlay yo‘qoladi. Faol baytlar zanjiri kalitga bog‘liq bo‘lmay qoladi va hozirgi mediana qiymatlaridan ham katta: 4 ta yutish qatlamida 24 ta, 5 ta qatlamda 43 ta faol bayt. Bu Standart-256 uchun 5 ta qatlamda |c| ≤ 2⁻⁸⁶, SBZ bilan 4 ta qatlamda |c| ≤ 2⁻¹⁴⁴ chegarasini beradi; «eng yomon kalitlar» muammosi yo‘qoladi.")
H2('2.5. Cheklovlar')
BL("Kalitli (128 bitli) rejimda kalitning 32 ta eng kichik biti algoritmga ta’sir qilmay qoladi va kalit formal ravishda 96 bitga qisqaradi. Hozirgi algoritmda bu bitlar qolganlaridan alohida 2³⁰ ta urinishda tiklanadi, shuning uchun amaldagi xavfsizlik deyarli o‘zgarmaydi; lekin standartda kalit uzunligini shunga mos ko‘rsatish yoki bu bitlarni boshqa joyda (masalan, boshlang‘ich holatda) ishlatish kerak. 256 bitli rejim standartga ko‘ra kalitsiz.")
BL("Qo‘sh dagi «x⁻² ≡ 0 bo‘lsa A₂ + B₂» qoidasi element akslantirishini bijeksiya bo‘lmagan qiladi (256 kirishdan 255 xil chiqish); bu juda kichik ehtimollik bilan ichki kolliziyalarga olib kelishi mumkin. Ushbu tajribada (3000 juftlik) so‘nish kuzatilmadi, boshqa tajribada 256 bitli rejimda 0,07% qayd etilgan. To‘liq bartaraf etish uchun bu qoidani ham bijektiv qilish kerak.")
BL("Raund funksiyasi T-funksiyaligicha qoladi: MSB izi hamon har raundda ≈0,9 ehtimollik bilan saqlanadi (256 bitli rejimda 7 raunddan keyin " + fz(so['256_1']['msb'][6],2) + "). Bu kamchilikni uchinchi tavsiya bartaraf etadi.")

# ===================== 2. 3-TAVSIYA =====================
PB(); H1('3. Uchinchi tavsiya: raund funksiyasining T-funksiya xossasini yo‘qotish')
H2('3.1. T-funksiya va uning oqibatlari')
P("T-funksiya — natijaning j-biti kirishlarning faqat 0…j-bitlariga bog‘liq bo‘lgan akslantirish. 2ⁿ moduli bo‘yicha qo‘shish, ayirish, ko‘paytirish va teskarilash T-funksiyalar, chunki ko‘chirish faqat yuqoriga tarqaladi. 1-algoritmning yutishsiz raundlari (Aralash, Qo‘sh, SurHolat, SurKalit, TuzilmaKalit) T-funksiyadir: SurHolat elementlarni joyidan ko‘chiradi, lekin bitlarni bayt ichida siljitmaydi. Natijada 0-qatlam raundlarda chiziqli tenglama bilan aniq kuzatiladi, MSB ayirmalari quyi bitlarga o‘tmaydi, 0-qatlam darajasi 1 bo‘lib qoladi va integral to‘plamlarda balanslanadi. Buni tuzatish uchun raund ichiga yuqori bitlarni quyi bitlarga o‘tkazuvchi element qo‘shish kerak.")
H2('3.2. Tanlangan elementlar va ularning joylashuvi')
P("Element har bir raundda SurHolat dan keyin, ikkinchi Qo‘sh dan oldin, holat massivining har bir elementiga qo‘llanadi:")
F("Aralash → Qo‘sh(holat, kₑ) → SurHolat, SurKalit → E(holat) → Qo‘sh(holat, kₑ) → TuzilmaKalit")
Tb([2700,3327,3327],[["Element E","256 bitli rejim (bayt)","128 bitli rejim (yarim bayt)"],["Davriy aylantirish","x ← x ⋘ 3","x ← x ⋘ 1"],["XOR-surish","x ← x ⊕ (x ≫ 4)","x ← x ⊕ (x ≫ 2)"],["S-box qatlami","x ← S(x), AES S-box","x ← S₄(x), PRESENT S-box"]],"Tekshirilgan elementlar")
P("Uchala element ham bijeksiya, shuning uchun yangi kolliziyalar keltirib chiqarmaydi. Element faqat holatga qo‘llanadi, kₑ ga emas, shuning uchun ikkinchi tavsiyadagi toq kₑ sharti saqlanadi.")
H2('3.3. Baholash ko‘rsatkichlari')
BL("0-qatlam raund tenglamasi h₀ ← L·h₀ ning korrelyatsiyasi (600 kalit) — chiziqli tahlil;")
BL("bitta raunddan keyingi eng yaxshi «bitta kirish biti → bitta chiqish biti» korrelyatsiyasi (6000 namuna; shovqin chegarasi 0,058) — chiziqli tahlil;")
BL("MSB izining saqlanish ehtimolligi (2000 juftlik) — differensial tahlil;")
BL("qat’iy ko‘chki mezoni (SAC): bitta kirish biti o‘zgarganda har bir chiqish bitining o‘zgarish ehtimolligi, 1 va 2 raunddan keyin; o‘rtacha qiymat (ideal 0,5) va bog‘liqligi umuman yo‘q (kirish, chiqish) juftliklari ulushi — algebraik va differensial tarqalish;")
BL("MSB ning 0-bitga ta’siri (SAC ning tegishli qismi) — T-funksiya xossasining buzilishi;")
BL("integral: bitta faol bayt bo‘yicha 0-qatlam XOR yig‘indisining nol bo‘lish ulushi (60 tajriba; tasodifiy funksiya uchun 0,5);")
BL("hisoblash vaqti (Python, 2000 blok, 10 raund).")
H2('3.4. Natijalar')
def erow(p):
    rows=[["Ko‘rsatkich","Hozirgi","Aylantirish","XOR-surish","S-box"]]
    ks=[f'{p}_{n}' for n in ('yoq','aylantirish','xor_surish','sbox')]
    rows.append(["0-qatlam tenglamasi c, 1 / 2 / 3-raund"]+[" / ".join(fz(v,2) for v in E[k]['qatlam0_c'][:3]) for k in ks])
    rows.append(["Bitta raund: bit → bit |c|"]+[fz(E[k]['bit_bit'],3) for k in ks])
    rows.append(["MSB izi: 1 / 2-raund"]+[" / ".join(fz(v,3) for v in E[k]['msb_izi'][:2]) for k in ks])
    rows.append(["SAC, 1 raund: o‘rtacha / bog‘liqsiz"]+[f"{fz(E[k]['sac1']['ortacha'],3)} / {fz(100*E[k]['sac1']['nol'],1)}%" for k in ks])
    rows.append(["SAC, 2 raund: o‘rtacha / bog‘liqsiz"]+[f"{fz(E[k]['sac2']['ortacha'],3)} / {fz(100*E[k]['sac2']['nol'],1)}%" for k in ks])
    rows.append(["MSB → 0-bit ta’siri: 1 / 2 raund"]+[f"{fz(E[k]['msb_0bit1'],3)} / {fz(E[k]['msb_0bit2'],3)}" for k in ks])
    rows.append(["Integral 0-qatlam nol ulushi: 1 / 2 / 3-raund"]+[" / ".join(fz(v,2) for v in E[k]['integral0']) for k in ks])
    rows.append(["Vaqt, s (Python)"]+[fz(E[k]['vaqt'],3) for k in ks])
    return rows
Tb([2954,1600,1600,1600,1600],erow(256),"Uchinchi tavsiya: 256 bitli rejim")
Tb([2954,1600,1600,1600,1600],erow(16),"Uchinchi tavsiya: 128 bitli rejim")
P("Natijalarning izohi. Hozirgi algoritmda 0-qatlam tenglamasi har raundda korrelyatsiya 1 bilan bajariladi, MSB izi 1-raundda 0,94 ehtimollik bilan saqlanadi, SAC matritsasining 12–24 foizi nol (ko‘plab chiqish bitlari ayrim kirish bitlariga umuman bog‘liq emas), MSB 0-bitga hech qachon ta’sir qilmaydi va 0-qatlam integral to‘plamda doim balanslangan. Har uchala element qo‘shilganda 0-qatlam tenglamasining korrelyatsiyasi birinchi raunddayoq shovqin darajasiga tushadi, «bit → bit» bog‘lanish shovqin chegarasigacha kamayadi, MSB izi 0,03 ga tushadi (qolgan qism — Aralash yadrosi orqali so‘nish, uni ikkinchi tavsiya yo‘qotadi), 2 raunddan keyin SAC ideal qiymatga (≈0,5) yetadi va bog‘liqsiz juftliklar qolmaydi, integral balans 1-raundda qisman, 2-raunddan boshlab to‘liq yo‘qoladi. Hisoblash vaqti amalda o‘zgarmaydi.")
H2('3.5. Elementni tanlash')
P("S-box qatlami tavsiya etiladi. Davriy aylantirish va XOR-surish T-funksiya xossasini buzadi, lekin o‘zlari GF(2) ustida chiziqli, ya’ni chiziqli bo‘lmaganlikni faqat modul arifmetikasi beradi. S-box esa har bir faol bayt uchun kafolatlangan chegaralar beradi (AES S-box: korrelyatsiya ≤ 2⁻³, differensial ehtimollik ≤ 2⁻⁶). Bu raundlar bo‘yicha faol S-box larni sanash orqali isbotlanadigan baholarni olish imkonini beradi. S-box bir raundda MSB ni 0-bitga eng kuchli o‘tkazadi (256 bitli rejimda 0,14, boshqa elementlarda ≈0,01) va 1 raunddan keyingi SAC ning minimal qiymati ham eng yuqori. 256 bitli rejimda SBZ dagi AES S-box jadvali qayta ishlatiladi, ya’ni qo‘shimcha jadval talab qilinmaydi. 128 bitli rejim uchun har qanday optimal 4 bitli S-box (differensial bir xillik 4, maksimal korrelyatsiya 2⁻¹) mos keladi; tekshiruvda PRESENT S-box ishlatildi. Milliy standartlar bilan muvofiqlik uchun O‘zMSt 270 almashtirish uzellaridan foydalanish ham mumkin, lekin ular shu mezonlar bo‘yicha alohida tekshirilishi kerak.")

# ===================== 3. BIRLASHGAN =====================

# ===================== 4. 4-TAVSIYA =====================
PB(); H1('4. To‘rtinchi tavsiya: yakuniy qatlam')
H2('4.1. Muammoning mohiyati')
BL("10-raund oxirgi yutish nuqtasidan keyin bajariladi va T-funksiya. Shuning uchun xesh qiymatning 0-qatlami L·x₀ ko‘rinishida: chiqishda doimiy chiziqli munosabatlar (o‘rtacha ≈6 ta) va doimiy bitlar, Standart-128 da esa 0-qatlam to‘liq chiziqli.")
BL("Bloklar orasida oldinga uzatish (feed-forward) yo‘q. 2- va 3-tavsiyalar qo‘llanganda bitta blok ishlovi holat bo‘yicha bijeksiyaga aylanadi, ya’ni xesh qiymatdan orqaga hisoblash va «o‘rtada uchrashish» tipidagi proobraz hujumlari imkoniyati paydo bo‘ladi.")
BL("Boshlang‘ich vektor yo‘q: boshlang‘ich holat — xabarning birinchi bloki, uni buzg‘unchi erkin tanlaydi.")
H2('4.2. Ochiq qaytariladigan qatlam yordam bermaydi')
P("Oxiriga ochiq bijektiv qatlam qo‘shilsa (masalan, chiqish = S(H)), buzg‘unchi S⁻¹ ni qo‘llab H ni to‘liq tiklaydi va barcha tuzilmaviy munosabatlar saqlanadi. Tekshiruvda S⁻¹ dan keyingi 0-qatlam rangi Standart-256 da 27, SBZ-256 da 21–25 chiqdi va doimiy bitlar saqlandi (4.4-bo‘lim jadvali). Demak, yakuniy qatlam qaytarib bo‘lmaydigan bo‘lishi kerak; buning oddiy usuli — natijani kirish bilan XOR qilish (oldinga uzatish).")
H2('4.3. Taklif etilayotgan o‘zgartirish')
P("Yakuniy qatlam ikki qismdan iborat:")
F("1) har bir blokdan keyin oldinga uzatish:  holatᵢ = F(holatᵢ₋₁, blokᵢ) ⊕ holatᵢ₋₁  (Davies–Meyer tarzida);")
F("2) chiqish o‘zgartirishi:  h(M) = P(H) ⊕ H,   P = Bog‘lash(Bog‘lash(H, C₁), C₂),  R = C8₁₆.")
P("Bu yerda F — bitta iteratsiya (10 raund), H — oxirgi holat, C₁, C₂ — doimiy toq konstantalar. Bog‘lash — Qo‘sh o‘rniga taklif etilgan bayt darajasidagi bijektiv akslantirish (holatning chap va o‘ng yarimlari ustida Feistel tarzidagi uchta yarim qadam, har birida parametrli Möbius ko‘paytmasi va AES S-box); u ikkala rejimda bir xil ishlaydi. Agar Bog‘lash qabul qilinmasa, P sifatida doimiy toq kalitli Aralash, S-box qatlami va SurHolat dan iborat ikki raund ishlatilishi mumkin. Oldinga uzatish blokka 32 ta XOR, chiqish o‘zgartirishi esa butun xabar uchun bir marta ikkita Bog‘lash chaqiruvini (≈0,26 mkS) talab qiladi.")
H2('4.4. Tekshiruv natijalari')
P("Har bir variant uchun to‘rtta ko‘rsatkich o‘lchandi: xesh qiymatlar 0-qatlamining rangi (300 xabar, 3 ta kalit; 32 dan kichik bo‘lsa, doimiy munosabatlar bor), eng kam o‘zgaradigan bitning chastotasi (0 — doimiy bit), 0-qatlamning affin modeli bo‘yicha bashorat aniqligi (80 ta xabar bo‘yicha qurilib, 200 ta yangi xabarda tekshirildi; ideal 0,5) va bitta faol bayt bo‘yicha 0-qatlamda doim balanslangan bitlar soni (10 tajriba).")
rows=[["Variant","Yakuniy qatlamsiz","Ochiq S (S⁻¹ bilan)","Faqat P(H) ⊕ H","Faqat oldinga uzatish","Ikkalasi birga"]]
for key,lab in (('256_std','Standart-256'),('16_std','Standart-128'),('256_sbz','SBZ-256'),('16_sbz','SBZ-128')):
    cells=[]
    for rj in ('yoq','S','Omega','DM','DM+Omega'):
        d=YK.get(f'{key}_{rj}')
        cells.append("—" if d is None else f"{min(d['rang'])}–{max(d['rang'])} / {fz(d['min_chastota'],2)} / {fz(d['affin_0'],2)} / {d['integral_0']}")
    rows.append([lab]+cells)
Tb([1554,1560,1560,1560,1560,1560],rows,"Yakuniy qatlam variantlari: rang / min. chastota / affin model / integral")
P("Faqat P(H) ⊕ H chiqish darajasidagi barcha kamchiliklarni (doimiy munosabatlar, doimiy bitlar, affin model, integral farqlovchi) yo‘qotadi — hatto Standart-128 da ham. Faqat oldinga uzatish doimiy munosabatlar va doimiy bitlarni yo‘qotadi, lekin XOR chiziqli bo‘lgani uchun Standart-128 dagi 0-qatlam chiziqliligi saqlanadi (affin model 1,00, integral 32). Ikkalasi birga barcha variantlarda barcha ko‘rsatkichlarni ideal darajaga keltiradi.")
Tb([2200,7154],[["Variant (yakuniy qatlam bilan)","Nazorat qiymati (A ilova kaliti va xabari)"],["Standart-256","68d366250892b00aaa0110fe612473cf4f9dac6b4e43034facabe63abea07079"],["SBZ-256","09c4feb63dc88817bbabc6205ce8a5037a1f6941f9177e6b2fa2a97a5b4f8c2f"],["Standart-128","f61fbc30c5d417d8689053faecccbd55"],["SBZ-128","452e53b21f3b46f2ccfe2dc961aaa72d"]],"Oldinga uzatish va P(H) ⊕ H qo‘shilgan variantlarning nazorat qiymatlari",mono=(1,))
H2('4.5. Cheklovlar')
BL("Yakuniy qatlam faqat oxirgi himoya chizig‘i: agar ikki xabar ichki holatda bir xil H ga olib kelsa, P(H) ⊕ H ham bir xil. Shuning uchun Standart-128 dagi 2⁴⁸ murakkablikdagi kolliziya hujumi, raundlarning T-funksiya xossasi va Aralash yadrosi orqali ichki kolliziyalar yakuniy qatlam bilan bartaraf etilmaydi — ular uchun 1–3-tavsiyalar kerak.")
BL("Kalitli rejimda kalitni chiqish o‘zgartirishiga ham kiritish mumkin: h = P(H ⊕ K) ⊕ H (HMAC dagi «tashqi o‘ram» g‘oyasi).")

PB(); H1('5. Barcha to‘rtta tavsiya birgalikda')
H2('5.1. Algoritmdagi o‘zgarishlar jamlanmasi')
Tb([2600,3377,3377],[["Akslantirish","Standart","Taklif etilgan variant"],
 ["Yutish (0-, 8-, 9-nuqtalar)","BaytZichlash: Z(h) ‖ Z(n) (256) yoki h ⊕ n (128)","SBZ: S(h ⊕ S(n)); 128 bitli rejimda qo‘shni yarim baytlar juftlanadi"],
 ["TuzilmaKalit","kₑ juftligi k juftligiga tenglashtiriladi; kₑ ≡ 0 → 2","kₑ ← kₑ ∨ 1 (barcha elementlar toq)"],
 ["Iteratsiyalardan oldin","kₑ ← k","kₑ ← k ∨ 1"],
 ["Raund ichida (SurHolat dan keyin)","—","holat ← S(holat) (256) yoki S₄(holat) (128)"],
 ["Bloklar orasida","—","oldinga uzatish: holatᵢ = F(holatᵢ₋₁, blokᵢ) ⊕ holatᵢ₋₁"],
 ["Chiqish","oxirgi holat","h(M) = P(H) ⊕ H, P = Bog‘lash(Bog‘lash(H, C₁), C₂)"],
 ["Aralash, Qo‘sh, SurHolat, SurKalit, raundlar soni, uzunlik va NY bloklari","—","o‘zgarishsiz"]],"To‘rtta tavsiya qo‘llanilgan variantdagi o‘zgarishlar")
H2('5.2. Bitta iteratsiya psevdokodi')
code=["kₑ ← kₑ ∨ 1","(h̃, ñ) ← Qo‘sh(holat, blok);  holat ← SBZ(h̃, ñ)","For j = 1 to 10","    holat ← Aralash(holat, kₑ)","    (holat, kₑ) ← Qo‘sh(holat, kₑ)","    holat ← SurHolat(holat);  kₑ ← SurKalit(kₑ)","    holat ← S(holat)                      // yangi: S-box qatlami","    If j = 8: (h̃, ñ) ← Qo‘sh(holat, blok); holat ← SBZ(h̃, ñ)","    Else:     (holat, kₑ) ← Qo‘sh(holat, kₑ)","    kₑ ← kₑ ∨ 1                            // yangi TuzilmaKalit","    If j = 9: (h̃, ñ) ← Qo‘sh(holat, blok); holat ← SBZ(h̃, ñ)","End For"]
Tb([9354],[["Psevdokod"],["\n".join(code)]],"Taklif etilgan variantning bitta iteratsiyasi (F)",mono=(0,))
code2=["holat ← M₁;  kₑ ← k","For har bir keyingi kirish bloki Bᵢ (M₂, …, M_b, uzunlik, NY)","    H₀ ← holat","    (holat, kₑ) ← F(holat, Bᵢ, kₑ)","    holat ← holat ⊕ H₀                       // 4-tavsiya: oldinga uzatish","End For","h(M) ← Bog‘lash(Bog‘lash(holat, C₁), C₂) ⊕ holat   // 4-tavsiya: chiqish o‘zgartirishi"]
Tb([9354],[["Psevdokod"],["\n".join(code2)]],"Xesh qiymatni hisoblash (to‘rtta tavsiya bilan)",mono=(0,))
H2('5.3. Nazorat qiymatlari')
P("A ilova kaliti va 64 baytli xabari uchun barcha variantlarning nazorat qiymatlari quyidagi jadvalda keltirilgan. Ular C va Python realizatsiyalarida bir xil chiqdi; standart va SBZ qiymatlari standartning A ilovasi va SBZ materiali bilan mos keladi.")
lab={'std_0_0':'Standart','sbz_0_0':'SBZ','std_1_0':'Standart + toq kₑ','std_0_1':'Standart + S-qatlam','sbz_1_0':'SBZ + toq kₑ','sbz_1_1':'SBZ + toq kₑ + S-qatlam'}
rows=[["Rejim","Variant","Xesh qiymat"]]
for k,v in T['KAT'].items():
    p,rest=k.split('_',1); rows.append([p if p=='256' else '128',lab[rest],v])
rows.append(["256","To‘rtta tavsiya (+ oldinga uzatish va P(H) ⊕ H)",T4['KAT']['256']]); rows.append(["128","To‘rtta tavsiya (+ oldinga uzatish va P(H) ⊕ H)",T4['KAT']['16']])
Tb([900,3000,5454],rows,"Variantlar bo‘yicha nazorat qiymatlari",mono=(2,))
H2('5.4. Birlashgan variantning xossalari')
bb=T['birlashgan']
P(f"Birlashgan variantda yutishdan keyingi holatdagi bitta MSB ayirmasi 3000 juftlikning birortasida ham 1–7-raundlarning hech birida MSB ko‘rinishida saqlanmadi (256 bitli rejim: {', '.join(fz(v,3) for v in bb['256']['msb'])}) va ayirmasi so‘ngan juftlik ham bo‘lmadi (barcha raundlarda 0,000). 128 bitli rejimda ham natija xuddi shunday. Shunday qilib, hozirgi algoritmdagi to‘rtta asosiy kamchilik — 0-qatlamning chiziqliligi, MSB izlari, chiqishdagi doimiy munosabatlar va ichki kolliziyalar — birlashgan variantda kuzatilmaydi.")


a4=T4['256']; b4=T4['16']
P(f"To‘rtta tavsiya qo‘llanilgan variantning chiqish darajasidagi ko‘rsatkichlari: 256 bitli rejimda 0-qatlam rangi {a4['rang']}, minimal bit chastotasi {fz(a4['minf'],3)}, affin model aniqligi {fz(a4['affin'],3)}, integral sinovda doim balanslangan bitlar {a4['integral0']}, bitta xabar biti o‘zgarganda chiqishda o‘rtacha {fz(a4['HD'][0],1)} bit o‘zgaradi (ideal 128); 128 bitli rejimda mos ravishda {b4['rang']}, {fz(b4['minf'],3)}, {fz(b4['affin'],3)}, {b4['integral0']} va {fz(b4['HD'][0],1)} bit (ideal 64). Shunday qilib, hozirgi algoritmdagi beshta asosiy kamchilik — yutish nuqtasining zaifligi, 0-qatlam chiziqliligi, MSB izlari, chiqishdagi doimiy munosabatlar va ichki kolliziyalar, shuningdek orqaga hisoblash imkoniyati — to‘rtta tavsiya qo‘llanilgan variantda kuzatilmaydi.")

# ===================== 4. TEZLIK =====================
PB(); H1('6. O‘zgarishlarning tezlikka ta’siri')
H2('6.1. O‘lchash usuli')
P("Tezlik uch usulda baholandi. (1) Algoritmning C tilidagi realizatsiyasi barcha variantlarni bayroqlar orqali qo‘llab-quvvatlaydi va gcc -O2 bilan kompilyatsiya qilindi; o‘lchov Intel Xeon 2,3 GGs protsessorining bitta yadrosida, 262 144 baytli xabar uchun bajarildi. Har bir variant 3 marta aralash tartibda, har safar 5 takror bilan o‘lchandi va eng yaxshi vaqt olindi. (2) Python (numpy) realizatsiyasida 2000 ta mustaqil blok uchun bitta iteratsiya vaqti o‘lchandi. (3) Bitta blok uchun amallar soni C realizatsiyasi tuzilishi bo‘yicha sanaldi (Qo‘sh — 22 marta, Aralash — 10, TuzilmaKalit — 10, yutish — 3, S-box qatlami — 10 marta).")
H2('6.2. Natijalar')
VN=[('std','Standart'),('std+toq','Standart + toq kₑ'),('std+S','Standart + S-qatlam'),('sbz','SBZ'),('sbz+toq','SBZ + toq kₑ'),('sbz+toq+S','SBZ + toq kₑ + S-qatlam')]
rows=[["Rejim","Variant","C: vaqt, ms","C: mkS/blok","C: MB/s","C: farq, %"]]
for p in (256,16):
    for k,l in VN:
        d=Z['C'][f'{p}_{k}']; rows.append(['256' if p==256 else '128',l,fz(d['vaqt_ms'],2),fz(d['mks_blok'],3),fz(d['MBs'],2),sg(d['farq_foiz'])])
Tb([900,2900,1400,1400,1300,1454],rows,"C realizatsiyasi bo‘yicha tezlik (262 144 bayt, gcc -O2)")
c4=T4['C']
Tb([1300,2900,1700,1700,1754],[["Rejim","Variant","Vaqt, ms (eng yaxshi)","Barcha o‘lchovlar, ms","Standartga nisbatan, %"]]+[["256" if p=='256' else "128",l,fz(c4[f'{p}_{k}']['ms'],2),"; ".join(fz(x,1) for x in c4[f'{p}_{k}']['barcha']),sg(c4[f'{p}_{k}']['farq'])] for p in ('256','16') for k,l in (('std','Standart'),('uch','1–3-tavsiyalar'),('tort','To‘rtta tavsiya'))],"To‘rtinchi tavsiya qo‘shilgandagi tezlik (alohida o‘lchov, 4 marta)")
P("To‘rtinchi tavsiya (oldinga uzatish va chiqish o‘zgartirishi) 256 bitli rejimda tezlikni sezilarli o‘zgartirmaydi (farq 1% dan kam). 128 bitli rejimdagi bu o‘lchovda takroriy o‘lchovlar orasidagi farq juda katta bo‘ldi (virtual server yuklamasi), shuning uchun u yerdagi −14% ni tezlanish deb talqin qilmaslik kerak; amallar soni bo‘yicha to‘rtinchi tavsiya blokka atigi 32 ta XOR va xabarga bir marta ikkita Bog‘lash chaqiruvini qo‘shadi.")
rows=[["Rejim","Variant","Python: farq, %","Model: amallar soni","Model: farq, %"]]
for p in (256,16):
    for k,l in VN:
        rows.append(['256' if p==256 else '128',l,sg(Z['Python'][f'{p}_{k}']['farq_foiz']),f"{Z['model'][f'{p}_{k}']['jami']:,}".replace(',',' '),sg(Z['model'][f'{p}_{k}']['farq_foiz']) if abs(Z['model'][f'{p}_{k}']['farq_foiz'])>=0.05 else '0,0'])
Tb([900,2900,1900,1900,1754],rows,"Python realizatsiyasi va amallar modeli bo‘yicha nisbiy farq")
IMG('tezlik.png',16,5.8,"Variantlarning standart algoritmga nisbatan tezlik farqi")
m=Z['model']['256_std']
P(f"Bitta blok uchun amallarning asosiy qismi Qo‘sh o‘zgartirishiga to‘g‘ri keladi: {m['kopaytirish']:,} ta modul ko‘paytirish va {m['teskari_jadval']:,} ta teskarilash jadvali murojaatining 90 foizdan ortig‘i Qo‘sh da. S-box qatlami bir blokka 320 ta jadval murojaatini qo‘shadi (jami amallarning ≈0,7%), SBZ esa Z bilan bir xil sondagi jadval murojaatini talab qiladi. Toq kₑ qoidasi TuzilmaKalit dagi tarmoqlanuvchi taqqoslashlarni (blokka 640 ta) oddiy bit amallari (320 ta OR) bilan almashtiradi, shuning uchun biroz tezroq va doimiy vaqtli.".replace(',',' '))
P(f"C realizatsiyasida barcha variantlar standartdan {fz(min(d['farq_foiz'] for d in Z['C'].values()),1)}% … +{fz(max(d['farq_foiz'] for d in Z['C'].values()),1)}% oralig‘ida farq qiladi, bu o‘lchov shovqinidan (takroriy o‘lchovlar orasidagi farq {fz(Z['C_shovqin_foiz'],1)}% gacha) kichik. Birlashgan variant (uchala tavsiya) 256 bitli rejimda +{fz(Z['C']['256_sbz+toq+S']['farq_foiz'],1)}%, 128 bitli rejimda +{fz(Z['C']['16_sbz+toq+S']['farq_foiz'],1)}% farq berdi; amallar modeli 0,0% va +0,4% ni ko‘rsatadi. Python realizatsiyasida toq kₑ li variantlar 5–7% tezroq, chunki u yerda TuzilmaKalit dagi shartli tanlovlar (np.where) nisbatan qimmat.")
H2('6.3. Tezlik bo‘yicha xulosa')
BL("To‘rtta tavsiyaning hech biri algoritm tezligiga sezilarli ta’sir qilmaydi: C realizatsiyasida farq ±2% dan oshmaydi va o‘lchov shovqini doirasida, amallar modeli bo‘yicha esa 0,7% dan kam.")
BL("SBZ yutish nuqtasidagi jadval murojaatlari sonini o‘zgartirmaydi; toq kₑ qoidasi TuzilmaKalit ni soddalashtiradi va tezlikni biroz oshiradi; S-box qatlami blokka 320 ta jadval murojaati qo‘shadi; yakuniy qatlam blokka 32 ta XOR va xabarga bir marta ikkita Bog‘lash chaqiruvini qo‘shadi.")
BL("Algoritm tezligini deyarli butunlay Qo‘sh o‘zgartirishi (blokka 22 ta chaqiruv, 4224 ta modul teskarilash) belgilaydi; tezlikni oshirish kerak bo‘lsa, aynan Qo‘sh ni optimallashtirish kerak. Tavsiyalar bu qismga tegmaydi.")
P("Izoh: o‘lchangan mutlaq tezlik (≈4,4 MB/s, 256 bitli rejim) optimallashtirilmagan ma’lumotnoma realizatsiyasiga tegishli; maqsad variantlarni bir xil sharoitda nisbiy taqqoslash.")

# ===================== XULOSA =====================
PB(); H1('Xulosa')
P("Birinchi tavsiya yutish nuqtasidagi BaytZichlash ni AES S-boxiga asoslangan SBZ = S(h ⊕ S(n)) bilan almashtirish orqali amalga oshiriladi. Yutish nuqtasidagi maksimal korrelyatsiya va differensial ehtimollik 2⁻⁶ gacha kamayadi, bitta argumentdagi ayirma so‘nmaydi, algebraik daraja 13 ga oshadi; 128 bitli rejimdagi barcha asosiy zaifliklar yo‘qoladi, tezlik o‘zgarmaydi.")
P("Ikkinchi tavsiya kₑ ning barcha elementlarini toq qilish orqali amalga oshiriladi (kₑ ← kₑ ∨ 1, iteratsiyalardan oldin ham). Bu yagona naqsh 2¹⁶ naqsh orasida eng katta tarmoqlanish soniga (6) ega va Aralash ni barcha kalitlar uchun teskarilanuvchi qiladi. Natijada xesh qiymatdagi doimiy chiziqli munosabatlar va doimiy bitlar, Aralash yadrosi orqali ichki kolliziyalar hamda «eng yomon» kalitlar yo‘qoladi, yutish qatlamlaridagi faol baytlar soni oshadi.")
P("Uchinchi tavsiya raund ichida SurHolat dan keyin S-box qatlamini qo‘llash orqali amalga oshiriladi (256 bitli rejimda AES S-box, 128 bitli rejimda optimal 4 bitli S-box). Bu raund funksiyasining T-funksiya xossasini yo‘qotadi: 0-qatlam tenglamasi, MSB izlari va 0-qatlam integral balansi birinchi–ikkinchi raunddayoq yo‘qoladi, 2 raunddan keyin ko‘chki mezoni ideal qiymatga yetadi.")
P("To‘rtinchi tavsiya har bir blokdan keyin oldinga uzatish (holatᵢ = F(holatᵢ₋₁, blokᵢ) ⊕ holatᵢ₋₁) va chiqish o‘zgartirishi h(M) = P(H) ⊕ H orqali amalga oshiriladi. Ochiq qaytariladigan yakuniy qatlam (masalan, S-box) samarasiz — buzg‘unchi uni teskarilaydi; taklif etilgan qaytarib bo‘lmaydigan qatlam chiqishdagi doimiy munosabatlar, doimiy bitlar, affin va integral farqlovchilarni yo‘qotadi hamda orqaga hisoblash imkoniyatini yopadi.")
P("To‘rtta tavsiya birga qo‘llanganda ular bir-biriga xalal bermaydi va hozirgi algoritmdagi asosiy kamchiliklar kuzatilmaydi; algoritm tezligi amalda o‘zgarmaydi (±2%, o‘lchov shovqini doirasida). Tezlikni sezilarli oshirish uchun Qo‘sh o‘zgartirishini almashtirish kerak (Bog‘lash bo‘yicha alohida hisobotlarga qarang).")
H2('Keyingi qadamlar')
BL("Taklif etilgan variant uchun raundlar bo‘yicha faol S-box larning minimal sonini hisoblash va shu asosda chiziqli va differensial bardoshlilikning isbotlanadigan chegaralarini olish (Aralash ning toq kₑ dagi tarmoqlanish soni 6 bunda asos bo‘ladi).")
BL("Qo‘sh dagi nol qiymatni almashtirish qoidasini bijektiv qilish.")
BL("Kalitli rejimda kalitning 0-qatlamidan foydalanish usulini aniqlash yoki kalit uzunligini standartda mos ravishda ko‘rsatish.")
BL("128 bitli rejim uchun S-box ni (PRESENT yoki O‘zMSt 270 almashtirish uzellari) yakuniy tanlash va taklif etilgan variantni to‘liq kriptotahlil qilish.")
H2('Ilova: dasturlar')
Tb([3100,6254],[["Fayl","Vazifasi"],["tavsiyalar_tahlili.ipynb","2- va 3-tavsiyalarning kriptografik tekshiruvi: juft/toqlik naqshlari, L matritsasi va faol baytlar, chiqishdagi munosabatlar, ayirmalarning so‘nishi, elementlarni taqqoslash, birlashgan variant, nazorat qiymatlari"],["tezlik_tahlili.ipynb","Tezlik tahlili: C realizatsiyasini yozish, kompilyatsiya qilish va nazorat qiymatlarini tekshirish, C va Python o‘lchovlari, amallar modeli, jamlanma va grafik"],["uzmst285.c","Algoritmning C realizatsiyasi (barcha variantlar, nazorat qiymatlari va tezlik o‘lchovi); daftar uni avtomatik yaratadi"],["variant.py","Variantlarning Python realizatsiyasi (uzmst285_tahlil paketida)"]],"Ilova qilingan dasturlar")
P("Daftarlarni ishga tushirish uchun Python 3 va numpy kifoya; tezlik daftaridagi C o‘lchovi uchun kompyuterda C kompilyatori (gcc, clang yoki Windows da MinGW) bo‘lishi kerak, aks holda daftar C qismini o‘tkazib yuborib, Python va model natijalarini hisoblaydi.")
json.dump(B,open('blocks.json','w'),ensure_ascii=False); print(len(B),tc[0])
