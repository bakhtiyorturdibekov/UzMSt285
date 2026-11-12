import json, math
J=lambda f: json.load(open('/home/claude/ka/'+f+'.json'))
L1,L2,L3,D1,A1,A2,A3,EX=[J(x) for x in ['lin1','lin2','lin3','dif1','alg1','alg2','alg3','ex']]
D2=J('dif2'); D3=J('dif3')
B=[]
def H1(t): B.append(['h1',t])
def H2(t): B.append(['h2',t])
def H3(t): B.append(['h3',t])
def P(t): B.append(['p',t])
def F(t): B.append(['f',t])
def BL(t): B.append(['b',t])
def CAP(t): B.append(['cap',t])
def T(widths,rows,cap): B.append(['cap',cap]); B.append(['t',widths,rows])
def IMG(path,w,h,cap): B.append(['img',path,w,h]); B.append(['fcap',cap])
def PB(): B.append(['pb'])
def fz(x,d=2): return (f'{x:.{d}f}').replace('.',',')
def lg(x): return fz(math.log2(x),1)

# ---------------- TITUL ----------------
B.append(['title','O‘zMSt 285:2024 1-ALGORITMIDA BaytZichlash O‘RNIGA SBZ O‘ZGARTIRISHINI QO‘LLASHNING CHIZIQLI, DIFFERENSIAL VA ALGEBRAIK KRIPTOTAHLILGA TA’SIRI'])
B.append(['sub','Kriptotahlil hisoboti'])
H1('Kirish')
P("Ushbu hisobotda O‘zMSt 285:2024 standartining 1-algoritmida *BaytZichlash(holat, holatn)* o‘zgartirishini *SBZ(holat, holatn)* = §S§(§h§ ⊕ §S§(§n§)) o‘zgartirishi bilan almashtirish algoritmning chiziqli, differensial va algebraik kriptotahlilga bardoshliligiga qanday ta’sir qilishi buzg‘unchi (hujumchi) nuqtai nazaridan tekshiriladi. Har bir usul bo‘yicha avval algoritmning har bir akslantirishi alohida o‘rganiladi (korrelyatsion matritsa, ayirmalar matritsasi, algebraik tenglamalar), so‘ngra ular raund darajasida birlashtiriladi va qaysi raunddan keyin algoritm tegishli hujumga bardoshli bo‘lishi baholanadi.")
P("Tahlil to‘rtta variant uchun parallel olib boriladi: *Standart-256* (p = 256, B ilovadagi chiziqli zichlash massivi), *SBZ-256*, *Standart-128* (p = 16, XOR) va *SBZ-128*. Barcha hisob-kitoblar mustaqil dasturiy realizatsiyada bajarildi. Realizatsiya standartning A ilovasidagi nazorat misolini va SBZ materialidagi barcha nazorat qiymatlarini (KAT) bayt-ma-bayt takrorlaydi. Akslantirishlar ko‘rsatkichlari barcha kirishlar bo‘yicha to‘liq hisoblandi. Raund darajasidagi ko‘rsatkichlar tasodifiy kalit, holat va xabarlarda 1500–4000 juftlik tanlanmasida o‘lchandi; tanlanma hajmi har bir jadvalda ko‘rsatilgan.")
P("Tahlil davomida quyidagi atamalardan foydalaniladi. *Bit-qatlam* — holat massivining barcha elementlaridagi bir xil tartib raqamli bitlar to‘plami; *0-qatlam* (quyi qatlam) har bir elementning eng kichik bitidan iborat 32 bitli vektor. *Yutish nuqtasi* — kirish bloki holatga qo‘shiladigan va BaytZichlash (yoki SBZ) bajariladigan nuqta. Har bir tashqi iteratsiyada (har bir kirish bloki uchun) uchta yutish nuqtasi bor: raundlardan oldin (0-nuqta), 8-raund ichida va 9-raund oxirida. *Faol bayt* — chiziqli izda niqobi, differensial izda farqi noldan farqli bo‘lgan bayt (yoki yarim bayt).")
T([1700,7650],[["Qadam","Bajariladigan amallar (bitta kirish bloki uchun)"],
 ["0-nuqta","Qo‘sh(holat, blok), BZ(holat, holatn) — yutish"],
 ["1–7-raundlar","Aralash(holat, kₑ) → Qo‘sh(holat, kₑ) → SurHolat, SurKalit → Qo‘sh(holat, kₑ) → TuzilmaKalit(kₑ, k)"],
 ["8-raund","Aralash → Qo‘sh(holat, kₑ) → SurHolat, SurKalit → Qo‘sh(holat, blok), BZ — yutish → TuzilmaKalit"],
 ["9-raund","1–7-raundlar kabi, oxirida Qo‘sh(holat, blok), BZ — yutish"],
 ["10-raund","1–7-raundlar kabi"]],
 "1-jadval. Bitta tashqi iteratsiyadagi akslantirishlar ketma-ketligi (BZ — BaytZichlash yoki SBZ)")
P("Jadvaldan ko‘rinadiki, 1–7-raundlarda va 10-raundda faqat *Aralash, Qo‘sh, SurHolat, SurKalit, TuzilmaKalit* ishlaydi. Bu akslantirishlarning barchasi 2ⁿ moduli bo‘yicha arifmetika yoki o‘rin almashtirishdan iborat. Shuning uchun ular *T-funksiya* xossasiga ega: natijaning §j§-biti kirishlarning faqat 0…§j§-bitlariga bog‘liq. Bu xossa uchala kriptotahlil usulida ham hal qiluvchi rol o‘ynaydi. Yutish nuqtasidagi akslantirish esa yuqori bitlardagi axborotni quyi bitlarga o‘tkazuvchi yagona element hisoblanadi.")

