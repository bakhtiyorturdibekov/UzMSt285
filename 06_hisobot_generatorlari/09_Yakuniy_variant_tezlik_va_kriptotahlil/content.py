import json, math, re as _re
K='/home/claude/ka/'; J=lambda f: json.load(open(K+f+'.json'))
C=J('yakuniy_tezlik_c'); PY=J('yakuniy_tezlik_py'); R=J('yakuniy_tahlil'); QB=J('qb_tezlik'); L1=J('lin1'); L2=J('lin2'); L3=J('lin3'); D1=J('dif1'); A1=J('alg1'); A2=J('alg2'); A3=J('alg3'); D3=J('dif3'); DT=J('yakuniy_det')
IS=json.load(open('/home/claude/pkg/uzmst285_tahlil/natijalar/integral_sbz.json')); IST=json.load(open('/home/claude/pkg/uzmst285_tahlil/natijalar/integral.json'))
B=[]; tc=[0]; fc=[0]; TK={}
H1=lambda t:B.append(['h1',t]); H2=lambda t:B.append(['h2',t]); H3=lambda t:B.append(['h3',t])
P=lambda t:B.append(['p',t]); F=lambda t:B.append(['f',t]); BL=lambda t:B.append(['b',t]); PB=lambda:B.append(['pb'])
def T(w,rows,cap,mono=(),key=None):
    tc[0]+=1; B.append(['cap',f"{tc[0]}-jadval. {cap}"]); B.append(['t',w,rows,list(mono)])
    if key: TK[key]=tc[0]
def IMG(p,w,h,cap): fc[0]+=1; B.append(['img',p,w,h]); B.append(['fcap',f"{fc[0]}-rasm. {cap}"])
fz=lambda x,d=2:(f'{x:.{d}f}').replace('.',','); sp=lambda n:f"{n:,}".replace(',',' ')
NMA={'Bog0':'Bog‘lash(holat, blok)','SBZ0':'SBZ (0-nuqta)','Aralash':'Aralash','Bog1':'Bog‘lash(holat, kₑ)','Sur':'SurHolat, kalit jadvali','Bog2':'Bog‘lash(holat, kₑ)','SBZ8':'SBZ (8-nuqta)','SBZ9':'SBZ (9-nuqta)','Bog8':'Bog‘lash(holat, blok)','Bog9':'Bog‘lash(holat, blok)'}
nl='\n'.join
r256=R['raund_256']; r16=R['raund_16']; b256=R['bog_256']; b16=R['bog_16']; c256=R['chiqish_256']; c16=R['chiqish_16']

B.append(['title','O‘zMSt 285:2024 1-ALGORITMINING TAKLIF ETILGAN YAKUNIY VARIANTI: TEZLIK VA CHIZIQLI, DIFFERENSIAL, ALGEBRAIK, INTEGRAL KRIPTOTAHLIL'])
B.append(['sub','Barcha tavsiyalar birgalikda qo‘llanilgan variantni standart algoritm bilan solishtirish'])
H1('Kirish')
P("Oldingi tadqiqotlarda standart algoritmning to‘rtta kriptotahlil usuli bo‘yicha asosiy kamchiliklari aniqlangan va ularni bartaraf etish uchun to‘rtta tavsiya hamda Qo‘sh o‘zgartirishining o‘rniga yangi «Bog‘lash» akslantirishi taklif etilgan edi. Ushbu hisobotda barcha tavsiyalar birlashtirilgan *yakuniy variant* tezlik bo‘yicha standart algoritm bilan solishtiriladi va chiziqli, differensial, algebraik hamda integral kriptotahlil bo‘yicha baholanadi. Taqqoslash uchun standart algoritm va SBZ varianti natijalari ham keltiriladi.")
H2('Yakuniy variantning tavsifi')
T([2700,3300,3354],[["Akslantirish / qadam","Standart algoritm","Yakuniy variant"],
 ["Yutish (0-, 8-, 9-nuqtalar)","Qo‘sh(holat, blok) → BaytZichlash","Bog‘lash(holat, blok) → SBZ(holat, blok)"],
 ["Raund ichidagi aralashtirish (2 marta)","Qo‘sh(holat, kₑ)","Bog‘lash(holat, kₑ)"],
 ["Kalit jadvali","Qo‘sh orqali holatga bog‘liq; TuzilmaKalit: kₑ juftligi = k juftligi","kₑ ← (SurKalit(kₑ) ⊕ RCⱼ) ∨ 1; boshida kₑ ← k ∨ 1 (holatdan mustaqil, toq kₑ)"],
 ["Aralash, SurHolat","—","o‘zgarishsiz (toq kₑ bilan Aralash har doim teskarilanuvchi)"],
 ["Bloklar orasida","—","oldinga uzatish: holatᵢ = F(holatᵢ₋₁, blokᵢ) ⊕ holatᵢ₋₁"],
 ["Chiqish","holat","h(M) = P(H) ⊕ H, P = Bog‘lash(Bog‘lash(H, C₁), C₂)"]],"Yakuniy variantdagi o‘zgarishlar")
P("Bog‘lash(holat, X) — ikkala rejim uchun yagona, bayt darajasidagi akslantirish (128 bitli rejimda qo‘shni yarim baytlar juftlanadi). U holatning chap va o‘ng yarimlari ustida Feistel tarzidagi uchta yarim qadamdan iborat; bitta yarim qadam (T ← f(U)):")
F("J = Σ U,  K = Π (U ∨ 1);   aᵢ = 2·S(U[i] ⊕ X_U[i] ⊕ J) + 1,  bᵢ = 2·S(U[i+1] ⊕ X_T[i] ⊕ K) + 1;")
F("T[i] ← S( −aᵢ·T[i]·(bᵢ + R·T[i])⁻¹ ⊕ X_T[i] )   (mod 256),")
P("bu yerda S — AES S-box, R — kalitning birinchi bayti (juft). Bog‘lash qurilishiga ko‘ra bijeksiya, ma’lumotga bog‘liq tarmoqlanishsiz, bitta chaqiruvda to‘liq tarqalishni ta’minlaydi va Qo‘sh ning g‘oyalarini (parametrli Möbius ko‘paytirishi, global yig‘indi va ko‘paytma, ikki massiv bog‘lanishi) saqlaydi. Uchinchi tavsiya (T-funksiya xossasini yo‘qotish) Bog‘lash ichidagi S-box orqali bajariladi, shuning uchun alohida S-box qatlami talab qilinmaydi.")
P("Yakuniy variant Python va C tillarida mustaqil realizatsiya qilindi; ikkala realizatsiya bir xil natija beradi. A ilova kaliti va xabari uchun nazorat qiymatlari:")
F("256 bitli rejim:  ebbfa2572a1c0d784af3454c78ecd700 d30a74e81eb1b8bab213eae1bf01c6b7")
F("128 bitli rejim:  23a8fd8fdf3849afe0212e01f5e9e239")

