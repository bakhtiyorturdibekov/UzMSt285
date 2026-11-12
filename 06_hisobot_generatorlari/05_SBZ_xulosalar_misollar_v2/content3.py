import json, math
R=json.load(open('/home/claude/nb/misollar_natijalari.json'))
B=[]
H1=lambda t:B.append(['h1',t]); H2=lambda t:B.append(['h2',t]); H3=lambda t:B.append(['h3',t])
P=lambda t:B.append(['p',t]); F=lambda t:B.append(['f',t]); BL=lambda t:B.append(['b',t])
XUL=lambda t:B.append(['xul',t]); PB=lambda:B.append(['pb'])
tc=[0]
def T(w,rows,cap,mono=()):
    tc[0]+=1; B.append(['cap',f"{tc[0]}-jadval. {cap}"]); B.append(['t',w,rows,list(mono)])
fz=lambda x,d=2:(f'{x:.{d}f}').replace('.',',')
nl='\n'.join
opn={'Aralash':'Aralash(holat, kₑ)','Qosh1':'Qo‘sh(holat, kₑ)','Sur':'SurHolat, SurKalit','Qosh2':'Qo‘sh(holat, kₑ)','Tuz':'TuzilmaKalit(kₑ, k)'}
W5=[2300,2000,2000,3054]   # taqqoslash jadvali kengliklari
def TAQ(rows,cap): T([2200,1850,1850,3454],[["Ko‘rsatkich","Kutilgan","Olingan","Farq va uning izohi"]]+rows,cap)
def bolim(nima,nega,qanday):
    H3("Nima tekshiriladi?"); [P(x) for x in nima]
    H3("Nega bu muhim?"); [P(x) for x in nega]
    H3("Qanday tekshirildi?"); [BL(x) for x in qanday]

# ============ TITUL VA KIRISH ============
B.append(['title','SBZ O‘ZGARTIRISHI KRIPTOTAHLILI XULOSALARI: NIMA TEKSHIRILDI, NIMA KUTILDI VA NIMA OLINDI'])
B.append(['sub','Sodda izohlar va misollar bilan to‘ldirilgan ilova (2-tahrir)'])
H1('Kirish')
P("Asosiy hisobotda O‘zMSt 285:2024 xesh funksiyasining 1-algoritmi uchun 13 ta xulosa berilgan: chiziqli kriptotahlil bo‘yicha 5 ta, differensial va algebraik kriptotahlil bo‘yicha 4 tadan. Ushbu hujjat ularning har birini sodda tilda tushuntiradi. Har bir xulosa bir xil tartibda ko‘rib chiqiladi:")
BL("*Nima tekshiriladi?* — xulosaning ma’nosi oddiy so‘zlar bilan;")
BL("*Nega bu muhim?* — xulosa buzg‘unchi (hujumchi) uchun nimani anglatadi;")
BL("*Qanday tekshirildi?* — tajriba qadamma-qadam;")
BL("*Kutilgan natija* — nazariya bo‘yicha nima chiqishi kerak edi va nima uchun;")
BL("*Olingan natija* — dasturda haqiqatda nima chiqdi (jadvallar);")
BL("*Kutilgan va olingan natijalarni taqqoslash* — har bir ko‘rsatkich bo‘yicha farq bormi va bo‘lsa, uning sababi;")
BL("*Sodda xulosa* — bir-ikki gapda asosiy fikr.")
P("Barcha raqamlar *xulosalar_misollar.ipynb* Jupyter daftarida hisoblangan va daftar sizning kompyuteringizda ham bayt-ma-bayt bir xil natija bergan (*misollar_natijalari.json*). Dastlabki ma’lumotlar — standartning A ilovasidagi kalit va xabar:")
F("k = c86ed4b2 756df1cd 6b6eca81 d4418092 21ab81bb a0c7c150 44be8feb 934f95a2")
F("M = «funksiyaxeshirovaniyainformasionnayatexnologiyakriptograficheska» (64 bayt)")

H1('Asosiy tushunchalar sodda tilda')
P("Quyidagi tushunchalar butun hujjat davomida ishlatiladi. Ularni bir marta tushunib olish keyingi bo‘limlarni o‘qishni ancha osonlashtiradi.")
H3('Algoritm qanday ishlaydi')
P("Xesh funksiyaning ichki holati — 4 satr va 8 ustundan iborat jadval (*holat* massivi), har bir katakda bitta bayt (0 dan 255 gacha son) yoki 128 bitli rejimda yarim bayt (0 dan 15 gacha) turadi. Xabar bloklarga bo‘linadi va har bir blok uchun holat 10 ta raunddan o‘tadi. Har bir raundda holat ketma-ket bir nechta akslantirishdan o‘tadi: *Aralash* (kalit bilan matritsa ko‘paytirish), *Qo‘sh* (har bir sonni maxsus darajaga ko‘tarish), *SurHolat* (kataklarni joyidan surish), *TuzilmaKalit* (raund kalitini tuzatish). Xabar bloki holatga faqat uchta joyda qo‘shiladi; bu joylarni *yutish nuqtalari* deb ataymiz: raundlardan oldin (0-nuqta), 8-raundda va 9-raundda. Aynan shu nuqtalarda standartdagi *BaytZichlash* yoki taklif etilgan *SBZ* ishlaydi.")
H3('0-qatlam')
P("Har bir baytda 8 ta bit bor; eng o‘ngdagisi (eng kichik bit) son juft yoki toqligini bildiradi: juft son uchun 0, toq son uchun 1. Holatdagi 32 ta sonning juft/toqlik bitlarini yig‘sak, 32 bitli vektor hosil bo‘ladi — uni *0-qatlam* deymiz. Masalan, holat[0,0] = bf (toq) bo‘lsa, uning 0-qatlamdagi biti 1 ga teng.")
H3('Chiziqli munosabat va korrelyatsiya')
P("Chiziqli munosabat — bir nechta bitning XOR yig‘indisi (ya’ni «birlar soni juftmi yoki toqmi») haqidagi tenglik, masalan: «chiqishning 0-biti kirishning 0- va 2-bitlari yig‘indisiga teng». Agar bunday tenglik har doim bajarilsa, uning *korrelyatsiyasi* c = 1; hech qachon bajarilmasa, c = −1; tasodifiy holatdagidek yarim hollarda bajarilsa, c = 0. Buzg‘unchi uchun c qanchalik 0 dan uzoq bo‘lsa, shunchalik yaxshi. Tenglikni sezish uchun taxminan 1/c² ta misol kerak bo‘ladi: c = 2⁻⁶ bo‘lsa, ≈4 ming, c = 2⁻⁶⁴ bo‘lsa, 2¹²⁸ ta misol — bu amalda imkonsiz.")
H3('Ayirma va uning ehtimolligi')
P("Differensial tahlilda ikkita deyarli bir xil kirish olinadi va ular orasidagi farq (*ayirma*, XOR) akslantirishlardan qanday o‘tishi kuzatiladi. Masalan, holat[0,0] ning faqat eng katta biti (MSB, 80) farq qilsa, ayirma «80» deb yoziladi. Agar ayirma biror akslantirishdan aniq ma’lum ko‘rinishda o‘tsa, ehtimollik 1; ko‘pincha bu ehtimollik 2⁻⁶ (64 dan 1) kabi kichik sondir. Ehtimollik qanchalik kichik bo‘lsa, buzg‘unchiga shunchalik qiyin.")
H3('Faol bayt')
P("Chiziqli izda niqob (qaysi bitlarni kuzatayotganimiz) yoki differensial izda ayirma noldan farqli bo‘lgan bayt *faol bayt* deyiladi. Har bir faol bayt yutish nuqtasidan o‘tganda buzg‘unchidan «to‘lov» talab qiladi: SBZ da har bir faol bayt korrelyatsiyani kamida 2⁶ marta kamaytiradi.")
H3('Algebraik daraja')
P("Har bir chiqish bitini kirish bitlari orqali ko‘phad (masalan, x₁ ⊕ x₂·x₃) ko‘rinishida yozish mumkin. Ko‘phaddagi eng ko‘p ko‘paytuvchili hadning ko‘paytuvchilari soni *daraja* deyiladi. Daraja 1 — oddiy chiziqli tenglama, uni Gauss usulida darhol yechish mumkin. Daraja qanchalik katta bo‘lsa, tenglamalar tizimini yechish shunchalik qiyin.")
H3('Jadvallarni qanday o‘qish kerak')
P("4 qatorli o‘n oltilik jadvallar holat massivini ko‘rsatadi: birinchi satr holat[0,0] … holat[0,7], ikkinchi satr holat[1,0] … holat[1,7] va hokazo. Faqat 0 va 1 lardan iborat 4×8 jadvallar 0-qatlamni ko‘rsatadi. «Mos bitlar 32/32» degani nazariy bashorat 32 bitning hammasida haqiqiy qiymat bilan bir xil chiqqanini bildiradi.")

# ============ CHIZIQLI ============
PB(); H1('1. Chiziqli kriptotahlil xulosalari')
L1=R['L1']
H2('1.1. Birinchi xulosa: yutishsiz raundlarda juft/toqlik qatlami to‘liq bashorat qilinadi')
XUL("Yutish nuqtasi bo‘lmagan raundlar (1–7, 10) 0- va 1-bit qatlamlarda c ≈ 1 bilan o‘tadi, ya’ni chiziqli bardoshlilikka hissa qo‘shmaydi; bu barcha variantlar uchun umumiy xossa.")
bolim(
 ["Sodda qilib aytganda: agar biz holatdagi 32 ta sonning faqat juft yoki toqligini bilsak, 1–7-raundlardan keyin ham ularning juft/toqligini hech qanday hisoblashsiz, oddiy jadval (matritsa) yordamida aniq aytib bera olamizmi? Xulosa «ha» deydi: bu raundlarda juft/toqlik qatlami boshqa bitlar bilan aralashmaydi."],
 ["Kriptografik algoritmda har bir raund bitlarni yaxshilab aralashtirishi kerak. Agar 7 ta raunddan keyin ham holatning bir qismini (32 bit) aniq bashorat qilish mumkin bo‘lsa, bu 7 raund xavfsizlik nuqtai nazaridan «bo‘sh» o‘tadi: buzg‘unchi ularni hisobga olmasdan, to‘g‘ridan-to‘g‘ri keyingi raundlarga hujum qilishi mumkin. Demak, algoritmning haqiqiy kuchi qayerda ekanini bilish uchun bu xossani tekshirish shart."],
 ["SBZ-256 varianti, A ilova kaliti va xabari olindi, birinchi blok uchun 0-nuqtadagi yutish bajarildi.",
  "Shu paytdagi holatning juft/toqlik qatlami h₀ yozib olindi.",
  "Har bir akslantirishdan keyin juft/toqlik qatlami nazariy qoida bo‘yicha qog‘ozda hisoblandi: Aralash da h₀ ← M·h₀ (M — kalitning juft/toqligidan tuzilgan 32×32 jadval), SurHolat da bitlar joyini almashtiradi, Qo‘sh va TuzilmaKalit esa juft/toqlikni o‘zgartirmaydi.",
  "Har bir qadamda bashorat haqiqiy holat bilan solishtirildi va mos kelgan bitlar sanaldi.",
  "Qo‘sh o‘zgartirishining 1-bitini ham alohida tekshirish uchun bitta elementning barcha 256 ta qiymati sinab ko‘rildi."])
