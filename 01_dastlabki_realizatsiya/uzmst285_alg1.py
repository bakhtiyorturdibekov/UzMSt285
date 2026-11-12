"""
O'zMSt 285:2024, 1-algoritm (256 bitli rejim, p = 256) - ma'lumot uchun ishlab chiqilgan
mustaqil dasturiy realizatsiya. A ilovadagi nazorat misolini bayt-ma-bayt takrorlaydi.

Standart matni ochiq qoldirgan joylarda A ilova bo'yicha aniqlangan talqinlar:
  * R = kalitning BIRINCHI bayti (k[0] = 0xC8, ya'ni 1 dan sanalganda k[1]);
  * kirish bloklari va kalit 4x8 massivga SATR bo'yicha joylashtiriladi;
  * K1h = П h[s,u] da juft elementlar faqat ko'paytmada +1 qilinadi (elementning o'zi o'zgarmaydi);
  * K uchun Δ=10 sharti boshqa massiv yig'indisi bilan solishtiriladi (K1h <-> J1hn);
  * uzunlik bloki = xabar uzunligi BITLARDA, 256 bitli big-endian son;
  * NY = asosiy qism bloklarining 2^256 modul bo'yicha yig'indisi (big-endian).
Eslatma: A2 uchun Δ sharti va NY dagi ko'chirish (carry) yo'nalishi misolda sinalmaydi.
"""
P = 256
# B ilova (majburiy): 1x256 chiziqli zichlash massivi, satr = yuqori yarim bayt
ZICHLASH = bytes.fromhex(
    "050d060b010a0f0800040709020c030e"
    "0807020e0f030b06010c0d0a05040900"
    "0e020d040c07010b06090005030a080f"
    "000e090c030d07040f0605010b020a08"
    "030a0702040c09010e0d0f0800050b06"
    "02030108000e05090c0b06070a0f0d04"
    "0a040e0f090508020b0001030c06070d"
    "0b090a0106040d0f03050e000807020c"
    "010003070d0b0a0c090e04060f080502"
    "04080b090e0602050a030c0f070d0001"
    "090c0f0002010e0a05080b0d04030607"
    "060b080d07090003040f0a020e010c05"
    "0f0100050a0803070d02090c060e040b"
    "0c05040a0b02060d0807030e01000f09"
    "070f0c060500040e020a080b0d090103"
    "0d060503080f0c0007010204090b0e0a")
assert len(ZICHLASH) == 256

def _inv(x): return pow(x % P, -1, P)
def _prod_odd(a):
    p = 1
    for x in a: p = p * (x + 1 if x % 2 == 0 else x) % P
    return p
def _delta_k(prod, j_other): return 10 if prod in ((j_other + 1) % P, -(j_other + 1) % P) else 0
def _step(x, A, B, R): return (-A * x * _inv(B + R * x)) % P

def qosh(h, hn, R):
    """h, hn - 32 elementli ro'yxatlar (4x8 satr bo'yicha). Har bir element 'x = -3' darajaga."""
    J1h, J1hn = sum(h) % P, sum(hn) % P
    K1h = (_prod_odd(h) + _delta_k(_prod_odd(h), J1hn)) % P
    K1hn = (_prod_odd(hn) + _delta_k(_prod_odd(hn), J1h)) % P
    dA_h, dA_hn = (0 if J1hn % 2 else 1), (0 if J1h % 2 else 1)
    A1h = [(J1hn + 2 * y + dA_h) % P for y in hn]
    A1hn = [(J1h + 2 * x + dA_hn) % P for x in h]
    h1 = [_step(x, A1h[i], (K1h - 2 * x) % P, R) for i, x in enumerate(h)]
    hn1 = [_step(y, A1hn[i], (K1hn - 2 * y) % P, R) for i, y in enumerate(hn)]
    J2h, J2hn = sum(h1) % P, sum(hn1) % P
    K2h = (_prod_odd(h1) + _delta_k(_prod_odd(h1), J2hn)) % P
    K2hn = (_prod_odd(hn1) + _delta_k(_prod_odd(hn1), J2h)) % P
    dA2_h = 0 if (J1hn + J2hn) % 2 else 1      # talqin: A2h paritetini toq qiladigan shart
    dA2_hn = 0 if (J1h + J2h) % 2 else 1
    oh, ohn = [], []
    for i in range(32):
        for x, J1o, J2o, yo, dA, K1, K2, out in ((h1[i], J1hn, J2hn, hn1[i], dA2_h, K1h, K2h, oh),
                                                  (hn1[i], J1h, J2h, h1[i], dA2_hn, K1hn, K2hn, ohn)):
            A2 = (J1o + J2o + 2 * yo + dA) % P or 1
            B2 = (K1 * K2 - 2 * x) % P
            x2 = _step(x, A2, B2, R)
            if x2 == 0: x2 = (A2 + B2) % P
            out.append(_step(x2, A2, B2, R))
    return oh, ohn

