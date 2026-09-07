# Wet plate pinhole

Collodion is the one hand-coated process fast enough to expose through a
pinhole. The combination has a hard constraint the digital box does not: the
plate must be poured, sensitized, exposed, and developed before it dries,
roughly ten to fifteen minutes end to end. Everything below follows from
that clock.

## The clock

| Step | Time | Notes |
|---|---|---|
| Pour and set | ~1 min | Tacky gel, looks dry, is not |
| Silver bath | 3 to 5 min | In the dark or under red light |
| Load, walk to camera, uncap | 1 to 2 min | Holder must be light tight and silver proof |
| Exposure | budget | Whatever is left |
| Develop | 15 to 30 s | Iron sulfate, pour on, rock, stop with water |
| Fix, rinse | 2 to 5 min | Hypo; can be in daylight |

On a warm dry day the exposure budget is about five to eight minutes. On a
cool humid day it stretches to fifteen. Once the collodion dries it stops
being sensitive, and a plate that dries mid-exposure develops with a hard
edge where the wet front stopped.

## Exposure through a pinhole

Collodion is about ISO 0.5 to 1 in visible light and only responds to blue
and UV. Two things help the pinhole case:

- **Pinholes pass UV.** Glass lenses absorb much of it. Collodion through a
  pinhole is somewhat faster relative to a lens camera than the visible-ISO
  arithmetic suggests. Treat the numbers below as pessimistic.
- **Shallow boxes are fast.** The f-number falls with depth (see
  [02-pinhole-physics.md](02-pinhole-physics.md)). A plate camera wants a
  shallower box than the digital one.

| Plate | Depth | Optimum hole | f-number | Full sun, ISO 0.5 | Open shade |
|---|---|---|---|---|---|
| 4x5 | 75 mm | 0.39 mm | f/190 | ~5 min | ~40 min, plate dries |
| 4x5 | 100 mm | 0.45 mm | f/220 | ~6 min | no |
| 5x7 | 150 mm | 0.55 mm | f/270 | ~10 min | no |
| 5x7, hole opened to 0.8 mm | 150 mm | 0.80 mm | f/190 | ~5 min | no |

Wet plate pinhole is a full-sun process. Shade and overcast run out the
clock. An oversized hole buys speed at the cost of softness, and on a 5x7
plate the extra blur is barely visible.

Ways to stretch the window:

- **Keep the camera humid.** A damp sponge or wet blotter inside the box,
  away from the light path. Historic trick for long wet plate exposures.
- **Shoot in cool weather** or early morning.
- **Larger hole**, as above. Two stops for going from 0.45 to 0.9 mm at
  100 mm depth.
- **Longer silver bath is not a fix.** Sensitivity does not keep rising.

## Camera

The relay box with a swappable back (see
[04-relay-camera-obscura.md](04-relay-camera-obscura.md)) is the starting
point. The plate back needs:

- **A plate holder that silver cannot corrode.** Silver nitrate eats brass
  and steel and stains wood. Standard 4x5 film holders work for glass plates
  with plastic corner shims; purpose-made wet plate holders use plastic or
  Delrin liners and a drip channel. Print the holder: PETG or ASA, one part,
  with a dark slide.
- **A shallower body.** 75 to 100 mm depth for 4x5. Either a separate short
  box with the same pinhole plate, or a removable spacer on the digital box
  so its depth can be cut in half.
- **Plate registration.** The collodion side faces the hole. A silver drip
  will run down the plate in the holder; a small sump at the bottom edge
  keeps it off the box.

### In-camera processing

The Dubroni (1864) did the whole wet plate process inside the camera: the
plate sat in a glass-lined chamber and the chemistry went in and out
through a port with a pipette. The pinhole version is a box with a sealed
plate chamber, a fill port, a drain, and a red window. No darkbox on
location. Worth a prototype once the basic process is working; it is the
kind of object that belongs in the show.

## Chemistry

Kit form (Bostick & Sullivan, Lund, UVP and others) or mix from scratch.
Cadmium-free "Old Workhorse" style collodion is the sensible default.

| Item | Role | Notes |
|---|---|---|
| Salted collodion | image layer | ether + alcohol; flammable, ventilate |
| Silver nitrate 9% bath | sensitizer | stains skin black, caustic to eyes; gloves, glasses |
| Iron sulfate developer | develops | ferrous sulfate, acetic acid, alcohol, water |
| Sodium thiosulfate 20% | fixer | not cyanide |
| Sandarac varnish | protects | lavender oil + alcohol; the plate is fragile until varnished |
| Glass or trophy aluminum | plate | glass edges sanded; aluminum for tintypes |
| Whiting + alcohol | plate cleaning | collodion will not adhere to a dirty plate |

Silver bath maintenance (sunning, filtering, pH) is the part that wears
people down. Keep the bath in a vertical tank with a lid and filter it
before each session.

## What the plate is

- **On clear glass, backed black:** ambrotype, a direct positive. One of a
  kind. Hang it.
- **On blackened aluminum:** tintype. Cheap, unbreakable, the same look.
- **On clear glass, not backed:** a collodion negative. Contact print it.
  Historically the negative for albumen prints; here the negative for
  cyanotype (see [06-diy-chemistry.md](06-diy-chemistry.md)). A pinhole
  collodion negative printed as a hand-coated cyanotype is entirely
  nineteenth-century and entirely home-made.

## Look

Pinhole plus collodion is soft on soft. The pinhole blur is a couple of
millimeters on a 5x7 plate; the collodion adds pour marks, edge chemistry,
and the blue-only tonality (white skies, black reds, luminous skin). The
combination has not been done much because wet plate people use lenses and
pinhole people use paper. That is a reason to do it.

## Day one plan

1. Buy or mix a small kit. Cut six 4x5 glass plates, sand the edges.
2. Build or adapt a 4x5 plate holder with plastic liners.
3. Use an existing film pinhole box at 75 to 100 mm depth, or a shallow
   spacer on the relay box.
4. Full sun, static subject, damp sponge in the box. Expose 5 minutes.
5. Develop in a changing bag or dark tent next to the camera. Fix in
   daylight. Rinse, dry, varnish over a spirit lamp.
6. Log plate, depth, hole, sun, temperature, exposure. Adjust hole size
   before adjusting anything else.

## Show

The process is a performance. Pour, silver, expose, develop, and the image
appears in the fixer in front of people. A pinhole box beside the digital
box, both fed by the same hole geometry, with the plates drying on a rack.
