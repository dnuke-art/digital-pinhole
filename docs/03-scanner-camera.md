# Flatbed scanner as the sensing element

The "scanner camera" is a real thing from the mid-2000s: Michael Golembewski's
Scanner Photography Project and Andrew Davidhazy's strip-photography work at
RIT are the most visible examples. This note records why it is not a pinhole
camera and probably cannot be made into one.

## How scanner cameras work

A flatbed scanner is a line sensor swept across the glass by a carriage.

1. Remove the lid.
2. Disable or mask the lamp.
3. Mount the scanner at the back of a big box with a lens on the front.
4. The projected image lands on the glass plane, where the scanner's own
   optics are focused.
5. Scan. Each column is captured at a different moment, which produces the
   signature time-smear on anything that moves.

The result is a letter-size "sensor" for the price of an old scanner. The
time-smear is a feature: it is slit-scan photography with a huge format.

## Why it needs a lens and not a pinhole

A scanner is built to read paper lit by a lamp a few millimeters away. Its
per-line exposure is set by the carriage speed, roughly a millisecond, and
there is no shutter to hold open. In practice a scanner camera in daylight
wants about the same light as an ordinary camera at f/5.6.

| Aperture | Light at sensor, relative | On a flatbed |
|---|---|---|
| f/5.6 lens, daylight | 1 | works; what the scanner-camera builders used |
| f/32 lens stopped down | 1/33 | marginal; slowest scan setting plus software gain |
| f/300 pinhole, letter-size box | 1/3000 | not close |

Scanning at the highest resolution slows the carriage and lengthens line
integration, worth maybe a factor of ten. That does not cover a factor of
three thousand. Some SANE backends expose the CCD exposure time and a few
people have hacked it, but the scanner's own optics accept light only in a
narrow cone, so the corners go dark anyway.

Better Light and the other professional 4x5 scanning backs of the era were
this idea done properly. Even they wanted f/8, hot studio light and scans of
a minute or more. That is the ceiling for line-sensor capture.

## Hardware constraints if you try anyway

- **CCD, not CIS.** Thin modern scanners (the Canon LiDE family and most
  cheap units) use a contact image sensor with a rod-lens array that only
  sees about a millimeter above the glass. They cannot image a projected
  picture at all. Older, thicker Epson and HP units with a reduction lens
  inside the body can.
- **Firmware fights you.** Scanners calibrate against a white strip with the
  lamp on before every pass and may refuse to scan without it. Getting a raw,
  lamp-off pass means the SANE backend and flag fiddling.
- **Focus plane is the glass.** The scanner's optics have a few millimeters
  of depth of focus. The projected image has to land on the glass plane.

## Verdict

A scanner camera with a proper lens is a good separate project if the
time-smear aesthetic appeals. As a pinhole camera it is a photon-starvation
problem with no fix. The large-format digital pinhole look comes from the
relay camera obscura instead: [04-relay-camera-obscura.md](04-relay-camera-obscura.md).
