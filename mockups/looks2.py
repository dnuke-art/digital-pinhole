"""Aperture experiments and dither styles. python3 mockups/looks2.py -> out/look2_*.png, experiments_sheet.png, dither_sheet.png"""
import os, numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageOps
from scipy import ndimage
import looks as L

OUT = L.OUT; rng = np.random.default_rng(11)

# ------------------------------------------------------------ helpers
def conv_rgb(a, k):
    k = k / k.sum()
    return np.stack([ndimage.convolve(a[..., c], k, mode="nearest") for c in range(3)], axis=2)

def night_scene(w=1200, h=900, n=14, seed=5, size=2):
    r = np.random.default_rng(seed)
    a = np.zeros((h, w, 3), np.float32)
    a += 0.02 * L.smooth_noise(h, w, 120, seed)[..., None] * np.array([0.6, 0.7, 1.0])
    for _ in range(n):
        x, y = int(r.integers(60, w - 60)), int(r.integers(80, h * 0.7))
        col = r.choice([[1.0, 0.85, 0.5], [0.9, 0.95, 1.0], [1.0, 0.5, 0.3], [0.6, 0.9, 1.0]])
        a[y - size:y + size + 1, x - size:x + size + 1] += np.array(col) * 4.0
    a[int(h * 0.72):, :] += 0.03
    return a

def label_inset(im, box, scale=4):
    """Paste a zoomed crop of `box` in the corner."""
    x0, y0, x1, y1 = box
    crop = im.crop(box).resize(((x1 - x0) * scale, (y1 - y0) * scale), Image.NEAREST)
    out = im.copy(); out.paste(crop, (im.width - crop.width - 12, 12))
    d = ImageDraw.Draw(out); d.rectangle([im.width - crop.width - 13, 11, im.width - 12, 12 + crop.height], outline=(255, 255, 255), width=2)
    d.rectangle(box, outline=(255, 255, 255), width=1)
    return out

# ------------------------------------------------------------ 1. single slit (anamorphic blur)
def single_slit(im, slit_len_frac=0.08):
    a = L.to_np(L.pinhole(im, 250, 65, 0.85))
    a = ndimage.uniform_filter1d(a, int(slit_len_frac * a.shape[0]), axis=0, mode="nearest")
    return L.to_im(a)

