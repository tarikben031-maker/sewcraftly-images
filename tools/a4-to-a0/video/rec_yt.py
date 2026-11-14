"""YouTube version (EN, 1080p): intro card, tool demo synced to the voice-over, result card, outro."""
import asyncio, os, sys, subprocess, time, shutil
from playwright.async_api import async_playwright
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, 'out_yt'); FR = os.path.join(OUT, 'frames')
shutil.rmtree(OUT, ignore_errors=True); os.makedirs(FR)
ENC = ['-c:v', 'libx264', '-crf', '19', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-r', '30']
FPS = 30
# timeline (s), synced to the voice-over word timings
T = dict(intro=(0, 14.0), drop=(14.0, 23.2), detect=(23.2, 28.6), wrong=(28.6, 33.6), click=(33.6, 41.6), dl=(41.6, 46.0), result=(46.0, 55.8), outro=(55.8, 63.6))
scenes = []
OVERLAY = open(os.path.join(HERE, 'rec.py')).read().split('OVERLAY = r"""')[1].split('"""')[0]

def enc_still(img, dur, name):
    tmp = os.path.join(OUT, name + '.tmp.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', '30', '-i', img, '-vf', 'scale=1920:1080,format=yuv420p,loop=-1:1,trim=duration=%.3f' % dur] + ENC + [tmp], check=True)
    os.rename(tmp, os.path.join(OUT, name + '.mp4')); scenes.append(name + '.mp4')

def enc_seq(prefix, name):
    tmp = os.path.join(OUT, name + '.tmp.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', '30', '-i', os.path.join(FR, prefix + '%05d.jpg'), '-vf', 'scale=1920:1080'] + ENC + [tmp], check=True)
    os.rename(tmp, os.path.join(OUT, name + '.mp4')); scenes.append(name + '.mp4')

def nframes(key): a, b = T[key]; return round((b - a) * FPS)