# ===================== 1. TEZLIK =====================
PB(); H1('1. Tezlik bo‘yicha standart algoritm bilan solishtirish')
H2('1.1. O‘lchash usuli')
P("Tezlik C realizatsiyasida (gcc -O2, Intel Xeon 2,3 GGs, bitta yadro) 262 144 baytli xabar uchun o‘lchandi; har bir variant 3 marta aralash tartibda, har safar 3 takror bilan o‘lchanib, eng yaxshi vaqt olindi. Qo‘shimcha ravishda Python (numpy) realizatsiyasida 500 ta to‘rt blokli xabar uchun vaqt o‘lchandi va bitta blok uchun amallar soni sanaldi. Virtual server sharoitida takroriy o‘lchovlar orasidagi farq 10% gacha yetadi, shuning uchun jadvallarda barcha o‘lchovlar ham keltiriladi.")
H2('1.2. Natijalar')
rows=[["Rejim","Variant","Vaqt, ms (eng yaxshi)","Barcha o‘lchovlar, ms","mkS / blok","MB/s","Standartga nisbatan"]]
for p in ('256','16'):
    for n,l in (('standart','Standart'),('sbz','SBZ'),('yakuniy','Yakuniy variant')):
        d=C[f'{p}_{n}']; rows.append(['256' if p=='256' else '128',l,fz(d['ms']),"; ".join(fz(x) for x in d['barcha']),fz(d['mks_blok'],3),fz(d['MBs']),f"{fz(d['nisbat'])} ×"])
T([900,1700,1400,2100,1100,900,1254],rows,"C realizatsiyasi bo‘yicha to‘liq xesh tezligi (262 144 bayt)",key='ctez')
IMG('ch_tezlik.png',15.5,6.7,"Variantlarning to‘liq xesh tezligi (C, gcc -O2)")
P(f"Yakuniy variant 256 bitli rejimda standart algoritmdan {fz(C['256_yakuniy']['nisbat'])} marta (o‘lchovlar oralig‘i bo‘yicha 1,45–1,6 marta), 128 bitli rejimda {fz(C['16_yakuniy']['nisbat'])} marta (2,2–2,7 marta) tez. SBZ varianti standart bilan bir xil tezlikda (128 bitli rejimdagi farq o‘lchov shovqini bilan bog‘liq). Python realizatsiyasida ham xuddi shunday manzara: 256 bitli rejimda {fz(PY['256']['standart'],3)} s va {fz(PY['256']['yakuniy'],3)} s ({fz(PY['256']['standart']/PY['256']['yakuniy'])} marta), 128 bitli rejimda {fz(PY['16']['standart'],3)} s va {fz(PY['16']['yakuniy'],3)} s ({fz(PY['16']['standart']/PY['16']['yakuniy'])} marta).")
H2('1.3. Tezlik farqining sabablari')
q=QB['C_ns']
T([3400,1980,1987,1987],[["Ko‘rsatkich (bitta chaqiruv)","Qo‘sh","Bog‘lash, 256","Bog‘lash, 128"],["Modul ko‘paytirish","706","192","96"],["Teskarilash (jadvaldan)","192","48","24"],["S-box murojaati","0","144","72"],["Qo‘shish/XOR","≈1152","≈384","≈256"],["Shartli tekshiruvlar","132","0","0"],["Vaqt, ns (C)",f"{fz(q['qosh_256'],0)} / {fz(q['qosh_16'],0)}",fz(q['boglash_256'],0),fz(q['boglash_16'],0)]],"Qo‘sh va Bog‘lash: amallar soni va bitta chaqiruv vaqti")
P("Standart algoritmda vaqtning ≈91 foizini Qo‘sh egallaydi (blokka 22 ta chaqiruv, 4224 ta modul teskarilash). Yakuniy variantda har bir Qo‘sh chaqiruvi Bog‘lash bilan almashtirilgan (chaqiruvlar soni o‘zgarmagan — 22 ta), Bog‘lash esa Qo‘sh dan 256 bitli rejimda ≈2 marta, 128 bitli rejimda ≈2,6–2,9 marta tez. 128 bitli rejimda yutuq kattaroq, chunki Qo‘sh u yerda ham 64 ta element ustida ishlaydi, Bog‘lash esa 16 baytda. Qo‘shimcha elementlar — yutishdagi SBZ (blokka 3 × 32 ta jadval murojaati), kalit jadvalidagi XOR (blokka 320 ta), oldinga uzatish (blokka 32 ta XOR) — sezilarli vaqt talab qilmaydi.")
P(f"Chiqish o‘zgartirishi P(H) ⊕ H butun xabar uchun bir marta bajariladi (ikkita Bog‘lash, ≈{fz(2*q['boglash_256']/1000,2)} mkS 256 bitli rejimda). Bir blokli xabar uchun bu blok vaqtining (≈{fz(C['256_yakuniy']['mks_blok'],1)} mkS) 5 foizidan kam, uzun xabarlarda esa sezilmaydi.")
H2('1.4. Tezlik bo‘yicha xulosa')
BL(f"Yakuniy variant standart algoritmdan 256 bitli rejimda ≈1,5 marta, 128 bitli rejimda ≈2,2–2,7 marta tez (C realizatsiyasi).")
BL("Tezlanishning asosiy manbai — Qo‘sh ni Bog‘lash bilan almashtirish; boshqa tavsiyalar (SBZ, toq kₑ, kalit jadvali, oldinga uzatish, chiqish o‘zgartirishi) tezlikka deyarli ta’sir qilmaydi.")
BL("Bog‘lash bitta chaqiruvda to‘liq tarqalish bergani uchun raundlar sonini kamaytirish imkoniyati mavjud; bu tezlikni yanada oshiradi (alohida tahlil talab qilinadi).")

