import re, sys
sys.path.insert(0,'/tmp/ilo/tool')
from omml import omml, spans, is_ind, atoms
x=open('/tmp/ilo/u/word/document.xml',encoding='utf8').read()
stat={}
# ---------- 1) sarlavhalar: uslubni olib tashlab, ko'rinishni bevosita formatlash bilan saqlash
HS={'1':('<w:b/><w:bCs/>','<w:sz w:val="30"/><w:szCs w:val="30"/>'),'2':('<w:b/><w:bCs/>',''),'3':('<w:b/><w:bCs/><w:i/><w:iCs/>','')}
def fix_heading(m):
    p=m.group(0); lvl=re.search(r'<w:pStyle w:val="([123])"/>',p).group(1); bi,sz=HS[lvl]
    ppr=re.search(r'<w:pPr>(.*?)</w:pPr>',p,re.S).group(1)
    jc=re.search(r'<w:jc [^>]*/>',ppr); rest=re.sub(r'<w:pStyle [^>]*/>|<w:jc [^>]*/>|<w:spacing [^>]*/>|<w:keepNext/>','',ppr)
    assert rest.strip()=='' , rest
    newppr='<w:pPr><w:keepNext/><w:spacing w:before="240" w:after="120" w:line="360" w:lineRule="auto"/>'+(jc.group(0) if jc else '')+'<w:outlineLvl w:val="9"/></w:pPr>'
    p=p.replace(re.search(r'<w:pPr>.*?</w:pPr>',p,re.S).group(0),newppr,1)
    def fix_run(r):
        r=r.group(0)
        if '<w:rPr>' in r: r=r.replace('<w:rPr>','<w:rPr>'+bi+sz,1)
        else: r=re.sub(r'^<w:r( [^>]*)?>',lambda q:q.group(0)+'<w:rPr>'+bi+sz+'</w:rPr>',r,1)
        return r
    p=re.sub(r'<w:r(?: [^>]*)?>.*?</w:r>',fix_run,p,flags=re.S)
    stat['sarlavha']=stat.get('sarlavha',0)+1
    return p
x=re.sub(r'<w:p(?: [^>]*)?>(?:(?!</w:p>).)*?<w:pStyle w:val="[123]"/>.*?</w:p>',fix_heading,x,flags=re.S)
# ---------- 2) jadvallarning birinchi satridagi fon rangi
stat['fon']=x.count('<w:shd w:val="clear" w:color="auto" w:fill="E7EEF7"/>')
x=x.replace('<w:shd w:val="clear" w:color="auto" w:fill="E7EEF7"/>','')
# ---------- 3a) alohida satrdagi formulalar -> m:oMathPara
FPPR='<w:spacing w:before="60" w:after="60" w:line="360" w:lineRule="auto"/><w:jc w:val="center"/>'
def fix_display(m):
    p=m.group(0)
    if FPPR not in p or '<w:i/>' not in p: return p
    txt=''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>',p)).replace('&amp;','&').replace('&lt;','<').replace('&gt;','>')
    if not any(is_ind(a) for a in atoms(txt)): return p
    ppr=re.search(r'<w:pPr>.*?</w:pPr>',p,re.S).group(0)
    head=re.match(r'<w:p(?: [^>]*)?>',p).group(0)
    stat['formula_alohida']=stat.get('formula_alohida',0)+1
    return f'{head}{ppr}<m:oMathPara><m:oMath>{omml(txt)}</m:oMath></m:oMathPara></w:p>'
x=re.sub(r'<w:p(?: [^>]*)?>(?:(?!</w:p>).)*?</w:p>',fix_display,x,flags=re.S)
# ---------- 3b) matn ichidagi formulalar
def unesc(t): return t.replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').replace('&quot;','"')
def esc(t): return t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
def all_spans(t,off=0,depth=0):
    sp=[(a+off,b+off) for a,b in spans(t)]
    if depth>3: return sp
    res=[]; p=off
    for a,b in sp+[(off+len(t),off+len(t))]:
        if a>p: res+=all_spans(t[p-off:a-off],p,depth+1) if sp else []
        if a<b: res.append((a,b))
        p=b
    return sorted(res)
def fix_run(m):
    r=m.group(0)
    if '<w:br/>' in r or '<w:tab/>' in r or r.count('<w:t')!=1 or '<m:' in r: return r
    tm=re.search(r'<w:t(?: [^>]*)?>([^<]*)</w:t>',r)
    if not tm: return r
    txt=unesc(tm.group(1)); rpr=re.search(r'<w:rPr>.*?</w:rPr>',r,re.S); rpr=rpr.group(0) if rpr else ''
    mono='Courier' in rpr
    if mono and (re.fullmatch(r'[ABCU₇ ]+',txt) or not any(c in txt for c in '⊕=←≈≤≥→₀₁₂₃₄₅₆₇₈₉')): return r
    sp=all_spans(txt)
    if not sp: return r
    head=re.match(r'<w:r(?: [^>]*)?>',r).group(0)
    msz=''.join(re.findall(r'<w:sz [^>]*/>|<w:szCs [^>]*/>',rpr)); mb='<w:b/>' if '<w:b/>' in rpr else ''
    out=[]; p=0
    for a,b in sp:
        if a>p: out.append(f'{head}{rpr}<w:t xml:space="preserve">{esc(txt[p:a])}</w:t></w:r>')
        out.append(f'<m:oMath>{omml(txt[a:b],mb+msz)}</m:oMath>'); p=b
        stat['formula_ichki']=stat.get('formula_ichki',0)+1
    if p<len(txt): out.append(f'{head}{rpr}<w:t xml:space="preserve">{esc(txt[p:])}</w:t></w:r>')
    return ''.join(out)
x=re.sub(r'<w:r(?: [^>]*)?>(?:(?!</w:r>).)*?</w:r>',fix_run,x,flags=re.S)
open('/tmp/ilo/u/word/document.xml','w',encoding='utf8').write(x)
print(stat)
