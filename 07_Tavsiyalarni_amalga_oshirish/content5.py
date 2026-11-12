import json
T=json.load(open('/home/claude/ka/tavsiyalar_natijalari.json')); Z=json.load(open('/home/claude/ka/tezlik_natijalari.json'))
B=[]; tc=[0]; fc=[0]
H1=lambda t:B.append(['h1',t]); H2=lambda t:B.append(['h2',t]); H3=lambda t:B.append(['h3',t])
P=lambda t:B.append(['p',t]); F=lambda t:B.append(['f',t]); BL=lambda t:B.append(['b',t]); PB=lambda:B.append(['pb'])
def Tb(w,rows,cap,mono=()): tc[0]+=1; B.append(['cap',f"{tc[0]}-jadval. {cap}"]); B.append(['t',w,rows,list(mono)])
def IMG(p,w,h,cap): fc[0]+=1; B.append(['img',p,w,h]); B.append(['fcap',f"{fc[0]}-rasm. {cap}"])
fz=lambda x,d=2:(f'{x:.{d}f}').replace('.',','); sg=lambda x:(('+' if x>0 else '')+fz(x,1)) if x!=0 else '0,0'
E=T['element']

B.append(['title','O‘zMSt 285:2024 1-ALGORITMINI TAKOMILLASHTIRISH BO‘YICHA TAVSIYALARNI AMALGA OSHIRISH VA ULARNING TEZLIKKA TA’SIRI'])
B.append(['sub','Aralash/TuzilmaKalit va raund funksiyasidagi T-funksiya xossasi bo‘yicha tavsiyalar'])
H1('Kirish')
P("Standart algoritmning kriptotahlili natijasida uchta tavsiya berilgan edi: (1) yutish nuqtasidagi BaytZichlash ni SBZ = S(h ⊕ S(n)) bilan almashtirish; (2) Aralash va TuzilmaKalit o‘zgartirishlarini diamatritsa 2 moduli bo‘yicha har doim teskarilanuvchi bo‘ladigan qilib qayta loyihalash; (3) raund funksiyasiga yuqori bitlarni quyi bitlarga o‘tkazuvchi element qo‘shib, T-funksiya xossasini yo‘qotish. Birinchi tavsiya alohida materialda batafsil o‘rganilgan. Ushbu hujjatda ikkinchi va uchinchi tavsiyalarni amalda qanday bajarish mumkinligi, ularning kriptografik samarasi, uchala tavsiyaning birgalikdagi varianti va o‘zgarishlarning tezlikka ta’siri bayon etiladi.")
P("Barcha natijalar ilova qilingan ikkita Jupyter daftarida olingan: *tavsiyalar_tahlili.ipynb* (kriptografik tekshiruvlar) va *tezlik_tahlili.ipynb* (tezlik o‘lchovlari, C va Python realizatsiyalari, amallar modeli). Daftarlar mustaqil ishlaydi va bajarilgan holda topshirilgan. Algoritmning barcha 12 ta varianti (ikki rejim × olti variant) uchun C va Python realizatsiyalari bir xil nazorat qiymatlarini beradi; standart va SBZ variantlari uchun ular standartning A ilovasidagi va SBZ materialidagi qiymatlar bilan mos keladi.")

