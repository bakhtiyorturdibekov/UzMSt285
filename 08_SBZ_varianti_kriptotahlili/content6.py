import json, math, re as _re
K='/home/claude/ka/'; J=lambda f: json.load(open(K+f+'.json'))
L1,L2,L3,D1,A1,A2,A3,EX=[J(x) for x in ['lin1','lin2','lin3','dif1','alg1','alg2','alg3','ex']]
D2=J('dif2'); S2=J('sbz_extra2'); S3=J('sbz_extra3'); HO=J('ho_sbz256_jami'); HO16=json.load(open(K+'ho_16_sbz_16_2.json')); HOS=json.load(open(K+'ho_16_std_16_2.json')); D3=J('dif3'); SX=J('sbz_extra'); MR=json.load(open('/home/claude/nb/misollar_natijalari.json'))
I=json.load(open('/home/claude/pkg/uzmst285_tahlil/natijalar/integral_sbz.json'))
B=[]; tc=[0]; fc=[0]; TK={}
H1=lambda t:B.append(['h1',t]); H2=lambda t:B.append(['h2',t]); H3=lambda t:B.append(['h3',t])
P=lambda t:B.append(['p',t]); F=lambda t:B.append(['f',t]); BL=lambda t:B.append(['b',t]); PB=lambda:B.append(['pb'])
def T(w,rows,cap,mono=(),key=None):
    tc[0]+=1; B.append(['cap',f"{tc[0]}-jadval. {cap}"]); B.append(['t',w,rows,list(mono)])
    if key: TK[key]=tc[0]
def IMG(p,w,h,cap): fc[0]+=1; B.append(['img',p,w,h]); B.append(['fcap',f"{fc[0]}-rasm. {cap}"])
fz=lambda x,d=2:(f'{x:.{d}f}').replace('.',','); nl='\n'.join; sp=lambda n:f"{n:,}".replace(',',' ')
opn={'Aralash':'Aralash(holat, kₑ)','Qosh1':'Qo‘sh(holat, kₑ)','Sur':'SurHolat, SurKalit','Qosh2':'Qo‘sh(holat, kₑ)','Tuz':'TuzilmaKalit(kₑ, k)','Qosh0':'Qo‘sh(holat, blok)','BZ0':'SBZ (0-nuqta)','BZ8':'SBZ (8-nuqta)','BZ9':'SBZ (9-nuqta)','Qosh_inj8':'Qo‘sh(holat, blok)','Qosh_inj9':'Qo‘sh(holat, blok)'}

B.append(['title','BaytZichlash O‘RNIGA SBZ QO‘LLANILGAN O‘zMSt 285:2024 1-ALGORITMINING CHIZIQLI, DIFFERENSIAL, ALGEBRAIK VA INTEGRAL KRIPTOTAHLILI'])
B.append(['sub','SBZ varianti bo‘yicha hisobot (Aralash va TuzilmaKalit standartdagidek)'])
H1('Kirish')
P("Ushbu hisobotda O‘zMSt 285:2024 standartining 1-algoritmi yutish nuqtasida BaytZichlash o‘rniga SBZ o‘zgartirishi qo‘llanilgan holda to‘rtta kriptotahlil usuli bo‘yicha buzg‘unchi nuqtai nazaridan baholanadi: chiziqli, differensial, algebraik va integral. Algoritmning qolgan qismi — Qo‘sh, Aralash, SurHolat, SurKalit, TuzilmaKalit, raundlar soni, uzunlik va NY bloklari — standartdagidek qoldirilgan; Aralash/TuzilmaKalit va raund funksiyasi bo‘yicha boshqa tavsiyalar alohida tahlil qilinadi.")
P("SBZ o‘zgartirishi holat bayti h va Qo‘sh dan keyingi holatn bayti n ni bitta baytga birlashtiradi:")
F("holat[i] ← S( h[i] ⊕ S( n[i] ) ),   i = 0, …, 31   (256 bitli rejim),")
P("bu yerda S — AES (FIPS 197) standartining S-boxi. 128 bitli rejimda qo‘shni yarim baytlar juftlanadi: H = 16·h[2j] + h[2j+1], N = 16·n[2j] + n[2j+1], Q = S(H ⊕ S(N)), h[2j] = Q ≫ 4, h[2j+1] = Q ∧ 15. Ikkala rejim ko‘rib chiqiladi: *SBZ-256* va *SBZ-128*. Taqqoslash uchun standart algoritm natijalari (BaytZichlash bilan) qisqacha keltiriladi; ular «Standart algoritm kriptotahlili» hisobotida batafsil berilgan.")
P("Hisob-kitoblar mustaqil dasturiy realizatsiyada bajarildi; u standart va SBZ variantlari uchun barcha nazorat qiymatlarini takrorlaydi (SBZ-256: 42f97daa a8e7010b …, SBZ-128: bd745e2e d572ea42 …). Akslantirishlar ko‘rsatkichlari barcha kirishlar bo‘yicha to‘liq, raund darajasidagi ko‘rsatkichlar tanlanma asosida o‘lchandi.")
T([1700,7650],[["Qadam","Akslantirishlar (SBZ varianti)"],["0-nuqta","Qo‘sh(holat, blok), SBZ(holat, holatn) — yutish"],["1–7-raundlar","Aralash(holat, kₑ) → Qo‘sh(holat, kₑ) → SurHolat, SurKalit → Qo‘sh(holat, kₑ) → TuzilmaKalit(kₑ, k)"],["8-raund","Aralash → Qo‘sh(holat, kₑ) → SurHolat, SurKalit → Qo‘sh(holat, blok), SBZ — yutish → TuzilmaKalit"],["9-raund","1–7-raundlar kabi; oxirida Qo‘sh(holat, blok), SBZ — yutish"],["10-raund","1–7-raundlar kabi"]],"SBZ variantida bitta tashqi iteratsiyadagi akslantirishlar")
P("Asosiy strukturaviy kuzatish o‘zgarmaydi: 1–7- va 10-raundlar 2ⁿ moduli bo‘yicha arifmetika va o‘rin almashtirishlardan iborat bo‘lgani uchun T-funksiya bo‘lib qoladi — natijaning j-biti kirishlarning faqat 0…j-bitlariga bog‘liq. SBZ esa yutish nuqtasida barcha 16 kirish bitini aralashtiruvchi, optimal ko‘rsatkichli chiziqli bo‘lmagan akslantirish sifatida ishlaydi. Shuning uchun hisobotda har bir usul bo‘yicha alohida e’tibor yutish nuqtalariga qaratiladi.")
P("Belgilashlar: *bit-qatlam j* — holat elementlarining j-bitlari; *0-qatlam* — eng kichik bitlar (juft/toqlik); *yutish nuqtasi* — SBZ bajariladigan nuqta; *faol bayt* — niqobi yoki ayirmasi noldan farqli bayt; integral to‘plam xossalari: A (barcha qiymatlar bir martadan), C (doimiy), B (XOR yig‘indisi nol), U (noma’lum).")

