Name:           openmw
Version:        0.26.0
Release:        6%{?dist}
Summary:        Unofficial open source engine re-implementation of the game Morrowind

License:        GPLv3 and MIT and zlib
URL:            https://openmw.org/
Source0:        https://openmw.googlecode.com/files/%{name}-%{version}-source.tar.gz

# Unbundle tinyxml
Patch0:         openmw-bund_libs.patch
# Fix data path from /usr/share/games/openmw to /usr/share/openmw/data
Patch1:         openmw-datapath.patch

BuildRequires:  cmake
BuildRequires:  boost-devel       
BuildRequires:  bullet-devel
BuildRequires:  desktop-file-utils 
BuildRequires:  libblkid-devel
BuildRequires:  libmpg123-devel
BuildRequires:  libsndfile-devel
BuildRequires:  libXt-devel
BuildRequires:  mygui-devel
BuildRequires:  ogre-devel
BuildRequires:  openal-soft-devel
BuildRequires:  openexr-devel
BuildRequires:  qt-devel
BuildRequires:  SDL2-devel
BuildRequires:  tinyxml-devel
BuildRequires:  ffmpeg-devel
# New requirement as of 0.26.0
BuildRequires:  unshield-devel

# Version in openmw is modified.
Provides:       bundled(ocis)
# Shiny is designed to be copied in rather than a separate library.
# https://github.com/scrawl/shiny
Provides:       bundled(shiny) = 0.2


%description
OpenMW is a new engine for 2002's Game of the Year,
The Elder Scrolls 3: Morrowind.

It aims to be a fully playable (and improved!), open source implementation of
the game's engine and functionality. You will still need the original game data
to play OpenMW.


%prep
%setup -q -c %{name}-%{version}
%patch0 -p1 -b .bund_libs
%patch1 -p1 -b .datapath

# Remove bundled tinyxml files
rm -f extern/oics/tiny*.*


%build
rm -rf build && mkdir build && pushd build
%cmake -DDATADIR:PATH=%{_datadir}/%{name} \
       -DBINDIR=%{_bindir} \
       -DDATAROOTDIR:PATH=%{_datadir} \
       -DICONDIR=%{_datadir}/pixmaps \
       -DMORROWIND_RESOURCE_FILES=%{_datadir}/%{name}/resources \
       -DUSE_SYSTEM_TINYXML=TRUE \
       ../

make %{?_smp_mflags}


%install
pushd build
%make_install
popd
desktop-file-validate %{buildroot}/%{_datadir}/applications/opencs.desktop
desktop-file-validate %{buildroot}/%{_datadir}/applications/openmw.desktop

# Move license files back so they can be packaged by %%doc
mkdir _tmpdoc
mv %{buildroot}%{_datadir}/licenses/openmw/* _tmpdoc/
rm -rf %{buildroot}%{_datadir}/licenses

# Create data directory
mkdir -p %{buildroot}%{_datadir}/%{name}/data


%files
%doc GPL3.txt readme.txt _tmpdoc/*
%{_bindir}/esmtool
%{_bindir}/mwiniimport
%{_bindir}/omwlauncher
%{_bindir}/opencs
%{_bindir}/openmw
%{_datadir}/applications/opencs.desktop
%{_datadir}/applications/openmw.desktop
%{_datadir}/%{name}/
%{_datadir}/pixmaps/opencs.png
%{_datadir}/pixmaps/openmw.png
%config(noreplace) %{_sysconfdir}/openmw/


%changelog
* Wed Sep 18 2013 Alexandre Moine <nobrakal@fedoraproject.org> 0.26.0-6
- Change Licenses Tag

* Tue Sep 17 2013 Richard Shaw <hobbes1069@gmail.com> - 0.26.0-5
- Add patch for data path and add empty data directory.

* Sun Sep 15 2013 Alexandre Moine <nobrakal@fedoraproject.org> 0.26.0-4
- Change, in the %%file section, %%{_datadir}/%%{name}/resources/* to %%{_datadir}/%%{name}/

* Fri Sep 13 2013 Richard Shaw <hobbes1069@gmail.com> - 0.26.0-3
- Update to latest upstream release.
- Add patch to unbundle tinyxml.
- Update BuildRequires: per true build requirements.
- Change to out-of-source build which is preferred for cmake projects.
- Remove group tag as it is no longer required.
- Other misc spec cleanup.

* Fri Sep 13 2013 Alexandre Moine <nobrakal@fedoraproject.org> 0.26.0-2
- Add unshield-devel to the BuildRequires

* Wed Sep 11 2013 Alexandre Moine <nobrakal@fedoraproject.org> 0.26.0-1
- Update to the 0.26 release
- Change name of license files
- Remove install of licenses for the %%doc section

* Mon Sep 2 2013 Richard Shaw <hobbes1069@gmail.com> 0.25.0-7
- Remove unused requires

* Sat Aug 31 2013 Alexandre Moine <nobrakal@fedoraproject.org> 0.25.0-6
- Change BuildRquires tbb to tbb-devel.
- Change make install to the equivalent rpmmacro.
- Put one BuildRequires per line.

* Sun Aug 18 2013 Alexandre Moine <nobrakal@fedoraproject.org> 0.25.0-5
- Replace %%{_datadir}/games/%%{name}/resources/ to %%{_datadir}/%%{name}/resources/

* Sat Aug 17 2013 Alexandre Moine <nobrakal@fedoraproject.org> 0.25.0-4
- Remove "rm -rf $RPM-BUILD-ROOT" from the install part.
- Add a doc entry.
- Add the 'desktop-file-validate' for the .desktop.
- Add desktop-file-utils to the build requieres.

* Fri Aug 16 2013 Alexandre Moine <nobrakal@fedoraproject.org> 0.25.0-3
- Add a good link to the sources.
- Change the name of patch.
- Add a comment to the patch.
- Change the description.
- Add rpm macro in files part and in cmake part.

* Sat Aug 10 2013 Alexandre Moine <nobrakal@fedoraproject.org> 0.25.0-2
- Update to the 0.25.

* Wed Jul 03 2013 Alexandre Moine <nobrakal@fedoraproject.org> 0.24.0-1
- Add the changelog in the SPEC file.
