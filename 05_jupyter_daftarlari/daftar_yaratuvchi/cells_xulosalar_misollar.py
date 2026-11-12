SETUP = '# 0-hujayra. Dastur modullarini yuklash.\n# Daftar mustaqil ishlaydi: agar algoritm.py va boshqa modullar shu papkada bo\'lmasa,\n# ularning quyida keltirilgan matni xotirada modul sifatida yaratiladi.\nimport sys, types, importlib.util\n_MODULLAR = {\n    \'algoritm\': \'"""\\nO‘zMSt 285:2024, 1-algoritm: vektorlashtirilgan realizatsiya.\\nVariantlar: p = 256 yoki p = 16; yutish o‘zgartirishi bz = \\\'std\\\' (BaytZichlash) yoki \\\'sbz\\\' (S(h ⊕ S(n))).\\nBarcha funksiyalar (N, 32) o‘lchamli numpy massivlar ustida ishlaydi: bir vaqtda N ta mustaqil hisob.\\n"""\\nimport numpy as np\\n\\n# B ilova (majburiy): 1x256 chiziqli zichlash massivi (satr — yuqori yarim bayt)\\nZICHLASH = bytes.fromhex(\\n    "050d060b010a0f0800040709020c030e"\\n    "0807020e0f030b06010c0d0a05040900"\\n    "0e020d040c07010b06090005030a080f"\\n    "000e090c030d07040f0605010b020a08"\\n    "030a0702040c09010e0d0f0800050b06"\\n    "02030108000e05090c0b06070a0f0d04"\\n    "0a040e0f090508020b0001030c06070d"\\n    "0b090a0106040d0f03050e000807020c"\\n    "010003070d0b0a0c090e04060f080502"\\n    "04080b090e0602050a030c0f070d0001"\\n    "090c0f0002010e0a05080b0d04030607"\\n    "060b080d07090003040f0a020e010c05"\\n    "0f0100050a0803070d02090c060e040b"\\n    "0c05040a0b02060d0807030e01000f09"\\n    "070f0c060500040e020a080b0d090103"\\n    "0d060503080f0c0007010204090b0e0a")\\nZ = np.array(list(ZICHLASH), dtype=np.int64)\\ndef aes_sbox():\\n    s=[0]*256; p=q=1\\n    while True:\\n        p ^= (p<<1) ^ (0x1b if p&0x80 else 0); p&=0xff\\n        q ^= q<<1; q ^= q<<2; q ^= q<<4; q&=0xff\\n        if q&0x80: q^=0x09\\n        x=q ^ ((q<<1|q>>7)&0xff) ^ ((q<<2|q>>6)&0xff) ^ ((q<<3|q>>5)&0xff) ^ ((q<<4|q>>4)&0xff)\\n        s[p]=x^0x63\\n        if p==1: break\\n    s[0]=0x63; return np.array(s,dtype=np.int64)\\nS=aes_sbox()\\nclass Cfg:\\n    def __init__(s,p=256,bz=\\\'sbz\\\'):\\n        s.p=p; s.bz=bz\\n        s.INV=np.zeros(p,dtype=np.int64)\\n        for x in range(1,p,2): s.INV[x]=pow(x,-1,p)\\ndef prododd(a,p):\\n    b=np.where(a%2==0,a+1,a)%p; r=np.ones(a.shape[0],dtype=np.int64)\\n    for i in range(a.shape[1]): r=(r*b[:,i])%p\\n    return r\\ndef dK(P,Jo,p): return np.where((P==(Jo+1)%p)|(P==(-(Jo+1))%p),10,0)\\ndef step(x,A,B,R,c):\\n    d=(B+R*x)%c.p; return (-A*x*c.INV[d])%c.p\\ndef qosh(h,hn,R,c):\\n    p=c.p; R=R[:,None]\\n    J1h=h.sum(1)%p; J1hn=hn.sum(1)%p\\n    Ph=prododd(h,p); Phn=prododd(hn,p)\\n    K1h=(Ph+dK(Ph,J1hn,p))%p; K1hn=(Phn+dK(Phn,J1h,p))%p\\n    dAh=np.where(J1hn%2==1,0,1); dAhn=np.where(J1h%2==1,0,1)\\n    A1h=(J1hn[:,None]+2*hn+dAh[:,None])%p; A1hn=(J1h[:,None]+2*h+dAhn[:,None])%p\\n    h1=step(h,A1h,(K1h[:,None]-2*h)%p,R,c); hn1=step(hn,A1hn,(K1hn[:,None]-2*hn)%p,R,c)\\n    J2h=h1.sum(1)%p; J2hn=hn1.sum(1)%p\\n    P2h=prododd(h1,p); P2hn=prododd(hn1,p)\\n    K2h=(P2h+dK(P2h,J2hn,p))%p; K2hn=(P2hn+dK(P2hn,J2h,p))%p\\n    dA2h=np.where((J1hn+J2hn)%2==1,0,1); dA2hn=np.where((J1h+J2h)%2==1,0,1)\\n    A2h=(J1hn[:,None]+J2hn[:,None]+2*hn1+dA2h[:,None])%p; A2h=np.where(A2h==0,1,A2h)\\n    A2hn=(J1h[:,None]+J2h[:,None]+2*h1+dA2hn[:,None])%p; A2hn=np.where(A2hn==0,1,A2hn)\\n    B2h=((K1h*K2h)[:,None]-2*h1)%p; B2hn=((K1hn*K2hn)[:,None]-2*hn1)%p\\n    h2=step(h1,A2h,B2h,R,c); h2=np.where(h2==0,(A2h+B2h)%p,h2)\\n    hn2=step(hn1,A2hn,B2hn,R,c); hn2=np.where(hn2==0,(A2hn+B2hn)%p,hn2)\\n    return step(h2,A2h,B2h,R,c), step(hn2,A2hn,B2hn,R,c)\\ndef bzf(h,hn,c):\\n    if c.p==256:\\n        if c.bz==\\\'std\\\': return (Z[h]<<4)|Z[hn]\\n        return S[h^S[hn]]\\n    if c.bz==\\\'std\\\': return h^hn\\n    H=16*h[:,0::2]+h[:,1::2]; N=16*hn[:,0::2]+hn[:,1::2]; Q=S[H^S[N]]\\n    out=np.empty_like(h); out[:,0::2]=Q>>4; out[:,1::2]=Q&15; return out\\ndef dia(H,K,p):  # H,K: (N,4,4)\\n    sk=K.sum(1)            # sum_i K[i,u]  -> (N,4)\\n    sh=H.sum(1)            # sum_i H[i,u]\\n    R=np.empty_like(H)\\n    for s in range(4):\\n        for u in range(4):\\n            if s==u:\\n                v=H[:,u,u]*sk[:,u]-sum(H[:,i,i]*K[:,i,u] for i in range(4) if i!=u)\\n            else:\\n                v=H[:,s,u]*sk[:,u]+K[:,s,u]*sh[:,u]-sum(H[:,s,i]*K[:,i,u] for i in range(4) if i not in (s,u))\\n            R[:,s,u]=v%p\\n    return R\\ndef aralash(h,ke,c):\\n    H=h.reshape(-1,4,8); K=ke.reshape(-1,4,8)\\n    L=dia(H[:,:,:4],K[:,:,:4],c.p); Rr=dia(H[:,:,4:],K[:,:,4:],c.p)\\n    return np.concatenate([L,Rr],axis=2).reshape(-1,32)\\ndef _shift(h,rows,cols):\\n    m=h.reshape(-1,4,8).copy()\\n    for s in range(4): m[:,s,:]=np.roll(m[:,s,:],rows[s],axis=1)\\n    for u,n in cols.items(): m[:,:,u]=np.roll(m[:,:,u],n,axis=1)\\n    return m.reshape(-1,32)\\ndef surholat(h): return _shift(h,[1,2,3,4],{0:1,4:1,1:2,5:2,2:3,6:3})\\ndef surkalit(ke): return _shift(ke,[4,3,2,1],{1:-3,5:-3,2:-2,6:-2,3:-1,7:-1})\\ndef tuz(ke,k,c):\\n    p=c.p\\n    return np.where((ke==0)&(k%2==0),2,np.where((ke!=0)&(ke%2==k%2),ke,(ke-1)%p))\\ndef iteration(holat,blok,ke,k,c,trace=None,rounds=10):\\n    """Bitta tashqi iteratsiya (i): Qo\\\'sh+BZ, so\\\'ng \\\'rounds\\\' ta bosqich."""\\n    R=k[:,0]\\n    def T(name,j,h,kk):\\n        if trace is not None: trace.append((name,j,h.copy(),kk.copy()))\\n    holat,hn=qosh(holat,blok,R,c); T(\\\'Qosh0\\\',0,holat,ke)\\n    holat=bzf(holat,hn,c); T(\\\'BZ0\\\',0,holat,ke)\\n    for j in range(1,rounds+1):\\n        holat=aralash(holat,ke,c); T(\\\'Aralash\\\',j,holat,ke)\\n        holat,ke=qosh(holat,ke,R,c); T(\\\'Qosh1\\\',j,holat,ke)\\n        holat=surholat(holat); ke=surkalit(ke); T(\\\'Sur\\\',j,holat,ke)\\n        if j==8:\\n            holat,hn=qosh(holat,blok,R,c); T(\\\'Qosh_inj8\\\',j,holat,ke); holat=bzf(holat,hn,c); T(\\\'BZ8\\\',j,holat,ke)\\n        else:\\n            holat,ke=qosh(holat,ke,R,c); T(\\\'Qosh2\\\',j,holat,ke)\\n        ke=tuz(ke,k,c); T(\\\'Tuz\\\',j,holat,ke)\\n        if j==9:\\n            holat,hn=qosh(holat,blok,R,c); T(\\\'Qosh_inj9\\\',j,holat,ke); holat=bzf(holat,hn,c); T(\\\'BZ9\\\',j,holat,ke)\\n    return holat,ke\\ndef to_units(b,p):\\n    b=np.asarray(b,dtype=np.int64)\\n    if p==256: return b\\n    out=np.empty(b.shape[:-1]+(b.shape[-1]*2,),dtype=np.int64); out[...,0::2]=b>>4; out[...,1::2]=b&15; return out\\ndef hash_msgs(msgs,keys,c):\\n    """msgs: (N,L) bayt, L - blok uzunligiga karrali; keys: (N,32 yoki 16)."""\\n    return _hash_core(msgs,keys,c,bits=msgs.shape[1]*8)\\ndef _hash_core(msgs,keys,c,bits):\\n    N,L=msgs.shape; bl=32 if c.p==256 else 16\\n    nb=L//bl\\n    blocks=[msgs[:,i*bl:(i+1)*bl] for i in range(nb)]\\n    ny=[0]*N\\n    nyb=np.zeros((N,bl),dtype=np.int64)\\n    for n in range(N):\\n        v=sum(int.from_bytes(bytes(b[n].tolist()),\\\'big\\\') for b in blocks)%(2**(8*bl))\\n        nyb[n]=list(v.to_bytes(bl,\\\'big\\\'))\\n    lb=np.tile(np.array(list(bits.to_bytes(bl,\\\'big\\\'))),(N,1))\\n    kir=[to_units(b,c.p) for b in blocks]+[to_units(lb,c.p),to_units(nyb,c.p)]\\n    k=to_units(keys,c.p); ke=k.copy(); holat=kir[0]\\n    for i in range(1,len(kir)): holat,ke=iteration(holat,kir[i],ke,k,c)\\n    return holat\\n\\n\\n# ------------------------------------------------------------------ nazorat qiymatlari\\nKAT_KALIT = bytes.fromhex("c86ed4b2756df1cd6b6eca81d441809221ab81bba0c7c15044be8feb934f95a2")\\nKAT_XABAR = b"funksiyaxeshirovaniyainformasionnayatexnologiyakriptograficheska"\\nKAT = {\\n    (256, \\\'std\\\'): "55394f2d84fccd4d8d01d8fef756cd657ebecc3f96f81e5207767447de66e2b6",\\n    (256, \\\'sbz\\\'): "42f97daaa8e7010bc629ca695eaa77df7ae7443a0c3ae78d205c2e025d256c96",\\n    (16, \\\'std\\\'):  "e9eaccdd4ccce2d229228c864989eb9f",\\n    (16, \\\'sbz\\\'):  "bd745e2ed572ea4246ed68482ef46c5e",\\n}\\n\\ndef xesh(xabar: bytes, kalit: bytes, p=256, bz=\\\'sbz\\\') -> bytes:\\n    """Bitta xabar uchun xesh qiymat (xabar uzunligi blok uzunligiga karrali bo‘lishi shart emas)."""\\n    bl = 32 if p == 256 else 16\\n    m = xabar + b"\\\\x00" * (-len(xabar) % bl) if xabar else b"\\\\x00" * bl\\n    # uzunlik bloki asl xabar uzunligi bo‘yicha hisoblanadi\\n    c = Cfg(p, bz)\\n    msgs = np.array([list(m)]); keys = np.array([list(kalit[:bl])])\\n    out = _hash_core(msgs, keys, c, bits=len(xabar) * 8)[0]\\n    if p == 16: out = [out[2*i] << 4 | out[2*i+1] for i in range(16)]\\n    return bytes(int(x) for x in out)\\n\\ndef nazorat():\\n    """A ilova va SBZ materialidagi nazorat qiymatlarini tekshiradi."""\\n    ok = True\\n    for (p, bz), kut in KAT.items():\\n        r = xesh(KAT_XABAR, KAT_KALIT, p, bz).hex()\\n        print(f"  p={p:3d}, {bz}: {\\\'MOS\\\' if r == kut else \\\'MOS EMAS\\\'}")\\n        ok &= (r == kut)\\n    return ok\\n\\nif __name__ == "__main__":\\n    print("Nazorat qiymatlari:"); print("Hammasi mos" if nazorat() else "XATO")\\n\',\n    \'komponentlar\': \'"""Kriptotahlil uchun umumiy yordamchi funksiyalar."""\\nimport itertools\\nimport numpy as np\\nfrom algoritm import Cfg, aralash, surholat\\n\\nPAR8 = np.array([bin(i).count(\\\'1\\\') & 1 for i in range(256)])\\nX256 = np.arange(256)\\n\\ndef kalitlar(rng, N, p):\\n    """Tasodifiy kalitlar: R (1-element) va 2-element juft (5.1.2-band talabi)."""\\n    if p == 256:\\n        k = rng.integers(0, 256, (N, 32)); k[:, 0] &= 0xFE; k[:, 1] &= 0xFE\\n    else:\\n        k = rng.integers(0, 16, (N, 32)); k[:, 0] &= 0xE; k[:, 1] &= 0xE\\n    return k\\n\\ndef wht(f):\\n    """Walsh–Adamar o‘zgartirishi (f — ±1 vektor)."""\\n    a = f.astype(np.int64).copy(); h = 1; n = len(a)\\n    while h < n:\\n        a = a.reshape(-1, 2, h); a = np.stack([a[:, 0] + a[:, 1], a[:, 0] - a[:, 1]], 1).reshape(-1); h *= 2\\n    return a\\n\\ndef lat(F, nout):\\n    """8 bitli kirishli F uchun W[β][α] = Σ (−1)^(β·F(x) ⊕ α·x); korrelyatsiya c = W/256."""\\n    W = np.zeros((1 << nout, 256), dtype=np.int64)\\n    for b in range(1 << nout):\\n        W[b] = wht(1 - 2 * PAR8[F & b])\\n    return W\\n\\ndef ddt(F, nout):\\n    """Ayirmalar matritsasi DDT[Δx][Δy] (8 bitli kirish)."""\\n    return np.array([np.bincount(F ^ F[X256 ^ d], minlength=nout) for d in range(256)])\\n\\ndef anf_deg(fbits, nv):\\n    """Boolean funksiyaning ANF darajasi (Möbius o‘zgartirishi)."""\\n    a = fbits.astype(np.uint8).copy(); h = 1; N = 1 << nv\\n    while h < N:\\n        a = a.reshape(-1, 2, h); a[:, 1] ^= a[:, 0]; a = a.reshape(-1); h *= 2\\n    wt = np.array([bin(i).count(\\\'1\\\') for i in range(N)]); nz = wt[a == 1]\\n    return int(nz.max()) if len(nz) else -1\\n\\ndef bits(v, n): return (v[:, None] >> np.arange(n)) & 1\\n\\ndef implicit_count(points, deg):\\n    """deg darajali chiziqli bog‘liq bo‘lmagan implitsit tenglamalar soni (monomlar matritsasi rangi orqali)."""\\n    npts, nv = points.shape\\n    mons = [()] + [m for d in range(1, deg + 1) for m in itertools.combinations(range(nv), d)]\\n    words = (npts + 63) // 64; cols = []\\n    for m in mons:\\n        v = np.ones(npts, dtype=np.uint8)\\n        for i in m: v &= points[:, i].astype(np.uint8)\\n        pad = np.zeros(words * 64, dtype=np.uint8); pad[:npts] = v\\n        cols.append(np.packbits(pad).view(np.uint64))\\n    A = np.array(cols); rank = 0; n = A.shape[0]\\n    for w in range(A.shape[1]):\\n        for b in range(64):\\n            if rank >= n: break\\n            mask = np.uint64(1) << np.uint64(b)\\n            idx = np.nonzero((A[rank:, w] & mask) != 0)[0]\\n            if len(idx) == 0: continue\\n            piv = rank + idx[0]\\n            if piv != rank: A[[rank, piv]] = A[[piv, rank]]\\n            rows = np.nonzero((A[:, w] & mask) != 0)[0]; rows = rows[rows != rank]\\n            A[rows] ^= A[rank]; rank += 1\\n    return len(mons) - rank, len(mons)\\n\\ndef qosh_elem(A1, B1, A2, B2, R, p=256):\\n    """Qo‘sh o‘zgartirishining bitta elementi (parametrlar belgilangan): x → x^(−3)."""\\n    x = np.arange(p); INV = np.zeros(p, dtype=np.int64)\\n    for t in range(1, p, 2): INV[t] = pow(t, -1, p)\\n    s = lambda x, A, B: (-A * x * INV[(B + R * x) % p]) % p\\n    y1 = s(x, A1, B1); y2 = s(y1, A2, B2); y2 = np.where(y2 == 0, (A2 + B2) % p, y2)\\n    return s(y2, A2, B2)\\n\\ndef tasodifiy_param(rng):\\n    A1, B1, A2, B2 = [int(rng.integers(0, 128)) * 2 + 1 for _ in range(4)]\\n    return A1, B1, A2, B2, int(rng.integers(0, 128)) * 2\\n\\ndef rank2(A):\\n    A = A.copy() % 2; r = 0\\n    for col in range(A.shape[1]):\\n        piv = [i for i in range(r, A.shape[0]) if A[i, col]]\\n        if not piv: continue\\n        A[[r, piv[0]]] = A[[piv[0], r]]\\n        for i in range(A.shape[0]):\\n            if i != r and A[i, col]: A[i] ^= A[r]\\n        r += 1\\n    return r\\n\\n# 0-qatlam matritsalari: SurHolat (P) va Aralash (M(k0))\\n_C2 = Cfg(2, \\\'std\\\')\\n_perm = surholat(np.arange(32)[None, :].copy())[0]\\nP_SUR = np.zeros((32, 32), dtype=np.int64); P_SUR[np.arange(32), _perm] = 1\\n\\ndef M_aralash(k):\\n    """h0\\\' = M(k0)·h0 (mod 2) matritsasi."""\\n    E = np.eye(32, dtype=np.int64); K = np.tile(np.asarray(k) % 2, (32, 1))\\n    return (aralash(E, K, _C2).T) % 2\\n\\ndef L_raund(k):\\n    """Yutishsiz raundning 0-qatlam matritsasi L = P·M(k0)."""\\n    return (P_SUR @ M_aralash(k)) % 2\\n\',\n    \'differensial\': \'"""\\n2-bo‘lim. Differensial kriptotahlil.\\n  1) ayirmalar matritsalari: S, Z, SBZ, Qo‘sh elementi;\\n  2) orttirmalarni raundlar va har bir akslantirish bo‘yicha kuzatish:\\n       D0a/D0b — yutishdan keyingi holatdagi 1 / 2 baytli MSB ayirmasi,\\n       D1 — iteratsiya boshidagi holatdagi 1 baytli MSB ayirmasi,\\n       D2 — kirish blokidagi 2 baytli MSB ayirmasi, D3 — kirish blokidagi 1 baytli MSB ayirmasi;\\n  3) Aralash yadrosi: nol va teng ustunli kalitlar ulushi.\\nNatija: natijalar/differensial.json\\n"""\\nimport argparse, collections, json, os\\nimport numpy as np\\nfrom algoritm import S, Z, Cfg, iteration, aralash, qosh, surholat, surkalit, tuz, bzf\\nfrom komponentlar import ddt, qosh_elem, tasodifiy_param, kalitlar, M_aralash\\n\\ndef komponentlar_tahlili(rng, trials=200):\\n    R = {}; DS = ddt(S, 256); DZ = ddt(Z, 16); x = np.arange(256)\\n    dist = lambda D: {int(a): int(b) for a, b in zip(*np.unique(D[1:], return_counts=True))}\\n    R[\\\'S_max\\\'] = int(DS[1:].max()); R[\\\'S_taqsimot\\\'] = dist(DS)\\n    R[\\\'S_bolagi\\\'] = [[int(DS[d, y]) for y in range(8)] for d in range(1, 9)]\\n    R[\\\'Z_max\\\'] = int(DZ[1:].max()); i = np.unravel_index(DZ[1:].argmax(), DZ[1:].shape)\\n    R[\\\'Z_max_joyi\\\'] = (hex(int(i[0]) + 1), hex(int(i[1]))); R[\\\'Z_taqsimot\\\'] = dist(DZ)\\n    R[\\\'Z_sonishi_mumkin_ayirmalar\\\'] = int((DZ[1:, 0] > 0).sum())\\n    for d in (0x80, 0x01, 0x96): R[f\\\'Z_satr_{d:02x}\\\'] = DZ[d].tolist()\\n    def sbz(dh, dn):\\n        if dn == 0: return DS[dh] / 256.0\\n        return sum(DS[dn, d] * DS[dh ^ d] for d in range(256) if DS[dn, d]) / 65536.0\\n    R[\\\'SBZ_dh0_dn80_max\\\'] = float(sbz(0, 0x80).max()); R[\\\'SBZ_dh80_dn0_max\\\'] = float(sbz(0x80, 0).max())\\n    R[\\\'SBZ_dh0_dn80_sonish\\\'] = float(sbz(0, 0x80)[0]); R[\\\'SBZ_dh80_dn80_sonish\\\'] = float(sbz(0x80, 0x80)[0])\\n    R[\\\'SBZ_80dan80ga\\\'] = float((DS[0x80] * DS[:, 0x80]).sum() / 65536)\\n    mx, p80, pj = [], [], {j: [] for j in range(8)}\\n    for _ in range(trials):\\n        f = qosh_elem(*tasodifiy_param(rng)); D = ddt(f, 256)\\n        mx.append(int(D[1:].max())); p80.append(D[0x80, 0x80] / 256)\\n        for j in range(8): pj[j].append(D[1 << j].max() / 256)\\n    R[\\\'Qosh_max\\\'] = int(max(mx)); R[\\\'Qosh_p(80->80)\\\'] = float(np.mean(p80))\\n    R[\\\'Qosh_2^j_eng_ehtimolli\\\'] = [round(float(np.mean(pj[j])), 4) for j in range(8)]\\n    return R\\n\\ndef raundlar_yutishsiz(holat, blok, ke, k, c, trace):\\n    """Yutishdan keyingi holatdan boshlab 1–10-raundlar (0-nuqtadagi yutishsiz)."""\\n    R = k[:, 0]\\n    def T(nm, j): trace.append((nm, j, holat.copy(), ke.copy()))\\n    for j in range(1, 11):\\n        holat = aralash(holat, ke, c); T(\\\'Aralash\\\', j)\\n        holat, ke = qosh(holat, ke, R, c); T(\\\'Qosh1\\\', j)\\n        holat = surholat(holat); ke = surkalit(ke); T(\\\'Sur\\\', j)\\n        if j == 8:\\n            holat, hn = qosh(holat, blok, R, c); T(\\\'Qosh_inj8\\\', j); holat = bzf(holat, hn, c); T(\\\'BZ8\\\', j)\\n        else:\\n            holat, ke = qosh(holat, ke, R, c); T(\\\'Qosh2\\\', j)\\n        ke = tuz(ke, k, c); T(\\\'Tuz\\\', j)\\n        if j == 9:\\n            holat, hn = qosh(holat, blok, R, c); T(\\\'Qosh_inj9\\\', j); holat = bzf(holat, hn, c); T(\\\'BZ9\\\', j)\\n\\ndef hw(a, p): return sum(((a >> i) & 1) for i in range(8 if p == 256 else 4)).sum(1)\\n\\ndef kuzatish(rng, N=2000, holatlar=(\\\'D1\\\', \\\'D2\\\', \\\'D3\\\')):\\n    R = {}\\n    for p, bz in [(256, \\\'std\\\'), (256, \\\'sbz\\\'), (16, \\\'std\\\'), (16, \\\'sbz\\\')]:\\n        c = Cfg(p, bz); msb = p // 2\\n        for case in holatlar:\\n            k = kalitlar(rng, N, p); h = rng.integers(0, p, (N, 32)); bl = rng.integers(0, p, (N, 32))\\n            h2, bl2 = h.copy(), bl.copy()\\n            if case in (\\\'D0a\\\', \\\'D1\\\'): h2[:, 0] ^= msb\\n            elif case == \\\'D0b\\\': h2[:, 0] ^= msb; h2[:, 9] ^= msb\\n            elif case == \\\'D2\\\': bl2[:, 0] ^= msb; bl2[:, 9] ^= msb\\n            else: bl2[:, 0] ^= msb\\n            t1, t2 = [], []\\n            if case.startswith(\\\'D0\\\'):\\n                raundlar_yutishsiz(h, bl, k.copy(), k, c, t1); raundlar_yutishsiz(h2, bl, k.copy(), k, c, t2)\\n            else:\\n                iteration(h, bl, k.copy(), k, c, trace=t1); iteration(h2, bl2, k.copy(), k, c, trace=t2)\\n            rows = []\\n            for (nm, j, a, ka), (_, _, b, kb) in zip(t1, t2):\\n                d, dk = a ^ b, ka ^ kb; act = (d != 0).sum(1)\\n                msbonly = (((d == 0) | (d == msb)).all(1) & ((dk == 0) | (dk == msb)).all(1)).mean()\\n                top = collections.Counter(map(bytes, np.concatenate([d, dk], 1).astype(np.uint8))).most_common(1)[0][1] / N\\n                rows.append(dict(amal=nm, raund=j, faol_holat=round(float(act.mean()), 2), faol_holat_min=int(act.min()),\\n                                 faol_ke=round(float((dk != 0).sum(1).mean()), 2), P_MSB_izi=round(float(msbonly), 4),\\n                                 eng_ehtimolli_ayirma=round(top, 4), xemming=round(float(hw(d, p).mean()), 1),\\n                                 nol_ayirma=round(float(((act == 0) & ((dk != 0).sum(1) == 0)).mean()), 4)))\\n            R[f\\\'{p}_{bz}_{case}\\\'] = rows\\n        print(f"  p={p}, {bz}: tayyor")\\n    return R\\n\\ndef yadro(rng, nkeys=300):\\n    zc = eq = 0\\n    for _ in range(nkeys):\\n        M = M_aralash(kalitlar(rng, 1, 256)[0]); cols = [tuple(M[:, i]) for i in range(32)]\\n        zc += any(sum(cc) == 0 for cc in cols); eq += len(set(cols)) < 32\\n    return {\\\'nol_ustunli_kalitlar\\\': zc / nkeys, \\\'teng_ustunli_kalitlar\\\': eq / nkeys}\\n\\nif __name__ == "__main__":\\n    ap = argparse.ArgumentParser(); ap.add_argument(\\\'--tez\\\', action=\\\'store_true\\\')\\n    a = ap.parse_args(); s = 0.15 if a.tez else 1.0\\n    os.makedirs(\\\'natijalar\\\', exist_ok=True); out = {}\\n    print("1. Ayirmalar matritsalari..."); out[\\\'komponentlar\\\'] = komponentlar_tahlili(np.random.default_rng(11), int(200 * s))\\n    print("2. Orttirmalarni kuzatish...")\\n    out[\\\'kuzatish\\\'] = kuzatish(np.random.default_rng(5), int(2000 * s), (\\\'D1\\\', \\\'D2\\\', \\\'D3\\\'))\\n    out[\\\'kuzatish\\\'].update(kuzatish(np.random.default_rng(9), int(3000 * s), (\\\'D0a\\\', \\\'D0b\\\')))\\n    print("3. Aralash yadrosi..."); out[\\\'yadro\\\'] = yadro(np.random.default_rng(31), int(300 * s))\\n    json.dump(out, open(\\\'natijalar/differensial.json\\\', \\\'w\\\'), indent=1, ensure_ascii=False)\\n    print("Saqlandi: natijalar/differensial.json")\\n\',\n    \'algebraik\': \'"""\\n3-bo‘lim. Algebraik kriptotahlil.\\n  1) implitsit tenglamalar soni va ANF darajalari: S, Z, SBZ, BaytZichlash-256, Qo‘sh elementi;\\n  2) kub testlari: r = 0…3 raunddan keyin daraja o‘sishi;\\n  3) hujum namoyishi: chiqish 0-qatlamini xabar 0-qatlamining affin funksiyasi sifatida tiklash;\\n  4) bit darajasidagi tenglamalar soni (baho modeli) va linearizatsiya murakkabligi.\\nNatija: natijalar/algebraik.json\\n"""\\nimport argparse, json, math, os\\nimport numpy as np\\nfrom algoritm import S, Z, Cfg, iteration, hash_msgs, to_units\\nfrom komponentlar import implicit_count, anf_deg, bits, qosh_elem, tasodifiy_param, kalitlar\\n\\ndef tenglamalar_va_daraja(rng, trials=50):\\n    R = {}; x = np.arange(256)\\n    R[\\\'S_kvadrat\\\'] = implicit_count(np.concatenate([bits(x, 8), bits(S[x], 8)], 1), 2)\\n    R[\\\'Z_kvadrat\\\'] = implicit_count(np.concatenate([bits(x, 8), bits(Z[x], 4)], 1), 2)\\n    R[\\\'Z_kub\\\'] = implicit_count(np.concatenate([bits(x, 8), bits(Z[x], 4)], 1), 3)\\n    f = qosh_elem(*tasodifiy_param(rng))\\n    R[\\\'Qosh_kvadrat\\\'] = implicit_count(np.concatenate([bits(x, 8), bits(f, 8)], 1), 2)\\n    R[\\\'Qosh_kub\\\'] = implicit_count(np.concatenate([bits(x, 8), bits(f, 8)], 1), 3)\\n    hh = np.arange(65536) >> 8; nn = np.arange(65536) & 255\\n    y = S[hh ^ S[nn]]; yb = (Z[hh] << 4) | Z[nn]\\n    R[\\\'SBZ_kvadrat\\\'] = implicit_count(np.concatenate([bits(hh, 8), bits(nn, 8), bits(y, 8)], 1), 2)\\n    R[\\\'BZ256_kvadrat\\\'] = implicit_count(np.concatenate([bits(hh, 8), bits(nn, 8), bits(yb, 8)], 1), 2)\\n    R[\\\'S_daraja\\\'] = [anf_deg((S >> j) & 1, 8) for j in range(8)]\\n    R[\\\'Z_daraja\\\'] = [anf_deg((Z >> j) & 1, 8) for j in range(4)]\\n    R[\\\'SBZ_daraja\\\'] = [anf_deg((y >> j) & 1, 16) for j in range(8)]\\n    R[\\\'BZ256_daraja\\\'] = [anf_deg((yb >> j) & 1, 16) for j in range(8)]\\n    D = np.array([[anf_deg((qosh_elem(*tasodifiy_param(rng)) >> j) & 1, 8) for j in range(8)] for _ in range(trials)])\\n    R[\\\'Qosh_daraja_min\\\'] = D.min(0).tolist(); R[\\\'Qosh_daraja_mediana\\\'] = np.median(D, 0).tolist(); R[\\\'Qosh_daraja_max\\\'] = D.max(0).tolist()\\n    return R\\n\\ndef kub_testlari(rng, dlar=(2, 4, 6, 8, 10, 12), raundlar=(0, 1, 2, 3), ncubes=4):\\n    """Xabarning dastlabki 16 bitidan d ta bit; 4 ta kub bo‘yicha yig‘indisi doim nol bo‘lgan bitlar ulushi."""\\n    R = {}\\n    for p, bz in [(256, \\\'std\\\'), (256, \\\'sbz\\\'), (16, \\\'std\\\'), (16, \\\'sbz\\\')]:\\n        c = Cfg(p, bz); ub = 8 if p == 256 else 4\\n        for r in raundlar:\\n            row = {}\\n            for d in dlar:\\n                k = kalitlar(rng, 1, p)[0]; h = rng.integers(0, p, 32); bl = rng.integers(0, p, 32); allz = None\\n                for _ in range(ncubes):\\n                    pos = rng.choice(16, d, replace=False); base = bl.copy(); base[:16 // ub] = rng.integers(0, p, 16 // ub)\\n                    N = 1 << d; Bm = np.tile(base, (N, 1))\\n                    for t, q in enumerate(pos):\\n                        u, b = q // ub, q % ub; Bm[:, u] &= ~(1 << b); Bm[:, u] |= ((np.arange(N) >> t) & 1) << b\\n                    K = np.tile(k, (N, 1)); out, _ = iteration(np.tile(h, (N, 1)), Bm, K.copy(), K, c, rounds=r)\\n                    s = np.bitwise_xor.reduce(out, axis=0); zb = np.array([(s >> j) & 1 for j in range(ub)]).T == 0\\n                    allz = zb if allz is None else (allz & zb)\\n                row[str(d)] = {\\\'barcha_bitlar\\\': round(float(allz.mean()), 3), \\\'0-qatlam\\\': round(float(allz[:, 0].mean()), 3)}\\n            R[f\\\'{p}_{bz}_r{r}\\\'] = row\\n            print(f"  p={p}, {bz}, r={r}: " + ", ".join(f"d={d}:{v[\\\'barcha_bitlar\\\']}" for d, v in row.items()))\\n    return R\\n\\ndef gf2_solve(X, Y):\\n    A = np.concatenate([X, Y], 1).astype(np.uint8) % 2; m, n = X.shape; r = 0; piv = []\\n    for col in range(n):\\n        idx = [i for i in range(r, m) if A[i, col]]\\n        if not idx: continue\\n        A[[r, idx[0]]] = A[[idx[0], r]]\\n        for i in range(m):\\n            if i != r and A[i, col]: A[i] ^= A[r]\\n        piv.append(col); r += 1\\n    W = np.zeros((n, Y.shape[1]), dtype=np.uint8)\\n    for i, col in enumerate(piv): W[col] = A[i, n:]\\n    return W\\n\\ndef linearizatsiya_hujumi(rng, n_oquv=80, n_sinov=300):\\n    R = {}\\n    for p, bz in [(16, \\\'std\\\'), (16, \\\'sbz\\\'), (256, \\\'std\\\'), (256, \\\'sbz\\\')]:\\n        c = Cfg(p, bz); bl = 32 if p == 256 else 16\\n        if p == 256: k = rng.integers(0, 256, 32); k[0] &= 0xFE; k[1] &= 0xFE\\n        else: k = rng.integers(0, 256, 16); k[0] &= 0xEE\\n        H = lambda m: hash_msgs(m, np.tile(k, (len(m), 1)), c)\\n        feats = lambda m: np.concatenate([to_units(m, p) % 2, np.ones((len(m), 1), dtype=np.int64)], 1)\\n        tr = rng.integers(0, 256, (n_oquv, bl)); te = rng.integers(0, 256, (n_sinov, bl))\\n        W = gf2_solve(feats(tr), H(tr) % 2); pred = (feats(te) @ W) % 2; act = H(te) % 2\\n        R[f\\\'{p}_{bz}\\\'] = {\\\'toliq_32_bit\\\': float((pred == act).all(1).mean()), \\\'bitlar_boyicha\\\': round(float((pred == act).mean()), 4)}\\n        print(f"  p={p}, {bz}: {R[f\\\'{p}_{bz}\\\']}")\\n    return R\\n\\ndef tenglamalar_soni():\\n    """Bit darajasidagi baho modeli: (o‘zgaruvchilar, tenglamalar, nochiziqli tenglamalar)."""\\n    def counts(n, mode):\\n        w = 32; ADD = (2*n-1, 2*n-1, n-1); MUL = (n*(n+1)//2 + (n-1)*(2*n-1),) * 2 + (n*(n+1)//2 + (n-1)*(n-1),)\\n        add = lambda a, b, f=1: tuple(x + f*y for x, y in zip(a, b)); z = (0, 0, 0); q = z\\n        for _ in range(2):\\n            q = add(q, ADD, (w-1)*2); q = add(q, MUL, (w-1)*2); q = add(q, (2*n,)*3, 4); q = add(q, MUL, 1)\\n            q = add(q, ADD, w*4); q = add(q, MUL, w*9); q = add(q, ADD, w*6); q = add(q, (n,)*3, w)\\n        ar = add(add(z, MUL, 128), ADD, 144); tz = add(add(z, ADD, w), (n,)*3, w)\\n        if mode == \\\'sbz\\\': nb = w if n == 8 else w // 2; bz = (16*nb, 78*nb, 78*nb)\\n        elif n == 8: bz = (8*w, 43*2*w + 8*w, 43*2*w)\\n        else: bz = (0, n*w, 0)\\n        rnd = add(add(ar, q, 2), tz); r0 = add(q, bz)\\n        out = dict(qosh=q, aralash=ar, tuzilma=tz, yutish=bz, raund=rnd, r1=add(r0, rnd))\\n        out[\\\'r2\\\'] = add(out[\\\'r1\\\'], rnd); out[\\\'r3\\\'] = add(out[\\\'r2\\\'], rnd); return out\\n    E = {f\\\'{lab}_{m}\\\': counts(n, m) for n, lab in [(8, \\\'256\\\'), (4, \\\'128\\\')] for m in (\\\'std\\\', \\\'sbz\\\')}\\n    lc = lambda nv, d: round(2.8 * math.log2(sum(math.comb(nv, i) for i in range(d + 1))), 1)\\n    return E, {f\\\'{nv}_ozg_d{d}\\\': lc(nv, d) for nv in (128, 256) for d in (1, 4, 6, 7, 8, 13)}\\n\\nif __name__ == "__main__":\\n    ap = argparse.ArgumentParser(); ap.add_argument(\\\'--tez\\\', action=\\\'store_true\\\')\\n    a = ap.parse_args(); os.makedirs(\\\'natijalar\\\', exist_ok=True); out = {}\\n    print("1. Implitsit tenglamalar va darajalar..."); out[\\\'tenglamalar_daraja\\\'] = tenglamalar_va_daraja(np.random.default_rng(13), 10 if a.tez else 50)\\n    print("2. Kub testlari..."); out[\\\'kub\\\'] = kub_testlari(np.random.default_rng(21), dlar=(2, 4, 6, 8) if a.tez else (2, 4, 6, 8, 10, 12), raundlar=(0, 1) if a.tez else (0, 1, 2, 3))\\n    print("3. Linearizatsiya hujumi..."); out[\\\'linearizatsiya\\\'] = linearizatsiya_hujumi(np.random.default_rng(31), 80, 100 if a.tez else 300)\\n    E, LC = tenglamalar_soni(); out[\\\'tenglamalar_soni\\\'] = E; out[\\\'linearizatsiya_murakkabligi_log2\\\'] = LC\\n    json.dump(out, open(\\\'natijalar/algebraik.json\\\', \\\'w\\\'), indent=1, ensure_ascii=False, default=list)\\n    print("Saqlandi: natijalar/algebraik.json")\\n\',\n}\nfor _nom, _matn in _MODULLAR.items():\n    if importlib.util.find_spec(_nom) is not None and _nom not in sys.modules:\n        print(f"{_nom}.py — papkadagi fayldan olinadi"); continue\n    _m = types.ModuleType(_nom); _m.__file__ = f"<{_nom}>"\n    sys.modules[_nom] = _m; exec(compile(_matn, f"<{_nom}>", "exec"), _m.__dict__)\n    print(f"{_nom} — daftar ichidan yuklandi")\n'
CELLS=[]
def md(s): CELLS.append(('markdown',s.strip('\n')))
def code(s): CELLS.append(('code',s.strip('\n')))

