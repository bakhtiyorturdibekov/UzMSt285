/* O'zMSt 285:2024, 1-algoritm: C realizatsiyasi (tezlikni o'lchash uchun).
   Variantlar: p = 256 yoki 16; bz = 0 (BaytZichlash) yoki 1 (SBZ);
   toq = 1 — barcha kₑ elementlari toq (2-tavsiya); sqatlam = 1 — raund ichidagi S-box qatlami (3-tavsiya). */
#include <stdint.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

static const uint8_t ZICH[256] = {
 5,13,6,11,1,10,15,8,0,4,7,9,2,12,3,14, 8,7,2,14,15,3,11,6,1,12,13,10,5,4,9,0,
 14,2,13,4,12,7,1,11,6,9,0,5,3,10,8,15, 0,14,9,12,3,13,7,4,15,6,5,1,11,2,10,8,
 3,10,7,2,4,12,9,1,14,13,15,8,0,5,11,6, 2,3,1,8,0,14,5,9,12,11,6,7,10,15,13,4,
 10,4,14,15,9,5,8,2,11,0,1,3,12,6,7,13, 11,9,10,1,6,4,13,15,3,5,14,0,8,7,2,12,
 1,0,3,7,13,11,10,12,9,14,4,6,15,8,5,2, 4,8,11,9,14,6,2,5,10,3,12,15,7,13,0,1,
 9,12,15,0,2,1,14,10,5,8,11,13,4,3,6,7, 6,11,8,13,7,9,0,3,4,15,10,2,14,1,12,5,
 15,1,0,5,10,8,3,7,13,2,9,12,6,14,4,11, 12,5,4,10,11,2,6,13,8,7,3,14,1,0,15,9,
 7,15,12,6,5,0,4,14,2,10,8,11,13,9,1,3, 13,6,5,3,8,15,12,0,7,1,2,4,9,11,14,10};
static uint8_t SB[256];
static const uint8_t PRESENT[16] = {0xC,5,6,0xB,9,0,0xA,0xD,3,0xE,0xF,8,4,7,1,2};
static uint32_t INV256[256], INV16[16];

static void init_tables(void) {
    uint8_t p = 1, q = 1;
    do {
        p = p ^ (uint8_t)(p << 1) ^ ((p & 0x80) ? 0x1B : 0);
        q ^= q << 1; q ^= q << 2; q ^= q << 4; if (q & 0x80) q ^= 0x09;
        uint8_t x = q ^ (uint8_t)((q << 1) | (q >> 7)) ^ (uint8_t)((q << 2) | (q >> 6)) ^ (uint8_t)((q << 3) | (q >> 5)) ^ (uint8_t)((q << 4) | (q >> 4));
        SB[p] = x ^ 0x63;
    } while (p != 1);
    SB[0] = 0x63;
    for (uint32_t x = 1; x < 256; x += 2) for (uint32_t y = 1; y < 256; y += 2) if (((x * y) & 255) == 1) INV256[x] = y;
    for (uint32_t x = 1; x < 16; x += 2) for (uint32_t y = 1; y < 16; y += 2) if (((x * y) & 15) == 1) INV16[x] = y;
}

typedef struct { uint32_t p, m; const uint32_t *inv; int bz, toq, sq; } cfg_t;

