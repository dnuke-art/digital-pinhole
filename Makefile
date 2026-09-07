# Digital pinhole: regenerate every mockup from source.
#   make            build all sheets and the 3D render
#   make looks      simulated output looks        -> mockups/out/looks_sheet.png
#   make diagrams   cross-section diagrams        -> mockups/out/diagrams_sheet.png
#   make experiments  odd apertures + dithers     -> mockups/out/experiments_sheet.png, dither_sheet.png
#   make gratings   grating + zone plate          -> mockups/out/grating_sheet.png
#   make render     3D section of the relay box   -> mockups/out/render_relay_cutaway.png
#   make curved     curved gratings               -> mockups/out/curved_grating_sheet.png
#   make optics     FreeCAD Optics Workbench ray traces -> mockups/out/optics_*.png (needs the FreeCAD AppImage in /opt + the addon)
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
CURVED      := $(OUT)/curved_grating_sheet.png
OPTICS      := $(OUT)/optics_grating.png $(OUT)/optics_rowland.png
# FreeCAD, headless. Prefer the AppImage under /opt via its freecadcmd entry point; fall back to an extracted freecadcmd.
# Needs QT_QPA_PLATFORM=offscreen or it waits for a display. Do not use '--console': it drops into an
# interactive prompt after the script and never exits under make.
FREECAD_APPIMAGE ?= $(firstword $(wildcard /opt/FreeCAD*.AppImage))
FREECADCMD       ?= $(if $(FREECAD_APPIMAGE),$(FREECAD_APPIMAGE) freecadcmd,$(firstword $(wildcard $(HOME)/.cache/featuretree/freecad/squashfs-root/usr/bin/freecadcmd /tmp/squashfs-root/usr/bin/freecadcmd) freecadcmd))

.PHONY: all looks diagrams experiments gratings curved render optics photos deps clean distclean help
.DELETE_ON_ERROR:

all: looks diagrams experiments gratings curved render

looks:       $(LOOKS)
diagrams:    $(DIAGRAMS)
experiments: $(EXPERIMENTS)
gratings:    $(GRATINGS)
render:      $(RENDER)
curved:      $(CURVED)
optics:      $(OPTICS)
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

$(CURVED): $(M)/looks4.py $(M)/looks3.py $(M)/looks2.py $(M)/looks.py $(PHOTOS)
	$(PYTHON) $(M)/looks4.py

# FreeCAD Optics Workbench ray traces. Not part of 'all': needs FreeCAD's own python (the AppImage) and the
# OpticsWorkbench addon (git clone https://github.com/chbergmann/OpticsWorkbench ~/.local/share/FreeCAD/Mod/OpticsWorkbench).
$(OUT)/optics_%.json: $(M)/fc_optics.py
	@mkdir -p $(OUT)
	QT_QPA_PLATFORM=offscreen SCENE=$* OUT_JSON=$(abspath $@) $(FREECADCMD) $(M)/fc_optics.py < /dev/null

$(OUT)/optics_%.png: $(OUT)/optics_%.json $(M)/optics_plot.py $(M)/looks3.py
	$(PYTHON) $(M)/optics_plot.py $<

deps:
	@$(PYTHON) -c "import numpy, PIL, matplotlib, scipy" && echo "python: numpy PIL matplotlib scipy ok" || (echo "missing: pip install numpy pillow matplotlib scipy"; exit 1)
	@$(PYTHON) -c "import build123d" 2>/dev/null && echo "python: build123d ok" || echo "build123d missing (only needed for 'make render'): pip install build123d"
	@command -v $(OPENSCAD) >/dev/null && echo "openscad: $$($(OPENSCAD) --version 2>&1 | head -1)" || echo "openscad missing (only needed for 'make render')"
	@[ -x "$(firstword $(FREECADCMD))" ] && echo "freecad: $(FREECADCMD)" || echo "freecad missing (only needed for 'make optics'): put the AppImage in /opt or set FREECADCMD"
	@[ -d "$(HOME)/.local/share/FreeCAD/Mod/OpticsWorkbench" ] && echo "OpticsWorkbench addon ok" || echo "OpticsWorkbench addon missing (only needed for 'make optics')"

clean:
	rm -rf $(OUT)

distclean: clean
	rm -f $(PHOTOS)

help:
	@sed -n '2,12p' $(MAKEFILE_LIST)