md("""
# O‘zMSt 285:2024, 1-algoritm: kriptotahlil xulosalarini misollar bilan kuzatish

Ushbu daftar «SBZ o‘zgartirishining kriptotahlili» hisobotidagi 13 ta xulosaning har birini aniq misolda,
akslantirishlar ketma-ketligi bo‘yicha qadamma-qadam kuzatadi:
chiziqli tahlil — 5 ta, differensial tahlil — 4 ta, algebraik tahlil — 4 ta xulosa.

**Dastlabki ma’lumotlar:** standartning A ilovasidagi xeshlash kaliti va 64 baytli xabar.
Daftar mustaqil: kerakli modullar (`algoritm`, `komponentlar`, `differensial`, `algebraik`) 0-hujayrada daftar ichidan yuklanadi. Faqat `numpy` kutubxonasi kerak.
`R` lug‘atiga barcha natijalar yig‘iladi va oxirida `misollar_natijalari.json` fayliga yoziladi.
""")
CELLS.append(('code', SETUP))
code(r'''
import numpy as np, itertools, math, json
from algoritm import *
from komponentlar import *
np.set_printoptions(linewidth=140)

KALIT = np.array(list(KAT_KALIT))          # 32 bayt
XABAR = np.array(list(KAT_XABAR))          # 64 bayt
BLOK1, BLOK2 = XABAR[:32], XABAR[32:]
R = {}

def hx(a):
    """4x8 massivni o‘n oltilik jadval ko‘rinishida (satrlar ro‘yxati)."""
    a = np.asarray(a).reshape(4, 8); w = 2 if a.max() > 15 else 1
    return [' '.join(f'{int(v):0{w}x}' for v in row) for row in a]
def bx(a):
    """4x8 massivning 0-qatlami (har elementning eng kichik biti)."""
    a = np.asarray(a).reshape(4, 8) % 2
    return [' '.join(str(int(v)) for v in row) for row in a]
def chiqar(nom, a, f=hx):
    print(nom); [print('   ', s) for s in f(a)]
def iz(c, holat, blok, kalit):
    """Bitta iteratsiya izi: [(amal, raund, holat, ke), ...]."""
    tr = []; K = kalit[None]
    iteration(holat[None].copy(), blok[None].copy(), K.copy(), K, c, trace=tr)
    return [(n, j, h[0], k[0]) for n, j, h, k in tr]
def kirish_bloklari(xabar, p):
    """Asosiy qism bloklari + uzunlik bloki + NY bloki (birliklar: bayt yoki yarim bayt)."""
    bl = 32 if p == 256 else 16; nb = len(xabar) // bl
    bloks = [xabar[i*bl:(i+1)*bl] for i in range(nb)]
    ny = sum(int.from_bytes(bytes(b.tolist()), 'big') for b in bloks) % 2**(8*bl)
    return [to_units(b, p) for b in bloks] + [to_units(np.array(list((len(xabar)*8).to_bytes(bl, 'big'))), p),
                                              to_units(np.array(list(ny.to_bytes(bl, 'big'))), p)]
K16 = to_units(np.array(list(KAT_KALIT[:16])), 16)   # 128 bitli rejim kaliti (32 ta yarim bayt)

print("Nazorat qiymatlari:"); print("hammasi mos" if nazorat() else "XATO")
''')

