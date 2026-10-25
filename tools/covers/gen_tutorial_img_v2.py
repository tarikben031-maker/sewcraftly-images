import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S=sys.argv[1]; out=sys.argv[2]; name=sys.argv[3]
FD='/usr/share/fonts/truetype/google-fonts/'; F=lambda n,s: ImageFont.truetype(FD+n,s)
W=1200; bg=Image.new('RGB',(W,W),(244,238,232)); d=ImageDraw.Draw(bg)
TERRA=(196,112,86); K=(30,27,25)
def page(p,w,angle,pos):
    im=Image.open(p).convert('RGB'); im=im.resize((w,round(im.height*w/im.width)),Image.LANCZOS)
    big=Image.new('RGBA',(im.width+100,im.height+100),(0,0,0,0))
    sh=Image.new('L',big.size,0); ImageDraw.Draw(sh).rectangle((50,60,50+im.width,60+im.height),fill=90); sh=sh.filter(ImageFilter.GaussianBlur(16))
    big.paste((70,55,50,255),(0,0),sh); big.paste(im,(50,50))
    big=big.rotate(angle,expand=True,resample=Image.BICUBIC); bg.paste(big,pos,big)
page(f'{S}/p-04.png',470,6,(70,420)); page(f'{S}/p-14.png',470,-6,(690,420)); page(f'{S}/p-01.png',400,0,(350,350))
d=ImageDraw.Draw(bg)
f=F('Poppins-SemiBold.ttf',30) if False else F('Poppins-Medium.ttf',30); t='Printable sewing tutorial'; tw=d.textlength(t,font=f)
d.rounded_rectangle((W/2-tw/2-40,40,W/2+tw/2+40,108),radius=34,fill=TERRA); d.text((W/2,74),t,font=f,fill='white',anchor='mm')
d.text((W/2,175),name,font=F('Poppins-Bold.ttf',64),fill=K,anchor='mm')
d.text((W/2,245),'Illustrated step-by-step guide · PDF',font=F('Poppins-Medium.ttf',30),fill=(70,62,58),anchor='mm')
f=F('Poppins-Medium.ttf',28); t='Size charts · Fabric amounts · Video guides · Instant download'; tw=d.textlength(t,font=f)
d.rounded_rectangle((W/2-tw/2-40,1080,W/2+tw/2+40,1150),radius=35,fill=K); d.text((W/2,1115),t,font=f,fill='white',anchor='mm')
bg.save(out,quality=92)
