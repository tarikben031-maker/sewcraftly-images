#!/usr/bin/env python3
"""SewCraftly Instagram / Facebook post generator (1080x1350, 4:5).

Usage:
  python3 gen.py --cover covers/X.jpg --name "Spaghetti Strap Dress" --code SC1006 \
      --sizes "XXS–4XL" --level Intermediate --photo photos/X-model.jpg --out social/X-SC1006-ig.jpg
The sketch sticker and band colour come from the house cover (same as the pins).
Everything important stays inside the centre 1012 px so the 3:4 profile-grid crop keeps it.
Fonts: git clone --depth 1 --filter=blob:none --sparse https://github.com/google/fonts gf
       cd gf && git sparse-checkout set ofl/poppins ofl/anton ofl/rozhaone ; pass --fonts gf/ofl
"""
import argparse, os, statistics
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument('--cover', required=True); ap.add_argument('--name', required=True)
ap.add_argument('--code', required=True); ap.add_argument('--sizes', default='XXS–4XL')
ap.add_argument('--level', default=''); ap.add_argument('--photo', default=None)
ap.add_argument('--out', required=True); ap.add_argument('--fonts', default='gf/ofl')
ap.add_argument('--logo', default=os.path.join(HERE, '..', '..', 'brand', 'sewcraftly-logo.png'))
A = ap.parse_args()

FD = A.fonts.rstrip('/') + '/'
def F(p, s): return ImageFont.truetype(FD + p, s)
POP = lambda w, s: F(f'poppins/Poppins-{w}.ttf', s)
ROZHA = lambda s: F('rozhaone/RozhaOne-Regular.ttf', s)
K = (22, 22, 22); CREAM = (243, 239, 234); W, H = 1080, 1350
LOGO = Image.open(A.logo).convert('RGBA')

# ---- sketch sticker + band colour from the cover (same method as tools/pins/gen.py) ----
cov = Image.open(A.cover).convert('RGB')
reg = cov.crop((50, 60, 590, 800)); g = reg.convert('L')
m = ImageChops.lighter(g.point(lambda v: 255 if v >= 246 else 0), g.point(lambda v: 255 if v < 150 else 0)).filter(ImageFilter.MaxFilter(3))
fl = m.copy()
for pt in ((2, 2), (reg.width - 3, 2), (2, reg.height - 3), (reg.width - 3, reg.height - 3)):
    if fl.getpixel(pt) == 0: ImageDraw.floodfill(fl, pt, 128)
inside = fl.point(lambda v: 0 if v == 128 else 255).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
sticker = reg.copy(); sticker.putalpha(inside); sticker = sticker.crop(inside.point(lambda v: 255 if v > 128 else 0).getbbox())
strip = cov.crop((1165, 5, 1195, 795)); px = list(strip.get_flattened_data() if hasattr(strip, 'get_flattened_data') else strip.getdata())
BAND = tuple(int(statistics.median(c[i] for c in px)) for i in range(3))

def fit(img, mw, mh):
    s = min(mw / img.width, mh / img.height); return img.resize((int(img.width * s), int(img.height * s)), Image.LANCZOS)
