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
ap.add_argument('--style', default='split', choices=['split', 'photo', 'sketch'])
ap.add_argument('--fabric', default='')
ap.add_argument('--keyword', default='', help='search keyword shown as the headline, e.g. "Maxi Slip Dress"; the second line is always "Sewing Pattern"')
ap.add_argument('--line2', default='Free Sewing Pattern')
ap.add_argument('--badge', default='PDF + STEP-BY-STEP')
ap.add_argument('--axes', default='', help='"FRONT_X,BACK_X": centre lines of the front (left) and back (right) sketch inside the cover sticker; each is rebuilt by mirroring its visible half so they no longer overlap')
ap.add_argument('--front', default=None); ap.add_argument('--back', default=None)
ap.add_argument('--sketch', default=None, help='clean front-only sketch on white; used instead of the sticker cut from the cover (photo + front sketch layout)')
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
if A.sketch:
    # clean sketch on white: silhouette mask + white outline sticker (same method as tools/pins/gen.py)
    src = Image.open(A.sketch).convert('RGB'); pad = 30
    big = Image.new('RGB', (src.width + 2 * pad, src.height + 2 * pad), 'white'); big.paste(src, (pad, pad)); src = big
    gi = ImageChops.invert(src.convert('L')); ln = gi.point(lambda v: 255 if v > 60 else 0).filter(ImageFilter.MaxFilter(15))
    fl2 = ln.copy(); ImageDraw.floodfill(fl2, (0, 0), 128)
    sil = fl2.point(lambda v: 0 if v == 128 else 255).filter(ImageFilter.MinFilter(5))
    outl = sil.filter(ImageFilter.MaxFilter(17))
    st = Image.new('RGBA', src.size, (0, 0, 0, 0)); st.paste((255, 255, 255, 255), (0, 0), outl)
    st.paste(src, (0, 0), ImageChops.lighter(sil, gi))
    sticker = st.crop(outl.getbbox())
strip = cov.crop((1165, 5, 1195, 795)); px = list(strip.get_flattened_data() if hasattr(strip, 'get_flattened_data') else strip.getdata())
BAND = tuple(int(statistics.median(c[i] for c in px)) for i in range(3))

def _mirror(im, ax, keep_left):
    half = im.crop((0, 0, ax, im.height)) if keep_left else im.crop((ax, 0, im.width, im.height))
    out = Image.new('RGBA', (2 * half.width, im.height))
    if keep_left: out.paste(half, (0, 0)); out.paste(half.transpose(Image.FLIP_LEFT_RIGHT), (half.width, 0))
    else: out.paste(half.transpose(Image.FLIP_LEFT_RIGHT), (0, 0)); out.paste(half, (half.width, 0))
    return out.crop(out.getbbox())
PAIR = None
if A.front and A.back:
    PAIR = [Image.open(A.front).convert('RGBA'), Image.open(A.back).convert('RGBA')]
elif A.axes:
    fx, bx = [int(v) for v in A.axes.split(',')]
    PAIR = [_mirror(sticker, fx, True), _mirror(sticker, bx, False)]

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