# ===================== CHIZIQLI =====================
md("""
## 1. Chiziqli kriptotahlil

### 1-xulosa. Yutishsiz raundlar 0- va 1-bit qatlamlarni c ≈ 1 bilan o‘tkazadi

Misol: SBZ-256, A ilova kaliti va xabari, 1-iteratsiya. 0-nuqtadagi yutishdan keyingi holatning 0-qatlami
`h0` dan boshlab har bir akslantirishdan keyin 0-qatlamni nazariy bashorat qilamiz:
Aralash → `M(k0)·h0`, Qo‘sh → o‘zgarmaydi, SurHolat → `P·h0`, TuzilmaKalit → holatga ta’sir qilmaydi.
""")
code(r'''
c = Cfg(256, 'sbz'); tr = iz(c, BLOK1, BLOK2, KALIT)
Mk, Pm, L = M_aralash(KALIT), P_SUR, L_raund(KALIT)
h_bz0 = [t for t in tr if t[0] == 'BZ0'][0][2]
chiqar("0-nuqtadagi yutishdan (SBZ) keyingi holat:", h_bz0)
chiqar("uning 0-qatlami h0:", h_bz0, bx)
pred = h_bz0 % 2; qadamlar = []
for nom, j, h, ke in tr:
    if j != 1: continue
    if nom == 'Aralash': pred = (Mk @ pred) % 2
    if nom == 'Sur': pred = (Pm @ pred) % 2
    mos = int((pred == h % 2).sum())
    qadamlar.append(dict(amal=nom, holat=hx(h), qatlam0=bx(h), bashorat=bx(pred), mos=mos))
    print(f"\n1-raund, {nom}: 0-qatlamda bashorat bilan mos bitlar {mos}/32")
    chiqar("  holat:", h); chiqar("  0-qatlam (haqiqiy):", h, bx)
ke_t = [t for t in tr if t[0] == 'Tuz' and t[1] == 1][0][3]
ke_ok = bool(((ke_t % 2) == (KALIT % 2)).all())
print("\nTuzilmaKalit dan keyin ke 0-qatlami k 0-qatlamiga tengmi:", ke_ok)
pred = h_bz0 % 2; raund = []
for j in range(1, 11):
    pred = (L @ pred) % 2
    act = [t for t in tr if t[1] == j][-1][2] % 2
    raund.append(int((pred == act).sum()))
print("\nRaundlar oxirida L^j·h0 bashorati bilan mos bitlar (j = 1..10):", raund)
R['L1'] = dict(h_bz0=hx(h_bz0), h0=bx(h_bz0), qadamlar=qadamlar, raund_mos=raund, rangL=rank2(L), ke_ok=ke_ok)
''')
md("""
Endi 1-bit qatlamni tekshiramiz. Haqiqiy algoritmdagi 0-nuqta Qo‘sh o‘zgartirishining holat[0,0] elementi
uchun A, B parametrlarini hisoblab, bitta element akslantirishini barcha 256 kirish bo‘yicha tekshiramiz.
""")
code(r'''
from algoritm import prododd, dK, step
def qosh_batafsil(h, hn, Rv, p=256):
    """Qo‘sh(holat, holatn) ning holat qismi uchun barcha oraliq kattaliklar (algoritm.qosh bilan bir xil)."""
    c = Cfg(p); H, N = h[None], hn[None]; Rr = np.array([[Rv]])
    J1h, J1hn = int(h.sum() % p), int(hn.sum() % p)
    Ph, Phn = int(prododd(H, p)[0]), int(prododd(N, p)[0])
    K1h = (Ph + int(dK(np.array([Ph]), np.array([J1hn]), p)[0])) % p
    K1hn = (Phn + int(dK(np.array([Phn]), np.array([J1h]), p)[0])) % p
    A1 = (J1hn + 2 * hn + (0 if J1hn % 2 else 1)) % p; B1 = (K1h - 2 * h) % p
    x1 = step(H, A1[None], B1[None], Rr, c)[0]
    A1n = (J1h + 2 * h + (0 if J1h % 2 else 1)) % p; B1n = (K1hn - 2 * hn) % p
    xn1 = step(N, A1n[None], B1n[None], Rr, c)[0]
    J2h, J2hn = int(x1.sum() % p), int(xn1.sum() % p)
    P2h = int(prododd(x1[None], p)[0])
    K2h = (P2h + int(dK(np.array([P2h]), np.array([J2hn]), p)[0])) % p
    A2 = (J1hn + J2hn + 2 * xn1 + (0 if (J1hn + J2hn) % 2 else 1)) % p; A2 = np.where(A2 == 0, 1, A2)
    B2 = (K1h * K2h - 2 * x1) % p
    x2 = step(x1[None], A2[None], B2[None], Rr, c)[0]; x2 = np.where(x2 == 0, (A2 + B2) % p, x2)
    x3 = step(x2[None], A2[None], B2[None], Rr, c)[0]
    return dict(J1h=J1h, J1hn=J1hn, K1h=K1h, A1=A1, B1=B1, x1=x1, A2=A2, B2=B2, x2=x2, x3=x3, J2hn=J2hn, K2h=K2h)

Rv = int(KALIT[0]); q = qosh_batafsil(BLOK1, BLOK2, Rv)
print("Tekshiruv: qosh_batafsil natijasi algoritm.qosh bilan bir xilmi:",
      bool((q['x3'] == qosh(BLOK1[None], BLOK2[None], np.array([Rv]), Cfg(256))[0][0]).all()))
e = 0   # holat[0,0]
A1, B1, A2, B2 = int(q['A1'][e]), int(q['B1'][e]), int(q['A2'][e]), int(q['B2'][e])
print(f"R = {Rv:#04x}; holat[0,0] uchun A1 = {A1}, B1 = {B1}, A2 = {A2}, B2 = {B2}")
f = qosh_elem(A1, B1, A2, B2, Rv); x = np.arange(256)
y0_ok = int(((f & 1) == (x & 1)).sum())
best = max(((d, int((((f >> 1) & 1) == (((x >> 1) & 1) ^ (d * (x & 1)))).sum())) for d in (0, 1)), key=lambda t: t[1])
print(f"y0 = x0 tengligi: {y0_ok}/256 kirishda bajariladi")
print(f"y1 = x1 ⊕ {best[0]}·x0 tengligi: {best[1]}/256 kirishda bajariladi")
W = lat(f, 8); bitc = [round(float(np.abs(W[1 << j]).max() / 256), 3) for j in range(8)]
print("Har bir chiqish biti uchun eng yaxshi |c|:", bitc)
R['L1'].update(param=dict(R=Rv, A1=A1, B1=B1, A2=A2, B2=B2), y0_ok=y0_ok, y1=list(best), bitc=bitc)
''')