static inline uint32_t step(uint32_t x, uint32_t A, uint32_t B, uint32_t R, const cfg_t *c) {
    uint32_t d = (B + R * x) & c->m;
    return (0u - A * x * c->inv[d]) & c->m;
}
static inline uint32_t prododd(const uint32_t *a, const cfg_t *c) {
    uint32_t r = 1; for (int i = 0; i < 32; i++) r = (r * (a[i] | 1)) & c->m; return r;
}
static inline uint32_t dK(uint32_t P, uint32_t Jo, const cfg_t *c) {
    uint32_t t = (Jo + 1) & c->m; return (P == t || P == ((0u - t) & c->m)) ? 10 : 0;
}
static void qosh(uint32_t *h, uint32_t *hn, uint32_t R, const cfg_t *c) {
    uint32_t m = c->m, J1h = 0, J1hn = 0, h1[32], hn1[32];
    for (int i = 0; i < 32; i++) { J1h += h[i]; J1hn += hn[i]; }
    J1h &= m; J1hn &= m;
    uint32_t Ph = prododd(h, c), Phn = prododd(hn, c);
    uint32_t K1h = (Ph + dK(Ph, J1hn, c)) & m, K1hn = (Phn + dK(Phn, J1h, c)) & m;
    uint32_t dAh = (J1hn & 1) ? 0 : 1, dAhn = (J1h & 1) ? 0 : 1;
    for (int i = 0; i < 32; i++) {
        h1[i]  = step(h[i],  (J1hn + 2 * hn[i] + dAh) & m, (K1h - 2 * h[i]) & m, R, c);
        hn1[i] = step(hn[i], (J1h + 2 * h[i] + dAhn) & m, (K1hn - 2 * hn[i]) & m, R, c);
    }
    uint32_t J2h = 0, J2hn = 0;
    for (int i = 0; i < 32; i++) { J2h += h1[i]; J2hn += hn1[i]; }
    J2h &= m; J2hn &= m;
    uint32_t P2h = prododd(h1, c), P2hn = prododd(hn1, c);
    uint32_t K2h = (P2h + dK(P2h, J2hn, c)) & m, K2hn = (P2hn + dK(P2hn, J2h, c)) & m;
    uint32_t dA2h = ((J1hn + J2hn) & 1) ? 0 : 1, dA2hn = ((J1h + J2h) & 1) ? 0 : 1;
    uint32_t KKh = (K1h * K2h) & m, KKhn = (K1hn * K2hn) & m;
    for (int i = 0; i < 32; i++) {
        uint32_t A2 = (J1hn + J2hn + 2 * hn1[i] + dA2h) & m; if (!A2) A2 = 1;
        uint32_t B2 = (KKh - 2 * h1[i]) & m;
        uint32_t x2 = step(h1[i], A2, B2, R, c); if (!x2) x2 = (A2 + B2) & m;
        uint32_t A2n = (J1h + J2h + 2 * h1[i] + dA2hn) & m; if (!A2n) A2n = 1;
        uint32_t B2n = (KKhn - 2 * hn1[i]) & m;
        uint32_t y2 = step(hn1[i], A2n, B2n, R, c); if (!y2) y2 = (A2n + B2n) & m;
        h[i] = step(x2, A2, B2, R, c); hn[i] = step(y2, A2n, B2n, R, c);
    }
}
static void dia(uint32_t *h, const uint32_t *k, int off, const cfg_t *c) {
    uint32_t H[4][4], K[4][4], sk[4], sh[4], m = c->m;
    for (int s = 0; s < 4; s++) for (int u = 0; u < 4; u++) { H[s][u] = h[8 * s + off + u]; K[s][u] = k[8 * s + off + u]; }
    for (int u = 0; u < 4; u++) { sk[u] = K[0][u] + K[1][u] + K[2][u] + K[3][u]; sh[u] = H[0][u] + H[1][u] + H[2][u] + H[3][u]; }
    for (int s = 0; s < 4; s++) for (int u = 0; u < 4; u++) {
        uint32_t v;
        if (s == u) { v = H[u][u] * sk[u]; for (int i = 0; i < 4; i++) if (i != u) v -= H[i][i] * K[i][u]; }
        else { v = H[s][u] * sk[u] + K[s][u] * sh[u]; for (int i = 0; i < 4; i++) if (i != s && i != u) v -= H[s][i] * K[i][u]; }
        h[8 * s + off + u] = v & m;
    }
}
static void aralash(uint32_t *h, const uint32_t *ke, const cfg_t *c) { dia(h, ke, 0, c); dia(h, ke, 4, c); }
static void shift(uint32_t *a, const int *rows, const int *cols) {
    uint32_t t[32];
    for (int s = 0; s < 4; s++) for (int u = 0; u < 8; u++) t[8 * s + u] = a[8 * s + ((u - rows[s]) % 8 + 8) % 8];
    for (int u = 0; u < 8; u++) for (int s = 0; s < 4; s++) a[8 * s + u] = t[8 * (((s - cols[u]) % 4 + 4) % 4) + u];
}
static const int HR[4] = {1, 2, 3, 4}, HC[8] = {1, 2, 3, 0, 1, 2, 3, 0};
static const int KR[4] = {4, 3, 2, 1}, KC[8] = {0, -3, -2, -1, 0, -3, -2, -1};
static void tuz(uint32_t *ke, const uint32_t *k, const cfg_t *c) {
    for (int i = 0; i < 32; i++) {
        if (c->toq) { ke[i] |= 1; continue; }
        if (ke[i] == 0 && !(k[i] & 1)) ke[i] = 2;
        else if (ke[i] != 0 && (ke[i] & 1) == (k[i] & 1)) ;
        else ke[i] = (ke[i] - 1) & c->m;
    }
}
static void bzf(uint32_t *h, const uint32_t *hn, const cfg_t *c) {
    if (c->p == 256) {
        for (int i = 0; i < 32; i++) h[i] = c->bz ? SB[h[i] ^ SB[hn[i]]] : (uint32_t)((ZICH[h[i]] << 4) | ZICH[hn[i]]);
    } else {
        if (!c->bz) { for (int i = 0; i < 32; i++) h[i] ^= hn[i]; return; }
        for (int j = 0; j < 16; j++) {
            uint32_t H = 16 * h[2 * j] + h[2 * j + 1], N = 16 * hn[2 * j] + hn[2 * j + 1], Q = SB[H ^ SB[N]];
            h[2 * j] = Q >> 4; h[2 * j + 1] = Q & 15;
        }
    }
}
static void sqatlam(uint32_t *h, const cfg_t *c) {
    if (!c->sq) return;
    for (int i = 0; i < 32; i++) h[i] = (c->p == 256) ? SB[h[i]] : PRESENT[h[i]];
}
static void iteration(uint32_t *holat, const uint32_t *blok, uint32_t *ke, const uint32_t *k, const cfg_t *c) {
    uint32_t R = k[0], hn[32];
    if (c->toq) for (int i = 0; i < 32; i++) ke[i] |= 1;
    memcpy(hn, blok, sizeof hn); qosh(holat, hn, R, c); bzf(holat, hn, c);
    for (int j = 1; j <= 10; j++) {
        aralash(holat, ke, c);
        qosh(holat, ke, R, c);
        shift(holat, HR, HC); shift(ke, KR, KC);
        sqatlam(holat, c);
        if (j == 8) { memcpy(hn, blok, sizeof hn); qosh(holat, hn, R, c); bzf(holat, hn, c); }
        else qosh(holat, ke, R, c);
        tuz(ke, k, c);
        if (j == 9) { memcpy(hn, blok, sizeof hn); qosh(holat, hn, R, c); bzf(holat, hn, c); }
    }
}
static void units(const uint8_t *b, int bl, uint32_t *u, int p) {
    if (p == 256) for (int i = 0; i < 32; i++) u[i] = b[i];
    else for (int i = 0; i < bl; i++) { u[2 * i] = b[i] >> 4; u[2 * i + 1] = b[i] & 15; }
}
/* xesh: xabar, uzunlik (bayt), kalit (32 yoki 16 bayt) -> chiqish (32 yoki 16 bayt) */
void xesh(const uint8_t *msg, size_t len, const uint8_t *key, int p, int bz, int toq, int sq, uint8_t *out) {
    cfg_t c = {(uint32_t)p, (uint32_t)p - 1, p == 256 ? INV256 : INV16, bz, toq, sq};
    int bl = p == 256 ? 32 : 16;
    size_t nb = len ? (len + bl - 1) / bl : 1;
    uint8_t blk[32], ny[32] = {0}, lb[32] = {0};
    uint32_t holat[32], blok[32], ke[32], k[32];
    uint64_t bits = (uint64_t)len * 8;
    for (int i = 0; i < 8; i++) lb[bl - 1 - i] = (uint8_t)(bits >> (8 * i));
    units(key, bl, k, p); memcpy(ke, k, sizeof ke);
    for (size_t b = 0; b < nb + 2; b++) {
        if (b < nb) {
            memset(blk, 0, sizeof blk);
            size_t n = (b + 1) * bl <= len ? (size_t)bl : (len > b * bl ? len - b * bl : 0);
            if (n) memcpy(blk, msg + b * bl, n);
            unsigned carry = 0;
            for (int i = bl - 1; i >= 0; i--) { unsigned s = ny[i] + blk[i] + carry; ny[i] = s & 255; carry = s >> 8; }
        } else memcpy(blk, b == nb ? lb : ny, bl);
        if (b == 0) { units(blk, bl, holat, p); continue; }
        units(blk, bl, blok, p); iteration(holat, blok, ke, k, &c);
    }
    if (p == 256) for (int i = 0; i < 32; i++) out[i] = (uint8_t)holat[i];
    else for (int i = 0; i < 16; i++) out[i] = (uint8_t)(holat[2 * i] << 4 | holat[2 * i + 1]);
}
/* ---------- Bog'lash (ikkala rejim uchun yagona, bayt darajasida) ---------- */
static const int L256[16] = {0,1,2,3, 8,9,10,11, 16,17,18,19, 24,25,26,27};
static const int R256[16] = {4,5,6,7, 12,13,14,15, 20,21,22,23, 28,29,30,31};
static const int L128[8]  = {0,1, 4,5, 8,9, 12,13};
static const int R128[8]  = {2,3, 6,7, 10,11, 14,15};
static inline void yarim(uint8_t *H, const int *T, const int *U, int m, const uint8_t *X, uint32_t R) {
    uint32_t J = 0, K = 1;
    for (int i = 0; i < m; i++) { uint32_t u = H[U[i]]; J += u; K *= (u | 1); }
    J &= 255; K &= 255;
    uint32_t u0 = H[U[0]];
    for (int i = 0; i < m; i++) {
        uint32_t ui = H[U[i]], un = (i + 1 < m) ? H[U[i + 1]] : u0, xt = X[T[i]], x = H[T[i]];
        uint32_t a = 2u * SB[ui ^ X[U[i]] ^ J] + 1, b = 2u * SB[un ^ xt ^ K] + 1;
        uint32_t f = (0u - a * x * INV256[(b + R * x) & 255]) & 255;
        H[T[i]] = SB[f ^ xt];
    }
}
static void boglash(uint32_t *h, const uint32_t *x, uint32_t R, int p) {
    uint8_t H[32], X[32];
    if (p == 256) {
        for (int i = 0; i < 32; i++) { H[i] = (uint8_t)h[i]; X[i] = (uint8_t)x[i]; }
        yarim(H, R256, L256, 16, X, R); yarim(H, L256, R256, 16, X, R); yarim(H, R256, L256, 16, X, R);
        for (int i = 0; i < 32; i++) h[i] = H[i];
    } else {
        for (int j = 0; j < 16; j++) { H[j] = (uint8_t)((h[2*j] << 4) | h[2*j+1]); X[j] = (uint8_t)((x[2*j] << 4) | x[2*j+1]); }
        yarim(H, R128, L128, 8, X, R); yarim(H, L128, R128, 8, X, R); yarim(H, R128, L128, 8, X, R);
        for (int j = 0; j < 16; j++) { h[2*j] = H[j] >> 4; h[2*j+1] = H[j] & 15; }
    }
}

