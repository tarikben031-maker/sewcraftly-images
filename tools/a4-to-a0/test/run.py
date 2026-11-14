"""Drive the widget in Chrome on each synthetic PDF, build the output, verify accuracy against the master."""
import asyncio, base64, json, os, sys, time, subprocess
import numpy as np, fitz
from playwright.async_api import async_playwright
HERE=os.path.dirname(os.path.abspath(__file__)); PD=os.path.join(HERE,'pdfs'); OUTD=os.path.join(HERE,'out'); os.makedirs(OUTD,exist_ok=True)
MM=72/25.4

def render_gray(pdf_path_or_doc, page, ppmm, clip_mm=None):
    d = fitz.open(pdf_path_or_doc) if isinstance(pdf_path_or_doc,str) else pdf_path_or_doc
    p = d[page]
    mat = fitz.Matrix(ppmm/MM, ppmm/MM)
    clip = None
    if clip_mm: clip = fitz.Rect(*[v*MM for v in clip_mm])
    pix = p.get_pixmap(matrix=mat, clip=clip, colorspace=fitz.csRGB, alpha=False)
    a = np.frombuffer(pix.samples, np.uint8).reshape(pix.h, pix.w, 3).astype(np.int16)
    return a

def verify(name, truth, outpath, state, mg):
    """Compare every tile region of the output sheets with the master."""
    out = fitz.open(outpath); ppmm = 4
    master = fitz.open(os.path.join(PD, truth['master']))
    tw, th = truth['tile']
    res = []
    # output tile size as computed by tool
    ot = state['tile']
    # walk sheets: reconstruct tile positions from state.sheetsInfo
    for s_i, s in enumerate(state['sheets']):
        for row in range(s['r0'], s['r1']):
            for col in range(s['c0'], s['c1']):
                x0 = mg + (col - s['c0'])*ot[0]; y0 = mg + (row - s['r0'])*ot[1]
                inset = 0
                a = render_gray(out, s_i, ppmm, (x0+inset, y0+inset, x0+ot[0]-inset, y0+ot[1]-inset))
                # same region in master (master origin = tile grid origin)
                mx0 = col*tw + inset; my0 = row*th + inset
                b = render_gray(master, 0, ppmm, (mx0, my0, mx0+ot[0]-2*inset, my0+ot[1]-2*inset))
                h = min(a.shape[0], b.shape[0]); w = min(a.shape[1], b.shape[1]); a=a[:h,:w]; b=b[:h,:w]
                # ignore green guide lines in output
                green = (a[:,:,1] > 150) & (a[:,:,0] < 120) & (a[:,:,2] < 120)
                ga = a.mean(2); gb = b.mean(2)
                ink_b = gb < 200
                # best shift search +-2mm
                best=None
                for dy in range(-4,5,2):
                    for dx in range(-4,5,2):
                        A = np.roll(np.roll(ga,dy,0),dx,1); G = np.roll(np.roll(green,dy,0),dx,1)
                        m = (~G)[10:-10,10:-10]
                        diff = np.abs(A[10:-10,10:-10]-gb[10:-10,10:-10])[m].mean()
                        if best is None or diff < best[0]: best=(diff,dx,dy)
                diff0 = np.abs(ga-gb)[(~green)].mean()
                res.append(dict(sheet=s_i,row=row,col=col,diff0=round(float(diff0),3),best=(round(best[0],3),best[1]/ppmm,best[2]/ppmm)))
    return res