md("""
### 2-xulosa. Standart-128 da 0-qatlam butun xesh davomida c = 1 bilan kuzatiladi

Misol: Standart-128 (p = 16), kalit sifatida A ilova kalitining birinchi 16 bayti, 64 baytli A ilova xabari
(4 ta blok + uzunlik + NY = 6 ta kirish bloki, 5 ta iteratsiya). Bashorat qoidasi: har raundda `h0 ← L·h0`,
yutish nuqtalarida `h0 ← h0 ⊕ blok0`.
""")
code(r'''
c16 = Cfg(16, 'std'); kir = kirish_bloklari(XABAR, 16); M16 = M_aralash(K16)
holat = kir[0].copy(); ke = K16.copy(); pred = holat % 2; jurnal = []
for i in range(1, len(kir)):
    tr = []; K = K16[None]
    h_out, ke_out = iteration(holat[None], kir[i][None], ke[None].copy(), K, c16, trace=tr)
    b0 = kir[i] % 2; mos_iter = []
    for nom, j, h, kk in tr:
        if nom in ('BZ0', 'BZ8', 'BZ9'): pred = pred ^ b0
        if nom == 'Aralash': pred = (M16 @ pred) % 2
        if nom == 'Sur': pred = (P_SUR @ pred) % 2
        mos_iter.append(int((pred == h[0] % 2).sum()))
    jurnal.append(dict(iteratsiya=i, amallar=len(mos_iter), min_mos=min(mos_iter)))
    print(f"{i}-iteratsiya: {len(mos_iter)} ta akslantirishdan keyin bashorat bilan mos bitlar (minimum) = {min(mos_iter)}/32")
    holat, ke = h_out[0], ke_out[0]
xq = bytes(int(holat[2*i] << 4 | holat[2*i+1]) for i in range(16)).hex()
print("\nXesh qiymat:", xq, "(nazorat:", KAT[(16, 'std')] == xq, ")")
chiqar("Xesh qiymatning 0-qatlami (haqiqiy):", holat, bx)
chiqar("Bashorat qilingan 0-qatlam:", pred, bx)
R['L2'] = dict(jurnal=jurnal, xesh=xq, haqiqiy=bx(holat), bashorat=bx(pred), mos=int((pred == holat % 2).sum()))
''')

