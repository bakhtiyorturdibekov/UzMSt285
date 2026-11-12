const fs=require('fs');
const {Document,Packer,Paragraph,TextRun,Table,TableRow,TableCell,WidthType,AlignmentType,HeadingLevel,ShadingType,BorderStyle,LevelFormat,PageNumber,Footer}=require('docx');
const F="Times New Roman", W=9354;
const r=(t,o={})=>new TextRun({text:t,font:F,size:o.size||24,bold:o.b,italics:o.i,superScript:o.sup});
function P(parts,o={}){ if(typeof parts==='string') parts=[r(parts)];
  return new Paragraph({children:parts,alignment:o.align||AlignmentType.JUSTIFIED,indent:o.noind?undefined:{firstLine:567},spacing:{after:o.after??120,line:300},keepNext:o.keepNext});}
// inline markup: **bold**, ^sup^
function md(t){const out=[];const re=/(\*\*[^*]+\*\*|\^[^^]+\^|_[^_]+_)/g;let i=0,m;
  while((m=re.exec(t))){ if(m.index>i) out.push(r(t.slice(i,m.index)));
    const s=m[0]; if(s[0]=='*') out.push(r(s.slice(2,-2),{b:true})); else if(s[0]=='^') out.push(r(s.slice(1,-1),{sup:true})); else out.push(r(s.slice(1,-1),{i:true}));
    i=m.index+s.length;} if(i<t.length) out.push(r(t.slice(i))); return out;}
const p=(t,o)=>P(md(t),o);
const H1=t=>new Paragraph({heading:HeadingLevel.HEADING_1,children:[new TextRun({text:t,font:F})]});
const H2=t=>new Paragraph({heading:HeadingLevel.HEADING_2,children:[new TextRun({text:t,font:F})]});
const cap=t=>new Paragraph({children:md(t),alignment:AlignmentType.LEFT,spacing:{before:120,after:60},keepNext:true});
const bul=t=>new Paragraph({numbering:{reference:"b",level:0},children:md(t),alignment:AlignmentType.JUSTIFIED,spacing:{after:80,line:300}});
const bd={style:BorderStyle.SINGLE,size:4,color:"808080"}; const borders={top:bd,bottom:bd,left:bd,right:bd};
function T(widths,rows){ const sum=widths.reduce((a,b)=>a+b,0);
  return new Table({width:{size:sum,type:WidthType.DXA},columnWidths:widths,rows:rows.map((row,ri)=>new TableRow({tableHeader:ri==0,cantSplit:true,children:row.map((c,ci)=>new TableCell({borders,width:{size:widths[ci],type:WidthType.DXA},
    shading:ri==0?{fill:"D9E2F3",type:ShadingType.CLEAR,color:"auto"}:undefined,margins:{top:50,bottom:50,left:90,right:90},
    children:[new Paragraph({alignment:ci==0?AlignmentType.LEFT:AlignmentType.CENTER,children:md(ri==0?`**${c}**`:c).map(x=>{x.root&&0;return x;})})]}))}))});}
// smaller font in tables: rebuild md with size 20
function mds(t,b){return md(t).map(x=>x);} 
function Ts(widths,rows){ const sum=widths.reduce((a,b)=>a+b,0);
  const cell=(c,ri,ci)=>{const parts=[];const re=/(\*\*[^*]+\*\*|\^[^^]+\^)/g;let i=0,m;const s0=ri==0;
    while((m=re.exec(c))){ if(m.index>i) parts.push(r(c.slice(i,m.index),{size:20,b:s0})); const s=m[0];
      parts.push(s[0]=='*'?r(s.slice(2,-2),{size:20,b:true}):r(s.slice(1,-1),{size:20,sup:true,b:s0})); i=m.index+s.length;}
    if(i<c.length) parts.push(r(c.slice(i),{size:20,b:s0}));
    return new TableCell({borders,width:{size:widths[ci],type:WidthType.DXA},shading:s0?{fill:"D9E2F3",type:ShadingType.CLEAR,color:"auto"}:undefined,
      margins:{top:40,bottom:40,left:80,right:80},children:[new Paragraph({alignment:ci==0?AlignmentType.LEFT:AlignmentType.CENTER,children:parts})]});};
  return new Table({width:{size:sum,type:WidthType.DXA},columnWidths:widths,rows:rows.map((row,ri)=>new TableRow({tableHeader:ri==0,cantSplit:true,children:row.map((c,ci)=>cell(c,ri,ci))}))});}
