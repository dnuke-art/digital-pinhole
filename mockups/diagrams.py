"""Cross-section diagrams of each camera build. python3 mockups/diagrams.py -> mockups/out/diag_*.png"""
import os, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle, FancyBboxPatch, Wedge
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = f"{HERE}/out"; os.makedirs(OUT, exist_ok=True)
WALL, INT, CONE, CAM, PAPER, INK, DIM = "#4a4a4a", "#141414", "#ffd66b", "#7fc8ff", "#f3eee2", "#222", "#8a8a8a"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})

def fig(w=10, h=6.2):
    f, ax = plt.subplots(figsize=(w, h), dpi=150); ax.set_aspect("equal"); ax.axis("off"); return f, ax

def wall(ax, x, y, w, h):
    ax.add_patch(Rectangle((x, y), w, h, fc=WALL, ec="#222", lw=0.8, hatch="////", zorder=3))

def hollow_box(ax, x0, y0, depth, height, t, hole_y=None, hole_gap=4, back_open=False):
    """Interior origin at (x0,y0): x0 = inside face of front wall, y0 = floor. Returns nothing."""
    ax.add_patch(Rectangle((x0, y0), depth, height, fc=INT, ec="none", zorder=1))
    wall(ax, x0 - t, y0 - t, depth + 2 * t, t)                      # floor
    wall(ax, x0 - t, y0 + height, depth + 2 * t, t)                 # lid
    if hole_y is None: wall(ax, x0 - t, y0, t, height)
    else:
        wall(ax, x0 - t, y0, t, hole_y - hole_gap / 2)
        wall(ax, x0 - t, y0 + hole_y + hole_gap / 2, t, height - hole_y - hole_gap / 2)
    if not back_open: wall(ax, x0 + depth, y0, t, height)

def cone(ax, apex, x_far, y_lo, y_hi, color=CONE, alpha=0.45, z=2):
    ax.add_patch(Polygon([apex, (x_far, y_lo), (x_far, y_hi)], closed=True, fc=color, ec="none", alpha=alpha, zorder=z))

def pinhole_plate(ax, x, y, size=14, t=1.2, label=None):
    ax.add_patch(Rectangle((x - t, y - size / 2), t, size / 2 - 0.5, fc="#c9a227", ec="#222", lw=0.5, zorder=5))
    ax.add_patch(Rectangle((x - t, y + 0.5), t, size / 2 - 0.5, fc="#c9a227", ec="#222", lw=0.5, zorder=5))

def dim(ax, p0, p1, text, off=10, color=DIM):
    (x0, y0), (x1, y1) = p0, p1
    dx, dy = x1 - x0, y1 - y0; L = np.hypot(dx, dy); nx, ny = -dy / L * off, dx / L * off
    a, b = (x0 + nx, y0 + ny), (x1 + nx, y1 + ny)
    ax.plot([x0, a[0]], [y0, a[1]], color=color, lw=0.6); ax.plot([x1, b[0]], [y1, b[1]], color=color, lw=0.6)
    ax.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle="<->", color=color, lw=0.8))
    ax.text((a[0] + b[0]) / 2 + nx * 0.6, (a[1] + b[1]) / 2 + ny * 0.6, text, ha="center", va="center", color=color, fontsize=8,
            rotation=np.degrees(np.arctan2(dy, dx)), bbox=dict(fc="white", ec="none", pad=1))

def note(ax, xy, xytext, text, color=INK, ha="left"):
    ax.annotate(text, xy=xy, xytext=xytext, fontsize=8.5, color=color, ha=ha, va="center",
                bbox=dict(fc="white", ec="none", alpha=0.85, pad=1.5),
                arrowprops=dict(arrowstyle="-", color=color, lw=0.7, shrinkA=0, shrinkB=2), zorder=10)

def title(ax, t, sub=None):
    ax.set_title(t, loc="left", fontsize=13, fontweight="bold", pad=14)
    if sub: ax.text(0, 1.0, sub, transform=ax.transAxes, fontsize=9, color="#555", va="bottom")

def camera(ax, x, y, w=9, h=12, pointing=1, z=6):
    ax.add_patch(Rectangle((x, y - h / 2), w, h, fc="#2e7d32", ec="#111", lw=0.6, zorder=z))   # board
    lx = x + w if pointing > 0 else x - 3
    ax.add_patch(Rectangle((lx, y - 3.5), 3, 7, fc="#111", ec="#333", lw=0.5, zorder=z))       # lens barrel
    return (lx + 3 if pointing > 0 else lx, y)