md("""
### 3-xulosa. Standart-256: faol bayt boshiga c ≤ 2⁻²

Avval B ilovadagi Z jadvali uchun eng yaxshi approksimatsiyani barcha 256 kirishda tekshiramiz, so‘ng
uni haqiqiy yutish nuqtasida (Qo‘sh dan keyingi holatn bayti → yangi holatning quyi yarim bayti) o‘lchaymiz.
Keyin A ilova kaliti uchun yutish qatlamlari bo‘yicha minimal faol baytlarni topamiz.
""")
code(r'''
x = np.arange(256); z = Z[x]
lhs = (z & 1) ^ ((z >> 2) & 1); rhs = (x & 1) ^ ((x >> 2) & 1) ^ ((x >> 6) & 1) ^ ((x >> 7) & 1)
agree = int((lhs == rhs).sum()); cZ = 2 * agree / 256 - 1
print(f"z0 ⊕ z2 = x0 ⊕ x2 ⊕ x6 ⊕ x7 :  {agree}/256 kirishda bajariladi,  c = {cZ}")
rng = np.random.default_rng(1); N = 20000; cs = Cfg(256, 'std')
H = rng.integers(0, 256, (N, 32)); B = rng.integers(0, 256, (N, 32)); Kk = kalitlar(rng, N, 256)
h1, hn1 = qosh(H, B, Kk[:, 0], cs); out = bzf(h1, hn1, cs)
lo = out & 15; L_ = (lo & 1) ^ ((lo >> 2) & 1); Rr = (hn1 & 1) ^ ((hn1 >> 2) & 1) ^ ((hn1 >> 6) & 1) ^ ((hn1 >> 7) & 1)
c_meas = float(2 * (L_[:, 0] == Rr[:, 0]).mean() - 1)
print(f"Algoritmdagi yutish nuqtasida (bayt 0, {N} ta tasodifiy holat): o‘lchangan c = {c_meas:.3f}")

def zanjir(Lm):
    """Qatlamlar 0, 8, 9, 0', 8', 9' bo‘yicha minimal faol baytlar va eng yaxshi niqob pozitsiyalari."""
    L8 = np.linalg.matrix_power(Lm, 8) % 2; maps = [L8, Lm, Lm, L8, Lm]
    best = {kk: (99, None) for kk in range(1, 7)}
    cands = [np.eye(32, dtype=np.int64)[list(cc)].sum(0) % 2 for w in (1, 2) for cc in itertools.combinations(range(32), w)]
    for end in range(1, 6):
        for u in cands:
            tot = int(u.sum()); cur = u; n = 1; path = [tuple(int(v) for v in np.nonzero(u)[0])]
            if tot < best[1][0]: best[1] = (tot, list(path))
            for m in range(end - 1, -1, -1):
                cur = (maps[m].T @ cur) % 2
                if cur.sum() == 0: break
                tot += int(cur.sum()); n += 1; path.append(tuple(int(v) for v in np.nonzero(cur)[0]))
                if tot < best[n][0]: best[n] = (tot, list(path))
    return best
zA = zanjir(L)
print(f"\nA ilova kaliti uchun L ning [0,3] satri: {[pos3 for pos3 in np.nonzero(L[3])[0]]} -> 0-qatlamdagi holat[0,3] biti har raundda o‘zgarmay o‘tadi")
print("A ilova kaliti: qatlamlar soni -> minimal faol baytlar; Standart-256 chegarasi log2|c| <= -2·a")
for kk in range(1, 7):
    a, path = zA[kk]
    if path: print(f"  {kk} qatlam: a = {a:2d} -> log2|c| <= {-2*a:4d};  faol pozitsiyalar (oxirgi qatlamdan orqaga): {[list(p) for p in path]}")
R['L3'] = dict(agree=agree, cZ=cZ, c_meas=round(c_meas, 3),
               zanjir={kk: (zA[kk][0], [list(p) for p in zA[kk][1]] if zA[kk][1] else None) for kk in zA})
''')

