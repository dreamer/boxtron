.PHONY: lint test coverage \
	check-formatting pretty-code \
	install uninstall \
	user-install user-uninstall \
	clean shortlog \
	compatibilitytool.vdf version.py

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
	compatibilitytool.vdf \
	toolmanifest.vdf \
	LICENSE \
	README.md

ifeq ($(origin XDG_DATA_HOME), undefined)
	data_home := ${HOME}/.local/share
else
	data_home := ${XDG_DATA_HOME}
endif

# These two variables are to be overriden by packagers, for situations
# when source code is downloaded as a tarball, e.g.:
#
# make prefix=/usr version=v%{version} install
#
prefix = /usr/local
version = $(shell git describe --tags --dirty)

install_dir = $(DESTDIR)$(prefix)/share/steam/compatibilitytools.d/$(tool_dir)
devel_install_dir = $(data_home)/Steam/compatibilitytools.d/$(tool_dir_dev)

lint: version.py
	shellcheck scripts/codestyle.sh tests/coverage-report.sh
	pylint --rcfile=.pylint run-dosbox install-gog-game *.py tests/*.py scripts/*.py

test: preconfig.tar
	XDG_CONFIG_HOME=$(shell pwd)/tests/files/xdg_config_home \
	BOXTRON_QUIET=1 python3 -m unittest discover -v -s tests

coverage: preconfig.tar
	bash tests/coverage-report.sh 2> /dev/null

compatibilitytool.vdf: compatibilitytool.template
	sed 's/%name%/$(tool_name)/; s/%display_name%/$(tool_name_display)/' $< > $@

version.py:
	@echo "# pylint: disable=missing-docstring" > $@
	@echo "VERSION = '$(version)'" >> $@

preconfig.tar: $(shell find preconfig -type f | sed 's/\ /\\ /g')
	@tar \
	    --format=v7 --mode='a+rwX,o-w' \
	    --owner=0 --group=0 --mtime='@1560859200' \
	    -cf $@ $(shell find preconfig -type f | sed 's/\ /\\ /g' | sort) \
	    --transform='s|DIR_UP|..|'

$(tool_dir).zip: $(files)
	mkdir -p $(tool_dir)
	cp --reflink=auto -t $(tool_dir) $^
	zip $@ $(tool_dir)/*
	rm -rf $(tool_dir)
	./run-dosbox --version

$(tool_dir).tar.xz: $(files)
	mkdir -p $(tool_dir)
	cp --reflink=auto -t $(tool_dir) $^
	tar -cJf $@ $(tool_dir)
	rm -rf $(tool_dir)
	./run-dosbox --version

# TODO install-gog-game should actually go into a bindir
install: $(files)
	mkdir -p $(install_dir)
	cp --reflink=auto -t $(install_dir) $^

uninstall:
	rm -rf $(install_dir)

user-install: tool_name = $(tool_name_dev)
user-install: tool_name_display = $(tool_name_display_dev)
user-install: $(files)
	mkdir -p $(devel_install_dir)
	cp --reflink=auto -t $(devel_install_dir) $^

user-uninstall:
	rm -rf $(devel_install_dir)

clean:
	rm -f compatibilitytool.vdf
	rm -f version.py
	rm -f preconfig.tar
	rm -f $(tool_dir).tar.xz
	rm -f $(tool_dir).zip

# Summary to be included in CHANGELOG.md
shortlog:
	git shortlog $(shell git describe --tags --abbrev=0)..HEAD

check-formatting:
	yapf --version
	yapf -d -vv run-dosbox install-gog-game *.py scripts/*.py
	bash scripts/codestyle.sh --max-line-length=80 \
		run-dosbox install-gog-game *.py tests/*.py scripts/*.py

pretty-code:
	yapf -i -vv run-dosbox install-gog-game *.py
	git status