H3("Kutilgan natija")
P("Nazariya bo‘yicha: 2ⁿ moduli bo‘yicha qo‘shish va ko‘paytirishda natijaning juft/toqligi faqat qo‘shiluvchilarning juft/toqligiga bog‘liq (masalan, toq × toq = toq, juft + toq = toq). Qo‘sh dagi formula x⁻¹ = −A·x·(B + R·x)⁻¹ da A va B doim toq, R esa juft, shuning uchun x⁻¹ ning juft/toqligi x niki bilan bir xil. Demak, 1–7-raundlarning har bir qadamida bashorat 32/32 bo‘lishi, 8-raunddagi SBZ dan keyin esa tasodifiy darajaga (o‘rtacha 16/32) tushishi kutiladi. Qo‘sh ning 1-biti uchun asosiy hisobotda o‘rtacha korrelyatsiya 0,996 deb topilgan, ya’ni deyarli doim chiziqli bo‘lishi kutiladi.")
H3("Olingan natija")
T([4677,4677],[["0-nuqtadagi yutishdan keyingi holat","Uning juft/toqlik qatlami h₀"],[nl(L1['h_bz0']),nl(L1['h0'])]],"Kuzatish boshlanadigan holat",mono=(0,1))
rows=[["Akslantirish","Holat (haqiqiy)","Juft/toqlik qatlami","Mos bitlar"]]
for q in L1['qadamlar']: rows.append([opn[q['amal']],nl(q['holat']),nl(q['qatlam0']),f"{q['mos']}/32"])
T([2100,3150,2350,1754],rows,"1-raundning har bir akslantirishidan keyin",mono=(1,2))
P("Jadvalni o‘qish: masalan, Aralash dan keyin holat[0,0] = bf dan c0 ga o‘zgardi — son butunlay boshqacha bo‘ldi, lekin juft/toqlik bitlari (o‘rtadagi ustun) bashorat bilan 32 tadan 32 tasida mos keldi. Qo‘sh dan keyin c0 → 40 bo‘ldi, ammo juft/toqlik qatlami bitta ham bit o‘zgarmadi. SurHolat dan keyin bitlar joyi o‘zgardi, bu ham bashorat qilingan.")
rm=L1['raund_mos']
T([2600]+[675]*10,[["Raund"]+[str(j) for j in range(1,11)],["Mos bitlar"]+[str(v) for v in rm]],"Raundlar oxirida juft/toqlik bashoratining aniqligi")
p=L1['param']
P(f"Qo‘sh ning 1-biti: A ilovadagi holat[0,0] uchun haqiqiy parametrlar (R = {p['R']}, A₁ = {p['A1']}, B₁ = {p['B1']}, A₂ = {p['A2']}, B₂ = {p['B2']}) bilan 256 ta kirishning hammasida y₁ = x₁ ⊕ x₀ tengligi bajarildi ({L1['y1'][1]}/256), y₀ = x₀ tengligi ham {L1['y0_ok']}/256.")
H3("Kutilgan va olingan natijalarni taqqoslash")
TAQ([["1–7-raundlarda moslik","32/32","32/32 (har bir raundda)","Farq yo‘q. Nazariya to‘liq tasdiqlandi."],
     ["8–10-raundlarda moslik","≈16/32 (tasodifiy)",f"{rm[7]}, {rm[8]}, {rm[9]} /32","Farq kichik. Tasodifiy holatda 32 bitdan o‘rtacha 16 tasi tasodifan mos keladi, chetlanish ±3 bit odatiy hol."],
     ["Qo‘sh: y₀ = x₀","256/256",f"{L1['y0_ok']}/256","Farq yo‘q."],
     ["Qo‘sh: y₁ = x₁ ⊕ δ·x₀","≈255/256 (c ≈ 0,996)",f"{L1['y1'][1]}/256","Olingan natija kutilganidan ham kuchli. Hisobotdagi 0,996 — 200 ta tasodifiy parametr bo‘yicha o‘rtacha; ba’zi parametrlarda 254/256 chiqadi, bu elementda esa 256/256 chiqdi."],
     ["Qo‘sh: 2–7-bitlar korrelyatsiyasi","o‘rtacha 0,77; 0,69; 0,59; 0,46; 0,36; 0,27",", ".join(fz(v,2) for v in L1['bitc'][2:]),"Qiymatlar o‘rtachadan farq qiladi (masalan, 4-bitda 0,88), chunki bu bitta aniq element; o‘rtacha qiymat esa ko‘plab parametrlar bo‘yicha olingan. Asosiy tendensiya (yuqori bitlar sari kamayish) saqlangan."]],
    "1-xulosa: kutilgan va olingan natijalar")
H3("Sodda xulosa")
P("Raundlarda sonlar to‘liq o‘zgaradi, lekin ularning juft/toqligi oddiy jadval bilan oldindan aniq aytiladi. Demak, 1–7-raundlar juft/toqlik qatlamini umuman himoya qilmaydi va algoritmning kuchi faqat yutish nuqtalarida (SBZ yoki BaytZichlash) bo‘ladi. Bu xossa BaytZichlash yoki SBZ tanloviga bog‘liq emas.")

L2=R['L2']
H2('1.2. Ikkinchi xulosa: Standart-128 da xesh qiymatning 32 biti oldindan hisoblanadi')
XUL("Standart-128 da XOR tufayli 0-qatlam butun xesh davomida c = 1 bilan kuzatiladi; bu variant raundlar sonidan qat’i nazar chiziqli kriptotahlilga bardoshli emas.")
bolim(
 ["128 bitli rejimdagi standart variantda yutish nuqtasida oddiy XOR ishlatiladi. XOR juft/toqlikni ham «chiziqli» tarzda qo‘shadi. Demak, 1.1-bo‘limdagi xossa endi yutish nuqtalarida ham buzilmasligi kerak, ya’ni xesh qiymatning juft/toqlik qatlamini xabarning juft/toqlik qatlamidan boshidan oxirigacha aniq hisoblash mumkin bo‘lishi kerak."],
 ["Agar xesh qiymatning 32 biti xabarning oddiy chiziqli funksiyasi bo‘lsa, buzg‘unchi bu bitlarni kalitni bilmasdan ham hisoblay oladi (3.3-bo‘limda ko‘rsatiladi). Bu 128 bitli xesh aslida 96 bitli xesh kabi ishlashini, kolliziya topish esa 2⁶⁴ o‘rniga 2⁴⁸ mehnat talab qilishini anglatadi."],
 ["Standart-128 varianti, kalit — k ning birinchi 16 bayti, 64 baytli A ilova xabari olindi. 128 bitli rejimda blok 16 bayt, shuning uchun xabar 4 ta blok; ularga uzunlik va NY bloklari qo‘shiladi. 1-blok boshlang‘ich holat bo‘ladi, qolgan 5 ta blok uchun 5 ta iteratsiya bajariladi.",
  "Bashorat qoidasiga bitta qadam qo‘shildi: yutish nuqtasida yangi juft/toqlik = eski juft/toqlik ⊕ blokning juft/toqligi.",
  "Har bir iteratsiyaning 55 ta akslantirishidan keyin bashorat haqiqiy holat bilan solishtirildi.",
  "Oxirida bashorat qilingan juft/toqlik qatlami haqiqiy xesh qiymat bilan solishtirildi."])
H3("Kutilgan natija")
P("Qo‘sh(holat, blok) juft/toqlikni o‘zgartirmaydi, XOR esa juft/toqliklarni qo‘shadi, raundlar esa 1.1-bo‘limdagidek chiziqli. Shuning uchun barcha 5 × 55 = 275 ta qadamda moslik 32/32 bo‘lishi va yakuniy xesh qiymatning juft/toqlik qatlami to‘liq bashorat qilinishi kerak.")
H3("Olingan natija")
names={1:'2-blok',2:'3-blok',3:'4-blok',4:'uzunlik bloki',5:'NY bloki'}
rows=[["Iteratsiya","Kirish bloki","Akslantirishlar soni","Eng yomon moslik"]]
for j in L2['jurnal']: rows.append([str(j['iteratsiya']),names[j['iteratsiya']],str(j['amallar']),f"{j['min_mos']}/32"])
T([1700,2400,2750,2504],rows,"Standart-128: barcha iteratsiyalar bo‘yicha bashorat aniqligi")
T([4677,4677],[["Xesh qiymatning haqiqiy juft/toqlik qatlami","Bashorat"],[nl(L2['haqiqiy']),nl(L2['bashorat'])]],f"Yakuniy xesh qiymat ({L2['xesh']})",mono=(0,1))
H3("Kutilgan va olingan natijalarni taqqoslash")
TAQ([["275 ta qadamdagi moslik","32/32","32/32 (har birida)","Farq yo‘q."],
     ["Yakuniy xesh juft/toqlik qatlami","to‘liq bashorat",f"{L2['mos']}/32","Farq yo‘q. Xesh qiymatning o‘zi standart nazorat qiymati bilan ham mos keldi, ya’ni tajriba haqiqiy algoritmda o‘tkazilgan."]],
    "2-xulosa: kutilgan va olingan natijalar")
H3("Sodda xulosa")
P("Standart-128 da xesh qiymatning har bir yarim baytidagi juft/toqlik biti (jami 32 bit) xabarning juft/toqlik bitlaridan oddiy XOR va jadval yordamida aniq hisoblanadi. Raundlar sonini oshirish bu kamchilikni tuzatmaydi, chunki har bir raund ham chiziqli. Uni faqat yutish nuqtasidagi XOR ni chiziqli bo‘lmagan amal (SBZ) bilan almashtirish yo‘qotadi.")

