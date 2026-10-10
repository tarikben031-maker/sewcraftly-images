"""Replace the 'sewcraftly.com' wordmark baked into existing covers with the new domain.

Handles both house cover styles:
  * 1200x800 band covers (SC1005-SC1009, SC1011): letter-spaced text under a short line,
    on the diagonal striped band. The old text is covered with a patch of the same band
    taken 100 px higher and shifted along the stripe slope, so the stripes stay continuous.
  * 1650x1100 photo covers (SC1010+): black bottom bar with logo + site name; the bar is
    redrawn exactly as gen_cover.py does.

usage: python3 tools/covers/rebrand_domain.py IN.jpg OUT.jpg [--domain sewcraftlypatterns.com]
"""
import argparse, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
FD = '/usr/share/fonts/truetype/google-fonts/'

ap = argparse.ArgumentParser()
ap.add_argument('inp'); ap.add_argument('out')
ap.add_argument('--domain', default='sewcraftlypatterns.com')
a = ap.parse_args()

img = Image.open(a.inp).convert('RGB')
W, H = img.size
K = (20, 20, 20)

def spaced(d, cx, y, t, font, sp, fill):
    tw = sum(d.textlength(ch, font=font) + sp for ch in t) - sp
    x = cx - tw / 2
    for ch in t:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + sp
    return cx - tw / 2, cx + tw / 2

if (W, H) == (1200, 800):
    arr = np.array(img)
    # band left edge: polygon (430,0)->(700,800); stripes slope x = x0 - 0.375*y
    y0, y1, dy = 700, 762, 100
    dx = round(dy * 0.375)
    out = arr.copy()
    for y in range(y0, y1):
        edge = int(430 + 270 * y / 800) + 6
        sy = y - dy
        xs = np.arange(edge, W)
        sx = np.clip(xs + dx, 0, W - 1)
        out[y, edge:W] = arr[sy, sx]
    # feather the top/bottom seams a little
    for k, y in enumerate(range(y0 - 3, y0)):
        t = (k + 1) / 4
        out[y] = (arr[y] * (1 - t) + out[y] * t).astype(np.uint8)
    img = Image.fromarray(out)
    d = ImageDraw.Draw(img)
    d.line((880 - 50, 690, 880 + 50, 690), fill=K, width=5)
    sf = ImageFont.truetype(FD + 'Poppins-Medium.ttf', 26)
    l, r = spaced(d, 880, 711, a.domain, sf, 3, K)
    assert l > 430 + 270 * 740 / 800 + 6, ('text runs off the band', l)
elif (W, H) == (1650, 1100):
    INK, PW, BY = (30, 27, 25), 620, H - 110
    d = ImageDraw.Draw(img)
    d.rectangle((PW + 10, BY, W, H), fill=INK)
    r = 36
    lg = Image.open(os.path.join(REPO, 'brand', 'sewcraftly-icon.png')).convert('RGBA').resize((2 * r, 2 * r), Image.LANCZOS)
    m = Image.new('L', (2 * r, 2 * r), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, 2 * r - 1, 2 * r - 1), 16, fill=255)
    lg.putalpha(Image.fromarray(np.minimum(np.array(lg.getchannel('A')), np.array(m))))
    sf = ImageFont.truetype(FD + 'Poppins-Medium.ttf', 40)
    grp = 2 * r + 22 + d.textlength(a.domain, font=sf)
    gx = round((PW + 10 + W) / 2 - grp / 2)
    img.paste(lg, (gx, BY + 55 - r), lg)
    d.text((gx + 2 * r + 22, BY + 55), a.domain, font=sf, fill='white', anchor='lm')
else:
    raise SystemExit(f'unknown cover size {W}x{H}')

img.save(a.out, quality=92)
print(a.out)