const gap=()=>new Paragraph({children:[],spacing:{after:60}});

const C=[];
C.push(new Paragraph({alignment:AlignmentType.CENTER,spacing:{after:80},children:[r("«O‘zMSt 285:2024 1-algoritmini yangi o‘zgartirish yordamida takomillashtirish»",{b:true,size:28})]}));
C.push(new Paragraph({alignment:AlignmentType.CENTER,spacing:{after:80},children:[r("(BaytZichlash → SBZ) materialini ekspert tahlili",{b:true,size:28})]}));
C.push(new Paragraph({alignment:AlignmentType.CENTER,spacing:{after:240},children:[r("Tahlil qilingan fayl: BaytZichlash_SBZ.docx",{i:true})]}));

C.push(H1("1. Umumiy baho"));
C.push(p("Material O‘zMSt 285:2024 standartining 1-algoritmidagi BaytZichlash o‘zgartirishini bayt-baytli SBZ amali, ya’ni holat[i] ← S(h[i] ⊕ S(n[i])) bilan almashtirishni taklif qiladi. Bunda AES S-box (FIPS 197) ishlatiladi, algoritmning qolgan qismi o‘zgarishsiz qoladi. Materialning texnik yadrosi to‘g‘ri: asosiy sonli natijalar mustaqil realizatsiya orqali qayta hisoblandi va to‘liq mos keldi."));
C.push(p("Shu bilan birga, bir nechta joyda da’vo isbotlangan doiradan kengroq ifodalangan, muhim shartlar yozilmagan yoki statistik natijalar yetarlicha talqin qilinmagan. Bu kamchiliklar taklifning mohiyatini inkor etmaydi, lekin materialni ekspertizaga taqdim etishdan oldin tuzatilishi kerak."));

C.push(H1("2. Tekshirish usuli"));
C.push(p("Tahlil uchun 1-algoritm Python tilida mustaqil ravishda, faqat standart matni va A ilovadagi nazorat misoli asosida qayta yozildi. Bu realizatsiya A ilovaning yakuniy xeshini va barcha oraliq massivlarini bayt-ma-bayt takrorlaydi. Unga SBZ amali (AES S-box bilan) va 128-bitli rejim (p = 16) qo‘shildi. So‘ngra quyidagilar hisoblandi:"));
C.push(bul("materialning A ilovasidagi barcha nazorat qiymatlari (KAT);"));
C.push(bul("3-jadvaldagi lokal ko‘rsatkichlar, barcha 2^16^ kirish bo‘yicha to‘liq;"));
C.push(bul("300 ta tasodifiy muvozanatli 8→4 jadval bo‘yicha taqqoslash ko‘rsatkichlari;"));
C.push(bul("128-bitli rejimdagi bit-qatlam ajralishi testlari (T1, T2) va ikki blokli xabar uchun qo‘shimcha test;"));
C.push(bul("Aralash o‘zgartirishining mod 2 bo‘yicha rangi (2000 ta tasodifiy kalit);"));
C.push(bul("4-jadvaldagi χ² qiymatlarining statistik ahamiyatliligi."));

C.push(H1("3. Tasdiqlangan natijalar"));
C.push(H2("3.1. Nazorat qiymatlari (KAT)"));
C.push(p("Materialning A ilovasidagi 12 ta qiymatning barchasi mustaqil realizatsiya bilan mos keldi. Kalit: A ilova kaliti (256 bit), 128-bitli rejimda uning birinchi 16 bayti."));
C.push(cap("**1-jadval.** KAT qiymatlarini tekshirish natijasi"));
C.push(Ts([2600,2200,2200,2354],[["Variant","Bo‘sh xabar","A ilova xabari","«abc»"],
 ["Standart, 256 bit","mos","mos","mos"],["SBZ, 256 bit","mos","mos","mos"],["Standart, 128 bit","mos","mos","mos"],["SBZ, 128 bit","mos","mos","mos"]]));
