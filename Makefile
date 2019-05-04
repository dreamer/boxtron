.PHONY: install uninstall dist clean

tool_dir = steam-dos-0.1

files = compatibilitytool.vdf \
	toolmanifest.vdf

steam_dir = ${HOME}/.local/share/Steam
install_dir = $(steam_dir)/compatibilitytools.d/$(tool_dir)

dist: $(files)
	install -D -t $(tool_dir) $^
	tar -cJf $(tool_dir).tar.xz $(tool_dir)

install: $(files)
	install -D -t $(install_dir) $^

clean:
	rm -rf $(tool_dir)
	rm $(tool_dir).tar.xz

uninstall:
	rm -rf $(install_dir)