def save(f, name):
    f.savefig(f"{OUT}/diag_{name}.png", bbox_inches="tight", facecolor="white"); plt.close(f); print("wrote", name)

# 1 ------------------------------------------------------------ relay camera obscura
def relay():
    f, ax = fig(); D, H, T = 200, 200, 12; hy = H / 2
    hollow_box(ax, 0, 0, D, H, T, hole_y=hy)
    ax.add_patch(Rectangle((D - 3, 4), 3, H - 8, fc=PAPER, ec="none", zorder=4))                  # matte screen
    cone(ax, (0, hy), D - 3, 6, H - 6)
    pinhole_plate(ax, 0, hy)
    lens = camera(ax, 2, hy - 34)
    ax.add_patch(Polygon([lens, (D - 3, 4), (D - 3, H - 4)], fc=CAM, ec=CAM, lw=0.6, ls="--", alpha=0.18, zorder=2))
    ax.add_patch(Rectangle((2, 18), 30, 14, fc="#356", ec="#111", lw=0.5, zorder=6))               # Pi Zero
    ax.add_patch(Circle((D / 2, H + T + 6), 5, fc="#c33", ec="#111", lw=0.6, zorder=6))            # button
    ax.plot([D / 2, D / 2], [H + T, H + T + 2], color="#111", lw=1.5)
    ax.add_patch(Rectangle((D * 0.62, H + T), 62, 26, fc="#ddd", ec="#111", lw=0.6, zorder=6))     # receipt printer
    ax.add_patch(Rectangle((D * 0.62 + 66, H + T + 12), 34, 4, fc=PAPER, ec="#999", lw=0.4, zorder=6))
    ax.annotate("", xy=(-60, hy), xytext=(-T - 2, hy), arrowprops=dict(arrowstyle="<-", color="#c9a227", lw=1.2))
    ax.text(-62, hy + 6, "scene", ha="right", fontsize=8.5, color="#a58419")
    dim(ax, (0, -T - 6), (D, -T - 6), "200 mm", off=-14)
    dim(ax, (D + T + 6, 0), (D + T + 6, H), "200 mm", off=-14)
    note(ax, (0, hy), (-95, H + 30), "pinhole 0.63 mm, f/317\nswappable brass plate")
    note(ax, (lens[0] - 4, hy - 34), (-22, 45), "Pi camera, wide lens,\nbeside the hole, looks back\nat the screen (65° field)", ha="right")
    note(ax, (D - 1.5, H * 0.75), (D + 40, H * 0.75), "matte white screen\n250 x 200 mm\n(back wall)")
    note(ax, (D * 0.5, 30), (D + 40, 30), "interior flocked or\nflat black")
    note(ax, (D * 0.62 + 30, H + T + 26), (D * 0.62 + 30, H + T + 60), "receipt printer, prints\nevery frame, auto-cut")
    note(ax, (D / 2, H + T + 11), (D / 2 - 90, H + T + 55), "button: start exposure\n(seconds to minutes)")
    note(ax, (2, 25), (-22, -2), "Pi Zero 2 W", ha="right")
    ax.text(D * 0.5, H * 0.5, "pinhole image\nforms here", ha="center", va="center", fontsize=8, color="#7a5c00", zorder=9)
    ax.set_xlim(-175, D + 130); ax.set_ylim(-45, H + 95)
    title(ax, "1. Relay camera obscura", "side section; pinhole projects onto the back wall, a small camera photographs the projection")
    save(f, "01_relay")

