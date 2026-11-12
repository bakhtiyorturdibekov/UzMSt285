import re
SUB=dict(zip('₀₁₂₃₄₅₆₇₈₉ₑⱼᵢₙₖₘₚₜₐₒₓ₊₋₍₎ᵤₛₕₗᵣ','0123456789ejinkmptaox+−()ushlr'))
SUP=dict(zip('⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺ⁿ⁽⁾ʲⁱ','0123456789−+n()ji'))
LET=r"A-Za-zА-Яа-яЁёЎўҚқҒғҲҳ‘’ʻʼ'"
OPS=set('=⊕≤≥≈≡≠·×→←↔∨∧∑Σ∏Π√±∈∉⇔⇒⌊⌋⟨⟩|∞∂')
GREEK=set('ΔαβγδεσπλμνφψωΓΘΛΦΨΩ')
def esc(t): return t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
def mr(t,nor=False,rpr=''):
    if not t: return ''
    m='<m:rPr><m:nor/></m:rPr>' if nor else ''
    return f'<m:r>{m}<w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/>{rpr}</w:rPr><m:t xml:space="preserve">{esc(t)}</m:t></m:r>'
def atoms(s):
    """Belgilar ketma-ketligini atomlarga ajratish."""
    out=[]; i=0; n=len(s)
    while i<n:
        ch=s[i]
        if ch=='_' and i+1<n and s[i+1]=='{':
            j=s.index('}',i); out.append(('sub',s[i+2:j])); i=j+1; continue
        if ch=='_' and i+1<n and s[i+1].isalnum():
            out.append(('sub',s[i+1])); i+=2; continue
        m=re.match(r"0x[0-9a-fA-F]+",s[i:])
        if m: out.append(('n',m.group(0))); i+=len(m.group(0)); continue
        m=re.match(r"[A-Za-z0-9]+",s[i:])
        if m and re.search(r'[A-Za-z]',m.group(0)) and re.search(r'[0-9]',m.group(0)):
            tok=m.group(0); mm=re.match(r"^([A-Za-z])([0-9]+)$",tok)
            m2=re.match(r"^([0-9]+)([A-Za-z])$",tok)
            if mm: out.append(('w',mm.group(1))); out.append(('n',mm.group(2)))
            elif m2: out.append(('n',m2.group(1))); out.append(('w',m2.group(2)))
            else: out.append(('w',tok+'  '[:0]) if len(tok)>1 else ('w',tok))
            i+=len(tok); continue
        if ch in SUB:
            j=i
            while j<n and s[j] in SUB: j+=1
            out.append(('sub',''.join(SUB[c] for c in s[i:j]))); i=j; continue
        if ch in SUP:
            j=i
            while j<n and s[j] in SUP: j+=1
            out.append(('sup',''.join(SUP[c] for c in s[i:j]))); i=j; continue
        m=re.match(r"[%s]+[′″]*"%LET,s[i:])
        if m: out.append(('w',m.group(0))); i+=len(m.group(0)); continue
        m=re.match(r"\d+(,\d+)?",s[i:])
        if m: out.append(('n',m.group(0))); i+=len(m.group(0)); continue
        out.append(('c',ch)); i+=1
    return out
def base_xml(a,rpr):
    k,t=a
    if k=='w': return mr(t, nor=len(t.rstrip('′″'))>1, rpr=rpr)
    if k=='c' and t==' ': return mr(t,nor=True,rpr=rpr)
    return mr(t,rpr=rpr)
def omml(s,rpr=''):
    A=atoms(s); out=[]; i=0
    while i<len(A):
        a=A[i]
        if a[0] in ('sub','sup'):          # asosga biriktirilmagan indeks
            out.append(mr(a[1],rpr=rpr)); i+=1; continue
        sub=sup=None; j=i+1
        while j<len(A) and A[j][0] in ('sub','sup'):
            if A[j][0]=='sub' and sub is None: sub=A[j][1]
            elif A[j][0]=='sup' and sup is None: sup=A[j][1]
            else: break
            j+=1
        b=base_xml(a,rpr)
        if sub is not None and sup is not None:
            out.append(f'<m:sSubSup><m:e>{b}</m:e><m:sub>{omml_inner(sub,rpr)}</m:sub><m:sup>{omml_inner(sup,rpr)}</m:sup></m:sSubSup>')
        elif sub is not None: out.append(f'<m:sSub><m:e>{b}</m:e><m:sub>{omml_inner(sub,rpr)}</m:sub></m:sSub>')
        elif sup is not None: out.append(f'<m:sSup><m:e>{b}</m:e><m:sup>{omml_inner(sup,rpr)}</m:sup></m:sSup>')
        else: out.append(b)
        i=j
    return ''.join(out)
