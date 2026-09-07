# Can a diffraction grating be the lens?

Short answer: a plain grating cannot, because it bends light without
focusing it. A grating whose line spacing shrinks outward does focus, and
that is a zone plate. Both are useful here for different reasons. Mockups:
`mockups/out/look3_*.png`, sheet `grating_sheet.png`.

## Linear grating: a prism, not a lens

A grating with spacing `d` sends light of wavelength `lambda` off-axis by
`sin(theta) = m * lambda / d` for order `m`. Every wavelength goes a
different way, but nothing converges. Put one over the pinhole and the
pinhole still forms the image; the grating adds two rainbow copies of it.

Numbers on the 200 mm box with a 500 lines/mm film grating ($5):

| Wavelength | First-order angle | Displacement on the screen |
|---|---|---|
| 400 nm (violet) | 11.5° | 41 mm |
| 550 nm (green) | 16.0° | 57 mm |
| 700 nm (red) | 20.5° | 75 mm |

So each point of light becomes the point itself (zero order) plus a
34 mm rainbow on either side. At night with streetlights that is a
spectrograph: every light writes its spectrum, and sodium, LED and neon
sources look different. In daylight the whole scene gets two rainbow-smeared
ghosts overlaid, which is mostly mush. A crossed grating (the "rainbow
glasses" film, about 530 l/mm) gives four rainbows per light, on a cross.
Efficiency for a cheap sinusoidal film grating: roughly a third of the light
in zero order and a third in each first order.

Night piece, cheap, real, and it works in white light since dispersion
does not need coherence. Mockups: `look3_01_grating_night`, `look3_02_grating_day`.

## Zone plate: the grating that focuses

Rings at radii `r_n = sqrt(n * f * lambda)`. It is a circular grating whose
pitch falls with radius so every zone's first-order deflection lands at the
same focus. For the 200 mm box designed at 550 nm with 25 zones:

| Quantity | Value |
|---|---|
| Innermost zone radius | 0.33 mm |
| Outer diameter | 3.3 mm |
| Outermost zone width | 33 um |
| Focused spot (green) | ~0.07 mm, vs 1.2 mm for the pinhole |
| Light through the plate vs the optimum pinhole | ~12x (half of 25 zones open) |
| Of that, in the +1 focus | ~20 percent, so ~2.5x the pinhole, about 1.3 stops |
| Zero order | 25 percent of the total: a soft image through the whole 3.3 mm plate |
| Minus-one and higher orders | the rest, softer still |

So the zone plate image is a sharp green picture sitting on top of a pile
of soft copies of itself. That is the glow. Total light is many times a
pinhole's but most of it is fog, which is why real zone plate photographs
are low-contrast and dreamy.

Chromatic aberration is the other half of the character. Focal length is
inversely proportional to wavelength:

| Colour | Focal length | Defocus at the 200 mm screen | Blur diameter |
|---|---|---|---|
| Red 650 nm | 169 mm | 31 mm | 0.6 mm |
| Green 550 nm | 200 mm | 0 | sharp |
| Blue 450 nm | 244 mm | 44 mm | 0.6 mm |

Red and blue come out about as soft as the pinhole; green is roughly
fifteen times sharper. Mockups: `look3_03_zone_plate_pattern`,
`look3_04_zone_plate_capture`.

## Why the digital box makes the zone plate much better

Two things the film version cannot do:

- **The point spread function is known.** It is the sum of a sharp core
  and a few Gaussians of known size. Subtract the halo in software and the
  contrast comes back. Cheap deconvolution, no guessing.
- **Green carries the detail.** Take luminance from the sharp green channel
  and colour from the soft red and blue. The eye reads luminance for
  sharpness, so the result looks sharp in colour. Mockup:
  `look3_05_zone_plate_digital`.

A third option is mechanical: put the plate on a short rail and shoot red,
green and blue frames at their own foci (169, 200, 244 mm), then merge. Or
shoot under sodium light, which is monochromatic, and the plate is simply a
sharp fast lens.

Net: a printed transparency as the lens, deconvolved in software, gives a
picture several times sharper than the pinhole at a couple of stops faster.
Still a lensless, diffraction-only camera. Worth building.

## Related things that also count as "a grating as a lens"

- **Photon sieve.** The zone plate's rings replaced by many small holes
  distributed over each zone. Less halo, sharper, less light. Same file to
  make, different pattern.
- **Holographic optical element.** A hologram of a point source is a zone
  plate with a sinusoidal profile; volume holograms put most of the light in
  one order. Sold for AR displays; expensive for this.
- **Blazed or phase zone plate (kinoform).** Etched glass rather than
  printed black rings, 40 to nearly 100 percent in the focus. The
  diffractive elements in some camera lenses. Not home-makeable.
- **Fresnel lens.** Grooves, not lines; refractive, not diffractive. A page
  magnifier in the box is an ordinary lens camera obscura, bright and
  low-contrast. Different thing, often what people mean.

## Making a zone plate at this scale

Outer zone width is 33 um at 25 zones. Options:

| Method | Resolution | Fit |
|---|---|---|
| Laser printer on transparency | 20 um dots at 1200 dpi | marginal at 25 zones; fine at 10 |
| Print shop imagesetter film | ~7 um | good, ask for a film negative |
| Photograph a big printout onto litho film at 20:1 | ~10 um | the classic hobbyist route |
| Chrome-on-glass photomask | <1 um | best; ~$100+ |
| Buy (Lensbaby-style pinhole/zone plate optic, hobby kits) | made for 35 mm | wrong focal length for the box |

Fewer zones is easier to make and gives a smaller aperture with less fog;
more zones is sharper and brighter. Ten to twenty-five is the useful range.
Make it the same swappable plate as the pinhole, and keep the grating film
as a slip-over for night.