def style_split():
    im = noise_bg(CREAM).convert('RGBA'); d = ImageDraw.Draw(im)

    # ---- hero: model photo | sketch on band colour ----
    hx0, hy0, hx1, hy1 = 56, 56, W - 56, 820
    hero = noise_bg(BAND, (hx1 - hx0, hy1 - hy0), 0.06).convert('RGBA'); im.alpha_composite(hero, (hx0, hy0))
    if A.photo:
        pw = 470
        ph = cover_crop(Image.open(A.photo).convert('RGB'), pw, hy1 - hy0, 0.35)
        im.paste(ph, (hx0, hy0))
        if PAIR:
            # left sketch = FRONT, right sketch = BACK, each labelled underneath
            lab_h = 58
            aw, ah, gap = hx1 - hx0 - pw - 50, hy1 - hy0 - 100 - lab_h, 14
            sc = min((aw - gap) / (PAIR[0].width + PAIR[1].width), ah / max(p.height for p in PAIR))
            ps = [p.resize((int(p.width * sc), int(p.height * sc)), Image.LANCZOS) for p in PAIR]
            tw = ps[0].width + gap + ps[1].width; x = hx0 + pw + (hx1 - hx0 - pw - tw) // 2
            base = hy0 + (hy1 - hy0 + max(p.height for p in ps) - lab_h) // 2 - 12
            lf = POP('SemiBold', 24)
            for p, lab in zip(ps, ('FRONT', 'BACK')):
                shadowed(im, p, (x, base - p.height))
                ctext(ImageDraw.Draw(im), base + 22, lab, lf, cx=x + p.width // 2, spacing=5)
                x += p.width + gap
        else:
            s = fit(sticker, hx1 - hx0 - pw - 50, hy1 - hy0 - 90)
            shadowed(im, s, (hx0 + pw + (hx1 - hx0 - pw - s.width) // 2, hy0 + (hy1 - hy0 - s.height) // 2))
    else:
        s = fit(sticker, hx1 - hx0 - 120, hy1 - hy0 - 100)
        shadowed(im, s, (W // 2 - s.width // 2, hy0 + (hy1 - hy0 - s.height) // 2))

    # "FREE PDF PATTERN" badge, overlapping the bottom edge of the hero
    bf = POP('Bold', 30); t = A.badge; tw = d.textlength(t, font=bf); bh = 70
    bx0 = W // 2 - tw / 2 - 40; by0 = hy1 - bh // 2
    d.rounded_rectangle((bx0, by0, W // 2 + tw / 2 + 40, by0 + bh), radius=bh // 2, fill=K)
    d.text((W // 2 - tw / 2, by0 + (bh - bf.size * 1.42) / 2), t, font=bf, fill='white')

    # ---- title block ----
    meta = f"{A.code}" + (f"  ·  {A.level.upper()}" if A.level else '')
    ctext(d, 872, meta, POP('SemiBold', 26), spacing=4)
    lines = [A.keyword, A.line2] if A.keyword else split_title(d, A.name, ROZHA, 940)
    tf = autosize(d, lines, ROZHA, 880, 100 if len(lines) == 2 else 110)
    y = 905
    for ln in lines:
        ctext(d, y, ln, tf); y += int(tf.size * 1.02)
    ctext(d, y + 22, f"Sizes {A.sizes}  ·  A4 · US Letter · A0", POP('Medium', 30))

    # ---- footer: logo + link in bio ----
    fy = 1218
    lw = 250; lh = int(LOGO.height * lw / LOGO.width)
    im.alpha_composite(LOGO.resize((lw, lh), Image.LANCZOS), (96, fy + 6 + (84 - lh) // 2))
    # CTA: band-colour pill, "Link in bio" light + "sewcraftly.com" bold, centred on the logo row
    f1, f2 = POP('Medium', 24), POP('Bold', 26)
    t1, sep, t2 = 'Link in bio', '  ·  ', 'sewcraftly.com'
    w1, ws, w2 = d.textlength(t1, font=f1), d.textlength(sep, font=f1), d.textlength(t2, font=f2)
    ph_ = 62; px1 = W - 96; px0 = px1 - (w1 + ws + w2 + 64); py0 = fy + 6 + (84 - ph_) // 2
    d.rounded_rectangle((px0, py0, px1, py0 + ph_), radius=ph_ // 2, fill=BAND)
    x = px0 + 32; ty = py0 + (ph_ - f2.size * 1.42) / 2
    d.text((x, ty + 1), t1, font=f1, fill=(55, 55, 55)); x += w1
    d.text((x, ty + 1), sep, font=f1, fill=(55, 55, 55)); x += ws
    d.text((x, ty), t2, font=f2, fill=K)

    return im


def logo_at(im, xy, lw):
    lh = int(LOGO.height * lw / LOGO.width); im.alpha_composite(LOGO.resize((lw, lh), Image.LANCZOS), xy); return lh

def style_photo():
    # full-bleed model photo, sketch card bottom-right, title panel on band colour
    im = Image.new('RGBA', (W, H)); ph = cover_crop(Image.open(A.photo).convert('RGB'), W, H, 0.25).convert('RGBA'); im.alpha_composite(ph)
    d = ImageDraw.Draw(im)
    px0, py0 = 56, 900
    panel = noise_bg(BAND, (W - 2 * px0, H - py0 - 56), 0.06).convert('RGBA')
    shadowed(im, panel, (px0, py0), off=(0, 8), blur=18, alpha=70)
    d = ImageDraw.Draw(im)
    bf = POP('Bold', 26); t = 'FREE PDF PATTERN'; tw = d.textlength(t, font=bf)
    d.rounded_rectangle((96, py0 + 36, 96 + tw + 56, py0 + 96), radius=30, fill=K); d.text((124, py0 + 36 + (60 - bf.size * 1.42) / 2), t, font=bf, fill='white')
    lines = split_title(d, A.name, ROZHA, 560)
    tf = autosize(d, lines, ROZHA, 560, 84)
    y = py0 + 118
    for ln in lines: d.text((96, y), ln, font=tf, fill=K); y += int(tf.size * 1.0)
    d.text((96, H - 56 - 62), f"Sizes {A.sizes}  ·  {A.code}", font=POP('Medium', 26), fill=K)
    # sketch card
    cw, ch = 330, 470
    card = Image.new('RGBA', (cw, ch), (255, 255, 255, 255)); s = fit(sticker, cw - 40, ch - 40)
    card.alpha_composite(s, ((cw - s.width) // 2, (ch - s.height) // 2))
    shadowed(im, card, (W - 56 - 40 - cw, py0 - 200), off=(6, 10), blur=16, alpha=90)
    # logo chip top-left
    chip = Image.new('RGBA', (290, 96), (255, 255, 255, 235)); m = Image.new('L', chip.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, 289, 95), radius=48, fill=255); chip.putalpha(m)
    lw = 230; lh = int(LOGO.height * lw / LOGO.width); chip.alpha_composite(LOGO.resize((lw, lh), Image.LANCZOS), (30, (96 - lh) // 2))
    im.alpha_composite(chip, (72, 64))
    return im

def style_sketch():
    # clean flat-lay: big sketch on a band-colour arch, feature row, title on top
    im = noise_bg(CREAM).convert('RGBA'); d = ImageDraw.Draw(im)
    lh = logo_at(im, (W // 2 - 150, 52), 300)
    ctext(d, 52 + lh + 18, 'FREE SEWING PATTERN', POP('SemiBold', 26), spacing=6)
    lines = split_title(d, A.name, ROZHA, 900) if len(A.name) > 18 else [A.name]
    tf = autosize(d, lines, ROZHA, 900, 96 if len(lines) == 2 else 104)
    y = 52 + lh + 62
    for ln in lines: ctext(d, y, ln, tf); y += int(tf.size * 1.0)
    ax0, ax1, ay0, ay1 = 150, W - 150, y + 30, 1150
    arch = Image.new('L', (W, H), 0); ad = ImageDraw.Draw(arch)
    r = (ax1 - ax0) // 2; ad.pieslice((ax0, ay0, ax1, ay0 + 2 * r), 180, 360, fill=255); ad.rectangle((ax0, ay0 + r, ax1, ay1), fill=255)
    im = Image.composite(noise_bg(BAND, (W, H), 0.06).convert('RGBA'), im, arch); d = ImageDraw.Draw(im)
    s = fit(sticker, ax1 - ax0 + 120, ay1 - ay0 - 40); shadowed(im, s, (W // 2 - s.width // 2, ay1 - s.height - 10))
    # badge
    bf = POP('Bold', 28); t = 'FREE PDF'; tw = d.textlength(t, font=bf)
    d.rounded_rectangle((ax1 - tw - 20, ay0 + 40, ax1 + 60, ay0 + 106), radius=33, fill=K); d.text((ax1 - tw + 20, ay0 + 40 + (66 - bf.size * 1.42) / 2), t, font=bf, fill='white')
    # feature row
    items = [('SIZES', A.sizes), ('FORMATS', 'A4 · Letter · A0')] + ([('LEVEL', A.level)] if A.level else [])
    cw = (W - 112) // len(items); fy = 1185
    for i, (k, v) in enumerate(items):
        cx = 56 + cw * i + cw // 2
        ctext(d, fy, k, POP('SemiBold', 20), cx=cx, spacing=4, fill=(90, 90, 90))
        ctext(d, fy + 32, v, POP('SemiBold', 30), cx=cx)
        if i: d.line((56 + cw * i, fy + 6, 56 + cw * i, fy + 70), fill=(200, 195, 188), width=2)
    ctext(d, H - 62, f"{A.code}  ·  link in bio  ·  sewcraftly.com", POP('Medium', 24), spacing=2, fill=(70, 70, 70))
    return im

im = {'split': style_split, 'photo': style_photo, 'sketch': style_sketch}[A.style]()

os.makedirs(os.path.dirname(os.path.abspath(A.out)), exist_ok=True)
im.convert('RGB').save(A.out, quality=92)
print('band', BAND, '->', A.out)
