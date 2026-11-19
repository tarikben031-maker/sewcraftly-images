import re
from seg import *
def nb(b): return b.strip()!=''
def kind(b):
    s=sig(b)
    return s
def units(children):
    """group children into units: list of (key, [blocks])"""
    U=[];cur=None
    def start(k):
        nonlocal cur; cur=[k,[]]; U.append(cur)
    start('pre')
    for b in children:
        if not nb(b): cur[1].append(b); continue
        s=sig(b)
        if s.startswith('heading h2:'): start('h2')
        elif s.startswith('columns.pp-two-col'): start('materials')
        elif s.startswith('group.') and 'pp-help' in s.split(' h')[0]: start('help')
        elif 'pp-ad' in b and 'data-ad="' in b and len(b)<200: start('ad'+re.search(r'data-ad="(\d)"',b).group(1))
        elif s.startswith('html') and 'id="download"' in b: start('download')
        elif s.startswith('group.pp-cta'): start('cta')
        elif s.startswith('group.pp-tut'): start('tut')
        elif s.startswith('paragraph.pp-closing'): start('closing')
        elif s.startswith('group.pp-kofi'): start('kofi')
        cur[1].append(b)
    # classify h2 units
    h2=[u for u in U if u[0]=='h2']
    h2[0][0]='design'
    for u in h2[1:]:
        j=''.join(u[1]); first=[b for b in u[1][1:] if nb(b)]
        if 'pp-table' in j: u[0]='sizing'
        elif first and sig(first[0]).startswith('columns.pp-tips'): u[0]='notes'
        elif 'pp-steps' in j: u[0]='steps'
        elif 'pp-faq' in j: u[0]='questions'
    keys=[u[0] for u in U]
    ti=keys.index('tut')
    after=[u for u in U[ti+1:] if u[0]=='h2']
    assert len(after)==3,('after tut',len(after))
    for u,k in zip(after,['tips','style','care']): u[0]=k
    rest=[u for u in U if u[0]=='h2']
    assert len(rest)==1,('unclassified',[sig(u[1][0]) for u in rest])
    rest[0][0]='fabric'
    ks=[u[0] for u in U]; assert len(set(ks))==len(ks),ks
    return {u[0]:u[1] for u in U}, ks
ORDER=['pre','design','sizing','ad1','materials','fabric','ad2','help','notes','download','cta','steps','tut','tips','style','care','ad3','questions','closing','kofi']
