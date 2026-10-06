import sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

# Pin 3 (photo + small sketch) generator, validated by the user on SC1006.
# usage: python3 gen3.py MODEL_PHOTO SKETCH_FRONT_BACK OUT.jpg [SIZES] [BAND_R,G,B] [FONTS_DIR]
# Sketch = white-background PNG with front on the left and back on the right (FRONT/BACK labels cropped out below y=1250).
photo_p, sketch_p, out = sys.argv[1], sys.argv[2], sys.argv[3]
SIZES = sys.argv[4] if len(sys.argv) > 4 else 'XXS – 4XL'
BAND = tuple(int(v) for v in sys.argv[5].split(',')) if len(sys.argv) > 5 else (163, 186, 160)
FONTS = sys.argv[6] if len(sys.argv) > 6 else 'gf/ofl/poppins/'
FD = FONTS
def F(n, s): return ImageFont.truetype(FD + n, s)

W, H = 1000, 1500
SAGE = BAND
K = (20, 20, 20)

# --- photo full-bleed, 2:3
ph = Image.open(photo_p).convert('RGB')
ph = ph.resize((W, int(ph.height * W / ph.width)), Image.LANCZOS)
if ph.height > H:
    ph = ph.crop((0, 0, W, H))
bg = ph.convert('RGBA')

# soft cream veil at top so the text reads on the bright wall
veil = Image.new('L', (W, H), 0)
vd = ImageDraw.Draw(veil)
for y in range(0, 560):
    vd.line((0, y, W, y), fill=int(150 * (1 - y / 560) ** 1.6))
pass  # veil removed

# --- sketch stickers (front + back), build mask from the white-background sketch
sk = Image.open(sketch_p).convert('L')
def make_sticker(box, target_h):
    crop = sk.crop(box)
    lines = ImageChops.invert(crop).point(lambda v: 255 if v > 40 else 0)
    closed = lines.filter(ImageFilter.MaxFilter(15))
    fl = closed.copy()
    ImageDraw.floodfill(fl, (0, 0), 128)
    sil = fl.point(lambda v: 0 if v == 128 else 255).filter(ImageFilter.MinFilter(9))
    dark = ImageChops.invert(crop)
    mask = ImageChops.lighter(sil, dark)
    rgb = Image.new('RGB', crop.size, (255, 255, 255))
    ink = Image.new('RGB', crop.size, (45, 55, 55))
    rgb = Image.composite(ink, rgb, dark.point(lambda v: min(255, v * 2)))
    img = rgb.convert('RGBA'); img.putalpha(sil)
    sc = target_h / crop.height
    img = img.resize((int(crop.width * sc), target_h), Image.LANCZOS)
    pad = 36
    c = Image.new('RGBA', (img.width + 2 * pad, img.height + 2 * pad), (0, 0, 0, 0))
    c.paste(img, (pad, pad), img)
    a = c.split()[3]
    outline = a.filter(ImageFilter.MaxFilter(11))
    shadow = outline.filter(ImageFilter.GaussianBlur(10))
    o = Image.new('RGBA', c.size, (0, 0, 0, 0))
    o.paste((90, 80, 70, 120), (5, 7), shadow)
    o.paste((255, 255, 255, 255), (0, 0), outline)
    o.alpha_composite(c)
    return o

front = make_sticker((0, 60, 560, 1250), 290)
back = make_sticker((700, 60, 1290, 1250), 290)
bg.alpha_composite(front, (672, 385))
bg.alpha_composite(back, (800, 440))

d = ImageDraw.Draw(bg)
cx = 835
def ctext(y, t, font, fill=K):
    w = d.textlength(t, font=font)
    d.text((cx - w / 2, y), t, font=font, fill=fill)

# --- top text
pill_f = F('Poppins-SemiBold.ttf', 34)
t = 'FREE PDF'
tw = d.textlength(t, font=pill_f)
d.rounded_rectangle((cx - tw / 2 - 28, 40, cx + tw / 2 + 28, 102), radius=26, fill=K)
d.text((cx - tw / 2, 47), t, font=pill_f, fill='white')
ctext(112, 'Sewing', F('Poppins-Bold.ttf', 60))
ctext(180, 'Pattern', F('Poppins-Bold.ttf', 60))
ctext(262, SIZES, F('Poppins-Italic.ttf', 40))
ctext(318, '+ Instructions', F('Poppins-SemiBold.ttf', 24))

# --- bottom brand bar
bar = Image.new('RGBA', (W, 110), K + (255,))
bg.alpha_composite(bar, (0, H - 110))
d = ImageDraw.Draw(bg)
sf = F('Poppins-Medium.ttf', 40)
t = 'sewcraftly.com'; sp = 6
tw = sum(d.textlength(ch, font=sf) + sp for ch in t) - sp
x = W / 2 - tw / 2
for ch in t:
    d.text((x, H - 82), ch, font=sf, fill='white'); x += d.textlength(ch, font=sf) + sp

bg.convert('RGB').save(out, quality=92)
print('saved', out)