L3=R['L3']
H2('1.3. Uchinchi xulosa: Standart-256 da har bir faol bayt korrelyatsiyani faqat 4 marta kamaytiradi')
XUL("Standart-256 da har bir faol bayt ≤ 2⁻² hissa qo‘shadi; 2⁻⁶⁴ chegarasiga mediana kalitlarda 5–6 yutish qatlamidan keyin (≈19-raund) erishiladi, eng yomon kalitlarda amalda erishilmaydi.")
bolim(
 ["Standart-256 da yutish nuqtasida B ilovadagi Z jadvali ishlaydi. Buzg‘unchi yutish nuqtasidan o‘tadigan chiziqli tenglama qurmoqchi bo‘lsa, bu tenglama har bir faol bayt uchun qanchalik «zaiflashadi»? Xulosa: eng yaxshi holatda faqat 4 marta (c = 2⁻² = 0,25). So‘ngra butun algoritm uchun nechta yutish nuqtasidan keyin korrelyatsiya xavfsiz darajaga (2⁻⁶⁴) tushishi baholanadi."],
 ["Yutish nuqtalari algoritmning yagona himoya qatlami (1.1-bo‘lim). Agar har bir qatlam faqat 4 marta zaiflashtirsa, xavfsiz darajaga yetish uchun ko‘p qatlam kerak bo‘ladi. Bu esa xabarning ko‘p bloklari kerakligini yoki ayrim kalitlarda umuman xavfsiz darajaga erishilmasligini bildiradi."],
 ["Z jadvali uchun eng yaxshi chiziqli tenglama z₀ ⊕ z₂ = x₀ ⊕ x₂ ⊕ x₆ ⊕ x₇ ning nechta kirishda bajarilishi 256 ta kirishning hammasida sanaldi.",
  "Xuddi shu tenglama haqiqiy algoritmning yutish nuqtasida 20000 ta tasodifiy holatda o‘lchandi.",
  "A ilova kaliti uchun «iz» qurildi: chiziqli tenglama yutish qatlamlari 0, 8, 9, 0′, 8′, 9′ dan o‘tganda har bir qatlamda nechta faol bayt paydo bo‘lishi hisoblandi.",
  "Chegara: log₂|c| ≤ −2 × (faol baytlar soni)."])
H3("Kutilgan natija")
P("Asosiy hisobotdagi to‘liq hisobga ko‘ra Z jadvalida eng yaxshi tenglama 256 ta kirishdan 160 tasida bajariladi, ya’ni c = 2·160/256 − 1 = 0,25. Algoritmda ham taxminan 0,25 o‘lchanishi kerak. Faol baytlar soni uchun hisobotda 120 ta tasodifiy kalit bo‘yicha mediana qiymatlar topilgan: 1, 2, 3, 15, 31,5 va 46 (1 dan 6 tagacha qatlam uchun). Shunga o‘xshash qiymatlar kutiladi.")
H3("Olingan natija")
z=L3['zanjir']
rows=[["Qatlamlar","Faol baytlar (A ilova kaliti)","Hisobotdagi mediana","log₂|c| chegarasi","Faol pozitsiyalar"]]
med={'1':'1','2':'2','3':'3','4':'15','5':'31,5','6':'46'}
for kk in map(str,range(1,7)):
    a,path=z[kk]; rows.append([kk,str(a),med[kk],str(-2*a),"; ".join("{"+",".join(f"[{i//8},{i%8}]" for i in pth)+"}" for pth in path)])
T([1300,1900,1600,1600,2954],rows,"Standart-256: A ilova kaliti uchun yutish qatlamlaridagi faol baytlar")
H3("Kutilgan va olingan natijalarni taqqoslash")
TAQ([["Z tenglamasi bajarilgan kirishlar","160/256",f"{L3['agree']}/256","Farq yo‘q."],
     ["Z tenglamasi korrelyatsiyasi","0,25",fz(L3['cZ'],2),"Farq yo‘q."],
     ["Algoritmda o‘lchangan korrelyatsiya","0,25",fz(L3['c_meas'],3),"Farq 0,004. Bu tanlanma xatoligi: 20000 ta tajribada taxminiy xatolik ≈1/√20000 ≈ 0,007, olingan farq undan kichik."],
     ["1–3 qatlamda faol baytlar","1, 2, 3","1, 2, 3","Farq yo‘q."],
     ["4–6 qatlamda faol baytlar","15; 31,5; 46 (mediana)","4; 5; 6","Katta farq. Sababi: A ilova kaliti «eng yomon» kalitlar sinfiga kiradi (pastda izohlangan)."]],
    "3-xulosa: kutilgan va olingan natijalar")
P("*Katta farqning sababi.* A ilova kaliti uchun L jadvalining (bir raundning juft/toqlik matritsasi) [0,3] satrida faqat bitta 1 bor va u yana [0,3] ustunda turadi. Bu degani: holat[0,3] ning juft/toqlik biti har raundda o‘zgarmay o‘sha joyda qoladi. Jadvaldagi «faol pozitsiyalar» ustunida ham hamma joyda faqat [0,3] turganini ko‘rasiz. Shuning uchun buzg‘unchi shu bitta pozitsiya orqali iz quradi va har bir yutish qatlamida atigi bitta faol bayt «to‘laydi». Odatiy kalitlarda esa juft/toqlik matritsasi bitni ko‘plab pozitsiyalarga tarqatadi va 4-qatlamdan boshlab faol baytlar soni keskin oshadi (mediana 15). Bu farq xulosani inkor etmaydi, aksincha, uning ikkinchi qismini («eng yomon kalitlarda amalda erishilmaydi») tasdiqlaydi.")
H3("Sodda xulosa")
P("Standart Z jadvali har bir faol bayt uchun buzg‘unchidan juda kam «to‘lov» oladi (4 marta). Odatiy kalitda xavfsiz darajaga 5–6 ta yutish qatlamidan keyin yetiladi, A ilova kaliti kabi kalitlarda esa 32 ta qatlam kerak bo‘ladi, bu amalda erishib bo‘lmaydigan miqdor.")

L4=R['L4']
H2('1.4. To‘rtinchi xulosa: SBZ da har bir faol bayt korrelyatsiyani 64 marta kamaytiradi')
XUL("SBZ-256 da har bir faol bayt ≤ 2⁻⁶ hissa qo‘shadi; 2⁻⁶⁴ chegarasiga mediana kalitlarda 4 ta yutish qatlamidan keyin (≈11-raund) erishiladi; eng yomon kalitlarda 11 ta qatlam (≈4 ta iteratsiya) kerak.")
bolim(
 ["Xuddi 1.3-bo‘limdagi savol, lekin SBZ uchun: SBZ dan o‘tadigan eng yaxshi chiziqli tenglama qanchalik kuchli? Nazariya bo‘yicha SBZ ichidagi ikkita S-box korrelyatsiyalari ko‘paytiriladi: c = c_S(α→γ)·c_S(β→α). Har bir S-box uchun eng yaxshi korrelyatsiya 2⁻³, demak SBZ uchun 2⁻³ × 2⁻³ = 2⁻⁶."],
 ["Agar har bir faol bayt 64 marta zaiflashtirsa (Z dagi 4 marta o‘rniga), xavfsiz darajaga ancha kam qatlamda yetiladi. Bu SBZ ning asosiy afzalligi va uni raqamlar bilan tekshirish kerak."],
 ["SBZ uchun eng yaxshi tenglamalardan biri y₀ ⊕ (h₀ ⊕ h₂ ⊕ h₃ ⊕ h₅) ⊕ (n₁ ⊕ n₃ ⊕ n₄) = 1 barcha 65536 ta (h, n) juftlikda tekshirildi.",
  "Formuladagi ikkita S-box korrelyatsiyasi alohida hisoblanib, ko‘paytmasi olindi.",
  "A ilova kaliti va tasodifiy tanlangan odatiy kalit uchun faol baytlar zanjiri (1.3-bo‘limdagidek) qurildi; chegara: log₂|c| ≤ −6 × (faol baytlar)."])
H3("Kutilgan natija")
P("Tenglama korrelyatsiyasi aniq ±2⁻⁶ = ±0,015625 bo‘lishi kerak (bu 65536 juftlikdan 32768 ± 512 tasida bajarilishini anglatadi). Faol baytlar zanjiri yutish o‘zgartirishiga bog‘liq emas, shuning uchun A ilova kaliti uchun 1.3-bo‘limdagi qiymatlar (1, 2, …, 6) takrorlanishi, odatiy kalit uchun esa hisobotdagi medianaga yaqin qiymatlar chiqishi kutiladi.")
H3("Olingan natija")
za=L4['zanjir_A']; zy=L4['yomon']
rows=[["Qatlamlar","A ilova kaliti: faol baytlar","chegara log₂|c|","Odatiy kalit: faol baytlar","chegara log₂|c|"]]
for kk in map(str,range(1,7)): rows.append([kk,str(za[kk]),str(-6*za[kk]),str(zy[kk][0]),str(-6*zy[kk][0])])
T([1500,2050,1800,2200,1804],rows,"SBZ-256: yutish qatlamlari bo‘yicha chegaralar")
H3("Kutilgan va olingan natijalarni taqqoslash")
TAQ([["Tenglama bajarilgan juftliklar","32768 ± 512",f"{L4['ones']} (chap tomon = 1)","32768 + 512 = 33280. Farq yo‘q."],
     ["Korrelyatsiya","±0,015625","−0,015625","Kattaligi to‘liq mos. Manfiy ishora — tenglamaning teskarisi (o‘ng tomoni 0) 2⁻⁶ ustunlik bilan bajarilishini bildiradi; buzg‘unchi uchun bu bir xil darajada foydali, shuning uchun |c| muhim."],
     ["c_S(2D→01) · c_S(1A→2D)","2⁻³ · 2⁻³","−0,125 · 0,125","Formula tasdiqlandi."],
     ["A ilova kaliti: 4 qatlamda","4 (1.3-bo‘limdagidek)",str(za['4']),"Farq yo‘q. Eng yomon kalitda SBZ bilan ham 4 qatlamda chegara faqat 2⁻²⁴."],
     ["Odatiy kalit: 4 qatlamda","≈15 (mediana)",str(zy['4'][0]),"Farq kichik: 18 — tasodifiy kalitlar taqsimotida medianadan biroz yuqori, odatiy qiymat. Chegara 2⁻¹⁰⁸, ya’ni 2⁻⁶⁴ dan ancha kichik."]],
    "4-xulosa: kutilgan va olingan natijalar")