# ===================== 1. 2-TAVSIYA =====================
PB(); H1('1. Ikkinchi tavsiya: Aralash va TuzilmaKalit')
H2('1.1. Muammoning mohiyati')
P("Aralash holatning har bir 4×4 yarmini raund kaliti kₑ ning mos yarmiga diamatritsa qoidasi bo‘yicha 2ⁿ moduli bo‘yicha ko‘paytiradi. Belgilangan kₑ da bu Z/2ⁿ halqasi ustidagi chiziqli akslantirish. Halqa ustidagi chiziqli akslantirish faqat uning aniqlovchisi toq, ya’ni 2 moduli bo‘yicha ko‘rinishi teskarilanuvchi bo‘lgandagina teskarilanuvchi bo‘ladi. 2 moduli bo‘yicha ko‘rinish M(k₀) esa faqat kₑ elementlarining juft/toqligiga bog‘liq.")
P("Hozirgi TuzilmaKalit kₑ ning juft/toqligini kalit k ning juft/toqligiga tenglashtiradi, shuning uchun M(k₀) kalitga bog‘liq va kalitlarning ≈99 foizida teskarilanmaydi. Bundan uchta kamchilik kelib chiqadi: xesh qiymatning 0-qatlamida korrelyatsiyasi 1 bo‘lgan chiziqli munosabatlar (o‘rtacha ≈6 ta) va doimiy bitlar; M(k₀) yadrosidagi ayirmalarning ehtimollik 1 bilan so‘nishi (ichki kolliziyalar); chiziqli izlar uchun «eng yomon» kalitlar. Standartning 5.1.2-bandi ham kₑ ning kvadrat qismlari teskarilanuvchi bo‘lishini talab qiladi, lekin shartni «aniqlovchi noldan farqli» deb ifodalaydi; 2ⁿ moduli uchun to‘g‘ri shart — aniqlovchining toq bo‘lishi.")
H2('1.2. Juft/toqlik naqshlarini tahlil qilish')
P("M(K) matritsasi K ning juft/toqlik bitlariga nisbatan chiziqli (diamatritsa ko‘paytmasi bichiziqli), shuning uchun har bir 4×4 yarim uchun barcha 2¹⁶ = 65536 ta juft/toqlik naqshi uchun 16×16 matritsa tez quriladi. Har bir naqsh uchun GF(2) dagi rang va teskarilanuvchi naqshlar uchun tarmoqlanish soni — min (wt(x) + wt(M·x)), x ≠ 0 — barcha 2¹⁶ vektor bo‘yicha hisoblandi.")
nq=T['naqsh']
Tb([4677,4677],[["Ko‘rsatkich","Qiymat"],["Teskarilanuvchi naqshlar",f"{nq['teskarilanuvchi']} / 65536 ({fz(100*nq['teskarilanuvchi']/65536,1)}%)"]]+[[f"Tarmoqlanish soni {k}",f"{v} ta naqsh"] for k,v in nq['taqsimot'].items()]+[["Eng katta tarmoqlanishli naqsh","0xFFFF — barcha elementlar toq"]],"4×4 yarim uchun juft/toqlik naqshlari tahlili")
P("Natija juda aniq: tarmoqlanish soni 6 bo‘lgan yagona naqsh — kₑ ning barcha elementlari toq bo‘lgan holat. Qolgan teskarilanuvchi naqshlarning tarmoqlanish soni 2–4 ga teng. Toq son 2ⁿ moduli bo‘yicha doim teskarilanuvchi bo‘lgani uchun bu tanlov algebraik jihatdan ham tabiiy.")
H2('1.3. Taklif etilayotgan o‘zgartirish')
P("TuzilmaKalit o‘zgartirishi quyidagi qoida bilan almashtiriladi:")
F("kₑ[s,u] ← kₑ[s,u] ∨ 1   (0 ≤ s < 4, 0 ≤ u < 8),")
P("ya’ni juft element 1 ga oshiriladi, toq element o‘zgarmaydi. Hozirgi «k bilan bir xil juftlik» sharti va «kₑ ≡ 0 bo‘lsa 2» qoidasi kerak bo‘lmay qoladi, chunki toq son nolga teng bo‘lmaydi. Birinchi raunddagi Aralash TuzilmaKalit dan oldin bajarilgani uchun iteratsiyalardan oldin ham kₑ ← k ∨ 1 qo‘llanadi. Qo‘sh o‘zgartirishidagi R = k[0] parametri o‘zgarmaydi va avvalgidek juft bo‘lishi kerak (u kₑ dan emas, k dan olinadi). Aralash ning formulasi o‘zgarmaydi.")
H2('1.4. Tekshiruv natijalari')
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
H2('1.5. Cheklovlar')
BL("Kalitli (128 bitli) rejimda kalitning 32 ta eng kichik biti algoritmga ta’sir qilmay qoladi va kalit formal ravishda 96 bitga qisqaradi. Hozirgi algoritmda bu bitlar qolganlaridan alohida 2³⁰ ta urinishda tiklanadi, shuning uchun amaldagi xavfsizlik deyarli o‘zgarmaydi; lekin standartda kalit uzunligini shunga mos ko‘rsatish yoki bu bitlarni boshqa joyda (masalan, boshlang‘ich holatda) ishlatish kerak. 256 bitli rejim standartga ko‘ra kalitsiz.")
BL("Qo‘sh dagi «x⁻² ≡ 0 bo‘lsa A₂ + B₂» qoidasi element akslantirishini bijeksiya bo‘lmagan qiladi (256 kirishdan 255 xil chiqish); bu juda kichik ehtimollik bilan ichki kolliziyalarga olib kelishi mumkin. Ushbu tajribada (3000 juftlik) so‘nish kuzatilmadi, boshqa tajribada 256 bitli rejimda 0,07% qayd etilgan. To‘liq bartaraf etish uchun bu qoidani ham bijektiv qilish kerak.")
BL("Raund funksiyasi T-funksiyaligicha qoladi: MSB izi hamon har raundda ≈0,9 ehtimollik bilan saqlanadi (256 bitli rejimda 7 raunddan keyin " + fz(so['256_1']['msb'][6],2) + "). Bu kamchilikni uchinchi tavsiya bartaraf etadi.")

