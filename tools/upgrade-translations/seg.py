import re,json
TOK=re.compile(r'<!-- (/?)wp:([a-z0-9/-]+)(\s+\{.*?\})?\s*(/?)-->',re.S)
def segment(raw):
    """split into top-level blocks (incl. text between) -> list of strings, concatenation == raw"""
    out=[];depth=0;start=0;pos=0
    for m in TOK.finditer(raw):
        close,name,attrs,selfc=m.groups()
        if depth==0 and not close:
            if m.start()>start: out.append(raw[start:m.start()])
            start=m.start()
            if selfc: out.append(raw[start:m.end()]);start=m.end();continue
            depth=1;continue
        if selfc: continue
        if close: depth-=1
        else: depth+=1
        if depth==0:
            out.append(raw[start:m.end()]);start=m.end()
    if start<len(raw): out.append(raw[start:])
    assert ''.join(out)==raw
    return out
def sig(b):
    m=TOK.match(b.strip()) if b.strip().startswith('<!--') else None
    if not m: return 'TXT'
    name=m.group(2);attrs=m.group(3) or ''
    cls=re.search(r'"className":"([^"]+)"',attrs);anchor=re.search(r'"anchor":"([^"]+)"',attrs)
    h=re.search(r'<h([1-6])[^>]*>(.*?)</h\1>',b,re.S)
    s=name+('.'+cls.group(1) if cls else '')+('#'+anchor.group(1) if anchor else '')
    if 'adsbygoogle' in b or 'sc-ad' in b or 'ad-slot' in b: s+=' AD'
    if 'scp-vb' in b: s+=' VB'
    if h: s+=f' h{h.group(1)}:'+re.sub('<.*?>','',h.group(2))[:40]
    else:
        t=re.sub('<.*?>','',b);t=re.sub(r'\s+',' ',t).strip()[:40]
        s+=' «'+t+'»'
    return s
def inner(b):
    """return (head, children list, tail) of a group block"""
    m1=re.match(r'(<!-- wp:group.*?-->\s*<div[^>]*>)',b,re.S)
    m2=re.search(r'(</div>\s*<!-- /wp:group -->\s*)$',b,re.S)
    head=m1.group(1);tail=m2.group(1);mid=b[len(head):len(b)-len(tail)]
    return head,segment(mid),tail
