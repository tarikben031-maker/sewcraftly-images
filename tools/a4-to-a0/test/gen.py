"""Generate synthetic tiled sewing-pattern PDFs + ground truth."""
import fitz, json, math, random, sys, os
MM = 72/25.4
OUT = os.path.join(os.path.dirname(__file__), 'pdfs'); os.makedirs(OUT, exist_ok=True)

def master(wmm, hmm, seed):
    random.seed(seed)
    d = fitz.open(); p = d.new_page(width=wmm*MM, height=hmm*MM)
    sh = p.new_shape()
    W, H = wmm*MM, hmm*MM
    # pattern-piece like closed curves
    for k in range(14):
        cx, cy = random.uniform(.1,.9)*W, random.uniform(.1,.9)*H
        pts = []
        n = random.randint(5,9)
        for i in range(n):
            a = 2*math.pi*i/n + random.uniform(-.2,.2)
            r = random.uniform(60,240)*MM
            pts.append(fitz.Point(cx+r*math.cos(a), cy+r*math.sin(a)))
        pts.append(pts[0])
        sh.draw_polyline(pts); sh.finish(color=(0,0,0), width=0.8)
    for k in range(40):  # random straight lines, many angles
        a = fitz.Point(random.uniform(0,W), random.uniform(0,H)); b = fitz.Point(random.uniform(0,W), random.uniform(0,H))
        sh.draw_line(a,b); sh.finish(color=random.choice([(0,0,0),(.8,0,0),(0,0,.8),(.3,.3,.3)]), width=random.choice([.5,.8,1.2]), dashes=random.choice([None,'[4 2] 0']))
    for k in range(30):
        c = fitz.Point(random.uniform(0,W), random.uniform(0,H)); sh.draw_circle(c, random.uniform(10,120)*MM); sh.finish(color=(0,0,0), width=.6)
    for k in range(25):
        p.insert_text(fitz.Point(random.uniform(0,W-80*MM), random.uniform(20,H)), random.choice(['FRONT','BACK','CUT 2','SLEEVE','FOLD','grainline','Size 12']), fontsize=random.choice([10,14,24]))
    # 10 cm test square
    r = fitz.Rect(40*MM, 40*MM, 140*MM, 140*MM); sh.draw_rect(r); sh.finish(color=(0,0,0), width=1)
    sh.commit()
    return d

GREEN = (0, .8, 0)

def tile_doc(m, pw, ph, cols, rows, area, clipsz, origin_fn, deco, front_pages=0, skip=()):
    """area: target rect on page (mm) where master content is shown; clipsz: (w,h) mm of master shown; origin_fn(c,r)->(x,y) mm in master"""
    d = fitz.open()
    for i in range(front_pages):
        p = d.new_page(width=pw*MM, height=ph*MM); p.insert_text((40,80), 'COVER / INSTRUCTIONS page %d'%(i+1), fontsize=20)
        p.draw_rect(fitz.Rect(60,120,400,500), color=(0,0,0))
    n = 0
    for r in range(rows):
        for c in range(cols):
            if (c,r) in skip: continue
            n += 1
            p = d.new_page(width=pw*MM, height=ph*MM)
            x, y = origin_fn(c, r)
            clip = fitz.Rect(x*MM, y*MM, (x+clipsz[0])*MM, (y+clipsz[1])*MM)
            tgt = fitz.Rect(area[0]*MM, area[1]*MM, area[2]*MM, area[3]*MM)
            p.show_pdf_page(tgt, m, 0, clip=clip)
            deco(p, c, r, n)
    return d

def save(d, name, truth):
    d.save(os.path.join(OUT, name+'.pdf'), garbage=3, deflate=True)
    json.dump(truth, open(os.path.join(OUT, name+'.json'),'w'))

# S1 butt frame, A4 portrait, asymmetric margins, cover pages
L,T,R_,B = 12,15,10,13; tw, th = 210-L-R_, 297-T-B; C,Rw = 4,4
m = master(C*tw, Rw*th, 1)
def deco1(p,c,r,n):
    p.draw_rect(fitz.Rect(L*MM,T*MM,(210-R_)*MM,(297-B)*MM), color=GREEN, width=.5)
    p.insert_text((L*MM, 8*MM), 'Page %d   %s%d'%(n,'ABCDEFG'[r],c+1), fontsize=9)
d = tile_doc(m,210,297,C,Rw,(L,T,210-R_,297-B),(tw,th),lambda c,r:(c*tw,r*th),deco1,front_pages=2)
m.save(os.path.join(OUT,'s1_master.pdf'))
save(d,'s1',dict(trim=[L,T,R_,B],cols=C,rows=Rw,first=3,n=C*Rw,tile=[tw,th],master='s1_master.pdf'))

# S2 overlap with lines, A4 landscape
pw,ph=297,210; L,T=20,20; pitchw,pitchh=257,170; ov=10; C,Rw=4,3
m = master(C*pitchw+ov, Rw*pitchh+ov, 2)
def deco2(p,c,r,n):
    p.draw_line((L*MM,0),(L*MM,ph*MM),color=GREEN,width=.6)
    p.draw_line((0,T*MM),(pw*MM,T*MM),color=GREEN,width=.6)
    p.draw_line(((L+pitchw)*MM,0),((L+pitchw)*MM,ph*MM),color=GREEN,width=.6,dashes='[3 2] 0')
    p.draw_line((0,(T+pitchh)*MM),(pw*MM,(T+pitchh)*MM),color=GREEN,width=.6,dashes='[3 2] 0')
    p.insert_text((5*MM, 6*MM), 'overlap here  %d'%n, fontsize=8)