async def main():
    names = sys.argv[1:] or ['s1','s2','s3','s4','s5']
    srv = subprocess.Popen([sys.executable,'-m','http.server','8765'],cwd=os.path.join(HERE,'www'),stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    time.sleep(1)
    summary={}
    try:
        async with async_playwright() as p:
            br = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
            for name in names:
                truth = json.load(open(os.path.join(PD,name+'.json')))
                pg = await br.new_page(viewport={'width':1300,'height':1000})
                logs=[]; pg.on('console', lambda m: logs.append(m.text)); pg.on('pageerror', lambda e: logs.append('PAGEERR '+str(e)))
                await pg.goto('http://localhost:8765/index_en.html')
                t0=time.time()
                await pg.set_input_files('#a0-file', os.path.join(PD,name+'.pdf'))
                try:
                    await pg.wait_for_selector('#a0-main', state='visible', timeout=180000)
                except Exception as e:
                    print(name,'TIMEOUT', logs, await pg.inner_text('#a0-err')); continue
                el=time.time()-t0
                st = await pg.evaluate('''()=>{var S=window.__sca0();return {tiles:S.tiles,order:S.order,c:S.c,colMajor:S.colMajor,trim:S.trim,src:S.trimSrc,badge:document.getElementById('a0-badge').textContent}}''')
                await pg.select_option('#a0-out', 'one')
                info = await pg.evaluate('''async()=>{var S=window.__sca0();var b=await window.__sca0build();var bin='';for(var i=0;i<b.length;i+=32768)bin+=String.fromCharCode.apply(null,b.subarray(i,i+32768));return {b64:btoa(bin),size:document.getElementById('a0-size').textContent,sheets:document.getElementById('a0-sheets').textContent}}''')
                outp=os.path.join(OUTD,name+'_one.pdf'); open(outp,'wb').write(base64.b64decode(info['b64']))
                await pg.select_option('#a0-out', 'a0')
                info2 = await pg.evaluate('''async()=>{var b=await window.__sca0build();var bin='';for(var i=0;i<b.length;i+=32768)bin+=String.fromCharCode.apply(null,b.subarray(i,i+32768));return {b64:btoa(bin),sheets:document.getElementById('a0-sheets').textContent}}''')
                outa=os.path.join(OUTD,name+'_a0.pdf'); open(outa,'wb').write(base64.b64decode(info2['b64']))
                await pg.screenshot(path=os.path.join(OUTD,name+'_ui.png'), full_page=True)
                bl = await pg.evaluate('''async()=>{var S=window.__sca0();var o=S.order.slice();S.order.splice(1,0,-1);document.getElementById('a0-cols').dispatchEvent(new Event('input'));var b=await window.__sca0build();S.order=o;document.getElementById('a0-cols').dispatchEvent(new Event('input'));return b.length}''')
                print('   blank-cell build bytes', bl)
                exp_trim=truth['trim']; got=[st['trim'][k] for k in 'ltrb']
                ok_layout = (st['c']==truth['cols'] and not st['colMajor'] and st['tiles']==list(range(truth['first']-1,truth['first']-1+truth['n'])))
                print(f"== {name}: {el:.1f}s layout_ok={ok_layout} c={st['c']} colMajor={st['colMajor']} tiles={st['tiles'][0]+1}..{st['tiles'][-1]+1}({len(st['tiles'])})")
                print('   trim exp',exp_trim,'got',got,'err(mm)',[round(g-e,3) for g,e in zip(got,exp_trim)],'src',{k:v['k'] for k,v in st['src'].items()})
                print('   badge:',st['badge']); print('   one:',info['size'],info['sheets'],' a0:',info2['sheets'])
                errs=[l for l in logs if 'rror' in l or 'PAGEERR' in l]
                if errs: print('   LOGS',errs[:5])
                summary[name]=dict(st=st,ok_layout=ok_layout)
                if not truth.get('master'):
                    await pg.close(); continue
                # verification on 'one' output
                tm=[truth['tile'][0],truth['tile'][1]]
                sheets=[dict(r0=0,r1=truth['rows'],c0=0,c1=truth['cols'])]
                ot=[ (210 if False else 0) ]
                d=fitz.open(outp); pw=d[0].rect.width/MM; ph=d[0].rect.height/MM
                tile=[ (pw-2*10)/truth['cols'], (ph-2*10)/truth['rows'] ]
                r=verify(name,truth,outp,dict(tile=tile,sheets=sheets),10)
                worst=max(r,key=lambda x:x['diff0']); shifts=set((x['best'][1],x['best'][2]) for x in r)
                print('   page mm', round(pw,2), round(ph,2), 'tile mm', [round(v,3) for v in tile], 'expected', [round(v,3) for v in tm])
                print('   worst diff0', worst['diff0'], 'best shifts found', shifts, 'mean diff0', round(np.mean([x['diff0'] for x in r]),3))
                await pg.close()
            await br.close()
    finally:
        srv.terminate()
asyncio.run(main())