# ===================== 2. CHIZIQLI =====================
PB(); H1('2. Chiziqli kriptotahlil')
H2('2.1. Bardoshlilik mezoni')
P("Approksimatsiya korrelyatsiyasi c_F(α → β) = 2⁻ⁿ · Σₓ (−1)^(β·F(x) ⊕ α·x), chetlanish ε = c/2; iz korrelyatsiyasi oraliq korrelyatsiyalar ko‘paytmasiga teng, hujum uchun N ≈ c⁻² ma’lumot kerak. Talab: 256 bitli rejimda |c| ≤ 2⁻⁶⁴, 128 bitli rejimda |c| ≤ 2⁻³².")
H2('2.2. Akslantirishlarning korrelyatsion ko‘rsatkichlari')
H3('2.2.1. SBZ va Aralash')
P(f"SBZ uchun maksimal |c| = 2⁻⁶ (faqat 6375 ta uchlikda), faqat holatn orqali o‘tuvchi approksimatsiya yo‘q (SBZ varianti hisobotiga qarang). Aralash 0-qatlamda chiziqli (h′₀ = M·h₀), lekin toq kₑ bilan M har doim teskarilanuvchi (rang 32) va 4×4 yarim uchun tarmoqlanish soni 6 ga teng — barcha juft/toqlik naqshlari orasida eng kattasi.")
H3('2.2.2. Bog‘lash elementining korrelyatsion matritsasi')
lm=R['g_lat_max']
P("Bog‘lash dagi har bir element parametrlar belgilanganda g(x) = S(f_{a,b}(x) ⊕ t) akslantirishidan o‘tadi (f — Möbius ko‘paytmasi). 200 ta tasodifiy (a, b, R, t) to‘plami uchun g ning 256×256 korrelyatsion matritsasi to‘liq hisoblandi; maksimal |W| = 256·|c| taqsimoti quyidagi jadvalda.")
T([3354]+[1000]*6,[["Maks. |W| (×1/256)"]+list(lm.keys()),["Parametrlar to‘plamlari soni"]+[str(v) for v in lm.values()],["Maks. |c|"]+[fz(int(k)/256,3) for k in lm.keys()]],"Bog‘lash elementi g(x) uchun maksimal korrelyatsiya taqsimoti (200 ta parametrlar to‘plami)")
P("Belgilangan parametrlarda element akslantirishining maksimal korrelyatsiyasi 0,23–0,31 (≈2⁻²); bu S ning o‘zidan (2⁻³) yomonroq, chunki Möbius ko‘paytmasi T-funksiya va uning quyi bitlari chiziqli. Biroq Bog‘lash da parametrlar aᵢ, bᵢ har bir chaqiruvda boshqa yarimning S-box chiqishlaridan olinadi, ya’ni buzg‘unchi uchun ular tasodifiy; approksimatsiya parametrlar bo‘yicha o‘rtalashtirilganda korrelyatsiya yanada kamayadi. Bundan tashqari, har bir element chiqishida S-box turadi va 0-bit endi chiziqli emas.")
P(f"Parametrlar tasodifiy bo‘lgandagi samarali korrelyatsiyani baholash uchun 300 ta tasodifiy (a, b, t) to‘plami bo‘yicha W(α → β) qiymatlari ishorasi bilan o‘rtalashtirildi (R belgilangan). O‘rtacha korrelyatsiyaning maksimumi {fz(DT['g_ortacha_c_max'],4)} ≈ 2⁻⁶ ni tashkil qildi — bu S ning bitta o‘zidagi 2⁻³ dan ham kichik va SBZ dagi 2⁻⁶ ga teng. Demak, buzg‘unchi parametrlarni bilmagan yoki boshqara olmagan holatda Bog‘lash elementi amalda 2⁻⁶ korrelyatsiyali qatlam sifatida ishlaydi.")
H3('2.2.3. Bog‘lash massiv darajasida (bitta chaqiruv)')
T([3600,1500,1500,2754],[["Ko‘rsatkich","Qo‘sh","Bog‘lash (256 / 128)","Izoh"],["y₀ = x₀ bajarilish ulushi","1,000",f"{fz(b256['y0=x0'],3)} / {fz(b16['y0=x0'],3)}","0-bit endi chiziqli emas"],["Eng yaxshi «bit → bit» |c|","1,000",f"{fz(b256['bit_bit'],3)} / {fz(b16['bit_bit'],3)}",f"shovqin chegarasi {fz(b256['shovqin'],3)}"],["Ko‘chki (SAC): o‘rtacha / bog‘liqsiz / min","0,256 / 14,1% / 0",f"{fz(b256['sac'][0],3)} / {fz(100*b256['sac'][1],0)}% / {fz(b256['sac'][2],2)}","bitta chaqiruvda to‘liq bog‘liqlik"]],"Bitta chaqiruv: Qo‘sh va Bog‘lash ning chiziqli ko‘rsatkichlari")
H3('2.2.4. Yarim qadamlar bo‘yicha tarqalish')
yq=DT['yarim_qadam_faol']
T([3600,1900,1900,1954],[["Bitta chaqiruv ichidagi qadam","256: chap yarimdagi bayt faol / o‘ng","128: chap / o‘ng","Izoh"],["1-yarim qadam (o‘ng ← f(chap))",f"{fz(yq['256_1'][0],1)} / {fz(yq['256_1'][1],1)}",f"{fz(yq['16_1'][0],1)} / {fz(yq['16_1'][1],1)}","chap bayt J, K orqali butun o‘ng yarimga ta’sir qiladi"],["2-yarim qadam (chap ← f(o‘ng))",f"{fz(yq['256_2'][0],1)} / {fz(yq['256_2'][1],1)}",f"{fz(yq['16_2'][0],1)} / {fz(yq['16_2'][1],1)}",""],["3-yarim qadam (o‘ng ← f(chap))",f"{fz(yq['256_3'][0],1)} / {fz(yq['256_3'][1],1)}",f"{fz(yq['16_3'][0],1)} / {fz(yq['16_3'][1],1)}","har qanday bayt butun holatga ta’sir qiladi"]],"Bog‘lash yarim qadamlari bo‘yicha faol baytlar soni (bitta MSB ayirmasidan, 1500 juftlik)")
P("Jadvaldan uchinchi yarim qadamning zarurligi ko‘rinadi: ikki yarim qadamdan keyin o‘ng yarimdagi bayt atigi 16 baytga ta’sir qiladi (chap yarim va o‘zi), uchinchi yarim qadam esa bog‘liqlikni butun holatga yoyadi. Har bir yarim qadamdagi J va K (manba yarmining yig‘indisi va ko‘paytmasi) bitta baytdagi o‘zgarishni nishon yarimning barcha 16 (128 bitli rejimda 8) elementiga yetkazadi.")
H2('2.3. Raund approksimatsiyalari')
rows=[["Akslantirish (1-raund)","Holat (A ilova ma’lumotlari, 256 bitli rejim)","0-qatlam"]]
for e in DT['iz']: rows.append([NMA.get(e['amal'],e['amal']),nl(e['holat']),nl(e['q0'])])
T([2600,4200,2554],rows,"Yakuniy variant, A ilova ma’lumotlari: 0-nuqta va 1-raund akslantirishlaridan keyingi holat",mono=(1,2))
P("Standart algoritmda 1-raund akslantirishlaridan keyin 0-qatlam nazariy bashorat bilan 32/32 mos kelardi. Yakuniy variantda har bir Bog‘lash dan keyin 0-qatlam butunlay yangilanadi: u oldingi 0-qatlamning chiziqli funksiyasi emas.")
P("Standart va SBZ variantlarida yutishsiz raundlar 0-qatlamda h₀ ← L·h₀ tenglamasi bilan korrelyatsiya 1 bilan o‘tar edi. Yakuniy variantda bu tenglama haqiqiy algoritmda tekshirildi (600 kalit) va bir raunddan keyin «bitta bit → bitta bit» eng yaxshi korrelyatsiyasi o‘lchandi (6000 namuna).")
T([2600]+[675]*10,[["Raund j"]+[str(j) for j in range(1,11)],["Standart-256"]+[fz(v,2) for v in L2['lsb_pred_256_std']],["SBZ-256"]+[fz(v,2) for v in L2['lsb_pred_256_sbz']],["Yakuniy-256"]+[fz(v,2) for v in r256['qatlam0_c']],["Yakuniy-128"]+[fz(v,2) for v in r16['qatlam0_c']]],"0-qatlam raund tenglamasining korrelyatsiyasi")
P(f"Yakuniy variantda 0-qatlam tenglamasining korrelyatsiyasi birinchi raunddayoq nolga teng (|c| ≤ 0,016, ya’ni o‘lchash shovqini). Bir va ikki raunddan keyingi eng yaxshi «bit → bit» korrelyatsiyasi 256 bitli rejimda {fz(r256['bit_bit_1'],3)} va {fz(r256['bit_bit_2'],3)}, 128 bitli rejimda {fz(r16['bit_bit_1'],3)} va {fz(r16['bit_bit_2'],3)} — shovqin chegarasidan (0,058) past. Demak, har bir raund chiziqli bardoshlilikka hissa qo‘shadi; standart va SBZ variantlarida esa 1–7-raundlar hech qanday hissa qo‘shmas edi.")
bb=DT['bit_bit_raund']
T([3600]+[1438]*4,[["Raundlar soni","1","2","3","4"],["256: eng yaxshi «bit → bit» |c| (shovqin ≈0,064)"]+[fz(v,3) for v in bb['256']],["128: eng yaxshi «bit → bit» |c|"]+[fz(v,3) for v in bb['16']]],"Raundlar bo‘yicha eng yaxshi «bitta kirish biti → bitta chiqish biti» korrelyatsiyasi (5000 namuna)")
IMG('ch_tahlil.png',15.5,6.7,"0-qatlam tenglamasi korrelyatsiyasi (chapda) va MSB izining saqlanishi (o‘ngda): standart, SBZ va yakuniy variant")
H2('2.4. Iz korrelyatsiyasining baholari')
P("Bog‘lash ning har bir chaqiruvida chiqish niqobi noldan farqli bo‘lgan har bir bayt kamida bitta g elementidan o‘tadi. Pessimistik baho (har bir chaqiruvda bitta faol element, belgilangan parametrlardagi eng yomon |c| ≈ 0,31): bir raundda (ikki chaqiruv) |c| ≤ 0,31² ≈ 2⁻³·⁴. Real baho bitta chaqiruvdagi faollikdan kelib chiqadi: bitta bayt o‘zgarganda chiqishda o‘rtacha 31,3 (256 bitli rejim) va 29,5 (128 bitli rejim) bayt o‘zgaradi, ya’ni keyingi chaqiruvda deyarli barcha elementlar faol bo‘ladi. Yutish nuqtalarida esa SBZ har bir faol bayt uchun ≤ 2⁻⁶ hissa qo‘shadi.")
T([3200,2050,2050,2054],[["Baho turi","1 raunddan keyin","2 raunddan keyin","2⁻⁶⁴ / 2⁻³² ga erishish"],["Pessimistik (1 faol element / chaqiruv, belgilangan parametrlar)","≤ 2⁻³·⁴","≤ 2⁻⁶·⁸","≈19 / ≈10 raund"],["O‘rtacha parametrlar (1 faol element / chaqiruv, ≈2⁻⁶)","≤ 2⁻¹²","≤ 2⁻²⁴","≈6 / ≈3 raund"],["Real (≥ 16 faol element / chaqiruv)","≤ 2⁻⁵⁴","≤ 2⁻¹⁰⁸","2 raund"],["SBZ varianti (taqqoslash, mediana kalit)","1 (1–7-raundlar)","1","≈11 raund / 4 qatlam"],["Standart (taqqoslash)","1","1","≈19 raund / bardoshli emas"]],"Yakuniy variantda iz korrelyatsiyasining baholari")
P("Pessimistik baho ham hozirgi algoritmdagi bilan solishtirganda yaxshi, chunki standart va SBZ variantlarida yutishsiz raundlar umuman hissa qo‘shmaydi. Aniq (isbotlanadigan) chegara uchun Bog‘lash orqali faol elementlarning minimal sonini hisoblash kerak; bu keyingi ish sifatida qayd etiladi.")
H2('2.5. Chiqishdagi chiziqli munosabatlar')
T([3200,2050,2050,2054],[["Ko‘rsatkich","Standart-256","SBZ-256","Yakuniy (256 / 128)"],["Xesh 0-qatlami rangi","23–30","23–27",f"{min(c256['rang'])} / {min(c16['rang'])}"],["Minimal bit chastotasi","0,000","0,000",f"{fz(c256['min_chastota'],3)} / {fz(c16['min_chastota'],3)}"],["0-qatlam affin modeli aniqligi","0,64","0,56",f"{fz(c256['affin_0'],3)} / {fz(c16['affin_0'],3)}"]],"Xesh qiymatdagi chiziqli munosabatlar")
P("Yakuniy variantda xesh qiymatning 0-qatlami to‘liq rangli (32), doimiy bitlar yo‘q va affin model tasodifiy taxmin darajasida. Bunga toq kₑ (Aralash teskarilanuvchi), Bog‘lash va chiqish o‘zgartirishi P(H) ⊕ H birgalikda erishadi.")
H2('2.6. Chiziqli kriptotahlil bo‘yicha xulosalar')
BL("Yakuniy variantda har bir raund chiziqli bardoshlilikka hissa qo‘shadi: 0-qatlam tenglamasi va bit-qatlamlar bo‘yicha approksimatsiyalar birinchi raunddayoq yo‘qoladi.")
BL("Bog‘lash elementining belgilangan parametrlardagi maksimal korrelyatsiyasi ≈2⁻², lekin parametrlar har chaqiruvda S-box orqali o‘zgaradi va bitta chaqiruv to‘liq tarqalish beradi; real baho bo‘yicha 2⁻⁶⁴ chegarasiga 2 raundda erishiladi, pessimistik baho bo‘yicha ≈19 raundda.")
BL("Chiqishdagi c = 1 munosabatlar va doimiy bitlar yo‘qolgan (rang 32, minimal chastota ≈0,44).")

