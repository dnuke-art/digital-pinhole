# Thermal paper as film

Asked: can thermal (receipt) paper be used as the film in a pinhole camera?

Not by direct exposure. Two things do work: burning the sun's path with a
lens, and using a thermal printer as the camera's output. The second fits
this project unusually well.

## Why direct exposure cannot work

Thermal paper is a heat medium. The leuco dye and developer in the coating
react when it passes roughly 65 to 70 degrees C (some durable grades need
90+). Light only matters insofar as it heats the sheet.

Rough budget, still air, room temperature:

| Quantity | Value |
|---|---|
| Temperature rise needed | ~45 K |
| Convective loss coefficient | ~10 W/m^2/K |
| Absorptance of white thermal paper | ~0.15 |
| Irradiance needed to hold that rise | 45 * 10 / 0.15 = ~3000 W/m^2, about 3 suns |
| Direct sunlight | ~1000 W/m^2, 1 sun |
| Sunlit scene through an f/300 pinhole | ~0.002 W/m^2 |

A pinhole cannot concentrate light. The most it can ever deliver is slightly
under one sun, and only for an image of the sun itself. A sunlit scene
through the box arrives about six orders of magnitude short. Pre-warming the
sheet toward its threshold does not help: the margin needed is smaller than
the sheet-to-sheet and spot-to-spot variation, so the whole page develops.

Thermal paper also slowly darkens under months of UV and ambient light. Not
usable through a pinhole; too weak and too uneven.

## What works: burning the sun's path

The Campbell-Stokes sunshine recorder is a glass sphere that focuses the sun
onto a card and burns a trace across the day. Concentration through a lens
at f/2 is on the order of thousands of suns, so thermal paper develops
easily and at far lower power than charring. Even a marble or a small cheap
lens will leave a track. Gaps in the trace are clouds.

This is the thermal cousin of solargraphy (months of sun tracks recorded
through a pinhole onto photo paper). It needs a lens because only a lens
concentrates; a big pinhole yields a faint blurred sun disc under one sun
and nothing happens.

As an object: a glass sphere or lens on a stand, a curved thermal paper
strip behind it, changed daily. Thermal paper as film, with the sun as the
only subject.

## The fit for this project: thermal paper as output

Put a receipt printer on the relay box. The camera exposes, prints the frame,
cuts it. Visitors take it. The print fades over the next year or two because
thermal prints do, which suits the medium.

The resolution numbers line up:

| Item | Width | Dots or points across |
|---|---|---|
| Pinhole image on a 250 mm screen | 250 mm | ~200 real points |
| 58 mm receipt printer, 203 dpi | 48 mm printable | 384 |
| 80 mm receipt printer, 203 dpi | 72 mm printable | 576 |

The pinhole image carries fewer real points than the printer has dots. The
receipt loses nothing. Tone comes from dithering (Floyd-Steinberg or ordered
for a coarser look) or from the printer's native grayscale mode where it has
one.

Practical:

- Cheap ESC/POS printers drive from a Pi over USB or serial. `python-escpos`
  handles image printing.
- Pick a printer with an auto-cutter if prints are handed out.
- Thermal paper rolls are cheap; buy phenol-free stock if people will handle
  them.
- Keep the printer out of the light path and its head warmth away from the
  camera.

## Larger thermal prints: laser scanning

For prints bigger than a receipt, scan a low-power laser diode across
fax-roll thermal paper (216 mm width, still sold). Hobby engravers at very
low power develop the coating rather than burn it. Same dither pipeline, one
extra machine. Ventilate: heated thermal coatings release bisphenol vapor.
