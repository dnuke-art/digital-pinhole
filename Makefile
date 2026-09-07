# Digital pinhole: regenerate every mockup from source.
#   make            build all sheets and the 3D render
#   make looks      simulated output looks        -> mockups/out/looks_sheet.png
#   make diagrams   cross-section diagrams        -> mockups/out/diagrams_sheet.png
#   make experiments  odd apertures + dithers     -> mockups/out/experiments_sheet.png, dither_sheet.png
#   make gratings   grating + zone plate          -> mockups/out/grating_sheet.png
#   make render     3D section of the relay box   -> mockups/out/render_relay_cutaway.png
#   make photos     fetch the sample photos (picsum.photos) into mockups/src
#   make deps       check python modules and openscad
#   make clean      remove generated images; make distclean also removes the sample photos

PYTHON   ?= python3
OPENSCAD ?= openscad
M        := mockups
SRC      := $(M)/src
OUT      := $(M)/out

PHOTO_IDS := 1005 1015 1027 1040
PHOTOS    := $(addprefix $(SRC)/pic_,$(addsuffix .jpg,$(PHOTO_IDS)))

LOOKS       := $(OUT)/looks_sheet.png
DIAGRAMS    := $(OUT)/diagrams_sheet.png
EXPERIMENTS := $(OUT)/experiments_sheet.png
DITHERS     := $(OUT)/dither_sheet.png
GRATINGS    := $(OUT)/grating_sheet.png
RENDER      := $(OUT)/render_relay_cutaway.png

.PHONY: all looks diagrams experiments gratings render photos deps clean distclean help
.DELETE_ON_ERROR:

all: looks diagrams experiments gratings render

looks:       $(LOOKS)
diagrams:    $(DIAGRAMS)
experiments: $(EXPERIMENTS)
gratings:    $(GRATINGS)
render:      $(RENDER)
photos:      $(PHOTOS)

$(SRC)/pic_%.jpg:
	@mkdir -p $(SRC)
	curl -sSL --fail -m 60 -o $@ "https://picsum.photos/id/$*/1200/900"

$(LOOKS): $(M)/looks.py $(PHOTOS)
	$(PYTHON) $(M)/looks.py

$(DIAGRAMS): $(M)/diagrams.py
	$(PYTHON) $(M)/diagrams.py

# looks2 writes both the experiments and the dither sheet; it imports looks.py
$(EXPERIMENTS) $(DITHERS) &: $(M)/looks2.py $(M)/looks.py $(PHOTOS)
	$(PYTHON) $(M)/looks2.py

$(GRATINGS): $(M)/looks3.py $(M)/looks2.py $(M)/looks.py $(PHOTOS)
	$(PYTHON) $(M)/looks3.py

$(RENDER): $(M)/render3d.py
	$(PYTHON) $(M)/render3d.py

deps:
	@$(PYTHON) -c "import numpy, PIL, matplotlib, scipy" && echo "python: numpy PIL matplotlib scipy ok" || (echo "missing: pip install numpy pillow matplotlib scipy"; exit 1)
	@$(PYTHON) -c "import build123d" 2>/dev/null && echo "python: build123d ok" || echo "build123d missing (only needed for 'make render'): pip install build123d"
	@command -v $(OPENSCAD) >/dev/null && echo "openscad: $$($(OPENSCAD) --version 2>&1 | head -1)" || echo "openscad missing (only needed for 'make render')"

clean:
	rm -rf $(OUT)

distclean: clean
	rm -f $(PHOTOS)

help:
	@sed -n '2,12p' $(MAKEFILE_LIST)