md("""
### 4-xulosa. SBZ: faol bayt boshiga c ≤ 2⁻⁶

SBZ approksimatsiyasi `y0 ⊕ ⟨2D,h⟩ ⊕ ⟨1A,n⟩ = 1` ni barcha 65536 ta (h, n) juftlikda tekshiramiz,
so‘ng A ilova kaliti va «eng yomon» kalit uchun yutish qatlamlari bo‘yicha chegaralarni hisoblaymiz.
""")
code(r'''
hh = np.arange(65536) >> 8; nn = np.arange(65536) & 255; y = S[hh ^ S[nn]]
par = lambda v, m: PAR8[v & m]
rel = (y & 1) ^ par(hh, 0x2D) ^ par(nn, 0x1A)
ones = int(rel.sum()); cS = 1 - 2 * ones / 65536
WS = lat(S, 8)
print(f"y0 ⊕ <2D,h> ⊕ <1A,n> ifodasi {ones}/65536 juftlikda 1 ga teng;  korrelyatsiya = {cS} = −2^{math.log2(-cS):.0f}")
print(f"c_S(2D→01) = {WS[1,0x2D]/256},  c_S(1A→2D) = {WS[0x2D,0x1A]/256},  ko‘paytma = {WS[1,0x2D]*WS[0x2D,0x1A]/65536}")
print("\nA ilova kaliti: SBZ chegarasi log2|c| <= −6·a")
for kk in range(1, 7):
    a = zA[kk][0]
    if a < 99: print(f"  {kk} qatlam: a = {a:2d} -> log2|c| <= {-6*a}")
rng = np.random.default_rng(9); yomon = None
for t in range(300):
    kk_ = kalitlar(rng, 1, 256)[0]; zz = zanjir(L_raund(kk_))
    if zz[4][0] >= 14: yomon = (kk_, zz); break
if yomon:
    print("\nOdatiy kalit (4 ta qatlamda >= 14 faol bayt):", bytes(int(v) for v in yomon[0]).hex())
    for kk in range(1, 7):
        a = yomon[1][kk][0]
        if a < 99: print(f"  {kk} qatlam: a = {a:2d} -> log2|c| <= {-6*a};  pozitsiyalar: {[list(p) for p in yomon[1][kk][1]]}")
R['L4'] = dict(ones=ones, c=cS, zanjir_A={kk: zA[kk][0] for kk in zA},
               yomon_kalit=bytes(int(v) for v in yomon[0]).hex() if yomon else None,
               yomon={kk: (yomon[1][kk][0], [list(p) for p in yomon[1][kk][1]] if yomon[1][kk][1] else None) for kk in yomon[1]} if yomon else None)
''')

md("""
### 5-xulosa. Chiqish 0-qatlamidagi c = 1 munosabatlar SBZ ga bog‘liq emas

Oxirgi (10-) raund yutishdan keyin bajariladi, shuning uchun xesh qiymatning 0-qatlami `L·x0` ga teng.
`wᵀ·L = 0` bo‘lgan har bir `w` vektor chiqishda `w·h0 = 0` munosabatini beradi. A ilova kaliti uchun bu
munosabatlarni topib, 1000 ta tasodifiy xabarda ikkala variant uchun tekshiramiz.
""")
code(r'''
def chap_yadro(A):
    """wᵀA = 0 tenglamasining GF(2) dagi bazisi."""
    rows = A.T.copy() % 2; n = rows.shape[1]; piv = []; r = 0
    for col in range(n):
        p_ = [i for i in range(r, rows.shape[0]) if rows[i, col]]
        if not p_: continue
        rows[[r, p_[0]]] = rows[[p_[0], r]]
        for i in range(rows.shape[0]):
            if i != r and rows[i, col]: rows[i] ^= rows[r]
        piv.append(col); r += 1
    basis = []
    for fcol in [cl for cl in range(n) if cl not in piv]:
        v = np.zeros(n, dtype=np.int64); v[fcol] = 1
        for i, pc in enumerate(piv): v[pc] = rows[i, fcol]
        basis.append(v)
    return basis
baz = chap_yadro(L)
nol_satr = [int(i) for i in np.nonzero(L.sum(1) == 0)[0]]
pos = lambda i: f"[{i//8},{i%8}]"
print(f"rang(L) = {rank2(L)}, munosabatlar soni = {len(baz)}, nol satrlar (doimiy nol bitlar) = {[pos(i) for i in nol_satr]}")
for v in baz: print("   " + " ⊕ ".join(pos(i) for i in np.nonzero(v)[0]) + " = 0")
rng = np.random.default_rng(3); msgs = rng.integers(0, 256, (1000, 64)); Kt = np.tile(KALIT, (1000, 1))
tek = {}
for bz in ('std', 'sbz'):
    out = hash_msgs(msgs, Kt, Cfg(256, bz)) % 2
    tek[bz] = [float(((out @ v) % 2 == 0).mean()) for v in baz]
    print(f"{bz}: har bir munosabatning 1000 ta xabarda bajarilish ulushi = {tek[bz]}")
R['L5'] = dict(rang=rank2(L), munosabatlar=[[pos(i) for i in np.nonzero(v)[0]] for v in baz], nol_satr=[pos(i) for i in nol_satr], tekshiruv=tek)
''')

