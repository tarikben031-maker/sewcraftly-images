#!/usr/bin/env python3
"""SewCraftly Pinterest pin generator (2 designs, 1000x1500).

Usage:
  python3 gen.py --cover covers/X.jpg --name "Spaghetti Strap Dress" --garment Dress \
      --code SC1006 --sizes "XXS–4XL" --level Intermediate --out out/SC1006
Makes <out>-pin1.jpg (hero + title + 2 panels) and <out>-pin2.jpg (sketch sheet).
The sketch and band colour are taken from the house cover image (sketch stickers on the left).
Fonts: git clone --depth 1 --filter=blob:none --sparse https://github.com/google/fonts gf
       cd gf && git sparse-checkout set ofl/poppins ofl/anton ofl/rozhaone ; pass --fonts gf/ofl
"""
import argparse, os, statistics
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

HERE=os.path.dirname(os.path.abspath(__file__))
ap=argparse.ArgumentParser()
ap.add_argument('--cover',required=True); ap.add_argument('--name',required=True)
ap.add_argument('--garment',required=True); ap.add_argument('--code',required=True)
ap.add_argument('--sizes',default='XXS–4XL'); ap.add_argument('--level',default='')
ap.add_argument('--out',required=True); ap.add_argument('--fonts',default='gf/ofl')
ap.add_argument('--logo',default=os.path.join(HERE,'..','..','brand','sewcraftly-logo.png'))
A=ap.parse_args()

FD=A.fonts.rstrip('/')+'/'
def F(p,s): return ImageFont.truetype(FD+p,s)
POP=lambda w,s: F(f'poppins/Poppins-{w}.ttf',s)
ANTON=lambda s: F('anton/Anton-Regular.ttf',s)
ROZHA=lambda s: F('rozhaone/RozhaOne-Regular.ttf',s)
K=(22,22,22); CREAM=(243,239,234); W,H=1000,1500
LOGO=Image.open(A.logo).convert('RGBA')

# ---- sketch sticker + band colour from the cover ----
cov=Image.open(A.cover).convert('RGB')
reg=cov.crop((50,60,590,800)); g=reg.convert('L')
m=ImageChops.lighter(g.point(lambda v:255 if v>=246 else 0),g.point(lambda v:255 if v<150 else 0)).filter(ImageFilter.MaxFilter(3))
fl=m.copy()
for pt in((2,2),(reg.width-3,2),(2,reg.height-3),(reg.width-3,reg.height-3)):
    if fl.getpixel(pt)==0: ImageDraw.floodfill(fl,pt,128)
inside=fl.point(lambda v:0 if v==128 else 255).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
sticker=reg.copy(); sticker.putalpha(inside); sticker=sticker.crop(inside.point(lambda v:255 if v>128 else 0).getbbox())
strip=cov.crop((1165,5,1195,795)); px=list(strip.get_flattened_data()) if hasattr(strip,'get_flattened_data') else list(strip.getdata())
BAND=tuple(int(statistics.median(c[i] for c in px)) for i in range(3))

def fit(img,mw,mh):
    s=min(mw/img.width,mh/img.height); return img.resize((int(img.width*s),int(img.height*s)),Image.LANCZOS)
