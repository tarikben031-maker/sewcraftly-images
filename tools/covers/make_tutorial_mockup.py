"""SewCraftly - fixed "Sewing tutorial" mockup image (v2)."""
import argparse, base64, subprocess, tempfile, pathlib, html
from playwright.sync_api import sync_playwright

W, H = 1400, 1400  # CSS px; rendered at 2x -> 2800 x 2800 PNG

TEMPLATE = r"""<!doctype html><html><head><meta charset="utf-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:%(W)dpx;height:%(H)dpx;overflow:hidden}
body{font-family:'Poppins',sans-serif;position:relative;
  background:radial-gradient(circle at 85%% 45%%,#e7c3cf 0,#efd9df 32%%,transparent 60%%),
             radial-gradient(circle at 10%% 90%%,#f2d9c8 0,transparent 45%%),#f7efec}
.stitch{position:absolute;left:-60px;top:330px;width:1600px;height:900px;border-top:4px dashed rgba(200,85,61,.35);
  border-radius:50%%;transform:rotate(-8deg)}
.head{position:absolute;left:80px;top:62px;right:80px}
.tag{display:inline-block;background:#c8553d;color:#fff;font-weight:700;font-size:22px;letter-spacing:4px;
  padding:9px 20px;border-radius:40px}
.kicker{margin-top:18px;font-weight:800;font-style:italic;font-size:122px;line-height:.95;color:#1f2433;letter-spacing:-3px}
.kicker em{color:#c8553d;font-style:italic}
.sub{margin-top:18px;font-weight:600;font-size:23px;letter-spacing:6px;color:#3a3d52;text-transform:uppercase}
.badge{position:absolute;right:0;top:0;width:220px;height:220px;border-radius:50%%;
  background:#2a2c45;border:7px solid #fff;box-shadow:0 12px 30px rgba(40,20,40,.28);transform:rotate(8deg);
  color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}
.badge b{font-size:21px;letter-spacing:2px;font-weight:700}
.badge strong{font-size:76px;line-height:.95;font-weight:800}
.badge i{font-size:17px;font-weight:400;margin-top:4px;white-space:nowrap}
.pg{position:absolute;width:470px;aspect-ratio:1/1.414;background:#fff;
  box-shadow:0 20px 45px rgba(50,25,40,.28),0 2px 6px rgba(0,0,0,.12);border-radius:4px;overflow:hidden}
.pg img{width:100%%;height:100%%;display:block}
.pA{left:760px;top:470px;transform:rotate(8deg);z-index:1}
.pB{left:600px;top:500px;transform:rotate(-2deg);z-index:2}
.photo{position:absolute;left:80px;top:430px;width:560px;height:620px;z-index:3;background:#fff;padding:16px;
  border-radius:10px;transform:rotate(-4deg);box-shadow:0 24px 50px rgba(50,25,40,.32)}
.photo img{width:100%%;height:100%%;object-fit:cover;object-position:50%% 30%%;border-radius:4px;display:block}
.chips{position:absolute;left:80px;right:80px;top:1010px;z-index:6;display:flex;gap:14px;justify-content:flex-end}
.chip{background:#fff;color:#1f2433;font-weight:700;font-size:25px;padding:14px 26px;border-radius:50px;
  box-shadow:0 8px 22px rgba(40,20,40,.22);display:flex;align-items:center;gap:12px;white-space:nowrap}
.chip .dot{width:14px;height:14px;border-radius:50%%;background:#c8553d}
.chip.hl{background:#c8553d;color:#fff}.chip.hl .dot{background:#fff}
.band{position:absolute;left:0;right:0;bottom:0;height:290px;z-index:5;background:#2a2c45;
  display:flex;flex-direction:column;justify-content:center;padding:40px 80px 0}
.band::before{content:"";position:absolute;left:0;right:0;top:0;height:8px;background:#c8553d}
.name{font-weight:800;color:#fff;font-size:92px;line-height:1.05;letter-spacing:-1px}
.meta{margin-top:14px;color:#f0d6dd;font-size:30px;font-weight:600;letter-spacing:1px}
.meta span{color:#fff}
</style></head><body>
<div class="stitch"></div>
<div class="head">
  <div class="tag">STEP-BY-STEP GUIDE</div>
  <div class="kicker">Sewing <em>tutorial</em></div>
  <div class="sub">Illustrated instructions · video guides</div>
  <div class="badge"><b>PRINTABLE</b><strong>PDF</strong><i>instant download</i></div>
</div>
<div class="pg pA"><img src="%(PA)s"></div>
<div class="pg pB"><img src="%(PB)s"></div>
<div class="photo"><img src="%(PHOTO)s"></div>
<div class="chips">
  <div class="chip hl"><span class="dot"></span>A4 · US Letter · A0</div>
  <div class="chip"><span class="dot"></span>%(SIZES)s</div>
</div>
<div class="band">
  <div class="name" id="name">%(NAME)s</div>
  <div class="meta"><span>#%(CODE)s</span>  ·  SewCraftly</div>
</div>
<script>
const n=document.getElementById('name');let s=84;n.style.fontSize=s+'px';const maxW=n.parentElement.clientWidth-160;
while(s>44&&(n.scrollWidth>maxW||n.getBoundingClientRect().height>s*1.05*2+2)){s-=2;n.style.fontSize=s+'px';}
</script>
</body></html>"""


def b64(path):
    ext = pathlib.Path(path).suffix.lower().lstrip(".").replace("jpg", "jpeg")
    return f"data:image/{ext};base64," + base64.b64encode(pathlib.Path(path).read_bytes()).decode()


def page_png(pdf, num, tmp):
    out = pathlib.Path(tmp) / f"p{num}"
    subprocess.run(["pdftoppm", "-r", "150", "-png", "-singlefile", "-f", str(num), "-l", str(num), pdf, str(out)], check=True)
    return b64(out.with_suffix(".png"))


def cover_photo(pdf, tmp):
    """Largest image embedded on page 1 = the model photo."""
    subprocess.run(["pdfimages", "-f", "1", "-l", "1", "-png", pdf, f"{tmp}/c"], check=True)
    imgs = sorted(pathlib.Path(tmp).glob("c-*.png"), key=lambda p: p.stat().st_size)
    if not imgs:
        raise SystemExit("No photo on the cover: pass --photo")
    return b64(imgs[-1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf"); ap.add_argument("name"); ap.add_argument("code"); ap.add_argument("out")
    ap.add_argument("--sizes", default="Sizes US 00–22 · XXS–4XL")
    ap.add_argument("--pages", default="9,13", help="front,back page numbers")
    ap.add_argument("--photo", help="model photo (default: taken from the booklet cover)")
    a = ap.parse_args()
    front, back = [int(x) for x in a.pages.split(",")]
    with tempfile.TemporaryDirectory() as tmp:
        doc = TEMPLATE % dict(W=W, H=H, PA=page_png(a.pdf, back, tmp), PB=page_png(a.pdf, front, tmp),
                              PHOTO=b64(a.photo) if a.photo else cover_photo(a.pdf, tmp),
                              SIZES=html.escape(a.sizes), NAME=html.escape(a.name),
                              CODE=html.escape(a.code.lstrip("#")))
        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=2)
            pg.set_content(doc); pg.wait_for_timeout(300)
            pg.screenshot(path=a.out)
            b.close()
    print("saved", a.out)


if __name__ == "__main__":
    main()
