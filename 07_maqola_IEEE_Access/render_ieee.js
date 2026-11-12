const fs=require('fs');
const {Document,Packer,Paragraph,TextRun,Table,TableRow,TableCell,WidthType,AlignmentType,TabStopType,HeadingLevel,ShadingType,BorderStyle,LevelFormat,PageNumber,Footer,ImageRun,PageBreak}=require('docx');
const B=JSON.parse(fs.readFileSync('blocks.json','utf8'));
const F="Times New Roman";
function runs(t,size,base={}){const out=[];const re=/(\*[^*]+\*|§[^§]+§)/g;let i=0,m;
  while((m=re.exec(t))){ if(m.index>i) out.push(new TextRun({text:t.slice(i,m.index),font:F,size,...base}));
    const s=m[0]; if(s[0]=='*') out.push(new TextRun({text:s.slice(1,-1),font:F,size,bold:true,italics:true})); else out.push(new TextRun({text:s.slice(1,-1),font:F,size,italics:true,bold:base.bold}));
    i=m.index+s.length;} if(i<t.length) out.push(new TextRun({text:t.slice(i),font:F,size,...base})); return out;}
const body=(t)=>new Paragraph({children:runs(t,20),alignment:AlignmentType.JUSTIFIED,indent:{firstLine:284},spacing:{after:0,line:240}});
const bd={style:BorderStyle.SINGLE,size:4,color:"000000"}; const borders={top:bd,bottom:bd,left:bd,right:bd};
const C=[];
for(const b of B){
  const k=b[0];
  if(k=='title') C.push(new Paragraph({alignment:AlignmentType.CENTER,spacing:{before:0,after:240},children:[new TextRun({text:b[1],font:F,size:40,bold:true})]}));
  else if(k=='sub') C.push(new Paragraph({alignment:AlignmentType.CENTER,spacing:{after:600},children:[new TextRun({text:b[1],font:F,size:20,italics:true})]}));
  else if(k=='h1') C.push(new Paragraph({heading:HeadingLevel.HEADING_1,alignment:AlignmentType.CENTER,children:[new TextRun({text:b[1],font:F})]}));
  else if(k=='h2') C.push(new Paragraph({heading:HeadingLevel.HEADING_2,children:[new TextRun({text:b[1],font:F})]}));
  else if(k=='h3') C.push(new Paragraph({heading:HeadingLevel.HEADING_3,children:[new TextRun({text:b[1],font:F})]}));
  else if(k=='p') C.push(body(b[1]));
  else if(k=='xul') C.push(new Paragraph({children:[new TextRun({text:'Xulosa: ',font:F,size:20,bold:true}),new TextRun({text:b[1],font:F,size:20,italics:true})],alignment:AlignmentType.JUSTIFIED,spacing:{before:120,after:120,line:240},indent:{left:567,right:567},border:{left:{style:BorderStyle.SINGLE,size:18,color:"1F4E9A",space:8}},shading:{fill:"F2F6FB",type:ShadingType.CLEAR,color:"auto"}}));
  else if(k=='f') C.push(new Paragraph({tabStops:[{type:TabStopType.CENTER,position:4680},{type:TabStopType.RIGHT,position:9360}],spacing:{before:80,after:80,line:240},children:[new TextRun({text:'\t'+b[1]+'\t'+(b[2]||''),font:F,size:20})]}));
  else if(k=='b') C.push(new Paragraph({numbering:{reference:"d",level:0},children:runs(b[1],20),alignment:AlignmentType.JUSTIFIED,spacing:{after:0,line:240}}));
  else if(k=='cap') C.push(new Paragraph({alignment:AlignmentType.CENTER,keepNext:true,spacing:{before:160,after:80},children:[new TextRun({text:b[1],font:F,size:16})]}));
  else if(k=='fcap') C.push(new Paragraph({alignment:AlignmentType.CENTER,spacing:{before:60,after:160},children:[new TextRun({text:b[1],font:F,size:16})]}));
  else if(k=='pb') C.push(new Paragraph({children:[new PageBreak()]}));
  else if(k=='img'){ const data=fs.readFileSync(b[1]); const w=b[2]/2.54*96, h=b[3]/2.54*96;
    C.push(new Paragraph({alignment:AlignmentType.CENTER,keepNext:true,spacing:{before:120},children:[new ImageRun({type:'png',data,transformation:{width:Math.round(w),height:Math.round(h)}})]}));}
  else if(k=='t'){ const widths=b[1], rows=b[2], mono=b[3]||[]; const sum=widths.reduce((a,c)=>a+c,0); const ncol=widths.length;
    const fs_=16;
    C.push(new Table({width:{size:sum,type:WidthType.DXA},columnWidths:widths,alignment:AlignmentType.CENTER,rows:rows.map((row,ri)=>new TableRow({tableHeader:ri==0,cantSplit:true,children:row.map((c,ci)=>new TableCell({borders,width:{size:widths[ci],type:WidthType.DXA},
      shading:ri==0?{fill:"E7EEF7",type:ShadingType.CLEAR,color:"auto"}:undefined,margins:{top:30,bottom:30,left:60,right:60},
      children:String(c).split('\n').map((line,li,arr)=>new Paragraph({keepNext:(rows.length<=14&&(ri<rows.length-1||li<arr.length-1)),alignment:ci==0?AlignmentType.LEFT:AlignmentType.CENTER,children:(ri>0&&mono.includes(ci))?[new TextRun({text:line,font:'Courier New',size:14})]:runs(line,fs_,ri==0?{bold:true}:{})}))}))}))}));
    C.push(new Paragraph({children:[],spacing:{after:80}}));}
}
const hs=(id,name,size,extra={})=>({id,name,basedOn:"Normal",next:"Normal",quickFormat:true,run:{font:F,size,bold:true,...extra.run},paragraph:{spacing:{before:240,after:120,line:240},keepNext:true,outlineLevel:extra.ol}});
const doc=new Document({styles:{default:{document:{run:{font:F,size:20}}},paragraphStyles:[hs("Heading1","Heading 1",20,{ol:0,run:{smallCaps:true}}),hs("Heading2","Heading 2",20,{ol:1,run:{bold:false,italics:true}}),hs("Heading3","Heading 3",20,{ol:2,run:{bold:false,italics:true}})]},
 numbering:{config:[{reference:"d",levels:[{level:0,format:LevelFormat.BULLET,text:"–",alignment:AlignmentType.LEFT,style:{paragraph:{indent:{left:1069,hanging:360}}}}]}]},
 sections:[{properties:{page:{size:{width:12240,height:15840},margin:{top:1440,bottom:1440,left:1440,right:1440}}},
  footers:{default:new Footer({children:[new Paragraph({alignment:AlignmentType.CENTER,children:[new TextRun({children:[PageNumber.CURRENT],font:F,size:16})]})]})},children:C}]});
Packer.toBuffer(doc).then(b=>fs.writeFileSync(process.argv[2],b));
