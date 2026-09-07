# Odd apertures, and the dither catalogue

Asked: double slits, moire, anything to make it interesting; and the
receipt-printer dither looked like old PC graphics and the Game Boy Camera.
Mockups for all of it are in `mockups/out/look2_*.png`
(`experiments_sheet.png`) and `mockups/out/dither_*.png` (`dither_sheet.png`).

## The one rule that sorts the aperture ideas

A pinhole camera is a linear system. The image on the screen is the scene
convolved with the shape of the aperture. Every point in the scene becomes a
copy of the hole. That single fact predicts all of these:

- A **slit** makes every point a line: sharp across the slit, smeared along
  it. Anamorphic blur.
- **Two slits** make two smeared copies, shifted by the slit spacing. No
  fringes in daylight (see below for when there are).
- **Two crossed slits at different distances** give different focal lengths
  in x and y: a true anamorphic pinhole. Vertical slit at 200 mm and
  horizontal at 100 mm squeezes 2:1.
- **Several holes** make several overlapping copies, and add their light.
  Five holes, five times the light, five ghosts.
- A **shaped hole** (star, letter) stamps its shape on every point light. At
  night every streetlight is a star. In daylight the scene is just mush with
  starry highlights.
- A **hole array cannot make moire.** Convolution only weights the scene's
  existing frequencies; it never creates new ones. My first mockup of this
  was wrong and has been replaced.

## Where moire actually comes from

Moire is multiplication of two periodic patterns, and in this camera that
happens in three places, none of them the aperture:

1. **At the screen.** A screen printed with fine lines, or a mesh laid over
   it, multiplies the projected image. A picket fence projected onto a lined
   screen beats at the difference frequency. Walk toward the fence and the
   bands sweep as its projected period changes. Real, cheap, tunable.
2. **At the sensor.** The relay camera samples the screen on a pixel grid.
   Fine periodic detail near the pixel pitch aliases into bands. This is
   ordinary camera moire, and the fence on the screen will do it.
3. **At the printer.** A halftone dot screen or ordered dither is a periodic
   pattern multiplied into the image. Print a fence, get bands.

Mockup: `look2_06_moire`.

## Double slit: fringes need a small sensor

Fringe spacing is `lambda * L / d` (wavelength, slit-to-image distance,
slit separation). On the 200 mm box with slits 1 mm apart that is 0.13 mm,
a tenth of a screen-point, and white light smears it further. Invisible.

On the Pi HQ sensor with the lens off, the geometry flips in your favour.
Slits 0.12 mm apart, 5 mm from the sensor, under a red gel: fringe pitch is
about 16 microns, ten sensor pixels. Point the camera at streetlights at
night and every light becomes a vertical bar (from the slit length) carrying
horizontal fringes (from the slit pair). The "wrong" tiny-sensor camera is
the right one for interference. Mockup: `look2_03_double_slit_fringes`.

Slits at 0.05 mm width and 0.12 mm pitch are a laser-cut or photo-etched
part, not a knife job. A double-slit diffraction slide from a physics
supplier is a few dollars and drops into the C-mount cap.

## Zone plate

A Fresnel zone plate is a diffractive lens: concentric rings whose spacing
makes one wavelength focus at one distance. Compared with a pinhole of the
same focal length it is brighter (the open rings add up, roughly the number
of zones divided by 2 over a pinhole at the same resolution, call it two to
four stops) and its central spot can be smaller. The price is a big soft
halo from the other diffraction orders and strong colour: red focuses
nearer, blue farther, so the glow is chromatic. The look is a well-known
dreamy high-key glow with fringed edges. Mockup: `look2_08_zone_plate`.

Make one by laser-printing the ring pattern on transparency (fine for a
200 mm focal length, the outer rings are ~0.1 mm) or by ordering a
photo-etched plate. Design: ring radii `r_n = sqrt(n * f * lambda)`.

## Coded aperture: the computational pinhole