# 2 ------------------------------------------------------------ wet plate pinhole
def wetplate():
    f, ax = fig(); D, H, T = 100, 102, 10; hy = H / 2
    hollow_box(ax, 0, 0, D, H, T, hole_y=hy, back_open=True)
    # plate holder: slot in the back wall, plate + dark slide
    ax.add_patch(Rectangle((D, -T), 14, H + 2 * T, fc="#6b5a3e", ec="#222", lw=0.8, zorder=3))      # holder body
    ax.add_patch(Rectangle((D + 3, -T + 4), 8, H + 2 * T - 8, fc="#222", ec="none", zorder=4))       # cavity
    ax.add_patch(Rectangle((D + 6, 2), 2.2, H - 4, fc="#bfe3ff", ec="#5aa", lw=0.5, zorder=5))       # glass plate
    ax.add_patch(Rectangle((D + 5, 2), 1, H - 4, fc="#e8e2c8", ec="none", zorder=6))                 # collodion side facing hole
    ax.add_patch(Rectangle((D + 3.2, H + T - 2), 2, 40, fc="#111", ec="#444", lw=0.5, zorder=7))    # dark slide pulled up
    ax.add_patch(Rectangle((D + 3, -T + 1), 8, 3, fc="#555", ec="none", zorder=5))                   # sump
    cone(ax, (0, hy), D + 5, 3, H - 3)
    pinhole_plate(ax, 0, hy)
    ax.add_patch(FancyBboxPatch((D * 0.3, 2), 28, 8, boxstyle="round,pad=0.5", fc="#d9c27a", ec="#111", lw=0.5, zorder=6))
    ax.annotate("", xy=(-55, hy), xytext=(-T - 2, hy), arrowprops=dict(arrowstyle="<-", color="#c9a227", lw=1.2))
    ax.text(-57, hy + 5, "scene, full sun", ha="right", fontsize=8.5, color="#a58419")
    dim(ax, (0, -T - 6), (D, -T - 6), "75 to 100 mm", off=-12)
    dim(ax, (D + 24, 2), (D + 24, H - 2), "4x5 plate", off=-12)
    note(ax, (0, hy), (-80, H + 26), "pinhole 0.45 mm, f/220\n(open to 0.8 mm for speed)")
    note(ax, (D + 5.5, H * 0.7), (D + 34, H + 12), "collodion side faces the hole\nplate loaded wet, ~5 min exposure")
    note(ax, (D + 4.2, H + T + 30), (D + 34, H + T + 30), "dark slide")
    note(ax, (D + 7, -T + 2), (D + 34, -14), "sump catches silver drips")
    note(ax, (D + 12, 20), (D + 34, 6), "holder: PETG/ASA print,\nno brass or steel")
    note(ax, (D * 0.3 + 14, 6), (-80, 12), "damp sponge keeps the\nplate from drying")
    ax.set_xlim(-130, D + 110); ax.set_ylim(-30, H + 60)
    title(ax, "2. Wet plate pinhole", "shallow box for speed; the plate must be poured, silvered, exposed and developed in ~15 minutes")
    save(f, "02_wetplate")

# 3 ------------------------------------------------------------ swappable back, exploded
def swappable():
    f, ax = fig(11, 5.5); H, T = 200, 12; hy = H / 2
    # front body 100
    x = 0; D1 = 100
    ax.add_patch(Rectangle((x, 0), D1, H, fc=INT, ec="none", zorder=1))
    wall(ax, x - T, -T, D1 + T, T); wall(ax, x - T, H, D1 + T, T)
    wall(ax, x - T, 0, T, hy - 2); wall(ax, x - T, hy + 2, T, H - hy - 2)
    pinhole_plate(ax, 0, hy); camera(ax, 2, hy - 34)
    ax.text(D1 / 2, -T - 12, "front body\nhole + camera\n100 mm", ha="center", va="top", fontsize=8.5)
    # spacer 100
    x = D1 + 25; D2 = 100
    ax.add_patch(Rectangle((x, 0), D2, H, fc=INT, ec="none", zorder=1))
    wall(ax, x, -T, D2, T); wall(ax, x, H, D2, T)
    ax.text(x + D2 / 2, -T - 12, "spacer\n+100 mm\n(digital mode only)", ha="center", va="top", fontsize=8.5)
    # back A: screen
    x = D1 + D2 + 50
    wall(ax, x, -T, T, H + 2 * T); ax.add_patch(Rectangle((x - 3, 4), 3, H - 8, fc=PAPER, ec="none", zorder=4))
    ax.text(x + T / 2, -T - 12, "back A\nmatte screen", ha="center", va="top", fontsize=8.5)
    # back B: plate holder
    x = D1 + D2 + 50 + 80
    ax.add_patch(Rectangle((x, -T), 14, H + 2 * T, fc="#6b5a3e", ec="#222", lw=0.8, zorder=3))
    ax.add_patch(Rectangle((x + 3, -T + 4), 8, H + 2 * T - 8, fc="#222", ec="none", zorder=4))
    ax.add_patch(Rectangle((x + 6, 40), 2.2, 120, fc="#bfe3ff", ec="#5aa", lw=0.5, zorder=5))
    ax.add_patch(Rectangle((x + 3.2, H + T - 2), 2, 30, fc="#111", ec="#444", lw=0.5, zorder=7))
    ax.text(x + 7, -T - 12, "back B\n4x5 / 5x7\nplate holder", ha="center", va="top", fontsize=8.5)
    for xa, xb in [(D1 + T / 2 + 2, D1 + 25 - 4), (D1 + D2 + 25 + 4, D1 + D2 + 50 - 4)]:
        ax.annotate("", xy=(xb, hy), xytext=(xa, hy), arrowprops=dict(arrowstyle="<->", color=DIM, lw=0.8))
    ax.text(D1 + D2 + 50 + 44, H + 30, "one of", ha="center", fontsize=8.5, color="#555")
    ax.annotate("", xy=(D1 + D2 + 50 + 80 - 2, H + 26), xytext=(D1 + D2 + 50 + 12, H + 26), arrowprops=dict(arrowstyle="<->", color=DIM, lw=0.8))
    ax.text(D1 / 2, H + 30, "digital: body + spacer + back A, f/317\nplate: body + back B, f/220", ha="left", va="bottom", fontsize=8.5, color="#333")
    ax.set_xlim(-30, D1 + D2 + 50 + 80 + 40); ax.set_ylim(-70, H + 70)
    title(ax, "3. One body, two backs", "exploded side view; the same pinhole plate and camera serve both modes")
    save(f, "03_swappable")