# ===================== 3. DIFFERENSIAL =====================
PB(); H1('3. Differensial kriptotahlil')
H2('3.1. Bardoshlilik mezoni')
P("DDT_F(Δx, Δy) = #{x : F(x) ⊕ F(x ⊕ Δx) = Δy}, p = DDT/2ⁿ; iz ehtimolligi ko‘paytmaga teng. Talab: 256 bitli rejimda 2⁻¹²⁸, 128 bitli rejimda 2⁻⁶⁴.")
H2('3.2. Akslantirishlarning ayirmalar ko‘rsatkichlari')
dm=R['g_ddt_max']
P("SBZ uchun maksimal ehtimollik 2⁻⁶ (faqat Δn = 0 da), Δn ≠ 0 da ≤ 2⁻⁷·⁶, bitta argumentdagi ayirma so‘nmaydi. Aralash toq kₑ bilan teskarilanuvchi, shuning uchun uning yadrosi orqali ayirma so‘nishi (standartda ≈3%) yo‘qoladi. Bog‘lash elementi g uchun 200 ta parametrlar to‘plamida ayirmalar matritsasi hisoblandi:")
T([3354]+[1500]*4,[["Maks. DDT (×1/256)"]+list(dm.keys()),["Parametrlar to‘plamlari soni"]+[str(v) for v in dm.values()],["Maks. ehtimollik"]+[f"2^{fz(math.log2(int(k)/256),1)}" for k in dm.keys()]],"Bog‘lash elementi g(x) uchun maksimal differensial ehtimollik taqsimoti")
P(f"Element akslantirishining maksimal ehtimolligi 8–14/256 (2⁻⁵ … 2⁻⁴·²); bu S ning 2⁻⁶ qiymatidan biroz yomonroq, ammo Qo‘sh dagi 80 → 80 o‘tishining 254/256 ehtimolligidan beqiyos yaxshi. Bitta Bog‘lash chaqiruvida MSB ayirmasining faqat MSB ko‘rinishida qolish ehtimolligi 0 (Qo‘sh da 0,955), bitta faol baytdan chiqishda o‘rtacha {fz(b256['faol'],1)} (256) va {fz(b16['faol'],1)} (128) faol bayt hosil bo‘ladi.")
P(f"Parametrlar bo‘yicha o‘rtalashtirilgan ayirmalar matritsasining maksimal qiymati {fz(DT['g_ortacha_p_max'],4)} = 2⁻⁶, ya’ni parametrlar buzg‘unchi nazoratida bo‘lmaganda element S ning o‘zi kabi ishlaydi. Yarim qadamlar bo‘yicha tarqalish (2.2.4-band) differensial tahlil uchun ham o‘rinli: bitta bayt ayirmasi uchinchi yarim qadamdan keyin 31 ta baytga yetadi.")
H2('3.3. Orttirmalarning akslantirishlar va raundlar orqali o‘tishi')
P("Iteratsiya boshidagi holatning bitta baytiga MSB ayirmasi kiritildi (D1) va har bir akslantirishdan keyin faol elementlar soni, MSB izining saqlanishi va ayirmaning butunlay so‘nishi o‘lchandi (2000 juftlik).")
nm={'Bog0':'Bog‘lash(holat, blok)','SBZ0':'SBZ (0-nuqta)','Aralash':'Aralash','Bog1':'Bog‘lash(holat, kₑ)','Sur':'SurHolat, kalit jadvali','Bog2':'Bog‘lash(holat, kₑ)','SBZ8':'SBZ (8-nuqta)','SBZ9':'SBZ (9-nuqta)'}
rows=[["Akslantirish (raund)","256: faol / P(MSB) / so‘nish","128: faol / P(MSB) / so‘nish"]]
for a,b in zip(r256['D1'],r16['D1']): rows.append([f"{nm.get(a[0],a[0])} ({a[1]})",f"{fz(a[2],1)} / {fz(a[3],3)} / {fz(a[4],4)}",f"{fz(b[2],1)} / {fz(b[3],3)} / {fz(b[4],4)}"])
T([3800,2777,2777],rows,"Holatdagi bitta MSB ayirmasining akslantirishlar bo‘yicha o‘tishi (yakuniy variant)")
P("Ayirma birinchi Bog‘lash dayoq butun holatga tarqaladi (256 bitli rejimda 32 baytdan 31,4 tasi) va keyingi barcha akslantirishlarda to‘liq faol qoladi; MSB izi va ayirmaning so‘nishi hech bir qadamda kuzatilmadi. Standart va SBZ variantlarida MSB izi 7 raund davomida ≈0,34 ehtimollik bilan saqlanar va ≈3% juftliklarda ayirma Aralash da yo‘qolar edi.")
rows=[["Akslantirish (raund)","256: faol / so‘nish","128: faol / so‘nish"]]
for a,b in zip(r256['D2'],r16['D2']): rows.append([f"{nm.get(a[0],a[0])} ({a[1]})",f"{fz(a[2],1)} / {fz(a[3],4)}",f"{fz(b[2],1)} / {fz(b[3],4)}"])
T([3800,2777,2777],rows,"Kirish blokidagi ikki elementli MSB ayirmasining o‘tishi (yakuniy variant)")
P("Kirish blokidagi ayirma ham 0-nuqtadagi Bog‘lash dayoq 31 baytga (256) tarqaladi; ayirma so‘ngan juftlik bo‘lmadi. Standart algoritmda bu ayirma Qo‘sh dan holatga ta’sir qilmasdan o‘tar (ehtimollik 1) va keyingi qadamlarda boshqariladigan shaklda qolar edi.")
rows=[["Akslantirish (raund)","Δholat (A ilova, holat[0,0] da MSB ayirmasi)","Faol baytlar"]]
for e in DT['juft']:
    if e['raund']<=1: rows.append([f"{NMA.get(e['amal'],e['amal'])} ({e['raund']})",nl(e['d']),str(e['faol'])])