Replace the hole with a plate that is half open in a pseudo-random pattern
(a MURA, modified uniformly redundant array, prime size p). The screen shows
the scene shadowed through the pattern, an abstract mess. One correlation in
software with the matching decoding pattern recovers the picture.

Why bother: the plate passes about p^2 / 2 pinholes' worth of light. At
p = 101 that is roughly 5000 times a single pinhole, so the relay box's
half-hour interior exposure becomes a fraction of a second. Resolution is
p points across, set by the cell size, so at 101 it is Game Boy territory.
The raw capture and the decode are both images worth showing. This is
X-ray-astronomy technology; it works because our capture is digital.

Caveats that matter:

- Decoding assumes the scene is at infinity and fully inside the coded
  field. Nearer objects and the field edges decode with artefacts.
- The raw image has very low contrast, so it needs a clean, high-bit-depth
  capture. Noise in the raw becomes noise everywhere in the decode.
- The plate's cells must be small and sharp: 2 mm cells for p = 101 on a
  250 mm screen. Laser-cut steel or photo-etched brass.

Mockups: `look2_09_mura_mask`, `look2_10_mura_raw`, `look2_11_mura_decoded`.

## Two holes, two gels: an anaglyph straight out of the box

Two pinholes 65 mm apart, red gel on the left, cyan on the right. The two
images overlap on the screen with a parallax that depends on distance, and
the capture is already a red/cyan anaglyph. Put the glasses by the screen.
Nearer objects separate more, so a scene with something close works best.
Mockup: `look2_12_anaglyph` (fakes depth with a ground plane).

## Slit-scan onto the receipt roll

A vertical slit, and the relay camera reads one column per interval and the
printer prints it as one row. The roll is the film and the length is time.
A static scene prints as streaks; anything that crosses the slit prints as
itself, stretched by how slowly it crossed. A day is about a metre of paper.
Pure software on top of the relay box. Mockup: `look2_13_slit_scan`.

This is the scanner camera's aesthetic (see [03-scanner-camera.md](03-scanner-camera.md))
without the scanner, and with the printer doing the sweep.

## The dither catalogue

The receipt printer is a 1-bit device and every old 1-bit display had its
own dither. The pinhole image carries about 200 real points across, which
is exactly the resolution these styles were designed for. Sheet:
`mockups/out/dither_sheet.png`.

| Style | What it is | Read |
|---|---|---|
| Floyd-Steinberg | error diffusion, 1976 | smooth, "photographic", the printer default |
| Atkinson | Bill Atkinson's 1984 Mac dither, diffuses 6/8 of the error | lighter, crisper, blows highlights, drops shadow detail |
| Bayer 4x4 | ordered threshold matrix | the crosshatch of CGA/EGA-era art |
| Bayer 8x8 | larger matrix | smoother ramps, still a visible grid |
| Halftone dot, 45 degrees | newspaper screen | dots grow with darkness; moires against periodic subjects |
| Line screen | horizontal lines, thickness carries tone | engraving; suits the slit-scan strip |
| Game Boy Camera | 128 x 112, four greens, ordered dither | the look you remembered |
| CGA palette 1 | 320 x 200, black/cyan/magenta/white | cursed and lovely |
| 1-bit at 96 px | the pinhole's points quartered, then dithered | reads as the printer's own grain |

All of them are a few lines of numpy on the relay frame. Bayer and Atkinson
are the two that most say "old computer"; halftone and line screen most say
"print". A rotary switch on the box that picks the dither per print is a
cheap, legible piece of interaction.

## What survives as a build idea

- Screen printed with a line grid, swappable with the plain screen (moire).
- A double-slit slide in the Pi HQ cap, for night work.
- A laser-printed zone plate as a second aperture plate.
- A MURA plate, once the relay box works, for the fast/decoded mode.
- Two gelled holes for anaglyphs.
- Slit-scan mode and the dither switch in software.