# 4 ------------------------------------------------------------ Pi HQ direct
def pihq():
    f, ax = fig(); s = 6  # scale: mm * s
    D, S = 5 * s, 6.17 * s
    ax.add_patch(Rectangle((0, -S / 2 - 3 * s), D + 2 * s, S + 6 * s, fc="#222", ec="none", zorder=1))   # cap interior
    wall(ax, -1.5 * s, -S / 2 - 4.5 * s, 1.5 * s, S / 2 + 4.5 * s - 0.3 * s); wall(ax, -1.5 * s, 0.3 * s, 1.5 * s, S / 2 + 4.5 * s - 0.3 * s)
    wall(ax, -1.5 * s, -S / 2 - 4.5 * s, D + 3.5 * s, 1.5 * s); wall(ax, -1.5 * s, S / 2 + 3 * s, D + 3.5 * s, 1.5 * s)
    ax.add_patch(Rectangle((D, -S / 2), 1.2 * s, S, fc="#3a6", ec="#111", lw=0.5, zorder=5))      # sensor
    ax.add_patch(Rectangle((D + 1.2 * s, -S / 2 - 3 * s), 1 * s, S + 6 * s, fc="#2e7d32", ec="#111", lw=0.5, zorder=4))  # PCB
    cone(ax, (0, 0), D, -S / 2, S / 2)
    pinhole_plate(ax, 0, 0, size=6 * s, t=0.6 * s)
    ax.plot([0, D], [0, S / 2], color="#7a5c00", lw=0.8, ls="--", zorder=6)
    ax.add_patch(Wedge((0, 0), 2.2 * s, 0, np.degrees(np.arctan2(S / 2, D)), fc="none", ec="#7a5c00", lw=0.8, zorder=6))
    ax.text(2.6 * s, 0.9 * s, "32°", fontsize=8, color="#7a5c00")
    dim(ax, (0, -S / 2 - 6 * s), (D, -S / 2 - 6 * s), "5 mm", off=-8)
    dim(ax, (D + 3.2 * s, -S / 2), (D + 3.2 * s, S / 2), "6.17 mm", off=-8)
    note(ax, (0, 0), (-16 * s, 7 * s), "pinhole 0.07 mm, f/70\nlaser-drilled disc in a\nprinted C-mount cap")
    note(ax, (D + 0.6 * s, S / 2 - 1), (D + 6 * s, 7 * s), "IMX477 sensor, lens removed\n~45 resolvable points across")
    note(ax, (D * 0.8, S / 2 * 0.8), (D + 6 * s, -6 * s), "corner rays 32° off axis:\nmicrolens vignetting and\ncolour shift at the edges")
    ax.annotate("", xy=(-9 * s, 0), xytext=(-2 * s, 0), arrowprops=dict(arrowstyle="<-", color="#c9a227", lw=1.2))
    ax.set_xlim(-18 * s, D + 20 * s); ax.set_ylim(-11 * s, 11 * s)
    title(ax, "4. Pi HQ camera, sensor directly behind the hole", "section, 6x scale; bright and live but a tiny format")
    save(f, "04_pihq")