# =================== 1. CHIZIQLI ===================
PB(); H1('1. Chiziqli kriptotahlil')
H2('1.1. Usulning mohiyati va bardoshlilik mezoni')
P("Chiziqli kriptotahlilda buzg‘unchi kirish va chiqish bitlarining XOR yig‘indilari orasidagi tengliklarni qidiradi. F akslantirish uchun kirish niqobi α va chiqish niqobi β bo‘lgan approksimatsiyaning korrelyatsiyasi va chetlanishi:")
F("c_F(α → β) = 2⁻ⁿ · Σₓ (−1)^(β·F(x) ⊕ α·x),      ε = c/2.")
P("c = 2p − 1, bu yerda p — tenglikning bajarilish ehtimolligi. Iz korrelyatsiyasi oraliq korrelyatsiyalar ko‘paytmasiga teng, hujum uchun N ≈ c⁻² ma’lumot kerak. 256 bitli rejim uchun |c| ≤ 2⁻⁶⁴, 128 bitli rejim uchun |c| ≤ 2⁻³² talab qilinadi.")
H2('1.2. Akslantirishlarning korrelyatsion matritsalari va approksimatsiya tenglamalari')
H3('1.2.1. AES S-box')
d=L1['S_lat_dist']
P(f"S ning 256×256 korrelyatsion matritsasi to‘liq hisoblandi (Uolsh–Adamar o‘zgartirishi orqali). Noldan farqli chiqish niqoblari uchun |c| faqat {{0, 2⁻⁶, …, 7·2⁻⁶, 2⁻³}} qiymatlarini qabul qiladi; maksimal |c| = 32/256 = 2⁻³ (chetlanish 2⁻⁴), bunday approksimatsiyalar soni {L1['S_best_count']} ta. Matritsaning bo‘lagi va elementlar taqsimoti ⟦slat⟧- va ⟦sdist⟧-jadvallarda.")
blk=EX['S_lat_block']
T([1250]+[1012]*8,[["β \\ α"]+[f"{a:02X}" for a in range(1,9)]]+[[f"{b:02X}"]+[str(v) for v in blk[b-1]] for b in range(1,9)],"S korrelyatsion matritsasining bo‘lagi: W(α → β) = 256·c",key='slat')
T([3600,1400,1400,1400,1550],[["|W| qiymati","0","4…12","16…24","28…32"],["Elementlar soni",str(d['0']),str(d['4']+d['8']+d['12']),str(d['16']+d['20']+d['24']),str(d['28']+d['32'])],["|c|","0","2⁻⁶…3·2⁻⁶","2⁻⁴…3·2⁻⁵","7·2⁻⁶…2⁻³"]],"S korrelyatsion matritsasi elementlarining taqsimoti (β ≠ 0)",key='sdist')
F("y₀ = x₀ ⊕ x₂ ⊕ x₃ ⊕ x₅ ⊕ 1,     c = 2⁻³   (y = S(x), α = 2D, β = 01).")
H3('1.2.2. SBZ')
P("SBZ uchun korrelyatsiya S korrelyatsiyalari orqali aniq ifodalanadi. x = h ⊕ S(n) almashtirishida yig‘indi ikkita mustaqil yig‘indiga ajraladi:")
F("c_SBZ((α, β) → γ) = c_S(α → γ) · c_S(β → α),")
P("bu yerda α — h dagi niqob, β — n dagi niqob, γ — chiqish niqobi. Bundan uchta muhim xulosa: (1) h dagi niqob «o‘rta» niqobga teng bo‘lishi va noldan farq qilishi shart, ya’ni faqat n orqali o‘tuvchi approksimatsiya yo‘q; (2) maksimal |c| = (2⁻³)² = 2⁻⁶; (3) korrelyatsion matritsa (65536 × 255) S matritsasidan to‘liq quriladi. To‘liq hisob natijasi ⟦sbzdist⟧-jadvalda.")
sd=SX['SBZ_lat_taqsimot']
grp=[("0",[0]),("16…112 (≤ 2⁻⁹)",[16,32,48,64,80,96,112]),("128…240",[128,144,160,192,224,240]),("256…480",[256,288,320,336,384,400,448,480]),("512…896",[512,560,576,640,672,768,784,896]),("1024 (2⁻⁶)",[1024])]
T([4354,2500,2500],[["|W_SBZ| = 2¹⁶·|c|","Elementlar soni","Ulushi, %"]]+[[g,sp(sum(sd.get(str(v),0) for v in vs)),fz(100*sum(sd.get(str(v),0) for v in vs)/(255*65536),2)] for g,vs in grp],"SBZ korrelyatsion matritsasi elementlarining taqsimoti (γ ≠ 0; 255 × 65536 element)",key='sbzdist')
P(f"Maksimal |c| = 1024/65536 = 2⁻⁶ atigi {sp(sd['1024'])} ta (α, β, γ) uchlikda erishiladi (elementlarning 0,04 foizi). Masalan, α = 2D, β = 1A, γ = 01 uchun approksimatsiya tenglamasi barcha 65536 ta (h, n) juftlikda tekshirildi: chap tomon {MR['L4']['ones']} ta juftlikda 1 ga teng, ya’ni c = {MR['L4']['c']} = −2⁻⁶:")
F("y₀ ⊕ (h₀ ⊕ h₂ ⊕ h₃ ⊕ h₅) ⊕ (n₁ ⊕ n₃ ⊕ n₄) = 1,     c = 2⁻⁶   (y = S(h ⊕ S(n))).")
P("SBZ korrelyatsion matritsasini qurish tartibi: har bir chiqish niqobi γ uchun S matritsasining γ-satridan |c_S(α → γ)| katta bo‘lgan «o‘rta» niqoblar α tanlanadi, har bir α uchun S matritsasining α-satridan eng yaxshi kirish niqobi β olinadi. γ = 01 uchun eng yaxshi sakkizta approksimatsiya quyidagi jadvalda.")
rr=[["α (h niqobi)","β (n niqobi)","W_S(α → 01)","W_S(β → α)","c_SBZ"]]
for a,b,w1,w2,c_ in S2['gamma01']: rr.append([f"{a:02X}",f"{b:02X}",str(w1),str(w2),("−" if c_<0 else "")+("2⁻⁶" if abs(abs(c_)-2**-6)<1e-12 else fz(abs(c_),5))])
T([1800,1800,1900,1900,1954],rr,"γ = 01 (chiqishning 0-biti) uchun eng yaxshi SBZ approksimatsiyalari")
P(f"Agar buzg‘unchi h dagi niqobni faqat quyi bitlar bilan cheklasa (α ∈ {{01, 02, 03}}), eng yaxshi korrelyatsiya {fz(L1['SBZ_gamma1_alpha_low'],4)} ≈ 2⁻⁶·⁴ ga kamayadi. 128 bitli rejimda SBZ juftlangan baytlarga qo‘llanadi, shuning uchun bir faol bayt (ikki yarim bayt) uchun ham chegara 2⁻⁶. Taqqoslash: standart Z jadvalida maksimal |c| = 0,25, XOR da 1.")
T([2800]+[819]*8,[["SBZ chiqish biti j","0","1","2","3","4","5","6","7"],["Maks. |c|"]+["2⁻⁶"]*8,["Maks. approksimatsiyalar soni"]+[str(c_) for _,c_ in S3['sbz_bit_max']]],"SBZ: har bir chiqish biti uchun eng yaxshi korrelyatsiya")
P("Har bir chiqish biti uchun maksimal |c| bir xil (2⁻⁶) va 25 ta (α, β) juftligida erishiladi, ya’ni SBZ da «zaif» chiqish biti yo‘q. 128 bitli rejimda chiqish niqobi bitta yarim baytda bo‘lsa (γ ∈ {01, 02, 04, 08} — quyi yarim bayt, {10, 20, 40, 80} — yuqori yarim bayt), u juftlangan baytning mos bitiga to‘g‘ri keladi va chegara ham 2⁻⁶ bo‘ladi; kirish niqoblari esa juftlangan ikkala yarim baytga tarqaladi.")
H3('1.2.3. Qo‘sh, Aralash, SurHolat, SurKalit, TuzilmaKalit')
qa,qm,qs=L1['Qosh_bitj_bestcorr_avg'],L1['Qosh_bitj_bestcorr_min'],L1['Qosh_bitj_corr_avg']
P("Raund akslantirishlari standartdagidek bo‘lgani uchun ularning approksimatsiya tenglamalari ham o‘zgarmaydi. Qo‘sh da A va B toq, R juft, shuning uchun x⁻¹ ≡ x (mod 2): y₀ = x₀ (c = 1); 1-bit deyarli doim chiziqli (y₁ = x₁ ⊕ δ·x₀, c ≥ 0,992). Bit-qatlamlar bo‘yicha korrelyatsiyalar ⟦qosh⟧-jadvalda.")
T([2880]+[808]*8,[["Chiqish biti j","0","1","2","3","4","5","6","7"],["Eng yaxshi |c| (o‘rtacha)"]+[fz(v,3) for v in qa],["Eng yaxshi |c| (minimum)"]+[fz(v,3) for v in qm],["|c(xⱼ → yⱼ)| (o‘rtacha)"]+[fz(v,3) for v in qs]],"Qo‘sh elementining bit-qatlamlar bo‘yicha korrelyatsiyalari (200 ta parametrlar to‘plami)",key='qosh')
pm=MR['L1']['param']
P(f"A ilova ma’lumotlarida 0-nuqtadagi Qo‘sh ning holat[0,0] elementi uchun (R = {pm['R']}, A₁ = {pm['A1']}, B₁ = {pm['B1']}, A₂ = {pm['A2']}, B₂ = {pm['B2']}) barcha 256 kirishda y₀ = x₀ ({MR['L1']['y0_ok']}/256) va y₁ = x₁ ⊕ x₀ ({MR['L1']['y1'][1]}/256) tengliklari bajarildi; chiqish bitlari bo‘yicha eng yaxshi korrelyatsiyalar: " + ", ".join(fz(v,3) for v in MR['L1']['bitc']) + ".")
P("Aralash uchun 0-qatlamda aniq chiziqli tenglamalar o‘rinli (σᵤ = Σᵢ kₑ[i,u]₀):")
F("h′[u,u]₀ = σᵤ·h[u,u]₀ ⊕ Σ_{i≠u} kₑ[i,u]₀·h[i,i]₀,   h′[s,u]₀ = σᵤ·h[s,u]₀ ⊕ kₑ[s,u]₀·Σᵢ h[i,u]₀ ⊕ Σ_{i≠s,u} kₑ[i,u]₀·h[s,i]₀,")
P("ya’ni h′₀ = M(k₀)·h₀, c = 1; 1-bitda ko‘chirishlar paydo bo‘ladi (eng yaxshi korrelyatsiya o‘rtacha 0,53). SurHolat va SurKalit niqoblarni pozitsiyalar bo‘yicha ko‘chiradi (c = 1), TuzilmaKalit kₑ₀ = k₀ tengligini ta’minlaydi.")
T([3700,2800,2854],[["Akslantirish","SBZ-256","SBZ-128"],["SBZ (yutish), maks. |c|","2⁻⁶","2⁻⁶ (juftlangan bayt)"],["Qo‘sh: 0-bit / 1-bit","1 / ≥ 0,99","1 / ≥ 0,99"],["Aralash: 0-qatlam / 1-bit","1 / o‘rtacha 0,53","1 / o‘rtacha 0,53"],["SurHolat, SurKalit, TuzilmaKalit","1","1"]],"Akslantirishlar bo‘yicha eng yaxshi korrelyatsiyalar (SBZ varianti)")
H2('1.3. Raund approksimatsiya tenglamasi va uning raundlar bo‘yicha o‘tishi')
P("Yutishsiz raundlar uchun 0-qatlam raund tenglamasi standartdagidek:")
F("h₀⁽ʲ⁾ = P · M(k₀) · h₀⁽ʲ⁻¹⁾ = L · h₀⁽ʲ⁻¹⁾,     c = 1    (j = 1, …, 7, 10).")
P("8- va 9-raunddagi yutish nuqtasida yangi holatning 0-biti S(h ⊕ S(n)) ning 0-biti bo‘ladi; uni h₀ va n₀ ning chiziqli funksiyasi orqali yaqinlashtirishning eng yaxshi korrelyatsiyasi ≈2⁻⁶·⁴. A ilova kaliti va xabarida SBZ-256 da 1-raund akslantirishlari bo‘yicha kuzatuv ⟦izop⟧-jadvalda.")
rows=[["Akslantirish (1-raund)","Holat","0-qatlam","Mos bitlar"]]
for s in MR['L1']['qadamlar']: rows.append([opn[s['amal']],nl(s['holat']),nl(s['qatlam0']),f"{s['mos']}/32"])
T([2200,3200,2300,1654],rows,"SBZ-256, A ilova ma’lumotlari: 1-raund akslantirishlari bo‘yicha 0-qatlam tenglamasining bajarilishi",mono=(1,2),key='izop')
T([2600]+[675]*10,[["Raund j"]+[str(j) for j in range(1,11)],["A ilova: mos bitlar (SBZ-256)"]+[str(v) for v in MR['L1']['raund_mos']],["c, SBZ-256"]+[fz(v,2) for v in L2['lsb_pred_256_sbz']],["c, SBZ-128"]+[fz(v,2) for v in L2['lsb_pred_16_sbz']],["c, Standart-128 (taqqoslash)"]+[fz(v,2) for v in L2['lsb_pred_16_std']]],"0-qatlam raund tenglamasining raundlar bo‘yicha korrelyatsiyasi (1500 kalit)",key='raundc')
r8=S2['raund8_iz']
T([2800]+[1092]*6,[["8-raund akslantirishi"]+[opn.get(n,n) for n,_ in r8],["Mos bitlar (32 dan)"]+[str(m) for _,m in r8]],"SBZ-256, A ilova: 8-raund akslantirishlari bo‘yicha 0-qatlam bashoratining bajarilishi")
P("8-raundda Aralash, Qo‘sh, SurHolat va Qo‘sh(holat, blok) dan keyin ham 0-qatlam bashorati 32/32, faqat SBZ dan keyin moslik 17/32 ga — tasodifiy darajaga — tushadi. Bu chiziqli izning yagona «to‘lov» nuqtasi aynan SBZ ekanini akslantirishma-akslantirish ko‘rsatadi.")
IMG('ch1.png',15.5,6.9,"0-qatlam tenglamasining raundlar bo‘yicha korrelyatsiyasi (chapda) va SBZ yutish qatlamlari bo‘yicha iz korrelyatsiyasi chegarasi (o‘ngda)")
P("1–7-raundlarda korrelyatsiya ikkala rejimda aniq 1, 8-raunddagi SBZ dan keyin u tasodifiy darajaga tushadi. SBZ-128 dagi asosiy o‘zgarish shu: Standart-128 da 0-qatlam XOR tufayli butun xesh bo‘yicha c = 1 bilan kuzatilardi, SBZ-128 da esa u birinchi ichki yutishdayoq buziladi. 10-raunddagi kichik korrelyatsiya (≈0,07) chiqishdagi doimiy munosabatlar bilan bog‘liq (1.5-bo‘lim).")
H2('1.4. Yutish qatlamlari, faol baytlar va iz korrelyatsiyasi')
P("Chiziqli bardoshlilikni yutish qatlamlari ta’minlaydi: har bir faol bayt SBZ dan o‘tganda korrelyatsiyani kamida 2⁶ marta kamaytiradi. Qatlamlar 0, 8, 9, 0′, 8′, 9′ tartibida keladi, ular orasidagi 0-qatlam akslantirishlari L⁸, L, L, L⁸, L; iz oxirgi qatlamdan orqaga Lᵀ bilan tarqatiladi. Faol baytlar zanjiri yutish o‘zgartirishiga bog‘liq emas (u L bilan aniqlanadi), shuning uchun u standart hisobotdagi bilan bir xil; o‘zgaradigani — har bir faol bayt uchun to‘lov.")
rows=[["Qatlamlar","Faol baytlar: min / mediana","SBZ: log₂|c| (mediana)","SBZ: log₂|c| (eng yomon)","Standart-256: log₂|c| (mediana)"]]
for k_ in range(1,7):
    v=L3[str(k_)]; rows.append([str(k_),f"{v['min']} / {fz(v['median'],1)}",f"≤ −{fz(6*v['median'],0)}",f"≤ −{6*v['min']}",f"≤ −{fz(2*v['median'],0)}"])
T([1500,2300,1900,1900,1754],rows,"Yutish qatlamlari bo‘yicha faol baytlar va iz korrelyatsiyasi chegarasi",key='chain')
rr=[["Raund (umumiy hisob)","1–7","8","9–10","11 (2-iter. 0-nuqta)","12–18","19 (8′)","20 (9′)"],
    ["O‘tilgan yutish qatlamlari","0","1","2","3","3","4","5"],
    ["SBZ, mediana kalit: log₂|c| ≤","0",str(-6*int(L3['1']['median'])),str(-6*int(L3['2']['median'])),str(-6*int(L3['3']['median'])),str(-6*int(L3['3']['median'])),str(-6*int(L3['4']['median'])),fz(-6*L3['5']['median'],0)],
    ["SBZ, eng yomon kalit: log₂|c| ≤","0","−6","−12","−18","−18","−24","−30"]]
