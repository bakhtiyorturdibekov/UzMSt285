# O‘zMSt 285:2024, 1-algoritm: SBZ o‘zgartirishining kriptotahlili

Ushbu dasturlar «O‘zMSt 285:2024 1-algoritmida BaytZichlash o‘rniga SBZ o‘zgartirishini qo‘llashning
chiziqli, differensial va algebraik kriptotahlilga ta’siri» hisobotidagi barcha hisob-kitoblarni bajaradi.

## Talablar

- Python 3.9 yoki undan yangi
- `numpy`
- `matplotlib` (faqat grafiklar uchun)

O‘rnatish: `pip install numpy matplotlib`

## Ishga tushirish

```
python hammasi.py          # to‘liq tahlil (hisobotdagi tanlanmalar, bir necha daqiqa)
python hammasi.py --tez    # kichik tanlanmalar bilan tez sinov
```

Jupyter daftarini ochish: `jupyter notebook xulosalar_misollar.ipynb` (yoki JupyterLab / VS Code). Daftar shu papkadagi modullardan foydalanadi.

Har bir modulni alohida ham ishga tushirish mumkin: `python chiziqli.py`, `python differensial.py`,
`python algebraik.py`, `python grafiklar.py`. Natijalar `natijalar/` papkasiga JSON va PNG ko‘rinishida yoziladi.

## Fayllar

| Fayl | Vazifasi |
|---|---|
| `algoritm.py` | 1-algoritmning vektorlashtirilgan realizatsiyasi: p = 256 va p = 16, BaytZichlash (`std`) va SBZ (`sbz`). `xesh(xabar, kalit, p, bz)` funksiyasi va nazorat qiymatlari tekshiruvi (`python algoritm.py`). |
| `komponentlar.py` | Umumiy vositalar: korrelyatsion matritsa (LAT), ayirmalar matritsasi (DDT), ANF darajasi, implitsit tenglamalar soni, Qo‘sh elementi, 0-qatlam matritsalari P, M(k₀), L. |
| `chiziqli.py` | 1-bo‘lim: akslantirishlar korrelyatsiyalari, 0-qatlam raund tenglamasi, L matritsasining rangi va tarmoqlanish soni, yutish qatlamlari bo‘yicha faol baytlar. |
| `differensial.py` | 2-bo‘lim: ayirmalar matritsalari, orttirmalarni har bir akslantirish va raund bo‘yicha kuzatish (D0a, D0b, D1, D2, D3 tajribalari), Aralash yadrosi. |
| `algebraik.py` | 3-bo‘lim: implitsit tenglamalar, ANF darajalari, kub testlari, 0-qatlamni linearizatsiya qilish hujumi, tenglamalar soni va linearizatsiya murakkabligi. |
| `integral.py` | 4-bo‘lim (standart algoritm): akslantirishlarning tanlangan to‘plamlarga (A, C, B, U) ta’siri, raundlar va akslantirishlar bo‘yicha integral xossalar (bayt va bit-qatlam darajasida), to‘liq xesh uchun integral farqlovchi, Standart-128 da T-funksiya xossasi tekshiruvi. |
| `variant.py` | Tavsiyalar bo‘yicha variantlar: SBZ, toq kₑ (kₑ ← kₑ ∨ 1), raund ichidagi S-box qatlami; `xesh_v(xabar, kalit, p, bz, toq, sqatlam)`. |
| `boglash.py` | Qo‘sh o‘rniga taklif etilgan yagona Bog‘lash(holat, X) akslantirishi (256 va 128 bitli rejimlar uchun bir xil, bayt darajasida), uning teskarisi va yangi variantning xesh funksiyasi `xesh_b(xabarlar, kalitlar, p, sbz=True)`. |
| `qosh_boglash.c`, `qosh_boglash_tezlik.ipynb` | Qo‘sh va Bog‘lash akslantirishlarining C realizatsiyasi va tezlik solishtiruvi (daftar C kodini o‘zi yozadi, kompilyatsiya qiladi va natijalarni Python bilan tekshiradi). |
| `yakuniy.py` | 4-tavsiya: yakuniy qatlam — har bir blokdan keyin oldinga uzatish (DM) va chiqish o‘zgartirishi h = P(H) ⊕ H; `xesh_yakuniy(xabarlar, kalitlar, p, bz, dm, omega)`. |
| `yakuniy_variant.py`, `yakuniy.c`, `yakuniy_variant.ipynb` | Taklif etilgan yakuniy variant (SBZ + toq kₑ + Bog‘lash + oldinga uzatish + P(H) ⊕ H): Python va C realizatsiyalari, tezlikni standart bilan solishtirish va asosiy kriptografik tekshiruvlar (`./yak katy`, `./yak tezy p bayt takror`). |
| `yagona.py`, `yagona.c`, `chegaralar.py`, `yagona_variant.ipynb` | Yagona variant: ikkala rejim bayt darajasida (4×8 / 4×4), raundlar soni R, √2/√3 konstantalari; faol S-box larning minimal soni (differensial — to‘liq qidiruv va o‘lchamlar modeli, chiziqli — niqoblar zanjiri); C da tezlik (`./yag katg`, `./yag tezg bl R bayt takror`). |
| `uzmst285.c` | Algoritmning C realizatsiyasi (barcha variantlar): `./uzmst285 kat` — nazorat qiymatlari, `./uzmst285 p bz toq sq bayt takror` — tezlik o‘lchovi. |
| `tavsiyalar_tahlili.ipynb` | Jupyter daftar: 2- va 3-tavsiyalarning kriptografik tekshiruvi (mustaqil ishlaydi). |
| `sbz_kriptotahlili.ipynb` | Jupyter daftar: BaytZichlash o‘rniga SBZ qo‘llanilgan algoritmning chiziqli, differensial, algebraik va integral tahlili (mustaqil ishlaydi; `HAJM` — tanlanma hajmi, `OGIR` — 2¹⁶ to‘plamli to‘liq xesh sinovi). |
| `tezlik_tahlili.ipynb` | Jupyter daftar: variantlarning tezligi — C (avtomatik kompilyatsiya), Python va amallar modeli (mustaqil ishlaydi). |
| `grafiklar.py` | Hisobotdagi 1–3-rasmlar. |
| `hammasi.py` | Barcha bosqichlarni ketma-ket bajaradi. |
| `xulosalar_misollar.ipynb` | Jupyter daftar: hisobotdagi 13 ta xulosaning har birini A ilova ma’lumotlarida akslantirishlar ketma-ketligi bo‘yicha qadamma-qadam kuzatadi (bajarilgan holda, natijalari ichida). Natijalar `misollar_natijalari.json` ga yoziladi. |