# 5 ------------------------------------------------------------ body cap
def bodycap():
    f, ax = fig(); s = 2.5; FL, S = 18 * s, 24 * s   # flange distance, sensor height (24 mm)
    ax.add_patch(FancyBboxPatch((FL - 2, -S / 2 - 22 * s), 60 * s, S + 44 * s, boxstyle="round,pad=2", fc="#3c3c3c", ec="#111", lw=0.8, zorder=1))
    ax.add_patch(Rectangle((0, -S / 2 - 10 * s), FL - 2, S + 20 * s, fc="#181818", ec="none", zorder=2))   # mount throat
    ax.add_patch(Rectangle((-3 * s, -S / 2 - 12 * s), 3 * s, S + 24 * s, fc="#333", ec="#111", lw=0.8, zorder=3))  # body cap
    ax.add_patch(Rectangle((-3 * s, -1.5), 3 * s, 3, fc="#c9a227", ec="none", zorder=4))                    # pinhole shim
    ax.add_patch(Rectangle((-3 * s, -0.25), 3 * s, 0.5, fc=CONE, ec="none", zorder=5))
    ax.add_patch(Rectangle((FL, -S / 2), 1.5 * s, S, fc="#3a6", ec="#111", lw=0.5, zorder=5))               # sensor
    cone(ax, (0, 0), FL, -S / 2, S / 2, z=3)
    dim(ax, (0, -S / 2 - 16 * s), (FL, -S / 2 - 16 * s), "18 mm flange (Sony E)", off=-8)
    dim(ax, (FL + 4 * s, -S / 2), (FL + 4 * s, S / 2), "24 x 36 mm", off=-8)
    note(ax, (-1.5 * s, 0), (-30 * s, 20 * s), "body cap with 0.10 mm hole\nin brass shim, f/180")
    note(ax, (FL + 0.7 * s, S / 2 - 2), (FL + 64 * s, 26 * s), "full-frame sensor\n~180 resolvable points across\n1/6 s in sun at ISO 800")
    note(ax, (FL - 6, -S / 2 - 4), (FL + 64 * s, -24 * s), "clean the sensor first:\ndust is sharp at f/180")
    ax.annotate("", xy=(-14 * s, 0), xytext=(-4 * s, 0), arrowprops=dict(arrowstyle="<-", color="#c9a227", lw=1.2))
    ax.set_xlim(-34 * s, FL + 100 * s); ax.set_ylim(-36 * s, 36 * s)
    title(ax, "5. Full-frame body cap pinhole", "section; the best instrument, the least object")
    save(f, "05_bodycap")

# 6 ------------------------------------------------------------ sun trace recorder
def suntrace():
    f, ax = fig(); R = 40; c = (0, 0); Fd = 1.5 * R   # ball lens focus ~1.5 R from centre for n=1.5
    ax.add_patch(Circle(c, R, fc="#cfe8ff", ec="#5a8ab0", lw=1.2, alpha=0.85, zorder=5))
    ax.add_patch(Wedge(c, Fd + 6, 200, 340, width=6, fc="#f3eee2", ec="#222", lw=0.8, zorder=3))   # thermal strip (curved)
    ax.plot([-18, 18], [-Fd - 6, -Fd - 6], color="#222", lw=2)                                       # stand
    ax.plot([0, 0], [-Fd - 6, -R], color="#222", lw=1.2, zorder=2)
    for ang, col in [(35, "#f0b000"), (90, "#ffcc00"), (145, "#f0b000")]:
        a = np.radians(ang); dx, dy = np.cos(a), np.sin(a)
        for off in (-10, 0, 10):
            px, py = -dy * off, dx * off
            ax.plot([px + dx * 140, px + dx * R], [py + dy * 140, py + dy * R], color=col, lw=1.0, alpha=0.9, zorder=4)
            ax.plot([px + dx * R, -dx * Fd], [py + dy * R, -dy * Fd], color=col, lw=1.0, alpha=0.9, zorder=6)
        ax.add_patch(Circle((-dx * Fd, -dy * Fd), 3.2, fc="#3a2a1a", ec="none", zorder=7))
    ax.add_patch(Wedge(c, Fd + 3.5, 215, 325, width=2.5, fc="#3a2a1a", ec="none", zorder=7))
    ax.text(0, 150, "sun, morning to evening", ha="center", fontsize=9, color="#a58419")
    note(ax, (R * 0.7, R * 0.7), (70, 90), "glass sphere or short lens:\nthousands of suns at focus")
    note(ax, (-Fd - 4, -20), (-150, -40), "curved thermal paper strip,\ndevelops (not burns) along\nthe sun's path; gaps are clouds")
    note(ax, (0, -Fd - 6), (70, -80), "changed daily, like a\nCampbell-Stokes card")
    ax.set_xlim(-170, 170); ax.set_ylim(-95, 165)
    title(ax, "6. Sun-trace recorder on thermal paper", "the one subject bright enough for thermal paper; needs a lens, not a pinhole")
    save(f, "06_suntrace")