T([2800,800,750,800,1300,900,900,1104],rr,"SBZ: raundlar bo‘yicha iz korrelyatsiyasi chegarasi (1-raund kirishidan boshlab)")
P("SBZ-256 da 2⁻⁶⁴ chegarasiga mediana kalitlarda 4-qatlamda (−90), ya’ni 2-iteratsiyaning 0-nuqtasida (≈11-raund) erishiladi; standart algoritmda buning uchun 5–6 ta qatlam kerak edi. Eng yomon kalitlarda har bir qatlamda bitta faol bayt qoladi va 2⁻⁶⁴ ga 11 ta qatlamda (≈4 ta iteratsiya, ≈37 raund) erishiladi; bunday kalitlar SBZ ga emas, Aralash matritsasining tuzilishiga bog‘liq (A ilova kaliti ham shunday: L ning [0,3] satrida bitta birlik bor). SBZ-128 uchun 2⁻³² chegarasiga mediana kalitlarda 4-qatlamda, eng yomon holatda 6-qatlamda (2 ta iteratsiya, 20 raund) erishiladi.")
P("Ma’lumot hajmi nuqtai nazaridan: bitta yutish qatlamidan bitta faol bayt bilan o‘tuvchi iz uchun |c| ≤ 2⁻⁶, ya’ni hujum uchun ≈2¹² xabar kerak; mediana kalitda 4 ta qatlamdan keyin |c| ≤ 2⁻⁹⁰ va zarur ma’lumotlar hajmi 2¹⁸⁰ dan oshadi. Standart-256 da xuddi shu 4 ta qatlam uchun chegara 2⁻³⁰ (2⁶⁰ xabar) edi.")
H3('1.4.1. Iz qurish misoli (SBZ-256, A ilova kaliti)')
P("Quyidagi jadvalda A ilova kaliti uchun uchta yutish qatlamidan (0, 8, 9) o‘tuvchi eng yaxshi izning qurilishi qadamma-qadam ko‘rsatilgan. Bu kalit uchun L ning [0,3] satri va ustunida yagona birlik bor, shuning uchun iz barcha qatlamlarda holat[0,3] pozitsiyasidan o‘tadi.")
T([1900,2100,3254,2100],[["Qadam","Niqob pozitsiyasi","Approksimatsiya tenglamasi","Korrelyatsiya"],
 ["Xesh chiqishi (10-raunddan keyin)","[0,3]₀","h₀⁽¹⁰⁾[0,3] = h₀⁽⁹⁾[0,3] (L ning [0,3] satri)","1"],
 ["9-nuqtadagi SBZ","[0,3] bayt","y₀ = ⟨α, h⟩ ⊕ ⟨β, n⟩ (α ∈ {01, 02, 03})","≤ 2⁻⁶·⁴"],
 ["9-raund (yutishsiz qism)","[0,3]₀","h₀ ← L·h₀ (bitta birlik)","1"],
 ["8-nuqtadagi SBZ","[0,3] bayt","xuddi shunday","≤ 2⁻⁶·⁴"],
 ["1–7-raundlar","[0,3]₀","h₀⁽⁷⁾[0,3] = h₀⁽⁰⁾[0,3]","1"],
 ["0-nuqtadagi SBZ","[0,3] bayt","xuddi shunday","≤ 2⁻⁶·⁴"],
 ["Jami (3 ta qatlam)","—","—","≤ 2⁻¹⁹"]],"A ilova kaliti uchun uch qatlamli chiziqli izning tuzilishi")
P("Izning har bir qatlamida niqob bitta baytda va undagi h tomondagi niqob faqat quyi bitlardan iborat bo‘lishi kerak, aks holda yutishsiz raundlarda yuqori bitlar uchun c < 1 bo‘lgan approksimatsiyalar talab qilinadi. Shuning uchun real iz har qatlamda 2⁻⁶·⁴ dan ham kuchsizroq bo‘ladi. Odatiy kalitlarda esa L niqobni ko‘plab pozitsiyalarga tarqatadi va to‘rtinchi qatlamdayoq 15 tagacha faol bayt paydo bo‘ladi.")
H2('1.5. SBZ ga bog‘liq bo‘lmagan qoldiq munosabatlar')
L5=MR['L5']
P(f"10-raund oxirgi yutishdan keyin bajarilgani uchun xesh qiymatning 0-qatlami L matritsasining obrazida yotadi. L ning o‘rtacha rangi {fz(L2['rank_L']['mean'],1)}, ya’ni chiqishda o‘rtacha ≈{fz(32-L2['rank_L']['mean'],1)} ta c = 1 munosabat bor; kalitlarning {fz(100*L2['zero_rows']['share_keys_with_zero_row'],1)} foizida doimiy bitlar ham paydo bo‘ladi. A ilova kaliti uchun rang {L5['rang']}, ya’ni {len(L5['munosabatlar'])} ta munosabat; ular SBZ-256 bilan hisoblangan 1000 ta tasodifiy xesh qiymatning barchasida bajarildi (masalan, [0,4]₀ ⊕ [1,5]₀ = 0). SBZ bu munosabatlarni yo‘qotmaydi.")
T([700,6354,2300],[["№","Munosabat (xesh qiymatning 0-bitlari)","SBZ-256 da bajarilish ulushi"]]+[[str(i+1)," ⊕ ".join(m)+" = 0",fz(L5['tekshiruv']['sbz'][i],3)] for i,m in enumerate(L5['munosabatlar'])],"A ilova kaliti uchun xesh qiymatdagi c = 1 munosabatlar (SBZ-256, 1000 ta xabar)")
H2('1.6. Chiziqli kriptotahlil bo‘yicha xulosalar')
BL("Yutishsiz raundlar (1–7, 10) 0-qatlamda c = 1 bilan o‘tadi; bu xossa SBZ ga bog‘liq emas.")
BL("SBZ yutish nuqtasidagi maksimal korrelyatsiyani 2⁻⁶ gacha kamaytiradi; faqat holatn orqali o‘tuvchi approksimatsiya mavjud emas. SBZ-128 da Standart-128 dagi «butun xesh bo‘yicha c = 1» zaifligi yo‘qoladi.")
BL("SBZ-256 da 2⁻⁶⁴ chegarasiga mediana kalitlarda 4 ta yutish qatlamidan keyin (≈11-raund), eng yomon kalitlarda 11 ta qatlamdan keyin erishiladi; SBZ-128 da 2⁻³² chegarasiga 4–6 qatlamdan keyin.")
BL("Chiqishdagi c = 1 munosabatlar (o‘rtacha ≈6 ta) va doimiy bitlar Aralash degeneratsiyasidan kelib chiqadi va SBZ bilan saqlanib qoladi.")

# =================== 2. DIFFERENSIAL ===================
PB(); H1('2. Differensial kriptotahlil')
H2('2.1. Usulning mohiyati va bardoshlilik mezoni')
P("Differensial tahlilda kirish ayirmasining Δx = x ⊕ x′ akslantirishlar orqali Δy ga o‘tish ehtimolligi o‘rganiladi:")
F("DDT_F(Δx, Δy) = #{ x : F(x) ⊕ F(x ⊕ Δx) = Δy },     p(Δx → Δy) = DDT_F(Δx, Δy) / 2ⁿ.")
P("Iz ehtimolligi oraliq ehtimolliklar ko‘paytmasiga teng; kolliziyaga bardoshlilik uchun 256 bitli rejimda 2⁻¹²⁸ dan, 128 bitli rejimda 2⁻⁶⁴ dan kichik bo‘lishi kerak. MSB ayirmasi 2ⁿ moduli bo‘yicha amallarda ko‘chirish hosil qilmasligi alohida hisobga olinadi.")
H2('2.2. Akslantirishlarning ayirmalar matritsalari')
H3('2.2.1. AES S-box')
sdd=D1['S_ddt_dist']
P(f"S ning ayirmalar matritsasida Δx ≠ 0 satrlari faqat 0, 2 va 4 qiymatlardan iborat: 0 — {sdd['0']} ta, 2 — {sdd['2']} ta, 4 — {sdd['4']} ta element; maksimal ehtimollik 4/256 = 2⁻⁶ (differensial bir xillik 4). Matritsaning bo‘lagi ⟦sddt⟧-jadvalda.")
db=EX['S_ddt_block']
T([1250]+[1012]*8,[["Δx \\ Δy"]+[f"{y:02X}" for y in range(8)]]+[[f"{d_:02X}"]+[str(v) for v in db[d_-1]] for d_ in range(1,9)],"S ayirmalar matritsasining bo‘lagi",key='sddt')
H3('2.2.2. SBZ')
P("SBZ uchun ayirmalar matritsasi (Δh, Δn) juftligi (65536 ta) va Δy (256 ta) bo‘yicha aniq formula bilan to‘liq hisoblandi:")
F("DDT_SBZ((Δh, Δn), Δy) = Σ_d DDT_S(Δn, d) · DDT_S(Δh ⊕ d, Δy)   (2¹⁶ ta (h, n) juftligi bo‘yicha).")
sxd=SX['SBZ_ddt_taqsimot']
grp=[("0",["0"]),("164–220",[str(v) for v in range(164,221,4)]),("224–252",[str(v) for v in range(224,253,4)]),("256 (2⁻⁸)",["256"]),("260–288",[str(v) for v in range(260,289,4)]),("292–340",[str(v) for v in range(292,341,4)]),("512 (2⁻⁷)",["512"]),("1024 (2⁻⁶)",["1024"])]
T([3354,3000,3000],[["DDT qiymati (×2⁻¹⁶)","Elementlar soni","Izoh"]]+[[g,sp(sum(sxd.get(v,0) for v in vs)),{"0":"o‘tish mumkin emas","256 (2⁻⁸)":"tekis taqsimot qiymati","512 (2⁻⁷)":"faqat Δn = 0","1024 (2⁻⁶)":"faqat Δn = 0"}.get(g,"Δn ≠ 0")] for g,vs in grp],"SBZ ayirmalar matritsasi elementlarining taqsimoti ((Δh, Δn) ≠ (0, 0))",key='sbzddt')
P(f"Natijalar: (1) maksimal ehtimollik 1024/65536 = 2⁻⁶ faqat Δn = 0, Δh ≠ 0 bo‘lganda (510 ta element) erishiladi — bu S ning o‘z ayirmalar matritsasi; (2) Δn ≠ 0 bo‘lganda ehtimolliklar 164/65536 dan 340/65536 gacha (2⁻⁸·⁶ … 2⁻⁷·⁶), ya’ni tekis taqsimotga (2⁻⁸) juda yaqin; (3) Δh = 0, Δn ≠ 0 bo‘lganda ayirma hech qachon so‘nmaydi (so‘nishlar soni {SX['SBZ_sonish_dh0']}); (4) ikkala argumentda ayirma bo‘lganda so‘nish faqat Δh = S(n) ⊕ S(n ⊕ Δn) da mumkin va uning ehtimolligi DDT_S(Δn, Δh)/256 ≤ 2⁻⁶ ({sp(SX['SBZ_sonish_soni'])} ta (Δh, Δn) juftligi uchun). Taqqoslash: Z da maksimal ehtimollik 0,156 (so‘nish bilan), XOR da 1.")
rr=[["Δn","Δh","maks. DDT (×2⁻¹⁶)","eng ehtimolli Δy","so‘nish (Δy = 0)"]]
for dn,dh,mx,am,v in S2['sbz_ddt_kichik']: rr.append([f"{dn:02X}",f"{dh:02X}",str(mx),f"{am:02X}",str(v)])
T([1500,1500,2300,2054,2000],rr,"SBZ ayirmalar matritsasidan namunalar (Δn ∈ {01, 80}, Δh = 00…07)")
P("Jadvaldan ko‘rinadiki, Δn ≠ 0 bo‘lganda eng ehtimolli chiqish ayirmasi odatda 296–312/65536 ≈ 2⁻⁷·⁷ ehtimollikka ega; 512/65536 = 2⁻⁷ qiymatlar faqat Δh = S(n) ⊕ S(n ⊕ Δn) bo‘ladigan juftliklarda va faqat Δy = 0 (so‘nish) uchun uchraydi. Masalan, (Δn, Δh) = (01, 00) da so‘nish mumkin emas, (01, 01) da esa 2⁻⁷ ehtimollik bilan.")
P(f"A ilova misoli: h = bf, n = 6e, n′ = n ⊕ 80. Standart Z uchun ayirma faqat quyi yarim baytda (06), SBZ uchun butun baytda (3f).")
H3('2.2.3. Qo‘sh, Aralash, SurHolat, SurKalit, TuzilmaKalit')
pj=D1['Qosh_pj_best_mean']
P(f"Raund akslantirishlari standartdagidek. Qo‘sh elementining eng ehtimolli o‘tishi 80 → 80 ({D1['Qosh_ddt_max_max']}/256): toq y uchun (y + 2ⁿ⁻¹)⁻¹ ≡ y⁻¹ + 2ⁿ⁻¹, R juft. 2ʲ ko‘rinishidagi ayirmalar uchun eng ehtimolli o‘tish ehtimolliklari ⟦qddt⟧-jadvalda. Aralash MSB ayirmalarini M(k₀) orqali ehtimollik 1 bilan tarqatadi, M(k₀) yadrosidagi ayirmalar so‘nadi (kalitlarning {fz(100*A3['keys_zero_col'],0)} foizida nol ustun bor); SurHolat, SurKalit ayirmani ko‘chiradi, TuzilmaKalit faqat kₑ ga ta’sir qiladi.")
T([3100]+[780]*8,[["Kirish ayirmasi Δx = 2ʲ, j","0","1","2","3","4","5","6","7"],["Eng ehtimolli Δy ehtimolligi"]+[fz(v,3) for v in pj]],"Qo‘sh elementining ayirmalar o‘tkazish ehtimolliklari",key='qddt')
H2('2.3. Orttirmalarning akslantirishlar va raundlar orqali o‘tishi')
P("Birinchi tajribada (D0) 0-nuqtadagi yutishdan keyingi holatning bitta baytiga MSB ayirmasi kiritildi (3000 juftlik). 1- va 2-raund akslantirishlari bo‘yicha natija ⟦d0op⟧-jadvalda, raundlar bo‘yicha — ⟦d0r⟧-jadvalda.")
def opsRow(key,j,lab):
    rs=[r for r in D3[key] if r['j']==j]; return [lab]+[f"{fz(r['act'],1)} / {fz(r['actk'],1)}; {fz(r['msb'],2)}" for r in rs]
