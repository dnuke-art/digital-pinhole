# Ideas

Running list. Loose thoughts land here first; the ones that grow get a
numbered note in `docs/`. Mark status inline.

## Cameras

- **Relay camera obscura** — pinhole box, matte screen, Pi camera beside the
  hole. The main build. → docs/04
- **Walk-in version** — same idea at room scale for the show. Blackout a
  room or a big crate, hole in one wall, camera on a tripod inside doing
  minute-long frames. Morell's move. Untested; needs a dark enough space.
- **Swappable back on the relay box** — screen + Pi camera in one back, a
  4x5/5x7 plate holder in another. Same box shoots digital and wet/dry plate.
- **8x10 or larger relay box** — sharper (~300+ points across) and slower.
  Only if the gallery light budget allows.
- **Full-frame body cap pinhole** — better instrument than the box, worse
  object. Keep as the fast way to make digital pinhole images. → docs/01
- **Pi HQ camera, lens off** — small, bright, soft. Live video outdoors.
  Good for a handheld or a video piece. → docs/01
- **Scanner camera with a lens** — separate project; time-smear aesthetic on
  a letter-size format. Not pinhole. → docs/03
- **Sun-trace recorder** — Campbell-Stokes on thermal paper. Glass sphere or
  lens, curved thermal strip, changed daily. Thermal paper as film for the
  one subject bright enough. → docs/05
- **Solargraphy cans** — months-long pinhole exposures on photo paper, no
  developer. Uses existing cameras. → docs/06

- **Double-slit slide in the Pi HQ cap** — fringes are 16 um on the small
  sensor, invisible on the big screen. Night, red gel, streetlights. → docs/08
- **Zone plate aperture plate** — printed or litho-film, green ~15x sharper
  than the pinhole, ~1.3 stops more focused light plus fog; deconvolve in
  software, luminance from green. → docs/09
- **Grating film slip-over for night** — 500 l/mm, every streetlight writes
  its spectrum 34 mm long. Disperses, does not focus. → docs/09
- **Photon sieve** — zone plate rings as scattered holes; less halo. → docs/09
- **Concave grating spectrograph box** — grating film on a makeup mirror,
  slit and detector strip on the Rowland circle, Pi camera reads the
  spectrum. Streetlight fingerprints at night; spectrum of the day on the
  receipt roll. Ray-traced in FreeCAD: focus 0.14 mm, ~2 mm astigmatism. → docs/10
- **Circular constant-pitch aperture** — diffractive axicon; every night
  light a disc inside a rainbow ring. → docs/10
- **MURA coded aperture plate** — thousands of times the light, decoded in
  software at ~100 points across; the raw capture is its own image. → docs/08
- **Crossed slits at two depths** — anamorphic 2:1 pinhole. → docs/08
- **Star-shaped hole for night lights** — every streetlight wears the
  shape. → docs/08
- **Two gelled holes, 65 mm apart** — capture is already an anaglyph. → docs/08
- **Lined screen for moire** — a hole array cannot make moire (linear);
  a printed grid on the screen can. Swappable screen. → docs/08

- **110 cartridge pinhole camera** — the cartridge is the film gate, the
  transport and the pressure plate, so the camera is a printed box with a
  0.2 mm hole, a thumbwheel and a sliding shutter. Lomography still makes
  the film; a printed Paterson-fit reel develops it at home. Existing
  design: bergytone's 110 pinhole on Thingiverse (0.18 mm hole). Hand-out
  camera for the show; caffenol develops it.
- **Printed lens for the 110 box** — Amos Dudley's SLO (Downloads has the
  STL + .form set, no source) printed its lens on a Form 2 and polished it.
  Dan has printed lenses and smoothed them by resin dip and spray lacquer.
  A single printed element over the 110 gate is the next step up from the
  hole; the tiny format forgives a rough lens.
- **Printed lens plate for the relay box** — swap the pinhole plate for a
  printed singlet at f/4 to f/8: 10 to 12 stops brighter, so the screen goes
  live on the Pi camera. Pinhole mode is slow, lens mode is a live camera
  obscura. The Pi's live view is also the fastest way to judge a printed lens.
- **Droplet lens** — a drop of clear UV resin cured on a printed ring forms a
  spherical cap by surface tension; the print is only the holder and the
  liquid makes the optical surface. No sanding, repeatable by drop volume.
- **Spin-cure the resin dip** — rotate the dipped lens slowly under the UV
  lamp so the coat does not sag into a wedge at the bottom edge.

- **Peel-apart pinhole** — only One Instant (Supersense, Vienna) still makes
  pack film, hand-made, Type 100 size, plus a cheaper DIY kit since late
  2023. ~ISO 100: ~1.6 s at f/200 in sun. Do not print the rollers: build a
  pinhole body that takes a Polaroid 405 back, or put a hole in a Land
  camera lens board. The B&W POS/NEG stock yields a reclaimable negative.
