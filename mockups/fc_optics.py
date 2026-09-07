"""Geometric ray trace of the grating ideas in FreeCAD's Optics Workbench, headless.
Run under freecadcmd (see Makefile 'optics' target):  SCENE=grating|rowland OUT_JSON=path freecadcmd mockups/fc_optics.py
Needs the OpticsWorkbench addon in ~/.local/share/FreeCAD/Mod.
"""
import os, sys, json, math
import FreeCAD, FreeCADGui
FreeCADGui.addCommand = lambda *a, **k: None            # the addon registers GUI commands at import; stub them
sys.path.append(os.path.expanduser("~/.local/share/FreeCAD/Mod/OpticsWorkbench"))
import Part
from FreeCAD import Vector, Rotation
import OpticalObject, Ray

_orig_redraw = Ray.RayWorker.redrawRay
def _headless_redraw(self, fp):                          # the addon colours fp.ViewObject at the end of redraw; there is none headless
    try: _orig_redraw(self, fp)
    except AttributeError as e:
        if "NoneType" not in str(e): raise
Ray.RayWorker.redrawRay = _headless_redraw

SCENE = os.environ.get("SCENE", "grating")
OUT_JSON = os.environ.get("OUT_JSON", f"/tmp/optics_{SCENE}.json")
WLS = [400, 450, 500, 550, 600, 650, 700]
doc = FreeCAD.newDocument("optics")
params = {}

def feature(name, shape):
    o = doc.addObject("Part::Feature", name); o.Shape = shape; return o

def absorber(base):
    fp = doc.addObject("Part::FeaturePython", "Absorber")
    OpticalObject.OpticalObjectWorker(fp, [base], type="absorber", collectStatistics=True, transparency=0, reflectionRate=0)
    return fp

def grating(base, lpm, gtype, lines_plane=Vector(0, 1, 0)):
    fp = doc.addObject("Part::FeaturePython", "Grating")
    OpticalObject.GratingWorker(fp, [base], RefractionIndex=1, material="", lpm=lpm, GratingType=gtype,
                                GratingLinesPlane=lines_plane, order=1, ray_order_override=False, collectStatistics=False)
    return fp

def ray(pos, direction, wl, order, **meta):
    fp = doc.addObject("Part::FeaturePython", "Ray")
    fp.Placement.Base = pos
    fp.Placement.Rotation = Rotation(Vector(1, 0, 0), direction)
    Ray.RayWorker(fp, True, False, 1, 1, 0.1, False, 3000, 12, wl, order, 360, [], None, Vector(0, 0, 100), "", 100.0, "isotropic", False, 0)
    params[fp.Name] = dict(wl=wl, order=order, **meta)
    return fp

def unit(a, b): v = b - a; return v / v.Length

if SCENE == "grating":
    # pinhole at the origin; 500 l/mm transmission film just behind it; screen 200 mm away, 250 x 200 mm
    screen = absorber(feature("Screen", Part.makeBox(2, 250, 200, Vector(200, -125, -100))))
    grating(feature("Film", Part.makeBox(0.5, 8, 8, Vector(1.0, -4, -4))), 500, "transmission - diffraction at 1st surface")
    for az in (-30, -15, 0, 15, 30):
        for el in (-15, 0, 15):
            d = Vector(math.cos(math.radians(el)) * math.cos(math.radians(az)),
                       math.cos(math.radians(el)) * math.sin(math.radians(az)), math.sin(math.radians(el)))
            for wl in WLS:
                for order in (-1, 0, 1):
                    ray(Vector(0, 0, 0), d, wl, order, az=az, el=el)

elif SCENE == "rowland":
    # concave reflection grating, R = 400 mm (f = 200), vertex at origin, concave side facing +x.
    R = 400.0; C = Vector(R, 0, 0)
    blank = Part.makeBox(20, 80, 80, Vector(-19, -40, -40)).cut(Part.makeSphere(R, C))
    grating(feature("ConcaveGrating", blank), 500, "reflection")
    # detector: annulus sector on the Rowland circle (radius R/2 about (R/2, 0, 0)). Polar angle phi is measured
    # about that centre from +x, so phi = 0 is the centre-of-curvature point and phi = 180 is the grating vertex.
    # The slit sits at phi = 2*alpha = 40 deg; the spectrum lands near phi = 0; specular (zero order) at phi = -40.
    rc = R / 2; centre = Vector(rc, 0, 0)
    sector = Part.makeCylinder(rc + 3, 60, Vector(rc, 0, -30), Vector(0, 0, 1), 130).cut(
             Part.makeCylinder(rc - 2, 60, Vector(rc, 0, -30), Vector(0, 0, 1), 130))
    sector.rotate(centre, Vector(0, 0, 1), -95)                  # phi from -95 to +35 deg
    absorber(feature("Detector", sector))
    # slit on the Rowland circle at 20 deg incidence: theta = 180 - 2*alpha = 140 deg
    th = math.radians(140); S = Vector(rc - rc * math.cos(th), rc * math.sin(th), 0)
    for zs in (-4, 0, 4):                                        # slit height 8 mm
        src = Vector(S.x, S.y, zs)
        for yg in (-12, -6, 0, 6, 12):                             # fan across the grating width
            for zg in (-8, 0, 8):
                d = unit(src, Vector(0, yg, zg))
                for wl in WLS:
                    ray(src, d, wl, -1, zs=zs, yg=yg, zg=zg)        # the addon's order sign: -1 diffracts back toward the normal
                if zs == 0 and zg == 0:
                    ray(src, d, 550, 0, zs=zs, yg=yg, zg=zg)        # zero order (specular) reference
                    for wl in (400, 700):
                        ray(src, d, wl, 1, zs=zs, yg=yg, zg=zg)     # +1 goes the other way, past the specular
    params["_slit"] = [S.x, S.y]

doc.recompute()
out = {"scene": SCENE, "rays": []}
absorbers = [o for o in doc.Objects if getattr(o, "OpticalType", "") == "absorber"]
for name, meta in params.items():
    if name.startswith("_"): continue
    hits = []
    for ab in absorbers:
        h = getattr(ab, "HitCoordsFrom" + doc.getObject(name).Label, None)
        if h: hits += [[v.x, v.y, v.z] for v in h]
    out["rays"].append(dict(name=name, hits=hits, **meta))
out["meta"] = {k: v for k, v in params.items() if k.startswith("_")}
json.dump(out, open(OUT_JSON, "w"))
n_hit = sum(1 for r in out["rays"] if r["hits"])
print(f"{SCENE}: {len(out['rays'])} rays, {n_hit} with detector hits -> {OUT_JSON}")