rr=[["Rejim, raund","Aralash","Qo‘sh(holat, kₑ)","SurHolat, SurKalit","Qo‘sh(holat, kₑ)","TuzilmaKalit"]]
for key,lab in [('256_sbz_D0a','SBZ-256'),('16_sbz_D0a','SBZ-128')]:
    for j in (1,2): rr.append(opsRow(key,j,f"{lab}, j = {j}"))
T([1750,1520,1520,1520,1520,1520],rr,"Akslantirishlardan keyingi faol elementlar (holat / kₑ) va MSB izining saqlanish ehtimolligi",key='d0op')
def r0(key,f): return [ (fz(r[f],3) if f=='msb' else fz(r[f],1)) for r in D3[key] if r['op']=='Tuz']
T([2850]+[650]*10,[["Raund j"]+[str(j) for j in range(1,11)],["SBZ-256: P(MSB izi)"]+r0('256_sbz_D0a','msb'),["SBZ-256: faol baytlar"]+r0('256_sbz_D0a','act'),["SBZ-128: P(MSB izi)"]+r0('16_sbz_D0a','msb'),["SBZ-128: faol el."]+r0('16_sbz_D0a','act')],"Bitta MSB ayirmasining raundlar orqali o‘tishi (8- va 9-raundlarda SBZ)",key='d0r')
IMG('ch2.png',15.5,6.9,"MSB izining saqlanish ehtimolligi va faol elementlar soni (SBZ varianti)")
rows=[["Raund, akslantirish","Δholat","Faol (holat / kₑ)","Faqat MSB"]]
for q in MR['D1']['qadam']:
    if q['amal'] in ('Aralash','Qosh1','Qosh2'): rows.append([f"{q['raund']}: {opn[q['amal']]}",nl(q['dh']),f"{q['faol']} / {q['faol_ke']}","ha" if q['msb'] else "yo‘q"])
T([2700,3300,1800,1554],rows,"SBZ-256, A ilova ma’lumotlari: holat[0,0] dagi MSB ayirmasining 1–2-raundlarda o‘tishi",mono=(1,))
P("Yutishsiz raundlarda MSB izi standartdagidek har raundda ≈0,85–0,94 ehtimollik bilan saqlanadi (7 raunddan keyin ≈0,34). 8-raunddagi SBZ izni to‘liq buzadi: qolgan ≈3,3% — 1-raundda Aralash yadrosi orqali ayirmasi butunlay so‘ngan juftliklar.")
rr=[["Rejim (8-raund)","Aralash","Qo‘sh(holat, kₑ)","SurHolat, SurKalit","Qo‘sh(holat, blok)","SBZ (8-nuqta)","TuzilmaKalit"]]
for key,lab in [('256_sbz_D0a','SBZ-256'),('16_sbz_D0a','SBZ-128')]:
    rs=[r for r in D3[key] if r['j']==8]; rr.append([lab]+[f"{fz(r['act'],1)}; {fz(r['msb'],3)}" for r in rs])
T([1600,1250,1300,1300,1300,1300,1304],rr,"8-raund akslantirishlari bo‘yicha faol elementlar va MSB izining saqlanish ehtimolligi")
P("8-raundda SBZ dan oldin MSB izi hali 0,33 (256 bitli rejim) ehtimollik bilan saqlanadi; SBZ dan keyin u 0,033 ga tushadi (ya’ni faqat ayirmasi to‘liq so‘ngan juftliklar qoladi), faol baytlar soni esa ≈27 ga oshadi: SBZ har bir faol baytdagi MSB ayirmasini to‘liq baytga yoyadi.")
H3('2.3.1. Kirish blokidagi ayirmalar')
def d2(key,op,j=None):
    for r in D2[key]:
        if r['op']==op and (j is None or r['j']==j): return r
rr=[["Tajriba, rejim","Qo‘sh(0): faol / p","SBZ(0): faol / p","1-raund","2-raund","7-raund","8-nuqta","9-nuqta","10-raund: Xemming"]]
for case in ('D2','D1'):
    for key,lab in [('256_sbz','SBZ-256'),('16_sbz','SBZ-128')]:
        k_=f'{key}_{case}'; q=d2(k_,'Qosh0'); b=d2(k_,'BZ0')
        rr.append([f"{case}, {lab}",f"{fz(q['act'],1)} / {fz(q['top'],2)}",f"{fz(b['act'],1)} / {fz(b['top'],4)}",fz(d2(k_,'Tuz',1)['act'],1),fz(d2(k_,'Tuz',2)['act'],1),fz(d2(k_,'Tuz',7)['act'],1),fz(d2(k_,'BZ8')['act'],1),fz(d2(k_,'BZ9')['act'],1),fz(d2(k_,'Tuz',10)['hd'],1)])
T([1350,1150,1200,800,800,800,850,850,1550],rr,"Kirish bloki (D2) va holatdagi (D1) ayirmalarning tarqalishi",key='d2')
P("D2 tajribasida (blokning ikki elementida MSB ayirmasi) Qo‘sh(0-nuqta) holatga ta’sir qilmaydi (p = 1), SBZ esa ayirmani ikkita bayt bo‘yicha butun baytlarga tarqatadi; eng ehtimolli natija ehtimolligi har bir bayt uchun ≤ 2⁻⁷·⁸, ikki bayt uchun ≈2⁻¹⁵·⁶ (o‘lchangan qiymat tanlanmaning sezgirlik chegarasida). D1 tajribasida SBZ yutishdan keyin Xemming masofasini 99 bitga (256 bitli rejim) va 62 bitga (128 bitli rejim) yetkazadi; standart algoritmda bu qiymatlar 71 va 31 edi. SBZ-128 da 10-raunddan keyingi Xemming masofasi 64 ga yaqin, Standart-128 da 47 edi.")
H2('2.4. Optimal orttirmalar')
BL("*Yutishsiz raundlardagi MSB izlari* — har raundda ≈0,85–0,94 (256 bitli rejim); 7 raund uchun ≈2⁻¹·⁶.")
BL("*SBZ dan o‘tish* — eng yaxshi holat Δn = 0, Δh ≠ 0 da 2⁻⁶ (holatdagi ayirma S orqali o‘tadi); Δn ≠ 0 da ≤ 2⁻⁷·⁶. Holatdagi ayirma (Δn = 0) yoki faqat blokdagi ayirma (Δh = 0) SBZ da so‘nmaydi; so‘nish faqat Δh = S(n) ⊕ S(n ⊕ Δn) da, ≤ 2⁻⁶ ehtimollik bilan.")
BL("*Aralash yadrosi* — MSB ayirmasi M(k₀) yadrosida bo‘lsa, ehtimollik 1 bilan so‘nadi (≈3% juftliklar). SBZ chiqishida aynan 80 ayirmasini olish ehtimolligi bir bayt uchun ≈2⁻⁷·⁹.")
P("*Kolliziya izining tuzilishi.* Blok ayirmasi 0-, 8-, 9-nuqtalarda uch marta holatga kiradi. Kolliziya uchun 8-nuqtaga kelganda holat ayirmasi faqat blokning faol pozitsiyalarida bo‘lishi va u yerda Δh = S(n) ⊕ S(n ⊕ Δn) tengligi bajarilishi kerak; Δn = 0 bo‘lgan barcha baytlarda holat ayirmasi nol bo‘lishi shart, chunki SBZ ularni so‘ndira olmaydi. Tajribada SBZ-256 da ikki baytli MSB ayirmasi bilan boshlangan 2000 juftlikning birortasida ham 7-raunddan keyin faol baytlar soni 29 dan kam bo‘lmadi. Standart-256 da holat ayirmasi Z(h) da Δn ga bog‘liq bo‘lmagan holda so‘nishi mumkin edi; SBZ bu yo‘lni yopadi.")
D3m=MR['D3']
rr=[["Rejim","Qo‘sh(0): faol","Yutishdan keyingi Δholat","1-raund","8-nuqtada","9-nuqtada","Chegara 8 / 8+9"]]
for k_,lab in [('256_sbz','SBZ-256'),('16_sbz','SBZ-128')]:
    v=D3m[k_]; rr.append([lab,str(v['faol_q0']),nl(v['dbz0']),str(v['r1']),str(v['a8']),str(v['a9']),f"2^{v['chegara8']:.0f} / 2^{v['chegara89']:.0f}"])
