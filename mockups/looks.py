"""Simulate what each approach's output looks like, from sample photos.
Run from anywhere: python3 mockups/looks.py -> mockups/out/look_*.png + looks_sheet.png
"""
import os, numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
SRC, OUT = f"{HERE}/src", f"{HERE}/out"
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(7)

def load(name, size=(1200, 900)):
    return Image.open(f"{SRC}/{name}").convert("RGB").resize(size, Image.LANCZOS)

def font(sz):
    try:
        return ImageFont.truetype("DejaVuSans.ttf", sz)
    except Exception:
        try: return ImageFont.load_default(size=sz)
        except Exception: return ImageFont.load_default()

def to_np(im): return np.asarray(im).astype(np.float32) / 255
def to_im(a): return Image.fromarray(np.clip(a * 255, 0, 255).astype(np.uint8))

def falloff(w, h, fov_deg):
    """cos^4 illumination falloff for a horizontal field of view."""
    yy, xx = np.mgrid[0:h, 0:w]
    xn = (xx - w / 2) / (w / 2); yn = (yy - h / 2) / (w / 2)
    half = np.tan(np.radians(fov_deg / 2))
    theta = np.arctan(np.hypot(half * xn, half * yn))
    return np.cos(theta) ** 4

def pinhole(im, points, fov_deg=65, contrast=0.85, noise=0.0, mono=False):
    """Pinhole rendering: `points` resolvable points across, cos^4 falloff, flare."""
    w, h = im.size
    small = im.resize((points, max(1, int(points * h / w))), Image.LANCZOS)
    back = small.resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(w / points * 0.45))
    a = to_np(back)
    if mono: a = np.repeat(a.mean(axis=2, keepdims=True), 3, axis=2)
    a = a * falloff(w, h, fov_deg)[..., None]
    a = a * contrast + (1 - contrast) * 0.30
    if noise: a = a + rng.normal(0, noise, a.shape)
    return to_im(a)

# ---------- digital captures ----------
def relay_digital(im):
    return pinhole(im, 200, fov_deg=65, contrast=0.82, noise=0.012)

def pi_hq_direct(im):
    out = to_np(pinhole(im, 45, fov_deg=95, contrast=0.75, noise=0.02))
    w, h = im.size
    yy, xx = np.mgrid[0:h, 0:w]
    r2 = ((xx - w/2)/(w/2))**2 + ((yy - h/2)/(w/2))**2
    out[..., 1] *= (1 - 0.25 * r2)          # green drops in corners -> magenta cast
    out[..., 2] *= (1 + 0.10 * r2)
    return to_im(out)

def fullframe_bodycap(im):
    return pinhole(im, 180, fov_deg=90, contrast=0.85, noise=0.008)

# ---------- receipt printer ----------
def receipt(im, dots=384, scale=2, caption="DIGITAL PINHOLE   2026-09-07   240 s"):
    g = ImageOps.grayscale(pinhole(im, 200, 65, 0.85))
    w, h = g.size
    g = g.resize((dots, int(dots * h / w)), Image.LANCZOS)
    g = ImageOps.autocontrast(g, cutoff=1)
    bw = np.asarray(g.convert("1"))          # Floyd-Steinberg by default
    margin = 40; pw = dots + 2 * margin; ph = bw.shape[0] + 150
    paper = np.ones((ph, pw, 3), np.float32) * np.array([0.965, 0.95, 0.91])
    paper += rng.normal(0, 0.012, paper.shape)
    ink = np.array([0.13, 0.13, 0.15])
    y0 = 60
    region = paper[y0:y0 + bw.shape[0], margin:margin + dots]
    region[~bw] = ink
    out = to_im(paper).resize((pw * scale, ph * scale), Image.NEAREST)
    d = ImageDraw.Draw(out)
    f = font(11 * scale)
    d.text((margin * scale, 20 * scale), "* * *  pinhole box  * * *", fill=(40, 40, 45), font=f)
    d.text((margin * scale, (y0 + bw.shape[0] + 18) * scale), caption, fill=(40, 40, 45), font=f)
    d.text((margin * scale, (y0 + bw.shape[0] + 40) * scale), "f/317  ISO 800  250 mm screen", fill=(40, 40, 45), font=f)
    # torn bottom edge
    arr = to_np(out); H, W, _ = arr.shape
    tear = (rng.random(W) * 6 * scale).astype(int)
    for x in range(W):
        arr[H - 8 * scale + tear[x]:, x] = 1.0
    return to_im(arr)

