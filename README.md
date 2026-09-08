# Digital Pinhole

Notes toward a digital pinhole camera, started while showing analog pinhole
work at an art show (September 2026). The question was simple: can a pinhole
camera be built with a digital sensing element, and what does it look like?

Short answer: yes, three ways, and the interesting one is a camera obscura
with a small camera inside looking back at the projection.

Loose ideas go in [IDEAS.md](IDEAS.md); the ones that grow get a numbered note below.
Pictures of all of it are in [mockups/](mockups/README.md): simulated output looks, cross-section diagrams, a 3D cutaway. `make` regenerates them.

## Documents

| File | What it covers |
|---|---|
| [docs/01-approaches.md](docs/01-approaches.md) | The three viable designs and how they compare |
| [docs/02-pinhole-physics.md](docs/02-pinhole-physics.md) | Hole sizing, diffraction, resolution vs format, exposure |
| [docs/03-scanner-camera.md](docs/03-scanner-camera.md) | Flatbed scanner as sensor: why it works with a lens and not a pinhole |
| [docs/04-relay-camera-obscura.md](docs/04-relay-camera-obscura.md) | The chosen direction: pinhole box with a relay camera inside |
| [docs/05-thermal-paper.md](docs/05-thermal-paper.md) | Thermal paper: why it cannot be film, sun-trace recorder, receipt printer as output |
| [docs/06-diy-chemistry.md](docs/06-diy-chemistry.md) | DIY chemistry: cyanotype as print side, caffenol, hand-coated emulsion, solargraphy, no-fixer processes |
| [docs/07-wet-plate-pinhole.md](docs/07-wet-plate-pinhole.md) | Wet plate collodion through a pinhole: the wet-window clock, exposure, plate back, chemistry, day-one plan |
| [docs/08-apertures-and-dither.md](docs/08-apertures-and-dither.md) | Slits, shaped holes, zone plate, coded aperture, anaglyph holes, slit-scan, where moire really comes from, dither catalogue |
| [docs/09-diffraction-grating.md](docs/09-diffraction-grating.md) | Grating as lens: linear grating disperses (night spectra), zone plate focuses; numbers, chromatic behaviour, digital deconvolution, how to make one |
| [docs/10-curved-grating.md](docs/10-curved-grating.md) | Curved grating: the Rowland concave-grating spectrograph box, rainbow-ring aperture, FreeCAD Optics Workbench ray traces and what they can and cannot simulate |
| [docs/11-printed-lenses-110-and-instant.md](docs/11-printed-lenses-110-and-instant.md) | The SLO and printed lenses (dip, spin-cure, droplet lens, the relay box as test rig), the 110 cartridge camera, peel-apart and Instax, home-made diffusion transfer, Instax Link as digital output |

## Where this is headed

A wooden or printed box, a pinhole plate on the front, a matte white screen on
the back wall, and a Raspberry Pi camera mounted beside the hole photographing
the screen with multi-minute exposures. It is a slow camera on purpose. The
box is the sculpture and the screen beside it shows what the box has seen.

Next steps once a box size is chosen:

- [x] Mockups: simulated looks, cross-section diagrams, 3D cutaway (mockups/)
- [x] FreeCAD Optics Workbench ray traces of the grating ideas (make optics)
- [ ] Pick box depth and screen size (sets hole diameter and field of view)
- [ ] Decide on a swappable back: screen + camera vs plate holder
- [ ] build123d model of the box, pinhole plate, and camera mount
- [ ] Capture script: long exposure on button press, optional frame stacking
- [ ] Display: e-ink or small monitor next to the prints
- [ ] Receipt printer output: ESC/POS over USB, dither pipeline, auto-cutter
- [ ] Digital negative pipeline: invert, curve, print transparency, cyanotype contact print
- [ ] Wet plate: kit, six 4x5 plates, silver-proof holder, one sunny afternoon
- [ ] Lens plate for the relay box (live mode) and Instax Link output
- [ ] 110 pinhole box and a printed Pa-110 developing reel