T([1400,1200,2600,900,1000,1000,1254],rr,"A ilova misoli: blokdagi ikki elementli MSB ayirmasining yutish nuqtalarigacha o‘tishi",mono=(2,))
P("128 bitli rejimda yuqori bit-qatlamdagi o‘zgarishlarning chiqish quyi qatlamlariga ta’siri ham tekshirildi (⟦tf⟧-jadval). Standart-128 da 0-qatlam doim saqlanardi (ehtimollik 1), SBZ-128 da esa u hech qachon saqlanmaydi.")
tf=I['tfunksiya_128']
T([2800]+[1310]*5,[["O‘zgartirilgan bitlar soni w","1","2","4","8","32"],["0-qatlam saqlandi"]+[fz(tf[w]['0_qatlam_saqlandi'],3) for w in ('1','2','4','8','32')],["Yarim baytlarning quyi 3 biti saqlandi (ulush)"]+[fz(tf[w]['quyi_qatlam_bitlari_saqlandi'],3) for w in ('1','2','4','8','32')]],"SBZ-128: yuqori bit-qatlam o‘zgarganda chiqish quyi qatlamlarining saqlanishi (2000 juftlik)",key='tf')
P("Quyi 3 bitning saqlanish ulushi ≈0,14 ga teng, bu tasodifiy funksiya uchun kutilgan 1/8 = 0,125 ga yaqin: SBZ-128 da chiqish bitlari bit-qatlamlar bo‘yicha ajralmaydi va Standart-128 dagi 2⁴⁸ murakkablikdagi kolliziya hujumi uchun asos yo‘qoladi.")
H2('2.5. Bardoshlilik bahosi')
T([1900,1800,2000,2000,1654],[["Rejim","Faol bayt boshiga maks. p","8-nuqtadan keyin (≈27 bayt)","8- va 9-nuqtalardan keyin","Talab"],["SBZ-256","2⁻⁶","≤ 2⁻¹⁶²","≤ 2⁻³⁴⁸","2⁻¹²⁸"],["SBZ-128","2⁻⁶ (15 bayt)","≤ 2⁻⁹⁰","≤ 2⁻¹⁸⁰","2⁻⁶⁴"],["Standart-256 (taqqoslash)","2⁻²·⁶⁸","≤ 2⁻⁷²","≤ 2⁻¹⁵⁶","2⁻¹²⁸"]],"Birinchi iteratsiyadagi differensial iz ehtimolligining yuqori chegaralari")
P("Chegaralar har bir faol bayt uchun eng yaxshi ehtimollikni olish orqali hisoblangan (yuqori chegara). SBZ-256 va SBZ-128 birinchi iteratsiyaning 8-raundidagi yutishdayoq talab qilingan chegaradan o‘tadi; standart algoritmda buning uchun 9-raund kerak edi (256 bitli rejim) yoki umuman erishilmas edi (128 bitli rejim).")
H2('2.6. Differensial kriptotahlil bo‘yicha xulosalar')
BL("Yutishsiz raundlar MSB izlarini ≈0,85–0,94 ehtimollik bilan o‘tkazadi; bu xossa SBZ ga bog‘liq emas.")
BL("SBZ ning maksimal o‘tish ehtimolligi 2⁻⁶ (faqat Δn = 0 da), Δn ≠ 0 da ≤ 2⁻⁷·⁶; bitta argumentdagi ayirma so‘nmaydi, ikki argumentdagi ayirmaning so‘nishi ≤ 2⁻⁶.")
BL("SBZ-256 va SBZ-128 birinchi iteratsiyaning 8-raundidan keyin differensial chegaraga erishadi; SBZ-128 da bit-qatlamlar bo‘yicha ajralish yo‘qoladi.")
BL("Aralash yadrosi orqali so‘nish (≈3% juftlik) SBZ ga bog‘liq bo‘lmagan qoldiq xavf.")

# =================== 3. ALGEBRAIK ===================
PB(); H1('3. Algebraik kriptotahlil')
H2('3.1. Usulning mohiyati va bardoshlilik mezoni')
P("Algoritm noma’lum bitlarga nisbatan tenglamalar tizimi ko‘rinishida yoziladi. Linearizatsiya murakkabligi C(n, d) ≈ (Σ_{i≤d} binom(n, i))^2,8; 128 bitli rejim uchun d ≥ 4, 256 bitli rejim uchun d ≥ 8 talab qilinadi. Implitsit tenglamalar soni monomlar matritsasining rangi orqali aniq hisoblandi.")
H2('3.2. Akslantirishlar uchun algebraik tenglamalar')
H3('3.2.1. AES S-box va SBZ')
P(f"S GF(2⁸) da x·y = 1 (x ≠ 0) tenglamasi bilan ifodalanadi; bit darajasida 16 ta o‘zgaruvchiga nisbatan {A1['S_quad'][0]} ta chiziqli bog‘liq bo‘lmagan kvadrat implitsit tenglama mavjud (137 ta monomdan), har bir chiqish biti darajasi {A1['S_deg'][0]}. SBZ uchun oraliq o‘zgaruvchilar kiritiladi:")
F("u = S(n),     v = h ⊕ u,     y = S(v),")
P(f"natijada har bir bayt uchun 16 ta yangi o‘zgaruvchi (u, y), 8 ta chiziqli va 2 × 39 = 78 ta kvadrat tenglama hosil bo‘ladi. Oraliq o‘zgaruvchilarsiz SBZ 24 ta o‘zgaruvchiga nisbatan birorta ham kvadrat implitsit tenglamaga ega emas ({A1['SBZ_quad'][0]} / {A1['SBZ_quad'][1]}), har bir chiqish bitining ANF darajasi 16 ta kirish bitiga nisbatan {A1['SBZ_deg'][0]}. 128 bitli rejimda 16 ta juftlangan bayt uchun xuddi shunday tenglamalar yoziladi (256 o‘zgaruvchi, 1248 tenglama).")
P("S ning 39 ta kvadrat tenglamasi x·y = 1 munosabatidan kelib chiqadi: GF(2⁸) da x·y = 1, x²·y = x, x·y² = y tengliklari bit darajasida bichiziqli va kvadrat tenglamalarni beradi (23 ta bi-affin va 16 ta to‘liq kvadrat tenglama). Bu tenglamalar x = 0 da ham bajariladigan ko‘rinishda tanlanadi (AES S-box da 0 → 0 + 63 affin siljish). Shunday qilib, bitta SBZ bayti uchun algebraik tizim: 8 ta o‘zgaruvchi u, 8 ta y, u bilan n orasida 39 ta, y bilan v = h ⊕ u orasida 39 ta kvadrat tenglama.")
P("128 bitli rejimda juftlash va ajratish chiziqli: H ning bitlari h[2j] va h[2j+1] bitlarining birlashmasi, Q ning yuqori va quyi 4 biti mos ravishda h[2j] va h[2j+1] ga yoziladi; bu qadamlar yangi tenglama talab qilmaydi.")
sa=S3['sbz_anf']
T([1500,1500]+[580]*11,[["SBZ biti","Monomlar"]+[f"d={d_}" for d_ in range(3,14)]]+[[f"y{j}",sp(a['jami'])]+[sp(v) for v in a['daraja_boyicha'][3:14]] for j,a in enumerate(sa)],"SBZ oshkor tenglamalarining (ANF) tarkibi: 16 kirish bitiga nisbatan darajalar bo‘yicha monomlar soni")
P("Har bir SBZ chiqish bitining ANF ida 27–31 mingta monom bor (mumkin bo‘lgan 65536 tadan qariyb yarmi), ularning asosiy qismi 6–10-darajali, eng yuqori daraja 13. Bunday zich va yuqori darajali oshkor tenglamalarni bevosita ishlatish amaliy emas, shuning uchun algebraik tizimda oraliq o‘zgaruvchilar bilan 78 ta kvadrat tenglama ishlatiladi; lekin oraliq o‘zgaruvchilar kiritilishi har bir SBZ bayti uchun 16 ta yangi noma’lumni anglatadi.")
H3('3.2.2. Raund akslantirishlari')
qd=EX['Qosh_deg_median']
P("Qo‘sh uchun halqa tenglamalari (t = 1, 2, 3):")
F("x⁽ᵗ⁾ · (B_t + R · x⁽ᵗ⁻¹⁾) + A_t · x⁽ᵗ⁻¹⁾ ≡ 0 (mod 2ⁿ),   A₁ = J₁′ + 2·x′ + Δ,   B₁ = K₁ − 2·x,   J₁ = Σ x,   K₁ = Π (x | 1) + Δ′.")
P(f"A ilova ma’lumotlarida holat[0,0] uchun bu tenglamalar tekshirildi: uchala bosqichda chap tomon aynan 0. Bitta element (parametrlar belgilangan) 16 ta o‘zgaruvchiga nisbatan {A1['Qosh_quad'][0]} ta kvadrat implitsit tenglamaga ega, chiqish bitlari darajalari (mediana) {', '.join(str(int(v)) for v in qd)}. Aralash uchun bichiziqli tenglamalar (h′[u,u] = h[u,u]·Σᵢ kₑ[i,u] − Σ_{{i≠u}} h[i,i]·kₑ[i,u] va h.k.), 0-qatlamda chiziqli. SurHolat, SurKalit — o‘zgaruvchilarni qayta nomlash; TuzilmaKalit: kₑ′ = kₑ − (kₑ₀ ⊕ k₀).")
T([3200,3077,3077],[["Akslantirish","0-qatlam darajasi","j-bit darajasi"],["SBZ (yutish)","13 (16 kirish bitiga nisbatan)","13"],["Aralash (kₑ ma’lum / noma’lum)","1 / 2","≤ j + 1 / ≤ 2(j + 1)"],["Qo‘sh","1","≈ j (mediana)"],["SurHolat, SurKalit","1","1"],["TuzilmaKalit","1","≤ j + 1"]],"Akslantirishlar bo‘yicha algebraik darajalar (SBZ varianti)")
a2=MR['A2']; x_=a2['x']
T([1100,3100,3500,1654],[["Bosqich","O‘zgaruvchilar","Tenglama","Qiymat (mod 256)"],["1",f"x = {x_[0]:#04x}, x⁻¹ = {x_[1]:#04x}","x⁻¹·(B₁ + R·x) + A₁·x ≡ 0",str(a2['tekshiruv'][0])],["2",f"x⁻¹ = {x_[1]:#04x}, x⁻² = {x_[2]:#04x}","x⁻²·(B₂ + R·x⁻¹) + A₂·x⁻¹ ≡ 0",str(a2['tekshiruv'][1])],["3",f"x⁻² = {x_[2]:#04x}, x⁻³ = {x_[3]:#04x}","x⁻³·(B₂ + R·x⁻²) + A₂·x⁻² ≡ 0",str(a2['tekshiruv'][2])]],f"Qo‘sh halqa tenglamalarining A ilova ma’lumotlarida tekshiruvi (J₁h = {a2['J1h']}, J₁hn = {a2['J1hn']}, K₁h = {a2['K1h']}, A₁ = {a2['A1']}, B₁ = {a2['B1']})")
H3('3.2.3. Bit darajasidagi tenglamalar soni')
E=A3['eq']; e2=E['256_sbz']; e1=E['128_sbz']
rr=[["Akslantirish","256: o‘zg. / tengl. / nochiziqli","128: o‘zg. / tengl. / nochiziqli"]]
for lab,k_ in [("Qo‘sh (ikki massiv, 3 bosqich)",'qosh'),("Aralash",'aralash'),("TuzilmaKalit",'tuzilma'),("SBZ (yutish qatlami)",'bz'),("Raund (yutishsiz)",'raund')]:
    rr.append([lab," / ".join(sp(v) for v in e2[k_])," / ".join(sp(v) for v in e1[k_])])
T([3200,3077,3077],rr,"SBZ variantida akslantirishlar uchun bit darajasidagi tenglamalar soni (baho)")
P("SBZ qatlami 256 bitli rejimda 512 ta o‘zgaruvchi va 2496 ta kvadrat tenglama qo‘shadi — bu raund tizimining 0,2 foizi; tizim hajmini Qo‘sh belgilaydi (≈91%), lekin SBZ unga yagona 13-darajali bog‘lanishni qo‘shadi.")
H2('3.3. Raund tenglamalari va 2–3 raund uchun tizimlar')
F("a = Aralash(h⁽ʲ⁻¹⁾, kₑ⁽ʲ⁻¹⁾);  (b, c) = Qo‘sh(a, kₑ⁽ʲ⁻¹⁾);  b′ = P·b, c′ = Q·c;  (h⁽ʲ⁾, d) = Qo‘sh(b′, c′);  kₑ⁽ʲ⁾ = TuzilmaKalit(d, k).")
P("8- va 9-raundlarda yutish tenglamalari qo‘shiladi: (h̃, ñ) = Qo‘sh(h, blok), u = S(ñ), v = h̃ ⊕ u, h = S(v). 2 va 3 raund uchun tizimlar raund tenglamalarini zanjirlash bilan olinadi (⟦eqsys⟧-jadval).")
rr=[["Rejim","1 raund: o‘zg. / tengl.","2 raund: o‘zg. / tengl.","3 raund: o‘zg. / tengl."]]
for key,lab in [('256_sbz','SBZ-256'),('128_sbz','SBZ-128')]: rr.append([lab]+[f"{sp(E[key][r][0])} / {sp(E[key][r][1])}" for r in ('r1','r2','r3')])
T([2050,2450,2450,2400],rr,"1, 2 va 3 raund uchun bit darajasidagi tenglamalar tizimlari hajmi",key='eqsys')
rr=[["Tizim qismi (SBZ-256, 2 raund)","O‘zgaruvchilar","Tenglamalar"]]
rr.append(["0-nuqta: Qo‘sh(holat, blok)",sp(e2['qosh'][0]),sp(e2['qosh'][1])]); rr.append(["0-nuqta: SBZ",sp(e2['bz'][0]),sp(e2['bz'][1])])
for j in (1,2):
    rr.append([f"{j}-raund: Aralash",sp(e2['aralash'][0]),sp(e2['aralash'][1])]); rr.append([f"{j}-raund: 2 × Qo‘sh",sp(2*e2['qosh'][0]),sp(2*e2['qosh'][1])]); rr.append([f"{j}-raund: TuzilmaKalit",sp(e2['tuzilma'][0]),sp(e2['tuzilma'][1])])
