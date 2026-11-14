"""Film the A4->A0 tool: frames as JPEG, scenes encoded separately, joined with concat."""
import asyncio, os, sys, subprocess, time, json, shutil
from playwright.async_api import async_playwright
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
LANG = sys.argv[1] if len(sys.argv) > 1 else 'en'
ONLY_PREVIEW = '--preview' in sys.argv
CAP = {
 'en': ["1. Drop your A4 or US Letter PDF pattern", "2. The tool finds the cut lines and the page order",
        "Pages in the wrong place? The lines don’t join (here pages 33 and 34)", "3. Click the page to add an empty square before it",
        "Click again until the lines join up ✓", "4. Download your A0 PDF and print it at 100%"],
 'fr': ["1. Déposez votre patron PDF A4 ou US Letter", "2. L’outil trouve les lignes de coupe et l’ordre des pages",
        "Pages mal placées ? Les lignes ne se rejoignent pas (ici les pages 33 et 34)", "3. Cliquez sur la page pour ajouter une case vide avant elle",
        "Cliquez encore jusqu’à ce que les lignes se rejoignent ✓", "4. Téléchargez le PDF A0 et imprimez à 100 %"],
 'de': ["1. A4- oder US-Letter-Schnittmuster ablegen", "2. Das Tool findet Schnittlinien und Seitenreihenfolge",
        "Seiten am falschen Platz? Die Linien passen nicht (hier Seite 33 und 34)", "3. Auf die Seite klicken, um davor ein leeres Feld einzufügen",
        "Noch einmal klicken, bis die Linien passen ✓", "4. A0-PDF herunterladen und mit 100 % drucken"],
 'nl': ["1. Sleep je A4- of US Letter-PDF-patroon erin", "2. De tool vindt de kniplijnen en de paginavolgorde",
        "Pagina’s op de verkeerde plek? De lijnen sluiten niet aan (hier pagina 33 en 34)", "3. Klik op de pagina om er een leeg vak voor te zetten",
        "Klik nog eens tot de lijnen aansluiten ✓", "4. Download de A0-PDF en print op 100%"]}[LANG]
W, H, DPR = 1280, 720, 1.5
OUT = os.path.join(HERE, 'out_' + LANG); FR = os.path.join(OUT, 'frames')
shutil.rmtree(OUT, ignore_errors=True); os.makedirs(FR)
ENC = ['-c:v', 'libx264', '-crf', '20', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-r', '30']
scenes = []

OVERLAY = r"""
(()=>{const s=document.createElement('style');s.textContent=`
body{margin:0!important;background:#F6F1F2!important;max-width:none!important}
#vwrap{max-width:1240px;margin:0 auto;padding:8px 20px 90px}
.sca0{margin:0!important}
.sca0 .a-pvw{max-height:470px!important}
.sca0 .a-pvw canvas{width:100%!important;max-height:none!important}
#vcap{position:fixed;left:50%;bottom:22px;transform:translateX(-50%);background:#14213D;color:#fff;font:600 21px/1.3 system-ui,-apple-system,Segoe UI,sans-serif;padding:13px 24px;border-radius:999px;box-shadow:0 14px 34px -12px rgba(20,33,61,.6);white-space:nowrap;z-index:99;display:flex;gap:12px;align-items:center}
#vcap:before{content:"";width:11px;height:11px;border-radius:50%;background:#E8A0B0;flex:none}
#a0-badge{display:none!important}
#vbrand{display:none;position:fixed;right:18px;top:12px;font:600 13px system-ui;color:#7A2340;opacity:.85;z-index:99}
#vcur{position:fixed;left:0;top:0;width:28px;height:28px;z-index:100;pointer-events:none;display:none}
#vring{position:fixed;width:46px;height:46px;margin:-23px 0 0 -23px;border-radius:50%;border:3px solid #7A2340;z-index:99;pointer-events:none;display:none}
#vhl{position:fixed;border:3px solid #E0002B;border-radius:12px;z-index:98;pointer-events:none;display:none;box-shadow:0 0 0 9999px rgba(20,33,61,.18)}
`;document.head.appendChild(s);
const w=document.createElement('div');w.id='vwrap';const t=document.getElementById('sca0');t.parentNode.insertBefore(w,t);w.appendChild(t);
document.body.insertAdjacentHTML('beforeend','<div id="vcap"></div><div id="vbrand">sewcraftlypatterns.com</div><div id="vring"></div><div id="vhl"></div><svg id="vcur" viewBox="0 0 28 28"><path d="M5 3l16 11-7 1.5 4 8-3 1.5-4-8L6 22z" fill="#fff" stroke="#14213D" stroke-width="1.6" stroke-linejoin="round"/></svg>');})()
"""

async def shot(pg, name):
    p = os.path.join(FR, name)
    await pg.screenshot(path=p, type='jpeg', quality=92)
    return p

def enc_still(img, dur, name):
    tmp = os.path.join(OUT, name + '.tmp.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', '30', '-i', img, '-vf', 'format=yuv420p,loop=-1:1,trim=duration=%.2f' % dur] + ENC + [tmp], check=True)
    os.rename(tmp, os.path.join(OUT, name + '.mp4')); scenes.append(name + '.mp4')

