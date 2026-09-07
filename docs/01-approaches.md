# Three ways to build a digital pinhole camera

All three work. They differ in how much you build and in how large the
"format" is, which is what sets pinhole image quality (see
[02-pinhole-physics.md](02-pinhole-physics.md)).

## 1. Body cap on a mirrorless camera

Drill or laser-cut a hole in a body cap, mount it, shoot. Zero build effort and
the sensor is large, which is the single biggest factor in pinhole sharpness.

- Sony E flange distance is 18 mm, giving an optimum hole of about 0.10 mm and
  f/180.
- Sensor dust is brutally visible at these apertures. Clean the sensor first.
- Exposure is friendly: about 1/6 s in sunlight at ISO 800, seconds to minutes
  indoors.
- The sensor stack (cover glass, IR filter, microlenses) expects near-normal
  incidence. With the hole only 18 mm from the sensor the corners get steep
  rays, so expect some vignetting and color shift at the edges.

Good for making pinhole images quickly. Not much of an object to show.

## 2. Raspberry Pi HQ camera in a box you make

The HQ camera (Sony IMX477, 1/2.3", 6.17 x 4.55 mm) has a C/CS mount. Remove
the lens and a printed cap with a pinhole disc bolts straight on.

- Exposures up to several minutes under libcamera.
- Live view on a screen, which film pinhole can never do. Good gallery
  behavior: the box is the object, the screen shows what it sees.
- The sensor is tiny, so the image is very soft. A hole 5 mm from the sensor
  wants a 0.07 mm hole at f/70 and resolves roughly 45 points across the
  frame. Dreamy, not sharp.
- Same steep-ray vignetting issue as above, worse because the hole is closer.
  Moving the hole back trades field of view for evenness.

Good if the soft look is the point. Sharpness will never approach 4x5 film.

## 3. Camera obscura with a relay camera inside

A large pinhole box projects onto a matte screen on the back wall. A small
camera mounted beside the hole on the inside of the front wall photographs the
screen with a long exposure.

- The pinhole geometry is large format, so softness, vignetting and
  perspective all come from the pinhole, not from the little camera.
- The relay camera absorbs the light deficit because it has a real shutter
  and ISO.
- Costs about four stops of light versus a sensor at the screen plane, so it
  is a slow camera. Suits the medium.
- Cheapest large-format digital pinhole there is.

This is the direction the project is taking. Details in
[04-relay-camera-obscura.md](04-relay-camera-obscura.md).

## Comparison

| Setup | Hole-to-image distance | Hole | f-number | Resolvable points across frame |
|---|---|---|---|---|
| Full-frame body cap (Sony E) | 18 mm | 0.10 mm | f/180 | ~180 |
| Pi HQ camera, hole close to sensor | 5 mm | 0.07 mm | f/70 | ~45 |
| 4x5-style box, sensor at screen plane | 150 mm | 0.29 mm | f/520 | ~200 |
| 200 mm deep box with relay camera | 200 mm | 0.63 mm | f/317 | ~200 |

## Rejected: flatbed scanner as the sensor

Scanner cameras are real and lovely but they need roughly f/5.6 worth of light
and a pinhole delivers about three thousand times less. Full reasoning in
[03-scanner-camera.md](03-scanner-camera.md).

## Sensor directly behind the hole vs a screen

Asked after the relay design was sketched: why not put a wide Pi camera right
behind the pinhole?

Two different things hide in that question.

**Lens removed, bare sensor behind the hole.** This is approach 2. Its one big
advantage is light: at 5 mm the pinhole runs about f/70 with no screen loss,
roughly eight stops brighter than the relay box. Live video outdoors, seconds
indoors. It gives up format: the pinhole image forms on a 4.6 mm sensor
instead of a 250 mm screen, so ~45 points across instead of ~200, plus
steep-ray vignetting and color shift in the corners. Practical snag: the
Module 3 lens lives in an autofocus module and is not meant to come off. The
v2 module lens unscrews; the HQ and Global Shutter cameras are built for lens
swaps.

**Lens kept on, hole in front of it.** Not a pinhole camera. The lens forms
the image and the hole is an aperture stop; a 0.6 mm hole on a Module 3 Wide
is about f/4.6 and makes a sharp deep-focus lens photo. Shrink the hole until
diffraction dominates and it is a lens shot at f/60. A hole a few millimeters
ahead of the lens also crops the field into a circle. Can look pinhole-ish
but the rendering is the lens's.

The screen buys exactly one thing, format size, and the relay camera absorbs
the four-stop cost because it has a shutter and ISO.

| Design | Format width | Points across | Effective speed | Live view? |
|---|---|---|---|---|
| Pi camera, lens off, behind hole | 4.6 mm | ~45 | f/70 | yes, outdoors |
| Full-frame body cap | 36 mm | ~180 | f/180 | slow, seconds |
| Relay box, 250 mm screen | 250 mm | ~200 | f/317 + 4 stops | no |

Worth keeping in view: a used full-frame body with a body cap pinhole matches
the relay box's sharpness at about five stops brighter, tethers over USB, and
costs a few hundred dollars used. As an instrument it is better. The box wins
on being a made object at the scale of the film cameras, and on scaling to
8x10 and beyond where no sensor follows.