H3("Sodda xulosa")
P("SBZ har bir faol bayt uchun buzg‘unchidan Z ga qaraganda 16 baravar ko‘p to‘lov oladi (2⁻⁶ va 2⁻²). Odatiy kalitda xavfsiz darajaga 4-yutish qatlamida, ya’ni taxminan 11-raundda erishiladi. A ilova kaliti kabi «eng yomon» kalitlarda bu kamida 11 ta qatlamni talab qiladi; bu SBZ ning emas, Aralash ning tuzilishi bilan bog‘liq kamchilik.")

L5=R['L5']
H2('1.5. Beshinchi xulosa: xesh qiymatda har doim bajariladigan tengliklar bor va SBZ ularni yo‘qotmaydi')
XUL("Chiqish 0-qatlamidagi c = 1 munosabatlar (o‘rtacha ≈6 ta) SBZ ga bog‘liq emas va Aralash o‘zgartirishining 2 moduli bo‘yicha degeneratsiyasidan kelib chiqadi.")
bolim(
 ["Oxirgi, 10-raund oxirgi yutish nuqtasidan keyin keladi. Unda Aralash bajariladi va juft/toqlik qatlamiga L jadvali bilan ta’sir qiladi. Agar L «to‘liq» bo‘lmasa (rangi 32 dan kichik bo‘lsa), xesh qiymatning juft/toqlik bitlari orasida har doim bajariladigan tengliklar paydo bo‘ladi, masalan «[0,4] va [1,5] baytlarning juft/toqligi doim bir xil». Tekshiriladi: bunday tengliklar bormi va ular SBZ ga bog‘liqmi?"],
 ["Yaxshi xesh funksiyaning chiqishi tasodifiy ko‘rinishi kerak. Agar chiqishda doim bajariladigan 8 ta tenglik bo‘lsa, buzg‘unchi bitta xesh qiymatga qarab uning shu algoritm natijasi ekanini 255/256 aniqlik bilan aniqlay oladi. Kalitsiz rejimda kalit hammaga ma’lum, demak tengliklar ham hammaga ma’lum."],
 ["A ilova kaliti uchun L jadvalining rangi va «bo‘sh yo‘nalishlari» (wᵀ·L = 0 bo‘lgan w vektorlar) topildi; har bir w xesh qiymatda bitta tenglikni beradi.",
  "1000 ta tasodifiy 64 baytli xabar Standart-256 va SBZ-256 bilan xeshlandi va har bir tenglik tekshirildi."])
H3("Kutilgan natija")
P("Hisobotda 200 ta kalit bo‘yicha L ning o‘rtacha rangi 25,8 (16 dan 31 gacha), ya’ni o‘rtacha 32 − 25,8 ≈ 6 ta tenglik kutiladi; aniq soni kalitga bog‘liq. Har bir tenglik 1000 ta xabarning hammasida (ulush 1,000) bajarilishi va natija ikkala variantda bir xil bo‘lishi kerak, chunki tengliklar faqat oxirgi Aralash dan kelib chiqadi.")
H3("Olingan natija")
rows=[["№","Tenglik (xesh qiymatning juft/toqlik bitlari)","Standart-256","SBZ-256"]]
for i,m in enumerate(L5['munosabatlar']): rows.append([str(i+1)," ⊕ ".join(m)+" = 0",fz(L5['tekshiruv']['std'][i],3),fz(L5['tekshiruv']['sbz'][i],3)])
T([700,5254,1700,1700],rows,f"A ilova kaliti uchun tengliklar (rang L = {L5['rang']}) va 1000 ta xabarda bajarilish ulushi")
H3("Kutilgan va olingan natijalarni taqqoslash")
TAQ([["Tengliklar soni","≈6 (kalitga bog‘liq)",str(len(L5['munosabatlar'])),f"A ilova kaliti uchun rang L = {L5['rang']}, shuning uchun 32 − {L5['rang']} = 8. Bu o‘rtachadan biroz ko‘p, lekin hisobotdagi 1–16 oralig‘ida."],
     ["Bajarilish ulushi (Standart)","1,000","1,000 (8 tasida)","Farq yo‘q."],
     ["Bajarilish ulushi (SBZ)","1,000","1,000 (8 tasida)","Farq yo‘q — SBZ tengliklarni yo‘qotmadi."],
     ["Doimiy nol bitlar","kalitlarning ≈yarmida bor","yo‘q","Farq emas: bu kalitda L da nol satr yo‘q, shuning uchun doimiy bitlar paydo bo‘lmadi."]],
    "5-xulosa: kutilgan va olingan natijalar")
H3("Sodda xulosa")
P("A ilova kaliti bilan hisoblangan har qanday xesh qiymatda, masalan, [0,4] va [1,5] baytlarning juft/toqligi doim bir xil. Bunday 8 ta tenglik SBZ bilan ham, standart bilan ham bajariladi, chunki ular oxirgi raunddagi Aralash dan kelib chiqadi. Bu kamchilikni tuzatish uchun Aralash ni o‘zgartirish kerak.")

# ============ DIFFERENSIAL ============
PB(); H1('2. Differensial kriptotahlil xulosalari')
D1=R['D1']
H2('2.1. Birinchi xulosa: yutishsiz raundlarda kichik farq deyarli o‘zgarmay o‘tadi')
XUL("1–7- va 10-raundlar MSB izlarini ≈0,85–0,94 ehtimollik bilan o‘tkazadi; differensial bardoshlilik faqat yutish nuqtalarida hosil bo‘ladi.")
bolim(
 ["Ikkita holat olinadi: ular faqat bitta baytning eng katta biti (MSB) bilan farq qiladi. Tekshiriladi: bu farq raundlardan o‘tganda butun holatga «yoyilib» ketadimi (yaxshi algoritmda shunday bo‘lishi kerak) yoki tartibli ko‘rinishda, faqat MSB bitlarda qoladimi."],
 ["Agar farq raundlardan oldindan aytib beriladigan ko‘rinishda o‘tsa, buzg‘unchi bundan kolliziya (ikki xil xabar uchun bir xil xesh) qidirishda foydalanadi. Demak, raundlar farqni qanchalik tez «buzishini» bilish kerak."],
 ["SBZ-256, A ilova kaliti; 0-nuqtadagi yutishdan keyingi holat va undan holat[0,0] ning MSB biti bilan farq qiladigan ikkinchi holat olindi.",
  "Ikkala holat bir xil kalit bilan raundlardan o‘tkazildi va har bir akslantirishdan keyin farq yozib borildi.",
  "Bitta misol tasodifiy bo‘lishi mumkinligi uchun tajriba 3000 ta tasodifiy juftlikda takrorlandi va farq «faqat MSB» ko‘rinishida qolgan juftliklar ulushi sanaldi."])
H3("Kutilgan natija")
P("Nazariya bo‘yicha 2⁸ moduli bo‘yicha qo‘shish va ko‘paytirishda MSB dagi farq ko‘chirish hosil qilmaydi: (x + 128)·c ≡ x·c + 128·(c mod 2). Shuning uchun Aralash da MSB farqi ehtimollik 1 bilan saqlanadi va M jadvali bo‘yicha boshqa baytlarga tarqaladi. Qo‘sh da ham MSB farqi deyarli doim saqlanadi (254/256). Faqat Qo‘sh dagi maxsus holatlar (nol qiymatni almashtirish, Δ = 10 tuzatmasi, yig‘indilar juftligining o‘zgarishi) izni buzishi mumkin. Hisobotda har raundda ≈0,85–0,94 saqlanish ehtimolligi va 7 raunddan keyin ≈0,34 topilgan. 8-raunddagi SBZ izni to‘liq buzishi kutiladi.")
H3("Olingan natija")
rows=[["Raund, akslantirish","Farq (Δholat)","Faol baytlar (holat / kₑ)","Faqat MSB?"]]
for q in D1['qadam']: rows.append([f"{q['raund']}: {opn[q['amal']]}",nl(q['dh']),f"{q['faol']} / {q['faol_ke']}","ha" if q['msb'] else "yo‘q"])
T([2600,3300,1900,1554],rows,"Misoldagi juftlik: 1- va 2-raundlarda farqning o‘tishi",mono=(1,))
P("Jadvalni o‘qish: 1-raundda Aralash bitta 80 farqini ikkita baytga ([1,0] va [2,0]) tarqatdi, Qo‘sh ularni o‘zgartirmadi, SurHolat ularni [0,2] va [2,3] ga ko‘chirdi. 2-raundda Aralash farqni 4 ta baytga tarqatdi. Hamma joyda farq faqat 80 ko‘rinishida qoldi.")
xs=D1['xulosa']; st=D1['stat']
T([2900]+[645]*10,[["Raund"]+[str(r_['raund']) for r_ in xs],["Misol: faol baytlar"]+[str(r_['faol']) for r_ in xs],["Misol: faqat MSB?"]+["ha" if r_['msb'] else "yo‘q" for r_ in xs],["3000 juftlik: P(faqat MSB)"]+[fz(v,3) for v in st]],"Raundlar oxirida: bitta misol va 3000 juftlik statistikasi")
H3("Kutilgan va olingan natijalarni taqqoslash")
TAQ([["Aralash da MSB farqi","ehtimollik 1, M bo‘yicha tarqaladi","1-raundda 1 → 2 bayt, 2-raundda 2 → 4 bayt, hammasi 80","Farq yo‘q."],
     ["Misolda iz necha raund saqlandi","o‘rtacha 3–4 raund","2 raund, 3-raundda buzildi","Farq emas. 3 raund saqlanish ehtimolligi 0,70; demak taxminan har uchinchi juftlikda iz 3-raundgacha buziladi. Bitta misolda bu tasodif, shuning uchun xulosa statistika bilan tekshirildi."],
     ["1-raunddan keyin P","0,94",fz(st[0],3),"Farq yo‘q."],
     ["7-raunddan keyin P","≈0,34",fz(st[6],3),"Farq 0,003 — tanlanma xatoligi (3000 juftlikda ≈ ±0,009)."],
     ["8-raunddan (SBZ) keyin P","≈0 (iz buziladi)",fz(st[7],3),f"0 emas, chunki {fz(st[7]*100,1)}% juftliklarda farq butunlay yo‘qolgan (ikkala holat bir xil bo‘lib qolgan). «Farq nol» ham rasman «faqat MSB» shartini qanoatlantiradi. Bu hodisa 2.4-bo‘limda tushuntiriladi."]],
    "2.1-xulosa: kutilgan va olingan natijalar")