C.push(gap());
C.push(H2("3.2. Lokal ko‘rsatkichlar (materialning 3-jadvali)"));
C.push(p("3-jadvaldagi barcha qiymatlar aniq takrorlandi. Qo‘shimcha ravishda B ilova jadvalining lotin kvadrati ekani (har bir satr va ustun 0…15 ning o‘rin almashtirishi) va 300 ta tasodifiy jadval medianasi (DDT 38, |Walsh| 60) ham tasdiqlandi."));
C.push(cap("**2-jadval.** Siqish nuqtasidagi o‘zgartirish ko‘rsatkichlari (16 → 8 bit, mustaqil hisob)"));
C.push(Ts([3354,2000,2000,2000],[["Ko‘rsatkich","BaytZichlash, p = 256","XOR, p = 16","SBZ"],
 ["Maks. differensial ehtimollik","40/256 (ΔX = 0x96 → 0)","1","2^−6^"],
 ["Bitta argument farqining so‘nishi","0,156","0","0"],
 ["Maks. |korrelyatsiya|","0,25","1","2^−6^"],
 ["Algebraik daraja","6","1","13"],
 ["SAC: min – max (o‘rtacha)","0 – 0,641 (0,266)","0 – 1 (0,125)","0,453 – 0,563 (0,503)"],
 ["BIC: maks. |ρ|","0,319","—","0,134"],
 ["Bog‘liqliklar","64/128","16/128","128/128"]]));
C.push(gap());
C.push(H2("3.3. 128-bitli rejimdagi tuzilmaviy zaiflik"));
C.push(p("Bir blokli xabarda har bir yarim baytning 1–3-bitlari o‘zgartirilganda Standart variantida chiqishning 0-qatlami (32 bit) 30 ta tajribaning 30 tasida o‘zgarmadi. Kalitning 1–3-bitlari o‘zgartirilganda (R juftligi saqlangan holda) natija yana 30/30 bo‘ldi. SBZ variantida esa 0-qatlam 30 holatning barchasida o‘zgardi (0/30). Bu materialdagi T1 va T2 testlarini va p = 16 rejimidagi zaiflik haqidagi asosiy xulosani tasdiqlaydi."));
C.push(H2("3.4. Aralash o‘zgartirishining mod 2 bo‘yicha rangi"));
C.push(cap("**3-jadval.** Aralash rangi (kalitning dastlabki ikki yarim bayti juft, 2000 ta kalit)"));
C.push(Ts([4354,2500,2500],[["Ko‘rsatkich","Mustaqil hisob","Materialda"],
 ["O‘rtacha rang (min – max)","26,3 (13 – 32)","26,0 (16 – 32)"],["To‘liq rangli kalitlar ulushi","1,15 %","1,3 %"],["Nol satrli kalitlar ulushi","47,5 %","49,0 – 51,7 %"]]));
C.push(gap());
C.push(p("Farqlar tanlanma hajmi bilan bog‘liq xatolik doirasida. Hisoblash narxiga oid da’volar ham to‘g‘ri: bir blokda Qo‘sh o‘zgartirishi 22 marta chaqiriladi, bu 22 × 192 = 4224 ta modul bo‘yicha teskarilashni beradi."));

