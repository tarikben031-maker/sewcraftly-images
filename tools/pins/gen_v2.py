#!/usr/bin/env python3
"""SewCraftly pins v2 (style of SC1015): 1000x1500. 
python3 tools/pins/gen_v2.py --name "Fitted Blazer" --garment Blazer --code SC1016 --sizes "XXS–4XL" --level Intermediate \
  --photo P --detail D --sketch-front F --sketch-both B --out pins/<base> --fonts /path/gf/ofl
"""
import argparse, os
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops
ap=argparse.ArgumentParser()
for k in ['name','garment','code','sizes','level','photo','detail','sketch-front','sketch-both','out','fonts']: ap.add_argument('--'+k,required=True)
A=ap.parse_args(); BAND=tuple(int(v) for v in os.environ.get('BAND','244,239,233').split(',')); W,H=1000,1500; K=(22,22,22); CREAM=(236,232,227); TERRA=(244,239,233)
FD=A.fonts.rstrip('/')+'/'
F=lambda p,s: ImageFont.truetype(FD+p,s); POP=lambda w,s:F(f'poppins/Poppins-{w}.ttf',s)
HERE=os.path.dirname(os.path.abspath(__file__)); LOGO=Image.open(os.path.join(HERE,'..','..','brand','sewcraftly-logo.png')).convert('RGBA')
def logo(w):
    return LOGO.resize((w,round(LOGO.height*w/LOGO.width)),Image.LANCZOS)
def cover_crop(im,w,h,fx=.5,fy=.5):
    s=max(w/im.width,h/im.height); im=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    x=round((im.width-w)*fx); y=round((im.height-h)*fy); return im.crop((x,y,x+w,y+h))
def shadow(cv,box,r=0,off=(6,9),blur=14,alpha=80):
    sh=Image.new('L',cv.size,0); ImageDraw.Draw(sh).rounded_rectangle(box,r,fill=alpha); sh=sh.filter(ImageFilter.GaussianBlur(blur))
    cv.paste(Image.new('RGB',cv.size,(110,95,85)),off,sh)
def sticker(path,maxw,maxh):
    src=Image.open(path).convert('RGB'); pad=30
    big=Image.new('RGB',(src.width+2*pad,src.height+2*pad),'white'); big.paste(src,(pad,pad)); src=big
    gi=ImageChops.invert(src.convert('L')); ln=gi.point(lambda v:255 if v>60 else 0).filter(ImageFilter.MaxFilter(15))
    fl=ln.copy(); ImageDraw.floodfill(fl,(0,0),128)
    sil=fl.point(lambda v:0 if v==128 else 255).filter(ImageFilter.MinFilter(5)); outl=sil.filter(ImageFilter.MaxFilter(17))
    st=Image.new('RGBA',src.size,(0,0,0,0)); st.paste((255,255,255,255),(0,0),outl); st.paste(src,(0,0),ImageChops.lighter(sil,gi))
    st=st.crop(outl.getbbox()); s=min(maxw/st.width,maxh/st.height); return st.resize((round(st.width*s),round(st.height*s)),Image.LANCZOS)