- **Home-made peel-apart (diffusion transfer)** — expose a paper negative,
  sandwich it face to face with a receiver sheet with a developer paste
  between, wait five minutes in the dark, peel. The Photrio "Diffusion
  Transfer Printing recipes" thread is the working lab notebook (receiver
  nucleation layers, thiosulphate/phenol paste). Not instant in the camera,
  but a positive and a negative from one paper exposure, and the same
  rollers-or-squeegee question as pack film. The Supersense DIY kit is the
  packaged version of the same idea.
- **Instax pinhole** — integral film that is cheap and everywhere, ISO 800,
  ~1/9 s at f/150 in sun. Printed bodies exist; Jollylook sells hand-crank
  Instax backs. The hand-out camera with a print in 90 s.

## Outputs

- **Instax Link printer on the relay box** — the Pi prints each frame to
  instant film over Bluetooth (javl/InstaxBLE). Wide Link is 800 x 1260 px,
  far more than the pinhole's ~200 points. A real photograph pops out next
  to the receipt.
- **Peel-apart negative to cyanotype** — One Instant B&W POS/NEG: keep the
  positive, contact print the peeled negative as a cyanotype. All analog,
  all hand-made, two prints per exposure.
- **Peel-apart image transfer** — pull early, press the wet negative onto
  watercolor paper: pigment transfer, the classic pack-film manipulation.

- **Receipt printer on the box** — ESC/POS, dither, auto-cutter, prints
  fade. Resolution match with the pinhole image is near perfect. → docs/05
- **Laser onto fax-roll thermal paper** — bigger thermal prints, hobby
  engraver at very low power. Ventilate. → docs/05
- **Digital negative → cyanotype** — hand-coated, contact printed. The wall
  piece that ties digital capture to hand printing. → docs/06
- **Receipt as oiled paper negative** — print inverted on thermal paper,
  oil it, contact print cyanotype from it. One-afternoon experiment; UV
  opacity of the thermal dye unknown.
- **Slit-scan onto the receipt roll** — one printed row per interval, the
  roll is the film, a day is a metre. Software only. → docs/08
- **Dither switch on the box** — Floyd-Steinberg, Atkinson, Bayer, halftone,
  line screen, Game Boy, CGA. Rotary switch picks the print style. → docs/08
- **Frame stacking vs single long exposure** — different motion character.
  Decide per piece, not globally. → docs/04
- **E-ink display beside the box** — slow refresh matches the medium.
  LCD is easier.

## Process

- **Bitumen heliograph plate in a lens camera obscura** — all-day exposure,
  developed in lavender oil, no fixer, no darkroom. Niépce 1826. → docs/06
- **Calotype paper negatives in the pinhole boxes** — brush-on sensitizing,
  expose damp, develop at once. ~30 min pinhole exposure in sun. → docs/06
- **Identify the Instagram no-fixer glass plate process** — find the
  account. Candidates listed in docs/06.

- **Caffenol** for developing paper in the film boxes. → docs/06
- **Hand-coated liquid emulsion** on glass, wood, found objects, exposed in
  the pinhole boxes. → docs/06
- **Wet plate pinhole** — collodion through a pinhole. Full-sun process,
  ~5 min at f/190, plate must stay wet. Shallow 4x5 box, silver-proof
  holder, damp sponge in the camera. Pursuing. → docs/07
- **Dubroni-style in-camera processing** — sealed plate chamber, fill port,
  drain, red window; no darkbox on location. Prototype after the basic
  process works. → docs/07
- **Pinhole collodion negative → cyanotype** — nineteenth-century end to
  end, all hand-made. → docs/07
- **Stacked frames as dark-frame subtraction** — free noise cleanup on the
  relay camera.

## Dead ends, kept for the record

- Curving the grating film at the pinhole: the hole samples a patch too
  small for curvature to matter.

- A linear grating as the lens: no optical power, it only disperses.

- Pinhole array as a moire generator: convolution is linear, no new
  frequencies. Moire needs multiplication (screen grid, sensor sampling,
  halftone).
- Double slit on the big screen: fringes 0.13 mm, a tenth of a screen
  point, washed out in white light.

- Pinhole directly onto thermal paper: needs ~3 suns, pinhole delivers <1.
- Cyanotype in a pinhole camera: ~8 years at f/300.
- Flatbed scanner behind a pinhole: ~3000x short on light.
- Pi camera with lens on behind a hole: that is a lens at f/60, not a
  pinhole.

## Questions to settle before building

- Box depth and screen size.
- Front-projection matte card vs rear-projection second chamber.
- Which Pi camera (Module 3 Wide vs HQ) — set by box depth.
- What the box points at during the show.
- Plate holder standard for the swappable back (4x5 is cheapest and most
  available; 5x7 is closer to the screen size).
