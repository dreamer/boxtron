.PHONY: lint install uninstall clean

tool_dir = steam-dos-0.1

files = run_dosbox \
	compatibilitytool.vdf \
	toolmanifest.vdf

steam_dir = ${HOME}/.local/share/Steam
install_dir = $(steam_dir)/compatibilitytools.d/$(tool_dir)

lint:
	pycodestyle-3 run_dosbox
	pylint run_dosbox

$(tool_dir).tar.xz: $(files)
	mkdir -p $(tool_dir)
	cp --reflink=auto -t $(tool_dir) $^
	tar -cJf $(tool_dir).tar.xz $(tool_dir)
	rm -rf $(tool_dir)

install: $(files)
	mkdir -p $(install_dir)
	cp --reflink=auto -t $(install_dir) $^

clean:
	rm -f $(tool_dir).tar.xz

uninstall:
	rm -rf $(install_dir)
