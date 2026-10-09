"""SewCraftly post cover generator (validated by the user on SC1010, oct 2026).

Layout (1650x1100): real model photo on the left, terracotta divider; on the right
the garment keyword title (never the pattern name), subtitle, black pill
"FREE PDF SEWING PATTERN", terracotta pill "PATTERN CODE | #SCxxxx", check list,
SKILL LEVEL badge, front+back sketch in a white card (no FRONT/BACK labels),
black bottom bar with the site logo + sewcraftly.com centred.

usage:
  python3 tools/covers/gen_cover.py PHOTO SKETCH OUT.jpg \
      --title "Flutter Sleeve Crop Top|& Maxi Skirt" --subtitle "Two-Piece Set" \
      --code SC1010 --sizes "XXS – 4XL" --formats "A4 & US Letter" --level 2

  --title   use "|" to split into lines (2 lines max recommended)
  --level   1=Beginner 2=Intermediate 3=Advanced
  --photo-x horizontal centre of the photo crop, 0..1 (default 0.5)
"""
import argparse, math, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))

ap = argparse.ArgumentParser()
ap.add_argument('photo'); ap.add_argument('sketch'); ap.add_argument('out')
ap.add_argument('--title', required=True)
ap.add_argument('--subtitle', default='')
ap.add_argument('--code', required=True)
ap.add_argument('--sizes', default='XXS – 4XL')
ap.add_argument('--formats', default='A4 & US Letter')
ap.add_argument('--level', type=int, default=1, choices=[1, 2, 3])
ap.add_argument('--photo-x', type=float, default=0.5)
ap.add_argument('--logo', default=os.path.join(REPO, 'brand', 'sewcraftly-icon.png'))
ap.add_argument('--fonts', default=None, help='dir containing Poppins-*.ttf')
a = ap.parse_args()

FONT_DIRS = [a.fonts, '/usr/share/fonts/truetype/google-fonts/', 'gf/ofl/poppins/']
def F(name, size):
    for d_ in FONT_DIRS:
        if d_ and os.path.exists(os.path.join(d_, name)):
            return ImageFont.truetype(os.path.join(d_, name), size)
    raise SystemExit(f'font {name} not found; pass --fonts')

W, H = 1650, 1100
CREAM = (247, 240, 233)
TERRA = (181, 83, 60)
INK = (30, 27, 25)
MUTED = (110, 98, 90)
code = a.code if a.code.startswith('#') else '#' + a.code
keyword = a.title.replace('|', '\n')
LEVEL = {1: 'Beginner', 2: 'Intermediate', 3: 'Advanced'}[a.level]

img = Image.new('RGB', (W, H), CREAM)
d = ImageDraw.Draw(img)

