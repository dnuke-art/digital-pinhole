"""Plot the FreeCAD Optics Workbench ray-trace results. python3 mockups/optics_plot.py out/optics_grating.json out/optics_rowland.json"""
import sys, json, math, os
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from looks3 import wl_rgb

def colour(wl): return tuple(np.clip(wl_rgb(np.array([float(wl)]))[0], 0, 1))

def plot_grating(data, path):
    fig, ax = plt.subplots(figsize=(9, 6.5), dpi=150)
    ax.add_patch(plt.Rectangle((-125, -100), 250, 200, fc="#f3eee2", ec="#333"))
    for r in data["rays"]:
        for x, y, z in r["hits"]:
            ax.plot(y, z, "o", ms=5 if r["order"] == 0 else 3.5, color="k" if r["order"] == 0 else colour(r["wl"]), mec="none", alpha=0.9)
    # analytic check for the on-axis ray, order 1: y = 200 tan(asin(lambda/d))
    for wl in (400, 550, 700):
        y = 200 * math.tan(math.asin(wl * 1e-3 / 2.0))
        ax.axvline(y, color=colour(wl), lw=0.6, ls="--"); ax.axvline(-y, color=colour(wl), lw=0.6, ls="--")
    ax.set_aspect("equal"); ax.set_xlim(-135, 135); ax.set_ylim(-110, 110)
    ax.set_xlabel("screen y, mm"); ax.set_ylabel("screen z, mm")
    ax.set_title("FreeCAD Optics Workbench: 500 l/mm film behind the pinhole, screen at 200 mm\n"
                 "black: zero order (the pinhole image); colours: first orders; dashed: analytic 400/550/700 nm", fontsize=9, loc="left")
    fig.savefig(path, bbox_inches="tight", facecolor="white"); plt.close(fig)

def plot_rowland(data, path):
    rc = 200.0
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6), dpi=150, gridspec_kw=dict(width_ratios=[1.15, 1]))
    # layout: Rowland circle, grating, slit, detector sector, spectrum hits
    th = np.linspace(0, 2 * np.pi, 400); ax1.plot(rc - rc * np.cos(th), rc * np.sin(th), color="#bbb", lw=0.8, ls="--")
    ax1.plot([0, 0], [-40, 40], color="#333", lw=4); ax1.text(12, 52, "concave grating\nR = 400 mm, 500 l/mm", ha="left", fontsize=8)
    sx, sy = data["meta"]["_slit"]; ax1.plot(sx, sy, "s", color="#c9a227", ms=8); ax1.text(sx + 8, sy, "slit", fontsize=8, va="center")
    phis = np.radians(np.linspace(-95, 35, 100)); ax1.plot(rc + rc * np.cos(phis), rc * np.sin(phis), color="#333", lw=3)
    ax1.text(250, -120, "detector arc on\nthe Rowland circle", fontsize=8)
    ax1.plot(400, 0, "+", color="#888"); ax1.text(392, 8, "centre of curvature", fontsize=7, color="#888")
    hits_all = []
    for r in data["rays"]:
        for x, y, z in r["hits"]:
            hits_all.append((r["wl"], r["order"], r["zs"], x, y, z))
            ax1.plot(x, y, "o" if r["order"] != 1 else "^", ms=3, color="k" if r["order"] == 0 else colour(r["wl"]), mec="none", alpha=0.7)
            if r["zs"] == 0 and r["zg"] == 0 and r["yg"] == 0:
                ax1.plot([sx, 0, x], [sy, 0, y], color="k" if r["order"] == 0 else colour(r["wl"]), lw=0.5, alpha=0.5)
    ax1.set_aspect("equal"); ax1.set_xlim(-60, 440); ax1.set_ylim(-215, 230)
    ax1.set_xlabel("x, mm"); ax1.set_ylabel("y, mm"); ax1.set_title("Rowland-circle spectrograph, top view", fontsize=10, loc="left")
    # detector view: arc position vs height
    for wl, order, zs, x, y, z in hits_all:
        s = rc * math.atan2(y, x - rc)                                               # arc length from the centre-of-curvature point
        ax2.plot(s, z, "o" if order != 1 else "^", ms=3.5, color="k" if order == 0 else colour(wl), mec="none", alpha=0.8)
    # analytic: sin(beta) = sin(20 deg) - lambda/d ; on the Rowland circle the focus sits at phi = 2*beta, s = rc * 2*beta
    for wl in (400, 550, 700):
        beta = math.asin(math.sin(math.radians(20)) - wl * 1e-3 / 2.0)
        ax2.axvline(-rc * 2 * beta, color=colour(wl), lw=0.6, ls="--")          # the addon's -1 order lands on the -s side
    ax2.set_xlim(-72, 14); ax2.set_ylim(-7, 7)
    ax2.text(-70, 6.2, "off this plot: specular (zero order) at -140 mm, +1 order at -230 to -308 mm", fontsize=7, color="#555")
    ax2.axhline(0, color="#ccc", lw=0.5); ax2.set_xlabel("position along the detector arc, mm (0 = centre of curvature)"); ax2.set_ylabel("height z, mm")
    ax2.set_title("What the detector sees: circles = order -1 (the spectrum), triangles = order +1, black = specular\ndashed: analytic grating equation; vertical spread of each line = astigmatism", fontsize=9, loc="left")
    fig.savefig(path, bbox_inches="tight", facecolor="white"); plt.close(fig)

if __name__ == "__main__":
    for p in sys.argv[1:]:
        d = json.load(open(p)); out = p.replace(".json", ".png")
        (plot_grating if d["scene"] == "grating" else plot_rowland)(d, out); print("wrote", out)