def shadowed(cv, img, pos, off=(8, 10), blur=14, alpha=90):
    a = img.split()[3]; sh = Image.new('RGBA', img.size, (90, 80, 75, 0)); sh.putalpha(a.point(lambda v: v * alpha // 255))
    pad = 40; big = Image.new('RGBA', (img.width + 2 * pad, img.height + 2 * pad), (0, 0, 0, 0)); big.paste(sh, (pad, pad), sh)
    cv.alpha_composite(big.filter(ImageFilter.GaussianBlur(blur)), (pos[0] - pad + off[0], pos[1] - pad + off[1])); cv.alpha_composite(img, pos)
def ctext(d, y, t, font, cx=W // 2, fill=K, spacing=0):
    if spacing:
        tw = sum(d.textlength(c, font=font) + spacing for c in t) - spacing; x = cx - tw / 2
        for c in t: d.text((x, y), c, font=font, fill=fill); x += d.textlength(c, font=font) + spacing
    else: d.text((cx - d.textlength(t, font=font) / 2, y), t, font=font, fill=fill)
def autosize(d, texts, mk, maxw, start):
    s = start
    while max(d.textlength(t, font=mk(s)) for t in texts) > maxw: s -= 2
    return mk(s)
def noise_bg(color, size=(W, H), amt=0.05):
    bg = Image.new('RGB', size, color); n = Image.effect_noise(size, 20).convert('L')
    return Image.blend(bg, Image.merge('RGB', (n, n, n)), amt)
def cover_crop(ph, w, h, fy=0.5):
    s = max(w / ph.width, h / ph.height); p = ph.resize((int(ph.width * s) + 1, int(ph.height * s) + 1), Image.LANCZOS)
    x = (p.width - w) // 2; y = int((p.height - h) * fy); return p.crop((x, y, x + w, y + h))
def split_title(d, name, font_maker, maxw):
    words = name.split(); best = None
    for i in range(1, len(words)):
        a, b = ' '.join(words[:i]), ' '.join(words[i:]); w = max(d.textlength(a, font=font_maker(100)), d.textlength(b, font=font_maker(100)))
        if best is None or w < best[0]: best = (w, [a, b])
    one = d.textlength(name, font=font_maker(100))
    return [name] if len(words) < 2 or one * 0.9 < maxw * 100 / 110 else best[1]

im = noise_bg(CREAM).convert('RGBA'); d = ImageDraw.Draw(im)

# ---- hero: model photo | sketch on band colour ----
hx0, hy0, hx1, hy1 = 56, 56, W - 56, 820
hero = noise_bg(BAND, (hx1 - hx0, hy1 - hy0), 0.06).convert('RGBA'); im.alpha_composite(hero, (hx0, hy0))
if A.photo:
    pw = 470
    ph = cover_crop(Image.open(A.photo).convert('RGB'), pw, hy1 - hy0, 0.35)
    im.paste(ph, (hx0, hy0))
    s = fit(sticker, hx1 - hx0 - pw - 50, hy1 - hy0 - 90)
    shadowed(im, s, (hx0 + pw + (hx1 - hx0 - pw - s.width) // 2, hy0 + (hy1 - hy0 - s.height) // 2))
else:
    s = fit(sticker, hx1 - hx0 - 120, hy1 - hy0 - 100)
    shadowed(im, s, (W // 2 - s.width // 2, hy0 + (hy1 - hy0 - s.height) // 2))

# "FREE PDF PATTERN" badge, overlapping the bottom edge of the hero
bf = POP('Bold', 30); t = 'FREE PDF PATTERN'; tw = d.textlength(t, font=bf); bh = 70
bx0 = W // 2 - tw / 2 - 40; by0 = hy1 - bh // 2
d.rounded_rectangle((bx0, by0, W // 2 + tw / 2 + 40, by0 + bh), radius=bh // 2, fill=K)
d.text((W // 2 - tw / 2, by0 + (bh - bf.size * 1.42) / 2), t, font=bf, fill='white')

# ---- title block ----
meta = f"{A.code}" + (f"  ·  {A.level.upper()}" if A.level else '')
ctext(d, 880, meta, POP('SemiBold', 26), spacing=4)
lines = split_title(d, A.name, ROZHA, 940)
tf = autosize(d, lines, ROZHA, 940, 104 if len(lines) == 2 else 110)
y = 915
for ln in lines:
    ctext(d, y, ln, tf); y += int(tf.size * 1.02)
ctext(d, y + 34, f"Sizes {A.sizes}  ·  A4 · US Letter · A0", POP('Medium', 30))

# ---- footer: logo + link in bio ----
fy = 1215
lw = 250; lh = int(LOGO.height * lw / LOGO.width)
im.alpha_composite(LOGO.resize((lw, lh), Image.LANCZOS), (96, fy + (80 - lh) // 2))
lf = POP('SemiBold', 26); t = 'Link in bio  ·  sewcraftly.com'; tw = d.textlength(t, font=lf)
d.rounded_rectangle((W - 96 - tw - 60, fy + 8, W - 96, fy + 72), radius=32, fill=BAND)
d.text((W - 96 - tw - 30, fy + 8 + (64 - lf.size * 1.42) / 2), t, font=lf, fill=K)

os.makedirs(os.path.dirname(os.path.abspath(A.out)), exist_ok=True)
im.convert('RGB').save(A.out, quality=92)
print('band', BAND, '->', A.out)
