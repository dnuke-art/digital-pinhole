"""Diffraction gratings: linear grating over the pinhole (disperses), zone plate (focuses), digital fixes.
python3 mockups/looks3.py -> out/look3_*.png, grating_sheet.png"""
import numpy as np
from PIL import Image
from scipy import ndimage
import looks as L, looks2 as L2

OUT = L.OUT; rng = np.random.default_rng(21)
PX_PER_MM = 1200 / 250.0                     # relay screen: 250 mm across 1200 px
F_MM = 200.0                                 # box depth

def wl_rgb(lam):
    """Crude wavelength (nm) -> linear RGB."""
    r = np.clip(np.where(lam < 440, -(lam - 440) / 60, np.where(lam < 510, 0, np.where(lam < 580, (lam - 510) / 70, 1))), 0, 1)
    g = np.clip(np.where(lam < 440, 0, np.where(lam < 490, (lam - 440) / 50, np.where(lam < 580, 1, np.where(lam < 645, -(lam - 645) / 65, 0)))), 0, 1)
    b = np.clip(np.where(lam < 490, 1, np.where(lam < 510, -(lam - 510) / 20, 0)), 0, 1)
    fade = np.clip(np.where(lam < 420, 0.3 + 0.7 * (lam - 380) / 40, np.where(lam > 680, 0.3 + 0.7 * (700 - lam) / 20, 1)), 0, 1)
    return np.stack([r, g, b], -1) * fade[..., None]

def disp_px(lam_nm, lines_per_mm=500.0, f_mm=F_MM):
    d_um = 1000.0 / lines_per_mm
    s = np.clip(lam_nm * 1e-3 / d_um, 0, 0.999)
    return f_mm * np.tan(np.arcsin(s)) * PX_PER_MM

LAMS = np.linspace(400, 700, 61)

# ------------------------------------------------------------ 1. linear grating over the pinhole, night
def grating_night(w=1200, h=900):
    scene = L2.night_scene(w, h, n=10, seed=17, size=1)
    scene = np.where(scene > 1, scene, 0)
    out = 0.35 * scene.copy()
    ys, xs = np.where(scene.sum(-1) > 1)
    seen = set()
    for y, x in zip(ys, xs):
        key = (y // 4, x // 4)
        if key in seen: continue
        seen.add(key)
        col = scene[y, x] / scene[y, x].max()
        for lam in LAMS:
            c = wl_rgb(np.array([lam]))[0]
            wgt = (c * col).sum() / max(c.sum(), 1e-6)               # how much of this light is at this wavelength
            dx = int(round(disp_px(lam)))
            for sgn in (1, -1):
                xx = x + sgn * dx
                if 0 <= xx < w:
                    out[y - 1:y + 2, xx - 1:xx + 2] += c * wgt * 0.55 / len(LAMS) * 12
    out = ndimage.gaussian_filter(out, (1.2, 1.2, 0))
    return L.to_im(np.clip(out / np.percentile(out, 99.9), 0, 1))

# ------------------------------------------------------------ 2. linear grating, daylight
def grating_day(im):
    a = L.to_np(L.pinhole(im, 200, 65, 0.85)); h, w, _ = a.shape
    out = 0.4 * a
    for lam in LAMS:
        c = wl_rgb(np.array([lam]))[0]
        band = (a * c).sum(-1) / c.sum()                               # scene energy near this wavelength
        dx = int(round(disp_px(lam)))
        for sgn in (1, -1):
            out += 0.3 * np.roll(band, sgn * dx, axis=1)[..., None] * c * (3.0 / len(LAMS))
    return L.to_im(np.clip(out, 0, 1))

# ------------------------------------------------------------ 3. zone plate on the box, white light, as captured
def zone_plate_capture(im, N=25):
    src = L.to_np(im); h, w, _ = src.shape
    lam = np.array([650., 550., 450.])
    f = F_MM * 550 / lam                                                # focal length per colour
    R = np.sqrt(N * F_MM * 550e-6)                                      # outer radius, mm
    blur_mm = 2 * R * abs(F_MM - f) / f                                 # defocus blur diameter at the screen
    out = np.zeros_like(src)
    for c in range(3):
        sig = max(0.35, blur_mm[c] * PX_PER_MM / 2.4)
        focused = ndimage.gaussian_filter(src[..., c], sig)             # +1 order
        zero = ndimage.gaussian_filter(src[..., c], 2 * R * PX_PER_MM / 2.4)      # 0 order: soft image through the whole plate
        minus = ndimage.gaussian_filter(src[..., c], 4 * R * PX_PER_MM / 2.4)     # -1 order and the rest
        out[..., c] = 1.0 * focused + 2.5 * zero + 1.5 * minus
    out = out / out.max()
    out = out * L.falloff(w, h, 65)[..., None] + rng.normal(0, 0.006, out.shape)
    return L.to_im(np.clip(out, 0, 1)), blur_mm, 2 * R

# ------------------------------------------------------------ 4. digital fix: deconvolve the known PSF, luminance from green
def zone_plate_digital(cap):
    a = L.to_np(cap)
    sharp = np.zeros_like(a)
    for c in range(3):
        halo = ndimage.gaussian_filter(a[..., c], 18)
        sharp[..., c] = np.clip((a[..., c] - 0.72 * halo) / 0.28, 0, 1)
    lum = sharp[..., 1]
    col = ndimage.gaussian_filter(sharp, (4, 4, 0)); col_l = col.mean(-1) + 1e-6
    out = col / col_l[..., None] * lum[..., None]
    return L.to_im(np.clip(out, 0, 1))

def zone_plate_pattern(size=700, N=25):
    yy, xx = np.mgrid[-size // 2:size // 2, -size // 2:size // 2]; r2 = xx ** 2 + yy ** 2
    r1 = (size / 2) ** 2 / N
    m = ((r2 // r1) % 2 == 0) & (r2 < (size / 2) ** 2)
    return Image.fromarray((m * 255).astype(np.uint8)).convert("RGB")

if __name__ == "__main__":
    castle = L.load("pic_1040.jpg"); R = []
    def save(name, im, title, sub):
        im.save(f"{OUT}/look3_{name}.png"); R.append((title, sub, im)); print("wrote", name)
    save("01_grating_night", grating_night(), "500 l/mm grating over the pinhole, night", "every light: a point plus two 34 mm rainbows; it disperses, it does not focus")
    save("02_grating_day", grating_day(castle), "Same grating, daylight", "the scene plus two rainbow-smeared ghosts 40 to 75 mm to each side")
    cap, blur, D = zone_plate_capture(castle)
    save("03_zone_plate_pattern", zone_plate_pattern(), "Zone plate, 25 zones, f = 200 mm", "a grating whose pitch shrinks outward; 3.3 mm across, outer zone 33 um")
    save("04_zone_plate_capture", cap, "Zone plate as captured, white light", f"green sharp, red/blue defocused {blur[0]:.1f}/{blur[2]:.1f} mm, glow from the 0 and -1 orders")
    save("05_zone_plate_digital", zone_plate_digital(cap), "Zone plate, digital fix", "known halo subtracted, luminance from the sharp green channel")
    L.sheet(R, cols=3).save(f"{OUT}/grating_sheet.png"); print("wrote grating_sheet.png")