T([2700,4600,2054],rows,"Yakuniy variant, A ilova ma’lumotlari: boshlang‘ich holatdagi MSB ayirmasining o‘tishi",mono=(1,))
P("A ilova misolida birinchi Bog‘lash dan keyin 32 baytning hammasi farq qiladi va ayirma keyingi akslantirishlarda tasodifiy ko‘rinishda qoladi; standart algoritmda xuddi shu ayirma 1–2-raundlarda 2 va 4 ta baytda, faqat MSB ko‘rinishida saqlanar edi.")
H2('3.4. Kolliziya izlari va ichki kolliziyalar')
BL("Bog‘lash belgilangan X da bijeksiya, Aralash toq kₑ bilan teskarilanuvchi, SurHolat — o‘rin almashtirish: raund funksiyasi holat bo‘yicha bijeksiya, ya’ni ichki kolliziyalar faqat yutish nuqtalarida va xabar farqlari orqali paydo bo‘lishi mumkin.")
BL("Yutish nuqtasida Bog‘lash(holat, blok) dan keyin SBZ(holat, blok) keladi: blok ayirmasi Bog‘lash orqali butun holatga tarqaladi, SBZ esa bitta argumentdagi ayirmani so‘ndirmaydi.")
BL("Oldinga uzatish va chiqish o‘zgartirishi xesh qiymatdan ichki holatni tiklashni va orqaga hisoblashni (o‘rtada uchrashish hujumlari) imkonsiz qiladi.")
H2('3.5. Bardoshlilik bahosi')
T([3200,2050,2050,2054],[["Baho turi","1 raunddan keyin","2 raunddan keyin","2⁻¹²⁸ / 2⁻⁶⁴ ga erishish"],["Pessimistik (1 faol element / chaqiruv, p ≤ 2⁻⁴·²)","≤ 2⁻⁸·⁴","≤ 2⁻¹⁶·⁸","≈16 / ≈8 raund"],["O‘rtacha parametrlar (1 faol element / chaqiruv, ≈2⁻⁶)","≤ 2⁻¹²","≤ 2⁻²⁴","≈11 / ≈6 raund"],["Real (≥ 16 faol element / chaqiruv)","≤ 2⁻¹³⁴","≤ 2⁻²⁶⁹","1 raund"],["SBZ varianti (taqqoslash)","≈1 (MSB izi 0,94)","≈1","8-raund (yutishda)"],["Standart (taqqoslash)","≈1","≈1","9-raund / bardoshli emas"]],"Yakuniy variantda differensial iz ehtimolligining baholari")
H2('3.6. Differensial kriptotahlil bo‘yicha xulosalar')
BL("Yakuniy variantda MSB izlari yo‘qolgan: ayirma birinchi Bog‘lash dayoq butun holatga tarqaladi va hech bir qadamda boshqariladigan shaklda qolmaydi.")
BL("Aralash yadrosi orqali ayirmalar so‘nishi (ichki kolliziyalar) toq kₑ tufayli yo‘qolgan; raund funksiyasi holat bo‘yicha bijeksiya.")
BL("Real baho bo‘yicha differensial chegaraga birinchi raunddayoq, pessimistik baho bo‘yicha 256 bitli rejimda ≈16 raundda erishiladi; standart va SBZ variantlarida yutishsiz raundlar umuman hissa qo‘shmas edi.")

