# Relay camera obscura

The chosen design. A pinhole box projects onto a matte screen on its back
wall, and a small camera mounted beside the hole on the inside of the front
wall photographs the screen with a long exposure.

This is what Abelardo Morell does at room scale: black out a window, cut a
hole, photograph the picture that lands on the far wall with a long
exposure. Ours is the same thing in a box.

```
   front wall                                    back wall
   +-----------------------------------------------+
   |  o  <- pinhole                                |
   |                                               |
   | [cam] -------- looks at screen -------->  ####|  matte white screen
   |                                           ####|
   |  black interior                           ####|
   +-----------------------------------------------+
   <------------------ depth f -------------------->
```

## Geometry

- **The camera never shadows the image.** The pinhole cone diverges from the
  hole toward the back wall. Anything on the front wall beside the hole is
  outside the cone.
- **Off-axis is fine.** Mount the camera a couple of centimeters from the hole.
  Keystone is negligible at that offset, or correct it once with a homography.
- **The screen is the back wall.** Matte white card. Nothing glossy.
- **Everything else is black.** Flocking or flat black paint on all interior
  surfaces, especially the front wall around the camera. Otherwise the screen
  lights the interior and the interior fogs the screen.
- **Relay camera field of view.** To see a 250 mm screen from 200 mm away
  the camera needs about a 65 degree horizontal field. Pi Camera Module 3
  Wide covers it; a standard Module 3 or HQ camera with a short lens also
  works with a deeper box.
- **Resolution is not a concern.** A 200 mm deep box wants a 0.63 mm hole,
  giving a blur spot near 1.2 mm on the screen. The pinhole image holds
  about 200 resolvable points across. Any 1080p sensor captures all of it.

## Light budget

A matte screen scatters the pinhole image in all directions and the relay
camera collects only a small cone of it. Relative to a sensor sitting at the
screen plane, the relay loses about

    albedo / (4 * N_relay^2)

which at f/2 and a 0.9 albedo screen is roughly 1/18, or four stops.

| Scene | Sensor at screen, f/300, ISO 100 | Relay at f/2, ISO 800 |
|---|---|---|
| Sunlit exterior | 3.5 s | 8 s |
| Overcast or open shade | 30 s | 1 min |
| Bright interior room | 15 min | 30 min |

So it is a slow camera. Pointed out a window or set outside it makes a frame
every few seconds to a minute. Inside a gallery it needs the same patience as
a film box, or the equivalent trick of stacking many shorter frames, which
also cleans up sensor noise.

Ways to buy back light, in order of preference:

1. Higher relay ISO (noise is fixable by stacking).
2. Faster relay lens (f/1.4 board lenses exist, but corners suffer).
3. Larger pinhole. Softer, and the box gets a stop per doubling of area.
4. Shallower box. Lower f-number but wider angle and more screen falloff.

## Relay camera choice

The exposure ceiling decides it.

| Camera | Max single exposure | Notes |
|---|---|---|
| USB webcam | ~1 s | Noisy; can only work by stacking frames |
| Pi Camera Module 3 / 3 Wide | ~112 s (libcamera) | Wide variant fits shallow boxes; autofocus |
| Pi HQ camera (IMX477) | ~670 s (libcamera) | Larger sensor, cleaner; needs a CS lens |
| Mirrorless body | bulb | Best quality, biggest box, no live feed |

The Pi cameras produce a genuine long exposure with the same motion-blur
character as film. Stacking gives the same total light but averages motion
differently, which is a different look. Pick one deliberately.

Practical details:

- Kill every LED on the camera and Pi. Tape over what cannot be disabled.
- Remove the IR filter from nothing. Keep it; the screen is neutral.
- Lock white balance and gain per session. Auto anything drifts across
  minute-long frames.
- Shoot raw or at least uncompressed to keep the shadow tones the screen
  gives you.

## Build sketch

- Box: plywood or printed, roughly 250 x 200 mm screen, 200 mm deep. Light
  tight seams; a lip on the lid.
- Pinhole plate: 0.05 mm brass shim or a laser-drilled disc in a printed
  holder, 0.6 mm hole for 200 mm depth. Make the plate swappable so
  different holes can be tried.
- Camera mount: printed bracket on the inside of the front wall, 20 to
  30 mm from the hole, aimed at screen center.
- Electronics: Pi Zero 2 W, Camera Module 3 Wide, one button, optional
  small display or e-ink panel on the outside.
- Software: one script. Button press starts an exposure of a configured
  length (or a stack of N frames), writes a file, pushes it to the display
  and to a folder the gallery screen watches.

## Show behavior

The box sits with the prints. It faces a window or a lit tableau. Every few
minutes it takes a frame and the screen beside it updates. Visitors see a
pinhole image forming with the same slowness the film prints were made with,
but on a screen, which makes the link between the two bodies of work
legible without explanation.

## Open questions

- Box size. Larger is sharper and slower. 8x10 inch screen at 300 mm depth
  is a real option if the gallery light allows it.
- Screen material. Plain matte card vs a slight-gain rear projection screen
  with the camera behind it (a second chamber). Front projection is simpler
  and is the plan unless the four-stop loss proves too much.
- Display. Live e-ink is slow and matches the medium; an LCD is easier.
