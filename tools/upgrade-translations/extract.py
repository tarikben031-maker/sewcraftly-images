import json,re,sys
from roles import *
def parts(enraw, trraw):
    _,ech,_=inner(segment(enraw)[0]); _,tch,_=inner(segment(trraw)[0])
    E,_=units(ech); T,_=units(tch)
    ed=[b for b in E['design'] if nb(b)]; td=[b for b in T['design'] if nb(b)]
    assert 'scp-vb' in ed[2] and 'scp-vb' not in ''.join(td)
    assert sig(ed[3]).startswith('heading h3')
    reading=[]
    for b in ed[4:]:
        if not sig(b).startswith('paragraph'): break
        reading.append(b)
    assert reading
    ef=[b for b in E['questions'] if nb(b) and 'pp-faq' in b]; tf=[b for b in T['questions'] if nb(b) and 'pp-faq' in b]
    newfaq=ef[len(tf):]
    return dict(vb=ed[2],h3=ed[3],reading=reading,faq=newfaq,ntr=len(tf),nef=len(ef))
if __name__=='__main__':
    d=json.load(open(sys.argv[1])); en=sys.argv[2]; tr=sys.argv[3]
    p=parts(d[en]['raw'],d[tr]['raw'])
    vb=p['vb']; body=vb[vb.index('</style>')+8:]
    print('VB body:',body)
    print('H3:',p['h3']);print('READING:');[print(x) for x in p['reading']]
    print('FAQ new',len(p['faq']),'of',p['nef'],'tr has',p['ntr']);[print(x) for x in p['faq']]