def enc_seq(pattern, name):
    tmp = os.path.join(OUT, name + '.tmp.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', '30', '-i', pattern] + ENC + [tmp], check=True)
    os.rename(tmp, os.path.join(OUT, name + '.mp4')); scenes.append(name + '.mp4')

async def main():
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8766'], cwd=os.path.join(ROOT, 'test', 'www'), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
    try:
        async with async_playwright() as p:
            br = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
            pg = await br.new_page(viewport={'width': W, 'height': H}, device_scale_factor=DPR)
            await pg.goto('http://localhost:8766/index_%s.html' % LANG)
            await pg.evaluate(OVERLAY)
            async def cap(t):
                await pg.evaluate('t=>{document.getElementById("vcap").textContent=t}', t)
            async def cursor(x, y, show=True):
                await pg.evaluate('([x,y,s])=>{const c=document.getElementById("vcur");c.style.display=s?"block":"none";c.style.left=(x-5)+"px";c.style.top=(y-3)+"px"}', [x, y, show])
            async def ring(x, y, r, a):
                await pg.evaluate('([x,y,r,a])=>{const c=document.getElementById("vring");c.style.display=a>0?"block":"none";c.style.left=x+"px";c.style.top=y+"px";c.style.transform="scale("+r+")";c.style.opacity=a}', [x, y, r, a])
            async def hl(box):
                await pg.evaluate('b=>{const h=document.getElementById("vhl");if(!b){h.style.display="none";return}h.style.display="block";h.style.left=b[0]+"px";h.style.top=b[1]+"px";h.style.width=b[2]+"px";h.style.height=b[3]+"px"}', box)
            # scene 1: drop zone
            await cap(CAP[0]); d = await pg.locator('#a0-drop').bounding_box()
            await cursor(d['x'] + d['width'] / 2 + 10, d['y'] + d['height'] - 40)
            enc_still(await shot(pg, 's1.jpg'), 2.6, 's1')
            # load file
            await pg.set_input_files('#a0-file', os.path.join(ROOT, 'test', 'pdfs', 'pf.pdf'))
            await pg.wait_for_selector('#a0-main', state='visible', timeout=120000)
            await cursor(0, 0, False)
            # force the "wrong" layout: no empty squares
            await pg.evaluate('()=>{const S=__sca0();S.order=S.tiles.slice();document.getElementById("a0-cols").dispatchEvent(new Event("input"))}')
            await pg.evaluate('()=>{document.getElementById("vwrap").scrollIntoView();window.scrollTo(0,0)}')
            await cap(CAP[1])
            enc_still(await shot(pg, 's2.jpg'), 2.8, 's2')
            # scene 3: scroll preview to the bottom and highlight the last row
            await pg.evaluate('()=>{const w=document.getElementById("a0-pvw");w.scrollTop=w.scrollHeight}')
            await cap(CAP[2])
            async def cellbox(page_no):
                return await pg.evaluate('''(n)=>{const S=__sca0(),c=document.getElementById("a0-pv"),r=c.getBoundingClientRect();const cols=S.c,ord=S.order,i=ord.indexOf(n-1);const rows=Math.ceil(ord.length/cols);const cw=r.width/cols,ch=r.height/rows;return [r.left+(i%cols)*cw,r.top+Math.floor(i/cols)*ch,cw,ch]}''', page_no)
            b33 = await cellbox(33); b34 = await cellbox(34)
            await hl([b33[0] - 4, b33[1] - 4, b33[2] * 2 + 8, b33[3] + 8])
            enc_still(await shot(pg, 's3.jpg'), 3.6, 's3')
            await hl(None)
            # scene 4 + 5: animated clicks on page 33
            fi = [0]
            async def frame():
                fi[0] += 1; await shot(pg, 'a%04d.jpg' % fi[0])
            async def move(x0, y0, x1, y1, n):
                for k in range(n + 1):
                    t = k / n; e = t * t * (3 - 2 * t)
                    await cursor(x0 + (x1 - x0) * e, y0 + (y1 - y0) * e); await frame()
            async def click_at(x, y):
                for k in range(4):
                    await ring(x, y, .6 + .15 * k, 1); await frame()
                await pg.mouse.click(x, y)
                await pg.evaluate('()=>{const w=document.getElementById("a0-pvw");w.scrollTop=w.scrollHeight}')
                for k in range(7):
                    await ring(x, y, 1.2 + .12 * k, max(0, 1 - k / 6)); await frame()
                await ring(0, 0, 1, 0)
            async def hold(n):
                for k in range(n): await frame()
            await cap(CAP[3])
            cx, cy = b33[0] + b33[2] / 2, b33[1] + b33[3] / 2
            await move(cx + 260, cy - 200, cx, cy, 24); await hold(6)
            await click_at(cx, cy); await hold(18)
            b33 = await cellbox(33); cx2, cy2 = b33[0] + b33[2] / 2, b33[1] + b33[3] / 2
            await cap(CAP[4])
            await move(cx, cy, cx2, cy2, 16); await hold(4)
            await click_at(cx2, cy2); await hold(8)
            b33 = await cellbox(33)
            await hl([b33[0] - 4, b33[1] - b33[3] - 4, b33[2] * 2 + 8, b33[3] * 2 + 8]); await hold(45); await hl(None)
            await cursor(0, 0, False)
            enc_seq(os.path.join(FR, 'a%04d.jpg'), 's45')
            # scene 6: download button
            await pg.evaluate('()=>{document.getElementById("a0-dl").scrollIntoView({block:"center"})}')
            await cap(CAP[5]); bb = await pg.locator('#a0-dl').bounding_box()
            await hl([bb['x'] - 6, bb['y'] - 6, bb['width'] + 12, bb['height'] + 12])
            await cursor(bb['x'] + bb['width'] * .62, bb['y'] + bb['height'] * .62)
            enc_still(await shot(pg, 's6.jpg'), 3.0, 's6')
            await br.close()
    finally:
        srv.terminate()
    with open(os.path.join(OUT, 'list.txt'), 'w') as f:
        for s in scenes: f.write("file '%s'\n" % s)
    final = os.path.join(OUT, 'a4-to-a0-empty-squares-%s.mp4' % LANG)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', os.path.join(OUT, 'list.txt'), '-c', 'copy', '-movflags', '+faststart', final + '.tmp.mp4'], check=True)
    os.rename(final + '.tmp.mp4', final); print(final)
asyncio.run(main())