# ---------------- 1. CHIZIQLI ----------------
PB(); H1('1. Chiziqli kriptotahlil')
H2('1.1. Asosiy tushunchalar')
P("Chiziqli kriptotahlilda buzg‘unchi kirish va chiqish bitlarining XOR yig‘indilari orasidagi ehtimolligi 1/2 dan farq qiladigan munosabatlarni (chiziqli approksimatsiyalarni) qidiradi. §F§: GF(2)ⁿ → GF(2)ᵐ akslantirish uchun kirish niqobi §α§ va chiqish niqobi §β§ bo‘lgan approksimatsiyaning korrelyatsiyasi quyidagicha aniqlanadi:")
F("c_F(α → β) = 2⁻ⁿ · Σₓ (−1)^(β·F(x) ⊕ α·x),        ε = c/2,")
P("bu yerda ε — chetlanish (bias), ya’ni munosabatning bajarilish ehtimolligi 1/2 + ε. Barcha (§β§, §α§) juftliklari uchun c qiymatlaridan tuzilgan matritsa *korrelyatsion matritsa* deyiladi. Raundlar orqali chiziqli iz (trail) korrelyatsiyasi oraliq korrelyatsiyalar ko‘paytmasiga teng (Matsui «piling-up» qoidasi): c_iz = Π cᵢ. Hujum uchun kerakli ma’lumotlar hajmi N ≈ c⁻² ga teng. Shuning uchun 256 bitli xesh uchun chiziqli farqlovchi umumiy hujumdan (2¹²⁸) samaraliroq bo‘lmasligi uchun |c| ≤ 2⁻⁶⁴, 128 bitli rejim uchun |c| ≤ 2⁻³² talab qilinadi.")
H2('1.2. Akslantirishlarning korrelyatsion matritsalari va approksimatsiya tenglamalari')
H3('1.2.1. AES S-box (SBZ tarkibidagi S)')
d=L1['S_lat_dist']
P(f"S akslantirish uchun 256×256 korrelyatsion matritsa to‘liq hisoblandi. Nolga teng bo‘lmagan chiqish niqoblari uchun |c| qiymatlari faqat {{0, 2⁻⁶, 2⁻⁵, 3·2⁻⁶, 2⁻⁴, 5·2⁻⁶, 3·2⁻⁵, 7·2⁻⁶, 2⁻³}} to‘plamidan olinadi; maksimal |c| = 2⁻³ (chetlanish 2⁻⁴). Bunday eng yaxshi approksimatsiyalar soni {L1['S_best_count']} ta. Matritsaning bir qismi 2-jadvalda keltirilgan (jadvalda W = 256·c qiymatlari).")
blk=EX['S_lat_block']
T([1250]+[1012]*8,[["β \\ α"]+[f"{a:02X}" for a in range(1,9)]]+[[f"{b:02X}"]+[str(v) for v in blk[b-1]] for b in range(1,9)],"2-jadval. S korrelyatsion matritsasining bo‘lagi: W(α→β) = 256·c (α — kirish, β — chiqish niqobi)")
T([3600,1400,1400,1400,1550],[["|W| qiymati","0","4…12","16…24","28…32"],["Matritsa elementlari soni",str(d['0']),str(d['4']+d['8']+d['12']),str(d['16']+d['20']+d['24']),str(d['28']+d['32'])],["Korrelyatsiya |c|","0","2⁻⁶…3·2⁻⁶","2⁻⁴…3·2⁻⁵","7·2⁻⁶…2⁻³"]],"3-jadval. S korrelyatsion matritsasi elementlarining taqsimoti (β ≠ 0)")
P("Eng yaxshi approksimatsiyalardan biri: kirish niqobi α = 2D, chiqish niqobi β = 01:")
F("y₀ = x₀ ⊕ x₂ ⊕ x₃ ⊕ x₅ ⊕ 1,     c = 2⁻³  (y = S(x)).")
H3('1.2.2. Standart B ilovadagi zichlash massivi (8 → 4)')
dz=L1['Z_lat_dist']
P(f"Standart BaytZichlash o‘zgartirishi har bir baytni 8 → 4 bitli Z jadvali orqali siqadi. Z ning 15×256 korrelyatsion matritsasida maksimal |c| = 0,25 (chetlanish 2⁻³); u α = C5, β = 5 niqoblarda erishiladi. Chiqishning 0-biti uchun eng yaxshi korrelyatsiya {fz(L1['Z_out_bit0_best'],3)} ga teng. Taqsimot: |W| = 0 — {dz['0']} ta, 8 — {dz['8']}, 16 — {dz['16']}, 24 — {dz['24']}, 32 — {dz['32']}, 40 — {dz['40']}, 48 — {dz['48']}, 56 — {dz['56']}, 64 — {dz['64']} ta. 300 ta tasodifiy muvozanatli 8 → 4 jadval medianasi |W| = 60 bo‘lgani uchun Z tasodifiy jadval darajasida, lekin optimallashtirilmagan.")
F("z₀ ⊕ z₂ = x₀ ⊕ x₂ ⊕ x₆ ⊕ x₇,     c = 2⁻²  (z = Z(x)).")
P("BaytZichlash natijasida holatning yangi bayti (Z(h) ‖ Z(n)) ko‘rinishida hosil bo‘ladi, shuning uchun chiqishning yuqori yarim bayti faqat holatga, quyi yarim bayti faqat kirish blokiga bog‘liq; 16 bitli kirish va 8 bitli chiqish orasidagi 128 ta mumkin bo‘lgan bog‘liqlikdan faqat 64 tasi mavjud.")
H3('1.2.3. XOR (p = 16 rejimidagi BaytZichlash)')
P("128 bitli rejimda BaytZichlash yarim baytlarni bitma-bit qo‘shadi: §y§ = §h§ ⊕ §n§. Bu to‘liq chiziqli akslantirish bo‘lib, uning har bir bit uchun approksimatsiya tenglamasi aniq bajariladi:")
F("yᵢ = hᵢ ⊕ nᵢ,     c = 1,   i = 0, 1, 2, 3.")
H3('1.2.4. SBZ o‘zgartirishi')
P("SBZ uchun korrelyatsiya S korrelyatsiyalari orqali aniq ifodalanadi. §x§ = §h§ ⊕ §S§(§n§) almashtirish kiritilsa, yig‘indi ikkita mustaqil yig‘indiga ajraladi:")
F("c_SBZ((α, β) → γ) = c_S(α → γ) · c_S(β → α),")
P(f"bu yerda α — h dagi niqob, β — n dagi niqob, γ — chiqish niqobi. Bundan ikkita muhim xulosa kelib chiqadi: (1) noldan farqli korrelyatsiya uchun h dagi niqob «o‘rta» niqobga teng bo‘lishi va noldan farq qilishi shart, ya’ni faqat n orqali o‘tuvchi approksimatsiya mavjud emas; (2) maksimal |c| = (2⁻³)² = 2⁻⁶. To‘liq hisob bu qiymatni tasdiqladi: max |c| = {fz(L1['SBZ_corr_max'],6)} = 2⁻⁶, bunday (α, β, γ) uchliklar soni {L1['SBZ_best_triples']} ta. Masalan, α = 2D, β = 1A, γ = 01 uchun c_S(2D → 01) = −2⁻³, c_S(1A → 2D) = +2⁻³, demak:")
F("y₀ ⊕ (h₀ ⊕ h₂ ⊕ h₃ ⊕ h₅) ⊕ (n₁ ⊕ n₃ ⊕ n₄) = 1,     c = 2⁻⁶.")
P(f"Agar buzg‘unchi h dagi niqobni faqat quyi bitlar bilan cheklasa (α ∈ {{01, 02, 03}}), eng yaxshi korrelyatsiya {fz(L1['SBZ_gamma1_alpha_low'],4)} ≈ 2⁻⁶·⁴ gacha kamayadi. Bu holat quyida ko‘rib chiqiladigan quyi qatlam izlari uchun muhim.")
H3('1.2.5. Qo‘sh o‘zgartirishi')
qa=L1['Qosh_bitj_bestcorr_avg']; qm=L1['Qosh_bitj_bestcorr_min']; qs=L1['Qosh_bitj_corr_avg']
P("Qo‘sh o‘zgartirishi har bir elementni ( A, B, R ) parametrli −3 darajaga ko‘taradi: x → x⁻¹ → x⁻² → x⁻³, bunda x⁻¹ ≡ −A·x·(B + R·x)⁻¹ (mod p). A, B, R parametrlari massivlarning yig‘indilari (J) va ko‘paytmalariga (K) bog‘liq, lekin bitta element nuqtai nazaridan ular belgilangan qiymatlardir. A va B doim toq, R juft bo‘lgani uchun (B + R·x) toq va teskarilanuvchi, bundan:")
F("x⁻¹ ≡ x (mod 2),     ya’ni  y₀ = x₀,   c = 1.")
P("Barcha amallar (ko‘paytirish, qo‘shish, teskarilash) 2ⁿ moduli bo‘yicha bajarilgani uchun element darajasidagi akslantirish T-funksiya hisoblanadi (yagona istisno — x⁻² ≡ 0 bo‘lganda A₂ + B₂ ga almashtirish, u 256 ta kirishdan 2 tasida ishlaydi va akslantirishni bijektiv bo‘lmagan qiladi: 255 xil qiymat). 200 ta tasodifiy parametrlar to‘plami bo‘yicha element korrelyatsion matritsasi hisoblandi. Natijalar 4-jadvalda keltirilgan.")
T([2880]+[808]*8,[["Chiqish biti j","0","1","2","3","4","5","6","7"],
 ["Eng yaxshi |c| (o‘rtacha)"]+[fz(v,3) for v in qa],["Eng yaxshi |c| (minimum)"]+[fz(v,3) for v in qm],["|c(xⱼ → yⱼ)| (o‘rtacha)"]+[fz(v,3) for v in qs]],
 "4-jadval. Qo‘sh elementining bit-qatlamlar bo‘yicha korrelyatsiyalari (200 ta parametrlar to‘plami)")
P("Jadvaldan ko‘rinadiki, 0- va 1-bitlar deyarli har doim chiziqli: y₀ = x₀ (c = 1) va y₁ = x₁ ⊕ δ·x₀ (δ ∈ {0,1} parametrlarga bog‘liq, c ≥ 0,992). 2- va 3-bitlar uchun o‘rtacha 0,77 va 0,69 korrelyatsiyali chiziqli tenglamalar mavjud. Demak, Qo‘sh o‘zgartirishi quyi bit-qatlamlarni chiziqli darajada amalda o‘zgartirmaydi va ular orqali chiziqli izlar deyarli yo‘qotishsiz o‘tadi.")
H3('1.2.6. Aralash o‘zgartirishi')
P("Aralash diamatritsalarni 2ⁿ moduli bo‘yicha ko‘paytiradi. Belgilangan kₑ uchun u h ga nisbatan Z/2ⁿ halqasi ustida chiziqli. 2 moduli bo‘yicha (0-qatlamda) har bir chiqish biti kirish 0-qatlamining aniq chiziqli funksiyasi bo‘ladi. Chap yarim uchun (s, u ∈ {0,1,2,3}, σᵤ = Σᵢ kₑ[i,u]₀):")
F("h′[u,u]₀ = σᵤ·h[u,u]₀ ⊕ Σ_{i≠u} kₑ[i,u]₀·h[i,i]₀,")
F("h′[s,u]₀ = σᵤ·h[s,u]₀ ⊕ kₑ[s,u]₀·Σᵢ h[i,u]₀ ⊕ Σ_{i≠s,u} kₑ[i,u]₀·h[s,i]₀   (s ≠ u),")
P(f"o‘ng yarim uchun ham xuddi shunday. Bu tenglamalar c = 1 bilan bajariladi va ularni h′₀ = M(k₀)·h₀ ko‘rinishida yozish mumkin, bu yerda M(k₀) — 32×32 o‘lchamli GF(2) matritsa bo‘lib, u faqat kalitning 0-qatlamiga bog‘liq (TuzilmaKalit kₑ juftligini doim k juftligiga tenglashtiradi). 200 ta tasodifiy kalit uchun L = P·M matritsasining o‘rtacha rangi {fz(L2['rank_L']['mean'],1)} (min {L2['rank_L']['min']}, max {L2['rank_L']['max']}); to‘liq rangli kalit uchramadi. Kalitlarning {fz(100*L2['zero_rows']['share_keys_with_zero_row'],1)} foizida M da nol satr bor (o‘rtacha {fz(L2['zero_rows']['mean'],2)} ta). Yuqori bit-qatlamlarda ko‘chirishlar (carry) tufayli nochiziqlilik paydo bo‘ladi, lekin j-bit faqat 0…j-bitlarga bog‘liqligicha qoladi.")
H3('1.2.7. SurHolat, SurKalit va TuzilmaKalit')
P("SurHolat va SurKalit — o‘rin almashtirishlar: chiziqli izdagi niqob shunchaki boshqa pozitsiyalarga ko‘chadi, korrelyatsiya 1 ga teng. SurHolat ni 32×32 o‘rin almashtirish matritsasi P bilan ifodalaymiz. TuzilmaKalit faqat raund kalitini o‘zgartiradi va kₑ′₀ = k₀ tenglamasini ta’minlaydi, ya’ni kₑ ning 0-qatlami har raundda kalitning 0-qatlamiga tenglashtiriladi (nol kirish niqobli c = ±1 munosabatlar).")
T([3500,1950,1950,1950],[["Akslantirish","Standart-256","Standart-128","SBZ (ikkala rejim)"],
 ["Yutish (BZ / SBZ), maks. |c|","2⁻² (0-bit: 2⁻²·²)","1","2⁻⁶"],
 ["Qo‘sh, 0- va 1-bit","1 / ≈1","1 / ≈1","1 / ≈1"],["Aralash, 0-qatlam","1","1","1"],["SurHolat, SurKalit","1","1","1"],["TuzilmaKalit (kₑ₀ = k₀)","1","1","1"]],
 "5-jadval. Akslantirishlar bo‘yicha eng yaxshi korrelyatsiyalar")