# 7 ------------------------------------------------------------ Dubroni in-camera processing
def dubroni():
    f, ax = fig(); D, H, T = 100, 110, 10; hy = H / 2
    hollow_box(ax, 0, 0, D, H, T, hole_y=hy)
    ax.add_patch(Rectangle((D - 22, -4), 22, H + 8, fc="#5a4630", ec="#222", lw=0.8, zorder=3))          # sealed chamber
    ax.add_patch(Rectangle((D - 19, 0), 16, H, fc="#0e0e0e", ec="none", zorder=4))
    ax.add_patch(Rectangle((D - 17, 3), 10, H - 6, fc="#8fb8d8", ec="#5aa", lw=0.5, alpha=0.5, zorder=4))  # glass lining
    ax.add_patch(Rectangle((D - 14, 4), 2.2, H - 8, fc="#bfe3ff", ec="#5aa", lw=0.5, zorder=5))           # plate
    ax.add_patch(Rectangle((D - 15, 4), 1, H - 8, fc="#e8e2c8", ec="none", zorder=6))
    ax.add_patch(Rectangle((D - 16.5, 4), 7, 14, fc="#7d6a3c", ec="none", alpha=0.9, zorder=5))           # liquid pool
    cone(ax, (0, hy), D - 15, 4, H - 4); pinhole_plate(ax, 0, hy)
    ax.add_patch(Rectangle((D - 13, H + T), 5, 18, fc="#888", ec="#111", lw=0.6, zorder=6))               # fill port
    ax.add_patch(Polygon([(D - 12.5, H + T + 18), (D - 8.5, H + T + 18), (D - 6, H + T + 48), (D - 15, H + T + 48)], fc="#ddd", ec="#111", lw=0.6, zorder=6))  # pipette
    ax.add_patch(Rectangle((D - 13, -T - 16), 5, 12, fc="#888", ec="#111", lw=0.6, zorder=6))             # drain
    ax.add_patch(Rectangle((D - 22, -T - 40), 24, 22, fc="#6a3a10", ec="#111", lw=0.6, alpha=0.8, zorder=6))
    ax.add_patch(Rectangle((-T, H * 0.15), T, 22, fc="#b22", ec="#111", lw=0.6, alpha=0.9, zorder=6))     # red window
    ax.annotate("", xy=(-55, hy), xytext=(-T - 2, hy), arrowprops=dict(arrowstyle="<-", color="#c9a227", lw=1.2))
    note(ax, (D - 10.5, H + T + 9), (D + 30, H + T + 30), "fill port: collodion, then silver,\nthen developer, by pipette")
    note(ax, (D - 10.5, -T - 10), (D + 30, -T - 30), "drain to waste bottle")
    note(ax, (D - 12, H * 0.5), (D + 30, H * 0.55), "glass-lined chamber\nholds the plate and\nthe chemistry")
    note(ax, (-T / 2, H * 0.15 + 11), (-100, H * 0.15 + 30), "red window to watch\ndevelopment")
    note(ax, (0, hy), (-100, H + 20), "pinhole, f/220")
    ax.text(D / 2, -T - 50, "Dubroni, 1864: the whole wet plate process inside the camera. No darkbox on location.", ha="center", fontsize=8.5, color="#333")
    ax.set_xlim(-135, D + 110); ax.set_ylim(-70, H + 75)
    title(ax, "7. In-camera wet plate processing", "section; a later prototype once the basic wet plate pinhole works")
    save(f, "07_dubroni")

