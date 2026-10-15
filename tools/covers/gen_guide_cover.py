"""SewCraftly tutorial/guide cover (1200x630) used as featured image + og:image.

usage: python3 tools/covers/gen_guide_cover.py OUT.jpg --title "How to Choose|Fabric for|Sewing Patterns" --motif fabric
motifs: measure | size | fabric | print
"""
import argparse, os
from PIL import Image, ImageDraw, ImageFont
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
ap = argparse.ArgumentParser()
ap.add_argument('out'); ap.add_argument('--title', required=True)
ap.add_argument('--motif', default='fabric', choices=['measure', 'size', 'fabric', 'print'])
ap.add_argument('--tag', default='FREE SEWING GUIDE')
a = ap.parse_args()

FD = '/usr/share/fonts/truetype/google-fonts/'
F = lambda n, s: ImageFont.truetype(FD + n, s)
W, H = 1200, 630
CREAM, TERRA, INK, NAVY, ROSE = (247, 240, 233), (181, 83, 60), (30, 27, 25), (44, 62, 80), (192, 132, 151)
img = Image.new('RGB', (W, H), CREAM)
d = ImageDraw.Draw(img)

# left text
lines = a.title.split('|')
size = 84
while True:
    f = F('Poppins-Bold.ttf', size)
    if max(d.textlength(l, font=f) for l in lines) <= 640:
        break
    size -= 2
tx, ty = 70, 70
pf = F('Poppins-Bold.ttf', 26)
tw = d.textlength(a.tag, font=pf)
d.rounded_rectangle((tx, ty, tx + tw + 50, ty + 56), 28, fill=TERRA)
d.text((tx + 25, ty + 28), a.tag, font=pf, fill='white', anchor='lm')
d.multiline_text((tx, ty + 96), '\n'.join(lines), font=f, fill=INK, spacing=8)

# motif card
cx0, cy0, cx1, cy1 = 760, 70, 1130, 470
d.rounded_rectangle((cx0, cy0, cx1, cy1), 30, fill='white', outline=(230, 221, 214), width=3)
m = a.motif
if m == 'fabric':  # woven vs knit swatches
    for i in range(0, 8):
        for j in range(0, 4):
            x, y = cx0 + 30 + i * 20, cy0 + 40 + j * 20
            d.rectangle((x, y, x + 18, y + 18), fill=ROSE if (i + j) % 2 == 0 else NAVY)
    for j in range(5):
        for i in range(7):
            x, y = cx0 + 40 + i * 44, cy0 + 190 + j * 38
            d.line((x, y, x + 20, y + 28, x + 40, y), fill=ROSE, width=7, joint='curve')
    d.text((cx0 + 30, cy0 + 12), 'WOVEN', font=F('Poppins-Bold.ttf', 18), fill=NAVY)
    d.text((cx0 + 30, cy0 + 150), 'KNIT', font=F('Poppins-Bold.ttf', 18), fill=NAVY)
elif m == 'measure':  # tape measure + body ellipses
    d.rounded_rectangle((cx0 + 40, cy0 + 40, cx1 - 40, cy0 + 110), 14, fill=(250, 226, 150), outline=NAVY, width=3)
    for k in range(0, 24):
        x = cx0 + 52 + k * 11
        d.line((x, cy0 + 40, x, cy0 + (75 if k % 5 == 0 else 60)), fill=NAVY, width=2)
    for k, (yy, rw) in enumerate([(190, 80), (260, 56), (330, 92)]):
        cxm = (cx0 + cx1) // 2
        d.ellipse((cxm - rw, cy0 + yy - 16, cxm + rw, cy0 + yy + 16), outline=ROSE, width=6)
    d.line(((cx0 + cx1) // 2, cy0 + 150, (cx0 + cx1) // 2, cy0 + 370), fill=NAVY, width=4)
elif m == 'size':  # size chart bars
    for k, (lab, wd) in enumerate([('XS', 90), ('S', 130), ('M', 170), ('L', 210), ('XL', 250)]):
        y = cy0 + 50 + k * 65
        d.rounded_rectangle((cx0 + 40, y, cx0 + 40 + wd, y + 42), 21, fill=TERRA if lab == 'M' else ROSE)
        d.text((cx0 + 58, y + 21), lab, font=F('Poppins-Bold.ttf', 22), fill='white', anchor='lm')
else:  # print: stacked pages with test square
    for k in range(3):
        o = k * 26
        d.rectangle((cx0 + 70 + o, cy0 + 50 + o, cx0 + 230 + o, cy0 + 260 + o), fill='white', outline=NAVY, width=3)
    d.rectangle((cx0 + 70 + 52 + 22, cy0 + 50 + 52 + 22, cx0 + 70 + 52 + 22 + 60, cy0 + 50 + 52 + 22 + 60), outline=TERRA, width=4)
    d.text((cx0 + 70 + 52 + 52, cy0 + 50 + 52 + 52), '4 in', font=F('Poppins-Bold.ttf', 20), fill=TERRA, anchor='mm')
    d.rounded_rectangle((cx0 + 70, cy0 + 310, cx1 - 70, cy0 + 360), 25, fill=INK)
    d.text(((cx0 + cx1) // 2, cy0 + 335), 'PRINT AT 100%', font=F('Poppins-Bold.ttf', 20), fill='white', anchor='mm')

# bottom bar
BY = H - 110
d.rectangle((0, BY, W, H), fill=INK)
r = 34
lg = Image.open(os.path.join(REPO, 'brand', 'sewcraftly-icon.png')).convert('RGBA').resize((2 * r, 2 * r), Image.LANCZOS)
mk = Image.new('L', (2 * r, 2 * r), 0)
ImageDraw.Draw(mk).rounded_rectangle((0, 0, 2 * r - 1, 2 * r - 1), 16, fill=255)
lg.putalpha(Image.fromarray(np.minimum(np.array(lg.getchannel('A')), np.array(mk))))
sf = F('Poppins-Medium.ttf', 38)
grp = 2 * r + 22 + d.textlength('sewcraftlypatterns.com', font=sf)
gx = round(W / 2 - grp / 2)
img.paste(lg, (gx, BY + 55 - r), lg)
d.text((gx + 2 * r + 22, BY + 55), 'sewcraftlypatterns.com', font=sf, fill='white', anchor='lm')
img.save(a.out, quality=92)
print(a.out)
