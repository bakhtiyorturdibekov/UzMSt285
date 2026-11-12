import docx, copy, re
from docx.shared import Cm
from lxml import etree
import numpy as np, sys
sys.path.insert(0,'/home/claude/v')
exec(open('/home/claude/v/loc.py').read().split('h=np.arange(65536)')[0]); AES=S
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'; Mn='http://schemas.openxmlformats.org/officeDocument/2006/math'
w=lambda t:'{%s}%s'%(W,t); mq=lambda t:'{%s}%s'%(Mn,t)
d=docx.Document('merged.docx'); body=d.element.body; E=list(body.iterchildren())

def wts(el): return [x for x in el.iter(w('t'))]
def repl_text(el,old,new,count=0):
    n=0
    for t in wts(el):
        if t.text and old in t.text:
            t.text=t.text.replace(old,new); t.set('{http://www.w3.org/XML/1998/namespace}space','preserve'); n+=1
    return n
def rpr(b=False,i=False,va=None,sz=28):
    r=etree.SubElement(etree.Element(w('r')),w('rPr'))
    f=etree.SubElement(r,w('rFonts'));[f.set(w(k),'Times New Roman') for k in ('ascii','hAnsi','cs')]
    if b: etree.SubElement(r,w('b')); etree.SubElement(r,w('bCs'))
    if i: etree.SubElement(r,w('i')); etree.SubElement(r,w('iCs'))
    etree.SubElement(r,w('sz')).set(w('val'),str(sz)); etree.SubElement(r,w('szCs')).set(w('val'),str(sz))
    if va: etree.SubElement(r,w('vertAlign')).set(w('val'),va)
    return r
def run(text,**k):
    r=etree.Element(w('r')); r.append(rpr(**k)); t=etree.SubElement(r,w('t')); t.text=text
    t.set('{http://www.w3.org/XML/1998/namespace}space','preserve'); return r
TOK=re.compile(r'(\*[^*]+\*|~[^~]+~|\^[^^]+\^|§[^§]+§)')
def runs(s,sz=28,base_i=False,base_b=False):
    out=[]
    for part in TOK.split(s):
        if not part: continue
        if part[0]=='*': out.append(run(part[1:-1],b=True,i=True,sz=sz))
        elif part[0]=='~': out.append(run(part[1:-1],i=True,b=base_b,va='subscript',sz=sz))
        elif part[0]=='^': out.append(run(part[1:-1],i=base_i,b=base_b,va='superscript',sz=sz))
        elif part[0]=='§': out.append(run(part[1:-1],i=True,b=base_b,sz=sz))
        else: out.append(run(part,i=base_i,b=base_b,sz=sz))
    return out
def para(s,kind='body',sz=28):
    p=etree.Element(w('p')); pPr=etree.SubElement(p,w('pPr'))
    if kind=='bullet':
        pPr.append(copy.deepcopy(E[5].find(w('pPr')).find(w('pStyle'))))
        pPr.append(copy.deepcopy(E[5].find(w('pPr')).find(w('numPr'))))
    sp=etree.SubElement(pPr,w('spacing')); sp.set(w('after'),'0'); sp.set(w('line'),'360'); sp.set(w('lineRule'),'auto')
    if kind in('body','bullet','head'): ind=etree.SubElement(pPr,w('ind')); ind.set(w('firstLine'),'709'); 
    if kind=='bullet': ind.set(w('left'),'0')
    etree.SubElement(pPr,w('jc')).set(w('val'),{'body':'both','bullet':'both','head':'both','formula':'center','caption':'center','tcap':'right'}[kind])
    for r in runs(s,sz=sz,base_i=(kind=='formula'),base_b=(kind=='head')): p.append(r)
    return p
def insert_after(ref,new_list):
    for n in reversed(new_list): ref.addnext(n)
def pic_para(path,width_cm):
    p=d.add_paragraph(); p.add_run().add_picture(path,width=Cm(width_cm))
    el=p._p; pPr=el.get_or_add_pPr(); 
    sp=etree.SubElement(pPr,w('spacing')); sp.set(w('before'),'120'); sp.set(w('after'),'0')
    etree.SubElement(pPr,w('jc')).set(w('val'),'center'); el.getparent().remove(el); return el
KE='k~e~'