/* ---------- Yakuniy variant ---------- */
static uint8_t RCT[11][32];
static uint8_t C1T[32], C2T[32];
static void init_yak(void) {
    for (int j = 0; j < 11; j++) for (int i = 0; i < 32; i++) RCT[j][i] = SB[(16 * j + i) & 255];
    for (int i = 0; i < 32; i++) { C1T[i] = SB[(7 * i + 1) & 255] | 1; C2T[i] = SB[(11 * i + 3) & 255] | 1; }
}
static void iteration_y(uint32_t *holat, const uint32_t *blok, uint32_t *ke, const uint32_t *k, const cfg_t *c) {
    int p = c->p; uint32_t m = c->m;
    uint32_t R = (p == 256 ? k[0] : ((k[0] << 4) | k[1])) & 0xFE;
    for (int i = 0; i < 32; i++) ke[i] |= 1;
    boglash(holat, blok, R, p); bzf(holat, blok, c);
    for (int j = 1; j <= 10; j++) {
        aralash(holat, ke, c);
        boglash(holat, ke, R, p);
        shift(holat, HR, HC); shift(ke, KR, KC);
        for (int i = 0; i < 32; i++) ke[i] = ((ke[i] ^ (RCT[j][i] & m)) | 1);
        if (j == 8) { boglash(holat, blok, R, p); bzf(holat, blok, c); }
        else boglash(holat, ke, R, p);
        if (j == 9) { boglash(holat, blok, R, p); bzf(holat, blok, c); }
    }
}
void xesh_y(const uint8_t *msg, size_t len, const uint8_t *key, int p, uint8_t *out) {
    cfg_t c = {(uint32_t)p, (uint32_t)p - 1, p == 256 ? INV256 : INV16, 1, 0, 0};
    int bl = p == 256 ? 32 : 16; size_t nb = len ? (len + bl - 1) / bl : 1;
    uint8_t blk[32], ny[32] = {0}, lb[32] = {0};
    uint32_t holat[32], blok[32], ke[32], k[32], h0[32], c1[32], c2[32], P[32];
    uint64_t bits = (uint64_t)len * 8;
    for (int i = 0; i < 8; i++) lb[bl - 1 - i] = (uint8_t)(bits >> (8 * i));
    units(key, bl, k, p); memcpy(ke, k, sizeof ke);
    for (size_t b = 0; b < nb + 2; b++) {
        if (b < nb) {
            memset(blk, 0, sizeof blk);
            size_t n = (b + 1) * bl <= len ? (size_t)bl : (len > b * bl ? len - b * bl : 0);
            if (n) memcpy(blk, msg + b * bl, n);
            unsigned carry = 0;
            for (int i = bl - 1; i >= 0; i--) { unsigned s = ny[i] + blk[i] + carry; ny[i] = s & 255; carry = s >> 8; }
        } else memcpy(blk, b == nb ? lb : ny, bl);
        if (b == 0) { units(blk, bl, holat, p); continue; }
        units(blk, bl, blok, p); memcpy(h0, holat, sizeof h0);
        iteration_y(holat, blok, ke, k, &c);
        for (int i = 0; i < 32; i++) holat[i] ^= h0[i];                 /* oldinga uzatish */
    }
    for (int i = 0; i < 32; i++) { c1[i] = C1T[i] & c.m; c2[i] = C2T[i] & c.m; }
    memcpy(P, holat, sizeof P); boglash(P, c1, 0xC8, p); boglash(P, c2, 0xC8, p);
    for (int i = 0; i < 32; i++) holat[i] ^= P[i];                        /* chiqish o'zgartirishi */
    if (p == 256) for (int i = 0; i < 32; i++) out[i] = (uint8_t)holat[i];
    else for (int i = 0; i < 16; i++) out[i] = (uint8_t)(holat[2 * i] << 4 | holat[2 * i + 1]);
}
static double now(void) { return (double)clock() / CLOCKS_PER_SEC; }
int main(int argc, char **argv) {
    init_tables(); init_yak();
    static const uint8_t KEY[32] = {0xc8,0x6e,0xd4,0xb2,0x75,0x6d,0xf1,0xcd,0x6b,0x6e,0xca,0x81,0xd4,0x41,0x80,0x92,
                                    0x21,0xab,0x81,0xbb,0xa0,0xc7,0xc1,0x50,0x44,0xbe,0x8f,0xeb,0x93,0x4f,0x95,0xa2};
    const char *M = "funksiyaxeshirovaniyainformasionnayatexnologiyakriptograficheska";
    uint8_t out[32];
    if (argc > 1 && !strcmp(argv[1], "katy")) {
        for (int p = 256; p >= 16; p /= 16) { xesh_y((const uint8_t *)M, 64, KEY, p, out);
            printf("%d ", p); for (int i = 0; i < (p == 256 ? 32 : 16); i++) printf("%02x", out[i]); printf("\n"); }
        return 0;
    }
    if (argc > 1 && !strcmp(argv[1], "tezy")) {       /* tezy p bayt takror */
        int p = atoi(argv[2]); size_t n = (size_t)atol(argv[3]); int rep = atoi(argv[4]);
        uint8_t *buf = malloc(n); for (size_t i = 0; i < n; i++) buf[i] = (uint8_t)(i * 131 + 7);
        double best = 1e9;
        for (int r = 0; r < rep; r++) { double t = now(); xesh_y(buf, n, KEY, p, out); t = now() - t; if (t < best) best = t; }
        printf("%.6f %02x\n", best, out[0]); free(buf); return 0;
    }
    if (argc > 1 && !strcmp(argv[1], "kat")) {               /* nazorat qiymatlari */
        for (int p = 256; p >= 16; p /= 16) for (int v = 0; v < 6; v++) {
            int bz = v >= 1, toq = v >= 2, sq = v >= 3;
            if (v == 4) { bz = 0; toq = 1; sq = 0; } if (v == 5) { bz = 0; toq = 0; sq = 1; }
            xesh((const uint8_t *)M, 64, KEY, p, bz, toq, sq, out);
            printf("%d %d %d %d ", p, bz, toq, sq); for (int i = 0; i < (p == 256 ? 32 : 16); i++) printf("%02x", out[i]); printf("\n");
        }
        return 0;
    }
    /* tezlik: argv = p bz toq sq bayt_soni takror */
    int p = atoi(argv[1]), bz = atoi(argv[2]), toq = atoi(argv[3]), sq = atoi(argv[4]);
    size_t n = (size_t)atol(argv[5]); int rep = atoi(argv[6]);
    uint8_t *buf = malloc(n); for (size_t i = 0; i < n; i++) buf[i] = (uint8_t)(i * 131 + 7);
    double best = 1e9;
    for (int r = 0; r < rep; r++) { double t = now(); xesh(buf, n, KEY, p, bz, toq, sq, out); t = now() - t; if (t < best) best = t; }
    printf("%.6f %02x\n", best, out[0]);
    free(buf); return 0;
}