H2('1.3. Raund approksimatsiyalari')
P("Yuqoridagi tenglamalarni birlashtirsak, yutish nuqtasi bo‘lmagan raund uchun 0-qatlam bo‘yicha aniq chiziqli raund tenglamasi hosil bo‘ladi. Qo‘sh juftlikni saqlaydi, SurHolat pozitsiyalarni almashtiradi, Aralash M(k₀) matritsasi bilan ko‘paytiradi:")
F("h₀⁽ʲ⁾ = P · M(k₀) · h₀⁽ʲ⁻¹⁾ = L · h₀⁽ʲ⁻¹⁾,     c = 1,    j = 1, …, 7, 10.")
P("Bundan 0-nuqtadagi yutishdan keyingi holat va 7-raund natijasi orasida h₀⁽⁷⁾ = L⁷·h₀⁽⁰⁾ munosabati korrelyatsiya 1 bilan bajariladi. Bu tenglamani buzg‘unchi kalitning 0-qatlamini bilgan holda yoki noma’lum L matritsa koeffitsiyentlari sifatida ishlatishi mumkin. 6-jadvalda bu bashoratning haqiqiy algoritmda bajarilishi o‘lchangan (har bir variantda 1500 ta tasodifiy kalit va holat).")
lp=lambda k:[fz(v,2) for v in L2['lsb_pred_'+k]]
T([2350]+[700]*10,[["Variant \\ raund j"]+[str(j) for j in range(1,11)],["Standart-256"]+lp('256_std'),["SBZ-256"]+lp('256_sbz'),["Standart-128"]+lp('16_std'),["SBZ-128"]+lp('16_sbz')],
 "6-jadval. 0-qatlam bo‘yicha raund tenglamasi korrelyatsiyasi (o‘lchangan)")
P("Natijalar nazariy tahlilni to‘liq tasdiqlaydi: 1–7-raundlarda to‘rttala variantda ham korrelyatsiya 1 ga teng, ya’ni yutish nuqtasi bo‘lmagan raundlar chiziqli kriptotahlilga hech qanday qarshilik ko‘rsatmaydi. 8-raunddagi yutish nuqtasida Standart-256 va SBZ variantlarida korrelyatsiya nolga tushadi. Standart-128 da esa XOR chiziqli bo‘lgani uchun 0-qatlam butun iteratsiya davomida, yutish nuqtalarini ham qo‘shgan holda, c = 1 bilan aniq kuzatiladi: h₀ ← L·h₀ ⊕ blok₀. 10-raunddan keyingi kichik korrelyatsiya (≈0,07) chiqishdagi doimiy bitlar bilan bog‘liq (1.5-bo‘lim).")
H2('1.4. Yutish nuqtalari va faol baytlar soni')
P("Demak, chiziqli bardoshlilikni faqat yutish nuqtalari ta’minlaydi va iz korrelyatsiyasini baholash uchun iz qancha yutish qatlamidan va ularning har birida nechta faol bayt orqali o‘tishini aniqlash kifoya. Yutish qatlamlari orasidagi 0-qatlam akslantirishi ma’lum: 0-nuqtadan 8-raundgacha L⁸, 8-dan 9-gacha L, 9-dan keyingi iteratsiyaning 0-nuqtasigacha L. Iz orqaga tarqalganda niqob Lᵀ bilan ko‘paytiriladi. 200 ta tasodifiy kalit uchun ikkita ketma-ket qatlamdagi minimal faol baytlar yig‘indisi (chiziqli tarmoqlanish soni) hisoblandi:")
b1=L2['branch_L1']; b8=L2['branch_L8']
P(f"L (bitta raund) uchun: 2 — {b1.get('2',0)} ta kalitda, 3 — {b1.get('3',0)} ta kalitda; L⁸ uchun minimum 2 ({b8.get('2',0)} ta kalit), mediana 7–8. So‘ngra 1 dan 6 tagacha ketma-ket yutish qatlamidan o‘tuvchi izlar uchun minimal faol baytlar soni qidirildi (120 ta kalit, oxirgi qatlamda og‘irligi 1–2 bo‘lgan niqoblar). Natijalar va ulardan kelib chiqadigan korrelyatsiya chegaralari 7-jadvalda keltirilgan.")
rows=[["Qatlamlar soni","Faol baytlar: min / mediana","SBZ: log₂|c| (mediana)","SBZ: log₂|c| (eng yomon kalit)","Standart-256: log₂|c| (mediana)","Standart-128"]]
for k in range(1,7):
    v=L3[str(k)]; rows.append([str(k),f"{v['min']} / {fz(v['median'],1)}",f"≤ −{fz(6*v['median'],0)}",f"≤ −{6*v['min']}",f"≤ −{fz(2*v['median'],0)}","0"])
T([1400,1800,1550,1600,1650,1350],rows,"7-jadval. Yutish qatlamlari bo‘yicha faol baytlar va iz korrelyatsiyasining yuqori chegarasi")
IMG('/home/claude/ka/ch_lin.png',15.5,8.0,"1-rasm. Iz korrelyatsiyasi chegarasining yutish qatlamlari soniga bog‘liqligi")
P("Qatlamlar quyidagi tartibda keladi: 1-iteratsiyaning 0-, 8-, 9-nuqtalari, so‘ng 2-iteratsiyaning 0-, 8-, 9-nuqtalari. 4-qatlamda faol baytlar soni keskin oshadi (mediana 15), chunki iz L⁸ akslantirishi orqali o‘tadi va u niqobni ko‘p baytlarga tarqatadi. Eng yomon kalitlarda esa har bir qatlamda faqat bitta faol bayt qoladi; bu M(k₀) matritsasining degeneratsiyasi bilan bog‘liq.")
H2('1.5. SBZ ga bog‘liq bo‘lmagan qoldiq chiziqli munosabatlar')
P(f"10-raund (oxirgi) yutish nuqtasidan keyin keladi va unda Aralash bajariladi. Shuning uchun xesh qiymatning 0-qatlami L matritsasining aksi (obrazi) ichida yotadi: rang o‘rtacha {fz(L2['rank_L']['mean'],1)} bo‘lgani uchun chiqishning 0-qatlamida o‘rtacha ≈{fz(32-L2['rank_L']['mean'],1)} ta chiziqli munosabat c = 1 bilan bajariladi, L dagi nol satrlar esa doimiy bitlarni beradi (kalitlarning {fz(100*L2['zero_rows']['share_keys_with_zero_row'],1)} foizida). Bu munosabatlar biror yutish qatlamidan o‘tmaydi va BaytZichlash yoki SBZ tanloviga bog‘liq emas. Kalitsiz rejimda k ochiq bo‘lgani uchun ular hamma uchun ma’lum bo‘lib, to‘liq xesh uchun chiziqli farqlovchini beradi. Bu kamchilikni faqat Aralash/TuzilmaKalit o‘zgartirishlarini qayta loyihalash orqali bartaraf etish mumkin.")
H2('1.6. Chiziqli kriptotahlil bo‘yicha xulosa')
BL("Yutish nuqtasi bo‘lmagan raundlar (1–7, 10) 0- va 1-bit qatlamlarda c ≈ 1 bilan o‘tadi, ya’ni chiziqli bardoshlilikka hissa qo‘shmaydi; bu barcha variantlar uchun umumiy xossa.")
BL("Standart-128 da XOR tufayli 0-qatlam butun xesh davomida c = 1 bilan kuzatiladi; bu variant raundlar sonidan qat’i nazar chiziqli kriptotahlilga bardoshli emas.")
BL("Standart-256 da har bir faol bayt ≤ 2⁻² hissa qo‘shadi; 2⁻⁶⁴ chegarasiga mediana kalitlarda 5–6 yutish qatlamidan keyin (2-iteratsiyaning 8–9-raundi, umumiy hisobda ≈19-raund) erishiladi, eng yomon kalitlarda amalda erishilmaydi.")
BL("SBZ-256 da har bir faol bayt ≤ 2⁻⁶ hissa qo‘shadi; 2⁻⁶⁴ chegarasiga mediana kalitlarda 4 ta yutish qatlamidan keyin, ya’ni 1-iteratsiya va 2-iteratsiyaning 0-nuqtasidan so‘ng (≈11-raund) erishiladi; eng yomon kalitlarda 11 ta qatlam (≈4 ta iteratsiya) kerak bo‘ladi. SBZ-128 uchun 2⁻³² chegarasiga mediana bo‘yicha 4 ta, eng yomon holatda 6 ta qatlamdan keyin (2 ta iteratsiya, 20 raund) erishiladi.")
BL("Chiqish 0-qatlamidagi c = 1 munosabatlar (o‘rtacha ≈6 ta) SBZ ga bog‘liq emas va Aralash o‘zgartirishining 2 moduli bo‘yicha degeneratsiyasidan kelib chiqadi.")