# --- left: real photo, full height
PW = 620
ph = Image.open(a.photo).convert('RGB')
s = H / ph.height
ph = ph.resize((max(PW, round(ph.width * s)), H), Image.LANCZOS)
cx = min(max(round(ph.width * a.photo_x), PW // 2), ph.width - PW // 2)
img.paste(ph.crop((cx - PW // 2, 0, cx + PW // 2, H)), (0, 0))
d.rectangle((PW, 0, PW + 10, H), fill=TERRA)

# --- sketch card (front + back)
sk = Image.open(a.sketch).convert('RGB')
SW = 400
sk = sk.resize((SW, round(sk.height * SW / sk.width)), Image.LANCZOS)
if sk.height > 444:  # keep the card above the bottom bar
    SH = 444
    sk = sk.resize((round(sk.width * SH / sk.height), SH), Image.LANCZOS)
sx, sy = W - 62 - SW + (SW - sk.width) // 2, 502
card = (W - 62 - SW - 28, sy - 28, W - 62 + 28, sy + sk.height + 28)
sh = Image.new('L', (W, H), 0)
ImageDraw.Draw(sh).rounded_rectangle(card, 26, fill=70)
sh = sh.filter(ImageFilter.GaussianBlur(18))
img.paste(Image.new('RGB', (W, H), (120, 90, 70)), (0, 8), sh)
d = ImageDraw.Draw(img)
d.rounded_rectangle(card, 26, fill=(255, 255, 255))
img.paste(sk, (sx, sy))

# --- text column
tx = PW + 70
maxw = W - 60 - tx
size = 96
while True:
    kf = F('Poppins-Bold.ttf', size)
    if max(d.textlength(l, font=kf) for l in keyword.split('\n')) <= maxw:
        break
    size -= 2
d.multiline_text((tx, 80), keyword, font=kf, fill=INK, spacing=6)
tb = d.multiline_textbbox((tx, 80), keyword, font=kf, spacing=6)
bottom = tb[3]
if a.subtitle:
    d.text((tx, bottom + 18), a.subtitle, font=F('Poppins-Light.ttf', 40), fill=MUTED)
    bottom += 82
else:
    bottom += 18

# black pill
pf = F('Poppins-Bold.ttf', 40)
py = bottom + 18
lab = 'FREE PDF SEWING PATTERN'
d.rounded_rectangle((tx, py, tx + d.textlength(lab, font=pf) + 60, py + 76), 38, fill=INK)
d.text((tx + 30, py + 38), lab, font=pf, fill='white', anchor='lm')

# pattern code pill
ty = py + 76 + 20
th = 64
cf = F('Poppins-Bold.ttf', 21)
kf2 = F('Poppins-Bold.ttf', 34)
lw_ = d.textlength('PATTERN CODE', font=cf)
x1 = tx + 28 + lw_ + 34 + d.textlength(code, font=kf2) + 30
d.rounded_rectangle((tx, ty, x1, ty + th), th // 2, fill=TERRA)
d.text((tx + 28, ty + th // 2), 'PATTERN CODE', font=cf, fill='white', anchor='lm')
d.line((tx + 28 + lw_ + 17, ty + 16, tx + 28 + lw_ + 17, ty + th - 16), fill='white', width=2)
d.text((tx + 28 + lw_ + 34, ty + th // 2 + 1), code, font=kf2, fill='white', anchor='lm')

# check list
ff = F('Poppins-Medium.ttf', 30)
y = max(610, ty + th + 40)
for t in [f'Sizes {a.sizes}', a.formats, 'Step-by-step instructions']:
    d.ellipse((tx, y + 4, tx + 34, y + 38), fill=TERRA)
    d.line((tx + 9, y + 21, tx + 15, y + 28, tx + 26, y + 13), fill='white', width=4)
    d.text((tx + 52, y + 21), t, font=ff, fill=INK, anchor='lm')
    y += 58

# skill level badge
y += 22
Hh = 64
lf = F('Poppins-Bold.ttf', 20)
vf = F('Poppins-Bold.ttf', 25)
lab = 'SKILL LEVEL'
lw = d.textlength(lab, font=lf) + 40
vw = d.textlength(LEVEL, font=vf) + 3 * 25 + 44
shm = Image.new('L', (W, H), 0)
ImageDraw.Draw(shm).rounded_rectangle((tx, y, tx + lw + vw, y + Hh), Hh // 2, fill=60)
shm = shm.filter(ImageFilter.GaussianBlur(10))
img.paste(Image.new('RGB', (W, H), (120, 90, 70)), (0, 5), shm)
d = ImageDraw.Draw(img)
d.rounded_rectangle((tx, y, tx + lw + vw, y + Hh), Hh // 2, fill='white', outline=TERRA, width=3)
d.rounded_rectangle((tx, y, tx + lw + Hh // 2, y + Hh), Hh // 2, fill=TERRA)
d.rectangle((tx + lw, y + 3, tx + lw + Hh // 2, y + Hh - 3), fill='white')
d.text((tx + 22, y + Hh // 2), lab, font=lf, fill='white', anchor='lm')
vx = tx + lw + 20
for i in range(3):
    cx_, cy_ = vx + i * 25 + 9, y + Hh // 2
    pts = [(cx_, cy_ - 10), (cx_ + 9, cy_), (cx_, cy_ + 10), (cx_ - 9, cy_)]
    if i < a.level:
        d.polygon(pts, fill=TERRA)
    else:
        d.polygon(pts, outline=TERRA, width=2)
d.text((vx + 3 * 25 + 6, y + Hh // 2), LEVEL, font=vf, fill=INK, anchor='lm')

# --- bottom bar: logo + site, centred
BY = H - 110
d.rectangle((PW + 10, BY, W, H), fill=INK)
r = 36
lg = Image.open(a.logo).convert('RGBA').resize((2 * r, 2 * r), Image.LANCZOS)
m = Image.new('L', (2 * r, 2 * r), 0)
ImageDraw.Draw(m).rounded_rectangle((0, 0, 2 * r - 1, 2 * r - 1), 16, fill=255)
lg.putalpha(Image.fromarray(np.minimum(np.array(lg.getchannel('A')), np.array(m))))
sf = F('Poppins-Medium.ttf', 40)
grp = 2 * r + 22 + d.textlength('sewcraftly.com', font=sf)
gx = round((PW + 10 + W) / 2 - grp / 2)
img.paste(lg, (gx, BY + 55 - r), lg)
d.text((gx + 2 * r + 22, BY + 55), 'sewcraftly.com', font=sf, fill='white', anchor='lm')

img.save(a.out, quality=92)
print(a.out)
