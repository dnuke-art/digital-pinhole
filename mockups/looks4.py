"""Curved gratings: concave grating spectrograph (Rowland) and a circular constant-pitch aperture (axicon rings).
python3 mockups/looks4.py -> out/look4_*.png, curved_grating_sheet.png"""
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
import looks as L, looks2 as L2, looks3 as L3

OUT = L.OUT; rng = np.random.default_rng(31)
LAM = np.linspace(400, 700, 301)                      # nm
RGB_L = L3.wl_rgb(LAM)                                # colour of each wavelength

def basis(centre, width): return np.exp(-0.5 * ((LAM - centre) / width) ** 2)
BR, BG, BB = basis(610, 40), basis(545, 40), basis(460, 35)

def spectrum_from_rgb(rgb):
    return rgb[0] * BR + rgb[1] * BG + rgb[2] * BB

def render_spectrograph(rows, w=1200, h=900, slit_nm=5.0, zero_order=True, title=None, labels=None):
    """rows: list of (y_frac, height_frac, spectrum over LAM (0..1), rgb of the zero-order)."""
    img = np.zeros((h, w, 3), np.float32)
    x0, x1 = int(0.22 * w), int(0.97 * w)                                  # 400 .. 700 nm
    xs = x0 + (LAM - 400) / 300 * (x1 - x0)
    px_per_nm = (x1 - x0) / 300
    for yf, hf, S, rgb0 in rows:
        ya, yb = int(yf * h), int((yf + hf) * h)
        line = np.zeros((w, 3), np.float32)
        for k in range(len(LAM) - 1):
            xa, xb = int(xs[k]), int(xs[k + 1]) + 1
            line[xa:xb] += S[k] * RGB_L[k]
        img[ya:yb, :, :] += line[None]
        if zero_order:
            img[ya:yb, int(0.06 * w):int(0.06 * w) + 6, :] += rgb0 * 0.9
    img = ndimage.gaussian_filter(img, (1.0, slit_nm * px_per_nm / 2.4, 0))   # slit width sets spectral resolution
    img = img / max(np.percentile(img, 99.8), 1e-6)
    img += rng.normal(0, 0.008, img.shape)
    im = L.to_im(np.clip(img, 0, 1)); d = ImageDraw.Draw(im); f = L.font(16); f2 = L.font(13)
    for nm in (400, 450, 500, 550, 600, 650, 700):
        x = int(x0 + (nm - 400) / 300 * (x1 - x0))
        d.line([(x, h - 40), (x, h - 30)], fill=(150, 150, 150)); d.text((x - 12, h - 26), f"{nm}", fill=(170, 170, 170), font=f2)
    d.text((int(0.06 * w) - 24, h - 26), "0 order", fill=(170, 170, 170), font=f2)
    if title: d.text((16, 12), title, fill=(200, 200, 200), font=f)
    if labels:
        for yf, text in labels: d.text((int(0.10 * w), int(yf * h)), text, fill=(180, 180, 180), font=f2)
    return im

# ------------------------------------------------------------ 1. daylight: the scene through a vertical slit
def spectrograph_day(im, n=150):
    a = L.to_np(L.pinhole(im, 200, 65, 0.9)); h, w, _ = a.shape
    col = a[:, int(0.42 * w) - 3:int(0.42 * w) + 4].mean(axis=1)
    col = np.asarray(Image.fromarray((col[None] * 255).astype(np.uint8)).resize((n, 1), Image.LANCZOS))[0] / 255
    rows = [(k / n, 1 / n, spectrum_from_rgb(c), c) for k, c in enumerate(col)]
    return render_spectrograph(rows, title="concave grating, vertical slit through the castle: position along the slit vs wavelength")