def ctext(d,y,t,font,fill=K,cx=W//2,sp=0):
    if sp:
        w=sum(d.textlength(c,font=font)+sp for c in t)-sp; x=cx-w/2
        for c in t: d.text((x,y),c,font=font,fill=fill); x+=d.textlength(c,font=font)+sp
    else: d.text((cx-d.textlength(t,font=font)/2,y),t,font=font,fill=fill)
def fit_font(d,t,mk,maxw,start):
    s=start
    while d.textlength(t,font=mk(s))>maxw: s-=2
    return mk(s)
G=A.garment.upper()
# ---------- pin 1
cv=Image.new('RGB',(W,H),CREAM); d=ImageDraw.Draw(cv)
ph=cover_crop(Image.open(A.photo).convert('RGB'),480,580,.45,.5); cv.paste(ph,(40,40))
d.rectangle((520,40,960,620),fill=BAND)
sk=sticker(A.sketch_front,400,520); cv.paste(sk,(520+(440-sk.width)//2,40+(580-sk.height)//2),sk)
d.text((40,636),f"THE {A.name.upper()}  ·  {A.code}",font=POP('SemiBold',29),fill=K)
rozha=lambda s:F('rozhaone/RozhaOne-Regular.ttf',s)
t1=f"FREE {G}"; t2="SEWING PATTERN"
f1=fit_font(d,t2,rozha,880,118)
ctext(d,725,t1,f1); ctext(d,725+int(f1.size*1.12),t2,f1)
card=(60,985,490,1370); shadow(cv,card,0,(5,8),12,60); d=ImageDraw.Draw(cv); d.rectangle(card,fill='white')
lg=logo(340); cv.paste(lg,(card[0]+(430-340)//2,card[1]+(385-lg.height)//2),lg)
det=cover_crop(Image.open(A.detail).convert('RGB'),430,385,.5,.5); shadow(cv,(510,985,940,1370),0,(5,8),12,60); d=ImageDraw.Draw(cv); cv.paste(det,(510,985))
pf=POP('Bold',21); d.rounded_rectangle((530,1003,630,1040),18,fill=K); d.text((580,1022),'DETAILS',font=pf,fill='white',anchor='mm')
ctext(d,1385,f"Sizes {A.sizes}  ·  PDF  ·  Free download",POP('Medium',31))
ctext(d,1437,'Enter sewcraftlypatterns.com · Enjoy your free pattern',POP('SemiBold',27))
cv.save(A.out+'-pin1.jpg',quality=93)
# ---------- pin 2
cv=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(cv)
lg=logo(380); cv.paste(lg,(40,45),lg)
pf=POP('Bold',30); t='FREE PDF DOWNLOAD'; tw=d.textlength(t,font=pf); bw=tw+30+16+56; x1=W-44; x0=x1-bw; y0=58; bh=78
d.rounded_rectangle((x0,y0,x1,y0+bh),bh//2,fill=K); ax=x0+28+15; ay=y0+bh//2
d.line((ax,ay-15,ax,ay+5),fill='white',width=5); d.polygon([(ax-11,ay-1),(ax+11,ay-1),(ax,ay+11)],fill='white'); d.line((ax-13,ay+16,ax+13,ay+16),fill='white',width=4)
d.text((x0+28+30+16,y0+bh//2),t,font=pf,fill='white',anchor='lm')
nt=f"{A.name.upper()}  ·  {A.code}"; ctext(d,212,nt,POP('SemiBold',32),sp=3)
b=Image.open(A.sketch_both).convert('RGB'); s=min(880/b.width,640/b.height); b=b.resize((round(b.width*s),round(b.height*s)),Image.LANCZOS)
cv.paste(b,((W-b.width)//2,300+(700-b.height)//2))
d.rectangle((0,1080,W,H),fill=BAND)
anton=lambda s:F('anton/Anton-Regular.ttf',s)
ft=fit_font(d,f"FREE {G} SEWING PATTERN",anton,870,112); ctext(d,1128,f"FREE {G} SEWING PATTERN",ft)
pf2=POP('SemiBold',34); t='+ Step-by-Step Instructions'; tw=d.textlength(t,font=pf2)
d.rounded_rectangle((W/2-tw/2-38,1252,W/2+tw/2+38,1322),35,fill='white'); d.text((W/2,1287),t,font=pf2,fill=K,anchor='mm')
ctext(d,1340,f"Sizes {A.sizes}  ·  {A.level}",POP('SemiBoldItalic',38))
d.line((W/2-50,1409,W/2+50,1409),fill=K,width=4); ctext(d,1430,'sewcraftlypatterns.com',POP('Medium',34),sp=3)
cv.save(A.out+'-pin2.jpg',quality=93)
print('ok')