## Natijalar va hisobot jadvallari

| JSON kaliti | Hisobotdagi joyi |
|---|---|
| `chiziqli.json → komponentlar` | 1.2-bo‘lim (2–5-jadvallar) |
| `chiziqli.json → raund_0qatlam` | 6-jadval |
| `chiziqli.json → L_matritsa`, `faol_baytlar` | 1.4–1.5-bo‘limlar, 7-jadval, 1-rasm |
| `differensial.json → komponentlar` | 2.2-bo‘lim (8–10-jadvallar) |
| `differensial.json → kuzatish` | 2.3–2.4-bo‘limlar (11–15-jadvallar), 2-rasm |
| `differensial.json → yadro` | 2.2.5 va 2.4-bo‘limlar |
| `algebraik.json → tenglamalar_daraja` | 3.2-bo‘lim |
| `algebraik.json → tenglamalar_soni` | 3.2.5 va 3.3-bo‘limlar |
| `algebraik.json → kub` | 3.4-bo‘lim |
| `algebraik.json → linearizatsiya` | 3.5-bo‘lim |
| `integral.json` | «Standart algoritm kriptotahlili» hisobotining 4-bo‘limi |
| `integral_sbz.json` (`python integral.py --bz sbz`) | «SBZ varianti kriptotahlili» hisobotining 4-bo‘limi |

## Muhim izohlar

- **Nazorat qiymatlari.** `algoritm.py` O‘zMSt 285:2024 A ilovasidagi va SBZ materialidagi barcha nazorat qiymatlarini takrorlaydi.
- **Realizatsiya kelishuvlari.**
  - R — kalitning birinchi bayti (yarim bayti).
  - Massivlar satr bo‘yicha joylashtiriladi.
  - Uzunlik bloki bitlarda, big-endian ko‘rinishda yoziladi.
  - NY bloki — bloklarning blok uzunligi moduli bo‘yicha yig‘indisi.
  - 128 bitli rejimda uzunlik va NY bloklari ham 128 bitli.
- **Kalit cheklovi.** Tasodifiy kalitlarda birinchi va ikkinchi elementlar juft qilib olinadi. R toq bo‘lsa, Qo‘sh o‘zgartirishidagi teskarilash bajarilmaydi.
- **Tanlanmaga asoslangan natijalar.** Raund darajasidagi ko‘rsatkichlar tanlanma asosida o‘lchanadi. Tasodifiy sonlar generatorlarining boshlang‘ich qiymatlari hisobotdagi qiymatlarni takrorlaydigan qilib qo‘yilgan. Tanlanma hajmi yoki boshlang‘ich qiymat o‘zgartirilsa, natijalar statistik xatolik doirasida farq qiladi.
- **Dasturlarning vazifasi.** Dasturlar tahlil va tadqiqot uchun mo‘ljallangan. Ular doimiy vaqtli emas va amaliy himoya tizimlarida foydalanish uchun emas.