# ------------------------------------------------------------ 2. night: lamps of different kinds along the slit
def lamp(kind):
    if kind == "sodium":       return 1.0 * basis(589, 1.2) + 0.15 * basis(569, 1.0) + 0.1 * basis(616, 1.0)
    if kind == "warm LED":     return 0.55 * basis(452, 9) + 0.9 * basis(590, 45) + 0.3 * basis(530, 30)
    if kind == "cool LED":     return 1.0 * basis(452, 9) + 0.6 * basis(555, 45)
    if kind == "neon":         return 0.5 * basis(585, 1) + 0.8 * basis(614, 1) + 1.0 * basis(640, 1) + 0.6 * basis(703, 1) + 0.3 * basis(540, 1)
    if kind == "mercury / fluorescent": return 0.5 * basis(436, 1.2) + 1.0 * basis(546, 1.2) + 0.6 * basis(578, 1.5) + 0.25 * basis(611, 8) + 0.15 * (LAM > 0)
    if kind == "incandescent": return np.exp(-((LAM - 720) / 220) ** 2) * (LAM / 700) ** 2
    if kind == "laser pointer":return basis(532, 0.6)

def spectrograph_night():
    kinds = ["sodium", "warm LED", "cool LED", "neon", "mercury / fluorescent", "incandescent", "laser pointer"]
    rows, labels = [], []
    for k, kind in enumerate(kinds):
        S = lamp(kind); S = S / S.max()
        rgb0 = (S[:, None] * RGB_L).sum(0); rgb0 = rgb0 / max(rgb0.max(), 1e-6)
        yf = 0.10 + k * 0.115
        rows.append((yf, 0.05, S, rgb0)); labels.append((yf + 0.012, kind))
    return render_spectrograph(rows, slit_nm=3.0, title="the same box at night: each streetlight writes its spectrum", labels=labels)

# ------------------------------------------------------------ 3. circular constant-pitch aperture: discs with rainbow rings
def axicon_night(w=1200, h=900, f_mm=200.0, pitch_um=20.0, disc_mm=3.0):
    scene = L2.night_scene(w, h, n=10, seed=23, size=0)
    scene = np.where(scene > 1, scene, 0)
    ys, xs = np.where(scene.sum(-1) > 1)
    out = np.zeros_like(scene)
    yy, xx = np.mgrid[0:h, 0:w]
    px = L3.PX_PER_MM
    for y, x in zip(ys, xs):
        col = scene[y, x] / scene[y, x].max()
        r = np.hypot(xx - x, yy - y)
        out += (r <= disc_mm / 2 * px)[..., None] * col * 0.6                       # zero order: the 3 mm aperture's blur disc
        for k in range(0, len(LAM), 6):
            rad = f_mm * (LAM[k] * 1e-3) / pitch_um * px                             # ring radius = f * lambda / d
            ring = np.exp(-((r - rad) ** 2) / (2 * 1.2 ** 2))
            wgt = (RGB_L[k] * col).sum() / max(RGB_L[k].sum(), 1e-6)
            out += ring[..., None] * RGB_L[k] * wgt * 0.9 * 6 / len(LAM) * 4
    out = ndimage.gaussian_filter(out, (0.8, 0.8, 0))
    out = out / np.percentile(out, 99.9) + rng.normal(0, 0.01, out.shape)
    return L.to_im(np.clip(out, 0, 1))

if __name__ == "__main__":
    castle = L.load("pic_1040.jpg"); R = []
    def save(name, im, title, sub):
        im.save(f"{OUT}/look4_{name}.png"); R.append((title, sub, im)); print("wrote", name)
    save("01_spectrograph_day", spectrograph_day(castle), "Concave grating, slit, daylight", "the grating is the lens: each point on the slit becomes a horizontal spectrum")
    save("02_spectrograph_night", spectrograph_night(), "Concave grating, slit, night", "0.5 mm slit, 500 l/mm on an f = 200 mm mirror: ~5 nm resolution")
    save("03_axicon_night", axicon_night(), "Circular constant-pitch aperture, night", "3 mm plate, 20 um rings: every light is a disc inside a rainbow ring")
    L.sheet(R, cols=3).save(f"{OUT}/curved_grating_sheet.png"); print("wrote curved_grating_sheet.png")