C.push(H1("4. Aniqlik kiritish va tuzatish talab qilinadigan joylar"));
C.push(H2("4.1. «R juft» — xossa emas, kalitga qo‘yiladigan talab"));
C.push(p("Qo‘sh o‘zgartirishi juftlikni saqlashi haqidagi isbot R juft bo‘lishiga tayanadi. Agar R toq bo‘lsa, toq a uchun B + R·a juft bo‘ladi va (B + R·a)^−1^ (mod p) mavjud emas, ya’ni Qo‘sh umuman hisoblanmaydi. Tajribada birinchi yarim bayti toq bo‘lgan 20 ta kalitning 20 tasida ham algoritm teskarilash nuqtasida to‘xtadi. Bu cheklov Standart va SBZ variantlariga bir xil tegishli."));
C.push(p("Standartning o‘zida ham ziddiyat bor: 5.1.2-band ikkinchi yarim bayt (bayt) juft va 4…10 (10…120) oralig‘ida bo‘lishini talab qiladi, nazorat misolida esa R sifatida birinchi bayt (0xC8 = 200) ishlatiladi va u bu oraliqqa kirmaydi. **Tavsiya:** materialda kalitga qo‘yiladigan shartni alohida band sifatida aniq yozish va 2^126^ kalit fazosi bahosi aynan shu shartdan kelib chiqishini ko‘rsatish."));
C.push(H2("4.2. «Qolgan 96 bit 0-qatlamga ta’sir qilmaydi» degan da’voni toraytirish"));
C.push(p("Bu da’vo faqat NY blokining 0-qatlami o‘zgarmaganda to‘g‘ri: bir blokli xabarda yoki NY saqlanganda (materialdagi T4 testi). Ikki blokli xabarda yuqori bitlar tasodifiy o‘zgartirilganda NY yig‘indisidagi ko‘chirish (carry) 0-qatlamga o‘tadi va 30 tajribaning birortasida ham 0-qatlam saqlanmadi (0/30)."));
C.push(p("Kolliziya hujumi baribir ishlaydi, chunki 2^96^ elementli sinflar bir blokli xabarlar uchun hisoblangan. **Tavsiya:** umumiy jumlaga «NY blokining 0-qatlami o‘zgarmagan holda» shartini qo‘shish."));
C.push(H2("4.3. 128-bitli rejimdagi kelishuvlar yozilmagan"));
C.push(p("128-bitli KAT qiymatlarini faqat quyidagi kelishuvlarni taxmin qilish orqali takrorlash mumkin bo‘ldi:"));
C.push(bul("uzunlik va NY bloklari 128 bitli (16 bayt), holbuki Standartning 6.1.1-bandida 256 bit deyilgan;"));
C.push(bul("har bir baytda yuqori yarim bayt birinchi keladi (5.2.2.3 va 5.2.3.1-bandlar);"));
C.push(bul("R — kalitning birinchi yarim bayti;"));
C.push(bul("A2 uchun Δ sharti J1hn + J2hn (mos ravishda J1h + J2h) bo‘yicha olinadi."));
C.push(p("Shuningdek 256-bitli rejim uchun ham satr bo‘yicha joylashtirish, uzunlik blokining bitlarda va big-endian ko‘rinishda yozilishi, NY ning 2^256^ moduli bo‘yicha yig‘indi ekani standart matnida aniq aytilmagan. **Tavsiya:** bu kelishuvlarni materialda «Realizatsiya kelishuvlari» degan alohida bandda keltirish, aks holda boshqa ishlab chiquvchi KAT qiymatlarini takrorlay olmaydi."));
C.push(H2("4.4. χ² qiymatlari statistik ahamiyatli"));
C.push(p("Materialning 4-jadvalidagi chiqish bitlari balansi «kichik og‘ish» deb baholangan. α = 0,01 darajasida Bonferroni tuzatmasi bilan kritik qiymatlar 128 bitli chiqish uchun 15,6 ga, 256 bitli chiqish uchun 16,9 ga teng."));
C.push(cap("**4-jadval.** 4-jadvaldagi maksimal χ² qiymatlarining ahamiyatliligi (1 erkinlik darajasi)"));
C.push(Ts([2854,1500,2000,1500,1500],[["Variant","χ²","p-qiymat","Kritik qiymat","Ahamiyatli"],
 ["Standart, 128 bit","16,0","6,3·10^−5^","15,6","ha"],["SBZ, 128 bit","19,4","1,1·10^−5^","15,6","ha"],
 ["Standart, 256 bit","13,5","2,4·10^−4^","16,9","yo‘q"],["SBZ, 256 bit","21,7","3,2·10^−6^","16,9","ha"]]));
