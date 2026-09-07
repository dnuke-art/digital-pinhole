"""3D cutaway of the relay camera obscura. build123d parts -> STL -> OpenSCAD preview render.
python3 mockups/render3d.py -> mockups/out/render_relay_cutaway.png
"""
import os, subprocess
from build123d import *

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = f"{HERE}/out"; STL = f"{OUT}/stl"; os.makedirs(STL, exist_ok=True)

# interior: x = depth (hole at x=0, screen at x=D), y = width, z = height
D, W, H, T = 200, 250, 200, 12
HOLE = (0, W / 2, H / 2)

def slab(x, y, z, l, w, h):
    return Pos(x + l / 2, y + w / 2, z + h / 2) * Box(l, w, h)

parts = {}
# body: floor, back, far side (y=W), lid, front wall with hole. Near side wall (y<0) omitted = cutaway.
front = slab(-T, -T, -T, T, W + 2 * T, H + 2 * T) - Pos(-T / 2, W / 2, H / 2) * Rot(0, 90, 0) * Cylinder(2.0, T + 2)
body = slab(-T, -T, -T, D + 2 * T, W + 2 * T, T) + slab(D, -T, -T, T, W + 2 * T, H + 2 * T) \
     + slab(-T, W, -T, D + 2 * T, T, H + 2 * T) + front
CUT = W / 2 - 30                                    # section plane: keep y > CUT
keep = slab(-T - 1, CUT, -T - 1, D + 2 * T + 2, W, H + 2 * T + 2)
parts["body"] = body & keep
parts["lid"] = slab(-T, -T, H, D + 2 * T, W + 2 * T, T) & keep
parts["screen"] = slab(D - 3, 4, 4, 3, W - 8, H - 8) & keep
parts["plate"] = Pos(-T - 0.5, W / 2, H / 2) * Rot(0, 90, 0) * (Cylinder(16, 1.0) - Cylinder(0.6, 2))   # brass pinhole disc on the outside
cam_z = H / 2 - 34
parts["camera"] = slab(0, W / 2 - 12.5, cam_z - 12, 1.2, 25, 24) + Pos(4, W / 2, cam_z) * Rot(0, 90, 0) * Cylinder(4, 6)
parts["pi"] = slab(0, W / 2 - 20, 14, 1.5, 65, 30)
P = lambda x, y, z: Plane((x, y, z), x_dir=(0, 1, 0), z_dir=(1, 0, 0))
parts["cone"] = loft([P(0.5, W / 2, H / 2) * Rectangle(1.2, 1.2), P(D - 4, W / 2, H / 2) * Rectangle(W - 10, H - 10)]) & keep
parts["printer"] = slab(D * 0.55, W * 0.55, H + T, 90, 70, 42) + slab(D * 0.55 + 90, W * 0.55 + 10, H + T + 20, 40, 50, 1)
parts["button"] = Pos(D * 0.25, W * 0.75, H + T + 4) * Cylinder(7, 8)
parts["fov"] = loft([P(7, W / 2, cam_z) * Rectangle(2, 2), P(D - 4, W / 2, H / 2) * Rectangle(W - 10, H - 10)]) & keep

for name, p in parts.items():
    export_stl(p, f"{STL}/{name}.stl")

colors = {"body": ("#6b5a3e", 1.0), "lid": ("#6b5a3e", 0.3), "screen": ("#f3eee2", 1.0), "plate": ("#c9a227", 1.0), "camera": ("#2e7d32", 1.0),
          "pi": ("#335577", 1.0), "printer": ("#d0d0d0", 1.0), "button": ("#c33333", 1.0),
          "cone": ("#ffd66b", 0.22), "fov": ("#7fc8ff", 0.10)}
scad = "\n".join(f'color("{c}", {a}) import("{STL}/{n}.stl");' for n, (c, a) in colors.items())
# interior black: a thin dark skin on the visible inner faces
scad += f'\ncolor("#151515") translate([0.2,{W-0.8},0.2]) cube([{D-0.4},0.6,{H-0.4}]);'
scad += f'\ncolor("#151515") translate([0.2,{CUT},0.2]) cube([{D-0.4},{W-CUT-0.4},0.6]);'
scad += f'\ncolor("#1a1a1a") translate([0.2,{CUT},0.2]) cube([0.6,{W-CUT-0.4},{H-0.4}]);'
open(f"{OUT}/relay.scad", "w").write(scad)
cx, cy, cz = D / 2, W / 2, H / 2
cmd = ["openscad", "-o", f"{OUT}/render_relay_cutaway.png", "--imgsize=1800,1200", "--projection=p",
       f"--camera={cx+90},{cy-820},{cz+470},{cx},{cy-10},{cz+10}", "--colorscheme=Cornfield", f"{OUT}/relay.scad"]
env = dict(os.environ, LC_ALL="C")
r = subprocess.run(cmd, capture_output=True, text=True, env=env)
print(r.returncode, (r.stderr or "")[-600:])