rr.append(["Jami",sp(e2['r2'][0]),sp(e2['r2'][1])])
T([4554,2400,2400],rr,"SBZ-256 uchun 2 raundli tenglamalar tizimining tarkibi")
P("Yutishsiz raundlarda 0-qatlam tenglamalari chiziqli bo‘lib qoladi (h₀⁽ʲ⁾ = L·h₀⁽ʲ⁻¹⁾), lekin har bir yutish nuqtasida 0-qatlam 13-darajali SBZ orqali o‘tadi. Shuning uchun Standart-128 dagi «barcha raundlar uchun chiziqli 0-qatlam tizimi» SBZ-128 da mavjud emas.")
H3('3.3.1. Bitta raund tizimidagi noma’lumlar guruhlari')
T([3900,2700,2754],[["Noma’lumlar guruhi","256 bitli rejim (bit)","128 bitli rejim (bit)"],["Raund kirishidagi holat va kₑ","256 + 256","128 + 128"],["Aralash chiqishi va ko‘paytmalar",sp(e2["aralash"][0]),sp(e1["aralash"][0])],["Qo‘sh: J, K zanjirlari, A, B, x⁻¹, x⁻², x⁻³ (2 ta Qo‘sh)",sp(2*e2["qosh"][0]),sp(2*e1["qosh"][0])],["TuzilmaKalit",sp(e2["tuzilma"][0]),sp(e1["tuzilma"][0])],["Yutish nuqtasi (SBZ, 8- va 9-raundlarda)",sp(e2["bz"][0])+" (u, y)",sp(e1["bz"][0])+" (u, y)"]],"SBZ variantida bitta raund tizimidagi noma’lumlar guruhlari (baho)")
P("Noma’lumlarning qariyb hammasi Qo‘sh o‘zgartirishining oraliq qiymatlaridir. Ularning ko‘pchiligi ko‘chirish bitlari va qisman ko‘paytmalar bo‘lib, kvadrat tenglamalar orqali bog‘langan. Buzg‘unchi uchun asosiy qiyinchilik — yutish nuqtasidagi 13-darajali bog‘lanish: bu nuqtada 0-qatlam tenglamalari chiziqlilikni yo‘qotadi.")
T([2800,2200,2200,2154],[["Qadam","0-qatlam darajasi (yuqori chegara)","Kub testida kuzatilgan","Izoh"],["0-nuqtadagi SBZ dan keyin","13 (bayt bo‘yicha)","SBZ-256: d = 12 da 0,30 nol ulushi","har bir bayt 16 bitga bog‘liq"],["1–7-raundlar","o‘zgarmaydi (L chiziqli)","SBZ-128: d = 12 da 0,75–0,78","0-qatlam yutish chiqishining chiziqli funksiyasi"],["Yuqori bit-qatlamlar, r ≥ 1","tez o‘sadi","SBZ-256: tasodifiy daraja (0,06–0,14)","Qo‘sh dagi J, K bog‘lanishi"],["8-, 9-nuqtalardagi SBZ","13 × (oldingi daraja), noma’lumlar soni bilan cheklangan","—","kompozitsiya"]],"SBZ variantida algebraik darajaning raundlar bo‘yicha o‘zgarishi")
H2('3.4. Raundlar bo‘yicha algebraik darajaning o‘sishi')
P("Kub testlari: xabarning dastlabki 16 bitidan d ta bit tanlanadi, 2ᵈ qiymat bo‘yicha r raunddan keyingi holat bitlari yig‘indisi hisoblanadi; 4 ta kub uchun yig‘indisi doim nol bo‘lgan bitlar ulushi o‘lchandi (yuqori darajali funksiya uchun ≈0,06).")
def cr(key,lay=None):
    row=A2[key]; return [fz((row[str(d_)][1][lay] if lay is not None else row[str(d_)][0]),2) for d_ in (2,4,6,8,10,12)]
rr=[["Rejim, raund r","d = 2","d = 4","d = 6","d = 8","d = 10","d = 12"]]
for r in (0,1,2,3): rr.append([f"SBZ-256, r = {r}"]+cr(f'256_sbz_r{r}'))
for r in (0,1,2,3): rr.append([f"SBZ-128, r = {r} (0-qatlam)"]+cr(f'16_sbz_r{r}',0))
for r in (1,3): rr.append([f"SBZ-128, r = {r} (barcha bitlar)"]+cr(f'16_sbz_r{r}'))
T([3150,1030,1030,1030,1030,1030,1030],rr,"Kub testlari: yig‘indisi doim nol bo‘lgan chiqish bitlari ulushi")
lay1=A2['256_sbz_r1']
rr=[["Bit-qatlam j (SBZ-256, r = 1)"]+[str(j) for j in range(8)]]
for d_ in (4,8,12): rr.append([f"d = {d_}"]+[fz(v,2) for v in lay1[str(d_)][1]])
T([3354]+[750]*8,rr,"SBZ-256, 1 raunddan keyin: bit-qatlamlar bo‘yicha nol yig‘indilar ulushi")
P("SBZ-256 da r = 0 da ham (faqat 0-nuqtadagi yutish) d = 12 da ulush 0,30 (Standart-256 da 0,84), r ≥ 1 da tasodifiy funksiya darajasida (0,06–0,14). SBZ-128 da 0-qatlam ulushi d ortishi bilan ko‘tariladi (r = 1–3 da d = 12 uchun 0,75–0,78), ya’ni bu qatlam darajasi 12 atrofida chegaralangan: 1–3-raundlarda u yutish chiqishlarining chiziqli funksiyasi, har bir yutish bayti esa ko‘pi bilan 13-darajali. Bu 128 bitli rejim uchun talab qilinadigan darajadan (4) ancha yuqori. Standart-128 da esa 0-qatlam barcha d uchun 1,00 edi.")
lay16=A2['16_sbz_r1']
rr=[["Bit-qatlam j (SBZ-128, r = 1)"]+[str(j) for j in range(4)]]
for d_ in (4,8,12): rr.append([f"d = {d_}"]+[fz(v,2) for v in lay16[str(d_)][1]])
T([4554,1200,1200,1200,1200],rr,"SBZ-128, 1 raunddan keyin: bit-qatlamlar bo‘yicha nol yig‘indilar ulushi")
P("*Taxmin qilish va aniqlash strategiyasi.* Buzg‘unchi kalitning 0-qatlamini (2³⁰ variant) taxmin qilsa, 1–7-raundlarning 0-qatlam tenglamalari chiziqli bo‘ladi, lekin har bir yutish nuqtasida 0-bit 13-darajali SBZ chiqishi bo‘lib qoladi va chiziqli tizim keyingi yutishdan o‘tolmaydi. Standart-128 dagidan farqli o‘laroq, kalit 0-qatlamini tekshirish uchun buzg‘unchida chiziqli tekshiruv tenglamalari yo‘q.")
H2('3.5. Hujum namoyishi: linearizatsiya')
P("Kalitli rejimda 0-qatlamning affin modeli (o₀ = A·m₀ ⊕ c) 80 ta xabar bo‘yicha qurildi va 300 ta yangi xabarda tekshirildi.")
T([3000,3200,3154],[["Rejim","32 bitning hammasi to‘g‘ri","Bitlar bo‘yicha to‘g‘ri"],["SBZ-128",fz(A3['16_sbz']['full_vec'],3),fz(A3['16_sbz']['per_bit'],3)],["SBZ-256",fz(A3['256_sbz']['full_vec'],3),fz(A3['256_sbz']['per_bit'],3)],["Standart-128 (taqqoslash)",fz(A3['16_std']['full_vec'],3),fz(A3['16_std']['per_bit'],3)]],"Chiqish 0-qatlamining affin modelini qurish natijasi")
rr=[["SBZ-128: sinov xabari","Haqiqiy 0-qatlam","Bashorat"]]
for m_,a_,p_ in MR['A3']['sbz']['misollar']: rr.append([m_,a_,p_])
T([3154,3100,3100],rr,"SBZ-128: sinov xabarlari uchun bashorat misollari",mono=(0,1,2))
P(f"SBZ variantlarida affin model ishlamaydi: 32 bitning hammasi hech bir xabarda to‘g‘ri chiqmadi, bitlar bo‘yicha aniqlik 0,5 ga yaqin (SBZ-128 da {fz(A3['16_sbz']['per_bit'],3)}; 0,5 dan biroz yuqori qiymat chiqishdagi doimiy munosabatlar hisobiga). Standart-128 dagi 80 so‘rovli hujum va kalit 0-qatlamini alohida tiklash (2³⁰) SBZ-128 da qo‘llanilmaydi.")
H2('3.6. Bardoshlilik bahosi')
LC=A3['lin_cost']
T([2600,1350,1350,1350,1350,1354],[["Noma’lum bitlar soni n","d = 1","d = 6","d = 7","d = 8","d = 13"],["128 (128 bitli rejim)"]+[f"2^{fz(LC[f'128_{d_}'],1)}" for d_ in (1,6,7,8,13)],["256 (256 bitli rejim)"]+[f"2^{fz(LC[f'256_{d_}'],1)}" for d_ in (1,6,7,8,13)]],"Linearizatsiya mehnatining tenglamalar darajasiga bog‘liqligi (raqamli qiymatlar)")
P("SBZ ning 13-darajasi bilan linearizatsiya mehnati 128 bitli rejimda 2¹⁶¹·⁶, 256 bitli rejimda 2¹⁹⁹·¹ ni tashkil qiladi, bu talab qilingan 2⁶⁴ va 2¹²⁸ dan ancha katta. Gröbner bazislari yoki XL usullari tizim siyrakligidan foydalanishi mumkin, lekin har bir yutish nuqtasida 512 (256 bitli rejim) yoki 256 (128 bitli rejim) ta yangi noma’lum va 13-darajali bog‘lanish paydo bo‘lishi bu usullarning ham murakkabligini keskin oshiradi.")
IMG('ch3.png',15.5,7.3,"Linearizatsiya mehnatining tenglamalar darajasiga bog‘liqligi")
LC=A3['lin_cost']
T([2600,2000,2000,2754],[["Rejim","Yutishdagi daraja","Talab qilinadigan","Bardoshlilikka erishiladigan raund"],["SBZ-128","13","≥ 4 (2^65,5)","0-nuqtadagi yutishdan keyin"],["SBZ-256","13","≥ 8 (2^136)","0-nuqtadagi yutishdan keyin"]],"Algebraik bardoshlilik bahosi")
H2('3.7. Algebraik kriptotahlil bo‘yicha xulosalar')
BL("Yutish nuqtasidagi SBZ algoritmning yagona yuqori darajali elementi (daraja 13, kvadrat implitsit tenglamalar yo‘q); raund akslantirishlari T-funksiya, 0-qatlami chiziqli.")
BL("Tenglamalar tizimining hajmini Qo‘sh belgilaydi; SBZ tizimni amalda kattalashtirmaydi (0,2%), lekin darajasini oshiradi.")
BL("SBZ-128 da 0-qatlam linearizatsiya hujumi ishlamaydi (aniqlik ≈0,5); Standart-128 dagi algebraik zaiflik yo‘qoladi.")
BL("Ikkala SBZ varianti algebraik bardoshlilik chegarasiga 0-nuqtadagi yutishdan keyinoq erishadi.")

