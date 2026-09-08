# Printed cameras and lenses, 110 cartridges, instant film

Notes from a conversation about a half-remembered 3D printed camera, which
turned out to be Amos Dudley's SLO, and where it led: printed lenses, the
110 cartridge as a ready-made film transport, and instant film as both a
capture medium and a digital output. Ideas are summarised in
[IDEAS.md](../IDEAS.md); this is the detail.

## The SLO, and other printed cameras

The camera was the SLO (2016): a 35 mm camera printed entirely on a Form 2,
including its lens, iris and leaf shutter. The download in `~/Downloads`
is 34 STLs plus six PreForm `.form` files, no editable source. The lens was
printed in clear resin, then wet-sanded through the grits and polished.

Other printed cameras that ship as exported geometry only, for reference:

| Project | Format | Files |
|---|---|---|
| Amos Dudley, SLO | 35 mm, printed lens | STL + PreForm |
| Dora Goodman, Goodman One / Zone (GoodLAB) | 120, uses real lenses | STL + STP, free after sign-up |
| Velvia, Open 6x12 / 6x17 / 6x24 | 120 panoramic | STEP on Printables |
| OpenReflex (Léo Marius) | 35 mm SLR | STL |
| terraPin, P6*6 (schlem) | 120 pinhole | OpenSCAD source |

## Printed lenses

Dan has printed lenses since seeing the SLO, smoothing them by dipping in
clear resin and with spray lacquer. Notes on what governs the result:

- **Surface, not figure, is the usual limit.** Layer lines scatter light
  into haze. A dip coat fills them by surface tension and cures to a
  glass-like skin; it adds 0.1 to 0.3 mm of material and a meniscus at the
  edge. Lacquer is thinner but orange-peels and can craze resin.
- **Gravity makes a wedge.** A dipped lens left to cure hanging drains
  toward one edge. Rotating it slowly under the UV lamp while it cures
  keeps the coat even. Old trick from resin coating, cheap to rig with a
  small motor.
- **Droplet lens.** Skip printing the optical surface at all: a measured
  drop of clear UV resin on a printed ring forms a spherical cap by surface
  tension and cures in place. The print is the holder; the liquid makes the
  surface. Focal length follows drop volume, so it is repeatable, and there
  is nothing to sand. Same idea as the PDMS droplet microscope lenses.
- **A singlet is soft wide open.** Spherical aberration dominates at f/4;
  by f/8 a decent singlet resolves a few hundred points across a small
  frame. Chromatic aberration is fixed by the resin (Abbe number around
  40 to 50), and shows as colour fringes at edges.
- **Pinhole standards are generous.** A lens with a millimetre of blur on
  the relay screen is ten times sharper than the pinhole and hundreds of
  times brighter. On a 110 frame even a rough singlet beats the hole.

### The relay box as a lens test rig

Swap the pinhole plate for a printed lens plate and the box becomes a live
camera obscura: at f/4 to f/8 it is ten to twelve stops brighter than the
f/317 hole, so the Pi camera shows the screen in real time. Judge a lens in
seconds, compare two prints side by side, watch the focus as the plate
slides. This is the fastest feedback loop available for printed optics and
costs one extra plate. Pinhole mode stays slow; lens mode is live.

Lens plus Pi needs no shutter, because the sensor has one. Lens plus film
does: at f/8 and ISO 200 in sun the exposure is 1/800 s, which a sliding
cover cannot do. That is the reason the SLO needed a printed leaf shutter,
and the reason the 110 box below stays a pinhole.

## The 110 cartridge camera

The cartridge does everything a camera body usually does:

- **Film gate.** The frame window (13 x 17 mm) is in the cartridge; the
  film plane sits about a millimetre behind its face.
- **Transport.** Supply and take-up spools are inside; the camera turns the
  take-up hub with a thumbwheel or gear.
- **Pressure plate.** Moulded into the cartridge. Film flatness is famously
  poor in 110, which a pinhole does not care about.
- **Frame counter.** Printed on the backing paper, read through a small
  window in the camera back. One perforation per frame lets a pin stop the
  wind on better cameras; reading the numbers is enough here.

So the camera is a light-tight printed box with a hole in front of the
window, a thumbwheel, a sliding shutter and a peephole. No darkroom
loading; a bad print is a light leak rather than a jam. bergytone's 110
film pinhole camera on Thingiverse is an existing design (0.18 mm hole,
two-piece body, gear assembly) to start from or check against.