H3("Sodda xulosa")
P("Bitta bitdagi farq birinchi raundlarda tartibli ko‘rinishda qoladi va 7 raunddan keyin ham taxminan har uchinchi juftlikda oldindan aytib beriladigan ko‘rinishda bo‘ladi. Demak, oddiy raundlar farqni yaxshi aralashtirmaydi; farqni haqiqatan «buzadigan» joy — 8-raunddagi yutish nuqtasi.")

D2=R['D2']
H2('2.2. Ikkinchi xulosa: SBZ farqni yo‘qotib bo‘lmaydigan qiladi')
XUL("SBZ yutish nuqtasidagi maksimal ehtimollikni 0,156 (Standart-256) va 1 (Standart-128) dan 2⁻⁶ gacha kamaytiradi va bitta argumentdagi ayirmaning so‘nishini imkonsiz qiladi.")
bolim(
 ["Yutish nuqtasida ikkita qiymat birlashtiriladi: holat bayti h va xabar bayti n. Kolliziya uchun buzg‘unchi farqni shu joyda «yo‘qotishga» (so‘ndirishga) urinadi: ikki xil kirish bir xil chiqish bersin. Tekshiriladi: buni qanchalik oson qilish mumkin — Z da, XOR da va SBZ da."],
 ["Agar farqni yutish nuqtasida oson yo‘qotish mumkin bo‘lsa, kolliziya ham oson topiladi. Shuning uchun yutish nuqtasidagi «farqni yo‘qotish ehtimolligi» xesh funksiyaning kolliziyaga bardoshliligini bevosita belgilaydi."],
 ["A ilova ma’lumotlaridan h = " + f"{D2['h']:#04x}" + " va n = " + f"{D2['n']:#04x}" + " olindi, n ning MSB biti o‘zgartirildi va ikkala variantda natijalar solishtirildi.",
  "Z jadvalining tuzilishi (lotin kvadrati) tekshirildi.",
  "Z uchun 96 farqining necha marta yo‘qolishi sanaldi.",
  "SBZ uchun h bir xil, n esa har xil bo‘lgan barcha 255 × 65536 ta juftlik tekshirildi: qaysi birida chiqish bir xil bo‘ladi?"])
H3("Kutilgan natija")
P("Nazariya: Z — lotin kvadrati, ya’ni har bir satr va ustunda 0…15 sonlari bir martadan uchraydi. Shuning uchun faqat bitta yarim baytdagi farq Z da yo‘qolmaydi, lekin ikkala yarim baytdagi farq (masalan, 96) yo‘qolishi mumkin; ayirmalar matritsasiga ko‘ra 96 farqi 256 tadan 40 ta kirishda yo‘qoladi (0,156). SBZ da n → S(h ⊕ S(n)) o‘rin almashtirish (har xil n uchun har xil natija), shuning uchun h bir xil bo‘lsa, farq hech qachon yo‘qolmasligi kerak (0 marta). Ikkala argumentda farq bo‘lsa, yo‘qolish ehtimolligi 2⁻⁷ chiqishi kerak. XOR da h va n farqlari teng bo‘lsa, farq doim yo‘qoladi.")
H3("Olingan natija")
T([3000,3177,3177],[["Variant","n uchun natija","n ⊕ 80 uchun natija va farq"],
   ["Standart-256: Z(h) ‖ Z(n)",f"{D2['std'][0]:#04x}",f"{D2['std'][1]:#04x}, farq {D2['std'][0]^D2['std'][1]:#04x}"],
   ["SBZ: S(h ⊕ S(n))",f"{D2['sbz'][0]:#04x}",f"{D2['sbz'][1]:#04x}, farq {D2['sbz'][0]^D2['sbz'][1]:#04x}"]],"Yutish nuqtasida bitta argumentdagi farq")
P("Standart-256 da farq faqat quyi yarim baytda qoldi (06): yuqori yarim bayt faqat h ga bog‘liq va h o‘zgarmagan. SBZ da farq butun baytga tarqaldi (3f).")
H3("Kutilgan va olingan natijalarni taqqoslash")
TAQ([["Z — lotin kvadrati","ha","ha" if D2['lotin'] else "yo‘q","Farq yo‘q."],
     ["Z: 96 farqi yo‘qoladigan kirishlar","40/256",f"{D2['v96']}/256","Farq yo‘q (masalan, x = 07: Z(07) = Z(91) = 8)."],
     ["SBZ: h bir xil, n har xil — yo‘qolishlar","0",str(D2['sbz_sonish_bir']),"Farq yo‘q. 16 711 680 ta juftlikning birortasida ham farq yo‘qolmadi."],
     ["SBZ: ikkala argumentda 80 farqi","2⁻⁷ (512/65536)",f"{D2['sbz_sonish_80']}/65536","Farq yo‘q."],
     ["Eng katta o‘tish ehtimolligi","Z: 0,156; SBZ: 2⁻⁶; XOR: 1","Z: 40/256; S: 4/256","Farq yo‘q."]],
    "2.2-xulosa: kutilgan va olingan natijalar")
H3("Sodda xulosa")
P("SBZ da holat yoki xabar baytlaridan faqat bittasi farq qilsa, natija albatta farq qiladi: farqni bu nuqtada yo‘qotib bo‘lmaydi. Standart Z da esa farq har 6–7 urinishdan birida yo‘qolishi mumkin, XOR da esa buni har doim qilish mumkin. Bu SBZ ning kolliziyalarga qarshi eng muhim afzalligi.")

D3=R['D3']
H2('2.3. Uchinchi xulosa: SBZ variantlari 8-raunddayoq xavfsiz darajaga yetadi')
XUL("SBZ-256 va SBZ-128 birinchi iteratsiyaning 8-raundidan keyin differensial chegaraga (mos ravishda 2⁻¹²⁸ va 2⁻⁶⁴) erishadi; Standart-256 — 9-raunddan keyin; Standart-128 esa raundlar sonidan qat’i nazar bardoshli emas.")
bolim(
 ["Buzg‘unchi kolliziya uchun eng qulay farqni tanlaydi: xabar blokining ikkita baytidagi MSB bitlari. Bunday farq Qo‘sh dagi yig‘indilarni o‘zgartirmaydi va birinchi qadamlardan oson o‘tadi. Tekshiriladi: bu farq to‘rttala variantda qanday tarqaladi va yutish nuqtalarigacha nechta faol bayt hosil qiladi; shu asosda «farqning to‘liq izdan o‘tish ehtimolligi» qaysi raundda xavfsiz darajaga tushishi hisoblanadi."],
 ["Xavfsiz daraja: 256 bitli xesh uchun 2⁻¹²⁸, 128 bitli uchun 2⁻⁶⁴. Agar ehtimollik bundan katta bo‘lsa, buzg‘unchi kolliziyani oddiy «tug‘ilgan kunlar» usulidan tezroq topishi mumkin."],
 ["A ilova kaliti va xabari; 2-blokning 0- va 9-elementlariga MSB farqi kiritildi (256 bitli rejimda 80, 128 bitli rejimda 8).",
  "Farq 0-nuqtadan 9-raund yutishigacha har bir variantda kuzatildi.",
  "8- va 9-yutish nuqtalariga kirishdagi faol baytlar sanaldi.",
  "Chegara: log₂p ≤ −(faol bayt boshiga to‘lov) × (faol baytlar). To‘lov: SBZ — 6 bit, Z — 2,68 bit (log₂(256/40)), XOR — 0 bit."])
H3("Kutilgan natija")
P("Qo‘sh(0-nuqta) da holatda farq paydo bo‘lmasligi kerak (ehtimollik 1). Yutishdan keyin: XOR farqni o‘zgarishsiz o‘tkazadi (8 va 8), Z faqat quyi yarim baytda farq beradi, SBZ esa butun baytlarda farq beradi. Birinchi raunddan keyin farq deyarli butun holatga tarqalishi va 8-nuqtaga ≈27–32 ta faol bayt bilan yetishi kutiladi. Hisobotda (27 ta faol bayt bilan) chegaralar: SBZ-256 — 2⁻¹⁶², Standart-256 — 2⁻⁷² (8-nuqta) va 2⁻¹⁵⁶ (8+9), Standart-128 — 1.")
H3("Olingan natija")
lab={'256_std':'Standart-256','256_sbz':'SBZ-256','16_std':'Standart-128','16_sbz':'SBZ-128'}
rows=[["Variant","Qo‘sh(0): holatda faol","Yutishdan keyingi farq","1-raund","8-nuqtada","9-nuqtada"]]
for k_,v in D3.items(): rows.append([lab[k_],str(v['faol_q0']),nl(v['dbz0']),str(v['r1']),str(v['a8']),str(v['a9'])])
T([1700,1350,2700,1100,1250,1254],rows,"Xabardagi ikki elementli MSB farqining tarqalishi (faol elementlar soni)",mono=(2,))
rows=[["Variant","8-nuqtadan keyin log₂p ≤","8 va 9 dan keyin log₂p ≤","Talab","Xulosa"]]
treb={'256_std':-128,'256_sbz':-128,'16_std':-64,'16_sbz':-64}
for k_,v in D3.items():
    t_=treb[k_]; x8=v['chegara8']<=t_; x9=v['chegara89']<=t_
    rows.append([lab[k_],fz(v['chegara8'],1),fz(v['chegara89'],1),str(t_),"8-raunddan keyin" if x8 else ("9-raunddan keyin" if x9 else "bardoshli emas")])
T([1800,2100,2100,1200,2154],rows,"Misoldagi faol baytlar asosida chegaralar")
H3("Kutilgan va olingan natijalarni taqqoslash")
TAQ([["Qo‘sh(0) dan keyin holatda faol","0 (to‘rttala variant)","0, 0, 0, 0","Farq yo‘q."],
     ["Yutishdan keyingi farq (Standart-128)","8 va 8 (XOR)","8 va 8","Farq yo‘q."],
     ["8-nuqtada faol elementlar","≈27–32","32, 31, 31, 28","Farq yo‘q, oraliq ichida."],
     ["SBZ-256 chegarasi (8-nuqta)","2⁻¹⁶² (27 bayt bilan)",f"2^{D3['256_sbz']['chegara8']:.0f} (31 bayt bilan)","Hisobotda ehtiyotkorlik uchun 27 bayt olingan; bu misolda faol baytlar ko‘proq (31), shuning uchun chegara yanada kichik. Xulosa o‘zgarmaydi: 2⁻¹²⁸ dan kichik."],
     ["Standart-256 chegarasi","2⁻⁷² / 2⁻¹⁵⁶",f"2^{D3['256_std']['chegara8']:.0f} / 2^{D3['256_std']['chegara89']:.0f}","Xuddi shu sabab (32 faol bayt). 8-nuqtadan keyin hali talabdan katta, 9-nuqtadan keyin kichik — xulosa tasdiqlandi."],
     ["Standart-128 chegarasi","0 (XOR to‘lov olmaydi)","0","Farq yo‘q."]],
    "2.3-xulosa: kutilgan va olingan natijalar")
