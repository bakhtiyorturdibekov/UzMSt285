import json, sys, numpy as np
sys.path.insert(0,'/home/claude/pkg/uzmst285_tahlil')
from yagona import RC, C1, C2, iteration_g, xesh_bayt_g, boglash_y
from algoritm import KAT_XABAR, KAT_KALIT
B=[]; tc=[0]
H1=lambda t:B.append(['h1',t]); H2=lambda t:B.append(['h2',t]); H3=lambda t:B.append(['h3',t])
P=lambda t:B.append(['p',t]); F=lambda t:B.append(['f',t]); BL=lambda t:B.append(['b',t]); PB=lambda:B.append(['pb'])
def T(w,rows,cap,mono=()): tc[0]+=1; B.append(['cap',f"{tc[0]}-jadval. {cap}"]); B.append(['t',w,rows,list(mono)])
hx=lambda a,w:[' '.join(f'{int(v):02x}' for v in a[i*w:(i+1)*w]) for i in range(4)]
B.append(['title','6.2. XESHLASH FUNKSIYASI ALGORITMI (YANGI TAHRIR LOYIHASI)'])
B.append(['sub','O‘zMSt 285:2024 standartining 6.2-bandi uchun taklif etilayotgan matn'])
P("*Izoh.* Ushbu matn kriptotahlil natijalari asosida taklif etilgan yagona variantni standart uslubida bayon qiladi. U standartning 6.2-bandi o‘rniga qo‘llanishi mo‘ljallangan; 5-bo‘limdagi atamalar va belgilashlar o‘zgarishsiz qoladi, yangi atamalar shu bandda ta’riflanadi.")
H2('6.2.1. Umumiy qoidalar')
P("Xeshlash funksiyasi ikki rejimda qo‘llaniladi: 256 bitli (n = 256) va 128 bitli (n = 128). Barcha amallar baytlar ustida, 256 moduli bo‘yicha bajariladi. Ichki holat (holat) va raund kaliti (kₑ) — 4 satr va w ustundan iborat baytli massivlar: n = 256 da w = 8, n = 128 da w = 4. Massiv elementlari satrma-satr raqamlanadi: holat[s, u] = holat[w·s + u]. Blok uzunligi bl = 4w bayt (32 yoki 16), kalit k ham bl baytdan iborat va uning birinchi bayti juft bo‘lishi kerak.")
P("Raundlar soni R (tavsiya etilgan qiymat R = 6; R ≥ 4). S — FIPS 197 standartining S-box jadvali; S⁻¹ — unga teskari jadval. x⁻¹ — 256 moduli bo‘yicha toq x ning teskarisi. ⊕ — bitma-bit qo‘shish, ∨ — bitma-bit «yoki».")
H2('6.2.2. Aralash(holat, kₑ) o‘zgartirishi')
P("Aralash o‘zgartirishi 6.2-bandning amaldagi tahriridagi diamatritsa ko‘paytmasi qoidasi bo‘yicha bajariladi (256 moduli bo‘yicha). n = 256 da holat va kₑ massivlarining chap (0–3 ustunlar) va o‘ng (4–7 ustunlar) 4×4 qismlari alohida ko‘paytiriladi; n = 128 da butun 4×4 massiv bitta ko‘paytmadan o‘tadi. 6.2.6-band bo‘yicha kₑ ning barcha elementlari toq, shuning uchun Aralash har doim teskarilanuvchi.")
H2('6.2.3. Bog‘lash(holat, X) o‘zgartirishi')
P("Holat ikki yarimga bo‘linadi: chap yarim Ch — har bir satrning birinchi w/2 bayti, o‘ng yarim O‘ — qolgan w/2 bayti; har bir yarim m = 2w baytdan iborat va satrma-satr tartiblanadi. R₀ = k[0] ∧ FE₁₆ — kalitning birinchi bayti (juft). X — kₑ yoki kirish bloki.")
P("Yarim qadam f(T, U, X_T, X_U), bu yerda T — o‘zgartiriladigan yarim, U — o‘zgarmaydigan yarim, X_T, X_U — X ning mos yarimlari:")
F("1) J = Σᵢ U[i] (mod 256),   K = Πᵢ (U[i] ∨ 1) (mod 256);")
F("2) i = 0, 1, …, m − 1 uchun:  aᵢ = 2·S(U[i] ⊕ X_U[i] ⊕ J) + 1,   bᵢ = 2·S(U[(i+1) mod m] ⊕ X_T[i] ⊕ K) + 1;")
F("3) yᵢ = −aᵢ · T[i] · (bᵢ + R₀ · T[i])⁻¹ (mod 256);   T[i] ← S(yᵢ ⊕ X_T[i]).")
P("Bog‘lash uchta yarim qadamdan iborat: O‘ ← f(O‘, Ch, X_O‘, X_Ch); Ch ← f(Ch, O‘, X_Ch, X_O‘); O‘ ← f(O‘, Ch, X_O‘, X_Ch). aᵢ va bᵢ toq, R₀ juft bo‘lgani uchun (bᵢ + R₀·T[i]) doim toq va teskarisi mavjud; Bog‘lash belgilangan X da holat bo‘yicha o‘zaro bir qiymatli akslantirish. Teskari akslantirish: yarim qadamlar teskari tartibda, T[i] = −bᵢ·y·(aᵢ + R₀·y)⁻¹, y = S⁻¹(T′[i]) ⊕ X_T[i].")
H2('6.2.4. SBZ(holat, blok) o‘zgartirishi')
F("holat[i] ← S( holat[i] ⊕ S(blok[i]) ),   i = 0, 1, …, bl − 1.")
H2('6.2.5. SurHolat va SurKalit o‘zgartirishlari')
P("SurHolat: har bir s-satr o‘ngga davriy suriladi, so‘ng har bir u-ustun pastga davriy suriladi. n = 256 da satrlar 1, 2, 3, 4 pozitsiyaga, ustunlar (u mod 4 = 0, 1, 2, 3 uchun) 1, 2, 3, 0 pozitsiyaga; n = 128 da satrlar 1, 2, 3, 0, ustunlar 1, 2, 3, 0 pozitsiyaga. SurKalit: n = 256 da satrlar 4, 3, 2, 1, ustunlar (u mod 4 = 0, 1, 2, 3 uchun) 0, −3, −2, −1; n = 128 da satrlar 0, 3, 2, 1, ustunlar 0, −3, −2, −1 (manfiy qiymat — yuqoriga surish).")
H2('6.2.6. Raund kalitlari')
F("boshlang‘ich qiymat:  kₑ ← k ∨ 1 (har bir bayt uchun);   j-raundda:  kₑ ← (SurKalit(kₑ) ⊕ RCⱼ) ∨ 1,")
P("bu yerda RCⱼ — 1-jadvaldagi j-raund konstantasi (n = 128 da uning birinchi 16 bayti). Raund kalitlari holatga bog‘liq emas va barcha elementlari toq.")
H2('6.2.7. Iteratsiya F(holat, blok, kₑ)')
code=["kₑ ← kₑ ∨ 1","holat ← SBZ(Bog‘lash(holat, blok), blok)","For j = 1 to R","    holat ← Aralash(holat, kₑ)","    holat ← Bog‘lash(holat, kₑ)","    holat ← SurHolat(holat);  kₑ ← (SurKalit(kₑ) ⊕ RCⱼ) ∨ 1","    If j = R − 2:  holat ← SBZ(Bog‘lash(holat, blok), blok)","    Else:          holat ← Bog‘lash(holat, kₑ)","    If j = R − 1:  holat ← SBZ(Bog‘lash(holat, blok), blok)","End For","Return holat, kₑ"]
T([9354],[["Iteratsiya algoritmi"],["\n".join(code)]],"Iteratsiya F (R raund)",mono=(0,))
H2('6.2.8. Xesh qiymatni hisoblash')
P("1) M xabar bl baytli bloklarga bo‘linadi (oxirgi blok nollar bilan to‘ldiriladi; bo‘sh xabar — bitta nol blok): M₁, …, M_b. 2) Uzunlik bloki — xabar uzunligi bitlarda, bl baytli katta-endian son; NY bloki — M₁ + … + M_b (mod 2^(8·bl)), katta-endian. 3) Kirish bloklari ketma-ketligi: M₁, …, M_b, uzunlik, NY. 4) holat ← M₁, kₑ ← k. 5) Qolgan har bir kirish bloki Bᵢ uchun:")
F("H₀ ← holat;   (holat, kₑ) ← F(holat, Bᵢ, kₑ);   holat ← holat ⊕ H₀   (oldinga uzatish).")
P("6) Chiqish o‘zgartirishi (H — oxirgi holat; C₁, C₂ — 2-jadvaldagi konstantalar, n = 128 da birinchi 16 bayti; Bog‘lash da R₀ = C8₁₆):")
F("h(M) = Bog‘lash(Bog‘lash(H, C₁), C₂) ⊕ H.")
H2('6.2.9. Konstantalar')
P("RCⱼ — √2 ning kasr qismining dastlabki 320 bayti (RCⱼ = baytlar 32(j−1) … 32j − 1); C₁ ∥ C₂ — √3 ning kasr qismining dastlabki 64 bayti, har bir baytning eng kichik biti 1 ga tenglashtirilgan.")
rows=[["j","RCⱼ (32 bayt, o‘n oltilik)"]]+[[str(j),' '.join(f'{int(v):02x}' for v in RC[j][:16])+'\n'+' '.join(f'{int(v):02x}' for v in RC[j][16:])] for j in range(1,11)]
T([700,8654],rows,"Raund konstantalari RCⱼ",mono=(1,))
T([900,8454],[["","32 bayt (o‘n oltilik)"],["C₁",' '.join(f'{int(v):02x}' for v in C1[:16])+'\n'+' '.join(f'{int(v):02x}' for v in C1[16:])],["C₂",' '.join(f'{int(v):02x}' for v in C2[:16])+'\n'+' '.join(f'{int(v):02x}' for v in C2[16:])]],"Chiqish o‘zgartirishi konstantalari",mono=(1,))
H2('6.2.10. Nazorat misoli')
for bl,lab in ((32,'256'),(16,'128')):
    w=bl//4; M=np.array(list(KAT_XABAR)); Kk=np.array(list(KAT_KALIT[:bl]))
    h=M[:bl][None].copy(); blok=M[bl:2*bl][None].copy(); tr=[]
    iteration_g(h,blok,Kk[None].copy(),Kk[None],6,trace=tr)
    P(f"n = {lab}, R = 6. Kalit k = {KAT_KALIT[:bl].hex()}; xabar — standartning A ilovasidagi 64 baytli xabar («funksiyaxeshirovaniya…»). Birinchi iteratsiya (holat = M₁, blok = M₂) bo‘yicha oraliq qiymatlar:")
    rows=[["Qadam","holat"]]
    for nm,j,hh,kk in tr:
        rows.append([("0-nuqta: SBZ(Bog‘lash(holat, blok), blok)" if nm=='yutish0' else f"{j}-raund oxiri"),"\n".join(hx(hh[0],w))])
    T([3300,6054],rows,f"Nazorat misoli (n = {lab}, R = 6): birinchi iteratsiyaning oraliq qiymatlari",mono=(1,))
    P(f"Xesh qiymat (R = 6): {xesh_bayt_g(KAT_XABAR,KAT_KALIT,bl,6).hex()}")
    P(f"Xesh qiymat (R = 10): {xesh_bayt_g(KAT_XABAR,KAT_KALIT,bl,10).hex()}")
json.dump(B,open('blocksB.json','w'),ensure_ascii=False); print(len(B),tc[0])