# ===================== DIFFERENSIAL =====================
md("""
## 2. Differensial kriptotahlil

### 1-xulosa. Yutishsiz raundlar MSB izlarini ≈0,85–0,94 ehtimollik bilan o‘tkazadi

Misol: SBZ-256, A ilova kaliti. 0-nuqtadagi yutishdan keyingi holat (`h_bz0`) va undan holat[0,0] baytining
MSB biti bilan farq qiladigan ikkinchi holat olinadi. Har bir akslantirishdan keyin ayirma kuzatiladi.
""")
code(r'''
from differensial import raundlar_yutishsiz
def juft_iz(c, h, h2, blok, kalit):
    K = kalit[None]; t1, t2 = [], []
    raundlar_yutishsiz(h[None].copy(), blok[None], K.copy(), K, c, t1)
    raundlar_yutishsiz(h2[None].copy(), blok[None], K.copy(), K, c, t2)
    return [(a[0], a[1], a[2][0] ^ b[2][0], a[3][0] ^ b[3][0]) for a, b in zip(t1, t2)]
msb_only = lambda d, dk, m=0x80: bool(((d == 0) | (d == m)).all() and ((dk == 0) | (dk == m)).all())
c = Cfg(256, 'sbz'); h2 = h_bz0.copy(); h2[0] ^= 0x80
jr = juft_iz(c, h_bz0, h2, BLOK2, KALIT); D1qadam = []
for nom, j, d, dk in jr:
    if j > 2: break
    D1qadam.append(dict(amal=nom, raund=j, dh=hx(d), faol=int((d != 0).sum()), faol_ke=int((dk != 0).sum()), msb=msb_only(d, dk)))
    print(f"\n{j}-raund, {nom}: holatda {int((d!=0).sum())} ta, ke da {int((dk!=0).sum())} ta faol bayt; faqat MSB: {msb_only(d, dk)}")
    chiqar("  Δholat:", d)
xul = []
for j in range(1, 11):
    d, dk = [(t[2], t[3]) for t in jr if t[1] == j][-1]
    xul.append(dict(raund=j, faol=int((d != 0).sum()), faol_ke=int((dk != 0).sum()), msb=msb_only(d, dk)))
print("\nRaundlar oxirida (raund, faol holat, faol ke, faqat MSB):", [(r_['raund'], r_['faol'], r_['faol_ke'], r_['msb']) for r_ in xul])
rng = np.random.default_rng(9); N = 3000; Kk = kalitlar(rng, N, 256)
Hh = rng.integers(0, 256, (N, 32)); Bb = rng.integers(0, 256, (N, 32)); H2 = Hh.copy(); H2[:, 0] ^= 0x80
t1, t2 = [], []; raundlar_yutishsiz(Hh, Bb, Kk.copy(), Kk, c, t1); raundlar_yutishsiz(H2, Bb, Kk.copy(), Kk, c, t2)
stat = []
for (nm, j, a, ka), (_, _, b, kb) in zip(t1, t2):
    if nm == 'Tuz':
        d, dk = a ^ b, ka ^ kb
        stat.append(round(float((((d == 0) | (d == 0x80)).all(1) & ((dk == 0) | (dk == 0x80)).all(1)).mean()), 3))
print("MSB izining saqlanish ehtimolligi, 3000 juftlik (raund 1..10):", stat)
R['D1'] = dict(qadam=D1qadam, xulosa=xul, stat=stat)
''')

md("""
### 2-xulosa. SBZ yutish nuqtasidagi ehtimollikni 2⁻⁶ gacha kamaytiradi va bitta argumentdagi ayirma so‘nmaydi
""")
code(r'''
x = np.arange(256)
col_ok = all(len(set(int(Z[(r << 4) | cc]) for r in range(16))) == 16 for cc in range(16))
row_ok = all(len(set(int(Z[(r << 4) | cc]) for cc in range(16))) == 16 for r in range(16))
print("Z ning har bir ustuni va satri 0..15 ning o‘rin almashtirishi (lotin kvadrati):", col_ok and row_ok)
v96 = [int(v) for v in x if Z[v] == Z[v ^ 0x96]]
print(f"Z(x) = Z(x ⊕ 96) bajariladigan x lar soni: {len(v96)}/256; masalan x = {v96[0]:#04x}: Z(x) = {int(Z[v96[0]]):#x}, Z(x ⊕ 96) = {int(Z[v96[0]^0x96]):#x}")
h0, n0 = int(h_bz0[0]), int(BLOK2[0])
std = [int((Z[h0] << 4) | Z[n0]), int((Z[h0] << 4) | Z[n0 ^ 0x80])]
s1, s2 = int(S[h0 ^ S[n0]]), int(S[h0 ^ S[n0 ^ 0x80]])
print(f"\nMisol: h = {h0:#04x}, n = {n0:#04x}, n' = n ⊕ 80 = {n0^0x80:#04x}")
print(f"  Standart-256:  Z(h)‖Z(n) = {std[0]:#04x},  Z(h)‖Z(n') = {std[1]:#04x}  ->  Δ = {std[0]^std[1]:#04x}")
print(f"  SBZ:           S(h⊕S(n)) = {s1:#04x},  S(h⊕S(n')) = {s2:#04x}  ->  Δ = {s1^s2:#04x}")
cnt0 = 0
for dn in range(1, 256): cnt0 += int((S[hh ^ S[nn]] == S[hh ^ S[nn ^ dn]]).sum())
print(f"\nSBZ: Δh = 0, Δn ≠ 0 bo‘lgan barcha 255·65536 juftlikda so‘nishlar soni = {cnt0}")
both = int((S[hh ^ S[nn]] == S[(hh ^ 0x80) ^ S[nn ^ 0x80]]).sum())
print(f"SBZ: Δh = Δn = 80 da so‘nishlar: {both}/65536 = 2^{math.log2(both/65536):.1f}")
DS = ddt(S, 256); DZ = ddt(Z, 16)
print(f"Maksimal ehtimolliklar: Z — {DZ[1:].max()}/256 = {DZ[1:].max()/256:.3f};  S va SBZ — {DS[1:].max()}/256 = 2^-6;  XOR — 1")
R['D2'] = dict(lotin=col_ok and row_ok, v96=len(v96), v96_misol=[v96[0], int(Z[v96[0]])], h=h0, n=n0, std=std, sbz=[s1, s2],
               sbz_sonish_bir=cnt0, sbz_sonish_80=both, Zmax=int(DZ[1:].max()))
''')

md("""
### 3-xulosa. SBZ variantlari 8-raunddan keyin differensial chegaraga erishadi

Misol: A ilova kaliti va xabari; ikkinchi blokning 0- va 9-elementlariga MSB ayirmasi kiritiladi.
To‘rttala variantda ayirma 0-nuqtadan 9-raund yutishigacha kuzatiladi va yutish nuqtalaridagi faol elementlar
asosida iz ehtimolligi chegarasi hisoblanadi (bayt boshiga: SBZ — 2⁻⁶, Z — 2⁻²·⁶⁸, XOR — 1).
""")
code(r'''
D3 = {}
for p, bz in [(256, 'std'), (256, 'sbz'), (16, 'std'), (16, 'sbz')]:
    c = Cfg(p, bz); msb = p // 2
    if p == 256: h, b, kk = BLOK1, BLOK2, KALIT
    else:
        kir16 = kirish_bloklari(XABAR, 16); h, b, kk = kir16[0], kir16[1], K16
    b2 = b.copy(); b2[0] ^= msb; b2[9] ^= msb
    t1, t2 = iz(c, h, b, kk), iz(c, h, b2, kk)
    rows = [(nm, j, int(((x1 ^ x2) != 0).sum()), x1 ^ x2) for (nm, j, x1, k1), (_, _, x2, k2) in zip(t1, t2)]
    get = lambda nm: [r_ for r_ in rows if r_[0] == nm]
    q0, bz0 = get('Qosh0')[0], get('BZ0')[0]
    a8 = get('Qosh_inj8')[0][2]; a9 = get('Qosh_inj9')[0][2]
    per = {(256, 'std'): 2.68, (256, 'sbz'): 6.0, (16, 'std'): 0.0, (16, 'sbz'): 6.0}[(p, bz)]
    unit = 1 if p == 256 else 2        # 128 bitli rejimda bitta SBZ bayti = 2 ta yarim bayt
    r1 = [r_[2] for r_ in rows if r_[0] == 'Tuz' and r_[1] == 1][0]
    D3[f'{p}_{bz}'] = dict(faol_q0=q0[2], dbz0=hx(bz0[3]), faol_bz0=bz0[2], r1=r1, a8=a8, a9=a9,
                          chegara8=round(-per * a8 / unit, 1), chegara89=round(-per * (a8 + a9) / unit, 1))
    print(f"\n{p}-{bz}: Qo‘sh(0) dan keyin holatdagi faol: {q0[2]}; yutishdan keyin: {bz0[2]}; 1-raund: {r1}; 8-nuqtaga kirishda: {a8}; 9-nuqtaga kirishda: {a9}")
    chiqar("  yutishdan (0-nuqta) keyingi Δholat:", bz0[3])
    print(f"  chegara: 8-nuqtadan keyin log2 p <= {D3[f'{p}_{bz}']['chegara8']}, 8- va 9-nuqtalardan keyin <= {D3[f'{p}_{bz}']['chegara89']}")
R['D3'] = D3
''')

md("""
### 4-xulosa. Aralash yadrosi orqali ayirma ehtimollik 1 bilan so‘nadi

M(k0) matritsasida nol ustun bo‘lgan kalit topiladi. Shu ustunga mos holat baytiga MSB ayirmasi kiritilsa,
Aralash dan keyin ayirma to‘liq yo‘qoladi va keyingi barcha holatlar bir xil bo‘ladi (ichki kolliziya).
""")
code(r'''
rng = np.random.default_rng(4)
for t in range(500):
    kk = kalitlar(rng, 1, 256)[0]; Mm = M_aralash(kk); zc = [int(i) for i in np.nonzero(Mm.sum(0) == 0)[0]]
    if zc: break
pos_ = zc[0]; s_, u_ = pos_ // 8, pos_ % 8
print("Kalit:", bytes(int(v) for v in kk).hex()); print(f"M(k0) ning nol ustunlari: {[pos(i) for i in zc]};  tanlangan pozitsiya holat[{s_},{u_}]")
kcol = [int(kk[8*i + u_]) for i in range(4)]
print(f"Shu ustundagi ke[i,{u_}] qiymatlari: {[hex(v) for v in kcol]}  ->  juftliklari {[v % 2 for v in kcol]}")
h = rng.integers(0, 256, 32); h2 = h.copy(); h2[pos_] ^= 0x80
c = Cfg(256, 'sbz'); jr = juft_iz(c, h, h2, BLOK2, kk)
d_ar = [t for t in jr if t[0] == 'Aralash' and t[1] == 1][0][2]
chiqar("1-raund Aralash dan keyingi Δholat:", d_ar)
oxir = [t for t in jr if t[1] == 10][-1]
print("10-raunddan keyin Δholat nolmi:", bool((oxir[2] == 0).all()), "; Δke nolmi:", bool((oxir[3] == 0).all()))
R['D4'] = dict(kalit=bytes(int(v) for v in kk).hex(), nol_ustunlar=[pos(i) for i in zc], pozitsiya=[s_, u_], kcol=kcol,
               d_aralash=hx(d_ar), oxir_nol=bool((oxir[2] == 0).all() and (oxir[3] == 0).all()))
''')

