import sys, numpy as np
from PIL import Image
SRC = np.array([(247,240,233),(255,255,255),(30,27,25),(181,83,60),(192,132,151),(44,62,80),(230,221,214),(244,241,238),(233,214,222),(250,226,150)], float)
DST = np.array([(238,244,239),(255,255,255),(31,59,51),(47,107,87),(122,166,138),(31,59,51),(213,227,216),(241,246,242),(214,232,220),(207,227,212)], float)
def recolor(img):
    a = np.array(img.convert('RGB'), float); H, W, _ = a.shape
    p = a.reshape(-1, 3)
    d = ((p[:, None, :] - SRC[None]) ** 2).sum(-1)
    o = np.argsort(d, 1)[:, :2]; i, j = o[:, 0], o[:, 1]
    A, B, A2, B2 = SRC[i], SRC[j], DST[i], DST[j]
    AB = B - A
    t = np.clip(((p - A) * AB).sum(1) / np.maximum((AB ** 2).sum(1), 1e-6), 0, 1)[:, None]
    q = A + t * AB; r = p - q
    out = np.clip(A2 + t * (B2 - A2) + r, 0, 255).reshape(H, W, 3)
    # keep the brand logo untouched (terracotta icon in the bottom bar)
    bar = a[520:]
    terra = (np.abs(bar - SRC[3]).sum(-1) < 90) | ((bar[..., 0] > 200) & (bar[..., 2] < 230) & (bar[..., 0] - bar[..., 2] > 15))
    ys, xs = np.nonzero(terra[:, :W // 2 + 100])
    if len(xs):
        x0, x1, y0, y1 = xs.min() - 1, xs.max() + 2, ys.min() + 520 - 1, ys.max() + 520 + 2
        box = a[y0:y1, x0:x1]
        ink = np.abs(box - SRC[2]).sum(-1) < 40
        sub = out[y0:y1, x0:x1]
        sub[~ink] = box[~ink]
        out[y0:y1, x0:x1] = sub
    return Image.fromarray(out.astype(np.uint8))
if __name__ == '__main__':
    recolor(Image.open(sys.argv[1])).save(sys.argv[2], quality=93)