H3("Sodda xulosa")
P("SBZ bilan farq birinchi iteratsiyaning 8-raundidayoq shunchalik ko‘p faol baytdan o‘tadiki, uni oldindan aytib berish ehtimolligi xavfsiz darajadan ancha kichik bo‘ladi. Standart-256 ga buning uchun bitta qo‘shimcha yutish nuqtasi (9-raund) kerak. Standart-128 da esa XOR farqni hech qachon «jazolamaydi».")

D4=R['D4']; s_,u_=D4['pozitsiya']
H2('2.4. To‘rtinchi xulosa: ayrim kalitlarda farq Aralash da izsiz yo‘qoladi')
XUL("Aralash yadrosi orqali ayirmaning ehtimollik 1 bilan so‘nishi SBZ ga bog‘liq bo‘lmagan qoldiq xavf hisoblanadi; uni bartaraf etish uchun Aralash/TuzilmaKalit o‘zgartirishlarini qayta ko‘rib chiqish talab qilinadi.")
bolim(
 ["Aralash holatni kalitdagi sonlarga ko‘paytiradi. MSB farqi (128) juft songa ko‘paytirilsa, 128·juft = 256·(…) ≡ 0 (mod 256), ya’ni farq yo‘qoladi. Agar biror holat baytiga mos kalit ustunidagi barcha sonlar juft bo‘lsa, shu baytdagi MSB farqi Aralash dan keyin butunlay yo‘qolishi kerak. Natijada ikki xil holat bir xil holatga aylanadi. Tekshiriladi: bu haqiqatan sodir bo‘ladimi?"],
 ["Ikki xil ichki holatning bir xil holatga aylanishi — *ichki kolliziya*. Agar buzg‘unchi shunday farqni hosil qila olsa, keyingi barcha hisoblar bir xil bo‘ladi va xesh qiymatlar ham bir xil chiqadi. Bu hodisa yutish nuqtasidan oldin, Aralash da sodir bo‘ladi, shuning uchun SBZ uni to‘xtata olmaydi."],
 ["Tasodifiy kalitlar orasidan juft/toqlik jadvali M da nol ustun bo‘lgan kalit qidirildi.",
  f"Nol ustunga mos holat bayti (holat[{s_},{u_}]) va unga ko‘paytiriladigan kalit sonlari ko‘rib chiqildi.",
  "Tasodifiy holat va undan shu baytning MSB biti bilan farq qiladigan holat raundlardan o‘tkazildi."])
H3("Kutilgan natija")
P(f"holat[{s_},{u_}] ga ko‘paytiriladigan kₑ[i,{u_}] sonlarining hammasi juft bo‘lishi; Aralash dan keyingi farq to‘liq nol bo‘lishi; keyingi barcha raundlarda (10-raundgacha) holatlar bir xil qolishi kutiladi. Hisobot statistikasi: tasodifiy kalitlarning taxminan yarmida bunday nol ustun bor.")
H3("Olingan natija")
P(f"Topilgan kalit: {D4['kalit'][:32]}… Nol ustunlar: {', '.join(D4['nol_ustunlar'])}. Tanlangan pozitsiya holat[{s_},{u_}]; unga mos kalit sonlari: {', '.join(hex(v) for v in D4['kcol'])}.")
T([4677,4677],[["Aralash dan oldingi farq","Aralash dan keyingi farq"],[nl([' '.join('80' if (i==s_ and j==u_) else '00' for j in range(8)) for i in range(4)]),nl(D4['d_aralash'])]],"Farqning Aralash da yo‘qolishi",mono=(0,1))
H3("Kutilgan va olingan natijalarni taqqoslash")
TAQ([["Kalit ustunidagi sonlar","hammasi juft","f0, a0, 56, f6 — hammasi juft","Farq yo‘q."],
     ["Aralash dan keyingi farq","to‘liq nol","to‘liq nol (32 bayt)","Farq yo‘q."],
     ["10-raunddan keyingi farq","nol (holat va kₑ)","nol" if D4['oxir_nol'] else "nol emas","Farq yo‘q: ikki xil holat bitta raunddan keyin butunlay bir xil bo‘ldi."]],
    "2.4-xulosa: kutilgan va olingan natijalar")
H3("Sodda xulosa")
P("Ayrim kalitlarda holatning ma’lum baytidagi farq Aralash dan keyin izsiz yo‘qoladi va ikki xil holat bir xil bo‘lib qoladi. Bu SBZ ga bog‘liq bo‘lmagan kamchilik. Buzg‘unchi uchun qiyin qismi — yutish nuqtasidan keyin aynan shu farqni hosil qilish (SBZ da bir bayt uchun ≈2⁻⁷·⁹ ehtimollik). Kamchilikni yo‘qotish uchun Aralash va TuzilmaKalit ni kalit jadvali doim «to‘liq» bo‘ladigan qilib o‘zgartirish kerak.")

# ============ ALGEBRAIK ============
PB(); H1('3. Algebraik kriptotahlil xulosalari')
A1=R['A1']; dg=A1['deg']
H2('3.1. Birinchi xulosa: murakkab tenglamalarni faqat yutish nuqtasi hosil qiladi')
XUL("Akslantirishlar ichida yagona yuqori darajali element — yutish nuqtasidagi o‘zgartirish: XOR — 1-daraja, Z — 6-daraja, SBZ — 13-daraja. Qo‘sh va Aralash bit darajasida T-funksiyalar bo‘lib, ularning 0-qatlami chiziqli.")
bolim(
 ["Algebraik hujumda buzg‘unchi algoritmni tenglamalar tizimi ko‘rinishida yozadi va uni yechadi. Tenglama qanchalik murakkab (darajasi katta) bo‘lsa, yechish shunchalik qiyin. Tekshiriladi: algoritmning har bir qismi qanday darajali tenglama beradi?"],
 ["Agar algoritmning ko‘p qismi oddiy (chiziqli) tenglamalar bersa, buzg‘unchi ularni Gauss usulida tez yechadi va faqat murakkab qismlar bilan kurashadi. Shuning uchun qaysi qism murakkablikni ta’minlashini bilish zarur."],
 ["Har bir akslantirishning har bir chiqish biti ko‘phad ko‘rinishida yozildi (Möbius o‘zgartirishi) va darajasi aniqlandi.",
  "Qo‘sh uchun A ilovadagi holat[0,0] elementining haqiqiy parametrlari olindi.",
  "Aralash uchun A ilova kaliti bilan holat′[0,0] ning juft/toqlik tenglamasi chiqarildi va nazariy formula bilan solishtirildi."])
H3("Kutilgan natija")
P("XOR — daraja 1 (chiziqli). Z jadvali 8 ta bitdan 4 bitga — hisobotda daraja 6 topilgan. AES S-box — daraja 7 (8 bitli o‘rin almashtirish uchun eng katta mumkin bo‘lgan qiymat). SBZ ikkita S-box dan iborat, 16 ta kirish biti bor — daraja 13. Qo‘sh — T-funksiya: j-bit faqat 0…j-bitlarga bog‘liq, shuning uchun uning darajasi j + 1 dan oshmasligi kerak (0-bit uchun 1).")
P("Aralash uchun nazariy formula: h′[0,0]₀ = σ₀·h[0,0]₀ ⊕ kₑ[1,0]₀·h[1,1]₀ ⊕ kₑ[2,0]₀·h[2,2]₀ ⊕ kₑ[3,0]₀·h[3,3]₀, bu yerda σ₀ = kₑ[0,0]₀ ⊕ kₑ[1,0]₀ ⊕ kₑ[2,0]₀ ⊕ kₑ[3,0]₀. A ilova kalitida kₑ ning 0-ustuni: c8, 6b, 21, 44, ularning juft/toqligi 0, 1, 1, 0 va σ₀ = 0. Demak, kutilgan tenglama: h′[0,0]₀ = h[1,1]₀ ⊕ h[2,2]₀.")
H3("Olingan natija")
rows=[["Akslantirish","Kirish bitlari","Chiqish bitlari darajalari"]]
for nm,lab_,nv in [('XOR','XOR (Standart-128)','8'),('Z','Z jadvali','8'),('BaytZichlash_256','BaytZichlash (Standart-256)','16'),('S','AES S-box','8'),('SBZ','SBZ','16'),('Qosh_element','Qo‘sh elementi (holat[0,0])','8')]:
    rows.append([lab_,nv,", ".join(str(v) for v in dg[nm])])
T([3800,1500,4054],rows,"Akslantirishlarning algebraik darajalari (olingan)")
P("Aralash uchun dastur chiqargan tenglama: h′[0,0]₀ = " + " ⊕ ".join(t_+"₀" for t_ in A1['aralash_tengl']) + ".")
H3("Kutilgan va olingan natijalarni taqqoslash")
q=dg['Qosh_element']
TAQ([["XOR, Z, S, SBZ darajalari","1; 6; 7; 13","1; 6; 7; 13","Farq yo‘q."],
     ["Qo‘sh: 0-, 1-bit darajasi","1; ≤ 2",f"{q[0]}; {q[1]}","Farq yo‘q (ikkalasi ham chiziqli)."],
     ["Qo‘sh: 3-, 5-bit darajasi","≤ 4; ≤ 6",f"{q[3]}; {q[5]}","Farq yo‘q."],
     ["Qo‘sh: 2-, 4-, 6-, 7-bit darajasi","≤ 3; ≤ 5; ≤ 7; ≤ 8",f"{q[2]}; {q[4]}; {q[6]}; {q[7]}","Farq bor: 8 chiqdi. Sababi pastda izohlangan."],
     ["Aralash tenglamasi","h[1,1]₀ ⊕ h[2,2]₀"," ⊕ ".join(A1['aralash_tengl']),"Farq yo‘q — nazariy formula aniq tasdiqlandi."]],
    "3.1-xulosa: kutilgan va olingan natijalar")