# ===================== ALGEBRAIK =====================
md("""
## 3. Algebraik kriptotahlil

### 1-xulosa. Yagona yuqori darajali element — yutish nuqtasidagi o‘zgartirish
""")
code(r'''
yb = (Z[hh] << 4) | Z[nn]
deg = dict(XOR=[1]*4, Z=[anf_deg((Z >> j) & 1, 8) for j in range(4)], BaytZichlash_256=[anf_deg((yb >> j) & 1, 16) for j in range(8)],
           S=[anf_deg((S >> j) & 1, 8) for j in range(8)], SBZ=[anf_deg((y >> j) & 1, 16) for j in range(8)],
           Qosh_element=[anf_deg((f >> j) & 1, 8) for j in range(8)])
for kk_, v in deg.items(): print(f"{kk_:17s} chiqish bitlari darajalari: {v}")
print(f"(Qo‘sh — holat[0,0] elementi, parametrlar: {R['L1']['param']})")
row = Mk[0]; terms = [f"h[{i//8},{i%8}]" for i in np.nonzero(row)[0]]
print("\nA ilova kaliti uchun Aralash 0-qatlam tenglamasi:  h'[0,0]₀ =", " ⊕ ".join(terms) if terms else "0")
R['A1'] = dict(deg=deg, aralash_tengl=terms)
''')

md("""
### 2-xulosa. Tizim hajmini Qo‘sh belgilaydi, SBZ esa darajani oshiradi

A ilova ma’lumotlari bo‘yicha 0-nuqtadagi Qo‘sh o‘zgartirishining holat[0,0] elementi uchun halqa
tenglamalarini haqiqiy sonlar bilan tekshiramiz, so‘ng bit darajasidagi tenglamalar sonini taqsimlaymiz.
""")
code(r'''
e = 0; x0 = int(BLOK1[e]); x1 = int(q['x1'][e]); x2 = int(q['x2'][e]); x3 = int(q['x3'][e])
print(f"J1h = Σ holat = {q['J1h']},  J1hn = Σ holatn = {q['J1hn']},  K1h = {q['K1h']},  K2h = {q['K2h']},  J2hn = {q['J2hn']}")
print(f"A1 = J1hn + 2·hn[0,0] + Δ = {A1},   B1 = K1h − 2·h[0,0] = {B1},   A2 = {A2},   B2 = {B2},   R = {Rv}")
t1 = (x1 * (B1 + Rv * x0) + A1 * x0) % 256
t2 = (x2 * (B2 + Rv * x1) + A2 * x1) % 256
t3 = (x3 * (B2 + Rv * x2) + A2 * x2) % 256
print(f"x = {x0:#04x} -> x⁻¹ = {x1:#04x} -> x⁻² = {x2:#04x} -> x⁻³ = {x3:#04x}")
print(f"1-bosqich: x⁻¹·(B1 + R·x) + A1·x ≡ {t1} (mod 256)")
print(f"2-bosqich: x⁻²·(B2 + R·x⁻¹) + A2·x⁻¹ ≡ {t2} (mod 256)")
print(f"3-bosqich: x⁻³·(B2 + R·x⁻²) + A2·x⁻² ≡ {t3} (mod 256)")
import algebraik
E, LC = algebraik.tenglamalar_soni(); e256 = E['256_sbz']; tot = e256['raund'][0]
print(f"\nBitta raund (256, yutishsiz): {tot} o‘zgaruvchi;  2×Qo‘sh = {2*e256['qosh'][0]} ({100*2*e256['qosh'][0]/tot:.1f}%),"
      f" Aralash = {e256['aralash'][0]}, TuzilmaKalit = {e256['tuzilma'][0]};  SBZ qatlami (o‘zg., tengl., kvadrat) = {e256['yutish']}")
R['A2'] = dict(x=[x0, x1, x2, x3], A1=A1, B1=B1, A2=A2, B2=B2, J1h=q['J1h'], J1hn=q['J1hn'], K1h=q['K1h'], tekshiruv=[t1, t2, t3],
               raund=tot, qosh2=2*e256['qosh'][0], aralash=e256['aralash'][0], tuz=e256['tuzilma'][0], sbz=list(e256['yutish']),
               bz_std=list(E['256_std']['yutish']))
''')

md("""
### 3-xulosa. Standart-128 da 0-qatlam chiziqli: 80 ta so‘rov bilan 32 bit bashorat qilinadi
""")
code(r'''
rng = np.random.default_rng(31); k16b = np.array(list(KAT_KALIT[:16]))
tr_m = rng.integers(0, 256, (80, 16)); te_m = rng.integers(0, 256, (300, 16))
feats = lambda m: np.concatenate([to_units(m, 16) % 2, np.ones((len(m), 1), dtype=np.int64)], 1)
A3 = {}
for bz in ('std', 'sbz'):
    c = Cfg(16, bz); Hf = lambda m: hash_msgs(m, np.tile(k16b, (len(m), 1)), c)
    Wm = algebraik.gf2_solve(feats(tr_m), Hf(tr_m) % 2); pred = (feats(te_m) @ Wm) % 2; act = Hf(te_m) % 2
    A3[bz] = dict(toliq=float((pred == act).all(1).mean()), bit=round(float((pred == act).mean()), 4),
                  rangA=rank2(Wm[:32].T.astype(np.int64)), c_vektor=''.join(map(str, Wm[32])),
                  misollar=[(bytes(te_m[i].tolist()).hex(), ''.join(map(str, act[i])), ''.join(map(str, pred[i]))) for i in range(3)])
    print(f"\n{bz}: 32 bitning hammasi to‘g‘ri — {A3[bz]['toliq']:.3f};  bitlar bo‘yicha — {A3[bz]['bit']:.3f};  rang(A) = {A3[bz]['rangA']}")
    for m_, a_, p_ in A3[bz]['misollar']: print(f"   xabar {m_}\n     haqiqiy:  {a_}\n     bashorat: {p_}")
R['A3'] = A3
''')

md("""
### 4-xulosa. SBZ variantlari algebraik chegaraga 0-nuqtadagi yutishdan keyinoq erishadi

Kub testi misoli: xabarning 0-baytidan 7 ta bit tanlanadi va 2⁷ ta qiymat bo‘yicha holat bitlari
yig‘indisi hisoblanadi (r — 0-nuqtadan keyingi raundlar soni). Shuningdek, talab qilinadigan daraja
linearizatsiya murakkabligi bo‘yicha aniqlanadi.
""")
code(r'''
def kub(p, bz, r, poz, kalit, h, bl):
    c = Cfg(p, bz); ub = 8 if p == 256 else 4; d = len(poz); N = 1 << d; Bm = np.tile(bl, (N, 1))
    for t, q_ in enumerate(poz):
        u, b_ = q_ // ub, q_ % ub; Bm[:, u] &= ~(1 << b_); Bm[:, u] |= ((np.arange(N) >> t) & 1) << b_
    K = np.tile(kalit, (N, 1)); out, _ = iteration(np.tile(h, (N, 1)), Bm, K.copy(), K, c, rounds=r)
    s_ = np.bitwise_xor.reduce(out, axis=0); return np.array([(s_ >> j) & 1 for j in range(ub)]).T
poz = [0, 1, 2, 3, 4, 5, 6]; A4 = {}   # xabarning 0-baytidagi 7 ta bit (d = 7)
for p, bz in [(256, 'std'), (256, 'sbz'), (16, 'std'), (16, 'sbz')]:
    if p == 256: kk_, h_, b_ = KALIT, BLOK1, BLOK2
    else: kir16 = kirish_bloklari(XABAR, 16); kk_, h_, b_ = K16, kir16[0], kir16[1]
    for r in (0, 1, 3):
        sm = kub(p, bz, r, poz, kk_, h_, b_)
        A4[f'{p}_{bz}_r{r}'] = dict(nol=int((sm == 0).sum()), jami=int(sm.size), qatlam0_nol=int((sm[:, 0] == 0).sum()))
        print(f"{p}-{bz}, r={r}: yig‘indisi nol bo‘lgan bitlar {int((sm==0).sum())}/{sm.size};  0-qatlamda {int((sm[:,0]==0).sum())}/32")
lc = lambda nv, d: 2.8 * math.log2(sum(math.comb(nv, i) for i in range(d + 1)))
dmin128 = min(d for d in range(1, 30) if lc(128, d) >= 64); dmin256 = min(d for d in range(1, 30) if lc(256, d) >= 128)
print(f"\nTalab qilinadigan daraja: 128 bitli rejimda d >= {dmin128} (2^{lc(128,dmin128):.1f}), 256 bitli rejimda d >= {dmin256} (2^{lc(256,dmin256):.1f})")
print(f"Yutishdagi darajalar: XOR = 1 (2^{lc(128,1):.1f}),  Z = 6 (2^{lc(256,6):.1f}),  SBZ = 13 (2^{lc(256,13):.1f} va 2^{lc(128,13):.1f})")
R['A4'] = dict(kub=A4, poz=poz, dmin128=dmin128, dmin256=dmin256, lc={f'{nv}_{d}': round(lc(nv, d), 1) for nv in (128, 256) for d in (1, 4, 6, 7, 8, 13)})
''')
code(r'''
json.dump(R, open('misollar_natijalari.json', 'w'), ensure_ascii=False, indent=1,
          default=lambda o: o.tolist() if hasattr(o, 'tolist') else (int(o) if isinstance(o, (np.integer,)) else str(o)))
print("Natijalar misollar_natijalari.json fayliga saqlandi.")
''')