# =================== 4. INTEGRAL ===================
PB(); H1('4. Integral (square) kriptotahlil')
H2('4.1. Usulning mohiyati')
P("Integral tahlilda tanlangan kirishlar to‘plami (masalan, bitta bayt barcha qiymatlarni qabul qiladi — A, qolganlari doimiy — C) akslantirishlardan o‘tganda har bir pozitsiyada qanday xossa saqlanishi kuzatiladi: A, C, B (XOR yig‘indisi nol) yoki U. Agar r raunddan keyin biror bit ehtimollik 1 bilan balanslangan bo‘lsa, bu r raund uchun integral farqlovchi.")
H2('4.2. Akslantirishlarning tanlangan to‘plamlarga ta’siri')
mk=I['komponentlar']
P(f"*SBZ.* n bo‘yicha ham, h bo‘yicha ham o‘rin almashtirish, shuning uchun faqat bitta argument faol bo‘lsa, faol to‘plam A ga o‘tadi: n faol, h = 3c — {mk['SBZ_n_faol_turli']} xil qiymat; h faol, n = 5a — {mk['SBZ_h_faol_turli']} xil qiymat. Ikkala argument bir xil faol qiymat bilan o‘zgarsa (h = n = x), natija {mk['SBZ_ikkalasi_faol_turli']} xil qiymatdan iborat va XOR yig‘indisi {mk['SBZ_ikkalasi_xor']:02x} — U. Taqqoslash: standart Z faol to‘plamni B ga (har bir yarim bayt qiymati 16 marta), XOR esa A ga o‘tkazadi.")
im=S2['ikkalasi_mustaqil']
T([3600,1900,1900,1954],[["SBZ kirish to‘plami","Turli qiymatlar","Har bir qiymat soni","XOR yig‘indi / xossa"],["n faol (256), h doimiy",str(mk['SBZ_n_faol_turli']),"1","00 / A"],["h faol (256), n doimiy",str(mk['SBZ_h_faol_turli']),"1","00 / A"],["h = n = x faol (256)",str(mk['SBZ_ikkalasi_faol_turli']),"har xil",f"{mk['SBZ_ikkalasi_xor']:02x} / U"],["h va n mustaqil faol (2¹⁶)",str(im['turli']),", ".join(map(str,im['har_qiymat'])),f"{im['xor']:02x} / B (har qiymat 256 marta)"]],"SBZ ning tanlangan to‘plamlarga ta’siri")
P(f"*Qo‘sh.* Element akslantirishi odatda bijeksiya emas (200 parametrdan {mk['Qosh_element_turli_qiymatlar'].get('255',0)} tasida 255 xil qiymat) va massiv darajasida J, K bog‘lanishlari tufayli faol to‘plamni deyarli butun massivga U sifatida tarqatadi. *Aralash* A to‘plamni A (toq koeffitsiyent), B (juft koeffitsiyent) yoki C ga o‘tkazadi va U hosil qilmaydi. *SurHolat* xossalarni ko‘chiradi, *SurKalit, TuzilmaKalit* holatga ta’sir qilmaydi.")
rr=[["Akslantirish (bitta faol element)","A","C","B","B7","U"]]
for p,lab in [(256,'256'),(16,'128')]:
    d_=mk[f'massiv_{p}']
    for k_,lb in [('Qosh_holat',"Qo‘sh: holat"),('Qosh_holatn',"Qo‘sh: holatn"),('Aralash','Aralash'),('BZ_n_faol','SBZ (holatn[0] faol)'),('BZ_h_faol','SBZ (holat[0] faol)')]:
        if k_ in d_: rr.append([f"{lab}: {lb}"]+[fz(d_[k_][t],2) for t in ('A','C','B','B7','U')])
T([3554,1160,1160,1160,1160,1160],rr,"Bitta faol elementli to‘plamning massiv akslantirishlaridan keyingi xossalari (32 pozitsiya bo‘yicha o‘rtacha)",key='intarr')
P("256 bitli rejimda SBZ bitta faol baytni bitta A pozitsiyaga o‘tkazadi; 128 bitli rejimda faol yarim bayt juftlangan baytning ikkala yarim baytiga U sifatida tarqaladi (ikkita pozitsiya). Bit darajasida: yutishsiz akslantirishlarda 0-qatlam chiziqli bo‘lgani uchun 0-bitlar to‘plam bo‘yicha balanslangan bo‘lib qoladi; SBZ esa 0-bitni barcha 16 kirish bitining yuqori darajali funksiyasiga aylantiradi.")
H2('4.3. Integral xossalarning akslantirishlar va raundlar orqali o‘tishi')
P("Birinchi tajribada 1-raund kirishidagi holat[0,0] faol qilindi (256 yoki 16 qiymat), 40 ta tasodifiy kalit va holatda takrorlandi; jadvallarda barcha 40 tajribada balanslangan bitlar soni keltirilgan.")
rr=[["1-raund akslantirishi","To‘plam bo‘yicha XOR yig‘indi (A ilova, SBZ-256)"]]
for r in SX['integral_misol']:
    if r['raund']==1: rr.append([opn[r['amal']],nl(r['yigindi'])])
T([3354,6000],rr,"SBZ-256, A ilova misoli: holat[0,0] faol, 256 ta holat bo‘yicha XOR yig‘indilar",mono=(1,))
P("Aralash dan keyin barcha yig‘indilar 00, Qo‘sh dan keyin yig‘indilar noldan farq qiladi, lekin hammasi juft — 0-qatlam balansi saqlanadi.")
def irow(key,j): return [r for r in I[key] if r['raund']==j]
rr=[["Rejim, akslantirish","Bayt: doim B","Bit-qatlamlar: doim nol bitlar","O‘rtacha: B / U"]]
for key,lab in [('raund_256_holat','256'),('raund_16_holat','128')]:
    for r in irow(key,1): rr.append([f"{lab}: {opn[r['amal']]}",str(r['doim_B']),", ".join(map(str,r['qatlam_doim_nol'])),f"{fz(r['ortacha']['B'],1)} / {fz(r['ortacha']['U'],1)}"])
T([2900,1300,3300,1854],rr,"1-raund akslantirishlari bo‘yicha integral xossalar (holat[0,0] faol, 40 tajriba)",key='intop')
rr=[["Raund j"]+[str(j) for j in range(1,11)]]
for key,lab in [('raund_256_holat','SBZ-256: 0-qatlam'),('raund_256_holat#','SBZ-256: 1–7-qatlamlar'),('raund_16_holat','SBZ-128: 0-qatlam'),('raund_16_holat#','SBZ-128: 1–3-qatlamlar')]:
    rows_=[r for r in I[key.rstrip('#')] if r['amal']=='Tuz']
    rr.append([lab]+([str(sum(r['qatlam_doim_nol'][1:])) for r in rows_] if key.endswith('#') else [str(r['qatlam_doim_nol'][0]) for r in rows_]))
T([2850]+[650]*10,rr,"Raundlar oxirida doim balanslangan bitlar soni (holat[0,0] faol)",key='intr')
IMG('ch4.png',15.5,6.9,"Raundlar bo‘yicha doim balanslangan bitlar soni bit-qatlamlar kesimida (SBZ varianti)")
r8=[r for r in SX['integral_misol'] if r['raund']==8]
rr=[["8-raund akslantirishi","XOR yig‘indi (A ilova, SBZ-256)"]]+[[opn[r['amal']],nl(r['yigindi'])] for r in r8]
T([3354,6000],rr,"SBZ-256, A ilova misoli: 8-raunddagi yutishda 0-qatlam balansining yo‘qolishi",mono=(1,))
P("Ikkala rejimda 0-qatlamning 32 biti 1–7-raundlarda ehtimollik 1 bilan balanslangan, 8-raunddagi SBZ dan keyin balans yo‘qoladi (A ilova misolida SBZ dan keyingi yig‘indilar toq qiymatlarni o‘z ichiga oladi). Standart-128 da bu balans butun xesh davomida saqlanar edi; SBZ-128 da u birinchi ichki yutishda yo‘qoladi.")
rr=[["Rejim (8-raund)","Bayt: doim B","Bit-qatlamlar: doim nol bitlar","O‘rtacha: B / U"]]
for key,lab in [('raund_256_holat','256'),('raund_16_holat','128')]:
    for r in irow(key,8): rr.append([f"{lab}: {opn[r['amal']]}",str(r['doim_B']),", ".join(map(str,r['qatlam_doim_nol'])),f"{fz(r['ortacha']['B'],1)} / {fz(r['ortacha']['U'],1)}"])
T([2900,1300,3300,1854],rr,"8-raund akslantirishlari bo‘yicha integral xossalar (holat[0,0] faol, 40 tajriba)")
P("8-raundda Qo‘sh(holat, blok) gacha 0-qatlam 32/32 balanslangan, SBZ dan keyin esa bitta ham balanslangan bit qolmaydi. Demak, integral farqlovchining uzunligi aniq 7 raund va 8-raundning yutishgacha bo‘lgan qismi.")
H3('4.3.1. Kirish blokidagi faol to‘plam')
rr=[["Rejim, qadam","Bayt: doim B","Bit-qatlamlar: doim nol bitlar","O‘rtacha: B / U"]]
for key,lab in [('raund_256_blok','256'),('raund_16_blok','128')]:
    for r in I[key]:
        if r['raund']==0 or (r['amal']=='Tuz' and r['raund'] in (1,7,10)) or r['amal'] in ('BZ8','BZ9'):
            nm=opn[r['amal']] if r['raund']==0 or r['amal'] in ('BZ8','BZ9') else f"{r['raund']}-raund oxiri"
            rr.append([f"{lab}: {nm}",str(r['doim_B']),", ".join(map(str,r['qatlam_doim_nol'])),f"{fz(r['ortacha']['B'],1)} / {fz(r['ortacha']['U'],1)}"])
