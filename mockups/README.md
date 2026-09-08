# Mockups

Plain Python generators (numpy, Pillow, matplotlib, scipy) plus a 3D
section of the relay box (build123d + OpenSCAD). From the repo root:

    make            # everything, about half a minute
    make deps       # check what is installed
    make looks | diagrams | experiments | gratings | render
    make photos     # fetch the sample photos (done automatically when needed)
    make clean      # remove generated images

Or run a generator directly:

    python3 mockups/looks.py       # simulated output images -> out/look_*.png, looks_sheet.png
    python3 mockups/diagrams.py    # cross-section diagrams  -> out/diag_*.png, diagrams_sheet.png
    python3 mockups/render3d.py    # 3D cutaway render        -> out/render_relay_cutaway.png
    python3 mockups/looks2.py      # aperture experiments + dither styles -> out/look2_*.png, dither_*.png, experiments_sheet.png, dither_sheet.png
    python3 mockups/looks3.py      # gratings and zone plate -> out/look3_*.png, grating_sheet.png
    python3 mockups/looks4.py      # curved gratings -> out/look4_*.png, curved_grating_sheet.png
    make optics                    # FreeCAD Optics Workbench ray traces -> out/optics_*.png (needs freecadcmd + addon)

Sample photos in `src/` are from picsum.photos (Unsplash) and are only here
as stand-ins for the simulations.

## Output looks (`out/look_*.png`)

Simulations of what each approach's picture looks like, all from the same
source photo so they compare directly. Sheet: `out/looks_sheet.png`.

| File | Approach | What is simulated |
|---|---|---|
| look_01_relay_digital | relay camera obscura | ~200 points across, cos^4 falloff over a 65° field, flare, long-exposure noise |
| look_02_fullframe_bodycap | full-frame body cap | ~180 points, 90° field falloff |
| look_03_pi_hq_direct | Pi HQ, lens off | ~45 points, steep-ray vignetting and magenta corner shift |
| look_04_receipt | receipt printer | relay frame at 384 dots, Floyd-Steinberg, 58 mm paper with caption |
| look_05_cyanotype | cyanotype from digital negative | Prussian blue on cream paper, brushed coating edge, uneven coat |
| look_06_collodion_landscape | wet plate pinhole, ambrotype | blue/UV-only response (white sky, dark foliage), ~110 points, pour marks, black backing |
| look_07_collodion_portrait | wet plate pinhole, portrait | red lips go black, skin goes luminous |
| look_08_solargraph | solargraphy | months of nested sun arcs, inverted paper-negative tones |
| look_09_sun_trace | sun-trace recorder | thermal strip with a burnt daily arc broken by clouds |
| look_10_heliograph | bitumen heliograph | pewter plate, only highlights harden, very low contrast |

The simulations are optics-first (resolution, falloff, spectral response)
with the surface character (pour marks, paper grain, dither) added on top.
They are for judging the look, not for exposure planning.

## Aperture experiments (`out/look2_*.png`, sheet `experiments_sheet.png`)

Single slit, double slit in daylight, double slit with real fringes on the
Pi sensor, crossed slits (anamorphic), five-hole X, moire from a lined
screen, star-shaped hole at night, zone plate, MURA coded aperture (mask,
raw, decoded), red/cyan two-hole anaglyph, slit-scan receipt strip.
Physics in [docs/08](../docs/08-apertures-and-dither.md).

## Gratings (`out/look3_*.png`, sheet `grating_sheet.png`)

Linear grating over the pinhole at night and in daylight, the zone plate
pattern, the zone plate as captured in white light, and the digital fix
(halo subtraction, luminance from green). Physics in [docs/09](../docs/09-diffraction-grating.md).

## Curved gratings (`out/look4_*.png`, sheet `curved_grating_sheet.png`)

Concave grating spectrograph in daylight (slit through the castle) and at
night (lamp fingerprints), and the circular constant-pitch aperture with
rainbow rings. Physics in [docs/10](../docs/10-curved-grating.md).

## FreeCAD ray traces (`out/optics_*.png`)

`fc_optics.py` runs under FreeCAD's own python (the AppImage in `/opt`,
`freecadcmd` entry point, offscreen Qt) with the OpticsWorkbench addon and writes hit
coordinates to JSON and saves the FreeCAD document (`optics_*.FCStd`, open
it in FreeCAD with the addon installed to see the rays); `optics_plot.py` plots the hits. Two scenes: a 500 l/mm
film behind the pinhole, and the Rowland concave-grating spectrograph.
`make optics` builds both. Not in `make all` because it needs FreeCAD;
`make deps` reports whether the AppImage and the addon are available.
Override with `make optics FREECADCMD="path/to/freecadcmd"`.

## Dither styles (`out/dither_*.png`, sheet `dither_sheet.png`)

The relay frame rendered as Floyd-Steinberg, Atkinson, Bayer 4x4 and 8x8,
45-degree halftone, line screen, Game Boy Camera (128x112, four greens),
CGA palette 1, and 1-bit at 96 px.

## Diagrams (`out/diag_*.png`)

Cross sections in millimetres. Sheet: `out/diagrams_sheet.png`.

1. Relay camera obscura, side section
2. Wet plate pinhole, shallow box with plate holder
3. One body, two backs, exploded
4. Pi HQ camera with the sensor directly behind the hole, 6x scale
5. Full-frame body cap
6. Sun-trace recorder on thermal paper
7. Dubroni-style in-camera wet plate processing
8. Show layout, elevation

## 3D (`out/render_relay_cutaway.png`)

The relay box with the near side wall removed: pinhole plate, camera beside
the hole, Pi, matte screen, light cone, receipt printer on the lid. Built in
build123d so the same file can grow into the real part model.
