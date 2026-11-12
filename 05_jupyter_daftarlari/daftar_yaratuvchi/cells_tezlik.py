
from builder import setup_cell
C = []
md = lambda s: C.append(('markdown', s.strip('\n')))
code = lambda s: C.append(('code', s.strip('\n')))
md("""
# O‘zMSt 285:2024, 1-algoritm: tavsiyalarning tezlikka ta’siri

Taqqoslanadigan variantlar (har ikkala rejimda, p = 256 va p = 16):

| Belgi | Variant |
|---|---|
| `std` | standart algoritm (BaytZichlash) |
| `std+toq` | standart + toq kₑ (2-tavsiya) |
| `std+S` | standart + raund ichidagi S-box qatlami (3-tavsiya) |
| `sbz` | SBZ (1-tavsiya) |
| `sbz+toq` | SBZ + toq kₑ |
| `sbz+toq+S` | uchala tavsiya birgalikda |

Tezlik uch xil usulda baholanadi:
1. **C realizatsiyasi** (gcc -O2) — eng ishonchli o‘lchov; kompyuterda C kompilyatori (gcc, clang yoki MinGW) bo‘lsa ishlaydi.
2. **Python (numpy)** realizatsiyasi — nisbiy taqqoslash uchun.
3. **Amallar sonining modeli** — platformaga bog‘liq bo‘lmagan baho.

Daftar mustaqil: modullar 0-hujayrada yuklanadi. Faqat `numpy` kerak (grafik uchun `matplotlib` ixtiyoriy).
""")
C.append(setup_cell(['algoritm', 'komponentlar', 'variant']))
code(r"""
import numpy as np, json, os, sys, time, shutil, subprocess, statistics
from algoritm import *
from komponentlar import kalitlar
from variant import xesh_v, iteration_v
VAR = [('std', 'std', 0, 0, 0), ('std+toq', 'std', 0, 1, 0), ('std+S', 'std', 0, 0, 1),
       ('sbz', 'sbz', 1, 0, 0), ('sbz+toq', 'sbz', 1, 1, 0), ('sbz+toq+S', 'sbz', 1, 1, 1)]
XABAR_HAJMI = 262144      # C o‘lchovi uchun xabar uzunligi (bayt)
TAKROR = 5                # har bir o‘lchov takrori (eng yaxshi natija olinadi)
TEZ = False
if TEZ: XABAR_HAJMI, TAKROR = 65536, 2
NATIJA = {}
print("Python: nazorat qiymatlari")
PYKAT = {}
for p in (256, 16):
    for nom, bz, _, toq, sq in VAR:
        PYKAT[(p, nom)] = xesh_v(KAT_XABAR, KAT_KALIT, p, bz, bool(toq), bool(sq)).hex()
        print(f"  p={p:3d}  {nom:10s} {PYKAT[(p, nom)]}")
""")
md("""
## 1. C realizatsiyasi

Quyidagi hujayra C manba kodini `uzmst285.c` fayliga yozadi, uni kompilyatsiya qiladi va nazorat qiymatlarini
Python realizatsiyasi bilan solishtiradi. C dastur argumentlari: `kat` — nazorat qiymatlari;
`p bz toq sq bayt_soni takror` — tezlik o‘lchovi (sekundlarda eng yaxshi vaqt).
""")
code("C_MANBA = " + repr('/* O\'zMSt 285:2024, 1-algoritm: C realizatsiyasi (tezlikni o\'lchash uchun).\n   Variantlar: p = 256 yoki 16; bz = 0 (BaytZichlash) yoki 1 (SBZ);\n   toq = 1 — barcha kₑ elementlari toq (2-tavsiya); sqatlam = 1 — raund ichidagi S-box qatlami (3-tavsiya). */\n#include <stdint.h>\n#include <string.h>\n#include <stdio.h>\n#include <stdlib.h>\n#include <time.h>\n\nstatic const uint8_t ZICH[256] = {\n 5,13,6,11,1,10,15,8,0,4,7,9,2,12,3,14, 8,7,2,14,15,3,11,6,1,12,13,10,5,4,9,0,\n 14,2,13,4,12,7,1,11,6,9,0,5,3,10,8,15, 0,14,9,12,3,13,7,4,15,6,5,1,11,2,10,8,\n 3,10,7,2,4,12,9,1,14,13,15,8,0,5,11,6, 2,3,1,8,0,14,5,9,12,11,6,7,10,15,13,4,\n 10,4,14,15,9,5,8,2,11,0,1,3,12,6,7,13, 11,9,10,1,6,4,13,15,3,5,14,0,8,7,2,12,\n 1,0,3,7,13,11,10,12,9,14,4,6,15,8,5,2, 4,8,11,9,14,6,2,5,10,3,12,15,7,13,0,1,\n 9,12,15,0,2,1,14,10,5,8,11,13,4,3,6,7, 6,11,8,13,7,9,0,3,4,15,10,2,14,1,12,5,\n 15,1,0,5,10,8,3,7,13,2,9,12,6,14,4,11, 12,5,4,10,11,2,6,13,8,7,3,14,1,0,15,9,\n 7,15,12,6,5,0,4,14,2,10,8,11,13,9,1,3, 13,6,5,3,8,15,12,0,7,1,2,4,9,11,14,10};\nstatic uint8_t SB[256];\nstatic const uint8_t PRESENT[16] = {0xC,5,6,0xB,9,0,0xA,0xD,3,0xE,0xF,8,4,7,1,2};\nstatic uint32_t INV256[256], INV16[16];\n\nstatic void init_tables(void) {\n    uint8_t p = 1, q = 1;\n    do {\n        p = p ^ (uint8_t)(p << 1) ^ ((p & 0x80) ? 0x1B : 0);\n        q ^= q << 1; q ^= q << 2; q ^= q << 4; if (q & 0x80) q ^= 0x09;\n        uint8_t x = q ^ (uint8_t)((q << 1) | (q >> 7)) ^ (uint8_t)((q << 2) | (q >> 6)) ^ (uint8_t)((q << 3) | (q >> 5)) ^ (uint8_t)((q << 4) | (q >> 4));\n        SB[p] = x ^ 0x63;\n    } while (p != 1);\n    SB[0] = 0x63;\n    for (uint32_t x = 1; x < 256; x += 2) for (uint32_t y = 1; y < 256; y += 2) if (((x * y) & 255) == 1) INV256[x] = y;\n    for (uint32_t x = 1; x < 16; x += 2) for (uint32_t y = 1; y < 16; y += 2) if (((x * y) & 15) == 1) INV16[x] = y;\n}\n\ntypedef struct { uint32_t p, m; const uint32_t *inv; int bz, toq, sq; } cfg_t;\n\nstatic inline uint32_t step(uint32_t x, uint32_t A, uint32_t B, uint32_t R, const cfg_t *c) {\n    uint32_t d = (B + R * x) & c->m;\n    return (0u - A * x * c->inv[d]) & c->m;\n}\nstatic inline uint32_t prododd(const uint32_t *a, const cfg_t *c) {\n    uint32_t r = 1; for (int i = 0; i < 32; i++) r = (r * (a[i] | 1)) & c->m; return r;\n}\nstatic inline uint32_t dK(uint32_t P, uint32_t Jo, const cfg_t *c) {\n    uint32_t t = (Jo + 1) & c->m; return (P == t || P == ((0u - t) & c->m)) ? 10 : 0;\n}\nstatic void qosh(uint32_t *h, uint32_t *hn, uint32_t R, const cfg_t *c) {\n    uint32_t m = c->m, J1h = 0, J1hn = 0, h1[32], hn1[32];\n    for (int i = 0; i < 32; i++) { J1h += h[i]; J1hn += hn[i]; }\n    J1h &= m; J1hn &= m;\n    uint32_t Ph = prododd(h, c), Phn = prododd(hn, c);\n    uint32_t K1h = (Ph + dK(Ph, J1hn, c)) & m, K1hn = (Phn + dK(Phn, J1h, c)) & m;\n    uint32_t dAh = (J1hn & 1) ? 0 : 1, dAhn = (J1h & 1) ? 0 : 1;\n    for (int i = 0; i < 32; i++) {\n        h1[i]  = step(h[i],  (J1hn + 2 * hn[i] + dAh) & m, (K1h - 2 * h[i]) & m, R, c);\n        hn1[i] = step(hn[i], (J1h + 2 * h[i] + dAhn) & m, (K1hn - 2 * hn[i]) & m, R, c);\n    }\n    uint32_t J2h = 0, J2hn = 0;\n    for (int i = 0; i < 32; i++) { J2h += h1[i]; J2hn += hn1[i]; }\n    J2h &= m; J2hn &= m;\n    uint32_t P2h = prododd(h1, c), P2hn = prododd(hn1, c);\n    uint32_t K2h = (P2h + dK(P2h, J2hn, c)) & m, K2hn = (P2hn + dK(P2hn, J2h, c)) & m;\n    uint32_t dA2h = ((J1hn + J2hn) & 1) ? 0 : 1, dA2hn = ((J1h + J2h) & 1) ? 0 : 1;\n    uint32_t KKh = (K1h * K2h) & m, KKhn = (K1hn * K2hn) & m;\n    for (int i = 0; i < 32; i++) {\n        uint32_t A2 = (J1hn + J2hn + 2 * hn1[i] + dA2h) & m; if (!A2) A2 = 1;\n        uint32_t B2 = (KKh - 2 * h1[i]) & m;\n        uint32_t x2 = step(h1[i], A2, B2, R, c); if (!x2) x2 = (A2 + B2) & m;\n        uint32_t A2n = (J1h + J2h + 2 * h1[i] + dA2hn) & m; if (!A2n) A2n = 1;\n        uint32_t B2n = (KKhn - 2 * hn1[i]) & m;\n        uint32_t y2 = step(hn1[i], A2n, B2n, R, c); if (!y2) y2 = (A2n + B2n) & m;\n        h[i] = step(x2, A2, B2, R, c); hn[i] = step(y2, A2n, B2n, R, c);\n    }\n}\nstatic void dia(uint32_t *h, const uint32_t *k, int off, const cfg_t *c) {\n    uint32_t H[4][4], K[4][4], sk[4], sh[4], m = c->m;\n    for (int s = 0; s < 4; s++) for (int u = 0; u < 4; u++) { H[s][u] = h[8 * s + off + u]; K[s][u] = k[8 * s + off + u]; }\n    for (int u = 0; u < 4; u++) { sk[u] = K[0][u] + K[1][u] + K[2][u] + K[3][u]; sh[u] = H[0][u] + H[1][u] + H[2][u] + H[3][u]; }\n    for (int s = 0; s < 4; s++) for (int u = 0; u < 4; u++) {\n        uint32_t v;\n        if (s == u) { v = H[u][u] * sk[u]; for (int i = 0; i < 4; i++) if (i != u) v -= H[i][i] * K[i][u]; }\n        else { v = H[s][u] * sk[u] + K[s][u] * sh[u]; for (int i = 0; i < 4; i++) if (i != s && i != u) v -= H[s][i] * K[i][u]; }\n        h[8 * s + off + u] = v & m;\n    }\n}\nstatic void aralash(uint32_t *h, const uint32_t *ke, const cfg_t *c) { dia(h, ke, 0, c); dia(h, ke, 4, c); }\nstatic void shift(uint32_t *a, const int *rows, const int *cols) {\n    uint32_t t[32];\n    for (int s = 0; s < 4; s++) for (int u = 0; u < 8; u++) t[8 * s + u] = a[8 * s + ((u - rows[s]) % 8 + 8) % 8];\n    for (int u = 0; u < 8; u++) for (int s = 0; s < 4; s++) a[8 * s + u] = t[8 * (((s - cols[u]) % 4 + 4) % 4) + u];\n}\nstatic const int HR[4] = {1, 2, 3, 4}, HC[8] = {1, 2, 3, 0, 1, 2, 3, 0};\nstatic const int KR[4] = {4, 3, 2, 1}, KC[8] = {0, -3, -2, -1, 0, -3, -2, -1};\nstatic void tuz(uint32_t *ke, const uint32_t *k, const cfg_t *c) {\n    for (int i = 0; i < 32; i++) {\n        if (c->toq) { ke[i] |= 1; continue; }\n        if (ke[i] == 0 && !(k[i] & 1)) ke[i] = 2;\n        else if (ke[i] != 0 && (ke[i] & 1) == (k[i] & 1)) ;\n        else ke[i] = (ke[i] - 1) & c->m;\n    }\n}\nstatic void bzf(uint32_t *h, const uint32_t *hn, const cfg_t *c) {\n    if (c->p == 256) {\n        for (int i = 0; i < 32; i++) h[i] = c->bz ? SB[h[i] ^ SB[hn[i]]] : (uint32_t)((ZICH[h[i]] << 4) | ZICH[hn[i]]);\n    } else {\n        if (!c->bz) { for (int i = 0; i < 32; i++) h[i] ^= hn[i]; return; }\n        for (int j = 0; j < 16; j++) {\n            uint32_t H = 16 * h[2 * j] + h[2 * j + 1], N = 16 * hn[2 * j] + hn[2 * j + 1], Q = SB[H ^ SB[N]];\n            h[2 * j] = Q >> 4; h[2 * j + 1] = Q & 15;\n        }\n    }\n}\nstatic void sqatlam(uint32_t *h, const cfg_t *c) {\n    if (!c->sq) return;\n    for (int i = 0; i < 32; i++) h[i] = (c->p == 256) ? SB[h[i]] : PRESENT[h[i]];\n}\nstatic void iteration(uint32_t *holat, const uint32_t *blok, uint32_t *ke, const uint32_t *k, const cfg_t *c) {\n    uint32_t R = k[0], hn[32];\n    if (c->toq) for (int i = 0; i < 32; i++) ke[i] |= 1;\n    memcpy(hn, blok, sizeof hn); qosh(holat, hn, R, c); bzf(holat, hn, c);\n    for (int j = 1; j <= 10; j++) {\n        aralash(holat, ke, c);\n        qosh(holat, ke, R, c);\n        shift(holat, HR, HC); shift(ke, KR, KC);\n        sqatlam(holat, c);\n        if (j == 8) { memcpy(hn, blok, sizeof hn); qosh(holat, hn, R, c); bzf(holat, hn, c); }\n        else qosh(holat, ke, R, c);\n        tuz(ke, k, c);\n        if (j == 9) { memcpy(hn, blok, sizeof hn); qosh(holat, hn, R, c); bzf(holat, hn, c); }\n    }\n}\nstatic void units(const uint8_t *b, int bl, uint32_t *u, int p) {\n    if (p == 256) for (int i = 0; i < 32; i++) u[i] = b[i];\n    else for (int i = 0; i < bl; i++) { u[2 * i] = b[i] >> 4; u[2 * i + 1] = b[i] & 15; }\n}\n/* xesh: xabar, uzunlik (bayt), kalit (32 yoki 16 bayt) -> chiqish (32 yoki 16 bayt) */\nvoid xesh(const uint8_t *msg, size_t len, const uint8_t *key, int p, int bz, int toq, int sq, uint8_t *out) {\n    cfg_t c = {(uint32_t)p, (uint32_t)p - 1, p == 256 ? INV256 : INV16, bz, toq, sq};\n    int bl = p == 256 ? 32 : 16;\n    size_t nb = len ? (len + bl - 1) / bl : 1;\n    uint8_t blk[32], ny[32] = {0}, lb[32] = {0};\n    uint32_t holat[32], blok[32], ke[32], k[32];\n    uint64_t bits = (uint64_t)len * 8;\n    for (int i = 0; i < 8; i++) lb[bl - 1 - i] = (uint8_t)(bits >> (8 * i));\n    units(key, bl, k, p); memcpy(ke, k, sizeof ke);\n    for (size_t b = 0; b < nb + 2; b++) {\n        if (b < nb) {\n            memset(blk, 0, sizeof blk);\n            size_t n = (b + 1) * bl <= len ? (size_t)bl : (len > b * bl ? len - b * bl : 0);\n            if (n) memcpy(blk, msg + b * bl, n);\n            unsigned carry = 0;\n            for (int i = bl - 1; i >= 0; i--) { unsigned s = ny[i] + blk[i] + carry; ny[i] = s & 255; carry = s >> 8; }\n        } else memcpy(blk, b == nb ? lb : ny, bl);\n        if (b == 0) { units(blk, bl, holat, p); continue; }\n        units(blk, bl, blok, p); iteration(holat, blok, ke, k, &c);\n    }\n    if (p == 256) for (int i = 0; i < 32; i++) out[i] = (uint8_t)holat[i];\n    else for (int i = 0; i < 16; i++) out[i] = (uint8_t)(holat[2 * i] << 4 | holat[2 * i + 1]);\n}\nstatic double now(void) { return (double)clock() / CLOCKS_PER_SEC; }\nint main(int argc, char **argv) {\n    init_tables();\n    static const uint8_t KEY[32] = {0xc8,0x6e,0xd4,0xb2,0x75,0x6d,0xf1,0xcd,0x6b,0x6e,0xca,0x81,0xd4,0x41,0x80,0x92,\n                                    0x21,0xab,0x81,0xbb,0xa0,0xc7,0xc1,0x50,0x44,0xbe,0x8f,0xeb,0x93,0x4f,0x95,0xa2};\n    const char *M = "funksiyaxeshirovaniyainformasionnayatexnologiyakriptograficheska";\n    uint8_t out[32];\n    if (argc > 1 && !strcmp(argv[1], "kat")) {               /* nazorat qiymatlari */\n        for (int p = 256; p >= 16; p /= 16) for (int v = 0; v < 6; v++) {\n            int bz = v >= 1, toq = v >= 2, sq = v >= 3;\n            if (v == 4) { bz = 0; toq = 1; sq = 0; } if (v == 5) { bz = 0; toq = 0; sq = 1; }\n            xesh((const uint8_t *)M, 64, KEY, p, bz, toq, sq, out);\n            printf("%d %d %d %d ", p, bz, toq, sq); for (int i = 0; i < (p == 256 ? 32 : 16); i++) printf("%02x", out[i]); printf("\\n");\n        }\n        return 0;\n    }\n    /* tezlik: argv = p bz toq sq bayt_soni takror */\n    int p = atoi(argv[1]), bz = atoi(argv[2]), toq = atoi(argv[3]), sq = atoi(argv[4]);\n    size_t n = (size_t)atol(argv[5]); int rep = atoi(argv[6]);\n    uint8_t *buf = malloc(n); for (size_t i = 0; i < n; i++) buf[i] = (uint8_t)(i * 131 + 7);\n    double best = 1e9;\n    for (int r = 0; r < rep; r++) { double t = now(); xesh(buf, n, KEY, p, bz, toq, sq, out); t = now() - t; if (t < best) best = t; }\n    printf("%.6f %02x\\n", best, out[0]);\n    free(buf); return 0;\n}\n'))
code(r"""
open('uzmst285.c', 'w', encoding='utf-8').write(C_MANBA)
EXE = os.path.abspath('uzmst285.exe' if sys.platform.startswith('win') else 'uzmst285')
KOMPILYATOR = next((c for c in ('gcc', 'cc', 'clang') if shutil.which(c)), None)
C_BOR = False
if KOMPILYATOR:
    r = subprocess.run([KOMPILYATOR, '-O2', '-o', EXE, 'uzmst285.c'], capture_output=True, text=True)
    C_BOR = (r.returncode == 0)
    print("Kompilyator:", KOMPILYATOR, "— muvaffaqiyatli" if C_BOR else "— xato:\n" + r.stderr)
    if C_BOR: print(subprocess.run([KOMPILYATOR, '--version'], capture_output=True, text=True).stdout.splitlines()[0])
else:
    print("C kompilyatori topilmadi: C o‘lchovi o‘tkazib yuboriladi (Python va model natijalari baribir hisoblanadi).")
if C_BOR:
    nom_kod = {(bz, toq, sq): nom for nom, _, bz, toq, sq in VAR}
    ok = True
    for line in subprocess.run([EXE, 'kat'], capture_output=True, text=True).stdout.split('\n'):
        if not line.strip(): continue
        p, bz, toq, sq, h = line.split(); key = (int(p), nom_kod[(int(bz), int(toq), int(sq))])
        mos = (PYKAT[key] == h); ok &= mos
        print(f"  p={p:>3s}  {key[1]:10s} C = Python: {'ha' if mos else 'YO‘Q'}")
    print("Barcha variantlar bo‘yicha C va Python natijalari mos:", ok)
""")
code(r"""
if C_BOR:
    NATIJA['C'] = {}
    o_lchov = {}
    for tur in range(3):                         # variantlar aralash tartibda 3 marta o‘lchanadi
        for p in (256, 16):
            for nom, _, bz, toq, sq in VAR:
                out = subprocess.run([EXE, str(p), str(bz), str(toq), str(sq), str(XABAR_HAJMI), str(TAKROR)], capture_output=True, text=True).stdout.split()
                o_lchov.setdefault((p, nom), []).append(float(out[0]))
    print(f"Xabar uzunligi {XABAR_HAJMI} bayt; har bir variant uchun eng yaxshi vaqt:")
    print(f"{'rejim':>6s} {'variant':>11s} {'vaqt, ms':>9s} {'mkS/blok':>9s} {'MB/s':>7s} {'farq, %':>8s}")
    for p in (256, 16):
        bl = 32 if p == 256 else 16; nb = XABAR_HAJMI // bl + 2; asos = min(o_lchov[(p, 'std')])
        for nom, *_ in VAR:
            t = min(o_lchov[(p, nom)])
            NATIJA['C'][f'{p}_{nom}'] = dict(vaqt_ms=round(t * 1e3, 2), mks_blok=round(t / nb * 1e6, 3), MBs=round(XABAR_HAJMI / t / 1e6, 2), farq_foiz=round((t / asos - 1) * 100, 1))
            d = NATIJA['C'][f'{p}_{nom}']
            print(f"{p:6d} {nom:>11s} {d['vaqt_ms']:9.2f} {d['mks_blok']:9.3f} {d['MBs']:7.2f} {d['farq_foiz']:+8.1f}")
    # o‘lchov shovqini: bir xil variantning takroriy o‘lchovlari orasidagi farq
    sh = max((max(v) / min(v) - 1) * 100 for v in o_lchov.values())
    NATIJA['C_shovqin_foiz'] = round(sh, 1); print(f"Takroriy o‘lchovlar orasidagi eng katta farq (shovqin): {sh:.1f}%")
""")
md("""
## 2. Python (numpy) realizatsiyasi

Bir vaqtda 2000 ta mustaqil blok uchun bitta iteratsiya (10 raund) vaqti o‘lchanadi.
Mutlaq qiymatlar C dan ancha sekin, lekin nisbiy farqlar ko‘rsatkichli.
""")
code(r"""
NATIJA['Python'] = {}
rng = np.random.default_rng(1); N = 500 if TEZ else 2000
for p in (256, 16):
    k = kalitlar(rng, N, p); h = rng.integers(0, p, (N, 32)); bl = rng.integers(0, p, (N, 32)); asos = None
    for nom, bz, _, toq, sq in VAR:
        c = Cfg(p, bz); t_ = []
        for r in range(3):
            t0 = time.perf_counter(); iteration_v(h, bl, k.copy(), k, c, bool(toq), bool(sq)); t_.append(time.perf_counter() - t0)
        t = min(t_); asos = asos or t
        NATIJA['Python'][f'{p}_{nom}'] = dict(vaqt_s=round(t, 3), farq_foiz=round((t / asos - 1) * 100, 1))
        print(f"p={p:3d} {nom:10s} {t:.3f} s / {N} blok   farq: {(t/asos-1)*100:+.1f}%")
""")
md("""
## 3. Amallar sonining modeli

Bitta kirish bloki (bitta iteratsiya) uchun amallar soni C realizatsiyasi tuzilishi bo‘yicha sanaladi:
Qo‘sh — 22 marta, Aralash — 10, SurHolat/SurKalit — 10, TuzilmaKalit — 10, yutish — 3, S-box qatlami — 10.
""")
code(r"""
def amallar(p, bz, toq, sq):
    q = dict(kopaytirish=128 + 64 * 3 + 2 + 64 * 6, teskari_jadval=64 * 3, qoshish=128 + 64 * 6 + 64 * 10)   # bitta Qo‘sh
    a = dict(kopaytirish=128, qoshish=144)                                                                    # bitta Aralash
    n = dict(kopaytirish=22 * q['kopaytirish'] + 10 * a['kopaytirish'], teskari_jadval=22 * q['teskari_jadval'],
             qoshish=22 * q['qoshish'] + 10 * a['qoshish'], jadval=0, taqqoslash=0, bit_amal=0)
    if p == 256: n['jadval'] += 3 * 64; n['bit_amal'] += 3 * 32           # BZ ham, SBZ ham: bayt boshiga 2 ta jadval
    else:
        if bz == 'std': n['bit_amal'] += 3 * 32                            # XOR
        else: n['jadval'] += 3 * 32; n['bit_amal'] += 3 * 64               # 16 bayt x 2 jadval, juftlash
    if toq: n['bit_amal'] += 10 * 32                                       # kₑ ∨ 1
    else: n['taqqoslash'] += 10 * 32 * 2                                   # juftlik va nol tekshiruvi
    if sq: n['jadval'] += 10 * 32                                          # S-box qatlami
    n['jami'] = sum(n.values()); return n
NATIJA['model'] = {}
for p in (256, 16):
    asos = amallar(p, 'std', 0, 0)['jami']
    for nom, bz, _, toq, sq in VAR:
        n = amallar(p, bz, toq, sq); n['farq_foiz'] = round((n['jami'] / asos - 1) * 100, 2); NATIJA['model'][f'{p}_{nom}'] = n
        print(f"p={p:3d} {nom:10s} ko‘paytirish {n['kopaytirish']}, teskarilash jadvali {n['teskari_jadval']}, qo‘shish {n['qoshish']}, "
              f"jadval {n['jadval']}, taqqoslash {n['taqqoslash']}, bit amali {n['bit_amal']}  -> jami {n['jami']} ({n['farq_foiz']:+.2f}%)")
""")
md("""
## 4. Jamlanma
""")
code(r"""
print(f"{'rejim':>6s} {'variant':>11s} {'C, %':>7s} {'Python, %':>10s} {'model, %':>9s}")
for p in (256, 16):
    for nom, *_ in VAR:
        cf = NATIJA.get('C', {}).get(f'{p}_{nom}', {}).get('farq_foiz', float('nan'))
        print(f"{p:6d} {nom:>11s} {cf:+7.1f} {NATIJA['Python'][f'{p}_{nom}']['farq_foiz']:+10.1f} {NATIJA['model'][f'{p}_{nom}']['farq_foiz']:+9.2f}")
json.dump(NATIJA, open('tezlik_natijalari.json', 'w'), ensure_ascii=False, indent=1)
print("Natijalar tezlik_natijalari.json ga yozildi.")
try:
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.6))
    for i, p in enumerate((256, 16)):
        noms = [v[0] for v in VAR]; x = np.arange(len(noms))
        for j, (manba, lab) in enumerate([('C', 'C (gcc -O2)'), ('Python', 'Python (numpy)'), ('model', 'amallar modeli')]):
            if manba not in NATIJA: continue
            ax[i].bar(x + (j - 1) * 0.27, [NATIJA[manba][f'{p}_{n}']['farq_foiz'] for n in noms], 0.27, label=lab)
        ax[i].set_xticks(x); ax[i].set_xticklabels(noms, rotation=30, fontsize=8); ax[i].axhline(0, color='k', lw=.6)
        ax[i].set_title(f'p = {p}'); ax[i].set_ylabel('standartga nisbatan farq, %'); ax[i].grid(alpha=.3)
    ax[0].legend(fontsize=8); fig.tight_layout(); fig.savefig('tezlik.png', dpi=200); plt.show()
except ImportError:
    print("matplotlib o‘rnatilmagan — grafik chizilmadi.")
""")