| Quantity | Value |
|---|---|
| Frame | 13 x 17 mm, 24 frames per cartridge |
| Hole about 25 mm from the film | 0.22 mm optimum, f/113 |
| Resolvable points across the frame | ~40 |
| Lomography Tiger 200 in full sun | ~1/4 s |
| Indoors | tens of seconds to minutes |

Soft, in the way the small-sensor Pi camera is soft, because the format is
small. That is the price of the convenience.

Film: Lomography makes 110 in black and white (Orca), colour (Tiger),
redscale (Lobster), slide (Peacock) and Metropolis. Developing: standard
reels do not take 16 mm film, but thinbegin's Pa-110 reel on Printables is
a free Paterson-fit design that holds a full cartridge, so the chain is
printed camera, caffenol, printed reel, all at home. The natural hand-out
camera for the show.

Design points if building one: make the pinhole plate the same swappable
part as the relay box's; keep the cartridge cavity a snug print with a
foam-backed door for light seal; the thumbwheel needs a ratchet or friction
so the film does not back-wind; put a red or opaque flip cover over the
counter window.

## Instant film

### Peel-apart pack film

Polaroid stopped in 2008 and Fujifilm's FP-100C in 2016; expired stock is
expensive and unreliable. The one current maker is Supersense in Vienna:
One Instant, hand-made Type 100 pack film in colour, black and white and
"Choco", sold in three-shot packs, plus a DIY kit since November 2023 where
the packs are assembled by hand for less per frame. A black and white
positive-negative version is a June 2026 limited edition with lead times of
about two months. Speed is around ISO 100.

| Quantity | Value |
|---|---|
| Pinhole at f/200 in full sun | ~1.6 s |
| Indoors | minutes, and instant chemistry loses reciprocity past a few seconds |

Mechanics: peel-apart needs two rollers that burst the pod and spread the
reagent as the tab is pulled. Roller gap and pressure are the one part not
worth printing. Either print a pinhole body that accepts a Polaroid 405
back, which carries its own rollers, or drill a hole in the lens board of a
Land camera.

Why it fits: the positive-negative stock gives a real 3.25 x 4.25 inch
negative. Contact print it and the cyanotype hangs beside the instant
positive, both from one press of the shutter, both hand-made. The wet
negative pressed onto watercolour paper is the classic image transfer, a
third print from the same shot.

### Home-made peel-apart: diffusion transfer

The chemistry behind pack film is diffusion transfer, and people make it
at home. Expose an ordinary paper negative, sandwich it face to face with a
receiver sheet with a developer paste between, wait five minutes in the
dark, peel: a positive on the receiver and a negative to fix. The Photrio
thread "Diffusion Transfer Printing recipes" is the working lab notebook,
covering receiver nucleation layers and thiosulphate/phenol pastes. It is
not instant in the camera, since the negative is shot separately and the
sandwich assembled in the dark, but it is a positive and a negative from
one paper exposure with kitchen-grade chemistry, and it belongs with the
caffenol and cyanotype work in [06](06-diy-chemistry.md). The Supersense
DIY kit is the packaged form of the same idea.

### Instax

Integral film, cheap and everywhere, ISO 800. The rollers live in the
camera, but Jollylook sells hand-crank Instax backs and printed pinhole
bodies exist. A pinhole at f/150 needs about 1/9 s in sun, and the print
appears in 90 seconds in front of whoever pressed the shutter. The
practical instant camera for the show.

### Instax as a digital output

The Instax Link printers (Mini, Square, Wide) take images over Bluetooth,
and the open-source InstaxBLE library drives them from a Pi in Python. The
Wide Link prints 800 x 1260 pixels, far beyond the pinhole's ~200 real
points. So the relay box can hand out an instant photograph beside the
receipt, with no chemistry on site. This joins the receipt printer and the
cyanotype negative as the third output of the digital box.

## Where this leaves the build list

- Relay box: add a lens plate (live mode) and an Instax Link (instant
  output) to the pinhole plate, receipt printer and cyanotype negative.
- 110 pinhole box: the hand-out camera; printed reel for home developing.
- Instax pinhole: the other hand-out camera, prints on the spot.
- Peel-apart: a 405-back pinhole body if One Instant POS/NEG is in stock;
  otherwise the diffusion-transfer experiment from paper negatives.
- Printed lenses: droplet lens and spin-cured dip, judged live on the
  relay box.