# --- 0. Kirish izohi
insert_after(E[2],[para("Ushbu bo‘limda 1-algoritm standartdagi *BaytZichlash(holat, holatn)* o‘zgartirishi o‘rniga taklif etilgan *SBZ(holat, holatn)* o‘zgartirishi bilan bayon etiladi. Standartdagi *BaytZichlash* o‘zgartirishi 256 bitli rejimda har bir bayt juftligini ikkita o‘zaro bog‘liq bo‘lmagan 8→4 jadval orqali siqadi: faqat bitta argumentdagi farq 0,156 gacha ehtimol bilan so‘nadi, holat va kirish bloki axboroti esa chiqish baytida aralashmaydi. 128 bitli rejimda XOR amali mod 16 arifmetika bilan birgalikda xesh qiymatning quyi bit-qatlamini (32 bit) xabar va kalitning quyi bit-qatlamlarining affin funksiyasiga aylantiradi, bu esa kolliziyaga bardoshlilikni ≈2^48^ gacha, kalitli rejimda kalitga bardoshlilikni ≈2^96^ gacha pasaytiradi."),
 para("*SBZ* o‘zgartirishi faqat kirish bloki holatga yutiladigan uchta nuqtada *BaytZichlash* o‘rniga qo‘llaniladi. *Qo‘sh, Aralash, SurHolat, SurKalit, TuzilmaKalit* o‘zgartirishlari, bosqichlar soni, *uzunlik* va *NY* bloklari o‘zgarishsiz qoladi.")])
# --- 1. NY, e0, SurKalit
repl_text(E[9],'o‘nlik sanoq tizimida dastlabki ma’lumotlar qiymatlari summasini','asosiy qism bloklari qiymatlarining 2²⁵⁶ (2¹²⁸) moduli bo‘yicha yig‘indisini')
for t in E[11].iter(mq('t')):
    if t.text=='+2': t.text='+1'
repl_text(E[11],') 10',')·10'); repl_text(E[11],'bo‘Igan','bo‘lgan')
om=E[16].find(mq('oMath')); idx=list(E[16]).index(om); E[16].remove(om)
for j,r in enumerate(runs('*(k*~e~*) - k*~e~')): E[16].insert(idx+j,r)
# p13: ta'rif
p13=E[13]; [p13.remove(c) for c in list(p13) if c.tag!=w('pPr')]
for r in runs("*SBZ(holat, holatn)* - *holat* va *holatn* massivlarining har bir bayti ustida (128 bitli rejimda qo‘shni yarim baytlar juftlab baytga birlashtiriladi) §S§(§h§ ⊕ §S§(§n§)) amalini bajaruvchi, kirish blokini holatga yutish uchun xeshlash protsedurasida foydalaniladigan o‘zgartirish; bu yerda §S§ — AES (FIPS 197) standartining 8 bitli o‘rniga qo‘yish jadvali (S-box);"): p13.append(r)
# p19, p24
repl_text(E[19],'to‘Idiriladi','to‘ldiriladi')
repl_text(E[24],'psevdokodi 7rasmda keltirilgan','psevdokodi 2.4.1-psevdokodda keltirilgan')
insert_after(E[24],[para("Standartning nazorat misoli (A ilova) asosida quyidagi realizatsiya kelishuvlari aniqlangan va ushbu algoritm uchun qabul qilinadi. Kirish bloklari va xeshlash kaliti 4×8 massivlarga satr bo‘yicha joylashtiriladi: §h§[§s,u§] = §x§[8§s§ + §u§]. §R§ ≡ §k§[1] — xeshlash kalitining birinchi bayti (128 bitli rejimda birinchi yarim bayti); u juft bo‘lishi shart, aks holda §B§ + §R·a§ toq §a§ uchun juft bo‘lib, *Qo‘sh* o‘zgartirishidagi teskarilash bajarilmaydi. *uzunlik* bloki xabarning bitlardagi uzunligini big-endian ko‘rinishda saqlaydi, *NY* bloki asosiy qism bloklarining blok uzunligi moduli bo‘yicha yig‘indisidir; 128 bitli rejimda *uzunlik* va *NY* bloklari ham 128 bitli. *Qo‘sh* o‘zgartirishidagi juft elementga 1 qo‘shish faqat §K§ ko‘paytmasini hisoblashda qo‘llaniladi. Xeshlash protsedurasi bosqichlarining umumiy soni (§b§+1)·10 ga teng.")])
# global BaytZichlash -> SBZ (1-algoritm qismida)
for el in E[:105]: repl_text(el,'BaytZichlash','SBZ')
# p85 kech -> ke
for t in E[85].iter(mq('t')):
    if t.text=='ech': t.text='e'