# 8 ------------------------------------------------------------ show setup
def show():
    f, ax = fig(12, 5.5)
    ax.add_patch(Rectangle((0, 0), 400, 4, fc="#bbb", ec="none"))                                           # floor
    ax.add_patch(Rectangle((0, 4), 400, 240, fc="#f7f5f0", ec="none", zorder=0))                            # wall
    ax.add_patch(Rectangle((10, 60), 70, 120, fc="#d7ecff", ec="#333", lw=1.2, zorder=1))                   # window
    ax.plot([45, 45], [60, 180], color="#333", lw=1); ax.plot([10, 80], [120, 120], color="#333", lw=1)
    ax.add_patch(Circle((30, 155), 8, fc="#ffd24d", ec="none", zorder=2))
    ax.add_patch(Rectangle((120, 4), 60, 96, fc="#e8e6e0", ec="#333", lw=0.8, zorder=2))                    # plinth
    ax.add_patch(Rectangle((115, 100), 70, 56, fc="#5c4a36", ec="#222", lw=1, zorder=3))                    # box
    ax.add_patch(Circle((115, 128), 2.2, fc="#c9a227", ec="none", zorder=4))
    ax.add_patch(Rectangle((150, 156), 26, 10, fc="#ddd", ec="#222", lw=0.6, zorder=4))                     # printer
    ax.add_patch(Rectangle((178, 140), 3, 20, fc=PAPER, ec="#999", lw=0.4, zorder=4))                      # receipt hanging
    ax.annotate("", xy=(84, 128), xytext=(112, 128), arrowprops=dict(arrowstyle="<-", color="#c9a227", lw=1.2, ls="--"))
    ax.add_patch(Rectangle((205, 4), 6, 100, fc="#444", ec="none", zorder=2))                               # screen stand
    ax.add_patch(Rectangle((188, 104), 40, 30, fc="#111", ec="#222", lw=1, zorder=3))
    ax.add_patch(Rectangle((191, 107), 34, 24, fc="#3a4a5a", ec="none", zorder=4))
    for i, (x, w, col) in enumerate([(250, 34, "#2b4a86"), (292, 34, "#2b4a86"), (334, 34, "#2b4a86")]):    # cyanotypes
        ax.add_patch(Rectangle((x, 150), w, 44, fc="#fff", ec="#222", lw=1, zorder=3)); ax.add_patch(Rectangle((x + 4, 154), w - 8, 36, fc=col, ec="none", zorder=4))
    for x in (262, 304):                                                                                    # ambrotypes
        ax.add_patch(Rectangle((x, 90), 26, 32, fc="#111", ec="#333", lw=1, zorder=3)); ax.add_patch(Rectangle((x + 3, 93), 20, 26, fc="#5a5548", ec="none", zorder=4))
    ax.add_patch(Rectangle((250, 4), 130, 3, fc="#aaa", ec="none", zorder=2))
    ax.add_patch(Rectangle((340, 4), 50, 60, fc="#e8e6e0", ec="#333", lw=0.8, zorder=2))                    # wet plate table
    for k, col in enumerate(["#cfe8ff", "#d9d9d9", "#e8d8a0"]):
        ax.add_patch(Rectangle((344 + k * 15, 64), 11, 22, fc=col, ec="#333", lw=0.6, zorder=3))
    ax.add_patch(Rectangle((342, 86), 45, 3, fc="#333", ec="none", zorder=3))
    for k in range(4): ax.add_patch(Rectangle((345 + k * 10, 89), 6, 12, fc="#bfe3ff", ec="#5aa", lw=0.5, zorder=3))
    lab = lambda x, y, t: ax.text(x, y, t, ha="center", fontsize=8.5, color="#333")
    lab(45, 190, "window: the subject"); lab(150, 40, "relay box on plinth\nframe every few minutes"); lab(236, 140, "screen: last frame")
    lab(313, 200, "cyanotypes from digital negatives"); lab(288, 84, "ambrotypes from the plate back"); lab(365, 108, "wet plate station\ntanks, drying rack")
    lab(163, 178, "receipts, take one"); 
    ax.set_xlim(0, 400); ax.set_ylim(0, 215)
    title(ax, "8. Show layout", "elevation; the box faces the window, everything it makes hangs beside it")
    save(f, "08_show")