# ------------------------------------------------------------ 2. double slit, white light (doubled + streaked)
def double_slit_white(im, sep_px=40):
    a = L.to_np(single_slit(im))
    b = 0.5 * (np.roll(a, -sep_px // 2, axis=1) + np.roll(a, sep_px // 2, axis=1))
    return L.to_im(b)

# ------------------------------------------------------------ 3. double slit on the Pi sensor, red filter, point lights: real fringes
def double_slit_fringes(w=1200, h=900):
    # Pi HQ direct: sensor 6.17 mm across 1200 px -> 5.1 um/px. L=5 mm, slit w=0.05 mm, d=0.12 mm, lambda=650 nm.
    um = 6170 / w; Ld = 5000.0; sw, d, lam = 50.0, 120.0, 0.65
    x = (np.arange(-60, 61)) * um
    beta = np.pi * sw * x / (lam * Ld); env = np.where(beta == 0, 1, np.sin(beta) / np.where(beta == 0, 1, beta)) ** 2
    fr = np.cos(np.pi * d * x / (lam * Ld)) ** 2
    kx = env * fr
    ky = np.ones(int(1000 / um))                              # 1 mm long slits -> 1 mm vertical streak
    k = np.outer(ky, kx)
    scene = night_scene(w, h, n=12, seed=6, size=0)
    scene = np.where(scene > 1, scene, scene * 0.03)          # distant lights on a dark night
    red = 0.7 * scene[..., 0] + 0.3 * scene[..., 1]           # red gel
    out = ndimage.convolve(red, k / k.sum(), mode="constant")
    out = out / np.percentile(out, 99.97)
    rgb = np.stack([out, out * 0.12, out * 0.08], axis=2)
    rgb += rng.normal(0, 0.02, rgb.shape)
    im = L.to_im(np.clip(rgb, 0, 1))
    ys, xs = np.where(red > 1); i = np.argmin(abs(ys - h * 0.4) + abs(xs - w * 0.4)); cx, cy = int(xs[i]), int(ys[i])
    return label_inset(im, (cx - 40, cy - 90, cx + 40, cy + 90), 4)

# ------------------------------------------------------------ 4. crossed slits at two distances: anamorphic
def crossed_slits(im, squeeze=2.0):
    w, h = im.size
    a = im.resize((int(w * squeeze), h), Image.LANCZOS).crop(((int(w * squeeze) - w) // 2, 0, (int(w * squeeze) - w) // 2 + w, h))
    a = L.to_np(L.pinhole(a, 220, 65, 0.85))
    a = ndimage.gaussian_filter1d(a, 3.0, axis=0)             # the nearer slit blurs its axis a bit more
    return L.to_im(a)

# ------------------------------------------------------------ 5. five pinholes in an X
def multi_pinhole(im, offs=26):
    a = L.to_np(L.pinhole(im, 200, 65, 0.85)); acc = np.zeros_like(a)
    for dx, dy in [(0, 0), (offs, offs), (-offs, offs), (offs, -offs), (-offs, -offs)]:
        acc += np.roll(np.roll(a, dx, 1), dy, 0)
    return L.to_im(acc / 5)

# ------------------------------------------------------------ 6. moire: picket fence through a row of pinholes
def moire(im):
    """A hole array is a linear convolution and cannot make moire. Multiplication can: here the
    projected picket fence lands on a screen printed with fine lines."""
    a = L.to_np(L.pinhole(im, 200, 65, 0.85)); h, w, _ = a.shape
    xx = np.arange(w)
    fence = ((xx % 18) < 9).astype(np.float32)                         # pickets, period 18 px at the screen
    fence = ndimage.gaussian_filter1d(fence, 1.5)                      # pinhole softening
    a = a * (0.15 + 0.85 * fence)[None, :, None]
    grid = 1 - 0.85 * ((xx % 19.5) < 7).astype(np.float32)            # thin lines printed on the screen, 19.5 px pitch
    b = a * grid[None, :, None]
    b = ndimage.gaussian_filter(b, (0.8, 0.8, 0))                      # relay camera
    return L.to_im(b / b.max())

# ------------------------------------------------------------ 7. shaped pinhole (star) on night lights
def star_kernel(r=15, points=5):
    s = 2 * r + 1; k = np.zeros((s, s), np.float32)
    yy, xx = np.mgrid[-r:r + 1, -r:r + 1]; ang = np.arctan2(yy, xx); rad = np.hypot(xx, yy)
    rr = r * (0.42 + 0.58 * (0.5 + 0.5 * np.cos(points * ang)) ** 2.5)
    k[rad <= rr] = 1
    return k

def shaped_pinhole(w=1200, h=900):
    scene = night_scene(w, h, n=18, seed=9)
    k = star_kernel(16)
    out = conv_rgb(scene, k) * 6
    out = ndimage.gaussian_filter(out, (1.0, 1.0, 0))
    return L.to_im(np.clip(out + rng.normal(0, 0.015, out.shape), 0, 1))

# ------------------------------------------------------------ 8. zone plate: sharp-ish core, big chromatic halo
def zone_plate(im):
    core = L.to_np(L.pinhole(im, 300, 65, 0.95))
    out = np.zeros_like(core)
    for c, sig in enumerate([26, 16, 34]):                    # designed for green; red and blue defocus
        halo = ndimage.gaussian_filter(core[..., c], sig)
        out[..., c] = 0.45 * core[..., c] + 0.75 * halo
    out = out / out.max() * 1.05
    return L.to_im(out)

def zone_plate_mask(size=600, zones=24):
    yy, xx = np.mgrid[-size // 2:size // 2, -size // 2:size // 2]; r2 = xx ** 2 + yy ** 2
    r1 = (size / 2) ** 2 / zones
    m = ((r2 // r1) % 2 == 0) & (r2 < (size / 2) ** 2)
    return Image.fromarray((m * 255).astype(np.uint8)).convert("RGB")

# ------------------------------------------------------------ 9. coded aperture (MURA): raw + decoded
def mura(p):
    qr = {(i * i) % p for i in range(1, p)}
    C = lambda x: 1 if (x % p) in qr else -1
    A = np.zeros((p, p), np.float32)
    for i in range(p):
        for j in range(p):
            if i == 0: A[i, j] = 0
            elif j == 0: A[i, j] = 1
            elif C(i) * C(j) == 1: A[i, j] = 1
    G = np.where(A == 1, 1.0, -1.0); G[0, 0] = 1.0
    return A, G

def coded_aperture(im, p=101, noise=0.0008):
    A, G = mura(p)
    g = np.asarray(ImageOps.grayscale(im).resize((p, p), Image.LANCZOS)).astype(np.float32) / 255
    FA = np.fft.fft2(A)
    raw = np.real(np.fft.ifft2(np.fft.fft2(g) * FA))          # scene shadowed through the mosaicked mask
    raw += rng.normal(0, noise * raw.mean(), raw.shape)
    dec = np.real(np.fft.ifft2(np.fft.fft2(raw) * np.conj(np.fft.fft2(G))))
    dec = (dec - dec.min()) / (dec.max() - dec.min())
    rawn = (raw - raw.min()) / (raw.max() - raw.min())
    up = lambda a: Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).resize((900, 900), Image.NEAREST).convert("RGB")
    mask = Image.fromarray((A * 255).astype(np.uint8)).resize((900, 900), Image.NEAREST).convert("RGB")
    return mask, up(rawn), up(dec)

# ------------------------------------------------------------ 10. anaglyph from two colour-filtered pinholes
def anaglyph(im, max_disp=14):
    a = L.to_np(L.pinhole(im, 200, 65, 0.85)); h, w, _ = a.shape
    yy = np.arange(h); disp = np.clip((yy - 0.42 * h) / (0.58 * h), 0, 1) * max_disp   # ground plane: nearer at the bottom
    left = np.zeros_like(a); right = np.zeros_like(a)
    for y in range(h):
        s = int(round(disp[y] / 2))
        left[y] = np.roll(a[y], -s, axis=0); right[y] = np.roll(a[y], s, axis=0)
    out = np.stack([left[..., 0], right[..., 1], right[..., 2]], axis=2)
    return L.to_im(out)

# ------------------------------------------------------------ 11. slit-scan time strip on the receipt roll
def slit_scan(im, length=1500, width=384):
    g = L.to_np(L.pinhole(im, 200, 65, 0.85)); h, w, _ = g.shape
    col = g[:, int(0.42 * w) - 2:int(0.42 * w) + 3].mean(axis=1)              # the vertical slice under the slit
    col = np.asarray(Image.fromarray((col[None] * 255).astype(np.uint8)).resize((width, 1), Image.LANCZOS))[0] / 255
    t = np.linspace(0, 1, length)
    day = np.clip(np.sin(np.pi * (t - 0.05) / 0.9), 0, 1) ** 0.7
    warm = np.exp(-((t - 0.88) / 0.05) ** 2); cool = np.exp(-((t - 0.1) / 0.05) ** 2)
    strip = np.repeat(col[None], length, axis=0) * day[:, None, None]
    strip *= (1 + 0.5 * warm[:, None, None] * np.array([1, 0.5, 0.1]) + 0.4 * cool[:, None, None] * np.array([0.1, 0.4, 1]))
    r = np.random.default_rng(3)
    for _ in range(6):                                           # people crossing the slit
        t0 = int(r.integers(int(0.15 * length), int(0.85 * length))); dur = int(r.integers(6, 30)); y0 = int(width * r.uniform(0.55, 0.85))
        strip[t0:t0 + dur, y0 - 30:y0 + 4] *= 0.35
    strip += rng.normal(0, 0.01, strip.shape)
    out = L.to_im(np.clip(strip, 0, 1)).transpose(Image.TRANSPOSE)
    out = ImageOps.grayscale(out).convert("1").convert("RGB")    # printed on the receipt: 1-bit dither
    paper = Image.new("RGB", (out.width + 40, out.height + 80), (246, 242, 232))
    paper.paste(out, (20, 40))
    d = ImageDraw.Draw(paper); f = L.font(14)
    d.text((24, 12), "SLIT-SCAN   06:00", fill=(60, 60, 60), font=f); d.text((paper.width - 140, 12), "21:00", fill=(60, 60, 60), font=f)
    d.text((24, paper.height - 28), "one printed row per 30 s; the roll is the film", fill=(60, 60, 60), font=f)
    return paper

# ------------------------------------------------------------ dithers
BAYER2 = np.array([[0, 2], [3, 1]]) / 4
def bayer(n):
    m = BAYER2
    while m.shape[0] < n:
        k = m.shape[0]; m = np.block([[4 * m, 4 * m + 2], [4 * m + 3, 4 * m + 1]]) / 4 / (k * k) * (k * k)
    return (m + 0.5) / (m.size) if m.max() > 1 else (m * (n * n) + 0.5) / (n * n)

def ordered(g, n=4, levels=2):
    m = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16 if n == 4 else \
        (np.array([[0, 2], [3, 1]]) / 4 if n == 2 else None)
    if n == 8:
        b4 = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]])
        m = np.block([[4 * b4, 4 * b4 + 2], [4 * b4 + 3, 4 * b4 + 1]]) / 64
    h, w = g.shape; T = np.tile(m, (h // m.shape[0] + 1, w // m.shape[1] + 1))[:h, :w]
    q = np.floor(g * (levels - 1) + T) / (levels - 1)
    return np.clip(q, 0, 1)

def atkinson(g):
    a = g.astype(np.float32).copy(); h, w = a.shape; out = np.zeros_like(a)
    for y in range(h):
        for x in range(w):
            old = a[y, x]; new = 1.0 if old > 0.5 else 0.0; out[y, x] = new; e = (old - new) / 8
            for dx, dy in [(1, 0), (2, 0), (-1, 1), (0, 1), (1, 1), (0, 2)]:
                if 0 <= x + dx < w and 0 <= y + dy < h: a[y + dy, x + dx] += e
    return out

def halftone(g, cell=9, angle=45):
    rot = ndimage.rotate(g, angle, reshape=True, order=1, cval=1.0); h, w = rot.shape
    out = np.ones_like(rot)
    yy, xx = np.mgrid[0:cell, 0:cell]; rr = np.hypot(yy - cell / 2 + 0.5, xx - cell / 2 + 0.5)
    for y in range(0, h - cell, cell):
        for x in range(0, w - cell, cell):
            dark = 1 - rot[y:y + cell, x:x + cell].mean()
            out[y:y + cell, x:x + cell] = np.where(rr <= cell * 0.62 * np.sqrt(dark), 0.0, 1.0)
    back = ndimage.rotate(out, -angle, reshape=True, order=0, cval=1.0)
    H, W = g.shape; cy, cx = back.shape[0] // 2, back.shape[1] // 2
    return back[cy - H // 2:cy - H // 2 + H, cx - W // 2:cx - W // 2 + W]

def line_screen(g, cell=7):
    h, w = g.shape; out = np.ones_like(g)
    for y in range(0, h - cell, cell):
        dark = 1 - g[y:y + cell].reshape(cell, -1).mean(axis=0)
        dark = ndimage.uniform_filter1d(dark, 3)
        for k in range(cell):
            out[y + k] = np.where(abs(k - cell / 2 + 0.5) < cell * dark / 2, 0.0, 1.0)
    return out

def gameboy(im):
    g = np.asarray(ImageOps.grayscale(L.pinhole(im, 200, 65, 0.85)).resize((128, 112), Image.LANCZOS)) / 255
    g = (g - g.min()) / (g.max() - g.min())
    q = ordered(g, 4, 4)
    pal = np.array([[15, 56, 15], [48, 98, 48], [139, 172, 15], [155, 188, 15]]) / 255
    idx = np.rint(q * 3).astype(int)
    return Image.fromarray((pal[idx] * 255).astype(np.uint8)).resize((128 * 7, 112 * 7), Image.NEAREST)

def cga(im):
    a = L.to_np(L.pinhole(im, 200, 65, 0.85).resize((320, 200), Image.LANCZOS))
    pal = np.array([[0, 0, 0], [85, 255, 255], [255, 85, 255], [255, 255, 255]]) / 255
    m = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16 - 0.5
    T = np.tile(m, (50, 80))[..., None]
    a2 = np.clip(a + 0.35 * T, 0, 1)
    d = ((a2[:, :, None, :] - pal[None, None, :, :]) ** 2).sum(-1)
    idx = d.argmin(-1)
    return Image.fromarray((pal[idx] * 255).astype(np.uint8)).resize((1280, 800), Image.NEAREST)

def gray_for_dither(im, w=384):
    g = ImageOps.grayscale(L.pinhole(im, 200, 65, 0.85)); h = int(w * g.height / g.width)
    g = ImageOps.autocontrast(g.resize((w, h), Image.LANCZOS), cutoff=1)
    return np.asarray(g) / 255

def as_print(bw, scale=3):
    im = Image.fromarray((np.clip(bw, 0, 1) * 255).astype(np.uint8)).convert("RGB")
    im = im.resize((im.width * scale, im.height * scale), Image.NEAREST)
    a = L.to_np(im); a = a * np.array([0.965, 0.95, 0.91]) + (1 - a) * np.array([0.13, 0.13, 0.15])
    return L.to_im(a)

if __name__ == "__main__":
    castle = L.load("pic_1040.jpg"); portrait = L.load("pic_1027.jpg")
    R = []
    def save(name, im, title, sub):
        im.save(f"{OUT}/look2_{name}.png"); R.append((title, sub, im)); print("wrote", name)
    save("01_single_slit", single_slit(castle), "Single slit", "0.5 x 20 mm vertical slit: sharp across, streaked along the slit")
    save("02_double_slit_white", double_slit_white(castle), "Double slit, daylight", "two slits 8 mm apart: two streaked copies, no fringes in white light")
    save("03_double_slit_fringes", double_slit_fringes(), "Double slit on the Pi sensor", "0.12 mm slit pair, red gel, point lights at night: real fringes, 16 um pitch")
    save("04_crossed_slits", crossed_slits(castle), "Crossed slits, two depths", "vertical slit at 200 mm, horizontal at 100 mm: anamorphic 2:1")
    save("05_multi_pinhole", multi_pinhole(castle), "Five pinholes in an X", "5 mm spacing: five overlapping copies, five times the light")
    save("06_moire", moire(castle), "Moire: fence projected onto a lined screen", "picket period 18 vs printed lines 19.5: beat bands every 234; a hole array cannot do this")
    save("07_star_pinhole", shaped_pinhole(), "Star-shaped hole, night", "6 mm star aperture: every point light wears the hole's shape")
    save("08_zone_plate", zone_plate(castle), "Zone plate", "diffractive lens: sharper core than a pinhole, chromatic glow, ~4x faster")
    mask, raw, dec = coded_aperture(castle)
    save("09_mura_mask", mask, "Coded aperture plate (MURA 101)", "half the plate is open: ~5000 holes, thousands of times a pinhole's light")
    save("10_mura_raw", raw, "Coded aperture, raw capture", "what the screen actually shows: the scene shadowed through the mask")
    save("11_mura_decoded", dec, "Coded aperture, decoded", "one correlation in software recovers the picture at 101 x 101")
    save("12_anaglyph", anaglyph(castle), "Two holes, red and cyan gels", "65 mm apart: the capture is already an anaglyph; wear the glasses")
    save("13_slit_scan", slit_scan(castle), "Slit-scan onto the receipt roll", "vertical slit, one printed row per 30 s; a day is a metre of paper")
    L.sheet(R, cols=3).save(f"{OUT}/experiments_sheet.png"); print("wrote experiments_sheet.png")

    g = gray_for_dither(castle); D = []
    def dsave(name, im, title, sub):
        im.save(f"{OUT}/dither_{name}.png"); D.append((title, sub, im)); print("wrote dither", name)
    dsave("01_floyd", as_print(np.asarray(Image.fromarray((g * 255).astype(np.uint8)).convert("1")) * 1.0), "Floyd-Steinberg", "error diffusion; the receipt printer default")
    dsave("02_atkinson", as_print(atkinson(g)), "Atkinson", "1984 Macintosh dither: lighter, crisper, loses shadow detail")
    dsave("03_bayer4", as_print(ordered(g, 4)), "Bayer 4x4 ordered", "the crosshatch of early PC graphics")
    dsave("04_bayer8", as_print(ordered(g, 8)), "Bayer 8x8 ordered", "smoother ramps, still a visible grid")
    dsave("05_halftone", as_print(halftone(g), 3), "Halftone dot screen, 45°", "newspaper; moires against any periodic subject")
    dsave("06_linescreen", as_print(line_screen(g), 3), "Line screen", "engraving-like; thickness carries tone")
    dsave("07_gameboy", gameboy(castle), "Game Boy Camera", "128 x 112, four greens, ordered dither")
    dsave("08_cga", cga(castle), "CGA palette 1", "320 x 200, black / cyan / magenta / white, ordered dither")
    dsave("09_chunky", as_print(np.asarray(Image.fromarray((np.asarray(Image.fromarray((g * 255).astype(np.uint8)).resize((96, 72), Image.LANCZOS))).astype(np.uint8)).convert("1")) * 1.0, 12), "1-bit at 96 px", "the pinhole's ~200 real points, quartered, then dithered")
    L.sheet(D, cols=3).save(f"{OUT}/dither_sheet.png"); print("wrote dither_sheet.png")
