Name:           openmw
Version:        0.44.0
Release:        2%{?dist}
Summary:        Unofficial open source engine re-implementation of the game Morrowind

License:        GPLv3 and MIT and zlib
URL:            https://openmw.org
# If you use a classic internet browser, Github renames the archive (openmw-%%{version}.tar.gz) into openmw-openmw-%%{version}.tar.gz. So, If you want the sources, use for example wget.
Source0:        https://github.com/OpenMW/openmw/archive/%{name}-%{version}.tar.gz

# Unbundle dejavu-lgc-sans-mono-fonts
Patch0:         %{name}.unbundle-dejavu-font.patch

# Unbundle tango icons
Patch1:         %{name}.undundle-tango-icons.patch

# Openmw has problems with big indian cpu
ExcludeArch:    ppc64

BuildRequires:  cmake
BuildRequires:  boost-devel
BuildRequires:  bullet-devel
BuildRequires:  desktop-file-utils
BuildRequires:  libblkid-devel
BuildRequires:  libmpg123-devel
BuildRequires:  libsndfile-devel
BuildRequires:  libXt-devel
# Recent version of MyGui required in 0.34.0
BuildRequires:  mygui-devel >= 3.2.1
# BuildRequires:  ogre-devel
BuildRequires:  openal-soft-devel
BuildRequires:  openexr-devel
BuildRequires:  qt-devel
BuildRequires:  SDL2-devel
BuildRequires:  tinyxml-devel
BuildRequires:  ffmpeg-devel
# New requirement as of 0.26.0
BuildRequires:  unshield-devel
BuildRequires:  libappstream-glib
# New requirement as of 0.37.0
BuildRequires:  OpenSceneGraph-devel OpenSceneGraph-qt-devel
BuildRequires:  gtest-devel
BuildRequires:  tango-icon-theme
BuildRequires:  dejavu-lgc-sans-mono-fonts

Requires:       dejavu-lgc-sans-mono-fonts
Requires:       tango-icon-theme

# Version in openmw is modified.
Provides:       bundled(ocis)
# Shiny is designed to be copied in rather than a separate library.
# https://github.com/scrawl/shiny
# Provides:       bundled(shiny) = 0.2


%description
OpenMW is a new engine for 2002's Game of the Year,
The Elder Scrolls 3: Morrowind.

It aims to be a fully playable (and improved!), open source implementation of
the game's engine and functionality. You will still need the original game data
to play OpenMW.


%prep
%setup -qn %{name}-%{name}-%{version}

# Remove bundled tinyxml files
rm -f extern/oics/tiny*.*

# Unbundle dejavu-lgc-sans-mono-fonts
rm -f files/mygui/DejaVuLGCSansMono.ttf
%patch0 -p1

# Unbundle tango icons
rm -rf files/wizard/icons/
rm -rf files/launcher/icons/
%patch1 -p1

%build
rm -rf build && mkdir build && pushd build
%cmake -DDATADIR:PATH=%{_datadir}/%{name} \
       -DLIBDIR=%{_libdir} \
       -DBINDIR=%{_bindir} \
       -DDATAROOTDIR:PATH=%{_datadir} \
       -DGLOBAL_DATA_PATH:PATH=%{_datadir} \
       -DICONDIR=%{_datadir}/pixmaps \
       -DMORROWIND_RESOURCE_FILES=%{_datadir}/%{name}/resources \
       -DOPENMW_RESOURCE_FILES=%{_datadir}/%{name}/resources \
       -DMORROWIND_DATA_FILES=%{_datadir}/%{name}/data \
       -DUSE_SYSTEM_TINYXML=TRUE \
       -DBUILD_UNITTESTS:BOOL=TRUE \
       -DCMAKE_CXX_STANDARD=11 \
       ../

make %{?_smp_mflags}
popd

%check
pushd build
./openmw_test_suite
popd

%install
pushd build
%make_install
popd
desktop-file-validate %{buildroot}/%{_datadir}/applications/openmw-cs.desktop
desktop-file-validate %{buildroot}/%{_datadir}/applications/openmw.desktop

# Test and install appdata file
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/%{name}.appdata.xml

# Remove font license file
rm -rf "%{buildroot}/%{_datadir}/licenses/%{name}/DejaVu Font License.txt"

# Create data directory
mkdir -p %{buildroot}/%{_datadir}/%{name}/data

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_bindir}/%{name}-launcher
%{_bindir}/%{name}-iniimporter
%{_bindir}/%{name}-essimporter
%{_bindir}/%{name}-wizard
%{_bindir}/%{name}-cs
%{_bindir}/esmtool
%{_bindir}/bsatool
# %%{_libdir}/Plugin_MyGUI_OpenMW_Resources.so
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}-cs.desktop
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}-cs.png
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/metainfo/%{name}.appdata.xml
%config(noreplace) %{_sysconfdir}/openmw/


%changelog
* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.44.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 10 2019 Ben Rosser <rosser.bjr@gmail.com> - 0.44.0-1
- Update to latest upstream release.

* Fri Jul 27 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.43.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 08 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.43.0-4
- Rebuilt for new ffmpeg snapshot

* Sun Feb 04 2018 Sérgio Basto <sergio@serjux.com> - 0.43.0-3
- Rebuild (boost)