# --- SBZ bo'limi (65..72), jadval 73
repl_text(E[65],'о‘zgartirishi','o‘zgartirishi')
for i in range(66,73): body.remove(E[i])
newsec=[
 para("*SBZ(holat, holatn)* o‘zgartirishi *holat* va *holatn* massivlarining *Qo‘sh* o‘zgartirishidan keyingi qiymatlari ustida bajariladi va kirish blokini holatga yutadi. O‘zgartirishda AES (FIPS 197) standartining 8 bitli §S§ o‘rniga qo‘yish jadvali (S-box) qo‘llaniladi; uning qiymatlari 2.4.1-jadvalda keltirilgan."),
 para("Agar kirish blokining uzunligi va xeshlash kalitining uzunligi *256* bit (§p§ = 256) bo‘lsa, *holat* va *holatn* massivlari bayt darajasidagi *holat1* va *holatn1* chiziqli massivlariga keltiriladi va har bir §i§ = 0, 1, …, 31 uchun quyidagi amal bajariladi:"),
 para("holat1[i] ← S( holat1[i] ⊕ S( holatn1[i] ) ).",kind='formula'),
 para("O‘zgartirish natijasi *holat1* massividan 4×8 tartibdagi *holat* massiviga satr bo‘yicha qayta ko‘chiriladi."),
 para("Agar kirish blokining uzunligi va xeshlash kalitining uzunligi *128* bit (§p§ = 16) bo‘lsa, *holat* va *holatn* massivlarining qo‘shni yarim baytlari kirish ketma-ketligidagi tartibda juftlab baytga birlashtiriladi va har bir §j§ = 0, 1, …, 15 uchun quyidagi amallar bajariladi:"),
 para("H[j] = 16·h[2j] + h[2j+1],    N[j] = 16·hn[2j] + hn[2j+1],",kind='formula'),
 para("Q[j] = S( H[j] ⊕ S( N[j] ) ),",kind='formula'),
 para("h[2j] = Q[j] ≫ 4,    h[2j+1] = Q[j] ∧ 0x0F,",kind='formula'),
 para("bu yerda §h§ va §hn§ — mos ravishda *holat* va *holatn* massivlarining chiziqli ko‘rinishdagi elementlari. Satr bo‘yicha joylashtirishda (§h§[§s§, 2§t§], §h§[§s§, 2§t§+1]) juftlari bir satrdagi qo‘shni yarim baytlardir. 2.4.1-rasmda *SBZ* o‘zgartirishining ikkala rejim uchun sxemasi keltirilgan."),
 pic_para('/home/claude/fig/sbz.png',16.0),
 para("2.4.1-rasm. SBZ o‘zgartirishining sxemasi",kind='caption'),
 para("*SBZ* o‘zgartirishi quyidagi xossalarga ega:"),
 para("har bir argument bo‘yicha bijektivlik: §n§ tayinlanganda §h§ ↦ §S§(§h§ ⊕ §S§(§n§)) va §h§ tayinlanganda §n§ ↦ §S§(§h§ ⊕ §S§(§n§)) o‘rin almashtirish bo‘ladi, shuning uchun faqat bitta argumentdagi farq so‘nmaydi (*BaytZichlash* uchun so‘nish ehtimolligi 0,156);",kind='bullet'),
 para("ikkala argumentda farq bo‘lganda so‘nish ehtimolligi DDT~S~(Δ§n§, Δ§h§)/256 ≤ 2^−6^ dan oshmaydi; maksimal differensial ehtimollik va maksimal korrelyatsiya 2^−6^ ga teng (*BaytZichlash* uchun mos ravishda 0,156 va 0,25);",kind='bullet'),
 para("har bir chiqish biti ikkala baytning barcha 16 bitiga bog‘liq (128/128), chiqish bitlarining algebraik darajasi 13 ga teng (*BaytZichlash* uchun 64/128 va 6), SAC ko‘rsatkichi 0,453…0,563 oralig‘ida;",kind='bullet'),
 para("128 bitli rejimda xesh qiymat quyi bit-qatlamining xabar va kalit quyi bit-qatlamlariga ajralishi bartaraf etiladi;",kind='bullet'),
 para("hisoblash narxi amalda o‘zgarmaydi: har bir bayt uchun ikkita jadvaldan o‘qish va bitta XOR amali bajariladi, jadval hajmi 256 bayt; §S§ AES S-boxi bo‘lgani uchun uni AES apparat buyruqlari orqali doimiy vaqtda hisoblash mumkin.",kind='bullet'),
 para("Quyidagi 2.4.1-jadvalda AES S-box qiymatlari keltirilgan: satr raqami — kirish baytining yuqori yarim bayti, ustun raqami — quyi yarim bayti."),
 para("2.4.1-jadval. SBZ o‘zgartirishida qo‘llaniladigan S o‘rniga qo‘yish jadvali (AES S-box)",kind='tcap'),
]
insert_after(E[65],newsec)
tbl=E[73]
for ri,tr in enumerate(tbl.findall(w('tr'))):
    if ri==0: continue
    for ci,tc in enumerate(tr.findall(w('tc'))):
        if ci==0: continue
        ts=list(tc.iter(w('t'))); ts[0].text=f'{int(AES[16*(ri-1)+(ci-1)]):02x}'
        for t in ts[1:]: t.text=''
