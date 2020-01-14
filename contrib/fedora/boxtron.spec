%global __python %{__python3}
%global steam_dir %{_datadir}/steam
%global gittag v%{version}

Name:      boxtron
Version:   0.5.3
Release:   1%{?dist}
BuildArch: noarch
Summary:   Steam Play Compatibility tool to run DOS games

License:   GPLv2
URL:       https://github.com/dreamer/boxtron
Source:    https://github.com/dreamer/boxtron/archive/%{gittag}/%{name}-%{version}.tar.gz

Requires:  dosbox inotify-tools timidity++ fluid-soundfont-gm

%description
Boxtron is a compatibility tool to run DOS games via Steam or other GUI
game launchers using native Linux DOSBox.

%prep
%autosetup -n boxtron-%{version}

%build

%install
%make_install prefix=/usr
%py_byte_compile %{__python3} %{buildroot}%{_datadir}/%{name}

%files
%license LICENSE
%doc README.md
%{steam_dir}/compatibilitytools.d/%{name}.vdf
{_datadir}/%{name}
%{_bindir}/install-gog-game

%changelog
* Thu Nov 28 2019 Patryk Obara <dreamer.tan@gmail.com> 0.5.3-1
- Initial release