# ---------------- 2. DIFFERENSIAL ----------------
PB(); H1('2. Differensial kriptotahlil')
H2('2.1. Asosiy tushunchalar')
P("Differensial kriptotahlilda buzg‘unchi kirish ayirmasi (orttirmasi) Δx = x ⊕ x′ ning akslantirishlar orqali ma’lum chiqish ayirmasiga Δy o‘tish ehtimolligidan foydalanadi. F akslantirish uchun *ayirmalar matritsasi* (DDT) elementlari:")
F("DDT_F(Δx, Δy) = #{ x : F(x) ⊕ F(x ⊕ Δx) = Δy },     p(Δx → Δy) = DDT_F(Δx, Δy) / 2ⁿ.")
P("Differensial iz ehtimolligi oraliq ehtimolliklar ko‘paytmasiga teng. Xesh funksiya uchun kolliziyaga bardoshlilik nuqtai nazaridan 256 bitli rejimda iz ehtimolligi 2⁻¹²⁸ dan, 128 bitli rejimda 2⁻⁶⁴ dan kichik bo‘lishi talab qilinadi. Algoritmda 2ⁿ moduli bo‘yicha amallar ishlatilgani uchun XOR-ayirmalar bilan birga eng katta bit (MSB) ayirmasi alohida ko‘riladi: x + 2ⁿ⁻¹ ≡ x ⊕ 2ⁿ⁻¹ (mod 2ⁿ) bo‘lgani uchun MSB ayirmasi modul arifmetikasida ko‘chirish hosil qilmaydi.")
H2('2.2. Akslantirishlarning ayirmalar matritsalari')
H3('2.2.1. AES S-box')
sd=D1['S_ddt_dist']
P(f"S ning 256×256 ayirmalar matritsasi to‘liq hisoblandi. Δx ≠ 0 satrlarida qiymatlar faqat 0, 2 va 4 ga teng: 0 — {sd['0']} ta, 2 — {sd['2']} ta, 4 — {sd['4']} ta element. Maksimal ehtimollik 4/256 = 2⁻⁶ (differensial bir xillik 4). Matritsaning bo‘lagi 8-jadvalda keltirilgan.")
db=EX['S_ddt_block']
T([1250]+[1012]*8,[["Δx \\ Δy"]+[f"{y:02X}" for y in range(8)]]+[[f"{d:02X}"]+[str(v) for v in db[d-1]] for d in range(1,9)],"8-jadval. S ayirmalar matritsasining bo‘lagi")
H3('2.2.2. Standart zichlash massivi Z (8 → 4)')
P(f"Z ning 256×16 ayirmalar matritsasida maksimal qiymat {D1['Z_ddt_max']}/256 = 0,156 bo‘lib, u Δx = 96 → Δy = 0 da erishiladi, ya’ni ayirma butunlay so‘nadi. 255 ta noldan farqli ayirmaning {D1['Z_vanish_count']} tasi musbat ehtimollik bilan so‘nishi mumkin. Lotin kvadrati tuzilishi tufayli faqat bitta yarim baytdagi ayirma hech qachon so‘nmaydi (DDT(80, 0) = DDT(01, 0) = 0). 9-jadvalda tipik satrlar keltirilgan.")
T([1100]+[515]*16,[["Δx \\ Δy"]+[f"{y:X}" for y in range(16)],["80"]+[str(v) for v in D1['Z_row_80']],["01"]+[str(v) for v in D1['Z_row_01']],["96"]+[str(v) for v in D1['Z_row_96']]],"9-jadval. Z ayirmalar matritsasining satrlari (×1/256)")
H3('2.2.3. XOR va SBZ')
P("XOR uchun Δy = Δh ⊕ Δn ehtimollik 1 bilan bajariladi; agar Δh = Δn bo‘lsa, ayirma ehtimollik 1 bilan so‘nadi. SBZ uchun chiqish ayirmasining taqsimoti aniq formula bilan ifodalanadi:")
F("P(Δy | Δh, Δn) = Σ_d DDT_S(Δn, d) · DDT_S(Δh ⊕ d, Δy) / 2¹⁶.")
P(f"Barcha (Δh, Δn, Δy) uchliklari bo‘yicha maksimum 2⁻⁶ ga teng. Δn = 0 bo‘lganda formula DDT_S(Δh, Δy)/256 ga, Δh = 0 bo‘lganda esa SBZ ning n bo‘yicha bijektivligi tufayli so‘nish ehtimolligi 0 ga aylanadi. Ba’zi xususiy qiymatlar: P(Δy | Δh = 0, Δn = 80) ≤ {fz(D1['SBZ_dn80_max'],4)} ≈ 2⁻⁷·⁸, P(Δy = 80 | Δh = 0, Δn = 80) = {fz(A3['SBZ_80to80'],4)} ≈ 2⁻⁷·⁹, ikkala argumentda 80 bo‘lganda so‘nish ehtimolligi {fz(D1['SBZ_both80_vanish'],4)} = 2⁻⁷.")
H3('2.2.4. Qo‘sh o‘zgartirishi')
pj=D1['Qosh_pj_best_mean']
P(f"Qo‘sh elementi (belgilangan parametrlarda) uchun ayirmalar matritsasining maksimal qiymati {D1['Qosh_ddt_max_max']}/256 bo‘lib, u 80 → 80 o‘tishda erishiladi. Haqiqatan, toq y uchun (y + 2ⁿ⁻¹)⁻¹ ≡ y⁻¹ + 2ⁿ⁻¹ (mod 2ⁿ), R juft bo‘lgani uchun R·2ⁿ⁻¹ ≡ 0, shuning uchun MSB ayirmasi har bir bosqichdan o‘zgarmay o‘tadi; faqat x⁻² ≡ 0 almashtirish nuqtasi (2/256) istisno. 10-jadvalda 2ʲ ko‘rinishidagi kirish ayirmalari uchun eng ehtimolli chiqish ayirmasi ehtimolligi keltirilgan.")
T([3100]+[780]*8,[["Kirish ayirmasi Δx = 2ʲ, j","0","1","2","3","4","5","6","7"],["Eng ehtimolli Δy ehtimolligi"]+[fz(v,3) for v in pj]],"10-jadval. Qo‘sh elementining ayirmalar o‘tkazish ehtimolliklari (200 ta parametrlar to‘plami)")
P("T-funksiya xossasi tufayli j-bitdagi ayirma faqat j va undan yuqori bitlarga ta’sir qiladi; quyi bitdagi ayirma esa ko‘chirishlar orqali barcha yuqori bitlarga tarqaladi (Δx = 01 uchun eng ehtimolli chiqish ehtimolligi atigi 0,12). Massiv darajasida bitta elementdagi MSB ayirmasi J yig‘indisini 2ⁿ⁻¹ ga o‘zgartiradi, bu boshqa massivning barcha A parametrlarini 2ⁿ⁻¹ ga siljitadi va ikkinchi massivning toq elementlarida MSB ayirmasini paydo qiladi. Juft sondagi MSB ayirmalari esa yig‘indini o‘zgartirmaydi va faqat o‘z pozitsiyalarida qoladi.")
H3('2.2.5. Aralash, SurHolat, SurKalit, TuzilmaKalit')
P("Aralash belgilangan kₑ uchun Z/2ⁿ ustida chiziqli bo‘lgani uchun modul ayirmalari uchun aniq chiziqli: Δh′ = Aralash(Δh, kₑ). MSB ayirmasi uchun 2ⁿ⁻¹·kₑ ≡ 2ⁿ⁻¹·(kₑ mod 2), ya’ni MSB ayirmalari 0-qatlamdagi bilan bir xil M(k₀) matritsasi orqali ehtimollik 1 bilan tarqaladi: Δh′_MSB = M(k₀)·Δh_MSB. Agar ayirma vektori M(k₀) ning yadrosida bo‘lsa, u ehtimollik 1 bilan so‘nadi. Tasodifiy kalitlarning " + fz(100*A3['keys_zero_col'],0) + " foizida M da nol ustun, " + fz(100*A3['keys_equal_cols'],0) + " foizida teng ustunlar juftligi mavjud. SurHolat va SurKalit ayirmalarni pozitsiyalar bo‘yicha ko‘chiradi (ehtimollik 1), TuzilmaKalit faqat raund kalitiga ta’sir qiladi va kₑ dagi MSB ayirmasini o‘zgartirmaydi.")
H2('2.3. Orttirmalarning raundlar orqali o‘tishi')
P("Ayirmalarning raundlar orqali o‘tishi haqiqiy algoritmda kuzatildi. Birinchi tajribada (D0) 0-nuqtadagi yutishdan keyingi holatning bitta baytiga MSB ayirmasi kiritildi va har bir raund oxirida MSB izining saqlanish ehtimolligi (barcha ayirmalar faqat MSB da), holat va kₑ dagi faol elementlar soni o‘lchandi (har bir variantda 3000 juftlik).")
def rowsD0(key):
    return [r for r in D3[key] if r['op']=='Tuz']
rr=[["Raund j"]+[str(j) for j in range(1,11)]]
for key,lab in [('256_std_D0a','Standart-256: P(MSB izi)'),('256_sbz_D0a','SBZ-256: P(MSB izi)'),('256_sbz_D0a#','SBZ-256: faol baytlar'),('16_std_D0a','Standart-128: P(MSB izi)'),('16_sbz_D0a','SBZ-128: P(MSB izi)'),('16_sbz_D0a#','SBZ-128: faol yarim baytlar')]:
    if key.endswith('#'): rr.append([lab]+[fz(r['act'],1) for r in rowsD0(key[:-1])])
    else: rr.append([lab]+[fz(r['msb'],3) for r in rowsD0(key)])
T([2850]+[650]*10,rr,"11-jadval. Bitta MSB ayirmasining raundlar orqali o‘tishi (8- va 9-raundlarda yutish)")
IMG('/home/claude/ka/ch_dif.png',15.5,7.1,"2-rasm. MSB izining saqlanish ehtimolligi va faol elementlar soni (8–9-raundlar — yutish nuqtalari)")
P("256 bitli rejimda MSB izi 1–7-raundlardan har raundda ≈0,85–0,94 ehtimollik bilan o‘tadi: yetti raunddan keyingi umumiy ehtimollik 0,34 ≈ 2⁻¹·⁶ ga teng. Bu raundlar differensial kriptotahlilga deyarli qarshilik ko‘rsatmaydi. 128 bitli rejimda Δ = 10 tuzatmasi va nol almashtirish shartlari tez-tez ishlagani uchun iz tezroq buziladi (1-raunddan keyin 0,48). 8-raunddagi yutishda MSB izi to‘liq buziladi; qolgan ≈3,3% juftliklar 1-raundning Aralash o‘zgartirishida ayirmasi butunlay so‘ngan (ichki kolliziya) juftliklardir. Bu hodisa 2.4-bo‘limda tahlil qilinadi.")
P("Har bir akslantirishning orttirmalarga ta’sirini aniqroq ko‘rish uchun 1- va 2-raundlar ichidagi har bir akslantirishdan keyingi holat o‘lchandi (20-jadval). Aralash bitta MSB ayirmasini M(k₀) ustunidagi birlar soniga teng (o‘rtacha 3 ta) baytga ehtimollik 1 bilan tarqatadi. Birinchi Qo‘sh(holat, kₑ) toq sondagi faol elementlar J yig‘indisini o‘zgartirgani uchun ayirmani kₑ massiviga ham o‘tkazadi; ikkinchi Qo‘sh da esa ayirmalarning bir qismi juft sonli bo‘lib qolgani uchun faol elementlar soni kamayadi. SurHolat va SurKalit faol elementlar sonini o‘zgartirmaydi, TuzilmaKalit esa MSB ayirmasiga ta’sir qilmaydi.")
def opsRow(key,j,lab):
    rs=[r for r in D3[key] if r['j']==j]
    return [lab]+[f"{fz(r['act'],1)} / {fz(r['actk'],1)}; {fz(r['msb'],2)}" for r in rs]
rr=[["Variant, raund","Aralash","Qo‘sh(holat, kₑ)","SurHolat, SurKalit","Qo‘sh(holat, kₑ)","TuzilmaKalit"]]
for key,lab in [('256_sbz_D0a','SBZ-256'),('16_sbz_D0a','SBZ-128')]:
    for j in (1,2): rr.append(opsRow(key,j,f"{lab}, j = {j}"))
