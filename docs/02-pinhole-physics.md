# Pinhole physics, as much as the project needs

## Optimum hole diameter

Two blurs compete. A bigger hole projects a bigger geometric spot; a smaller
hole diffracts more. The crossover (Lord Rayleigh's form, widely used) is

    d = 1.9 * sqrt(f * lambda)

where `f` is hole-to-image distance and `lambda` is the wavelength, taken as
550 nm (green, mid-visible). The f-number is then `N = f / d`.

| f (hole to image) | d | N |
|---|---|---|
| 5 mm | 0.07 mm | f/70 |
| 18 mm | 0.10 mm | f/180 |
| 50 mm | 0.31 mm | f/160 |
| 100 mm | 0.45 mm | f/220 |
| 150 mm | 0.55 mm | f/270 |
| 200 mm | 0.63 mm | f/317 |
| 300 mm | 0.77 mm | f/390 |

Note the f-number keeps rising with depth. Bigger boxes are slower.

## Resolution scales with format, not pixels

At the optimum, the blur spot on the image plane is roughly twice the hole
diameter. So the number of resolvable points across the frame is about

    frame_width / (2 * d)

Since `d` grows only with the square root of `f`, and frame width grows
linearly with `f` for a given field of view, larger formats are sharper.
This is why 4x5 and 8x10 pinhole prints look the way they do and why a
phone-sensor-sized pinhole camera never will.

A 12 MP sensor behind a correctly sized pinhole is capturing a picture that
holds maybe 50 to 200 real points across. Any sensor with more pixels than
that is oversampling, which is fine, but it buys nothing.

Consequence for the design: the sensing element's pixel count does not
matter. The size of the image plane does.

## Exposure

Sunny 16 rule: at ISO 100 in full sun, 1/100 s at f/16. Scale by
`(N / 16)^2` for the pinhole's f-number.

| Pinhole N | Factor vs f/16 | Sunlight, ISO 100 | Sunlight, ISO 800 |
|---|---|---|---|
| f/70 | 19 | 0.2 s | 1/40 s |
| f/180 | 127 | 1.3 s | 1/6 s |
| f/300 | 352 | 3.5 s | 0.44 s |
| f/500 | 977 | 10 s | 1.2 s |

Scenes darker than sunlight add stops on top of that:

| Scene | Stops below full sun | Multiply exposure by |
|---|---|---|
| Overcast | 3 | 8 |
| Open shade | 3-4 | 8-16 |
| Bright interior | 8 | 256 |
| Dim interior | 10 | 1024 |

Reciprocity failure is a film problem. Digital sensors do not suffer it, but
long exposures accumulate dark-current noise and hot pixels. Dark-frame
subtraction or stacking many shorter frames handles that.

## Small-sensor caveat: steep rays

Consumer sensors have microlenses over each pixel that assume light arriving
close to perpendicular, and a cover glass / IR filter stack that shifts color
with angle. A pinhole close to a sensor sends corner rays in at steep angles,
giving vignetting and a color cast at the edges. Moving the hole further
back reduces the effect and narrows the field of view. Large-format
projection onto a screen avoids the issue entirely, which is one more point
for the relay design.
