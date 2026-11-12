# O‘zMSt 285:2024 xesh funksiyasi tadqiqoti: dasturlar to‘plami

Ushbu arxivda O‘zMSt 285:2024 standartining 1-algoritmini tahlil qilish, takomillashtirish bo‘yicha tavsiyalarni
ishlab chiqish va sinash, hisobotlar hamda IEEE Access maqolasini tayyorlash jarayonida yaratilgan barcha dasturlar jamlangan.

## Talablar

- Python 3.9+ va `numpy` (barcha tahlil dasturlari); grafiklar uchun `matplotlib`.
- C kompilyatori (gcc, clang yoki Windows da MinGW) — tezlik o‘lchovlari uchun.
- Hisobotlarni Word formatida qayta yaratish uchun: Node.js va `docx` paketi (`npm install docx`).

```
pip install numpy matplotlib
```

## Tuzilish

| Papka | Mazmuni |
|---|---|
| `01_dastlabki_realizatsiya/` | `uzmst285_alg1.py` — 1-algoritmning birinchi mustaqil realizatsiyasi (A ilova nazorat misolini takrorlaydi); `dastlabki_tadqiqot_skriptlari/` — standartdagi noaniqliklarni aniqlash va nazorat qiymatlariga moslash bo‘yicha dastlabki skriptlar. |
| `02_tahlil_paketi_uzmst285_tahlil/` | Asosiy Python paketi (o‘z README si bor): algoritm (standart va SBZ), komponentlar, chiziqli/differensial/algebraik/integral tahlil, tavsiyalar variantlari (`variant.py`), Bog‘lash (`boglash.py`), yakuniy qatlam (`yakuniy.py`), yakuniy va yagona variantlar (`yakuniy_variant.py`, `yagona.py`), faol S-box chegaralari (`chegaralar.py`), C fayllari, Jupyter daftarlari va `natijalar/`. |
| `03_hisob_skriptlari/` | Hisobotlardagi raqamlarni hosil qilgan hisob skriptlari (chiziqli, differensial, algebraik tahlil, misollar). |
| `natijalar_json/` | Barcha hisoblarning JSON natijalari (hisobot va maqola generatorlari shu fayllardan foydalanadi). |
| `04_C_realizatsiyalar/` | C dasturlari: standart va variantlar (`standart_va_variantlar.c`), Qo‘sh va Bog‘lash solishtiruvi (`qosh_va_boglash.c`), to‘rtta tavsiya varianti (`tort_tavsiya_variant.c`), yakuniy variant (`yakuniy_variant.c`), yagona variant (`yagona_variant.c`). |
| `05_jupyter_daftarlari/` | Mustaqil ishlaydigan daftarlar (modullar daftar ichida): misollar, tavsiyalar tahlili, tezlik, SBZ kriptotahlili, Qo‘sh–Bog‘lash tezligi, yakuniy va yagona variantlar; `daftar_yaratuvchi/` — daftarlarni yaratuvchi skriptlar. |
| `06_hisobot_generatorlari/` | Har bir Word hisobotini yaratgan skriptlar (`content*.py` — matn va jadvallar, `render*.js` — Word fayl yaratish, `charts.py` — grafiklar). Papka nomlari hisobot nomlariga mos. |
| `07_maqola_IEEE_Access/` | Maqola: `maqola_inglizcha.py`, `maqola_ozbekcha.py` (matn), grafiklar skriptlari, `render_ieee.js` (Word), `to_omml.py` va `omml_en.py` (formulalarni Word formulasiga o‘tkazish), `rasmlar/`. |
| `08_word_formula_konvertori/` | Matndagi formulalarni Word formulasiga (OMML) o‘tkazuvchi vosita va «Ilovalarga» faylini o‘zgartirgan skript. |

## Tez boshlash

```
cd 02_tahlil_paketi_uzmst285_tahlil
python algoritm.py            # standart va SBZ nazorat qiymatlarini tekshirish
python hammasi.py --tez       # barcha tahlillar (qisqartirilgan tanlanmalar)
python integral.py --bz sbz   # SBZ varianti uchun integral tahlil
```

C dasturlari:

```
cd 04_C_realizatsiyalar
gcc -O2 -o yag yagona_variant.c
./yag katg                    # yagona variant nazorat qiymatlari (R = 10, 6, 5, 4)
./yag tezg 32 6 262144 3      # tezlik: 256 bitli rejim, R = 6
./yag 256 0 0 0 262144 3      # standart algoritm tezligi
```

## Nazorat qiymatlari (A ilova kaliti va xabari)

| Variant | Xesh qiymat |
|---|---|
| Standart, 256 bit | 55394f2d84fccd4d8d01d8fef756cd657ebecc3f96f81e5207767447de66e2b6 |
| Standart, 128 bit | e9eaccdd4ccce2d229228c864989eb9f |
| SBZ, 256 bit | 42f97daaa8e7010bc629ca695eaa77df7ae7443a0c3ae78d205c2e025d256c96 |
| SBZ, 128 bit | bd745e2ed572ea4246ed68482ef46c5e |
| Yagona variant, 256 bit, R = 6 | 9ab07b8d692c955e67e4e60362a929d516848f3b5733cab7a24aef26b2afade7 |
| Yagona variant, 128 bit, R = 6 | f84f8c106ba8ecfcf00188b0a24720f0 |

## Eslatmalar

- `02_…` paketi, `04_…` C fayllari va `05_…` daftarlari mustaqil ishlaydi.
- `03_…`, `06_…`, `07_…` va `08_…` papkalaridagi skriptlar ishlab chiqish muhitida yozilgan va fayllarga mutlaq
  yo‘llar orqali murojaat qiladi (masalan, `/home/claude/ka/` → `natijalar_json/`,
  `/home/claude/pkg/uzmst285_tahlil/` → `02_tahlil_paketi_uzmst285_tahlil/`,
  `/home/claude/nb/misollar_natijalari.json` → `natijalar_json/misollar_natijalari.json`,
  `/mnt/user-data/outputs/` → chiqish papkasi). Qayta ishga tushirishdan oldin bu yo‘llarni o‘z kompyuteringizdagi
  joylashuvga moslang.
- Tadqiqot davomida bir martalik tekshiruvlar uchun yozilgan ayrim vaqtinchalik skriptlar saqlanmagan; ularning
  natijalari `natijalar_json/` va hisobotlarda qayd etilgan.