# ---------- cyanotype ----------
def smooth_noise(h, w, scale, seed=0):
    r = np.random.default_rng(seed)
    small = r.random((max(2, h // scale), max(2, w // scale)))
    return np.asarray(Image.fromarray((small * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)) / 255

def brushed_mask(h, w, inset=50, wobble=18, seed=3):
    r = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:h, 0:w]
    n = smooth_noise(h, w, 40, seed)
    left = inset + (n[:, 0] - 0.5) * 2 * wobble
    right = w - inset + (n[:, -1] - 0.5) * 2 * wobble
    top = inset + (n[0, :] - 0.5) * 2 * wobble
    bot = h - inset + (n[-1, :] - 0.5) * 2 * wobble
    m = (xx >= left[:, None]) & (xx <= right[:, None]) & (yy >= top[None, :]) & (yy <= bot[None, :])
    # brush overshoots
    for _ in range(5):
        y = int(r.integers(inset, h - inset)); x0 = int(r.choice([inset - 60, w - inset]))
        m[y:y + int(r.integers(6, 14)), max(0, x0):min(w, x0 + 70)] = True
    for _ in range(4):
        x = int(r.integers(inset, w - inset)); y0 = int(r.choice([inset - 60, h - inset]))
        m[max(0, y0):min(h, y0 + 70), x:x + int(r.integers(6, 14))] = True
    return m.astype(np.float32)

def cyanotype(im, points=200):
    g = to_np(ImageOps.grayscale(pinhole(im, points, 65, 0.85)).convert("RGB"))[..., 0]
    h, w = g.shape
    pad = 70
    H, W = h + 2 * pad, w + 2 * pad
    d = np.zeros((H, W), np.float32)
    d[pad:pad + h, pad:pad + w] = (1 - g) ** 0.8
    mask = brushed_mask(H, W, inset=pad - 10)
    mask_soft = np.asarray(Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3))) / 255
    coat = mask_soft * (0.8 + 0.2 * smooth_noise(H, W, 60, 5))   # uneven coating density
    d = d * coat
    paper = np.array([0.93, 0.90, 0.82]); deep = np.array([0.04, 0.12, 0.32]); mid = np.array([0.18, 0.40, 0.67])
    rgb = paper * (1 - d[..., None]) + deep * d[..., None]
    wgt = (4 * d * (1 - d))[..., None]
    rgb = rgb * (1 - 0.45 * wgt) + mid * 0.45 * wgt
    # uncoated-but-brushed edge shows faint blue (the coat tone with no image)
    edge_only = np.clip(coat - d, 0, 1)[..., None] * (mask_soft[..., None] > 0.05)
    rgb = rgb * (1 - 0.08 * edge_only) + mid * 0.08 * edge_only
    rgb += (smooth_noise(H, W, 3, 9)[..., None] - 0.5) * 0.06      # paper grain
    rgb += (smooth_noise(H, W, 120, 11)[..., None] - 0.5) * 0.04   # paper tone variation
    return to_im(rgb)

# ---------- wet plate collodion (ambrotype) ----------
def collodion(im, points=110):
    a = to_np(im)
    lum = 0.8 * a[..., 2] + 0.2 * a[..., 1]                   # blue/UV sensitivity only
    lum_im = to_im(np.repeat(lum[..., None], 3, 2))
    p = to_np(pinhole(lum_im, points, 60, 0.9))[..., 0]
    h, w = p.shape
    t = np.clip((p - 0.10) / 0.52, 0, 1) ** 0.75
    t = t * (0.94 + 0.06 * smooth_noise(h, w, 90, 21))          # collodion thickness streaks
    # pour marks: uncoated wedge at one corner, drip edge along the bottom
    yy, xx = np.mgrid[0:h, 0:w]
    n = smooth_noise(h, w, 50, 22)
    wedge = (xx + 0.9 * (h - yy) < 0.30 * w + (n[:, 0][:, None] - 0.5) * 120)   # bottom-left corner
    drip = yy > h - 26 - (smooth_noise(1, w, 12, 23)[0] * 30)[None, :]
    coated = ~(wedge | drip)
    coat_edge = np.asarray(Image.fromarray((coated * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2))) / 255
    # oyster-shell ripple near the pour corner
    ripple = 0.5 + 0.5 * np.sin((np.hypot(xx - 0.05 * w, yy - 0.95 * h)) / 9.0)
    near = np.clip(1 - np.hypot(xx - 0.05 * w, yy - 0.95 * h) / (0.28 * w), 0, 1) ** 2
    t = t * (1 - 0.12 * near * ripple)
    cream = np.array([0.86, 0.84, 0.77]); black = np.array([0.07, 0.065, 0.06]); warm = np.array([0.45, 0.42, 0.37])
    rgb = black * (1 - t[..., None]) + cream * t[..., None]
    wgt = (4 * t * (1 - t))[..., None]
    rgb = rgb * (1 - 0.3 * wgt) + warm * 0.3 * wgt
    rgb = rgb * coat_edge[..., None] + black * (1 - coat_edge[..., None])
    # bevelled dark frame
    pad = 40
    frame = np.ones((h + 2 * pad, w + 2 * pad, 3), np.float32) * 0.12
    frame[pad:pad + h, pad:pad + w] = rgb
    frame[pad - 3:pad, pad - 3:pad + w + 3] = 0.35; frame[pad + h:pad + h + 3, pad - 3:pad + w + 3] = 0.05
    frame[pad - 3:pad + h + 3, pad - 3:pad] = 0.30; frame[pad - 3:pad + h + 3, pad + w:pad + w + 3] = 0.06
    return to_im(frame)

# ---------- sun-trace recorder on thermal paper ----------
def sun_trace(w=1500, h=300):
    paper = np.ones((h, w, 3), np.float32) * np.array([0.97, 0.955, 0.90])
    paper += rng.normal(0, 0.01, paper.shape)
    im = to_im(paper); d = ImageDraw.Draw(im); f = font(20)
    for hr in range(5, 20):
        x = int((hr - 4) / 16 * w)
        d.line([(x, 0), (x, h)], fill=(190, 185, 170), width=1)
        d.text((x + 6, h - 30), f"{hr:02d}", fill=(120, 115, 100), font=f)
    d.text((14, 12), "SUN TRACE  thermal paper  2026-09-07", fill=(90, 85, 75), font=f)
    a = to_np(im)
    # burnt arc: gentle curve, thickest at noon, broken by clouds
    xs = np.arange(int(0.12 * w), int(0.93 * w))
    T = (xs - xs.min()) / (xs.max() - xs.min())
    ys = h * 0.62 - 60 * np.sin(np.pi * T)
    width = 3 + 9 * np.sin(np.pi * T)
    cloudy = np.zeros_like(T, bool)
    for _ in range(7):
        c = rng.random(); L = rng.random() * 0.06 + 0.01
        cloudy |= (T > c) & (T < c + L)
    yy, xx = np.mgrid[0:h, 0:w]
    burn = np.zeros((h, w), np.float32)
    for x, y, wd, cl in zip(xs, ys, width, cloudy):
        if cl: continue
        col = np.exp(-((yy[:, x] - y) ** 2) / (2 * (wd / 2) ** 2))
        burn[:, x] = np.maximum(burn[:, x], col)
    burn = np.asarray(Image.fromarray((burn * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))) / 255
    dark = np.array([0.16, 0.12, 0.10])
    a = a * (1 - burn[..., None]) + dark * burn[..., None]
    halo = np.asarray(Image.fromarray((burn * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(9))) / 255
    a = a * (1 - 0.25 * halo[..., None]) + np.array([0.55, 0.45, 0.35]) * 0.25 * halo[..., None]
    return to_im(a)

# ---------- solargraphy ----------
def solargraph(im, points=120):
    p = to_np(pinhole(im, points, 75, 0.8, mono=True))[..., 0]
    h, w = p.shape
    # scanned paper negative, inverted: strange tones
    t = 1 - p
    shadow = np.array([0.10, 0.06, 0.20]); high = np.array([0.85, 0.72, 0.45]); mid = np.array([0.35, 0.30, 0.55])
    rgb = shadow * (1 - t[..., None]) + high * t[..., None]
    wgt = (4 * t * (1 - t))[..., None]; rgb = rgb * (1 - 0.5 * wgt) + mid * 0.5 * wgt
    rgb = 1 - rgb  # back to positive-ish
    # sun arcs across the upper half, many days
    arcs = np.zeros((h, w), np.float32)
    yy, xx = np.mgrid[0:h, 0:w]
    for k in range(22):
        peak = h * (0.08 + 0.32 * k / 27)
        xs = np.arange(int(0.05 * w), int(0.95 * w))
        T = (xs - xs.min()) / (xs.max() - xs.min())
        ys = peak + (h * 0.58 - peak) * (1 - np.sin(np.pi * T)) ** 1.3
        gaps = np.zeros_like(T, bool)
        for _ in range(int(rng.integers(0, 5))):
            c = rng.random(); gaps |= (T > c) & (T < c + rng.random() * 0.15)
        for x, y, g in zip(xs, ys, gaps):
            if g or y >= h: continue
            arcs[:, x] = np.maximum(arcs[:, x], np.exp(-((yy[:, x] - y) ** 2) / 4))
    arcs = np.asarray(Image.fromarray((np.clip(arcs, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.5))) / 255
    sun = np.array([1.0, 0.95, 0.75])
    rgb = rgb * (1 - 0.9 * arcs[..., None]) + sun * 0.9 * arcs[..., None]
    rgb += (smooth_noise(h, w, 4, 41)[..., None] - 0.5) * 0.08
    rgb = rgb * 0.9 + 0.05
    return to_im(rgb)

# ---------- bitumen heliograph ----------
def heliograph(im, points=60):
    p = to_np(pinhole(im, points, 60, 0.7, mono=True))[..., 0]
    h, w = p.shape
    pewter = np.array([0.46, 0.46, 0.45]); bitumen = np.array([0.72, 0.67, 0.55])
    t = np.clip((p - 0.30) / 0.35, 0, 1)            # only bright areas harden
    rgb = pewter * (1 - t[..., None]) + bitumen * t[..., None]
    yy, xx = np.mgrid[0:h, 0:w]
    spec = 0.10 * np.clip(1 - np.hypot((xx - 0.3 * w) / w, (yy - 0.3 * h) / h) * 1.6, 0, 1)
    rgb += spec[..., None] + (smooth_noise(h, w, 2, 51)[..., None] - 0.5) * 0.05
    return to_im(rgb)

# ---------- sheet ----------
def sheet(items, cols=3, cell=(560, 420), pad=24, label_h=56, bg=(28, 28, 30)):
    rows = (len(items) + cols - 1) // cols
    W = cols * (cell[0] + pad) + pad; H = rows * (cell[1] + label_h + pad) + pad
    out = Image.new("RGB", (W, H), bg); d = ImageDraw.Draw(out)
    f1 = font(20); f2 = font(15)
    for k, (title, sub, im) in enumerate(items):
        c, r = k % cols, k // cols
        x = pad + c * (cell[0] + pad); y = pad + r * (cell[1] + label_h + pad)
        th = ImageOps.contain(im, cell)
        out.paste(th, (x + (cell[0] - th.width) // 2, y + (cell[1] - th.height) // 2))
        d.text((x, y + cell[1] + 8), title, fill=(235, 235, 235), font=f1)
        d.text((x, y + cell[1] + 32), sub, fill=(160, 160, 165), font=f2)
    return out

if __name__ == "__main__":
    castle = load("pic_1040.jpg"); portrait = load("pic_1027.jpg"); fjord = load("pic_1015.jpg")
    results = []
    def save(name, im, title, sub):
        im.save(f"{OUT}/look_{name}.png"); results.append((title, sub, im)); print("wrote", name, im.size)

    save("00_source", castle, "Source scene", "sample photo, for comparison")
    save("01_relay_digital", relay_digital(castle), "Relay camera obscura", "f/317 pinhole, 250 mm screen, Pi camera, ~200 points across")
    save("02_fullframe_bodycap", fullframe_bodycap(castle), "Full-frame body cap", "f/180, 36 mm sensor, ~180 points across")
    save("03_pi_hq_direct", pi_hq_direct(castle), "Pi HQ camera, lens off", "f/70, 6 mm sensor, ~45 points, corner colour shift")
    save("04_receipt", receipt(castle), "Receipt printer output", "relay frame, 384 dots, Floyd-Steinberg, 58 mm paper")
    save("05_cyanotype", cyanotype(castle), "Cyanotype from digital negative", "hand-coated, contact printed from the relay frame")
    save("06_collodion_landscape", collodion(castle), "Wet plate pinhole, ambrotype", "blue/UV only: white sky, dark foliage; pour marks")
    save("07_collodion_portrait", collodion(portrait), "Wet plate pinhole, portrait", "red lips go black, skin goes luminous")
    save("08_solargraph", solargraph(castle), "Solargraphy", "months of sun arcs on photo paper, no developer")
    save("09_sun_trace", sun_trace(), "Sun-trace recorder", "glass sphere burns thermal paper across a day")
    save("10_heliograph", heliograph(castle), "Bitumen heliograph", "all-day lens exposure, lavender oil develop, no fixer")
    sheet(results).save(f"{OUT}/looks_sheet.png"); print("wrote looks_sheet.png")
