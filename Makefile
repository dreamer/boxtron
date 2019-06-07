.PHONY: lint test coverage install uninstall clean version.py shortlog \
	check-formatting pretty-code

tool_dir = steam-dos

files = run-dosbox \
	install-gog-game \
	confgen.py \
	midi.py \
	settings.py \
	toolbox.py \
	tweaks.py \
	version.py \
	winpathlib.py \
	compatibilitytool.vdf \
	toolmanifest.vdf \
	LICENSE \
	README.md

steam_dir = ${HOME}/.local/share/Steam
install_dir = $(steam_dir)/compatibilitytools.d/$(tool_dir)

lint: version.py
	shellcheck codestyle.sh tests/coverage-report.sh
	pylint --rcfile=.pylint run-dosbox install-gog-game *.py tests/*.py
	bash codestyle.sh run-dosbox install-gog-game *.py tests/*.py

test:
	XDG_CONFIG_HOME=$(shell pwd)/tests/files/xdg_config_home \
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

# Summary to be included in CHANGELOG.md
shortlog:
	git shortlog $(shell git describe --tags --abbrev=0)..HEAD

check-formatting:
	yapf -d -vv run-dosbox install-gog-game *.py

pretty-code:
	yapf -i -vv run-dosbox install-gog-game *.py
	git status
