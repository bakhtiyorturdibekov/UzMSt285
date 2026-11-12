import re, sys, zipfile, shutil, os
sys.path.insert(0,'/home/claude/paper')
from omml_en import omml, spans
src,dst=sys.argv[1],sys.argv[2]
z=zipfile.ZipFile(src); x=z.read('word/document.xml').decode('utf8')
if 'xmlns:m=' not in x[:3000]:
    x=x.replace('<w:document ','<w:document xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" ',1)
st={'disp':0,'inl':0}
def unesc(t): return t.replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').replace('&quot;','"')
def esc(t): return t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
def disp(m):
    p=m.group(0)
    if '<w:tab w:val="center" w:pos="4680"/>' not in p: return p
    r=re.search(r'<w:r>(.*?)</w:r>',p,re.S).group(1)
    tt=re.findall(r'<w:t[^>]*>([^<]*)</w:t>',r)
    if len(tt)!=1 or tt[0].count('\t')!=2: return p
    parts=tt[0].split('\t')[1:]
    f,n=unesc(parts[0]),unesc(parts[1])
    ppr=re.search(r'<w:pPr>.*?</w:pPr>',p,re.S).group(0); head=re.match(r'<w:p(?: [^>]*)?>',p).group(0)
    rpr='<w:sz w:val="20"/><w:szCs w:val="20"/>'
    st['disp']+=1
    return f'{head}{ppr}<w:r><w:tab/></w:r><m:oMath>{omml(f,rpr)}</m:oMath><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="20"/></w:rPr><w:tab/><w:t>{esc(n)}</w:t></w:r></w:p>'
x=re.sub(r'<w:p(?: [^>]*)?>(?:(?!</w:p>).)*?</w:p>',disp,x,flags=re.S)
def all_spans(t,off=0,depth=0):
    sp=[(a+off,b+off) for a,b in spans(t)]
    if depth>3 or not sp: return sp
    res=[]; p=off
    for a,b in sp+[(off+len(t),off+len(t))]:
        if a>p: res+=all_spans(t[p-off:a-off],p,depth+1)
        if a<b: res.append((a,b))
        p=b
    return sorted(res)
def fix_run(m):
    r=m.group(0)
    if '<w:br/>' in r or '<w:tab/>' in r or r.count('<w:t')!=1 or '<m:' in r: return r
    tm=re.search(r'<w:t(?: [^>]*)?>([^<]*)</w:t>',r)
    if not tm: return r
    txt=unesc(tm.group(1)); rpr=re.search(r'<w:rPr>.*?</w:rPr>',r,re.S); rpr=rpr.group(0) if rpr else ''
    if 'Courier' in rpr: return r
    masked=re.sub(r'\[\d+\]',lambda q:'Z'*len(q.group(0)),txt)   # havolalar [n] formulaga kirmaydi
    sp=all_spans(masked)
    if not sp: return r
    head=re.match(r'<w:r(?: [^>]*)?>',r).group(0)
    msz=''.join(re.findall(r'<w:sz [^>]*/>|<w:szCs [^>]*/>',rpr)); mb='<w:b/>' if '<w:b/>' in rpr else ''
    out=[]; p=0
    for a,b in sp:
        if a>p: out.append(f'{head}{rpr}<w:t xml:space="preserve">{esc(txt[p:a])}</w:t></w:r>')
        out.append(f'<m:oMath>{omml(txt[a:b],mb+msz)}</m:oMath>'); p=b; st['inl']+=1
    if p<len(txt): out.append(f'{head}{rpr}<w:t xml:space="preserve">{esc(txt[p:])}</w:t></w:r>')
    return ''.join(out)
x=re.sub(r'<w:r(?: [^>]*)?>(?:(?!</w:r>).)*?</w:r>',fix_run,x,flags=re.S)
x=re.sub(r'<w:shd w:fill="E7EEF7"[^>]*/>|<w:shd [^>]*w:fill="E7EEF7"[^>]*/>','',x)
zo=zipfile.ZipFile(dst,'w',zipfile.ZIP_DEFLATED)
for it in z.infolist(): zo.writestr(it, x.encode('utf8') if it.filename=='word/document.xml' else z.read(it.filename))
zo.close(); print(st)