P("*Qo‘sh dagi farqning sababi.* Standartdagi Qo‘sh formulasida maxsus qoida bor: agar oraliq qiymat x⁻² nolga teng chiqsa, u A₂ + B₂ ga almashtiriladi. Bu qoida 256 ta kirishdan faqat bittasida ishlaydi. Ko‘phad tilida bitta nuqtadagi o‘zgarish «hamma o‘zgaruvchilar ko‘paytmasi» kabi to‘liq darajali hadni qo‘shadi, shuning uchun daraja rasman 8 ga sakraydi. Amalda esa funksiya 256 ta qiymatdan 255 tasida past darajali funksiya bilan bir xil. Buzg‘unchi bu bitta nuqtani alohida ko‘rib chiqishi mumkin, shuning uchun bu yuqori daraja haqiqiy himoya bermaydi.")
H3("Sodda xulosa")
P("Algoritmning barcha raund qismlari juft/toqlik qatlamida oddiy chiziqli tenglamalar beradi. Murakkab (yuqori darajali) tenglamalarni faqat yutish nuqtasi hosil qiladi: XOR — umuman murakkab emas (1), Z — o‘rtacha (6), SBZ — eng murakkab (13).")

A2=R['A2']; x=A2['x']
H2('3.2. Ikkinchi xulosa: tenglamalar soni Qo‘sh dan, murakkabligi SBZ dan keladi')
XUL("Raund tenglamalari tizimining hajmini Qo‘sh o‘zgartirishi belgilaydi (bir raundda ≈2,4·10⁵ ta o‘zgaruvchi, 256 bitli rejim); SBZ tizim hajmini amalda o‘zgartirmaydi, lekin uning darajasini oshiradi.")
bolim(
 ["Algebraik hujum uchun algoritm tenglamalarga aylantiriladi. Tekshiriladi: (1) Qo‘sh uchun yozilgan tenglamalar haqiqiy algoritmda bajariladimi, ya’ni tenglamalar to‘g‘ri yozilganmi; (2) bitta raund tizimida qaysi qism nechta o‘zgaruvchi va tenglama beradi."],
 ["Tenglamalar noto‘g‘ri yozilgan bo‘lsa, butun algebraik baho noto‘g‘ri bo‘ladi, shuning uchun ularni haqiqiy qiymatlarda tekshirish kerak. Tizim hajmini bilish esa SBZ algoritmni «og‘irlashtiradimi» degan savolga javob beradi."],
 ["A ilova ma’lumotlari bilan 0-nuqtadagi Qo‘sh uchun barcha oraliq kattaliklar (yig‘indilar J, ko‘paytmalar K, parametrlar A, B) hisoblandi.",
  "holat[0,0] elementi uchun uch bosqichli tenglamalar x⁽ᵗ⁾·(B + R·x⁽ᵗ⁻¹⁾) + A·x⁽ᵗ⁻¹⁾ ≡ 0 (mod 256) haqiqiy sonlar bilan tekshirildi.",
  "Bit darajasidagi baho modeli bo‘yicha bitta raund tizimining tarkibi hisoblandi."])
H3("Kutilgan natija")
P("Agar tenglamalar to‘g‘ri yozilgan bo‘lsa, uchala tenglamaning chap tomoni 256 moduli bo‘yicha aynan 0 ga teng chiqishi kerak. Asosiy hisobotga ko‘ra bitta raundning ≈91% o‘zgaruvchilari Qo‘sh dan keladi, SBZ qatlami esa 512 ta o‘zgaruvchi va 2496 ta kvadrat tenglama qo‘shadi.")
H3("Olingan natija")
P(f"Hisoblangan qiymatlar: J₁h = {A2['J1h']}, J₁hn = {A2['J1hn']}, K₁h = {A2['K1h']}, A₁ = {A2['A1']}, B₁ = {A2['B1']}, A₂ = {A2['A2']}, B₂ = {A2['B2']}, R = 200. Element qiymatlari: x = {x[0]:#04x} → x⁻¹ = {x[1]:#04x} → x⁻² = {x[2]:#04x} → x⁻³ = {x[3]:#04x}.")
rows=[["Bosqich","Tenglama","Kutilgan","Olingan"]]
for i,(eq) in enumerate(["x⁻¹·(B₁ + R·x) + A₁·x","x⁻²·(B₂ + R·x⁻¹) + A₂·x⁻¹","x⁻³·(B₂ + R·x⁻²) + A₂·x⁻²"]):
    rows.append([str(i+1),eq+" (mod 256)","0",str(A2['tekshiruv'][i])])
T([1100,4700,1700,1854],rows,"Qo‘sh tenglamalarining haqiqiy qiymatlarda tekshiruvi")
tot=A2['raund']
rows=[["Tizim qismi","O‘zgaruvchilar","Ulushi"]]
for lab_,v in [("2 × Qo‘sh",A2['qosh2']),("Aralash",A2['aralash']),("TuzilmaKalit",A2['tuz'])]: rows.append([lab_,f"{v:,}".replace(',',' '),fz(100*v/tot,1)+" %"])
rows.append(["Jami (bitta raund)",f"{tot:,}".replace(',',' '),"100 %"])
rows.append(["SBZ qatlami: o‘zgaruvchi / tenglama",f"{A2['sbz'][0]} / {A2['sbz'][1]}","—"]); rows.append(["Z qatlami (Standart-256)",f"{A2['bz_std'][0]} / {A2['bz_std'][1]}","—"])
T([4554,2600,2200],rows,"Bitta raund tenglamalar tizimining tarkibi (256 bitli rejim, baho)")
H3("Kutilgan va olingan natijalarni taqqoslash")
TAQ([["Qo‘sh tenglamalari","0, 0, 0",", ".join(map(str,A2['tekshiruv'])),"Farq yo‘q — tenglamalar to‘g‘ri yozilgan."],
     ["Qo‘sh ulushi","≈91 %",fz(100*A2['qosh2']/tot,1)+" %","Farq yo‘q."],
     ["SBZ qatlami hajmi","512 o‘zg. / 2496 tengl.",f"{A2['sbz'][0]} / {A2['sbz'][1]}","Farq yo‘q. Raundning 243 108 ta o‘zgaruvchisiga nisbatan bu 0,2 %."]],
    "3.2-xulosa: kutilgan va olingan natijalar")
H3("Sodda xulosa")
P("Tenglamalar tizimining hajmini deyarli butunlay Qo‘sh belgilaydi. SBZ tizimni deyarli kattalashtirmaydi (raund hajmining 0,2 foizi), lekin unga eng murakkab, 13-darajali bog‘lanishni qo‘shadi. Demak, SBZ algoritmni «og‘irlashtirmasdan» murakkablashtiradi.")

A3=R['A3']
H2('3.3. Uchinchi xulosa: Standart-128 da 80 ta xesh qiymatdan keyin 32 bitni oldindan aytish mumkin')
XUL("Standart-128 da 0-qatlam butun xesh davomida chiziqli: 80 ta so‘rov bilan 32 bitli bashorat 100% aniqlikda ishlaydi. SBZ bu hujumni to‘liq bartaraf etadi.")
bolim(
 ["1.2-bo‘limda Standart-128 da xesh qiymatning juft/toqlik qatlami xabarning juft/toqlik qatlamidan chiziqli hisoblanishi ko‘rsatildi, lekin u yerda kalit ma’lum edi. Endi kalit noma’lum. Tekshiriladi: buzg‘unchi faqat xabarlar va ularning xesh qiymatlarini ko‘rib, chiziqli bog‘lanishni o‘zi tiklay oladimi va yangi xabarlar uchun 32 bitni oldindan ayta oladimi?"],
 ["Kalitli rejimda xesh qiymat autentifikatsiya kodi sifatida ishlatiladi: kalitni bilmagan odam to‘g‘ri kodni hisoblay olmasligi kerak. Agar buzg‘unchi kodning 32 bitini kalitsiz to‘g‘ri hisoblay olsa, bu jiddiy zaiflik: soxta kod yaratish 2¹²⁸ o‘rniga 2⁹⁶ ga osonlashadi."],
 ["Kalit noma’lum deb hisoblandi (k ning birinchi 16 bayti).",
  "80 ta tasodifiy 16 baytli xabar va ularning xesh qiymatlari olindi.",
  "Har bir chiqish biti uchun «chiqish = A·xabar ⊕ c» ko‘rinishidagi 33 noma’lumli chiziqli tenglamalar tizimi Gauss usulida yechildi.",
  "Topilgan A va c bilan 300 ta yangi xabar uchun xesh qiymatning juft/toqlik qatlami bashorat qilindi va haqiqiy qiymat bilan solishtirildi.",
  "Xuddi shu tajriba SBZ-128 uchun takrorlandi."])
H3("Kutilgan natija")
P("Standart-128 da bog‘lanish aniq chiziqli bo‘lgani uchun 80 ta misol (33 tadan ko‘p) yetarli va 300 ta yangi xabarning hammasida 32 bit to‘g‘ri bashorat qilinishi kerak (ulush 1,000). SBZ-128 da bog‘lanish chiziqli emas, shuning uchun bashorat tasodifiy taxmin darajasida bo‘lishi kerak: har bir bit uchun ≈0,5, 32 bitning hammasi bir vaqtda to‘g‘ri chiqish ehtimolligi esa 2⁻³² ≈ 0.")
H3("Olingan natija")
rows=[["Variant","32 bitning hammasi to‘g‘ri","Bitlar bo‘yicha to‘g‘ri"]]
for bz,lab_ in [('std','Standart-128'),('sbz','SBZ-128')]: rows.append([lab_,fz(A3[bz]['toliq'],3),fz(A3[bz]['bit'],3)])
T([3400,3000,2954],rows,"Bashorat aniqligi (300 ta yangi xabar)")
rows=[["Variant","Haqiqiy juft/toqlik qatlami","Bashorat"]]
for bz,lab_ in [('std','Standart-128'),('sbz','SBZ-128')]:
    for m_,a_,p_ in A3[bz]['misollar'][:2]: rows.append([lab_,a_,p_])
T([2000,3677,3677],rows,"Bashorat misollari (32 bit)",mono=(1,2))
H3("Kutilgan va olingan natijalarni taqqoslash")
TAQ([["Standart-128: 32 bit to‘g‘ri","1,000",fz(A3['std']['toliq'],3),"Farq yo‘q."],
     ["SBZ-128: 32 bit to‘g‘ri","≈0",fz(A3['sbz']['toliq'],3),"Farq yo‘q."],
     ["SBZ-128: bitlar bo‘yicha","≈0,5",fz(A3['sbz']['bit'],3),"Biroz yuqori (0,57). Sababi: 1.5-bo‘limdagi kabi, xesh qiymatning juft/toqlik bitlari orasida doim bajariladigan tengliklar bor (Aralash tufayli), ular ayrim bitlarni qisman bashorat qilinadigan qiladi. Bu SBZ ga emas, Aralash ga tegishli."]],
    "3.3-xulosa: kutilgan va olingan natijalar")