async def main():
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8767'], cwd=os.path.join(ROOT, 'test', 'www'), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
    try:
        async with async_playwright() as p:
            br = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox', '--allow-file-access-from-files'])
            # ---------- intro (animated) ----------
            cp = await br.new_page(viewport={'width': 1280, 'height': 720}, device_scale_factor=1.5)
            await cp.goto('file://' + os.path.join(HERE, 'cards.html')); await cp.evaluate("show('intro')"); await cp.wait_for_timeout(300)
            n = nframes('intro')
            for k in range(n):
                t = k / FPS
                if k == 0 or t < 6.0 or k == round(6.0 * FPS):
                    await cp.evaluate('t=>setT(t)', t)
                    await cp.screenshot(path=os.path.join(FR, 'i%05d.jpg' % (k + 1)), type='jpeg', quality=92)
                else:
                    shutil.copy(os.path.join(FR, 'i%05d.jpg' % k), os.path.join(FR, 'i%05d.jpg' % (k + 1)))
            enc_seq('i', 'v01_intro')
            # ---------- tool ----------
            pg = await br.new_page(viewport={'width': 1280, 'height': 720}, device_scale_factor=1.5)
            await pg.goto('http://localhost:8767/index_en.html')
            await pg.evaluate(OVERLAY)
            async def cap(t): await pg.evaluate('t=>{const c=document.getElementById("vcap");c.style.display=t?"flex":"none";c.textContent=t}', t)
            async def cursor(x, y, show=True): await pg.evaluate('([x,y,s])=>{const c=document.getElementById("vcur");c.style.display=s?"block":"none";c.style.left=(x-5)+"px";c.style.top=(y-3)+"px"}', [x, y, show])
            async def ring(x, y, r, a): await pg.evaluate('([x,y,r,a])=>{const c=document.getElementById("vring");c.style.display=a>0?"block":"none";c.style.left=x+"px";c.style.top=y+"px";c.style.transform="scale("+r+")";c.style.opacity=a}', [x, y, r, a])
            async def hl(box): await pg.evaluate('b=>{const h=document.getElementById("vhl");if(!b){h.style.display="none";return}h.style.display="block";h.style.left=b[0]+"px";h.style.top=b[1]+"px";h.style.width=b[2]+"px";h.style.height=b[3]+"px"}', box)
            await pg.evaluate('()=>{document.body.insertAdjacentHTML("beforeend",`<div id="vpdf" style="position:fixed;z-index:101;display:none;width:70px;height:92px;background:#fff;border:2px solid #7A2340;border-radius:6px;box-shadow:0 12px 24px -8px rgba(20,33,61,.5);font:800 18px system-ui;color:#7A2340;text-align:center;line-height:92px">PDF</div>`)}')
            async def pdf(x, y, show=True): await pg.evaluate('([x,y,s])=>{const c=document.getElementById("vpdf");c.style.display=s?"block":"none";c.style.left=(x-35)+"px";c.style.top=(y-46)+"px"}', [x, y, show])
            seq = {'p': 'd', 'k': 0}
            async def frame():
                seq['k'] += 1; await pg.screenshot(path=os.path.join(FR, '%s%05d.jpg' % (seq['p'], seq['k'])), type='jpeg', quality=92)
            def dup():
                seq['k'] += 1; shutil.copy(os.path.join(FR, '%s%05d.jpg' % (seq['p'], seq['k'] - 1)), os.path.join(FR, '%s%05d.jpg' % (seq['p'], seq['k'])))
            async def hold_until(sec_in_scene):
                while seq['k'] < round(sec_in_scene * FPS): dup()
            async def move(x0, y0, x1, y1, n, carry=False):
                for k in range(n + 1):
                    t = k / n; e = t * t * (3 - 2 * t); x = x0 + (x1 - x0) * e; y = y0 + (y1 - y0) * e
                    await cursor(x, y)
                    if carry: await pdf(x - 20, y - 30)
                    await frame()
            async def click_at(x, y, after=None):
                for k in range(4): await ring(x, y, .6 + .15 * k, 1); await frame()
                if after: await after()
                for k in range(7): await ring(x, y, 1.2 + .12 * k, max(0, 1 - k / 6)); await frame()
                await ring(0, 0, 1, 0)
            # ---- drop: 14.0-23.2 ----
            seq.update(p='d', k=0); await cap('Drop your A4 or US Letter PDF')
            await pg.evaluate('()=>{const s=document.createElement("style");s.id="vdrop";s.textContent="#vwrap{zoom:1.25;padding-top:120px!important}";document.head.appendChild(s)}')
            d = await pg.locator('#a0-drop').bounding_box(); dx, dy = d['x'] + d['width'] / 2, d['y'] + d['height'] / 2
            await cursor(1180, 640); await pdf(1160, 610); await frame(); await hold_until(0.6)
            await move(1180, 640, dx, dy, 60, carry=True)
            await pg.evaluate('()=>document.getElementById("a0-drop").classList.add("on")'); await frame(); await hold_until(3.6)
            await pdf(0, 0, False); await cursor(0, 0, False)
            await pg.evaluate('()=>document.getElementById("a0-drop").classList.remove("on")')
            # real load happens off-camera; show progress-looking still with the second caption
            await cap('Nothing is uploaded: it runs in your browser')
            await pg.evaluate('()=>{document.getElementById("a0-prog").style.display="block";document.getElementById("a0-bar").style.width="64%";document.getElementById("a0-msg").textContent="Reading page 22 of 34…"}')
            await frame(); await hold_until(T['drop'][1] - T['drop'][0])
            enc_seq('d', 'v02_drop')
            await pg.evaluate('()=>document.getElementById("vdrop").remove()')
            await pg.set_input_files('#a0-file', os.path.join(ROOT, 'test', 'pdfs', 'pf.pdf'))
            await pg.wait_for_selector('#a0-main', state='visible', timeout=120000)
            await pg.evaluate('()=>{const S=__sca0();S.order=S.tiles.slice();document.getElementById("a0-cols").dispatchEvent(new Event("input"));window.scrollTo(0,0)}')
            # ---- detect ----
            await cap('The tool finds the cut lines and the page order')
            await pg.screenshot(path=os.path.join(FR, 'detect.jpg'), type='jpeg', quality=92); enc_still(os.path.join(FR, 'detect.jpg'), T['detect'][1] - T['detect'][0], 'v03_detect')
            # ---- wrong ----
            await pg.evaluate('()=>{const w=document.getElementById("a0-pvw");w.scrollTop=w.scrollHeight}')
            async def cellbox(n):
                return await pg.evaluate('''(n)=>{const S=__sca0(),c=document.getElementById("a0-pv"),r=c.getBoundingClientRect();const cols=S.c,ord=S.order,i=ord.indexOf(n-1);const rows=Math.ceil(ord.length/cols);const cw=r.width/cols,ch=r.height/rows;return [r.left+(i%cols)*cw,r.top+Math.floor(i/cols)*ch,cw,ch]}''', n)
            b = await cellbox(33); await hl([b[0] - 4, b[1] - 4, b[2] * 2 + 8, b[3] + 8]); await cap('Pages in the wrong place? The lines don’t join')
            await pg.screenshot(path=os.path.join(FR, 'wrong.jpg'), type='jpeg', quality=92)
            enc_still(os.path.join(FR, 'wrong.jpg'), T['wrong'][1] - T['wrong'][0], 'v04_wrong'); await hl(None)
            # ---- clicks: 33.6-41.6 ----
            seq.update(p='c', k=0); await cap('Click the page to add an empty square before it')
            cx, cy = b[0] + b[2] / 2, b[1] + b[3] / 2
            await move(cx + 300, cy - 220, cx, cy, 30)
            await hold_until(1.25)
            async def do_click(x, y):
                await pg.mouse.click(x, y); await pg.evaluate('()=>{const w=document.getElementById("a0-pvw");w.scrollTop=w.scrollHeight}')
            await click_at(cx, cy, lambda: do_click(cx, cy))
            await hold_until(4.5)
            b2 = await cellbox(33); cx2, cy2 = b2[0] + b2[2] / 2, b2[1] + b2[3] / 2
            await cap('Click again until the lines join up ✓')
            await move(cx, cy, cx2, cy2, 14)
            await click_at(cx2, cy2, lambda: do_click(cx2, cy2))
            await hold_until(6.3)
            b3 = await cellbox(33); await hl([b3[0] - 4, b3[1] - b3[3] - 4, b3[2] * 2 + 8, b3[3] * 2 + 8]); await frame()
            await hold_until(T['click'][1] - T['click'][0]); await hl(None); await cursor(0, 0, False)
            enc_seq('c', 'v05_click')
            # ---- download: 41.6-46.0 ----
            await pg.evaluate('()=>document.getElementById("a0-out").scrollIntoView({block:"center"})')
            sb = await pg.locator('#a0-out').bounding_box(); await hl([sb['x'] - 6, sb['y'] - 6, sb['width'] + 12, sb['height'] + 12]); await cap('Choose “One sheet”')
            await cursor(sb['x'] + sb['width'] * .7, sb['y'] + sb['height'] * .65)
            await pg.screenshot(path=os.path.join(FR, 'dl1.jpg'), type='jpeg', quality=92); enc_still(os.path.join(FR, 'dl1.jpg'), 2.0, 'v06_dl1')
            bb = await pg.locator('#a0-dl').bounding_box(); await hl([bb['x'] - 6, bb['y'] - 6, bb['width'] + 12, bb['height'] + 12]); await cap('Download your A0 PDF')
            await cursor(bb['x'] + bb['width'] * .6, bb['y'] + bb['height'] * .62)
            await pg.screenshot(path=os.path.join(FR, 'dl2.jpg'), type='jpeg', quality=92); enc_still(os.path.join(FR, 'dl2.jpg'), T['dl'][1] - T['dl'][0] - 2.0, 'v07_dl2')
            # ---------- result + outro cards ----------
            for key in ['result', 'outro']:
                await cp.evaluate('c=>show(c)', key); await cp.wait_for_timeout(250)
                pth = os.path.join(FR, key + '.jpg'); await cp.screenshot(path=pth, type='jpeg', quality=92)
                enc_still(pth, T[key][1] - T[key][0], 'v08_' + key)
            await br.close()
    finally:
        srv.terminate()
    with open(os.path.join(OUT, 'list.txt'), 'w') as f:
        for s in scenes: f.write("file '%s'\n" % s)
    final = os.path.join(OUT, 'a4-to-a0-youtube-silent.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', os.path.join(OUT, 'list.txt'), '-c', 'copy', '-movflags', '+faststart', final + '.tmp.mp4'], check=True)
    os.rename(final + '.tmp.mp4', final); print(final)
asyncio.run(main())