C.push(gap());
C.push(p("Bu ko‘rsatkich bo‘yicha SBZ 256 Standart 256 dan yomonroq ko‘rinadi. Ehtimoliy sabab — Aralash o‘zgartirishi keltirib chiqaradigan, kalitga bog‘liq doimiy bitlar; bu xossa ikkala variantga ham xos. **Tavsiya:** bu natijani ochiq talqin qilish va o‘lchovni qayd etilgan kalitlarda, kattaroq tanlanma bilan qaytarish."));
C.push(H2("4.5. 256-bitli rejimda yutuq faqat lokal darajada"));
C.push(p("Materialning o‘zi 256-bitli rejimda ikkala variant ham tuzilmaviy testlardan o‘tishini, ko‘chki effekti deyarli bir xil ekanini (0,496 va 0,495) ko‘rsatadi. Demak bu rejimda SBZ namoyish qilingan hujumni bartaraf etmaydi, balki lokal ko‘rsatkichlarni yaxshilab, xavfsizlik zaxirasini oshiradi. 128-bitli rejimda esa SBZ isbotlangan zaiflikni yopadi. **Tavsiya:** xulosada bu ikki holatni aniq ajratib ifodalash."));
C.push(H2("4.6. Aralash muammosi materialda aytilganidan jiddiyroq bo‘lishi mumkin"));
C.push(p("Z/2^n^ halqasi ustidagi chiziqli akslantirish faqat uning mod 2 bo‘yicha reduksiyasi teskarilanuvchi bo‘lgandagina teskarilanuvchi bo‘ladi. Kalitlarning taxminan 99 foizida mod 2 rang 32 dan kichik, demak Aralash mod 256 (mod 16) bo‘yicha ham bijeksiya emas: har bir raundda kamida 2^6^ ta turli holat bitta holatga akslanadi. 6-jadvaldagi 2^125^ bahosi esa faqat chiqishning 0-qatlamini hisobga oladi, raund ichidagi yo‘qotishlarni emas."));
C.push(p("Kalitsiz rejimda k ochiq parametr bo‘ladi, shuning uchun chiqishdagi chiziqli bog‘liqliklar va doimiy bitlar hamma uchun ma’lum bo‘ladi va bu bevosita farqlovchi (distinguisher) beradi. **Tavsiya:** 6-jadvaldagi baholarni pastki chegara emas, evristik baho deb atash; Aralash/TuzilmaKalit masalasini «qoldiq xossa» emas, birinchi navbatdagi vazifa sifatida berish."));
C.push(H2("4.7. AES S-box tanlovini asoslash"));
C.push(p("Milliy standart uchun xorijiy standartdagi S-box bilan bog‘lanish ekspertiza jarayonida savol tug‘dirishi mumkin. Shu ko‘rsatkichlarga ega (differensial bir xillik 4, nochiziqlilik 112, algebraik daraja 7) muqobil S-boxni ko‘rsatish yoki tanlovni, masalan, O‘zMSt 270 bilan bog‘liq holda alohida asoslash foydali bo‘ladi. «Standartda xuddi shu mezonlarga javob beradigan S-boxlardan foydalaniladi» jumlasida qaysi standart nazarda tutilgani aytilmagan."));