H3("Sodda xulosa")
P("Standart-128 da buzg‘unchi kalitni bilmasdan, faqat 80 ta xesh qiymatni ko‘rib, istalgan yangi xabar uchun xesh qiymatning 32 bitini xatosiz hisoblay oladi. SBZ bilan bu imkoniyat butunlay yo‘qoladi: bashorat tasodifiy taxmindan amalda farq qilmaydi.")

A4=R['A4']; lc=A4['lc']; k_=A4['kub']
H2('3.4. To‘rtinchi xulosa: SBZ birinchi yutish nuqtasidayoq yetarli murakkablikni beradi')
XUL("SBZ variantlari algebraik bardoshlilik chegarasiga 0-nuqtadagi yutishdan keyinoq erishadi, Standart-256 esa 1-raunddan keyin erishadi.")
bolim(
 ["Tenglamalar tizimini yechishning keng tarqalgan usuli — *linearizatsiya*: har bir ko‘paytma (masalan, x₁x₂x₃) yangi o‘zgaruvchi deb olinadi va tizim chiziqli tizimga aylanadi. Bunday yangi o‘zgaruvchilar soni tenglamalar darajasiga bog‘liq. Tekshiriladi: xavfsiz bo‘lish uchun qanday daraja kerak va yutish nuqtasidagi har bir variant buni ta’minlaydimi? Qo‘shimcha ravishda «kub testi» bilan haqiqiy algoritmdagi daraja tekshiriladi."],
 ["Agar daraja past bo‘lsa, linearizatsiya tizimi kichik bo‘ladi va kompyuterda yechiladi. Daraja yetarli bo‘lsa, tizim shunchalik kattaki, uni yechish 2⁶⁴ (128 bitli rejim) yoki 2¹²⁸ (256 bitli rejim) dan ko‘p ish talab qiladi."],
 ["Linearizatsiya murakkabligi formula bo‘yicha hisoblandi: (yangi o‘zgaruvchilar soni)^2,8.",
  "Kub testi: xabarning 0-baytidagi 7 ta bit o‘zgaruvchi qilib olindi, ularning barcha 2⁷ = 128 ta kombinatsiyasi uchun xesh hisoblandi va har bir chiqish biti bo‘yicha natijalar XOR qilindi. Agar bit darajasi 7 dan kichik bo‘lsa, bu yig‘indi albatta 0 chiqadi; daraja yuqori bo‘lsa, taxminan yarim hollarda 0 chiqadi.",
  "Kub testi yutishdan keyin r = 0, 1 va 3 raunddan so‘ng to‘rttala variantda o‘tkazildi."])
H3("Kutilgan natija")
P(f"Formula bo‘yicha: 128 bitli rejimda daraja kamida {A4['dmin128']}, 256 bitli rejimda kamida {A4['dmin256']} bo‘lishi kerak. SBZ (13) ikkalasidan ham katta, Z (6) 256 bitli rejim uchun yetmaydi, XOR (1) hech qachon yetmaydi. Kub testida: Standart-128 ning juft/toqlik qatlami chiziqli bo‘lgani uchun 32 bitning hammasida yig‘indi 0 chiqishi; SBZ-128 da nol bo‘lmagan yig‘indilar paydo bo‘lishi; 256 bitli variantlarda esa taxminan yarim bitlar 0 chiqishi (yuqori darajali, tasodifiy funksiya kabi) kutiladi.")
H3("Olingan natija")
T([3500,1950,1950,1954],[["Yutish o‘zgartirishi","Daraja","128 bitli: log₂ mehnat","256 bitli: log₂ mehnat"],
   ["XOR","1",fz(lc['128_1'],1),fz(lc['256_1'],1)],["Z","6",fz(lc['128_6'],1),fz(lc['256_6'],1)],["SBZ","13",fz(lc['128_13'],1),fz(lc['256_13'],1)],["Talab qilinadigan","4 / 8","≥ 64","≥ 128"]],"Linearizatsiya mehnati (log₂ shkalada)")
rows=[["Variant","r = 0","r = 1","r = 3"]]
for p_,lab_ in [('256_std','Standart-256'),('256_sbz','SBZ-256'),('16_std','Standart-128'),('16_sbz','SBZ-128')]:
    rows.append([lab_]+[f"{k_[f'{p_}_r{r}']['nol']}/{k_[f'{p_}_r{r}']['jami']}  (juft/toqlik: {k_[f'{p_}_r{r}']['qatlam0_nol']}/32)" for r in (0,1,3)])
T([2350,2335,2335,2334],rows,"Kub testi: yig‘indisi 0 chiqqan bitlar soni")
H3("Kutilgan va olingan natijalarni taqqoslash")
TAQ([["Talab qilinadigan daraja","128 bitli: 4; 256 bitli: 8",f"{A4['dmin128']}; {A4['dmin256']}","Farq yo‘q."],
     ["Standart-128: juft/toqlik qatlami","32/32 nol (barcha r)","32/32; 32/32; 32/32","Farq yo‘q — bu qatlam chiziqli ekani yana tasdiqlandi."],
     ["SBZ-128: juft/toqlik qatlami","nol bo‘lmagan yig‘indilar bor","31/32; 30/32; 26/32 nol","Kutilgan natija tasdiqlandi (1, 2 va 6 ta bit nol emas), lekin tasodifiy funksiyadagi ≈16 tadan kam. Sababi: kub o‘zgaruvchilari faqat bitta baytda; boshqa pozitsiyalardagi juft/toqlik bitlari bu baytga faqat Qo‘sh dagi yig‘indilar orqali kuchsiz bog‘langan. Darajaning 7 dan yuqori ekanini ko‘rsatish uchun bitta nol bo‘lmagan bit yetarli."],
     ["256 bitli variantlar","≈128/256 nol","114–142/256","Farq yo‘q, tasodifiy funksiya kutilgan oralig‘ida."]],
    "3.4-xulosa: kutilgan va olingan natijalar")
H3("Sodda xulosa")
P("Linearizatsiya hujumi uchun xavfsizlik talabini SBZ birinchi yutish nuqtasidayoq bajaradi (daraja 13). Standart Z (daraja 6) 256 bitli rejimda bunga yetmaydi va keyingi raundlarga tayanadi. Standart-128 ning juft/toqlik qatlami esa hech qachon chiziqlilikdan chiqmaydi va kub testi buni yana bir bor ko‘rsatdi.")

# ============ JAMLANMA ============
PB(); H1('Umumiy jamlanma: kutilgan va olingan natijalar')
rows=[["Xulosa","Asosiy kutilgan natija","Asosiy olingan natija","Mos keladimi"]]
rows+= [["Ch-1. Raundlarda juft/toqlik bashorat qilinadi","1–7-raundlarda 32/32","32/32 har raundda","ha"],
 ["Ch-2. Standart-128 da 32 bit hisoblanadi","275 qadamda 32/32","32/32","ha"],
 ["Ch-3. Z: faol bayt boshiga 2⁻²","c = 0,25; mediana 15 (4 qatlam)","c = 0,25; 4 (A ilova kaliti)","ha; A ilova kaliti — eng yomon kalit"],
 ["Ch-4. SBZ: faol bayt boshiga 2⁻⁶","c = ±2⁻⁶","c = −2⁻⁶; odatiy kalitda 4 qatlamda 2⁻¹⁰⁸","ha"],
 ["Ch-5. Chiqishda doimiy tengliklar","≈6 ta, ulush 1,0","8 ta, ulush 1,0 (ikkala variant)","ha"],
 ["D-1. Raundlarda MSB izi saqlanadi","7 raunddan keyin ≈0,34","0,335; misolda 2 raund","ha; misol — tasodifiy hol"],
 ["D-2. SBZ da farq yo‘qolmaydi","0 ta yo‘qolish","0 ta (16,7 mln juftlik)","ha"],
 ["D-3. SBZ 8-raundda xavfsiz","≤ 2⁻¹⁶² (SBZ-256)","2⁻¹⁸⁶","ha (misolda faol baytlar ko‘proq)"],
 ["D-4. Aralash da farq yo‘qoladi","farq nol","farq nol, 10-raundgacha","ha"],
 ["A-1. Faqat yutish murakkab","1 / 6 / 13","1 / 6 / 13","ha; Qo‘sh dagi 8 — bitta maxsus nuqta"],
 ["A-2. Tizimni Qo‘sh belgilaydi","tenglamalar = 0; ≈91 %","0, 0, 0; 91,4 %","ha"],
 ["A-3. Standart-128 bashorat qilinadi","1,000 / ≈0,5","1,000 / 0,569","ha; 0,569 — Aralash tengliklari"],
 ["A-4. SBZ darhol yetarli","d ≥ 4 / 8; SBZ 13","tasdiqlandi, kub testi mos","ha"]]
T([2700,2250,2500,1904],rows,"13 ta xulosa bo‘yicha jamlanma")
P("Barcha 13 ta xulosa misollarda tasdiqlandi. Kutilgan va olingan natijalar orasidagi farqlar uch turga bo‘linadi: (1) tanlanma xatoligi doirasidagi kichik farqlar (masalan, 0,254 va 0,25); (2) misol uchun olingan aniq kalit yoki element xususiyatidan kelib chiqadigan farqlar (A ilova kalitining «eng yomon» kalit ekani, Qo‘sh dagi maxsus nuqta); (3) hisobotda ehtiyotkorlik uchun olingan qiymatlardan yaxshiroq natijalar (8-nuqtada 27 o‘rniga 31 faol bayt). Hech bir farq xulosalarni inkor etmaydi.")
P("Misollarning eng muhim amaliy natijalari: SBZ standart 128 bitli rejimdagi chiziqli zaiflikni (32 bitni oldindan aytish) butunlay yo‘qotadi va farqni yutish nuqtasida yo‘qotishni imkonsiz qiladi. Shu bilan birga, chiqishdagi doimiy tengliklar, ayrim kalitlarda farqning Aralash da yo‘qolishi va A ilova kaliti kabi «eng yomon» kalitlar Aralash/TuzilmaKalit o‘zgartirishlarining kamchiligi bo‘lib, ularni alohida tuzatish kerak.")
json.dump(B,open('blocks.json','w'),ensure_ascii=False); print(len(B),tc[0])