T([1750,1520,1520,1520,1520,1520],rr,"20-jadval. Akslantirishlardan keyingi faol elementlar (holat / kₑ) va MSB izining saqlanish ehtimolligi")
P("Ikkinchi tajribada (D2) kirish blokining ikkita baytiga MSB ayirmasi kiritildi; bunday ayirma J yig‘indisini o‘zgartirmaydi va kolliziya hujumlarining odatiy boshlang‘ich nuqtasi hisoblanadi (2000 juftlik).")
def d2(key,op,j=None):
    for r in D2[key]:
        if r['op']==op and (j is None or r['j']==j): return r
rr=[["Variant","Qo‘sh (0-nuqta)","Yutish (0-nuqta)","1-raund","2-raund","7-raund","8-raund yutishi","9-raund yutishi"]]
for key,lab in [('256_std_D2','Standart-256'),('256_sbz_D2','SBZ-256'),('16_std_D2','Standart-128'),('16_sbz_D2','SBZ-128')]:
    r0=d2(key,'Qosh0'); rb=d2(key,'BZ0'); r1=d2(key,'Tuz',1); r2=d2(key,'Tuz',2); r7=d2(key,'Tuz',7); r8=d2(key,'BZ8'); r9=d2(key,'BZ9')
    rr.append([lab,f"{fz(r0['act'],0)} / p={fz(r0['top'],2)}",f"{fz(rb['act'],1)} / p≈{fz(rb['top'],4)}",fz(r1['act'],1),fz(r2['act'],1),fz(r7['act'],1),fz(r8['act'],1),fz(r9['act'],1)])
T([1600,1300,1450,900,900,900,1150,1150],rr,"12-jadval. Kirish blokidagi ikki baytli MSB ayirmasi: faol elementlar soni va eng ehtimolli ayirma ehtimolligi p")
P("Qo‘sh (0-nuqta) bu ayirmani ehtimollik 1 bilan holatga ta’sir qilmasdan o‘tkazadi va u yutish nuqtasiga holatn dagi ikki baytli MSB ayirmasi sifatida yetib keladi. Standart-128 da XOR uni deyarli o‘zgarishsiz holatga kiritadi (p ≈ 0,79). Standart-256 da Z ikkala baytda past ehtimollik bilan aniqlangan quyi yarim bayt ayirmasini beradi (o‘lchangan p ≈ 0,0135, nazariy (26/256)² ≈ 2⁻⁶·⁶). SBZ da esa har bir bayt uchun P ≤ 2⁻⁷·⁸, ikki bayt uchun ≈2⁻¹⁵·⁶ (o‘lchangan qiymat tanlanmaning sezgirlik chegarasida). Bir raunddan keyin barcha variantlarda ayirma 17–31 ta elementga tarqaladi.")
P("Uchinchi tajribada (D1) ayirma iteratsiya boshidagi holatga, ya’ni 0-nuqtadagi yutishdan oldin kiritildi. Bu holat oldingi blokni qayta ishlash natijasidagi farqqa mos keladi. 23-jadvalda ayirmaning 0-nuqtadagi Qo‘sh va yutish o‘zgartirishlaridan, so‘ngra raundlardan o‘tishi, shuningdek 10-raunddan keyingi Xemming masofasi keltirilgan (ideal qiymat: 256 bitli rejimda 128, 128 bitli rejimda 64 bit).")
rr=[["Variant","Qo‘sh: faol el. / P(MSB)","Yutish: faol el. / Xemming","1-raund: faol el.","10-raund: faol el. / Xemming"]]
for key,lab in [('256_std_D1','Standart-256'),('256_sbz_D1','SBZ-256'),('16_std_D1','Standart-128'),('16_sbz_D1','SBZ-128')]:
    q=d2(key,'Qosh0'); b=d2(key,'BZ0'); r1=d2(key,'Tuz',1); r10=d2(key,'Tuz',10)
    rr.append([lab,f"{fz(q['act'],1)} / {fz(q['msb'],2)}",f"{fz(b['act'],1)} / {fz(b['hd'],1)}",fz(r1['act'],1),f"{fz(r10['act'],1)} / {fz(r10['hd'],1)}"])
T([1750,1950,1950,1700,2000],rr,"23-jadval. Iteratsiya boshidagi holatdagi bitta MSB ayirmasining tarqalishi (2000 juftlik)")
P("Jadvaldan ko‘rinadiki, holatdagi bitta MSB ayirmasi Qo‘sh o‘zgartirishining o‘zaro bog‘lanishi (J yig‘indilari) orqali 0-nuqtadayoq holat va holatn massivlarining yarmiga tarqaladi. SBZ yutishdan keyin Xemming masofasini Standart-256 dagi 71 bitdan 99 bitgacha, 128 bitli rejimda 31 bitdan 62 bitgacha oshiradi, ya’ni yutish nuqtasining o‘zidayoq ayirma deyarli to‘liq «ko‘chki» holatiga keladi. Standart-128 da 10-raunddan keyingi Xemming masofasi 47 bit bo‘lib, ideal 64 bitdan sezilarli kichik qoladi; bu XOR bilan bog‘liq bit-qatlam ajralishining natijasidir.")
H2('2.4. Optimal orttirmalar')
P("Buzg‘unchi uchun eng foydali izlar quyidagi uch turdagi bo‘g‘inlardan tuziladi.")
BL("*T-funksiyali raundlardagi MSB izlari.* 1–7-raundlarda MSB ayirmalari M(k₀) orqali chiziqli tarqaladi va har raundda ≈0,85–0,94 ehtimollik bilan saqlanadi; bu bo‘g‘inlar izning umumiy ehtimolligini atigi ≈2⁻¹·⁶ ga kamaytiradi.")
BL("*Yutish nuqtalari.* Faol bayt boshiga eng yaxshi ehtimollik: XOR — 1; Z — 0,156 (2⁻²·⁷), tasodifiy ayirma uchun so‘nish ehtimolligi o‘rtacha 2⁻⁴; SBZ — 2⁻⁶, faqat bitta argumentdagi ayirma uchun so‘nish mumkin emas. Shunday qilib, SBZ holatdagi ayirmani (Δn = 0) kirish bloki yordamida «o‘chirish» imkoniyatini to‘liq yo‘q qiladi.")
BL("*Aralash yadrosi orqali so‘nish.* Agar yutishdan keyingi ayirma M(k₀) ning yadrosidagi MSB ayirmasi bo‘lsa, u keyingi Aralash da ehtimollik 1 bilan so‘nadi. Tajribada bitta tasodifiy pozitsiyadagi MSB ayirmasi 3,1% (p = 256) va 3,3% (p = 16) hollarda 1-raunddayoq butunlay yo‘qoldi. SBZ da bunday ayirmani kirish blokidan hosil qilish ehtimolligi bir bayt uchun ≈2⁻⁷·⁹.")
P("Bu bo‘g‘inlardan ko‘rinadiki, optimal iz yutish nuqtalarida imkon qadar kam faol bayt bilan o‘tishi kerak. 1–7-raundlardan keyin MSB izi ham holatning 25–27 ta baytiga tarqalgan bo‘ladi (11-jadval), shuning uchun 8-raunddagi yutishda faol baytlar soni amalda 27–32 ni tashkil qiladi.")
H3('2.4.1. Kolliziya izini qurish')
P("Kolliziya hujumida buzg‘unchi ikki xil xabar uchun bir xil xesh qiymat olishga harakat qiladi. Bitta blokdagi ayirma o‘sha blok uchun uch marta (0-, 8- va 9-nuqtalarda) holatga kiritiladi, shuning uchun to‘liq kolliziya izi quyidagi bosqichlardan iborat bo‘lishi kerak: (1) 0-nuqtada kirish blokidagi ayirma holatga o‘tadi; (2) 1–7-raundlar va 8-raundning boshida holatdagi ayirma shunday shaklga kelishi kerakki, 8-nuqtada yana kiritilgan blok ayirmasi bilan birgalikda u so‘nsin; (3) xuddi shu shart 9-nuqtada ham bajarilishi kerak; (4) uzunlik va NY bloklari ham bir xil bo‘lishi kerak.")
P("SBZ da (2)-bosqich jiddiy cheklanadi: n bo‘yicha bijektivlik tufayli Δn = 0 bo‘lgan baytdagi holat ayirmasi hech qachon so‘nmaydi, Δn ≠ 0 bo‘lgan baytda esa so‘nish uchun Δh = S(n) ⊕ S(n ⊕ Δn) tengligi talab qilinadi (ehtimollik ≤ 2⁻⁶). Demak, 8-nuqtaga kelganda holat ayirmasi faqat kirish blokidagi faol pozitsiyalarda bo‘lishi kerak. Tajribada SBZ-256 da ikki baytli MSB ayirmasi bilan boshlangan 2000 juftlikning birortasida ham 7-raunddan keyin faol baytlar soni 29 dan kam bo‘lmadi. Standart-256 da esa Δn = 0 bo‘lgan baytdagi holat ayirmasi Z(h) da 0,156 gacha (tasodifiy ayirma uchun o‘rtacha 2⁻⁴) ehtimollik bilan so‘nishi mumkin, Standart-128 da esa Δh = Δn bo‘lganda XOR ayirmani ehtimollik 1 bilan so‘ndiradi.")
H2('2.5. Bardoshlilik bahosi')
rr=[["Variant","Faol bayt boshiga maks. p","8-raund yutishida (≈27 faol bayt)","8- va 9-raundlar (≈27 + 31)","Talab","Xulosa"]]
rr.append(["Standart-128","1 (XOR)","≈ 1","≈ 1","2⁻⁶⁴","bardoshli emas"])
rr.append(["SBZ-128","2⁻⁶","≤ 2⁻⁹⁰ (≈15 bayt)","≤ 2⁻¹⁸⁰","2⁻⁶⁴","8-raunddan keyin"])
rr.append(["Standart-256","2⁻²·⁷","≤ 2⁻⁷²","≤ 2⁻¹⁵⁶","2⁻¹²⁸","9-raunddan keyin"])
rr.append(["SBZ-256","2⁻⁶","≤ 2⁻¹⁶²","≤ 2⁻³⁴⁸","2⁻¹²⁸","8-raunddan keyin"])
T([1650,1500,1700,1600,1100,1800],rr,"13-jadval. Birinchi iteratsiyadagi differensial iz ehtimolligining yuqori chegaralari")
P("Jadvaldagi chegaralar «har bir faol bayt uchun eng yaxshi ehtimollik» qoidasi bilan olingan va izlar ichidagi bog‘liqliklarni hisobga olmaydi, shuning uchun ular yuqori chegaralar hisoblanadi. Shunga qaramay, ular asosiy farqni aniq ko‘rsatadi: SBZ-256 da birinchi iteratsiyaning 8-raundidayoq ehtimollik 2⁻¹²⁸ dan kichik bo‘ladi; Standart-256 da bunga faqat 9-raunddagi ikkinchi yutishdan keyin erishiladi; Standart-128 da yutish qatlami differensial qarshilik bermaydi va bardoshlilik faqat T-funksiyali raundlarga tayanadi, ular esa MSB izlariga deyarli qarshilik ko‘rsatmaydi.")
H2('2.6. Differensial kriptotahlil bo‘yicha xulosa')
BL("1–7- va 10-raundlar MSB izlarini ≈0,85–0,94 ehtimollik bilan o‘tkazadi; differensial bardoshlilik faqat yutish nuqtalarida hosil bo‘ladi.")
BL("SBZ yutish nuqtasidagi maksimal ehtimollikni 0,156 (Standart-256) va 1 (Standart-128) dan 2⁻⁶ gacha kamaytiradi va bitta argumentdagi ayirmaning so‘nishini imkonsiz qiladi.")
BL("SBZ-256 va SBZ-128 birinchi iteratsiyaning 8-raundidan keyin differensial chegaraga (mos ravishda 2⁻¹²⁸ va 2⁻⁶⁴) erishadi; Standart-256 — 9-raunddan keyin; Standart-128 esa raundlar sonidan qat’i nazar bardoshli emas.")
BL("Aralash yadrosi orqali ayirmaning ehtimollik 1 bilan so‘nishi SBZ ga bog‘liq bo‘lmagan qoldiq xavf hisoblanadi; uni bartaraf etish uchun Aralash/TuzilmaKalit o‘zgartirishlarini qayta ko‘rib chiqish talab qilinadi.")

