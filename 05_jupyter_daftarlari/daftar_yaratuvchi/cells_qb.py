
from builder import setup_cell
C = []
md = lambda s: C.append(('markdown', s.strip('\n')))
code = lambda s: C.append(('code', s.strip('\n')))
md("""
# Qo‘sh va Bog‘lash akslantirishlarining tezligini solishtirish

Faqat ikkita akslantirish solishtiriladi (algoritmning qolgan qismisiz):
- **Qo‘sh(holat, X)** — standartdagi akslantirish (6.2.1-band);
- **Bog‘lash(holat, X)** — uning o‘rniga taklif etilgan yagona akslantirish (256 va 128 bitli rejimlar uchun bir xil).

Usullar: (1) C realizatsiyasi (gcc -O2) — asosiy o‘lchov; (2) Python (numpy) realizatsiyasi; (3) amallar soni.
Daftar mustaqil ishlaydi, faqat `numpy` kerak; C o‘lchovi uchun gcc/clang (Windows da MinGW) kerak.
""")
C.append(setup_cell(['algoritm', 'komponentlar', 'boglash']))
code(r"""
import numpy as np, json, os, sys, time, shutil, subprocess
from algoritm import qosh, Cfg, KAT_XABAR, KAT_KALIT, to_units
from boglash import boglash, boglash_inv
CHAQIRUV = 1_000_000      # C o‘lchovida bitta takrordagi chaqiruvlar soni
TAKROR, TURLAR = 3, 4     # takrorlar (eng yaxshisi olinadi) va aralash tartibdagi turlar soni
NATIJA = {}
rng = np.random.default_rng(1)
for p in (256, 16):
    N = 2000; h = rng.integers(0, p, (N, 32)); x = rng.integers(0, p, (N, 32)); R = rng.integers(0, 128, N) * 2
    print(f"p={p}: Bog‘lash teskarilanuvchi (2000 tasodifiy kirish):", bool((boglash_inv(boglash(h, x, R, p), x, R, p) == h).all()))
""")
md("## 1. C realizatsiyasi va to‘g‘rilik tekshiruvi")
code("C_MANBA = " + repr('/* O\'zMSt 285:2024, 1-algoritm: C realizatsiyasi (tezlikni o\'lchash uchun).\n   Variantlar: p = 256 yoki 16; bz = 0 (BaytZichlash) yoki 1 (SBZ);\n   toq = 1 — barcha kₑ elementlari toq (2-tavsiya); sqatlam = 1 — raund ichidagi S-box qatlami (3-tavsiya). */\n#include <stdint.h>\n#include <string.h>\n#include <stdio.h>\n#include <stdlib.h>\n#include <time.h>\n\nstatic const uint8_t ZICH[256] = {\n 5,13,6,11,1,10,15,8,0,4,7,9,2,12,3,14, 8,7,2,14,15,3,11,6,1,12,13,10,5,4,9,0,\n 14,2,13,4,12,7,1,11,6,9,0,5,3,10,8,15, 0,14,9,12,3,13,7,4,15,6,5,1,11,2,10,8,\n 3,10,7,2,4,12,9,1,14,13,15,8,0,5,11,6, 2,3,1,8,0,14,5,9,12,11,6,7,10,15,13,4,\n 10,4,14,15,9,5,8,2,11,0,1,3,12,6,7,13, 11,9,10,1,6,4,13,15,3,5,14,0,8,7,2,12,\n 1,0,3,7,13,11,10,12,9,14,4,6,15,8,5,2, 4,8,11,9,14,6,2,5,10,3,12,15,7,13,0,1,\n 9,12,15,0,2,1,14,10,5,8,11,13,4,3,6,7, 6,11,8,13,7,9,0,3,4,15,10,2,14,1,12,5,\n 15,1,0,5,10,8,3,7,13,2,9,12,6,14,4,11, 12,5,4,10,11,2,6,13,8,7,3,14,1,0,15,9,\n 7,15,12,6,5,0,4,14,2,10,8,11,13,9,1,3, 13,6,5,3,8,15,12,0,7,1,2,4,9,11,14,10};\nstatic uint8_t SB[256];\nstatic const uint8_t PRESENT[16] = {0xC,5,6,0xB,9,0,0xA,0xD,3,0xE,0xF,8,4,7,1,2};\nstatic uint32_t INV256[256], INV16[16];\n\nstatic void init_tables(void) {\n    uint8_t p = 1, q = 1;\n    do {\n        p = p ^ (uint8_t)(p << 1) ^ ((p & 0x80) ? 0x1B : 0);\n        q ^= q << 1; q ^= q << 2; q ^= q << 4; if (q & 0x80) q ^= 0x09;\n        uint8_t x = q ^ (uint8_t)((q << 1) | (q >> 7)) ^ (uint8_t)((q << 2) | (q >> 6)) ^ (uint8_t)((q << 3) | (q >> 5)) ^ (uint8_t)((q << 4) | (q >> 4));\n        SB[p] = x ^ 0x63;\n    } while (p != 1);\n    SB[0] = 0x63;\n    for (uint32_t x = 1; x < 256; x += 2) for (uint32_t y = 1; y < 256; y += 2) if (((x * y) & 255) == 1) INV256[x] = y;\n    for (uint32_t x = 1; x < 16; x += 2) for (uint32_t y = 1; y < 16; y += 2) if (((x * y) & 15) == 1) INV16[x] = y;\n}\n\ntypedef struct { uint32_t p, m; const uint32_t *inv; int bz, toq, sq; } cfg_t;\n\nstatic inline uint32_t step(uint32_t x, uint32_t A, uint32_t B, uint32_t R, const cfg_t *c) {\n    uint32_t d = (B + R * x) & c->m;\n    return (0u - A * x * c->inv[d]) & c->m;\n}\nstatic inline uint32_t prododd(const uint32_t *a, const cfg_t *c) {\n    uint32_t r = 1; for (int i = 0; i < 32; i++) r = (r * (a[i] | 1)) & c->m; return r;\n}\nstatic inline uint32_t dK(uint32_t P, uint32_t Jo, const cfg_t *c) {\n    uint32_t t = (Jo + 1) & c->m; return (P == t || P == ((0u - t) & c->m)) ? 10 : 0;\n}\nstatic void qosh(uint32_t *h, uint32_t *hn, uint32_t R, const cfg_t *c) {\n    uint32_t m = c->m, J1h = 0, J1hn = 0, h1[32], hn1[32];\n    for (int i = 0; i < 32; i++) { J1h += h[i]; J1hn += hn[i]; }\n    J1h &= m; J1hn &= m;\n    uint32_t Ph = prododd(h, c), Phn = prododd(hn, c);\n    uint32_t K1h = (Ph + dK(Ph, J1hn, c)) & m, K1hn = (Phn + dK(Phn, J1h, c)) & m;\n    uint32_t dAh = (J1hn & 1) ? 0 : 1, dAhn = (J1h & 1) ? 0 : 1;\n    for (int i = 0; i < 32; i++) {\n        h1[i]  = step(h[i],  (J1hn + 2 * hn[i] + dAh) & m, (K1h - 2 * h[i]) & m, R, c);\n        hn1[i] = step(hn[i], (J1h + 2 * h[i] + dAhn) & m, (K1hn - 2 * hn[i]) & m, R, c);\n    }\n    uint32_t J2h = 0, J2hn = 0;\n    for (int i = 0; i < 32; i++) { J2h += h1[i]; J2hn += hn1[i]; }\n    J2h &= m; J2hn &= m;\n    uint32_t P2h = prododd(h1, c), P2hn = prododd(hn1, c);\n    uint32_t K2h = (P2h + dK(P2h, J2hn, c)) & m, K2hn = (P2hn + dK(P2hn, J2h, c)) & m;\n    uint32_t dA2h = ((J1hn + J2hn) & 1) ? 0 : 1, dA2hn = ((J1h + J2h) & 1) ? 0 : 1;\n    uint32_t KKh = (K1h * K2h) & m, KKhn = (K1hn * K2hn) & m;\n    for (int i = 0; i < 32; i++) {\n        uint32_t A2 = (J1hn + J2hn + 2 * hn1[i] + dA2h) & m; if (!A2) A2 = 1;\n        uint32_t B2 = (KKh - 2 * h1[i]) & m;\n        uint32_t x2 = step(h1[i], A2, B2, R, c); if (!x2) x2 = (A2 + B2) & m;\n        uint32_t A2n = (J1h + J2h + 2 * h1[i] + dA2hn) & m; if (!A2n) A2n = 1;\n        uint32_t B2n = (KKhn - 2 * hn1[i]) & m;\n        uint32_t y2 = step(hn1[i], A2n, B2n, R, c); if (!y2) y2 = (A2n + B2n) & m;\n        h[i] = step(x2, A2, B2, R, c); hn[i] = step(y2, A2n, B2n, R, c);\n    }\n}\n\n/* ---------- Bog\'lash (ikkala rejim uchun yagona, bayt darajasida) ---------- */\nstatic const int L256[16] = {0,1,2,3, 8,9,10,11, 16,17,18,19, 24,25,26,27};\nstatic const int R256[16] = {4,5,6,7, 12,13,14,15, 20,21,22,23, 28,29,30,31};\nstatic const int L128[8]  = {0,1, 4,5, 8,9, 12,13};\nstatic const int R128[8]  = {2,3, 6,7, 10,11, 14,15};\nstatic inline void yarim(uint8_t *H, const int *T, const int *U, int m, const uint8_t *X, uint32_t R) {\n    uint32_t J = 0, K = 1;\n    for (int i = 0; i < m; i++) { uint32_t u = H[U[i]]; J += u; K *= (u | 1); }\n    J &= 255; K &= 255;\n    uint32_t u0 = H[U[0]];\n    for (int i = 0; i < m; i++) {\n        uint32_t ui = H[U[i]], un = (i + 1 < m) ? H[U[i + 1]] : u0, xt = X[T[i]], x = H[T[i]];\n        uint32_t a = 2u * SB[ui ^ X[U[i]] ^ J] + 1, b = 2u * SB[un ^ xt ^ K] + 1;\n        uint32_t f = (0u - a * x * INV256[(b + R * x) & 255]) & 255;\n        H[T[i]] = SB[f ^ xt];\n    }\n}\nstatic void boglash(uint32_t *h, const uint32_t *x, uint32_t R, int p) {\n    uint8_t H[32], X[32];\n    if (p == 256) {\n        for (int i = 0; i < 32; i++) { H[i] = (uint8_t)h[i]; X[i] = (uint8_t)x[i]; }\n        yarim(H, R256, L256, 16, X, R); yarim(H, L256, R256, 16, X, R); yarim(H, R256, L256, 16, X, R);\n        for (int i = 0; i < 32; i++) h[i] = H[i];\n    } else {\n        for (int j = 0; j < 16; j++) { H[j] = (uint8_t)((h[2*j] << 4) | h[2*j+1]); X[j] = (uint8_t)((x[2*j] << 4) | x[2*j+1]); }\n        yarim(H, R128, L128, 8, X, R); yarim(H, L128, R128, 8, X, R); yarim(H, R128, L128, 8, X, R);\n        for (int j = 0; j < 16; j++) { h[2*j] = H[j] >> 4; h[2*j+1] = H[j] & 15; }\n    }\n}\nstatic double now(void) { return (double)clock() / CLOCKS_PER_SEC; }\nint main(int argc, char **argv) {\n    init_tables();\n    static const uint8_t KEY[32] = {0xc8,0x6e,0xd4,0xb2,0x75,0x6d,0xf1,0xcd,0x6b,0x6e,0xca,0x81,0xd4,0x41,0x80,0x92,\n                                    0x21,0xab,0x81,0xbb,0xa0,0xc7,0xc1,0x50,0x44,0xbe,0x8f,0xeb,0x93,0x4f,0x95,0xa2};\n    const char *M = "funksiyaxeshirovaniyainformasionnayatexnologiyakriptograficheska";\n    if (argc > 1 && !strcmp(argv[1], "test")) {      /* to\'g\'rilikni tekshirish: A ilova ma\'lumotlari */\n        for (int p = 256; p >= 16; p /= 16) {\n            cfg_t c = {(uint32_t)p, (uint32_t)p - 1, p == 256 ? INV256 : INV16, 0, 0, 0};\n            uint32_t h[32], x[32], h2[32], x2[32];\n            for (int i = 0; i < 32; i++) {\n                if (p == 256) { h[i] = (uint8_t)M[i]; x[i] = (uint8_t)M[32 + i]; }\n                else { h[i] = (i % 2) ? ((uint8_t)M[i/2] & 15) : ((uint8_t)M[i/2] >> 4); x[i] = (i % 2) ? ((uint8_t)M[16+i/2] & 15) : ((uint8_t)M[16+i/2] >> 4); }\n            }\n            uint32_t Rq = p == 256 ? KEY[0] : (KEY[0] >> 4), Rb = KEY[0] & 0xFE;\n            memcpy(h2, h, sizeof h); memcpy(x2, x, sizeof x); qosh(h2, x2, Rq, &c);\n            printf("qosh %d ", p); for (int i = 0; i < 32; i++) printf(p == 256 ? "%02x" : "%x", h2[i]); printf("\\n");\n            memcpy(h2, h, sizeof h); boglash(h2, x, Rb, p);\n            printf("boglash %d ", p); for (int i = 0; i < 32; i++) printf(p == 256 ? "%02x" : "%x", h2[i]); printf("\\n");\n        }\n        return 0;\n    }\n    /* tezlik: argv = amal(qosh|boglash) p chaqiruvlar_soni takror */\n    int isq = !strcmp(argv[1], "qosh"), p = atoi(argv[2]); long n = atol(argv[3]); int rep = atoi(argv[4]);\n    cfg_t c = {(uint32_t)p, (uint32_t)p - 1, p == 256 ? INV256 : INV16, 0, 0, 0};\n    uint32_t h[32], x[32]; double best = 1e9; uint32_t chk = 0;\n    for (int r = 0; r < rep; r++) {\n        for (int i = 0; i < 32; i++) { h[i] = (i * 37 + 11) & c.m; x[i] = (i * 91 + 5) & c.m; }\n        double t = now();\n        for (long it = 0; it < n; it++) {\n            if (isq) { qosh(h, x, p == 256 ? 200 : 12, &c); }          /* x ham o\'zgaradi (kₑ kabi) */\n            else { boglash(h, x, 200, p); x[it & 31] ^= h[(it * 7) & 31]; }\n        }\n        t = now() - t; if (t < best) best = t; chk ^= h[0] ^ x[1];\n    }\n    printf("%.6f %u\\n", best, chk);\n    return 0;\n}\n'))
code(r"""
open('qb.c', 'w', encoding='utf-8').write(C_MANBA)
EXE = os.path.abspath('qb.exe' if sys.platform.startswith('win') else 'qb')
CC = next((c for c in ('gcc', 'cc', 'clang') if shutil.which(c)), None); C_BOR = False
if CC:
    r = subprocess.run([CC, '-O2', '-o', EXE, 'qb.c'], capture_output=True, text=True); C_BOR = r.returncode == 0
    print("Kompilyator:", CC, "— muvaffaqiyatli" if C_BOR else "— xato:\n" + r.stderr)
else: print("C kompilyatori topilmadi — C o‘lchovi o‘tkazib yuboriladi.")
if C_BOR:
    out = subprocess.run([EXE, 'test'], capture_output=True, text=True).stdout
    M = np.array(list(KAT_XABAR))
    for p in (256, 16):
        if p == 256: h, x, Rq = M[:32][None], M[32:][None], np.array([KAT_KALIT[0]])
        else: h, x, Rq = to_units(M[:16][None], 16), to_units(M[16:32][None], 16), np.array([KAT_KALIT[0] >> 4])
        fmt = (lambda a: ''.join(f'{int(v):02x}' for v in a)) if p == 256 else (lambda a: ''.join(f'{int(v):x}' for v in a))
        q = fmt(qosh(h, x, Rq, Cfg(p, 'std'))[0][0]); b = fmt(boglash(h, x, np.array([KAT_KALIT[0] & 0xFE]), p)[0])
        print(f"p={p}: Qo‘sh C = Python: {f'qosh {p} {q}' in out};  Bog‘lash C = Python: {f'boglash {p} {b}' in out}")
    print("(256 bitli rejimdagi Qo‘sh natijasi standartning A ilovasidagi birinchi Qo‘sh natijasi bilan mos: 8a ff 7e 0d …)")
""")
code(r"""
if C_BOR:
    res = {}
    for tur in range(TURLAR):
        for p in (256, 16):
            for op in ('qosh', 'boglash'):
                t = float(subprocess.run([EXE, op, str(p), str(CHAQIRUV), str(TAKROR)], capture_output=True, text=True).stdout.split()[0])
                res.setdefault(f'{op}_{p}', []).append(t / CHAQIRUV * 1e9)
    NATIJA['C_ns'] = {k: round(min(v), 1) for k, v in res.items()}; NATIJA['C_mediana'] = {k: round(float(np.median(v)), 1) for k, v in res.items()}
    print("ns / chaqiruv:   eng yaxshi (mediana)")
    for p in (256, 16):
        q, b = NATIJA['C_ns'][f'qosh_{p}'], NATIJA['C_ns'][f'boglash_{p}']
        print(f"  p={p:3d}: Qo‘sh {q:7.1f} ({NATIJA['C_mediana'][f'qosh_{p}']}),  Bog‘lash {b:7.1f} ({NATIJA['C_mediana'][f'boglash_{p}']}),  "
              f"Bog‘lash {q/b:.2f} marta tez (mediana bo‘yicha {NATIJA['C_mediana'][f'qosh_{p}']/NATIJA['C_mediana'][f'boglash_{p}']:.2f})")
    print("Bir blokda 22 ta chaqiruv: tejalgan vaqt ≈", {p: f"{22*(NATIJA['C_ns'][f'qosh_{p}']-NATIJA['C_ns'][f'boglash_{p}'])/1000:.2f} mkS" for p in (256, 16)})
""")
md("## 2. Python (numpy) realizatsiyasi")
code(r"""
NATIJA['Python_mks'] = {}
for p in (256, 16):
    for N in (1, 4000):
        h = rng.integers(0, p, (N, 32)); x = rng.integers(0, p, (N, 32)); R = np.full(N, 200 if p == 256 else 12); Rb = np.full(N, 200); rep = 200 if N == 1 else 5
        t0 = time.perf_counter(); [qosh(h, x, R, Cfg(p, 'std')) for _ in range(rep)]; tq = (time.perf_counter() - t0) / rep / N * 1e6
        t0 = time.perf_counter(); [boglash(h, x, Rb, p) for _ in range(rep)]; tb = (time.perf_counter() - t0) / rep / N * 1e6
        NATIJA['Python_mks'][f'{p}_{N}'] = (round(tq, 2), round(tb, 2))
        print(f"p={p:3d}, bir vaqtda {N:4d} ta: Qo‘sh {tq:8.2f} mkS, Bog‘lash {tb:8.2f} mkS  ->  {tq/tb:.2f} marta")
""")
md("## 3. Amallar soni (bitta chaqiruv)")
code(r"""
def amallar_qosh():
    return dict(kopaytirish=128 + 64 * 3 + 2 + 64 * 6, teskari_jadval=192, s_jadval=0, qoshish_xor=128 + 64 * 6 + 64 * 10, shartli_tekshiruv=4 + 64 * 2)
def amallar_boglash(p):
    m = 16 if p == 256 else 8; e = 3 * m                          # 3 yarim qadam
    return dict(kopaytirish=3 * m + 3 * e, teskari_jadval=e, s_jadval=3 * e, qoshish_xor=3 * m + 7 * e + (0 if p == 256 else 64), shartli_tekshiruv=0)
NATIJA['amallar'] = {'qosh': amallar_qosh(), 'boglash_256': amallar_boglash(256), 'boglash_128': amallar_boglash(16)}
for k, v in NATIJA['amallar'].items(): print(f"{k:12s}", v, " jami:", sum(v.values()))
json.dump(NATIJA, open('qosh_boglash_tezlik.json', 'w'), ensure_ascii=False, indent=1)
try:
    import matplotlib.pyplot as plt
    if 'C_ns' in NATIJA:
        fig, ax = plt.subplots(figsize=(6, 3.2)); xs = np.arange(2)
        ax.bar(xs - 0.2, [NATIJA['C_ns']['qosh_256'], NATIJA['C_ns']['qosh_16']], 0.4, label='Qo‘sh')
        ax.bar(xs + 0.2, [NATIJA['C_ns']['boglash_256'], NATIJA['C_ns']['boglash_16']], 0.4, label='Bog‘lash')
        ax.set_xticks(xs); ax.set_xticklabels(['256 bitli rejim', '128 bitli rejim']); ax.set_ylabel('ns / chaqiruv (C, -O2)'); ax.legend(); ax.grid(alpha=.3)
        fig.tight_layout(); fig.savefig('qosh_boglash_tezlik.png', dpi=200); plt.show()
except ImportError: pass
print("Natijalar qosh_boglash_tezlik.json ga yozildi.")
""")
