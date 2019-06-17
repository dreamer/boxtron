.PHONY: lint test coverage \
	check-formatting pretty-code \
	install uninstall \
	user-install user-uninstall \
	clean version.py shortlog

tool_dir = steam-dos

files = run-dosbox \
	install-gog-game \
	confgen.py \
	fsl.py \
	midi.py \
	preconfig.py \
	preconfig.tar \
	settings.py \
	toolbox.py \
	tweaks.py \
	version.py \
	winpathlib.py \
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
devel_install_dir = $(data_home)/Steam/compatibilitytools.d/$(tool_dir)-dev


lint: version.py
	shellcheck codestyle.sh tests/coverage-report.sh
	pylint --rcfile=.pylint run-dosbox install-gog-game *.py tests/*.py

test: preconfig.tar
	XDG_CONFIG_HOME=$(shell pwd)/tests/files/xdg_config_home \
	python3 -m unittest discover -v -s tests

coverage: preconfig.tar
	bash tests/coverage-report.sh 2> /dev/null

version.py:
	@echo "# pylint: disable=missing-docstring" > $@
	@echo "VERSION = '$(version)'" >> $@

preconfig.tar: preconfig
	tar --owner=0 --group=0 --mtime='2019-06-17 00:13:37' -cf $@ $<

$(tool_dir).zip: $(files)
	mkdir -p $(tool_dir)
	cp --reflink=auto -t $(tool_dir) $^
	zip $@ $(tool_dir)/*
	rm -rf $(tool_dir)

$(tool_dir).tar.xz: $(files)
	mkdir -p $(tool_dir)
	cp --reflink=auto -t $(tool_dir) $^
	tar -cJf $@ $(tool_dir)
	rm -rf $(tool_dir)

# TODO install-gog-game should actually go into a bindir
install: $(files)
	mkdir -p $(install_dir)
	cp --reflink=auto -t $(install_dir) $^

uninstall:
	rm -rf $(install_dir)

user-install: $(files)
	mkdir -p $(devel_install_dir)
	cp --reflink=auto -t $(devel_install_dir) $^

user-uninstall:
	rm -rf $(devel_install_dir)

clean:
	rm -f version.py
	rm -f preconfig.tar
	rm -f $(tool_dir).tar.xz
	rm -f $(tool_dir).zip

# Summary to be included in CHANGELOG.md
shortlog:
	git shortlog $(shell git describe --tags --abbrev=0)..HEAD

check-formatting:
	bash codestyle.sh run-dosbox install-gog-game *.py tests/*.py
	yapf -d -vv run-dosbox install-gog-game *.py

pretty-code:
	yapf -i -vv run-dosbox install-gog-game *.py
	git status