# ---------------- 3. ALGEBRAIK ----------------
PB(); H1('3. Algebraik kriptotahlil')
H2('3.1. Asosiy tushunchalar')
P("Algebraik kriptotahlilda algoritm noma’lum bitlar (kalit yoki xabar) ga nisbatan GF(2) maydoni (yoki Z/2ⁿ halqasi) ustidagi tenglamalar tizimi ko‘rinishida ifodalanadi va tizim yechiladi. Hujum murakkabligi tenglamalarning darajasi, o‘zgaruvchilar soni va tizimning siyrakligiga bog‘liq. Linearizatsiya usulida d-darajali tizim har bir monomni yangi o‘zgaruvchi deb hisoblash orqali chiziqli tizimga keltiriladi; uning murakkabligi taxminan:")
F("C(n, d) ≈ ( Σ_{i=0..d} binom(n, i) )^ω,     ω ≈ 2,8,")
P("bu yerda n — noma’lum bitlar soni. Har bir akslantirish uchun *oshkor* (y = f(x)) va *implitsit* (g(x, y) = 0) tenglamalar ko‘riladi. Implitsit kvadrat tenglamalar soni barcha (x, y) juftliklari bo‘yicha 1, xᵢ, yⱼ, xᵢxⱼ, xᵢyⱼ, yᵢyⱼ monomlari matritsasining rangi orqali aniq hisoblandi.")
H2('3.2. Akslantirishlar uchun algebraik tenglamalar')
H3('3.2.1. AES S-box va SBZ')
P(f"S akslantirish GF(2⁸) maydonida x·y = 1 (x ≠ 0) tenglamasi bilan ifodalanadi. Bit darajasida u 16 ta o‘zgaruvchiga nisbatan {A1['S_quad'][0]} ta chiziqli bog‘liq bo‘lmagan kvadrat implitsit tenglamani qanoatlantiradi (137 ta monomdan); har bir chiqish bitining ANF darajasi {A1['S_deg'][0]} ga teng. SBZ uchun oraliq o‘zgaruvchilar kiritiladi:")
F("u = S(n),     v = h ⊕ u,     y = S(v).")
P(f"Natijada har bir bayt uchun 16 ta yangi o‘zgaruvchi (u, y), 8 ta chiziqli tenglama (v) va 2 × 39 = 78 ta kvadrat tenglama hosil bo‘ladi. Oraliq o‘zgaruvchilarsiz SBZ 24 ta o‘zgaruvchiga nisbatan birorta ham kvadrat implitsit tenglamaga ega emas ({A1['SBZ_quad'][0]} / {A1['SBZ_quad'][1]}), har bir chiqish bitining ANF darajasi {A1['SBZ_deg'][0]} ga teng (16 ta o‘zgaruvchidan).")
H3('3.2.2. Standart zichlash massivi va XOR')
P(f"Z jadvali (8 → 4) uchun kvadrat implitsit tenglamalar yo‘q ({A1['Z_quad'][0]} / {A1['Z_quad'][1]}), kub darajali implitsit tenglamalar soni {A1['Z_cubic'][0]} ta ({A1['Z_cubic'][1]} ta monomdan), oshkor tenglamalar darajasi {A1['Z_deg'][0]}. Standart-256 dagi BaytZichlash (16 → 8) uchun ham kvadrat implitsit tenglamalar yo‘q, chiqish bitlarining darajasi {A1['BZ256_deg'][0]}. 128 bitli rejimdagi XOR esa chiziqli tenglamalar bilan ifodalanadi: yᵢ = hᵢ ⊕ nᵢ (daraja 1).")
H3('3.2.3. Qo‘sh o‘zgartirishi')
P("Z/2ⁿ halqasi ustida Qo‘sh o‘zgartirishining har bir bosqichi bitta element uchun quyidagi tenglamalar bilan ifodalanadi (t = 1, 2, 3 — bosqich raqami, x⁽⁰⁾ = x):")
F("x⁽ᵗ⁾ · (B_t + R · x⁽ᵗ⁻¹⁾) + A_t · x⁽ᵗ⁻¹⁾ ≡ 0 (mod 2ⁿ),")
F("A₁ = J₁′ + 2·x′ + Δ,   B₁ = K₁ − 2·x,   J₁ = Σ x,   K₁ = Π (x | 1) + Δ′,")
P("bu yerda shtrixli kattaliklar ikkinchi massivga tegishli, (x | 1) — elementning 0-bitini 1 ga tenglashtirish (bit darajasida chiziqli amal), Δ va Δ′ — J yig‘indisining juftligi va K ning ±(J′+1) bilan tengligiga bog‘liq tuzatmalar. 2- va 3-bosqichlarda A₂ = J₁′ + J₂′ + 2·x′⁽¹⁾ + Δ, B₂ = K₁·K₂ − 2·x⁽¹⁾ ishlatiladi. Har bir element tenglamasi x⁽ᵗ⁾ va x⁽ᵗ⁻¹⁾ ga nisbatan kvadrat, lekin A, B parametrlari orqali massivning barcha elementlari bilan bog‘langan; K ko‘paytmasi 31 ta ketma-ket ko‘paytirish zanjirini talab qiladi.")
qd=EX['Qosh_deg_median']
P(f"Bitta element nuqtai nazaridan (parametrlar belgilangan) Qo‘sh algebraik jihatdan juda zaif: 16 ta o‘zgaruvchiga nisbatan {A1['Qosh_quad'][0]} ta kvadrat implitsit tenglama mavjud (S da 39 ta). Chiqish bitlarining ANF darajalari (50 ta parametrlar to‘plami bo‘yicha mediana) j = 0…7 uchun: {', '.join(str(int(v)) for v in qd)}. 0-bit chiziqli, j ≥ 2 bitlar uchun daraja j ga yaqin, bu T-funksiya xossasiga mos keladi; 1-bit darajasining 8 ga yetishi nol almashtirish nuqtasi (bitta kirish) bilan bog‘liq.")
T([2880]+[808]*8,[["Chiqish biti j","0","1","2","3","4","5","6","7"],["ANF darajasi: minimum"]+[str(v) for v in A1['Qosh_deg_min']],["ANF darajasi: mediana"]+[str(int(v)) for v in EX['Qosh_deg_median']],["ANF darajasi: maksimum"]+[str(v) for v in A1['Qosh_deg_max']]],"21-jadval. Qo‘sh elementi chiqish bitlarining algebraik darajalari (8 ta kirish bitiga nisbatan)")
H3('3.2.4. Aralash, SurHolat, SurKalit, TuzilmaKalit')
P("Aralash uchun Z/2ⁿ ustida har bir chiqish elementi uchun bitta bichiziqli tenglama yoziladi (chap yarim, s, u ∈ {0,1,2,3}):")
F("h′[u,u] = h[u,u]·Σᵢ kₑ[i,u] − Σ_{i≠u} h[i,i]·kₑ[i,u],")
F("h′[s,u] = h[s,u]·Σᵢ kₑ[i,u] + kₑ[s,u]·Σᵢ h[i,u] − Σ_{i≠s,u} h[s,i]·kₑ[i,u]   (s ≠ u).")
P("Ma’lum kₑ da bu tenglamalar h ga nisbatan chiziqli, kalit noma’lum bo‘lganda esa (h, kₑ) ga nisbatan kvadrat. Bit darajasida j-bit ko‘chirishlar tufayli j + 1 dan oshmaydigan darajaga ega, 0-qatlam esa chiziqli. SurHolat va SurKalit — o‘zgaruvchilarni qayta nomlash (tenglama talab qilinmaydi). TuzilmaKalit uchun kₑ ≠ 0 bo‘lganda kₑ′ = kₑ − (kₑ₀ ⊕ k₀) (mod 2ⁿ), kₑ = 0 va k₀ = 0 bo‘lganda kₑ′ = 2 tenglamalari o‘rinli.")
H3('3.2.5. Bit darajasidagi tenglamalar soni')
P("Tenglamalar sonini baholash uchun quyidagi model qabul qilindi: n bitli modul qo‘shish — 2n − 1 o‘zgaruvchi va tenglama (shulardan n − 1 tasi ko‘chirish uchun kvadrat); n bitli modul ko‘paytirish — n(n+1)/2 qisman ko‘paytma va n − 1 ta qo‘shish (n = 8 da 141 o‘zgaruvchi, shulardan 85 tasi kvadrat tenglama bilan); modul bo‘yicha teskarilash y·d = 1 ko‘paytirish tenglamasi bilan; S jadvali — 39 ta kvadrat tenglama.")
E=A3['eq']
def tr(lab,key): return [lab,f"{E[key][0]:,}".replace(',',' '),f"{E[key][1]:,}".replace(',',' '),f"{E[key][2]:,}".replace(',',' ')]
rr=[["Akslantirish (256 bitli rejim)","O‘zgaruvchilar","Tenglamalar","Shundan nochiziqli"]]
e=E['256_sbz']; es=E['256_std']
for lab,a in [("Qo‘sh (ikki massiv, 3 bosqich)",e['qosh']),("Aralash",e['aralash']),("TuzilmaKalit",e['tuzilma']),("SBZ (32 bayt)",e['bz']),("BaytZichlash Z (64 jadval)",es['bz']),("Raund (yutishsiz)",e['raund'])]:
    rr.append([lab]+[f"{v:,}".replace(',',' ') for v in a])