# ===================== 2. 3-TAVSIYA =====================
PB(); H1('2. Uchinchi tavsiya: raund funksiyasining T-funksiya xossasini yo‘qotish')
H2('2.1. T-funksiya va uning oqibatlari')
P("T-funksiya — natijaning j-biti kirishlarning faqat 0…j-bitlariga bog‘liq bo‘lgan akslantirish. 2ⁿ moduli bo‘yicha qo‘shish, ayirish, ko‘paytirish va teskarilash T-funksiyalar, chunki ko‘chirish faqat yuqoriga tarqaladi. 1-algoritmning yutishsiz raundlari (Aralash, Qo‘sh, SurHolat, SurKalit, TuzilmaKalit) T-funksiyadir: SurHolat elementlarni joyidan ko‘chiradi, lekin bitlarni bayt ichida siljitmaydi. Natijada 0-qatlam raundlarda chiziqli tenglama bilan aniq kuzatiladi, MSB ayirmalari quyi bitlarga o‘tmaydi, 0-qatlam darajasi 1 bo‘lib qoladi va integral to‘plamlarda balanslanadi. Buni tuzatish uchun raund ichiga yuqori bitlarni quyi bitlarga o‘tkazuvchi element qo‘shish kerak.")
H2('2.2. Tanlangan elementlar va ularning joylashuvi')
P("Element har bir raundda SurHolat dan keyin, ikkinchi Qo‘sh dan oldin, holat massivining har bir elementiga qo‘llanadi:")
F("Aralash → Qo‘sh(holat, kₑ) → SurHolat, SurKalit → E(holat) → Qo‘sh(holat, kₑ) → TuzilmaKalit")
Tb([2700,3327,3327],[["Element E","256 bitli rejim (bayt)","128 bitli rejim (yarim bayt)"],["Davriy aylantirish","x ← x ⋘ 3","x ← x ⋘ 1"],["XOR-surish","x ← x ⊕ (x ≫ 4)","x ← x ⊕ (x ≫ 2)"],["S-box qatlami","x ← S(x), AES S-box","x ← S₄(x), PRESENT S-box"]],"Tekshirilgan elementlar")
P("Uchala element ham bijeksiya, shuning uchun yangi kolliziyalar keltirib chiqarmaydi. Element faqat holatga qo‘llanadi, kₑ ga emas, shuning uchun ikkinchi tavsiyadagi toq kₑ sharti saqlanadi.")
H2('2.3. Baholash ko‘rsatkichlari')
BL("0-qatlam raund tenglamasi h₀ ← L·h₀ ning korrelyatsiyasi (600 kalit) — chiziqli tahlil;")
BL("bitta raunddan keyingi eng yaxshi «bitta kirish biti → bitta chiqish biti» korrelyatsiyasi (6000 namuna; shovqin chegarasi 0,058) — chiziqli tahlil;")
BL("MSB izining saqlanish ehtimolligi (2000 juftlik) — differensial tahlil;")
BL("qat’iy ko‘chki mezoni (SAC): bitta kirish biti o‘zgarganda har bir chiqish bitining o‘zgarish ehtimolligi, 1 va 2 raunddan keyin; o‘rtacha qiymat (ideal 0,5) va bog‘liqligi umuman yo‘q (kirish, chiqish) juftliklari ulushi — algebraik va differensial tarqalish;")
BL("MSB ning 0-bitga ta’siri (SAC ning tegishli qismi) — T-funksiya xossasining buzilishi;")
BL("integral: bitta faol bayt bo‘yicha 0-qatlam XOR yig‘indisining nol bo‘lish ulushi (60 tajriba; tasodifiy funksiya uchun 0,5);")
BL("hisoblash vaqti (Python, 2000 blok, 10 raund).")
H2('2.4. Natijalar')
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
H2('2.5. Elementni tanlash')
P("S-box qatlami tavsiya etiladi. Davriy aylantirish va XOR-surish T-funksiya xossasini buzadi, lekin o‘zlari GF(2) ustida chiziqli, ya’ni chiziqli bo‘lmaganlikni faqat modul arifmetikasi beradi. S-box esa har bir faol bayt uchun kafolatlangan chegaralar beradi (AES S-box: korrelyatsiya ≤ 2⁻³, differensial ehtimollik ≤ 2⁻⁶). Bu raundlar bo‘yicha faol S-box larni sanash orqali isbotlanadigan baholarni olish imkonini beradi. S-box bir raundda MSB ni 0-bitga eng kuchli o‘tkazadi (256 bitli rejimda 0,14, boshqa elementlarda ≈0,01) va 1 raunddan keyingi SAC ning minimal qiymati ham eng yuqori. 256 bitli rejimda SBZ dagi AES S-box jadvali qayta ishlatiladi, ya’ni qo‘shimcha jadval talab qilinmaydi. 128 bitli rejim uchun har qanday optimal 4 bitli S-box (differensial bir xillik 4, maksimal korrelyatsiya 2⁻¹) mos keladi; tekshiruvda PRESENT S-box ishlatildi. Milliy standartlar bilan muvofiqlik uchun O‘zMSt 270 almashtirish uzellaridan foydalanish ham mumkin, lekin ular shu mezonlar bo‘yicha alohida tekshirilishi kerak.")