T([2900,1300,3300,1854],rr,"Kirish blokidagi faol element: integral xossalarning o‘tishi (40 tajriba)",key='intblok')
P("0-nuqtadagi Qo‘sh dan keyin holatning 0-qatlami (va 256 bitli rejimda 1-qatlami) balanslangan, lekin SBZ dan keyin ikkala rejimda barcha balans yo‘qoladi: SBZ holat va holatn baytlarining barcha bitlarini aralashtiradi. Standart-128 da XOR bu balansni saqlab qolar edi.")
H2('4.4. Yuqori tartibli integral xossalar')
P("Bitta faol baytli to‘plamdan tashqari, kattaroq — 2¹⁶ elementli — to‘plamlar ham tekshirildi: kirish blokining ikkita bayti (128 bitli rejimda to‘rtta yarim bayti) barcha qiymatlarni qabul qiladi. Bunday to‘plam bo‘yicha XOR yig‘indisi daraja 16 dan kichik bo‘lgan har qanday bit uchun nolga teng, shuning uchun u SBZ ning 13-darajasini «chetlab o‘tishi» mumkin.")
ib=S3['ikki_bayt_blok']
nm8={('Qosh0',0):'Qo‘sh(holat, blok) (0-nuqta)',('BZ0',0):'SBZ (0-nuqta)',('Tuz',1):'1-raund oxiri',('Tuz',2):'2-raund oxiri',('Tuz',3):'3-raund oxiri'}
rr=[["Qadam","SBZ-256: bit-qatlamlar bo‘yicha doim nol bitlar (0…7)","SBZ-128: bit-qatlamlar bo‘yicha (0…3)"]]
for (a,b),(c_,d_) in zip(ib['256'],ib['16']): rr.append([nm8[tuple(a)],", ".join(map(str,b)),", ".join(map(str,d_))])
T([3000,3654,2700],rr,"Ikki faol baytli (2¹⁶) blok to‘plami: bitta iteratsiya ichidagi integral xossalar (8 tajriba)")
P("Iteratsiya ichida bunday to‘plam sezilarli xossalarni saqlaydi: SBZ-256 da 0-nuqtadagi SBZ dan keyin 32 baytdan 30 tasi barcha bitlari bo‘yicha balanslangan (faqat faol pozitsiyalardagi ikki bayt emas), so‘ng 0-qatlamda balanslangan bitlar soni raundlar bo‘yicha 21 → 10 → 2 ga kamayadi; SBZ-128 da 0-qatlam 1–3-raundlarda to‘liq balanslangan. Sababi: 0-nuqtadagi SBZ chiqishining har bir bayti 16 ta faol bitga nisbatan 16 dan kichik darajaga ega, yutishsiz raundlar esa 0-qatlamni chiziqli o‘zgartiradi.")
P("To‘liq xesh uchun xuddi shu turdagi 2¹⁶ to‘plamlar bilan sinov o‘tkazildi (har bir tajribada 65536 ta xabar).")
rr=[["Rejim (xabar, faol baytlar)","Tajribalar","Bit-qatlamlar bo‘yicha doim nol bitlar","Nol ulushi (o‘rtacha)"]]
rr.append(["SBZ-128 (16 bayt, 0–1-baytlar)","4",", ".join(map(str,HO16['doim_nol'])),fz(sum(HO16['nol_ulushi'])/4,2)])
rr.append(["SBZ-256 (64 bayt, 32–33-baytlar)","4",", ".join(map(str,HO['doim_nol_4'])),fz(sum(HO['nol_ulushi'])/8,2)])
rr.append(["Standart-128 (taqqoslash)","2",", ".join(map(str,HOS['doim_nol'])),fz(sum(HOS['nol_ulushi'])/4,2)])
T([3300,1300,2900,1854],rr,"To‘liq xesh: 2¹⁶ elementli to‘plam bo‘yicha XOR yig‘indisi doim nol bo‘lgan bitlar")
P("Tasodifiy funksiya uchun bitning 4 ta tajribada doim nol bo‘lish ehtimolligi 1/16, ya’ni har bir qatlamda o‘rtacha 2 bit; 2 ta tajribada — 8 bit. SBZ-128 natijalari (3, 1, 5, 1) va SBZ-256 natijalari (6, 1, 2, 2, 4, 2, 0, 3) shu darajaga mos; SBZ-256 ning 0-qatlamidagi biroz ortiqcha (6) qiymat chiqishdagi doimiy bitlar (Aralash nol satrlari) bilan izohlanadi — doimiy bit har qanday to‘plamda balanslangan. Standart-128 da esa 0-qatlamning 32 biti doim nol. Demak, ichki iteratsiyadagi yuqori tartibli xossalar 8- va 9-nuqtalardagi qayta yutishlar va keyingi iteratsiyalar (uzunlik, NY bloklari) tomonidan yo‘q qilinadi va SBZ variantida to‘liq xesh uchun yuqori tartibli integral farqlovchi ham topilmadi.")
H2('4.5. To‘liq xesh uchun integral farqlovchi (bitta faol bayt)')
tx=I['toliq_xesh']
rr=[["Rejim","Bit-qatlam j"]+[str(j) for j in range(8)]]
rr.append(["SBZ-128","doim nol bitlar"]+[str(v) for v in tx['16']['qatlam_boyicha_doim_nol_bitlar']]+["—"]*4)
rr.append(["SBZ-128","nol ulushi"]+[fz(v,2) for v in tx['16']['qatlam_boyicha_nol_ulushi']]+["—"]*4)
rr.append(["SBZ-256","doim nol bitlar"]+[str(v) for v in tx['256']['qatlam_boyicha_doim_nol_bitlar']])
rr.append(["SBZ-256","nol ulushi"]+[fz(v,2) for v in tx['256']['qatlam_boyicha_nol_ulushi']])
T([1750,1700]+[738]*8,rr,"To‘liq xesh: to‘plam bo‘yicha XOR yig‘indisi nol bo‘lgan bitlar (40 tajriba)",key='intfull')
P("SBZ-128 (bir blokli xabar, 0-bayt faol) va SBZ-256 (ikki blokli xabar, ikkinchi blokdagi 0-bayt faol) uchun xesh qiymatlar to‘plami bo‘yicha birorta ham bit doim balanslangan emas, nol ulushi ≈0,5. Standart-128 da esa 0-qatlamning 32 biti 40 tajribaning barchasida balanslangan edi. Demak, SBZ to‘liq xesh uchun integral farqlovchini yo‘qotadi.")
P("*Buzg‘unchi uchun foydalanish.* 7 raundli ichki farqlovchidan foydalanish uchun buzg‘unchi 1-raund kirishidagi holatda faol to‘plam hosil qilishi kerak. Holatga esa faqat xabar bloki va SBZ orqali ta’sir qilish mumkin: blokdagi faol to‘plam SBZ dan keyin balansini yo‘qotadi (4.3.1-band), holatda bitta faol bayt hosil qilish uchun esa SBZ chiqishi shu baytdan boshqa barcha baytlarda doimiy bo‘lishi kerak, Qo‘sh dagi bog‘lanish bunga yo‘l qo‘ymaydi. Shuning uchun SBZ variantida integral xossa amaliy hujumga aylanmaydi; Standart-128 da esa xuddi shu xossa XOR orqali to‘liq xeshgacha yetib borgan edi.")
H2('4.6. Bardoshlilik bahosi')
T([2000,2600,2600,2154],[["Rejim","Bayt darajasidagi xossa","Bit darajasidagi (0-qatlam) xossa","Xulosa"],["SBZ-256","bitta Qo‘sh dan keyin yo‘qoladi","1–7-raundlarda saqlanadi, 8-raunddagi SBZ da yo‘qoladi","xabar orqali — 0-nuqtadan keyin bardoshli; ichki holat orqali — 8-raunddan keyin"],["SBZ-128","bitta Qo‘sh dan keyin yo‘qoladi","1–7-raundlarda saqlanadi, 8-raunddagi SBZ da yo‘qoladi","xuddi shunday; to‘liq xesh uchun farqlovchi yo‘q"],["Standart-128 (taqqoslash)","bitta Qo‘sh dan keyin yo‘qoladi","butun xesh davomida saqlanadi","bardoshli emas"]],"Integral bardoshlilik bahosi")
H2('4.7. Integral kriptotahlil bo‘yicha xulosalar')
BL("Bayt darajasidagi integral xossalar Qo‘sh dagi massivlararo bog‘lanish tufayli bitta Qo‘sh dan keyin yo‘qoladi; SBZ bitta argumentdagi faol to‘plamni A ga o‘tkazadi.")
BL("0-qatlam T-funksiya xossasi tufayli yutishsiz raundlarda (1–7) balanslangan qoladi — bu ichki holat bo‘yicha 7 raundli farqlovchi; u 8-raunddagi SBZ da yo‘qoladi.")
BL("Xabar orqali kiritilgan faol to‘plam 0-nuqtadagi SBZ dan keyinoq balansini yo‘qotadi; to‘liq xesh uchun integral farqlovchi ikkala rejimda topilmadi.")
BL("SBZ-128 da Standart-128 dagi to‘liq xesh bo‘yicha 32 bitli integral farqlovchi yo‘qoladi.")
BL("2¹⁶ elementli to‘plamlar bitta iteratsiya ichida 0-qatlam balansini 1–3 raund saqlaydi, lekin to‘liq xesh uchun yuqori tartibli farqlovchi ham topilmadi (doimiy bitlardan tashqari).")

# =================== UMUMIY ===================
PB(); H1('Umumiy xulosa')
T([2300,2350,2350,2354],[["Usul","SBZ-256","SBZ-128","Standart (taqqoslash: 256 / 128)"],
 ["Chiziqli","2⁻⁶⁴: mediana — 4 qatlam (≈11-raund), eng yomon kalit — 11 qatlam","2⁻³²: mediana — 4 qatlam, eng yomon — 6 qatlam (20 raund)","≈18–19-raund / bardoshli emas"],
 ["Differensial","8-raunddan keyin","8-raunddan keyin","9-raund / bardoshli emas"],
 ["Algebraik","0-nuqtadan keyin","0-nuqtadan keyin","1-raund / bardoshli emas"],
 ["Integral","xabar orqali — 0-nuqtadan; ichki holat — 8-raunddan keyin; 2¹⁶ to‘plam bilan ham to‘liq xesh farqlovchisi yo‘q","xuddi shunday","xuddi shunday / bardoshli emas"],
 ["Qoldiq xossalar","chiqishda ≈6 ta c = 1 munosabat, doimiy bitlar, Aralash yadrosi orqali so‘nish (≈3%), eng yomon kalitlar","xuddi shunday","xuddi shunday"]],"SBZ variantining to‘rtta kriptotahlil usuliga bardoshliligi")
P("SBZ variantining tahlili quyidagi xulosalarga olib keladi. Birinchidan, SBZ yutish nuqtasini algoritmning kuchli qatlamiga aylantiradi: maksimal korrelyatsiya 2⁻⁶, maksimal differensial ehtimollik 2⁻⁶ (faqat holat ayirmasi uchun; xabar ayirmasi ishtirok etganda ≤ 2⁻⁷·⁶), bitta argumentdagi ayirma so‘nmaydi, algebraik daraja 13, integral to‘plamlar balansi yo‘qoladi. Natijada to‘rttala usul bo‘yicha bardoshlilikka standart algoritmga qaraganda ancha oldin erishiladi.")
P("Ikkinchidan, 128 bitli rejimda SBZ eng katta samara beradi: Standart-128 to‘rttala usulning hech biriga bardoshli emas edi (0-qatlam butun xesh bo‘yicha chiziqli, bashorat qilinadigan va balanslangan), SBZ-128 da bu zaifliklarning barchasi yo‘qoladi — 0-qatlam tenglamasi, linearizatsiya hujumi, bit-qatlamlar bo‘yicha ajralish va to‘liq xesh integral farqlovchisi kuzatilmaydi.")
P("Uchinchidan, SBZ yutishsiz raundlarning T-funksiya xossasiga ta’sir qilmaydi: 1–7-raundlarda 0-qatlam chiziqli tenglama bilan kuzatiladi, MSB izlari ≈0,9 ehtimollik bilan saqlanadi va 0-qatlam balanslangan. Shuningdek, Aralash degeneratsiyasidan kelib chiqadigan xossalar — chiqishdagi c = 1 munosabatlar, doimiy bitlar, ichki kolliziyalar va eng yomon kalitlar — SBZ bilan saqlanib qoladi. Bu kamchiliklar Aralash/TuzilmaKalit va raund funksiyasi bo‘yicha tavsiyalarning alohida tahlilida ko‘rib chiqiladi.")
H2('Tahlil usuli va cheklovlari')
P("Akslantirishlarning korrelyatsion va ayirmalar matritsalari (SBZ uchun 255 × 65536 va 65536 × 256 o‘lchamli to‘liq matritsalar), ANF darajalari, implitsit tenglamalar soni va to‘plam xossalari barcha kirishlar bo‘yicha aniq hisoblandi. Raund darajasidagi ko‘rsatkichlar tanlanma asosida o‘lchandi: chiziqli tenglama — 1500 kalit, ayirmalar — 2000–3000 juftlik, integral — 40 tajriba, kub testlari — 4 ta kub, faol baytlar — 120–200 kalit. Chiziqli izlar 0-qatlam modeli doirasida, differensial chegaralar har bir faol bayt uchun eng yaxshi ehtimollik bilan baholandi. Dasturlar uzmst285_tahlil paketida (integral.py --bz sbz rejimi qo‘shildi) va sbz_kriptotahlili.ipynb daftarida.")
def _fix(x):
    if isinstance(x,str): return _re.sub(r'⟦(\w+)⟧',lambda m:str(TK[m.group(1)]),x)
    if isinstance(x,list): return [_fix(y) for y in x]
    return x
B=[_fix(b) for b in B]
json.dump(B,open('blocks.json','w'),ensure_ascii=False); print(len(B),tc[0],fc[0])