# ===================== 4. ALGEBRAIK =====================
PB(); H1('4. Algebraik kriptotahlil')
H2('4.1. Bardoshlilik mezoni')
P("Linearizatsiya murakkabligi C(n, d) ≈ (Σ_{i≤d} binom(n, i))^2,8; talab: 128 bitli rejimda d ≥ 4, 256 bitli rejimda d ≥ 8.")
H2('4.2. Bog‘lash uchun algebraik tenglamalar')
P("Bitta yarim qadamdagi har bir element uchun tenglamalar quyidagicha yoziladi (u, v, w — oraliq o‘zgaruvchilar):")
F("u = S(U[i] ⊕ X_U[i] ⊕ J),   aᵢ = 2u + 1,   v = S(U[i+1] ⊕ X_T[i] ⊕ K),   bᵢ = 2v + 1,")
F("w · (bᵢ + R·T[i]) + aᵢ·T[i] ≡ 0 (mod 256),   T′[i] = S(w ⊕ X_T[i]),")
P("bu yerda S tenglamalari — har biri 39 ta kvadrat tenglama (8 ta yangi o‘zgaruvchi), Möbius tenglamasi — halqa ustidagi kvadrat tenglama (bit darajasida 2–3 ta modul ko‘paytirish), J va K — m − 1 ta qo‘shish va ko‘paytirish zanjirlari. Element darajasida (parametrlar belgilangan) g ning chiqish bitlari 8 ta kirish bitiga nisbatan 7-darajali (8 bitli bijeksiya uchun eng katta daraja), ya’ni Qo‘sh dagi chiziqli 0-bit va past darajali quyi bitlar endi yo‘q.")
dg=DT['bog_daraja']
T([4677,4677],[["Chiqish bitining ANF darajasi (holat[0] ning 8 bitiga nisbatan)","Bitlar soni (256 ta chiqish biti)"]]+[[k,str(v)] for k,v in dg.items()],"Bitta Bog‘lash chaqiruvi: chiqish bitlarining bitta kirish baytiga nisbatan darajasi")
P("Bitta chaqiruvdan keyin barcha 256 ta chiqish bitining holat[0] bayti bo‘yicha darajasi 7 yoki 8 — 8 o‘zgaruvchili funksiya uchun eng yuqori qiymatlar. Qo‘sh da esa chiqish elementlarining 0-bitlari chiziqli (daraja 1), quyi bitlar darajasi bit raqamiga yaqin edi.")
def cnt(n):
    ADD=(2*n-1,2*n-1,n-1); MUL=(n*(n+1)//2+(n-1)*(2*n-1),)*2+(n*(n+1)//2+(n-1)*(n-1),); Sx=(8,39,39)
    add=lambda a,b,f=1: tuple(x+f*y for x,y in zip(a,b)); return ADD,MUL,Sx,add
def bog(m):
    ADD,MUL,Sx,add=cnt(8); z=(0,0,0); h=z
    h=add(h,ADD,m-1); h=add(h,MUL,m-1); h=add(h,Sx,3*m); h=add(h,MUL,3*m); h=add(h,ADD,2*m)
    return add(z,h,3)
def aral(n): ADD,MUL,Sx,add=cnt(n); return add(add((0,0,0),MUL,128),ADD,144)
e256=A3['eq']['256_std']; e128=A3['eq']['128_std']
b2=bog(16); b1=bog(8); s2=(512,2496,2496); s1=(256,1248,1248)
def tot(*xs): return tuple(sum(v) for v in zip(*xs))
rnd2=tot(aral(8),b2,b2); rnd1=tot(aral(4),b1,b1); r0_2=tot(b2,s2); r0_1=tot(b1,s1)
T([3400,1980,1987,1987],[["Akslantirish","Qo‘sh (256)","Bog‘lash (256)","Bog‘lash (128)"],["O‘zgaruvchilar",sp(e256['qosh'][0]),sp(b2[0]),sp(b1[0])],["Tenglamalar",sp(e256['qosh'][1]),sp(b2[1]),sp(b1[1])],["Nochiziqli tenglamalar",sp(e256['qosh'][2]),sp(b2[2]),sp(b1[2])]],"Bitta chaqiruv uchun bit darajasidagi tenglamalar soni (baho)")
T([3600,2877,2877],[["Akslantirish","0-qatlam darajasi","Yuqori bitlar darajasi"],["Bog‘lash (bitta chaqiruv)","7–8 (bitta bayt bo‘yicha)","7–8"],["SBZ","13 (16 bit bo‘yicha)","13"],["Aralash (kₑ ma’lum)","1","≤ j + 1"],["SurHolat, kalit jadvali","1","1"],["Oldinga uzatish, P(H) ⊕ H","1 / 7–8","1 / 7–8"]],"Yakuniy variant akslantirishlari bo‘yicha algebraik darajalar")
H2('4.3. Raund tenglamalari va 1–3 raund uchun tizimlar')
F("a = Aralash(h⁽ʲ⁻¹⁾, kₑ⁽ʲ⁻¹⁾);  b = Bog‘lash(a, kₑ⁽ʲ⁻¹⁾);  b′ = P·b;  kₑ⁽ʲ⁾ = (Q·kₑ⁽ʲ⁻¹⁾ ⊕ RCⱼ) ∨ 1;  h⁽ʲ⁾ = Bog‘lash(b′, kₑ⁽ʲ⁾).")
P("Kalit jadvali chiziqli (XOR va eng kichik bitni 1 ga tenglashtirish), shuning uchun u tizimga yangi nochiziqli tenglama qo‘shmaydi. Yutish nuqtasida Bog‘lash(holat, blok) va SBZ tenglamalari qo‘shiladi; oldinga uzatish chiziqli.")
rows=[["Rejim","Variant","1 raund: o‘zg. / tengl.","2 raund: o‘zg. / tengl.","3 raund: o‘zg. / tengl."]]
for lab,e in (('256',e256),('128',e128)):
    rows.append([lab,"Standart"]+[f"{sp(e[r][0])} / {sp(e[r][1])}" for r in ('r1','r2','r3')])
for lab,r0,rn in (('256',r0_2,rnd2),('128',r0_1,rnd1)):
    rows.append([lab,"Yakuniy"]+[f"{sp(r0[0]+k*rn[0])} / {sp(r0[1]+k*rn[1])}" for k in (1,2,3)])
T([900,1300,2400,2400,2354],rows,"1, 2 va 3 raund uchun bit darajasidagi tenglamalar tizimlari hajmi (baho)")
P("Yakuniy variantning tenglamalar tizimi standartdagidan ≈3–4 marta kichik (Bog‘lash Qo‘sh dan soddaroq), lekin uning tarkibi buzg‘unchi uchun ancha noqulay: har bir yarim qadamda 3·m ta S-box (39 tadan kvadrat tenglama, kvadrat implitsit tenglamalarsiz oshkor ko‘rinishda 7-darajali) va 0-qatlamda ham chiziqli bo‘lmagan bog‘lanishlar. Standart algoritmda katta tizimning 0-qatlam qismi chiziqli bo‘lib qolardi va linearizatsiya hujumi (Standart-128 da 80 so‘rov bilan 100% aniqlik) amalda ishlardi.")
H2('4.4. Algebraik darajaning o‘sishi')
kb2=r256['kub']; kb1=r16['kub']
rows=[["Rejim, raund r","d = 4 (barcha / 0-qatlam)","d = 8","d = 10"]]
for lab,kb in (('Yakuniy-256',kb2),('Yakuniy-128',kb1)):
    for rr_ in (0,1): rows.append([f"{lab}, r = {rr_}"]+[f"{fz(kb[f'r{rr_}_d{d}'][0],3)} / {fz(kb[f'r{rr_}_d{d}'][1],3)}" for d in (4,8,10)])
rows.append(["Standart-256, r = 0 (taqqoslash)"]+[fz(A2['256_std_r0'][str(d)][0],3) for d in (4,8,10)])
rows.append(["Standart-128, r = 3, 0-qatlam (taqqoslash)"]+[fz(A2['16_std_r3'][str(d)][1][0],3) for d in (4,8,10)])
T([3400,2000,1977,1977],rows,"Kub testlari: yig‘indisi doim nol bo‘lgan bitlar ulushi (4 ta kub; tasodifiy funksiya uchun ≈0,06)")
P("Yakuniy variantda r = 0 (faqat 0-nuqtadagi Bog‘lash va SBZ) dayoq barcha bitlarda, shu jumladan 0-qatlamda, ulush tasodifiy funksiya darajasida (0,03–0,14): xabarning 16 biti bo‘yicha daraja 10 dan katta. Standart-256 da r = 0 da d = 12 uchun ulush 0,84, Standart-128 ning 0-qatlami esa barcha d da 1,00 edi.")
H2('4.5. Linearizatsiya hujumi')
P(f"Kalitli rejimda 0-qatlamning affin modeli (o₀ = A·m₀ ⊕ c) 80 ta xabar bo‘yicha qurildi va 200 ta yangi xabarda tekshirildi: bashorat aniqligi 256 bitli rejimda {fz(c256['affin_0'],3)}, 128 bitli rejimda {fz(c16['affin_0'],3)} — tasodifiy taxmin darajasi (Standart-128 da 1,000 edi).")
H2('4.6. Algebraik kriptotahlil bo‘yicha xulosalar')
BL("Bog‘lash har bir elementni S-box orqali o‘tkazadi; 0-qatlam ham chiziqli bo‘lmagan bog‘lanishga ega, tenglamalar darajasi bitta yarim qadamdayoq yuqori.")
BL("Tenglamalar tizimi standartdagidan kichik, lekin chiziqli qism yo‘q; kub testlarida daraja birinchi yutish nuqtasidan keyinoq tasodifiy funksiya darajasida.")
BL("Linearizatsiya hujumi ishlamaydi; algebraik bardoshlilik chegarasiga 0-nuqtadagi yutishdan keyinoq erishiladi.")

# ===================== 5. INTEGRAL =====================
PB(); H1('5. Integral kriptotahlil')
H2('5.1. Bog‘lash ning tanlangan to‘plamlarga ta’siri')
P(f"Bitta faol bayt (256 bitli rejimda holat[0] barcha 256 qiymatni qabul qiladi, 128 bitli rejimda holat[0], holat[1] yarim baytlari — juftlangan bayt) Bog‘lash dan keyin quyidagi xossalarga ega bo‘ladi (40 tajriba bo‘yicha 32 pozitsiya uchun o‘rtacha): 256 bitli rejimda U — {fz(b256['integral'].get('U',0),2)}, B — {fz(b256['integral'].get('B',0),2)}, C — {fz(b256['integral'].get('C',0),2)}; 128 bitli rejimda U — {fz(b16['integral'].get('U',0),2)}, B — {fz(b16['integral'].get('B',0),2)}. 0-qatlam yig‘indisining nol bo‘lish ulushi {fz(b256['integral_0qatlam'],3)} va {fz(b16['integral_0qatlam'],3)} (tasodifiy funksiya uchun 0,5). Qo‘sh dan farqli o‘laroq, Bog‘lash 0-qatlam balansini ham saqlamaydi: Qo‘sh da u ehtimollik 1 bilan saqlanar edi.")
H2('5.2. Integral xossalarning raundlar orqali o‘tishi')
ih2=r256['integral_holat']; ib2=r256['integral_blok']; ih1=r16['integral_holat']; ib1=r16['integral_blok']
nm2={'Bog0':'Bog‘lash(holat, blok)','SBZ0':'SBZ (0-nuqta)','Aralash':'Aralash','Bog1':'Bog‘lash(holat, kₑ)','Sur':'SurHolat, kalit jadvali','Bog2':'Bog‘lash(holat, kₑ)'}
rows=[["Akslantirish (raund)","256: holat faol","256: blok faol","128: holat faol","128: blok faol"]]
for key in list(ih2.keys())[:10]:
    j,n=key.split(':'); rows.append([f"{nm2.get(n,n)} ({j})",", ".join(map(str,ih2[key])),", ".join(map(str,ib2[key])),", ".join(map(str,ih1[key])),", ".join(map(str,ib1[key]))])
T([2700,1700,1700,1627,1627],rows,"Bit-qatlamlar bo‘yicha doim balanslangan bitlar soni (20 tajriba; 0…7 yoki 0…3-qatlamlar)")
P("Holatdagi faol to‘plam birinchi Bog‘lash dayoq balansini to‘liq yo‘qotadi (standart va SBZ variantlarida 0-qatlam 1–7-raundlarda balanslangan edi). Kirish blokidagi faol to‘plam 0-nuqtadagi Bog‘lash va SBZ dan keyin 15 baytda (128 bitli rejimda 14 baytda) balanslangan qoladi — bu blok bayti faqat Bog‘lash ning ayrim parametrlariga ta’sir qilishi bilan bog‘liq; Aralash dan keyin balanslangan baytlar qisman saqlanadi, birinchi raunddagi Bog‘lash(holat, kₑ) dan keyin esa balans butunlay yo‘qoladi.")
for joy,lab in (('holat','holat[0,0] faol'),('blok','blok[0] faol')):
    rows=[["Akslantirish",f"XOR yig‘indi ({lab}, A ilova, 256 bitli rejim)"]]
    for e in DT[f'int_{joy}']: rows.append([NMA.get(e['amal'],e['amal']),nl(e['yig'])])
    T([3000,6354],rows,f"Yakuniy variant, A ilova misoli: {lab}, 256 ta holat bo‘yicha XOR yig‘indilar (0-nuqta va 1-raund)",mono=(1,))
P("Holat faol bo‘lganda birinchi Bog‘lash dan keyinoq yig‘indilar tasodifiy (toq qiymatlar ham uchraydi). Blok faol bo‘lganda 0-nuqtadagi Bog‘lash va SBZ dan keyin yig‘indilarning bir qismi 00 — bu 15 ta balanslangan baytga mos keladi; 1-raunddagi Bog‘lash(holat, kₑ) dan keyin esa ular ham yo‘qoladi.")
H2('5.3. To‘liq xesh uchun integral farqlovchi')
T([3200,2050,2050,2054],[["Rejim","Standart","SBZ varianti","Yakuniy variant"],["256 bitli: 0-qatlam doim nol bitlar",str(IST['toliq_xesh']['256']['qatlam_boyicha_doim_nol_bitlar'][0]),str(IS['toliq_xesh']['256']['qatlam_boyicha_doim_nol_bitlar'][0]),str(c256['integral_toliq'][0])],["128 bitli: 0-qatlam doim nol bitlar",str(IST['toliq_xesh']['16']['qatlam_boyicha_doim_nol_bitlar'][0]),str(IS['toliq_xesh']['16']['qatlam_boyicha_doim_nol_bitlar'][0]),str(c16['integral_toliq'][0])],["Barcha qatlamlar (256 / 128)","—","—",f"{', '.join(map(str,c256['integral_toliq']))} / {', '.join(map(str,c16['integral_toliq']))}"]],"To‘liq xesh: bitta faol bayt bo‘yicha doim balanslangan bitlar (yakuniy variant uchun 10 tajriba)")
P("Yakuniy variantda to‘liq xesh uchun integral farqlovchi yo‘q (256 bitli rejimda bitta qatlamda 2 bit 10 tajribaning hammasida nol chiqdi, bu tasodifiy holatda kutilgan darajada). Standart-128 da 0-qatlamning 32 biti doim nol edi.")
H2('5.4. Integral kriptotahlil bo‘yicha xulosalar')
BL("Bog‘lash bayt darajasidagi va bit darajasidagi integral xossalarni bitta chaqiruvda yo‘qotadi; 0-qatlam balansi endi saqlanmaydi.")
BL("Holat bo‘yicha integral farqlovchi birinchi Bog‘lash dan keyin, blok bo‘yicha faol to‘plam — birinchi raunddagi Bog‘lash dan keyin yo‘qoladi; to‘liq xesh uchun farqlovchi topilmadi.")
BL("Standart va SBZ variantlaridagi 7 raundli ichki integral farqlovchi yakuniy variantda mavjud emas.")

# ===================== XULOSA =====================
PB(); H1('Umumiy xulosa')
T([2300,2350,2350,2354],[["Ko‘rsatkich","Standart","SBZ varianti","Yakuniy variant"],
 ["Tezlik (C), 256 / 128 bitli rejim","1 / 1","≈1 / ≈1",f"≈1,5 / ≈2,2–2,7 marta tez"],
 ["Chiziqli: yutishsiz raundlar hissasi","yo‘q (c = 1)","yo‘q (c = 1)","har raundda (c ≈ 0 birinchi raunddan)"],
 ["Chiziqli: chiqishdagi munosabatlar","≈6 ta, doimiy bitlar","≈6 ta, doimiy bitlar","yo‘q (rang 32)"],
 ["Differensial: MSB izi (7 raund)","0,34","0,34","0"],
 ["Differensial: ichki kolliziyalar (Aralash)","≈3%","≈3%","0"],
 ["Algebraik: 0-qatlam","chiziqli (128 bitli rejimda butun xesh)","yutishda 13-daraja","har bir Bog‘lash da S-box"],
 ["Integral: ichki farqlovchi","7 raund (128 da butun xesh)","7 raund","yo‘q"],
 ["Orqaga hisoblash / proobraz","mumkin (oldinga uzatish yo‘q)","mumkin","oldinga uzatish va P(H) ⊕ H bilan yopilgan"]],"Standart algoritm, SBZ varianti va yakuniy variantni solishtirish")
P("Yakuniy variant standart algoritmdan 256 bitli rejimda ≈1,5 marta, 128 bitli rejimda ≈2,2–2,7 marta tez va to‘rtta kriptotahlil usuli bo‘yicha aniqlangan barcha asosiy kamchiliklar unda kuzatilmaydi: yutishsiz raundlarning T-funksiya xossasi (0-qatlam chiziqliligi, MSB izlari, 0-qatlam balansi) Bog‘lash orqali, Aralash degeneratsiyasi (chiqishdagi doimiy munosabatlar, ichki kolliziyalar, eng yomon kalitlar) toq kₑ orqali, yutish nuqtasidagi zaiflik SBZ orqali, chiqishdagi tuzilmaviy munosabatlar va orqaga hisoblash imkoniyati oldinga uzatish va chiqish o‘zgartirishi orqali bartaraf etilgan.")
H2('Keyingi ishlar')
BL("Bog‘lash orqali faol elementlarning minimal sonini hisoblab, chiziqli va differensial bardoshlilikning isbotlanadigan chegaralarini olish (hozirgi pessimistik baholarni aniqlashtirish).")
BL("Bitta chaqiruvdagi to‘liq tarqalishni hisobga olib, raundlar sonini kamaytirish imkoniyatini baholash (tezlikni yanada oshiradi).")
BL("128 bitli rejimda Aralash va SurHolat ni ham bayt darajasiga o‘tkazib, ikkala rejim tuzilishini to‘liq birxillashtirish.")
BL("Raund konstantalari RCⱼ va chiqish o‘zgartirishi konstantalarini yakuniy tanlash; standart matnini (6.2-band) yangi akslantirishlar bilan qayta yozish.")
P("Barcha hisob-kitoblar uchun dasturlar uzmst285_tahlil paketida (yakuniy_variant.py, boglash.py, yakuniy.py, yakuniy.c) va yakuniy_variant.ipynb daftarida.")
def _fix(x):
    if isinstance(x,str): return _re.sub(r'⟦(\w+)⟧',lambda m:str(TK[m.group(1)]),x)
    if isinstance(x,list): return [_fix(y) for y in x]
    return x
B=[_fix(b) for b in B]
json.dump(B,open('blocks.json','w'),ensure_ascii=False); print(len(B),tc[0],fc[0])
