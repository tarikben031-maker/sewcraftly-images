import json,re,sys,html as H
from roles import *
from extract import parts
def P(t): return '<!-- wp:paragraph -->\n<p>'+t+'</p>\n<!-- /wp:paragraph -->'
def FAQ(q,a): return ('<!-- wp:details {"className":"pp-faq"} -->\n<details class="wp-block-details pp-faq"><summary>'+q+
    '</summary><!-- wp:paragraph -->\n<p>'+a+'</p>\n<!-- /wp:paragraph --></details>\n<!-- /wp:details -->')
def txt(s): return re.sub(r'\s+',' ',H.unescape(re.sub('<.*?>','',s))).strip()
DEF={'fr':(['Devant','Dos'],'Lire le croquis'),'de':(['Vorne','Hinten'],'Die technische Zeichnung lesen'),'nl':(['Voorkant','Achterkant'],'De technische tekening lezen')}
def build(enraw,trraw,T,lang='fr'):
    T=dict(T); T.setdefault('pill',DEF[lang][0]); T.setdefault('h3',DEF[lang][1])
    p=parts(enraw,trraw)
    vb=p['vb']; i=vb.index('</style>')+8; css,body=vb[:i],vb[i:]
    alts=re.findall(r'alt="[^"]*"',body); assert len(alts)==4
    for a,n in zip(alts,T['alt']): body=body.replace(a,'alt="'+H.escape(n,quote=True)+'"',1)
    tgs=re.findall(r'<span class="tg">[^<]*</span>',body); assert len(tgs)==2
    for a,n in zip(tgs,T['pill']): body=body.replace(a,'<span class="tg">'+n+'</span>',1)
    caps=re.findall(r'<figcaption>.*?</figcaption>',body,re.S); assert len(caps)==2
    for a,n in zip(caps,T['cap']): body=body.replace(a,'<figcaption>'+n+'</figcaption>',1)
    assert len(T['reading'])==len(p['reading']) and len(T['faq'])==len(p['faq'])
    newvb=css+body
    h3='<!-- wp:heading {"level":3} -->\n<h3 class="wp-block-heading">'+T['h3']+'</h3>\n<!-- /wp:heading -->'
    ins=[newvb,h3]+[P(x) for x in T['reading']]
    faqs=[FAQ(q,a) for q,a in T['faq']]
    segs=segment(trraw); head,ch,tail=inner(segs[0])
    U,ks=units(ch); assert sorted(ks)==sorted(ORDER),ks
    out=[]
    for k in ORDER:
        bl=[b for b in U[k] if nb(b)]
        if k=='design':
            fp=next(j for j,b in enumerate(bl) if sig(b).startswith('paragraph'))
            bl=bl[:fp+1]+ins+bl[fp+1:]
        if k=='questions':
            lf=max(j for j,b in enumerate(bl) if 'pp-faq' in b)
            bl=bl[:lf+1]+faqs+bl[lf+1:]
        out+=bl
    allf=[b for b in out if 'pp-faq' in b and b.startswith('<!-- wp:details')]
    qa=[]
    for b in allf:
        q=re.search(r'<summary>(.*?)</summary>',b,re.S).group(1); a=b[b.index('</summary>'):]
        qa.append({"@type":"Question","name":txt(q),"acceptedAnswer":{"@type":"Answer","text":txt(a)}})
    sch='<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":qa},ensure_ascii=False)+'</script>'
    di=[j for j,b in enumerate(out) if 'id="download"' in b and b.startswith('<!-- wp:html')]; assert len(di)==1
    added_schema=False
    if 'ld+json' not in out[di[0]]:
        out[di[0]]=out[di[0]].replace('<div id="download"></div>','<div id="download"></div>\n'+sch,1); added_schema=True
    new=head+'\n'+'\n\n'.join(out)+'\n'+tail+''.join(segs[1:])
    # integrity: every original non-blank line still present (multiset), new lines = inserted
    L=lambda s:sorted(x for x in s.split('\n') if x.strip())
    from collections import Counter
    co,cn=Counter(L(trraw)),Counter(L(new))
    missing=co-cn; extra=cn-co
    exp=Counter(L('\n'.join(ins+faqs)))
    if added_schema:
        exp-=Counter(['<div id="download"></div>']); exp+=Counter(L('<div id="download"></div>\n'+sch))
        exp-=Counter(['<div id="download"></div>'])  # line changed? no: div stays its own line
    miss_ok=not missing
    return new, dict(missing=list(missing.elements())[:5], extra_unexpected=list((extra-Counter(L('\n'.join(ins+faqs)))).elements())[:5], faq=len(allf), order=ks)
if __name__=='__main__':
    src,en,trf=sys.argv[1],sys.argv[2],sys.argv[3]; ids=dict(zip(['fr','de','nl'],sys.argv[4:7]))
    d=json.load(open(src)); T=json.load(open(trf)); res={}
    for l,i in ids.items():
        if i=='-': continue
        new,rep=build(d[en]['raw'],d[i]['raw'],T[l],l); res[i]={'raw':new,'modified':d[i]['modified']}
        print(l,i,'missing',rep['missing'],'extra',[x[:60] for x in rep['extra_unexpected']],'faq',rep['faq'])
    json.dump(res,open(sys.argv[7],'w'),ensure_ascii=False)