# ===================== 3. BIRLASHGAN =====================
PB(); H1('3. Uchala tavsiya birgalikda')
H2('3.1. Algoritmdagi o‘zgarishlar jamlanmasi')
Tb([2600,3377,3377],[["Akslantirish","Standart","Taklif etilgan variant"],
 ["Yutish (0-, 8-, 9-nuqtalar)","BaytZichlash: Z(h) ‖ Z(n) (256) yoki h ⊕ n (128)","SBZ: S(h ⊕ S(n)); 128 bitli rejimda qo‘shni yarim baytlar juftlanadi"],
 ["TuzilmaKalit","kₑ juftligi k juftligiga tenglashtiriladi; kₑ ≡ 0 → 2","kₑ ← kₑ ∨ 1 (barcha elementlar toq)"],
 ["Iteratsiyalardan oldin","kₑ ← k","kₑ ← k ∨ 1"],
 ["Raund ichida (SurHolat dan keyin)","—","holat ← S(holat) (256) yoki S₄(holat) (128)"],
 ["Aralash, Qo‘sh, SurHolat, SurKalit, raundlar soni, uzunlik va NY bloklari","—","o‘zgarishsiz"]],"Taklif etilgan variantdagi o‘zgarishlar")
H2('3.2. Bitta iteratsiya psevdokodi')
code=["kₑ ← kₑ ∨ 1","(h̃, ñ) ← Qo‘sh(holat, blok);  holat ← SBZ(h̃, ñ)","For j = 1 to 10","    holat ← Aralash(holat, kₑ)","    (holat, kₑ) ← Qo‘sh(holat, kₑ)","    holat ← SurHolat(holat);  kₑ ← SurKalit(kₑ)","    holat ← S(holat)                      // yangi: S-box qatlami","    If j = 8: (h̃, ñ) ← Qo‘sh(holat, blok); holat ← SBZ(h̃, ñ)","    Else:     (holat, kₑ) ← Qo‘sh(holat, kₑ)","    kₑ ← kₑ ∨ 1                            // yangi TuzilmaKalit","    If j = 9: (h̃, ñ) ← Qo‘sh(holat, blok); holat ← SBZ(h̃, ñ)","End For"]
Tb([9354],[["Psevdokod"],["\n".join(code)]],"Taklif etilgan variantning bitta iteratsiyasi",mono=(0,))
H2('3.3. Nazorat qiymatlari')
P("A ilova kaliti va 64 baytli xabari uchun barcha variantlarning nazorat qiymatlari quyidagi jadvalda keltirilgan. Ular C va Python realizatsiyalarida bir xil chiqdi; standart va SBZ qiymatlari standartning A ilovasi va SBZ materiali bilan mos keladi.")
lab={'std_0_0':'Standart','sbz_0_0':'SBZ','std_1_0':'Standart + toq kₑ','std_0_1':'Standart + S-qatlam','sbz_1_0':'SBZ + toq kₑ','sbz_1_1':'SBZ + toq kₑ + S-qatlam'}
rows=[["Rejim","Variant","Xesh qiymat"]]
for k,v in T['KAT'].items():
    p,rest=k.split('_',1); rows.append([p if p=='256' else '128',lab[rest],v])
