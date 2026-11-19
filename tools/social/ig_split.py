"""SewCraftly Instagram 4:5 split visual (style of SC1041): photo left, garment-colour panel right."""
import argparse
from PIL import Image, ImageDraw, ImageFont, ImageOps
import numpy as np
ap = argparse.ArgumentParser()
ap.add_argument('--photo', required=True); ap.add_argument('--sketch', required=True); ap.add_argument('--out', required=True)
ap.add_argument('--title', required=True); ap.add_argument('--code', required=True)
ap.add_argument('--chips', default='Sizes 35 – 52|A4 & US Letter|Beginner')
ap.add_argument('--color', default=None, help='panel colour r,g,b (default: sampled from photo centre)')
ap.add_argument('--icon', default='brand/sewcraftly-icon.png')
ap.add_argument('--photo-x', type=float, default=0.5)
a = ap.parse_args()
GF = '/usr/share/fonts/truetype/google-fonts/'
B = lambda s: ImageFont.truetype(GF+'Poppins-Bold.ttf', s); M = lambda s: ImageFont.truetype(GF+'Poppins-Medium.ttf', s); R = lambda s: ImageFont.truetype(GF+'Poppins-Regular.ttf', s)
W, H, PW, ST, BAR = 1080, 1350, 560, 14, 130
TERRA = (181, 83, 60); DARK = (37, 29, 27); CREAM = (247, 240, 233)
ph = Image.open(a.photo).convert('RGB')
if a.color: col = tuple(int(v) for v in a.color.split(','))
else:
    arr = np.array(ph); h, w = arr.shape[:2]
    col = tuple(int(v*0.82) for v in np.median(arr[int(h*.3):int(h*.45), int(w*.4):int(w*.6)].reshape(-1,3), axis=0))
img = Image.new('RGB', (W, H), col); d = ImageDraw.Draw(img)
# photo
ph_h = H - BAR; sc = ph_h / ph.height; pw_full = int(ph.width*sc)
p2 = ph.resize((pw_full, ph_h), Image.LANCZOS); x0 = int((pw_full-PW)*a.photo_x)
img.paste(p2.crop((x0, 0, x0+PW, ph_h)), (0, 0))
d.rectangle((PW, 0, PW+ST, H-BAR), fill=TERRA)
L = PW + ST + 46; Rr = W - 40; cx = (L + Rr)//2
# pill
f = B(25); t = 'FREE PDF + STEP-BY-STEP'; tw = d.textlength(t, font=f)
d.rounded_rectangle((L, 78, L+tw+52, 78+60), radius=30, fill=CREAM); d.text((L+26, 108), t, font=f, fill=DARK, anchor='lm')
# title
y = 172
s = 64
while any(d.textlength(l, font=B(s)) > Rr-L for l in a.title.split('|')) and s > 40: s -= 2
for line in a.title.split('|'):
    d.text((L, y), line, font=B(s), fill='white'); y += int(s*1.12)
d.text((L, y+10), 'Free sewing pattern', font=R(30), fill=(240, 236, 228)); y += 70
# sketch in white lines
sk = Image.open(a.sketch).convert('L'); arr = np.array(sk)
mask = Image.fromarray(((arr < 200)*255).astype('uint8'))
top, bot = y + 30, 860
mh = bot - top; mw = Rr - L
sc = min(mw/sk.width, mh/sk.height)
mask = mask.resize((int(sk.width*sc), int(sk.height*sc)), Image.LANCZOS)
from PIL import ImageFilter
mask = mask.filter(ImageFilter.MaxFilter(3))
white = Image.new('RGB', mask.size, 'white')
img.paste(white, (cx - mask.width//2, top + (mh-mask.height)//2), mask)
# chips
chips = ['#'+a.code.lstrip('#')] + a.chips.split('|')
f = B(27); x, y = L, 920
for i, c in enumerate(chips):
    w = d.textlength(c, font=f) + 52
    if x + w > Rr: x = L; y += 82
    if i == 0: d.rounded_rectangle((x, y, x+w, y+62), radius=31, fill=TERRA)
    else: d.rounded_rectangle((x, y, x+w, y+62), radius=31, outline='white', width=3)
    d.text((x+26, y+31), c, font=f, fill='white', anchor='lm'); x += w + 16
# bottom bar
d.rectangle((0, H-BAR, W, H), fill=DARK)
ic = Image.open(a.icon).convert('RGBA'); ic = ic.resize((74, int(74*ic.height/ic.width)), Image.LANCZOS)
img.paste(ic, (52, H-BAR + (BAR-ic.height)//2), ic)
d.text((52+74+22, H-BAR//2), 'sewcraftlypatterns.com', font=B(38), fill='white', anchor='lm')
f = B(28); t = 'Link in bio'; tw = d.textlength(t, font=f)
d.rounded_rectangle((W-52-tw-60, H-BAR//2-32, W-52, H-BAR//2+32), radius=32, fill=TERRA); d.text((W-52-tw/2-30, H-BAR//2), t, font=f, fill='white', anchor='mm')
img.save(a.out, quality=90); print('panel', col, a.out)