def shadowed(cv,img,pos,off=(8,10),blur=14,alpha=90):
    a=img.split()[3]; sh=Image.new('RGBA',img.size,(90,80,75,0)); sh.putalpha(a.point(lambda v:v*alpha//255))
    pad=40; big=Image.new('RGBA',(img.width+2*pad,img.height+2*pad),(0,0,0,0)); big.paste(sh,(pad,pad),sh)
    cv.alpha_composite(big.filter(ImageFilter.GaussianBlur(blur)),(pos[0]-pad+off[0],pos[1]-pad+off[1])); cv.alpha_composite(img,pos)
def ctext(d,y,t,font,cx=W//2,fill=K,spacing=0):
    if spacing:
        tw=sum(d.textlength(c,font=font)+spacing for c in t)-spacing; x=cx-tw/2
        for c in t: d.text((x,y),c,font=font,fill=fill); x+=d.textlength(c,font=font)+spacing
    else: d.text((cx-d.textlength(t,font=font)/2,y),t,font=font,fill=fill)
def autosize(d,texts,mk,maxw,start):
    s=start
    while max(d.textlength(t,font=mk(s)) for t in texts)>maxw: s-=2
    return mk(s)
def logo(cv,xy,width):
    l=LOGO.resize((width,int(LOGO.height*width/LOGO.width)),Image.LANCZOS); cv.alpha_composite(l,(int(xy[0]),int(xy[1]))); return l.height
def noise_bg(color,size=(W,H),amt=0.05):
    bg=Image.new('RGB',size,color); n=Image.effect_noise(size,20).convert('L')
    return Image.blend(bg,Image.merge('RGB',(n,n,n)),amt)
def pill(d,cx,y,text,font,fill=K,tc='white',padx=36,h=None):
    tw=d.textlength(text,font=font); h=h or int(font.size*1.9)
    d.rounded_rectangle((cx-tw/2-padx,y,cx+tw/2+padx,y+h),radius=h//2,fill=fill)
    d.text((cx-tw/2,y+(h-font.size*1.4)/2),text,font=font,fill=tc)

G=A.garment.upper()

def pin1(out):
    im=noise_bg(CREAM).convert('RGBA'); d=ImageDraw.Draw(im)
    hx0,hy0,hx1,hy1=40,40,960,620
    hero=noise_bg(BAND,(hx1-hx0,hy1-hy0),0.06).convert('RGBA')
    lay=Image.new('RGBA',hero.size,(0,0,0,0)); hd=ImageDraw.Draw(lay)
    for x in range(-400,1400,150): hd.polygon([(x,0),(x+40,0),(x-300,hero.height),(x-340,hero.height)],fill=(255,255,255,40))
    hero.alpha_composite(lay); im.alpha_composite(hero,(hx0,hy0))
    s=fit(sticker,820,540); shadowed(im,s,(W//2-s.width//2,hy0+(hy1-hy0-s.height)//2))
    d.text((hx0,hy1+14),f"THE {A.name.upper()}  ·  {A.code}",font=POP('Medium',20),fill=(60,60,60))
    l1,l2=f"FREE {G}",'SEWING PATTERN'
    tf=autosize(d,[l1,l2],ROZHA,860,120)
    ctext(d,700,l1,tf); ctext(d,700+tf.size,l2,tf)
    y0,y1=985,1370
    card=Image.new('RGBA',(430,y1-y0),(255,255,255,255))
    lh=logo(card,(18,14),190)
    sk=fit(sticker,380,card.height-lh-40); card.alpha_composite(sk,(card.width//2-sk.width//2,lh+26))
    shadowed(im,card,(60,y0),off=(4,6),blur=8,alpha=60)
    det=noise_bg(BAND,(430,y1-y0),0.06).convert('RGBA')
    top=int(sticker.height*0.42); al=sticker.split()[3].crop((0,0,sticker.width,top))
    cols=[(sum(al.crop((x,0,x+1,top)).get_flattened_data() if hasattr(al,'get_flattened_data') else al.crop((x,0,x+1,top)).getdata()),x) for x in range(int(sticker.width*0.45),int(sticker.width*0.8))]
    cut=min(cols)[1]
    crop=sticker.crop((0,0,cut,top))
    c=fit(crop,400,360); det.alpha_composite(c,(det.width//2-c.width//2,det.height-c.height+10))
    dd=ImageDraw.Draw(det); f=POP('SemiBold',18)
    dd.rounded_rectangle((20,18,20+dd.textlength('DETAILS',font=f)+28,54),radius=18,fill=K); dd.text((34,22),'DETAILS',font=f,fill='white')
    im.alpha_composite(det,(510,y0))
    ctext(d,1395,f"Sizes {A.sizes}  ·  PDF  ·  sewcraftly.com",POP('Medium',30))
    im.convert('RGB').save(out,quality=92)

def pin2(out):
    im=Image.new('RGBA',(W,H),(255,255,255,255)); d=ImageDraw.Draw(im)
    logo(im,(50,36),400)
    pf=POP('SemiBold',26); t='FREE PDF'; tw=d.textlength(t,font=pf)
    d.rounded_rectangle((W-60-tw-50,62,W-60,122),radius=30,fill=K); d.text((W-60-tw-25,72),t,font=pf,fill='white')
    ctext(d,215,f"{A.name.upper()}  ·  {A.code}",POP('Medium',22),fill=(90,90,90),spacing=3)
    s=fit(sticker,860,790); im.alpha_composite(s,(W//2-s.width//2,272+(790-s.height)//2))
    by=1080; d.rectangle((0,by,W,H),fill=BAND)
    t=f"FREE {G} SEWING PATTERN"; tf=autosize(d,[t],ANTON,880,96); ctext(d,by+40+(96-tf.size)//2,t,tf)
    sub=POP('SemiBold',34); t='+ Step-by-Step Instructions'; tw=d.textlength(t,font=sub)
    d.rounded_rectangle((W//2-tw/2-36,by+170,W//2+tw/2+36,by+238),radius=34,fill=(255,255,255)); ctext(d,by+180,t,sub)
    ctext(d,by+262,f"Sizes {A.sizes}"+(f"  ·  {A.level}" if A.level else ''),POP('Italic',30))
    d.line((W//2-45,by+328,W//2+45,by+328),fill=K,width=4)
    ctext(d,by+344,'sewcraftly.com',POP('Medium',30),spacing=4)
    im.convert('RGB').save(out,quality=92)

os.makedirs(os.path.dirname(os.path.abspath(A.out)),exist_ok=True)
pin1(A.out+'-pin1.jpg'); pin2(A.out+'-pin2.jpg')
print('band',BAND,'->',A.out+'-pin1.jpg',A.out+'-pin2.jpg')