Tb([900,2800,5654],rows,"Variantlar bo‘yicha nazorat qiymatlari",mono=(2,))
H2('3.4. Birlashgan variantning xossalari')
bb=T['birlashgan']
P(f"Birlashgan variantda yutishdan keyingi holatdagi bitta MSB ayirmasi 3000 juftlikning birortasida ham 1–7-raundlarning hech birida MSB ko‘rinishida saqlanmadi (256 bitli rejim: {', '.join(fz(v,3) for v in bb['256']['msb'])}) va ayirmasi so‘ngan juftlik ham bo‘lmadi (barcha raundlarda 0,000). 128 bitli rejimda ham natija xuddi shunday. Shunday qilib, hozirgi algoritmdagi to‘rtta asosiy kamchilik — 0-qatlamning chiziqliligi, MSB izlari, chiqishdagi doimiy munosabatlar va ichki kolliziyalar — birlashgan variantda kuzatilmaydi.")

# ===================== 4. TEZLIK =====================
PB(); H1('4. O‘zgarishlarning tezlikka ta’siri')
H2('4.1. O‘lchash usuli')
P("Tezlik uch usulda baholandi. (1) Algoritmning C tilidagi realizatsiyasi barcha variantlarni bayroqlar orqali qo‘llab-quvvatlaydi va gcc -O2 bilan kompilyatsiya qilindi; o‘lchov Intel Xeon 2,3 GGs protsessorining bitta yadrosida, 262 144 baytli xabar uchun bajarildi. Har bir variant 3 marta aralash tartibda, har safar 5 takror bilan o‘lchandi va eng yaxshi vaqt olindi. (2) Python (numpy) realizatsiyasida 2000 ta mustaqil blok uchun bitta iteratsiya vaqti o‘lchandi. (3) Bitta blok uchun amallar soni C realizatsiyasi tuzilishi bo‘yicha sanaldi (Qo‘sh — 22 marta, Aralash — 10, TuzilmaKalit — 10, yutish — 3, S-box qatlami — 10 marta).")
H2('4.2. Natijalar')
VN=[('std','Standart'),('std+toq','Standart + toq kₑ'),('std+S','Standart + S-qatlam'),('sbz','SBZ'),('sbz+toq','SBZ + toq kₑ'),('sbz+toq+S','SBZ + toq kₑ + S-qatlam')]
rows=[["Rejim","Variant","C: vaqt, ms","C: mkS/blok","C: MB/s","C: farq, %"]]
for p in (256,16):
    for k,l in VN:
        d=Z['C'][f'{p}_{k}']; rows.append(['256' if p==256 else '128',l,fz(d['vaqt_ms'],2),fz(d['mks_blok'],3),fz(d['MBs'],2),sg(d['farq_foiz'])])
