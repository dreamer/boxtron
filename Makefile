.PHONY: lint test coverage install uninstall clean version.py

# major.minor part of version of this release
# TODO inject it into .vdf files, so manual tweak won't be
# needed. Also, make sure it's compatible with the latest tag.
version_major_minor = 0.2

tool_dir = steam-dos-$(version_major_minor)

files = run_dosbox \
	confgen.py \
	midi.py \
	settings.py \
	toolbox.py \
	tweaks.py \
	version.py \
	compatibilitytool.vdf \
	toolmanifest.vdf \
	LICENSE

steam_dir = ${HOME}/.local/share/Steam
install_dir = $(steam_dir)/compatibilitytools.d/$(tool_dir)

lint: version.py
	shellcheck $(shell find . -name *.sh)
	pylint --rcfile=.pylint run_dosbox *.py tests/*.py
	pycodestyle run_dosbox *.py tests/*.py

test:
	python3 -m unittest discover -v -s tests

coverage:
	bash tests/coverage-report.sh

version.py:
	@printf "# pylint: disable=missing-docstring\n" > $@
	@printf "VERSION = '%s'\n" \
		$(shell git describe --tags --dirty --long) >> $@

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

install: $(files)
	mkdir -p $(install_dir)
	cp --reflink=auto -t $(install_dir) $^

clean:
	rm -f version.py
	rm -f $(tool_dir).tar.xz
	rm -f $(tool_dir).zip

uninstall:
	rm -rf $(install_dir)