# 9 ------------------------------------------------------------ concave grating spectrograph box
def rowland():
    f, ax = fig(10, 6.5); R = 400; rc = R / 2
    # Rowland circle, drawn in box coordinates: grating vertex at origin, centre of curvature at (R, 0)
    th = np.linspace(0, 2 * np.pi, 400); ax.plot(rc - rc * np.cos(th), rc * np.sin(th), color="#bbb", lw=0.8, ls="--")
    # box: a shallow wedge holding grating, slit and detector
    ax.add_patch(Polygon([(-16, -60), (-16, 60), (330, 175), (430, 175), (430, -95), (330, -95)], closed=True, fc=INT, ec="#222", lw=0.8, zorder=1))
    wall(ax, -28, -70, 12, 140)                                           # grating mount
    yy = np.linspace(-40, 40, 60); ax.plot((yy ** 2) / (2 * R), yy, color="#c9a227", lw=4, zorder=5)
    for k in range(-38, 39, 4): ax.plot([(k ** 2) / (2 * R) - 1.5, (k ** 2) / (2 * R) + 1.5], [k, k], color="#7a5c00", lw=0.6, zorder=6)
    a = np.radians(40); S = (rc + rc * np.cos(a), rc * np.sin(a))        # slit at phi = 40 deg (alpha = 20 deg incidence)
    ax.add_patch(Rectangle((S[0] - 3, S[1] - 12), 6, 24, fc=WALL, ec="#222", lw=0.6, zorder=6))
    ax.plot([S[0] - 3, S[0] + 3], [S[1], S[1]], color=CONE, lw=2, zorder=7)
    phis = np.radians(np.linspace(-45, 35, 80)); ax.plot(rc + rc * np.cos(phis), rc * np.sin(phis), color=PAPER, lw=6, zorder=5)
    # rays: slit -> grating -> spectrum on the arc
    for y in (-30, 0, 30): ax.plot([S[0], (y ** 2) / (2 * R)], [S[1], y], color=CONE, lw=0.8, alpha=0.8, zorder=4)
    for wl, col in [(400, "#6a3df5"), (550, "#3ad33a"), (700, "#e02020")]:
        beta = np.arcsin(np.sin(np.radians(20)) - wl * 1e-3 / 2.0); phi = 2 * beta
        P = (rc + rc * np.cos(phi), rc * np.sin(phi))
        for y in (-30, 0, 30): ax.plot([(y ** 2) / (2 * R), P[0]], [y, P[1]], color=col, lw=0.8, alpha=0.9, zorder=4)
        ax.plot(P[0], P[1], "o", color=col, ms=5, zorder=8)
    lens = camera(ax, 300, 20, pointing=1)
    ax.add_patch(Polygon([lens, (rc + rc * np.cos(np.radians(-40)), rc * np.sin(np.radians(-40))), (rc + rc * np.cos(np.radians(30)), rc * np.sin(np.radians(30)))], fc=CAM, ec=CAM, ls="--", lw=0.5, alpha=0.15, zorder=2))
    ax.annotate("", xy=(S[0] + 22, S[1] + 62), xytext=(S[0] + 4, S[1] + 14), arrowprops=dict(arrowstyle="<-", color="#c9a227", lw=1.2))
    ax.text(S[0] + 26, S[1] + 66, "scene,\nthrough the slit", fontsize=8.5, color="#a58419", va="bottom", ha="center")
    note(ax, (2, 0), (-60, 120), "concave reflection grating\nR = 400 mm, 500 l/mm\n(grating film on a\nmakeup mirror)", ha="right")
    note(ax, (S[0], S[1] - 12), (S[0] - 40, -75), "0.5 mm slit on the\nRowland circle,\n20° off the normal")
    note(ax, (rc + rc * np.cos(np.radians(10)), rc * np.sin(np.radians(10))), (150, 200), "spectrum forms on the circle:\nred near the centre of\ncurvature, violet 60 mm along")
    note(ax, (lens[0], 20), (240, -60), "Pi camera photographs\nthe spectrum strip", ha="right")
    ax.text(rc, -130, "Rowland circle: diameter = mirror radius, tangent to the grating. Anything on it images to the circle, dispersed. No lens anywhere.",
            ha="center", fontsize=8.5, color="#333")
    ax.set_xlim(-140, 470); ax.set_ylim(-150, 250)
    title(ax, "9. Concave grating spectrograph in a box", "top view; the curved grating is both the lens and the prism (Rowland, 1882)")
    save(f, "09_rowland")

def sheet():
    names = ["01_relay", "02_wetplate", "03_swappable", "04_pihq", "05_bodycap", "06_suntrace", "07_dubroni", "08_show", "09_rowland"]
    ims = [Image.open(f"{OUT}/diag_{n}.png").convert("RGB") for n in names]
    cell = (900, 600); cols = 2; pad = 20; rows = (len(ims) + 1) // 2
    S = Image.new("RGB", (cols * (cell[0] + pad) + pad, rows * (cell[1] + pad) + pad), "white")
    for k, im in enumerate(ims):
        th = ImageOps.contain(im, cell); x = pad + (k % cols) * (cell[0] + pad); y = pad + (k // cols) * (cell[1] + pad)
        S.paste(th, (x, y))
    S.save(f"{OUT}/diagrams_sheet.png"); print("wrote diagrams_sheet.png")

if __name__ == "__main__":
    for fn in (relay, wetplate, swappable, pihq, bodycap, suntrace, dubroni, show, rowland): fn()
    sheet()
