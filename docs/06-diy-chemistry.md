# Low-fi chemical processes you can do yourself

Asked: what DIY chemical process could the digital pinhole work feed, or
replace the digital capture? Cyanotype specifically.

The one fact that sorts every process is speed. Everything you can sensitize
in a kitchen is a contact-printing process. Only silver emulsions are fast
enough to expose inside a camera.

## Cyanotype in the camera: no

A cyanotype contact print in full sun takes about ten minutes. Inside a
camera the paper sees the scene through the aperture, which cuts the light
by about `4 * N^2 / albedo` relative to contact printing (albedo of a sunlit
white surface ~0.8).

| Where the paper sits | Light vs contact | Ten-minute contact print becomes |
|---|---|---|
| Contact frame in sun | 1 | 10 min |
| Behind an f/1 Fresnel camera obscura | 1/5 | ~1 hour |
| Behind an f/2.8 lens | 1/40 | ~7 hours full sun |
| Behind the f/300 pinhole box | 1/450,000 | ~8 years |

In-camera cyanotypes exist, made with big fast lenses over a day, and they
mostly record sky because UV drives the reaction. Through a pinhole it is
not a thing. Salt prints, anthotypes, lumen prints and chlorophyll prints are
slower still.

## Cyanotype as the print side: yes

This is the fit. The relay camera captures; the file is inverted and printed
on inkjet transparency; the transparency is contact printed by hand in sun or
under a UV lamp. It closes the loop between digital capture and hand
printing, and hangs beside the film pinholes as one body of work.

- The pinhole image carries ~200 real points across. A rough transparency
  loses nothing.
- Chemistry: ferric ammonium citrate + potassium ferricyanide, mixed 1:1
  before coating. Safest of the historical processes. Develop by rinsing in
  water. About $20 covers a show's worth of prints.
- Coat with a foam brush on watercolor paper, dry in the dark, expose 5 to
  20 minutes in sun (or a UV nail lamp / face-tanner tube box), rinse until
  the water runs clear, dry. Blue deepens over 24 hours.
- Tone in strong tea or coffee for brown-black; bleach lightly in washing
  soda first for split tones.
- Digital negative: invert, then apply a curve so the print's tonal range
  matches (cyanotype needs a dense, contrasty negative). Print on Pictorico
  or any inkjet transparency; a laser-printer overhead transparency works at
  the low end.

Experiment worth an afternoon: print the negative on the receipt printer
(see [05-thermal-paper.md](05-thermal-paper.md)), oil the receipt to make it
translucent, and contact print from that. Oiled paper negatives are a
classic technique. Open question is whether the thermal dye blocks enough
UV to print with contrast.

## In-camera chemistry you can do yourself

Silver paper, the same as in the film boxes, with two ways to make it more
homebrew, plus one no-development route.

- **Caffenol developer.** Instant coffee, washing soda (sodium carbonate)
  and vitamin C (ascorbic acid). Develops paper and film. Stop in water or
  dilute vinegar. Fix in sodium thiosulfate, sold as pool and aquarium
  dechlorinator. Nothing that can't come from a grocery and a pool store.
- **Hand-coated emulsion.** Liquid silver emulsion (Foma, Liquid Light)
  brushed onto paper, glass, wood, ceramic. Roughly ISO 1 to 3. Minutes in
  sun through a pinhole. Develop and fix as paper. Making the emulsion from
  scratch (silver nitrate + potassium bromide in gelatin) is a deeper rabbit
  hole, documented at The Light Farm.
- **Solargraphy.** Photo paper in a pinhole can, weeks to months of
  exposure, no developer. The latent image prints out visibly. Scan it (once;
  scanning light degrades it) and invert. Uses the cameras already built.

## Rough speed ladder

| Process | Approx. ISO | Pinhole exposure in sun at ~f/200 | Where it works |
|---|---|---|---|
| Silver gelatin paper | 3 to 6 | tens of seconds to minutes | in camera |
| Liquid emulsion / dry plate | 1 to 3 | minutes | in camera |
| Wet collodion | ~0.5 | minutes, must stay wet | in camera, not low-fi |
| Cyanotype | ~1e-6 | years | contact only |
| Salt print | lower than cyanotype | no | contact only |
| Anthotype | days in a contact frame | no | contact only |

ISO figures for the contact processes are back-of-envelope from contact
times and mean nothing beyond ordering.

## Where this leaves the project

Two chemical outputs sit naturally on the relay box:

1. A receipt printer for the instant, fading take-away.
2. A digital negative and hand-coated cyanotype for the wall.

And the film boxes keep doing what they do, now with caffenol if the point
is to own every step.

## Wet plate collodion (the Instagram "flow it on a glass plate" process)