* Thu Jan 18 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.43.0-2
- Rebuilt for ffmpeg-3.5 git

* Fri Dec 22 2017 Ben Rosser <rosser.bjr@gmail.com> - 0.43.0-1
- Update to latest upstream release.

* Wed Oct 18 2017 Ben Rosser <rosser.bjr@gmail.com> - 0.41.0-7
- Rebuild against new OpenSceneGraph 3.4.1 due to soname bump.

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.41.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed May 17 2017 Leigh Scott <leigh123linux@googlemail.com> - 0.41.0-5
- Rebuild for ffmpeg update

* Tue May 02 2017 Alexandre Moine <nobrakal@gmail.com> 0.41.0-4
- Exclude ppc64

* Sat Apr 29 2017 Leigh Scott <leigh123linux@googlemail.com> - 0.41.0-3
- Rebuild for ffmpeg update

* Mon Mar 20 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.41.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 27 2016 Alexandre Moine <nobrakal@gmail.com> 0.41.0-1
- New upstream release
- Update appdata.xml

* Sun Sep 04 2016 Alexandre Moine <nobrakal@gmail.com> 0.40.0-1
- New upstream release

* Tue May 10 2016 Alexandre Moine <nobrakal@gmail.com> 0.39.0-1
- New upstream release
- Force the use of c++11 standard

* Tue Jan 26 2016 Alexandre Moine <nobrakal@gmail.com> 0.38.0-1
- New upstream release

* Thu Dec 03 2015 Alexandre Moine <nobrakal@gmail.com> 0.37.0-1
- Update to new upstream.
- Remove obsolete library ogre (OpenMw now use OpenSceneGrpah).
- Remove unnecessary patch to compile with fPIC.
- Remove old bundled library shiny.
- Fix bad includes for osg-video-player, thanks to Dominik 'Rathann' Mierzejewski.
- Unbundle dejavu-lgc-sans-mono-fonts.
- Unbundle Tango icons.
- Remove intern .appdata, now supported by upstream
- Add the test suit.

* Thu Aug 13 2015 Alexandre Moine <nobrakal@gmail.com> 0.36.1-4
- Update the use of -fPIC

* Wed Aug 05 2015 Alexandre Moine <nobrakal@gmail.com> 0.36.1-3
- Use a more generic option to force independent code position for the library.

* Wed Aug 05 2015 Alexandre Moine <nobrakal@gmail.com> 0.36.1-2
- Specify the -fPIC flag in the right CMakeLists.txt

* Tue Aug 04 2015 Alexandre Moine <nobrakal@gmail.com> 0.36.1-1
- New maintenance update.
- Add appdata file for openmw.
- Add use of -fPIC flag for the compilation.

* Sat May 30 2015 Alexandre Moine <nobrakal@gmail.com> 0.36.0-1
- Update to new upstream.

* Mon Mar 16 2015 Alexandre Moine <nobrakal@fedoraproject.org> 0.35.1-1
- New maintenance update.

* Sat Feb 21 2015 Alexandre Moine <nobrakal@fedoraproject.org> 0.35.0-1
- Update to new upstream.
- Change binairies name from opencs to openmw-cs

* Wed Dec 31 2014 Alexandre Moine <nobrakal@fedoraproject.org> 0.34.0-1
- Update directly to 0.34.0 due to the new mygui just released in fedora (see BGZ #1145811)
- Remove openmw-datapath.patch, it set a variable in /components/files/linuxpath.cpp now in cmake
- Add new executables: bsatool and openmw-wizard
- Add new libraries: Plugin_MyGUI_OpenMW_Resources.so

* Thu Aug 07 2014 Sérgio Basto <sergio@serjux.com> - 0.31.0-2
- Rebuilt for ffmpeg-2.3

* Sun Jul 20 2014 Alexandre Moine <nobrakal@fedoraproject.org> 0.31.0-1
- Update to 0.31.0
- Finally fix the issue with the link.

* Thu May 29 2014 Alexandre Moine <nobrakal@fedoraproject.org> 0.30.0-1
- Update to 0.30.0
- Again issue with the source link. Github renames openmw-0.30.0.tar.gz into openmw-openmw-0.30.0.tar.gz, and I can't pick a direct link. So the Source0 is just the file's name, and I added a comment to specify the good URL.

* Fri Mar 14 2014 Alexandre Moine <nobrakal@fedoraproject.org> 0.29.0-2
- Fix the issue with the direct link

* Thu Mar 13 2014 Alexandre Moine <nobrakal@fedoraproject.org> 0.29.0-1
- Update to 0.29.0.
- The googlecode repo seems not supported anymore, the sources are now downloaded from github.
- Github renames openmw-0.29.0.tar.gz into openmw-openmw-0.29.0.tar.gz, and I can't pick a direct link. So the Source0 is just the file's name, and I added a comment to specify the good URL.
- The issues with the desktop files were fixed by upstream.

* Tue Jan 14 2014 Alexandre Moine <nobrakal@fedoraproject.org> 0.28.0-1
- Update to the new 0.28.0
- Add two patch to fix desktop files.

* Fri Nov 29 2013 Alexandre Moine <nobrakal@fedoraproject.org> 0.27.0-1
- Update to the new 0.27.0
- Retire patch to unbundle tinyxml, this was solved in upstream.

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