C.push(H1("5. Matn va atamalar bo‘yicha izohlar"));
C.push(cap("**5-jadval.** Tahririy tuzatishlar"));
C.push(Ts([2500,3200,3654],[["Joy","Hozirgi matn","Tavsiya"],
 ["Sarlavha","«…yangi o‘zgartish yordamida…»","«…yangi o‘zgartirish yordamida…»"],
 ["1-bo‘lim","«…asosiy yutish elementi hioblanadi»","«…hisoblanadi»"],
 ["256-bit rejim, 3-band","«mod 2n maydonda»","«2^n^ moduli bo‘yicha halqada» (Z/2^n^ maydon emas; «mod 2 maydon» esa to‘g‘ri)"],
 ["B ilova haqidagi jumla","«…satrlar ham, ustunlar ham 0…15 ning o‘rin almashtiriladi»","«…0…15 ning o‘rin almashtirishi bo‘ladi»"],
 ["Statistik testlar","«(P(1) ≈ 0,46, barcha variantlarda…»","yopuvchi qavs qo‘yish"],
 ["2-jadval","16 ta noma’lum bit bilan tajriba","«qisqartirilgan namoyish (30 o‘rniga 16 bit)» deb aniq yozish"],
 ["6-jadval kirishi","«yuqori chegara baholari»","«ma’lum hujumlar bo‘yicha murakkablik baholari»"],
 ["«AES S-box» bandi","«Standartda xuddi shu mezonlarga…»","qaysi standart nazarda tutilganini ko‘rsatish"]]));
C.push(gap());

C.push(H1("6. Xulosa"));
C.push(p("Materialda bayon etilgan SBZ taklifi texnik jihatdan asosli. Asosiy sonli natijalar — KAT qiymatlari, lokal kriptografik ko‘rsatkichlar, 128-bitli rejimdagi bit-qatlam zaifligi va Aralash rangi statistikasi — mustaqil hisoblash bilan to‘liq tasdiqlandi. SBZ 128-bitli rejimdagi isbotlangan zaiflikni bartaraf etadi, 256-bitli rejimda esa lokal ko‘rsatkichlarni sezilarli yaxshilaydi, hisoblash narxi amalda o‘zgarmaydi."));
C.push(p("Materialni yakunlash uchun quyidagilar tavsiya etiladi:"));
C.push(bul("kalitga qo‘yiladigan shartni (R juftligi) va barcha realizatsiya kelishuvlarini alohida bandda keltirish;"));
C.push(bul("bit-qatlam ajralishi haqidagi umumiy da’voga NY sharti qo‘shish;"));
C.push(bul("χ² natijalarini statistik ahamiyatli deb talqin qilish va qayd etilgan kalitlarda qayta o‘lchash;"));
C.push(bul("256 va 128 bitli rejimlardagi yutuqni xulosada aniq ajratish;"));
C.push(bul("Aralash o‘zgartirishining noteskarilanuvchiligini birinchi navbatdagi muammo sifatida ko‘rsatish va 6-jadval baholarini evristik deb belgilash;"));
C.push(bul("AES S-box tanlovini asoslash va 5-jadvaldagi tahririy tuzatishlarni kiritish."));

const doc=new Document({styles:{default:{document:{run:{font:F,size:24}}},
  paragraphStyles:[{id:"Heading1",name:"Heading 1",basedOn:"Normal",next:"Normal",quickFormat:true,run:{font:F,size:28,bold:true},paragraph:{spacing:{before:300,after:120},keepNext:true,outlineLevel:0}},
   {id:"Heading2",name:"Heading 2",basedOn:"Normal",next:"Normal",quickFormat:true,run:{font:F,size:24,bold:true,italics:true},paragraph:{spacing:{before:200,after:100},keepNext:true,outlineLevel:1}}]},
 numbering:{config:[{reference:"b",levels:[{level:0,format:LevelFormat.BULLET,text:"–",alignment:AlignmentType.LEFT,style:{paragraph:{indent:{left:851,hanging:284}}}}]}]},
 sections:[{properties:{page:{size:{width:11906,height:16838},margin:{top:1134,bottom:1134,left:1701,right:851}}},
  footers:{default:new Footer({children:[new Paragraph({alignment:AlignmentType.CENTER,children:[new TextRun({children:[PageNumber.CURRENT],font:F,size:20})]})]})},
  children:C}]});
Packer.toBuffer(doc).then(b=>fs.writeFileSync('/mnt/user-data/outputs/BaytZichlash_SBZ_tahlili.docx',b));