Tb([900,2900,1400,1400,1300,1454],rows,"C realizatsiyasi bo‘yicha tezlik (262 144 bayt, gcc -O2)")
rows=[["Rejim","Variant","Python: farq, %","Model: amallar soni","Model: farq, %"]]
for p in (256,16):
    for k,l in VN:
        rows.append(['256' if p==256 else '128',l,sg(Z['Python'][f'{p}_{k}']['farq_foiz']),f"{Z['model'][f'{p}_{k}']['jami']:,}".replace(',',' '),sg(Z['model'][f'{p}_{k}']['farq_foiz']) if abs(Z['model'][f'{p}_{k}']['farq_foiz'])>=0.05 else '0,0'])
Tb([900,2900,1900,1900,1754],rows,"Python realizatsiyasi va amallar modeli bo‘yicha nisbiy farq")
IMG('tezlik.png',16,5.8,"Variantlarning standart algoritmga nisbatan tezlik farqi")
m=Z['model']['256_std']
P(f"Bitta blok uchun amallarning asosiy qismi Qo‘sh o‘zgartirishiga to‘g‘ri keladi: {m['kopaytirish']:,} ta modul ko‘paytirish va {m['teskari_jadval']:,} ta teskarilash jadvali murojaatining 90 foizdan ortig‘i Qo‘sh da. S-box qatlami bir blokka 320 ta jadval murojaatini qo‘shadi (jami amallarning ≈0,7%), SBZ esa Z bilan bir xil sondagi jadval murojaatini talab qiladi. Toq kₑ qoidasi TuzilmaKalit dagi tarmoqlanuvchi taqqoslashlarni (blokka 640 ta) oddiy bit amallari (320 ta OR) bilan almashtiradi, shuning uchun biroz tezroq va doimiy vaqtli.".replace(',',' '))
P(f"C realizatsiyasida barcha variantlar standartdan {fz(min(d['farq_foiz'] for d in Z['C'].values()),1)}% … +{fz(max(d['farq_foiz'] for d in Z['C'].values()),1)}% oralig‘ida farq qiladi, bu o‘lchov shovqinidan (takroriy o‘lchovlar orasidagi farq {fz(Z['C_shovqin_foiz'],1)}% gacha) kichik. Birlashgan variant (uchala tavsiya) 256 bitli rejimda +{fz(Z['C']['256_sbz+toq+S']['farq_foiz'],1)}%, 128 bitli rejimda +{fz(Z['C']['16_sbz+toq+S']['farq_foiz'],1)}% farq berdi; amallar modeli 0,0% va +0,4% ni ko‘rsatadi. Python realizatsiyasida toq kₑ li variantlar 5–7% tezroq, chunki u yerda TuzilmaKalit dagi shartli tanlovlar (np.where) nisbatan qimmat.")
H2('4.3. Tezlik bo‘yicha xulosa')
BL("Uchala tavsiya ham algoritm tezligiga sezilarli ta’sir qilmaydi: C realizatsiyasida farq ±2% dan oshmaydi va o‘lchov shovqini doirasida, amallar modeli bo‘yicha esa 0,7% dan kam.")
BL("Toq kₑ qoidasi TuzilmaKalit ni soddalashtiradi va tezlikni biroz oshiradi; S-box qatlami blokka 320 ta jadval murojaati qo‘shadi; SBZ yutish nuqtasidagi jadval murojaatlari sonini o‘zgartirmaydi.")
BL("Algoritm tezligini deyarli butunlay Qo‘sh o‘zgartirishi (blokka 22 ta chaqiruv, 4224 ta modul teskarilash) belgilaydi; tezlikni oshirish kerak bo‘lsa, aynan Qo‘sh ni optimallashtirish kerak. Tavsiyalar bu qismga tegmaydi.")
P("Izoh: o‘lchangan mutlaq tezlik (≈4,4 MB/s, 256 bitli rejim) optimallashtirilmagan ma’lumotnoma realizatsiyasiga tegishli; maqsad variantlarni bir xil sharoitda nisbiy taqqoslash.")

