"""SewCraftly tutorial square (1000x1000) for the pp-tut block.
usage: python3 tools/covers/gen_tutorial_img.py OUT.jpg PAGE1.png PAGE2.png PAGE3.png --name "Fitted Blazer" --code SC1016 --rgb 163,186,160
"""
import argparse
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ap=argparse.ArgumentParser(); ap.add_argument('out'); ap.add_argument('p1'); ap.add_argument('p2'); ap.add_argument('p3')
ap.add_argument('--name',required=True); ap.add_argument('--code',required=True); ap.add_argument('--rgb',default='163,186,160')
a=ap.parse_args(); col=tuple(int(x) for x in a.rgb.split(','))
FD='/usr/share/fonts/truetype/google-fonts/'; F=lambda n,s: ImageFont.truetype(FD+n,s)
W=1000
bg=Image.new('RGB',(W,W),(236,231,226)); px=bg.load()
for x in range(W):
    for y in range(W):
        t=min(1,max(0,(x*0.7+y*0.3-250)/750)); px[x,y]=tuple(int(236*(1-t)+c*t) for c in col) if False else tuple(int(b*(1-t)+c*t) for b,c in zip((236,231,226),col))
d=ImageDraw.Draw(bg)
d.text((70,110),'Sewing tutorial',font=F('Poppins-BoldItalic.ttf',74),fill=(20,20,20),stroke_width=9,stroke_fill='white')
d.text((72,235),'S T E P - B Y - S T E P   I L L U S T R A T E D   I N S T R U C T I O N S',font=F('Poppins-Bold.ttf',17),fill=(44,52,60))
# badge
cx,cy,r=860,170,112
d.ellipse((cx-r-8,cy-r-8,cx+r+8,cy+r+8),fill='white'); d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=(40,42,64))
d.text((cx,cy-62),'PRINTABLE',font=F('Poppins-Bold.ttf',27),fill='white',anchor='mm')
d.text((cx,cy-4),'PDF',font=F('Poppins-Bold.ttf',78),fill='white',anchor='mm')
d.text((cx,cy+62),'instant download',font=F('Poppins-Italic.ttf',21),fill='white',anchor='mm')
def page(p,w,angle,pos):
    im=Image.open(p).convert('RGB'); im=im.resize((w,round(im.height*w/im.width)),Image.LANCZOS)
    big=Image.new('RGBA',(im.width+80,im.height+80),(0,0,0,0)); 
    sh=Image.new('L',big.size,0); ImageDraw.Draw(sh).rectangle((40,48,40+im.width,48+im.height),fill=110); sh=sh.filter(ImageFilter.GaussianBlur(14))
    big.paste((60,50,50,255),(0,0),sh); big.paste(im,(40,40))
    big=big.rotate(angle,expand=True,resample=Image.BICUBIC); bg.paste(big,pos,big)
page(a.p3,560,-5,(470,420)); page(a.p2,560,-3,(250,370)); page(a.p1,560,2,(90,350))
d=ImageDraw.Draw(bg)
d.text((930,870),a.name,font=F('Poppins-BoldItalic.ttf',62),fill=(20,20,20),stroke_width=7,stroke_fill='white',anchor='rm')
d.text((930,935),f'#{a.code} · sewcraftlypatterns.com',font=F('Poppins-Bold.ttf',36),fill=(20,20,20),stroke_width=5,stroke_fill='white',anchor='rm')
bg.save(a.out,quality=92)
