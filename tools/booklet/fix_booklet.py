import sys, pymupdf as fitz
FONT = '/usr/share/fonts/truetype/google-fonts/Poppins-Regular.ttf'
FONT_B = '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'
GF = '/usr/share/fonts/truetype/google-fonts/'
# keep the booklet's own font for brand lines (footer is Lora Italic)
FAMILIES = {'Lora-Italic': GF + 'Lora-Italic-Variable.ttf', 'Lora': GF + 'Lora-Variable.ttf', 'Poppins-Bold': FONT_B, 'Poppins': FONT}

def pick(fontname):
    for k, v in FAMILIES.items():
        if fontname.startswith(k) or k in fontname:
            return k.lower().replace('-', ''), v
    return 'popr', FONT
SITE = 'sewcraftlypatterns.com'
NEW = 'If a step is unclear, email us at contact@sewcraftlypatterns.com – we are happy to help.'
LANG = 'Need it in another language? Email us your order number, we send it within 48 h.'

def rgb(c):
    return ((c >> 16 & 255) / 255, (c >> 8 & 255) / 255, (c & 255) / 255)

def rebrand(t):
    for a, b in (('BenchGoods', 'SewCraftly'), ('BENCHGOODS', 'SEWCRAFTLY'), ('Benchgoods', 'SewCraftly'), ('benchgoods', 'sewcraftly')):
        t = t.replace(a, b)
    return t

def fix(src, dst, outdir='.'):
    d = fitz.open(src); hits = brand = 0; pages = set()
    for p in d:
        spans = [s for b in p.get_text('dict')['blocks'] for l in b.get('lines', []) for s in l['spans']
                 if 'benchgoods' in s['text'].lower()]
        if not spans:
            continue
        jobs = []
        for s in spans:
            r = fitz.Rect(s['bbox'])
            bg = p.get_pixmap(dpi=72, clip=fitz.Rect(r.x1 + 2, r.y0 + 2, r.x1 + 6, r.y1 - 2)).pixel(1, 1)
            p.add_redact_annot(fitz.Rect(r.x0 - 1, r.y0, r.x1 + 1, r.y1), fill=tuple(v / 255 for v in bg))
            jobs.append((s, r))
        p.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=fitz.PDF_REDACT_LINE_ART_NONE)
        p.insert_font(fontname='popr', fontfile=FONT)
        pw = p.rect.width
        for s, r in jobs:
            col = rgb(s['color']); o = s['origin']; size = s['size']
            print(f"  p{p.number+1}: {s['text']!r} size={size:.1f} font={s['font']} bbox={tuple(round(v) for v in r)}")
            if 'Etsy' in s['text']:
                p.insert_text(o, NEW, fontname='popr', fontsize=size, color=col)
                p.insert_text((o[0], o[1] + size * 1.45), LANG, fontname='popr', fontsize=size, color=col)
                hits += 1
            else:
                f, ff = pick(s['font'])
                p.insert_font(fontname=f, fontfile=ff)
                t = rebrand(s['text'])
                if SITE not in t and len(t.strip()) <= 30:
                    t = t.rstrip() + ' · ' + SITE
                x = o[0]
                if abs((r.x0 + r.x1) / 2 - pw / 2) < 6:
                    x = (pw - fitz.Font(fontfile=ff).text_length(t, fontsize=size)) / 2
                p.insert_text((x, o[1]), t, fontname=f, fontsize=size, color=col)
                brand += 1
            pages.add(p.number)
    m = d.metadata or {}
    d.set_metadata({k: rebrand(m.get(k) or '') for k in ('title', 'author', 'subject', 'keywords', 'creator', 'producer')})
    for n in sorted(pages):
        d[n].get_pixmap(dpi=80).save(f'{outdir}/check-p{n + 1}.png')
    d.save(dst, garbage=3, deflate=True)
    print(src, 'help line', hits, '| brand', brand, '| pages', [n + 1 for n in sorted(pages)])

if __name__ == '__main__':
    fix(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else '.')