def bayt_zichlash(h, hn):
    return [(ZICHLASH[a] << 4) | ZICHLASH[b] for a, b in zip(h, hn)]

def _dia(H, K):
    R = [[0] * 4 for _ in range(4)]
    for s in range(4):
        for u in range(4):
            sk = sum(K[i][u] for i in range(4))
            if s == u:
                v = H[u][u] * sk - sum(H[i][i] * K[i][u] for i in range(4) if i != u)
            else:
                v = (H[s][u] * sk + K[s][u] * sum(H[i][u] for i in range(4))
                     - sum(H[s][i] * K[i][u] for i in range(4) if i not in (s, u)))
            R[s][u] = v % P
    return R

def aralash(h, ke):
    H = [h[8 * s:8 * s + 8] for s in range(4)]; K = [ke[8 * s:8 * s + 8] for s in range(4)]
    L = _dia([r[:4] for r in H], [r[:4] for r in K]); Rr = _dia([r[4:] for r in H], [r[4:] for r in K])
    return [x for s in range(4) for x in L[s] + Rr[s]]

def _rot(a, n): n %= len(a); return a[-n:] + a[:-n]
def _shift(h, row_right, col_down):
    m = [_rot(h[8 * s:8 * s + 8], row_right[s]) for s in range(4)]
    for u, n in col_down.items():
        c = _rot([m[s][u] for s in range(4)], n)
        for s in range(4): m[s][u] = c[s]
    return [x for r in m for x in r]
def sur_holat(h): return _shift(h, [1, 2, 3, 4], {0: 1, 4: 1, 1: 2, 5: 2, 2: 3, 6: 3})
def sur_kalit(ke): return _shift(ke, [4, 3, 2, 1], {1: -3, 5: -3, 2: -2, 6: -2, 3: -1, 7: -1})

def tuzilma_kalit(ke, k):
    out = []
    for x, kv in zip(ke, k):
        if x == 0 and kv % 2 == 0: out.append(2)
        elif x != 0 and x % 2 == kv % 2: out.append(x)
        else: out.append((x - 1) % P)
    return out

def xesh(M: bytes, k: bytes) -> bytes:
    assert len(k) == 32
    bits = len(M) * 8
    M = M + b"\x00" * (-len(M) % 32) if M else b"\x00" * 32
    bloklar = [list(M[i:i + 32]) for i in range(0, len(M), 32)]
    ny = sum(int.from_bytes(bytes(b), "big") for b in bloklar) % 2 ** 256
    kirish = bloklar + [list(bits.to_bytes(32, "big")), list(ny.to_bytes(32, "big"))]
    k = list(k); R = k[0]; ke = k[:]; holat = kirish[0]
    for i in range(1, len(kirish)):                   # i = 1 .. b+1
        blok = kirish[i]
        holat, holatn = qosh(holat, blok, R); holat = bayt_zichlash(holat, holatn)
        for j in range(1, 11):
            holat = aralash(holat, ke)
            holat, ke = qosh(holat, ke, R)
            holat, ke = sur_holat(holat), sur_kalit(ke)
            if j == 8:
                holat, holatn = qosh(holat, blok, R); holat = bayt_zichlash(holat, holatn)
            else:
                holat, ke = qosh(holat, ke, R)
            ke = tuzilma_kalit(ke, k)
            if j == 9:
                holat, holatn = qosh(holat, blok, R); holat = bayt_zichlash(holat, holatn)
    return bytes(holat)

if __name__ == "__main__":
    M = b"funksiyaxeshirovaniyainformasionnayatexnologiyakriptograficheska"
    k = bytes.fromhex("c86ed4b2756df1cd6b6eca81d4418092" "21ab81bba0c7c15044be8feb934f95a2")
    kutilgan = bytes.fromhex("55394f2d84fccd4d8d01d8fef756cd65" "7ebecc3f96f81e5207767447de66e2b6")
    natija = xesh(M, k)
    print("Natija  :", natija.hex(" "))
    print("A ilova :", kutilgan.hex(" "))
    print("MOS KELDI" if natija == kutilgan else "MOS KELMADI")