T([3900,1800,1800,1850],rr,"14-jadval. 256 bitli rejimdagi akslantirishlar uchun bit darajasidagi tenglamalar soni (baho)")
P("Jadvaldan ko‘rinadiki, tenglamalar tizimining hajmini asosan Qo‘sh o‘zgartirishi belgilaydi (raunddagi o‘zgaruvchilarning ≈91 foizi). SBZ tizimga bor-yo‘g‘i 512 ta o‘zgaruvchi va 2496 ta kvadrat tenglama qo‘shadi, lekin ular algoritmdagi yagona yuqori darajali (13-daraja) bo‘g‘inni tashkil qiladi.")
H2('3.3. Raund tenglamalari va 2–3 raund uchun tizimlar')
P("Bitta raund (yutishsiz) uchun tenglamalar tizimi akslantirishlar tenglamalarini ketma-ket birlashtirish orqali hosil qilinadi. j-raund kirishidagi (h⁽ʲ⁻¹⁾, kₑ⁽ʲ⁻¹⁾) va chiqishidagi (h⁽ʲ⁾, kₑ⁽ʲ⁾) massivlari orqali raund tenglamalari quyidagicha yoziladi:")
F("a = Aralash(h⁽ʲ⁻¹⁾, kₑ⁽ʲ⁻¹⁾);   (b, c) = Qo‘sh(a, kₑ⁽ʲ⁻¹⁾);   b′ = P·b,  c′ = Q·c;")
F("(h⁽ʲ⁾, d) = Qo‘sh(b′, c′);   kₑ⁽ʲ⁾ = TuzilmaKalit(d, k),")
P("bu yerda P va Q — SurHolat va SurKalit o‘rin almashtirishlari, Qo‘sh(·,·) — 3.2.3-banddagi tenglamalar. 8- va 9-raundlarda bunga yutish tenglamalari qo‘shiladi: (h̃, ñ) = Qo‘sh(h, blok), h = SBZ(h̃, ñ). 2 va 3 raund uchun tizimlar raund tenglamalarini h⁽ʲ⁾ va kₑ⁽ʲ⁾ umumiy o‘zgaruvchilari orqali zanjirlash bilan olinadi. Tizimlar hajmi 15-jadvalda keltirilgan (1-raund — 0-nuqtadagi yutish va bitta raund).")
rr=[["Variant","1 raund: o‘zg. / tengl.","2 raund: o‘zg. / tengl.","3 raund: o‘zg. / tengl."]]
for key,lab in [('256_std','Standart-256'),('256_sbz','SBZ-256'),('128_std','Standart-128'),('128_sbz','SBZ-128')]:
    rr.append([lab]+[f"{E[key][r][0]:,} / {E[key][r][1]:,}".replace(',',' ') for r in ('r1','r2','r3')])
T([2050,2450,2450,2400],rr,"15-jadval. 1, 2 va 3 raund uchun bit darajasidagi tenglamalar tizimlari hajmi")
e=E['256_sbz']
rr=[["Tizim qismi (SBZ-256, 2 raund)","O‘zgaruvchilar","Tenglamalar","Darajasi"]]
rr.append(["0-nuqta: Qo‘sh(holat, blok)",f"{e['qosh'][0]:,}".replace(',',' '),f"{e['qosh'][1]:,}".replace(',',' '),"2"])
rr.append(["0-nuqta: SBZ (32 bayt)",f"{e['bz'][0]:,}".replace(',',' '),f"{e['bz'][1]:,}".replace(',',' '),"2 (oraliq o‘zg. bilan)"])
for j in (1,2):
    rr.append([f"{j}-raund: Aralash",f"{e['aralash'][0]:,}".replace(',',' '),f"{e['aralash'][1]:,}".replace(',',' '),"2"])
    rr.append([f"{j}-raund: 2 × Qo‘sh(holat, kₑ)",f"{2*e['qosh'][0]:,}".replace(',',' '),f"{2*e['qosh'][1]:,}".replace(',',' '),"2"])
    rr.append([f"{j}-raund: SurHolat, SurKalit, TuzilmaKalit",f"{e['tuzilma'][0]:,}".replace(',',' '),f"{e['tuzilma'][1]:,}".replace(',',' '),"1–2"])
rr.append(["Jami",f"{e['r2'][0]:,}".replace(',',' '),f"{e['r2'][1]:,}".replace(',',' '),"—"])
T([3950,1800,1800,1800],rr,"22-jadval. SBZ-256 uchun 2 raundli tenglamalar tizimining tarkibi")
P("Tizim hajmi bo‘yicha variantlar deyarli farq qilmaydi; asosiy farq yutish nuqtasidagi tenglamalar darajasida. Standart-128 da 0-nuqtadagi yutish va undan keyingi raundlarning 0-qatlami to‘liq chiziqli bo‘lib qoladi: Aralash ning 0-qatlami chiziqli, Qo‘sh va SurHolat juftlikni saqlaydi, XOR chiziqli. Natijada 3 raund va undan ko‘p raund uchun ham 0-qatlam tenglamalari h₀⁽ʲ⁾ = L·h₀⁽ʲ⁻¹⁾ ⊕ blok₀ ko‘rinishidagi chiziqli tizimni tashkil qiladi. SBZ variantida esa 0-qatlam har bir yutishda S∘(⊕)∘S kompozitsiyasidan o‘tadi va tenglamalar darajasi 13 gacha ko‘tariladi.")
H2('3.4. Raundlar bo‘yicha algebraik darajaning o‘sishi')
P("Raundlar soni ortishi bilan darajaning o‘sishi kub testlari yordamida tekshirildi. Xabarning dastlabki 16 bitidan tasodifiy d ta bit tanlanadi, qolgan bitlar belgilanadi va 2ᵈ ta qiymat bo‘yicha r raunddan keyingi holat bitlarining XOR yig‘indisi hisoblanadi. Agar bitning darajasi d dan kichik bo‘lsa, yig‘indi doim 0 ga teng. 4 ta tasodifiy kub uchun yig‘indisi doim nol bo‘lgan bitlar ulushi o‘lchandi: yuqori darajali (tasodifiy) funksiya uchun kutilgan qiymat 1/16 ≈ 0,06.")
def cubeRow(key,lab,lay=False):
    row=A2[key]
    return [lab]+[fz((row[str(d)][1][0] if lay else row[str(d)][0]),2) for d in (2,4,6,8,10,12)]
rr=[["Variant, raund r","d = 2","d = 4","d = 6","d = 8","d = 10","d = 12"]]
for p,lab in [('256_std','Standart-256'),('256_sbz','SBZ-256')]:
    for r in (0,1,3): rr.append(cubeRow(f'{p}_r{r}',f"{lab}, r = {r}"))
for p,lab in [('16_std','Standart-128'),('16_sbz','SBZ-128')]:
    for r in (0,1,3): rr.append(cubeRow(f'{p}_r{r}',f"{lab}, r = {r} (0-qatlam)",True))
T([3150,1030,1030,1030,1030,1030,1030],rr,"16-jadval. Kub testlari: yig‘indisi doim nol bo‘lgan chiqish bitlari ulushi")
P("256 bitli rejimda r ≥ 1 raunddan keyin ikkala variantda ham ulush tasodifiy funksiya darajasida (0,04–0,14), ya’ni xabarning 16 biti bo‘yicha daraja 12 dan oshadi. r = 0 da (faqat yutish) Standart-256 da d = 12 uchun ulush 0,84 ga yetadi, bu Z ning 6-darajasi va bayt bo‘yicha lokalligi bilan bog‘liq; SBZ-256 da bu ulush 0,30. Standart-128 da 0-qatlam barcha d va r uchun 1,00 ga teng: bu qatlam xabar bitlariga nisbatan chiziqli bo‘lib qoladi. SBZ-128 da 0-qatlam ulushi d ortishi bilan ko‘tariladi va r = 1–3 da d = 12 uchun 0,75–0,78 ga yetadi. Demak, bu qatlam darajasi 12 atrofida chegaralangan: 1–3-raundlarda u yutish chiqishlarining chiziqli funksiyasi bo‘lib qoladi, yutish chiqishining har bir bayti esa ko‘pi bilan 13-darajali. Bu daraja 128 bitli rejim uchun talab qilinadigan qiymatdan (3.6-bo‘lim) ancha yuqori.")
H2('3.5. Hujum namoyishi: 0-qatlamni linearizatsiya qilish')
P("3.3-bo‘lim natijasini amaliy tekshirish uchun buzg‘unchi modeli quyidagicha tanlandi: kalitli rejimda kalit noma’lum, buzg‘unchi bir blokli xabarlar uchun xesh qiymatlarni oladi. U chiqishning 0-qatlamini xabar 0-qatlamining affin funksiyasi deb faraz qiladi: o₀ = A·m₀ ⊕ c (32 × 33 noma’lum koeffitsiyent) va ularni 80 ta xabar bo‘yicha Gauss usulida topadi. So‘ngra 300 ta yangi xabar uchun chiqish 0-qatlamini bashorat qiladi.")
rr=[["Variant","32 bitning hammasi to‘g‘ri bashorat qilingan xabarlar ulushi","Bitlar bo‘yicha to‘g‘ri bashorat ulushi"]]
for key,lab in [('16_std','Standart-128'),('16_sbz','SBZ-128'),('256_std','Standart-256'),('256_sbz','SBZ-256')]:
    rr.append([lab,fz(A3[key]['full_vec'],3),fz(A3[key]['per_bit'],3)])
