%define name tremulous
%define version 1.1.0
%define release %mkrel 3

%define srcname %{name}-%{version}-src
%define gamelibdir %{_libdir}/games/%{name}

Summary: An open source game that blends a team based FPS with elements of an RTS.
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://ovh.dl.sourceforge.net/sourceforge/tremulous/%{name}-%{version}.zip
# http://www.gnome-look.org/content/show.php?content=42942
Source1: http://www.gnome-look.org/content/files/42942-Tremulous2.png
License: GPL 
Group: Games/Arcade
Url: http://tremulous.net
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Buildrequires: libSDL-devel libopenal-devel mesagl-devel
Requires: %name-maps

%description
Tremulous is a free, open source game that blends a team based FPS
with elements of an RTS.
Players can choose from 2 unique races, aliens and humans. 
Players on both teams are able to build working structures in-game like an RTS.
These structures provide many functions, the most important being spawning.
The designated builders must ensure there are spawn structures or 
other players will not be able to rejoin the game after death.
Other structures provide automated base defense (to some degree), 
healing functions and much more...

Player advancement is different depending on which team you are on.
As a human, players are rewarded with credits for each alien kill.
These credits may be used to purchase new weapons and upgrades from the Armoury
The alien team advances quite differently. Upon killing a human foe,
the alien is able to evolve into a new class.
The more kills gained the more powerful the classes available.

The overall objective behind Tremulous is to eliminate the opposing team.
This is achieved by not only killing the opposing players but also 
removing their ability to respawn by destroying their spawn structures.

# I did a separate package for the maps
# Maps are hudge, so if the binairy is getting better, we'll be able
# to provide a newest small binary but users will keep their maps
# There's no need to update the maps until they don't change ;)
%package maps
Summary: Maps for Tremulous 
License: CC 
Group: Games/Arcade
Requires: %name

%description maps
Provides the pk3 files needed for tremulous

%prep
%setup -q -n %name
# I know it's crappy but the project only provides the zip file
# This zip file contains the pak files the tar.gz doesn't provides
# I found cleaner to build the rpm from the original zip file
# instead of manually splitting the files
tar -xvzf %{srcname}.tar.gz

%build
make -C %{srcname}

%install
rm -rf %{buildroot}
install -d %{buildroot}%{gamelibdir}/base
install -m 644 base/*.{cfg,pk3} %{buildroot}%{gamelibdir}/base
pushd %{srcname}/build/release-*
  exec=`basename %{name}.*`
  arch=${exec#%{name}.}
  install -m 755 *.$arch %{buildroot}%{gamelibdir}
popd
install -d %{buildroot}%{_gamesbindir}
cat > %{buildroot}%{_gamesbindir}/%{name} <<EOF
#!/bin/sh
cd %{gamelibdir}
exec ./%{name}.$arch \$*
EOF
chmod 755 $RPM_BUILD_ROOT%{_gamesbindir}/%{name}

install -D -m 644 %{SOURCE1} %{buildroot}%{_datadir}/icons/%{name}.png

install -d %{buildroot}%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Tremulous
Comment=Team based FPS/RTS
Exec=soundwrapper %_gamesbindir/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Game;ArcadeGame;X-MandrivaLinux-MoreApplications-Games-Arcade;
EOF

%clean
rm -rf %{buildroot}

%post
%update_menus

%postun
%clean_menus

%files
%defattr(-,root,root)
%doc COPYING GPL ChangeLog manual.pdf
%{_gamesbindir}/%{name}
%{gamelibdir}/%{name}.*
%{gamelibdir}/tremded.*
%dir %{gamelibdir}
%dir %{gamelibdir}/base
%{gamelibdir}/base/*cfg
%{_datadir}/icons/%{name}.png
%{_datadir}/applications/mandriva-%{name}.desktop

%files maps
%defattr(-,root,root)
%doc COPYING CC
%{gamelibdir}/base/*pk3


