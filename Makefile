.PHONY: lint test coverage clean \
	check-formatting pretty-code \
	install uninstall dev-install dev-uninstall \
	compatibilitytool.vdf boxtron.vdf

# These variables are used to generate compatibilitytool.vdf:
#
tool_name             = boxtron
tool_name_dev         = boxtron_dev
tool_name_display     = Boxtron (native DOSBox)
tool_name_display_dev = Boxtron (dev)

# Default names for installation directories:
#
tool_dir              = boxtron
tool_dir_dev          = boxtron-dev

files = run-dosbox \
	install-gog-game \
	confgen.py \
	cuescanner.py \
	fakescripteval.py \
	fakesierralauncher.py \
	log.py \
	midi.py \
	preconfig.py \
	preconfig.tar \
	settings.py \
	toolbox.py \
	tweaks.py \
	version.py \
	winpathlib.py \
	xdg.py \
	xlib.py \
	toolmanifest.vdf \
	LICENSE \
	README.md

ifeq ($(origin XDG_DATA_HOME), undefined)
	data_home := ${HOME}/.local/share
else
	data_home := ${XDG_DATA_HOME}
endif

# See PACKAGING.md for detailed description about supported installation options.
#
prefix = /usr/local
devel_install_dir = $(data_home)/Steam/compatibilitytools.d/$(tool_dir_dev)

lint:
	shellcheck scripts/codestyle.sh tests/coverage-report.sh
	pylint --rcfile=.pylint run-dosbox install-gog-game *.py tests/*.py scripts/*.py

test: preconfig.tar
	XDG_CONFIG_HOME=$(shell pwd)/tests/files/xdg_config_home \
	BOXTRON_QUIET=1 python3 -m unittest discover -v -s tests

coverage: preconfig.tar
	bash tests/coverage-report.sh 2> /dev/null

boxtron.vdf: compatibilitytool.template
	sed 's/%name%/$(tool_name)/; s/%display_name%/$(tool_name_display)/; s|%path%|$(tool_vdf_path)|;' \
	    $< > $@

compatibilitytool.vdf: compatibilitytool.template
	sed 's/%name%/$(tool_name)/; s/%display_name%/$(tool_name_display)/; s|%path%|.|;' \
	    $< > $@

preconfig.tar: $(shell find preconfig -type f | sed 's/\ /\\ /g')
	@tar \
	    --format=v7 --mode='a+rwX,o-w' \
	    --owner=0 --group=0 --mtime='@1560859200' \
	    -cf $@ $(shell find preconfig -type f | sed 's/\ /\\ /g' | sort) \
	    --transform='s|DIR_UP|..|'

$(tool_dir).zip: compatibilitytool.vdf $(files)
	mkdir -p $(tool_dir)
	cp --reflink=auto -t $(tool_dir) $^
	zip $@ $(tool_dir)/*
	rm -rf $(tool_dir)
	./run-dosbox --version

$(tool_dir).tar.xz: compatibilitytool.vdf $(files)
	mkdir -p $(tool_dir)
	cp --reflink=auto -t $(tool_dir) $^
	tar -cJf $@ $(tool_dir)
	rm -rf $(tool_dir)
	./run-dosbox --version

install: tool_vdf_path = $(prefix)/share/boxtron
install: boxtron.vdf $(files)
	install -m 644 -Dt "$(DESTDIR)$(prefix)/share/steam/compatibilitytools.d/" boxtron.vdf
	install        -Dt "$(DESTDIR)$(prefix)/bin/"                              install-gog-game
	install        -Dt "$(DESTDIR)$(prefix)/share/boxtron/"                    run-dosbox
	install -m 644 -Dt "$(DESTDIR)$(prefix)/share/boxtron/"                    *.py
	install -m 644 -Dt "$(DESTDIR)$(prefix)/share/boxtron/"                    preconfig.tar
	install -m 644 -Dt "$(DESTDIR)$(prefix)/share/boxtron/"                    toolmanifest.vdf
	install -m 644 -Dt "$(DESTDIR)$(prefix)/share/doc/boxtron/"                README.md
	install -m 644 -Dt "$(DESTDIR)$(prefix)/share/licenses/boxtron"            LICENSE
	@echo
	@echo 'Restart Steam, so it can pick up new compatibility tool.'
	@echo 'You can type "make uninstall" to remove Boxtron.'

uninstall:
	rm    "$(DESTDIR)$(prefix)/bin/install-gog-game"
	rm    "$(DESTDIR)$(prefix)/share/boxtron"/*
	rmdir "$(DESTDIR)$(prefix)/share/boxtron"
	rm    "$(DESTDIR)$(prefix)/share/doc/boxtron"/*
	rmdir "$(DESTDIR)$(prefix)/share/doc/boxtron"
	rm    "$(DESTDIR)$(prefix)/share/licenses/boxtron"/*
	rmdir "$(DESTDIR)$(prefix)/share/licenses/boxtron"
	rm    "$(DESTDIR)$(prefix)/share/steam/compatibilitytools.d/boxtron.vdf"
	rmdir --ignore-fail-on-non-empty "$(DESTDIR)$(prefix)/share/steam/compatibilitytools.d"
	rmdir --ignore-fail-on-non-empty "$(DESTDIR)$(prefix)/share"/{doc,licenses,steam}

dev-install: tool_name = $(tool_name_dev)
dev-install: tool_name_display = $(tool_name_display_dev)
dev-install: compatibilitytool.vdf $(files)
	mkdir -p $(devel_install_dir)
	cp --reflink=auto -t $(devel_install_dir) $^

dev-uninstall:
	rm -rf $(devel_install_dir)

clean:
	rm -f boxtron.vdf
	rm -f compatibilitytool.vdf
	rm -f preconfig.tar
	rm -f $(tool_dir).tar.xz
	rm -f $(tool_dir).zip

check-formatting:
	yapf --version
	yapf -d -vv run-dosbox install-gog-game *.py scripts/*.py
	bash scripts/codestyle.sh --max-line-length=80 \
		run-dosbox install-gog-game *.py tests/*.py scripts/*.py

pretty-code:
	yapf -i -vv run-dosbox install-gog-game *.py
	git status