# --- rasmlar
E[97].clear(); 
E97=E[97]; E97.append(copy.deepcopy(E[101].find(w('pPr'))))
for r in runs("2.4.2-rasmda *SBZ* o‘zgartirishi qo‘llanilgan 1-algoritmning blok sxemasi, 2.4.3-rasmda esa uning SP tarmoqda ifodalanishi keltirilgan. 2.4.3-rasmda kirish bloki holatga yutiladigan 8- va 9-bosqichlar rang bilan ajratilgan; oxirgi ustunda holatn massiviga NY bloki, ya’ni (§b§+2)-blok ko‘chiriladi."): E97.append(r)
cap2=copy.deepcopy(E[100]); repl_text(cap2,'2.4.2-rasm. O‘zMSt 285:2024 standarti tarkibidagi 1-algoritmning SP tarmoqda ifodalanishi','2.4.2-rasm. SBZ o‘zgartirishi qo‘llanilgan 1-algoritmning blok sxemasi')
E[98].addprevious(pic_para('/home/claude/fig/blok.png',13.5)); E[98].addprevious(cap2); body.remove(E[98])
E[99].addprevious(pic_para('/home/claude/fig/sp.png',16.5)); body.remove(E[99])
repl_text(E[100],'2.4.2-rasm. O‘zMSt 285:2024 standarti tarkibidagi 1-algoritmning SP tarmoqda ifodalanishi','2.4.3-rasm. SBZ o‘zgartirishi qo‘llanilgan 1-algoritmning SP tarmoqda ifodalanishi')
repl_text(E[101],'2.4.1-psevdokod. O‘zMSt 285:2024 1-algoritm xesh protsedurasining psevdokodi','2.4.1-psevdokod. SBZ o‘zgartirishi qo‘llanilgan 1-algoritm xesh protsedurasining psevdokodi')
# --- psevdokod
T=E[102]; repl_text(T,'byte zichlash [256]','byte S[256]')
cell=T.find('.//'+w('tc')); ps=cell.findall(w('p')); last=ps[-1]
tmpl=ps[1]
lines=["","SBZ (byte holat[4,8], byte holatn[4,8], byte S[256])","Begin","   For  s = 0  step 1 to 3","      For  u = 0  step 1 to 7","         holat[s,u] = S[ holat[s,u] ⊕ S[ holatn[s,u] ] ]","      End For","   End For","End"]
prev=last
for ln in lines:
    np_=copy.deepcopy(tmpl); ts=list(np_.iter(w('t'))); ts[0].text=ln
    for t in ts[1:]: t.text=''
    prev.addnext(np_); prev=np_
# --- nazorat qiymatlari
insert_after(T,[para("*SBZ* o‘zgartirishi qo‘llanilgan algoritmning nazorat qiymatlari. Xeshlash kaliti va 64 baytli xabar sifatida standartning A ilovasidagi qiymatlar olinadi:"),
 para("k = c86ed4b2 756df1cd 6b6eca81 d4418092 21ab81bb a0c7c150 44be8feb 934f95a2,",kind='formula'),
 para("M = «funksiyaxeshirovaniyainformasionnayatexnologiyakriptograficheska».",kind='formula'),
 para("256 bitli rejimda quyidagi xesh qiymat olinadi:"),
 para("h(M) = 42f97daa a8e7010b c629ca69 5eaa77df",kind='formula'),
 para("7ae7443a 0c3ae78d 205c2e02 5d256c96.",kind='formula'),
 para("128 bitli rejimda (xeshlash kaliti sifatida §k§ ning birinchi 16 bayti olinadi) xuddi shu xabar uchun:"),
 para("h(M) = bd745e2e d572ea42 46ed6848 2ef46c5e.",kind='formula')])
# --- keyingi rasmlar raqamini surish
for el in E[105:]:
    for a,b in [('2.4.6-rasm','2.4.7-rasm'),('2.4.5-rasm','2.4.6-rasm'),('2.4.4-rasm','2.4.5-rasm'),('2.4.3-rasm','2.4.4-rasm')]:
        repl_text(el,a,b)
d.save('/mnt/user-data/outputs/2.4_Milliy_xesh_funksiya_SBZ.docx')
print("ok")