Bare glass to finished image in about fifteen minutes, every step wet. The
tacky set after pouring looks like drying but is not; once collodion truly
dries it loses almost all sensitivity, so the window is ~10 to 15 minutes.

1. Pour salted collodion onto the plate, tilt to flow to the corners, drain
   the excess off one corner. Sets to a gel in about a minute.
2. Silver nitrate bath, 3 to 5 minutes, in the dark. This sensitizes it.
3. Load wet, expose, develop within minutes (iron sulfate developer). Fix in
   plain hypo. Rinse, dry, varnish (sandarac / lavender oil).

Glass with black backing = ambrotype. Blackened aluminum = tintype. Both are
direct positives, one of a kind. Most people online shoot tintypes on
"trophy aluminum" because it is cheap and does not break.

Speed ~ISO 0.5 to 1, blue and UV sensitive only: skies white, reds black.

| Setup | Exposure in full sun |
|---|---|
| Lens camera at f/4 | ~1 s |
| Pinhole at f/200 | ~5 min |
| Pinhole at f/300, open shade | ~30 min, plate dries out first |

Wet plate pinhole in sun works. Shade and overcast run out the clock.

Hazards, complete list: collodion is ether + alcohol (no flames, ventilate);
silver nitrate stains skin black for a week and is caustic to eyes (gloves,
glasses); choose a cadmium-free collodion formula; fix in sodium thiosulfate
rather than the traditional potassium cyanide. Kits: Bostick & Sullivan and
similar.

**Dry-plate cousin without the timer:** liquid silver emulsion flowed onto
glass the same way, dried in the dark, stored for weeks. ISO 1 to 3, develops
in paper developer, gives a negative not a direct positive. Same look on
glass, no wet window.

**Design implication for the relay box:** make the back swappable. One back
holds the matte screen and the Pi camera; another is a 4x5 or 5x7 plate
holder. Same pinhole, same box, digital frames for the screen and plates for
the wall.

## Old processes with no fixer

Recalled from an Instagram video: a very old process, glass plate, flowed or
wiped on, dried, exposed and developed immediately, possibly no fixer. If the
no-fixer memory is right it is not collodion (which needs a fix, and the fix
is the dramatic clearing moment). Candidates, oldest first:

- **Bitumen heliograph, Niépce 1826.** Bitumen of Judea in lavender oil,
  flowed on pewter or glass, dried. Light hardens it. Develop by washing in
  lavender oil + petroleum, dissolving the unexposed parts. No fixer because
  nothing is left to fix. The oldest photograph. Hours to days of full sun
  with a lens.
- **Physautotype, Niépce & Daguerre 1832.** Lavender oil residue in alcohol
  flowed on a silver plate, dries white. Expose, develop over petroleum
  vapor. Direct positive, no fixer. Hours.
- **Dichromated gelatin / gum, 1850s (Talbot, Poitevin).** Gelatin +
  potassium dichromate flowed on glass, dried. Light hardens it. Develop in
  warm water. No fixer. Minutes in a contact frame. Hexavalent chromium:
  handle accordingly.
- **Cyanotype on glass, Herschel 1842.** Gelatin-subbed glass, water wash.
  No fixer. Contact only.
- **Calotype, Talbot 1841** (if "glass" is the fuzzy part). Silver nitrate
  brushed onto iodized paper, exposed damp, developed immediately in gallic
  acid. Originally stabilized with salt/bromide rather than fixed. Works in
  a camera: ~1 min at f/15 in sun, so roughly half an hour through a
  pinhole. The closest "wipe on, expose, develop now" process a pinhole box
  can actually use.

### Why no-fixer means slow

In every fixer-free process, light does the whole job directly by changing
the solubility of the coating. In silver processes light makes only a faint
latent image and the developer amplifies it by roughly 10^9. Fixer exists to
clear the unexposed silver the developer left behind. No fixer means no
amplification, which means on the order of 10^4 to 10^6 times more light.
Every no-fixer process is therefore contact-print speed or
hours-with-a-fast-lens speed, never pinhole speed.

| Process | Fixer | Speed in camera | Pinhole viable |
|---|---|---|---|
| Wet collodion | yes | ~5 min at f/200 in sun | yes |
| Calotype paper negative | salt stabilizer, later hypo | ~1 min at f/15 in sun | marginal, ~30 min |
| Dichromated gelatin | none | contact only | no |
| Bitumen heliograph | none | hours with a lens | no |
| Cyanotype | none | contact only | no |

Open: find the account and identify the actual process.

Piece idea: bitumen heliograph in a lens camera obscura. A plate that takes
all day to expose, developed in lavender oil, no darkroom at all.