def omml_inner(s,rpr): return ''.join(base_xml(a,rpr) if a[0] not in ('sub','sup') else mr(a[1],rpr=rpr) for a in atoms(s))
# ---------------- matn ichidagi formulalarni topish ----------------
def is_ind(a):
    k,t=a
    if k in ('sub','sup'): return True
    if k=='c' and (t in OPS or t in GREEK or t=='−'): return True
    if k=='w' and any(c in GREEK for c in t): return True
    return False
def mathish(a):
    k,t=a
    if is_ind(a) or k=='n': return True
    if k=='w': return len(t.rstrip('′″'))==1 or t in ('mod','binom','RC','SBZ')
    if k=='c': return t in ' []()+,/' or t in '−'
    return False
def spans(s):
    A=atoms(s); pos=[]; p=0
    for a in A:
        L=(len(a[1])+3 if a[0]=='sub' and False else None)
        pos.append(p); p+=0
    # atomlarning matndagi o'rnini hisoblash
    pos=[]; p=0
    for a in A:
        start=p
        if a[0]=='sub':
            if s.startswith('_{',p): p=s.index('}',p)+1
            elif s.startswith('_',p): p+=2
            else:
                while p<len(s) and s[p] in SUB: p+=1
        elif a[0]=='sup':
            while p<len(s) and s[p] in SUP: p+=1
        else: p+=len(a[1])
        pos.append((start,p))
    # tartib sonlar (8-nuqta, 2-chaqiruv): son ortidan '-' va harf kelsa — matn
    ok=[mathish(a) for a in A]
    for k,a in enumerate(A):
        if a[0] in ('n','w') and k+1<len(A) and A[k+1]==('c','-'): ok[k]=False   # 8-nuqta, 8- va, S-box
        if a[0]=='n' and k>=2 and A[k-1]==('c','-') and A[k-2][0]=='w': ok[k]=False                  # Standart-256
    res=[]; i=0
    while i<len(A):
        if not ok[i]: i+=1; continue
        j=i
        while j<len(A) and ok[j]: j+=1
        seg=list(range(i,j))
        if any(is_ind(A[k]) for k in seg):
            # chetlarni tozalash (bo'shliq, tinish belgilari, muvozanatsiz qavslar)
            def trim(seg):
                while seg and (A[seg[0]][0]=='c' and A[seg[0]][1] in ' ,/←→=+'): seg=seg[1:]
                while seg and (A[seg[-1]][0]=='c' and A[seg[-1]][1] in ' ,/←→=+'): seg=seg[:-1]
                return seg
            seg=trim(seg); changed=True
            while changed and seg:
                changed=False
                txt=s[pos[seg[0]][0]:pos[seg[-1]][1]]
                for o,c in (('(',')'),('[',']')):
                    if txt.count(o)>txt.count(c) and A[seg[0]]==('c',o): seg=trim(seg[1:]); changed=True; break
                    if txt.count(c)>txt.count(o) and A[seg[-1]]==('c',c): seg=trim(seg[:-1]); changed=True; break
                if not changed and seg:
                    txt=s[pos[seg[0]][0]:pos[seg[-1]][1]]
                    if txt.count('(')!=txt.count(')') or txt.count('[')!=txt.count(']'):
                        # muvozanatsiz ichki qavs: ochilgan qavsdan keyingi qismni olib tashlash
                        if txt.count('(')>txt.count(')'):
                            k=max(k for k in seg if A[k]==('c','(')); seg=trim([q for q in seg if q<k]); changed=True
                        elif txt.count(')')>txt.count('('):
                            k=min(k for k in seg if A[k]==('c',')')); seg=trim([q for q in seg if q>k]); changed=True
            if seg and any(is_ind(A[k]) for k in seg):
                res.append((pos[seg[0]][0],pos[seg[-1]][1]))
        i=j
    return res
