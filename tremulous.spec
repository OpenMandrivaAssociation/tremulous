%define client_release 1.011
%define srcname Release_%{client_release}
%define gamelibdir %{_libdir}/games/%{name}

Summary:	An open source game that blends a team based FPS with elements of an RTS
Name:		tremulous
Version:	1.1.0
Release:	13
Source0:	http://ovh.dl.sourceforge.net/sourceforge/tremulous/%{name}-%{version}.zip
# http://www.gnome-look.org/content/show.php?content=42942
Source1:	http://www.gnome-look.org/content/files/42942-Tremulous2.png

# The original client is generating troubles on x64.
# kevlarman from the tremulous irc chan consider svn://source.mercenariesguild.net/client better
# In the fact, it works far better
# Tremulous 1.2 will make that workaround useless
Source2:	%{name}-client-%{client_release}.tar.bz2
Source3:	tremulous.rpmlintrc
Patch0:		%name-1725.patch
License:	GPL 
Group:		Games/Arcade
Url:		http://tremulous.net
BuildRequires:	libSDL-devel
BuildRequires:	libopenal-devel
BuildRequires:	mesagl-devel
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	mesaglu-devel
Requires:	%{name}-maps

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
Summary:	Maps for Tremulous 
License:	CC 
Group:		Games/Arcade
Requires:	%name

%description maps
Provides the pk3 files needed for tremulous

%prep
%setup -q -n %name
# I know it's crappy but the project only provides the zip file
# This zip file contains the pak files the tar.gz doesn't provides
# I found cleaner to build the rpm from the original zip file
# instead of manually splitting the files
tar -xvjf %SOURCE2
cd %{srcname}
%patch0 -p1

%build
make -C %{srcname}

%install
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

%files
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




%changelog
* Tue Oct 13 2009 Erwan Velu <erwan@mandriva.org> 1.1.0-9mdv2010.0
+ Revision: 457200
- Using the mercenariesguild solves some x64 issues
  It also fix many more bugs of the game

* Mon Oct 05 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.1.0-8mdv2010.0
+ Revision: 454313
- rebuild for new libopenal

* Mon Oct 05 2009 Erwan Velu <erwan@mandriva.org> 1.1.0-7mdv2010.0
+ Revision: 453888
- Adding two patches : one for prevent a gcc error, another to prevent a memory corruption
- Rebuild

  + Thierry Vignaud <tvignaud@mandriva.com>
    - rebuild
    - rebuild
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request
    - fix summary-ended-with-dot
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot


* Thu Jan 04 2007 Olivier Blin <oblin@mandriva.com> 1.1.0-3mdv2007.0
+ Revision: 103939
- fix wrapper script

* Fri Dec 01 2006 Olivier Blin <oblin@mandriva.com> 1.1.0-2mdv2007.1
+ Revision: 89884
- buildrequires mesagl-devel
- add icon and menu entry
- add a wrapper in _gamesbindir and install data files in _libdir/games
- Import tremulous

* Mon Apr 10 2006 Erwan Velu <erwan@seanodes.com> 1.1.0-1mdk
- Initial Relase