T([2600,3700,3050],rr,"17-jadval. Chiqish 0-qatlamining affin modelini qurish natijasi (80 ta o‘quv, 300 ta sinov xabari)")
P("Standart-128 da 80 ta so‘rovdan keyin buzg‘unchi istalgan xabar uchun kalitli xesh qiymatining 32 bitini xatosiz bashorat qiladi; bu imitoqo‘yilma (soxta autentifikatsiya kodi) hujumining 32 bitga qisqartirilishini anglatadi. Bundan tashqari, A va c faqat kalitning 0-qatlamiga bog‘liq bo‘lgani uchun, bu qatlam (30 ta noma’lum bit) qolgan bitlardan alohida 2³⁰ ta sinov bilan tiklanadi. SBZ-128 da affin model ishlamaydi: bitlar bo‘yicha aniqlik 0,56 (0,5 dan biroz yuqori qiymat chiqishdagi doimiy bitlar hisobiga), 32 bitning hammasi bir vaqtda hech bir xabarda to‘g‘ri chiqmadi. 256 bitli variantlarda ham model ishlamaydi.")
P("Standart-128 da kalitning 0-qatlamini tiklash algoritmi quyidagicha qurilishi mumkin:")
BL("buzg‘unchi 33 tadan ortiq bir blokli xabar uchun kalitli xesh qiymatlarni oladi va chiqish 0-qatlamini xabar 0-qatlamining affin funksiyasi sifatida tiklaydi (A, c);")
BL("kalit 0-qatlamining har bir nomzodi (2³⁰ ta: R juftligi va ikkinchi yarim bayt juftligi ma’lum) uchun L = P·M(k₀) matritsalari va mos (A, c) qiymatlari hisoblanadi va kuzatilgan qiymat bilan solishtiriladi;")
BL("mos kelgan nomzod topilgach, kalitning qolgan 96 biti alohida qidiriladi; umumiy murakkablik ≈2⁹⁶ ga teng, bu 2¹²⁶ dan ancha kichik.")
P("SBZ da 1-qadam bajarilmaydi (17-jadval), shuning uchun kalit qatlamlarga ajralmaydi va bu hujum qo‘llanilmaydi.")
H2('3.6. Bardoshlilik bahosi')
LC=A3['lin_cost']
P("Linearizatsiya murakkabligi tenglamalar darajasiga bog‘liq ravishda 3-rasmda keltirilgan. 128 bitli rejim uchun (128 ta noma’lum xabar biti) 2⁶⁴ chegarasidan oshish uchun daraja d ≥ 4, 256 bitli rejim uchun (256 ta noma’lum bit) 2¹²⁸ chegarasidan oshish uchun d ≥ 8 bo‘lishi kerak.")
IMG('/home/claude/ka/ch_alg.png',15.5,7.5,"3-rasm. Linearizatsiya murakkabligining tenglamalar darajasiga bog‘liqligi")
rr=[["Variant","Yutishdagi daraja","Talab qilinadigan daraja","Bardoshlilikka erishiladigan raund"]]
rr+= [["Standart-128","1 (XOR)","≥ 4","erishilmaydi (0-qatlam doim chiziqli)"],["SBZ-128","13","≥ 4","0-nuqtadagi yutishdan keyin"],["Standart-256","6","≥ 8","1-raunddan keyin (yuqori bitlar darajasi o‘sishi hisobiga)"],["SBZ-256","13","≥ 8","0-nuqtadagi yutishdan keyin"]]
T([2100,1900,2000,3350],rr,"18-jadval. Algebraik bardoshlilik bahosi")
H2('3.7. Algebraik kriptotahlil bo‘yicha xulosa')
BL("Akslantirishlar ichida yagona yuqori darajali element — yutish nuqtasidagi o‘zgartirish: XOR — 1-daraja, Z — 6-daraja, SBZ — 13-daraja. Qo‘sh va Aralash bit darajasida T-funksiyalar bo‘lib, ularning 0-qatlami chiziqli.")
BL("Raund tenglamalari tizimining hajmini Qo‘sh o‘zgartirishi belgilaydi (bir raundda ≈2,4·10⁵ ta o‘zgaruvchi, 256 bitli rejim); SBZ tizim hajmini amalda o‘zgartirmaydi, lekin uning darajasini oshiradi.")
BL("Standart-128 da 0-qatlam butun xesh davomida chiziqli: 80 ta so‘rov bilan 32 bitli bashorat 100% aniqlikda ishlaydi. SBZ bu hujumni to‘liq bartaraf etadi.")
BL("SBZ variantlari algebraik bardoshlilik chegarasiga 0-nuqtadagi yutishdan keyinoq erishadi, Standart-256 esa 1-raunddan keyin erishadi.")

# ---------------- UMUMIY XULOSA ----------------
PB(); H1('Umumiy xulosa')
P("O‘tkazilgan chiziqli, differensial va algebraik kriptotahlil natijalari 19-jadvalda umumlashtirilgan.")
rr=[["Usul","Standart-128","SBZ-128","Standart-256","SBZ-256"]]
rr.append(["Chiziqli (|c| chegarasi)","bardoshli emas (c = 1)","≈20-raund (eng yomon), 11-raund (mediana)","≈19-raund (mediana)","≈11-raund (mediana), ≈37-raund (eng yomon)"])
rr.append(["Differensial (p chegarasi)","bardoshli emas","8-raund","9-raund","8-raund"])
rr.append(["Algebraik (daraja)","bardoshli emas","0-nuqta","1-raund","0-nuqta"])
rr.append(["Qoldiq xossalar (Aralash degeneratsiyasi)","mavjud","mavjud","mavjud","mavjud"])
T([2350,1750,1750,1750,1750],rr,"19-jadval. Bardoshlilikka erishiladigan raundlar (birinchi iteratsiyadan boshlab hisoblanganda)")
P("Asosiy xulosalar quyidagilardan iborat. Birinchidan, 1-algoritmning 1–7- va 10-raundlari T-funksiyalardan tashkil topgani uchun ular uchala usulga ham deyarli qarshilik ko‘rsatmaydi: 0-qatlam chiziqli tenglamalar bilan aniq kuzatiladi, MSB ayirmalari har raundda ≈0,9 ehtimollik bilan saqlanadi, quyi bitlar darajasi past bo‘lib qoladi. Shuning uchun algoritmning kriptografik bardoshliligi to‘liq yutish nuqtasidagi o‘zgartirishga bog‘liq.")
P("Ikkinchidan, SBZ yutish nuqtasidagi ko‘rsatkichlarni sezilarli yaxshilaydi: maksimal korrelyatsiya 0,25 (Standart-256) va 1 (Standart-128) dan 2⁻⁶ gacha, maksimal differensial ehtimollik 0,156 va 1 dan 2⁻⁶ gacha kamayadi, algebraik daraja 6 va 1 dan 13 gacha oshadi. Natijada 128 bitli rejimdagi tuzilmaviy zaiflik bartaraf etiladi, 256 bitli rejimda esa bardoshlilikka bir necha raund oldinroq erishiladi.")
P("Uchinchidan, Aralash o‘zgartirishining 2 moduli bo‘yicha degeneratsiyasi (rang o‘rtacha ≈26, nol satrlar va ustunlar) SBZ ga bog‘liq bo‘lmagan qoldiq zaifliklarni keltirib chiqaradi: chiqishdagi c = 1 chiziqli munosabatlar va ayirmalarning ehtimollik 1 bilan so‘nishi. Shuningdek, chiziqli bardoshlilik kalitga kuchli bog‘liq: eng yomon kalitlarda zarur raundlar soni 3–4 baravar oshadi. Tavsiya etiladi: (1) BaytZichlash o‘rniga SBZ ni qabul qilish; (2) Aralash va TuzilmaKalit o‘zgartirishlarini diamatritsa mod 2 bo‘yicha har doim teskarilanuvchi bo‘ladigan qilib qayta ko‘rib chiqish; (3) oxirgi raunddan keyin chiqishga ham yutish (yoki chiziqli bo‘lmagan) qatlami qo‘shishni ko‘rib chiqish.")
H2('Tahlil usuli va cheklovlari')
P("Akslantirishlarning korrelyatsion va ayirmalar matritsalari, ANF darajalari va implitsit tenglamalar soni barcha kirishlar bo‘yicha aniq hisoblandi. Raund darajasidagi ko‘rsatkichlar tanlanma asosida o‘lchandi: chiziqli bashorat — 1500 ta, ayirmalarni kuzatish — 2000–3000 ta juftlik, kub testlari — har bir holatda 4 ta kub, faol baytlar tahlili — 120–200 ta kalit. Chiziqli izlar uchun faol baytlar soni 0-qatlam modeli doirasida (yuqori bitlardagi niqoblarni hisobga olmasdan) va oxirgi qatlamda og‘irligi 1–2 bo‘lgan niqoblar bo‘yicha qidirildi, shuning uchun ular minimal qiymatlarning bahosi hisoblanadi. Differensial chegaralar har bir faol bayt uchun eng yaxshi ehtimollikni olish orqali hisoblandi. Tenglamalar soni 3.2.5-banddagi modelga asoslangan baholardir. Tahlil uchun foydalanilgan dasturiy realizatsiya O‘zMSt 285:2024 A ilovasidagi va SBZ materialidagi barcha nazorat qiymatlarini takrorlaydi.")
import re
order=[]
for b in B:
    if b[0]=='cap':
        m=re.match(r'(\d+)-jadval',b[1])
        if m: order.append(int(m.group(1)))
mp={o:i+1 for i,o in enumerate(order)}
def ren(t):
    return re.sub(r'(\d+)-jadval',lambda m: f"{mp.get(int(m.group(1)),int(m.group(1)))}-JADVAL",t).replace('-JADVAL','-jadval')
def walk(x):
    if isinstance(x,str): return ren(x)
    if isinstance(x,list): return [walk(y) for y in x]
    return x
B=[walk(b) for b in B]
json.dump(B,open('blocks.json','w'),ensure_ascii=False)
print(len(B))