# ===================== XULOSA =====================
PB(); H1('Xulosa')
P("Ikkinchi tavsiya kₑ ning barcha elementlarini toq qilish orqali amalga oshiriladi (kₑ ← kₑ ∨ 1, iteratsiyalardan oldin ham). Bu yagona naqsh 2¹⁶ naqsh orasida eng katta tarmoqlanish soniga (6) ega va Aralash ni barcha kalitlar uchun teskarilanuvchi qiladi. Natijada xesh qiymatdagi doimiy chiziqli munosabatlar va doimiy bitlar, Aralash yadrosi orqali ichki kolliziyalar hamda «eng yomon» kalitlar yo‘qoladi, yutish qatlamlaridagi faol baytlar soni oshadi.")
P("Uchinchi tavsiya raund ichida SurHolat dan keyin S-box qatlamini qo‘llash orqali amalga oshiriladi (256 bitli rejimda AES S-box, 128 bitli rejimda optimal 4 bitli S-box). Bu raund funksiyasining T-funksiya xossasini yo‘qotadi: 0-qatlam tenglamasi, MSB izlari va 0-qatlam integral balansi birinchi–ikkinchi raunddayoq yo‘qoladi, 2 raunddan keyin ko‘chki mezoni ideal qiymatga yetadi.")
P("Uchala tavsiya birga qo‘llanganda ular bir-biriga xalal bermaydi va hozirgi algoritmdagi asosiy kamchiliklar kuzatilmaydi; algoritm tezligi amalda o‘zgarmaydi (±2%, o‘lchov shovqini doirasida).")
H2('Keyingi qadamlar')
BL("Taklif etilgan variant uchun raundlar bo‘yicha faol S-box larning minimal sonini hisoblash va shu asosda chiziqli va differensial bardoshlilikning isbotlanadigan chegaralarini olish (Aralash ning toq kₑ dagi tarmoqlanish soni 6 bunda asos bo‘ladi).")
BL("Qo‘sh dagi nol qiymatni almashtirish qoidasini bijektiv qilish.")
BL("Kalitli rejimda kalitning 0-qatlamidan foydalanish usulini aniqlash yoki kalit uzunligini standartda mos ravishda ko‘rsatish.")
BL("128 bitli rejim uchun S-box ni (PRESENT yoki O‘zMSt 270 almashtirish uzellari) yakuniy tanlash va taklif etilgan variantni to‘liq kriptotahlil qilish.")
H2('Ilova: dasturlar')
Tb([3100,6254],[["Fayl","Vazifasi"],["tavsiyalar_tahlili.ipynb","2- va 3-tavsiyalarning kriptografik tekshiruvi: juft/toqlik naqshlari, L matritsasi va faol baytlar, chiqishdagi munosabatlar, ayirmalarning so‘nishi, elementlarni taqqoslash, birlashgan variant, nazorat qiymatlari"],["tezlik_tahlili.ipynb","Tezlik tahlili: C realizatsiyasini yozish, kompilyatsiya qilish va nazorat qiymatlarini tekshirish, C va Python o‘lchovlari, amallar modeli, jamlanma va grafik"],["uzmst285.c","Algoritmning C realizatsiyasi (barcha variantlar, nazorat qiymatlari va tezlik o‘lchovi); daftar uni avtomatik yaratadi"],["variant.py","Variantlarning Python realizatsiyasi (uzmst285_tahlil paketida)"]],"Ilova qilingan dasturlar")
P("Daftarlarni ishga tushirish uchun Python 3 va numpy kifoya; tezlik daftaridagi C o‘lchovi uchun kompyuterda C kompilyatori (gcc, clang yoki Windows da MinGW) bo‘lishi kerak, aks holda daftar C qismini o‘tkazib yuborib, Python va model natijalarini hisoblaydi.")
json.dump(B,open('blocks.json','w'),ensure_ascii=False); print(len(B),tc[0])
