# Curving the grating

Asked: what if the diffraction grating is curved? And can this be simulated
in FreeCAD's Optics Workbench?

Curving is the one move that turns a grating into a real imaging element,
and it is how the first lensless spectrographs worked. It only matters when
the grating is large. Mockups: `mockups/out/look4_*.png` (sheet
`curved_grating_sheet.png`), diagram `diag_09_rowland.png`, and two ray
traces from FreeCAD, `optics_grating.png` and `optics_rowland.png`.

## Three different things "curved grating" can mean

1. **Bending the film at the pinhole.** Does nothing. The hole samples a
   patch a fraction of a millimetre across; curvature over that patch is
   invisible. A film wrapped around the hole as a cylinder makes every ray
   hit at normal incidence, which slightly straightens the off-axis
   "smile" of the spectra, and that is all.
2. **Curving the lines.** Constant-pitch concentric rings are a diffractive
   axicon: every wavelength is thrown outward by the same angle, so a point
   light becomes a disc inside a rainbow ring. Rings whose pitch shrinks
   outward are the zone plate (see [09-diffraction-grating.md](09-diffraction-grating.md)).
3. **Curving the surface, big, and using it as the mirror.** A reflection
   grating ruled on a concave spherical mirror focuses and disperses at
   once: Rowland's concave grating, 1882. The mirror is the lens, the
   rulings are the prism, no other optic anywhere. This is the real answer.

## The concave grating spectrograph

Geometry: mirror radius R, grating at its vertex. Draw a circle of diameter
R tangent to the grating (the Rowland circle). A slit anywhere on that
circle is imaged, dispersed, back onto the circle. Each wavelength lands at
its own point; the detector is an arc of the circle.

For the box: R = 400 mm (f = 200), 500 lines/mm, slit 20 degrees off the
normal on the circle. Positions along the arc from the centre of curvature:

| Wavelength | Diffraction angle | Arc position |
|---|---|---|
| 700 nm | -0.5° | 3 mm |
| 550 nm | 3.8° | 27 mm |
| 400 nm | 8.2° | 57 mm |

Sixty millimetres of spectrum. Spectral resolution is set by the slit:
about 0.1 mm per nanometre at this dispersion, so a 0.5 mm slit resolves
roughly 5 nm, enough to tell a sodium lamp from an LED from neon at a
glance. Each point along the slit's height writes its own horizontal
spectrum, so the picture is position-along-the-slit versus wavelength.

What it makes:

- **Daylight.** Aim the slit through the scene; the image is the scene's
  colour, spread out. Sky is a broad blue ramp, a sunlit wall is a
  continuum, foliage dips in the red.
- **Night.** Every streetlight writes its fingerprint: sodium a yellow
  pair of lines, white LED a blue spike plus a yellow hump, neon a comb of
  red lines, mercury three sharp lines, incandescent a smooth ramp rising to
  red, a laser pointer one line. Mockup: `look4_02_spectrograph_night`.
- **Over time.** Combine with the slit-scan idea: one printed row per
  interval, and the receipt roll becomes the spectrum of the day. In 1-bit
  it prints as a barcode that changes with the weather.

DIY concave grating: a flexible 500 l/mm film grating laminated onto a
concave makeup mirror. The light passes the film twice (in and out) with
the mirror between, so it disperses roughly twice as hard as a single pass
and loses some efficiency, but it works; DIY spectroscope builders do it.
A 2x to 3x makeup mirror has a focal length around 125 to 250 mm. Proper
concave holographic gratings are a few hundred dollars from Edmund or
Thorlabs.

## Ray-traced in FreeCAD

FreeCAD's Optics Workbench addon (chbergmann/OpticsWorkbench) is a
geometric ray tracer: reflection, refraction, absorbers, and diffraction
gratings via the grating equation. It runs headless under FreeCAD's own
python once two GUI hooks are stubbed: the AppImage in `/opt` run through
its `freecadcmd` entry point with `QT_QPA_PLATFORM=offscreen` (without the
offscreen setting it waits for a display; with `--console` instead of
`freecadcmd` it finishes the script and then sits in an interactive prompt). The script is `mockups/fc_optics.py`,
the plotter `mockups/optics_plot.py`, target `make optics`. The addon lives
in `~/.local/share/FreeCAD/Mod/OpticsWorkbench`. The script also saves the
FreeCAD documents (`mockups/out/optics_*.FCStd`), which open in the GUI with
the addon installed and show the rays, grating and detector.

**Linear grating behind the pinhole** (`optics_grating.png`): 315 rays,
15 scene directions, 7 wavelengths, orders -1, 0, +1, onto the 250 x 200 mm
screen. The traced first-order positions match `200 tan(asin(lambda / d))`
to 0.5 percent (the film sits 1 mm behind the hole, which accounts for the
difference). Off-axis rows show the spectra curving into a "smile", which
is conical diffraction and is real.

**Rowland spectrograph** (`optics_rowland.png`): 330 rays from three
heights on the slit, fanned across 24 mm of grating width and 16 mm of
height. Results:

| Wavelength | Traced arc position | Spread across the fan | Vertical spread (slit point at z = 0) |
|---|---|---|---|
| 400 nm | 57.2 mm | 0.14 mm | ±1.2 mm |
| 550 nm | 26.9 mm | 0.13 mm | ±1.1 mm |
| 700 nm | 3.3 mm | 0.15 mm | ±1.0 mm |

So the tangential focus on the Rowland circle is essentially perfect (a
tenth of a millimetre from a 24 mm fan), the positions match the grating
equation, and the vertical direction is not focused: a point on the slit
smears to about 2 mm tall. That is the classic astigmatism of the concave
grating, and it is harmless here because the slit is a line anyway. A slit
point 4 mm up images 4 mm down, inverted 1:1. The zero-order (specular)
rays land at the mirror-image angle, 140 mm along the arc the other way,
and the +1 order goes further still, past the specular.

One convention to know: the addon's order sign is such that -1 diffracts
back toward the grating normal from a slit at +20 degrees. Trace both and
use the one that lands where you want.

## What the workbench can and cannot simulate

| Idea | Optics Workbench | Notes |
|---|---|---|
| Pinhole geometry, field of view, vignetting | yes | geometric; no diffraction blur |
| Relay camera field, anaglyph holes, crossed slits | yes | geometric |
| Linear grating over the hole, spectra positions | yes | grating equation, any order |
| Concave grating spectrograph, Rowland focus, astigmatism | yes | shown above |
| Fresnel lens / any refractive optic in the box | yes | Snell's law, Sellmeier materials |
| Zone plate | no | needs radially varying pitch and diffraction efficiency |
| Double-slit fringes, coded aperture, moire | no | wave optics or image processing, not ray tracing |
| Pinhole sharpness vs hole size | no | diffraction; use the formulas in [02](02-pinhole-physics.md) |

Where it earns its place: laying out the Rowland box (slit, grating and
detector all on one circle inside a wedge-shaped box), checking that the
Pi camera's field covers the spectrum strip, and sizing the film grating
on the makeup mirror. For everything wave-shaped the numpy mockups are the
right tool.

## Build idea

Diagram: `diag_09_rowland.png`. A shallow wedge box. Makeup mirror with
grating film at the narrow end. Slit and a curved white strip on the
Rowland circle at the wide end, the strip covering about 60 mm of arc.
Pi camera on the wide end looking at the strip. Same Pi, same printer,
same software as the relay box: this is the second head for it.
