import json,sys,re,html as H
from extract import parts
def t(s): return re.sub(r'\s+',' ',s).strip()
d=json.load(open(sys.argv[1]))
for en,tr in zip(sys.argv[2::2],sys.argv[3::2]):
    p=parts(d[en]['raw'],d[tr]['raw']); body=p['vb'][p['vb'].index('</style>')+8:]
    o={'en':en,'alt':[H.unescape(a) for a in re.findall(r'alt="([^"]*)"',body)],'cap':re.findall(r'<figcaption>(.*?)</figcaption>',body,re.S),
       'h3':re.sub('<.*?>','',p['h3']).strip(),'reading':[t(re.search(r'<p>(.*?)</p>',x,re.S).group(1)) for x in p['reading']],
       'faq':[[re.search(r'<summary>(.*?)</summary>',x).group(1),t(re.search(r'<p>(.*?)</p>',x,re.S).group(1))] for x in p['faq']]}
    # translation context: garment name used in tr post title h2
    print(json.dumps(o,ensure_ascii=False))