d = tile_doc(m,pw,ph,C,Rw,(L,T,L+pitchw+ov,T+pitchh+ov),(pitchw+ov,pitchh+ov),lambda c,r:(c*pitchw,r*pitchh),deco2)
m.save(os.path.join(OUT,'s2_master.pdf'))
save(d,'s2',dict(trim=[L,T,pw-L-pitchw,ph-T-pitchh],cols=C,rows=Rw,first=1,n=C*Rw,tile=[pitchw,pitchh],master='s2_master.pdf'))

# S3 corner marks only, US Letter
pw,ph=215.9,279.4; mg=12.7; tw,th=pw-2*mg,ph-2*mg; C,Rw=5,3
m = master(C*tw, Rw*th, 3)
def deco3(p,c,r,n):
    for (x,y) in [(mg,mg),(pw-mg,mg),(mg,ph-mg),(pw-mg,ph-mg)]:
        sx = -1 if x<pw/2 else 1; sy = -1 if y<ph/2 else 1
        p.draw_line(((x+sx*3)*MM,y*MM),((x+sx*12)*MM,y*MM),color=(0,0,0),width=.5)
        p.draw_line((x*MM,(y+sy*3)*MM),(x*MM,(y+sy*12)*MM),color=(0,0,0),width=.5)
    p.insert_text((pw/2*MM, 6*MM), '%d'%n, fontsize=8)
d = tile_doc(m,pw,ph,C,Rw,(mg,mg,pw-mg,ph-mg),(tw,th),lambda c,r:(c*tw,r*th),deco3)
m.save(os.path.join(OUT,'s3_master.pdf'))
save(d,'s3',dict(trim=[mg,mg,mg,mg],cols=C,rows=Rw,first=1,n=C*Rw,tile=[tw,th],master='s3_master.pdf'))

# S4 clip only (no lines), landscape displayed via /Rotate 90, with layers
pw,ph=297,210; mg=10; tw,th=pw-2*mg,ph-2*mg; C,Rw=3,4
m = master(C*tw, Rw*th, 4)
d = fitz.open()
ocg_on = d.add_ocg('Size 10', on=True); ocg_off = d.add_ocg('Size 12', on=False)
n=0
for r in range(Rw):
    for c in range(C):
        n+=1
        p = d.new_page(width=pw*MM, height=ph*MM)
        p.show_pdf_page(fitz.Rect(mg*MM,mg*MM,(pw-mg)*MM,(ph-mg)*MM), m, 0, clip=fitz.Rect(c*tw*MM,r*th*MM,(c+1)*tw*MM,(r+1)*th*MM))
        p.insert_text(((mg+60)*MM,(mg+60)*MM),'HIDDEN LAYER TEXT',fontsize=30,color=(1,0,0),oc=ocg_off)
        p.insert_text(((mg+60)*MM,(mg+90)*MM),'visible layer',fontsize=20,color=(0,0,1),oc=ocg_on)
m.save(os.path.join(OUT,'s4_master.pdf'))
d.save(os.path.join(OUT,'s4_tmp.pdf'))
# rotate: store landscape content in portrait user space + /Rotate 90
import pikepdf
pdf = pikepdf.open(os.path.join(OUT,'s4_tmp.pdf'))
for pg in pdf.pages:
    W = float(pg.mediabox[2]); H = float(pg.mediabox[3])
    pg.contents_coalesce()
    data = pg.Contents.read_bytes()
    pg.Contents.write(b'q 0 1 -1 0 %f 0 cm\n'%H + data + b'\nQ')
    pg.MediaBox = pikepdf.Array([0,0,H,W]); pg.Rotate = 90
pdf.save(os.path.join(OUT,'s4.pdf')); os.remove(os.path.join(OUT,'s4_tmp.pdf'))
json.dump(dict(trim=[mg,mg,mg,mg],cols=C,rows=Rw,first=1,n=C*Rw,tile=[tw,th],master='s4_master.pdf'),open(os.path.join(OUT,'s4.json'),'w'))

# S5 big: 7x6 A4 butt frame with symmetric margins and thick frame lines
L=T=R_=B=8; tw,th=210-16,297-16; C,Rw=7,6
m = master(C*tw, Rw*th, 5)
def deco5(p,c,r,n):
    p.draw_rect(fitz.Rect(L*MM,T*MM,(210-R_)*MM,(297-B)*MM), color=(0,0,0), width=1.0)
d = tile_doc(m,210,297,C,Rw,(L,T,210-R_,297-B),(tw,th),lambda c,r:(c*tw,r*th),deco5)
m.save(os.path.join(OUT,'s5_master.pdf'))
save(d,'s5',dict(trim=[L,T,R_,B],cols=C,rows=Rw,first=1,n=C*Rw,tile=[tw,th],master='s5_master.pdf'))
print('ok')
