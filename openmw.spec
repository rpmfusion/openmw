Name:           openmw
Version:        0.36.0
Release:        1%{?dist}
Summary:        Unofficial open source engine re-implementation of the game Morrowind

License:        GPLv3 and MIT and zlib
URL:            https://openmw.org
# If you use a classic internet browser, Github renames the archive (openmw-%%{version}.tar.gz) into openmw-openmw-%%{version}.tar.gz. So, If you want the sources, use for example wget.
Source0:        https://github.com/OpenMW/openmw/archive/%{name}-%{version}.tar.gz

# Fix data path from /usr/share/games/openmw to /usr/share/openmw/data
# Patch0:         openmw-datapath.patch

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
%setup -qn %{name}-%{name}-%{version} 

# Remove bundled tinyxml files
rm -f extern/oics/tiny*.*


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
       ../

make %{?_smp_mflags}
popd

%install
pushd build
%make_install 
popd
desktop-file-validate %{buildroot}/%{_datadir}/applications/openmw-cs.desktop
desktop-file-validate %{buildroot}/%{_datadir}/applications/openmw.desktop

# Move license files back so they can be packaged by %%doc
mkdir _tmpdoc
mv %{buildroot}%{_datadir}/licenses/openmw/* _tmpdoc/
rm -rf %{buildroot}%{_datadir}/licenses

# Create data directory
mkdir -p %{buildroot}/%{_datadir}/%{name}/data

%files
%doc docs/license/GPL3.txt README.md _tmpdoc/*
%{_bindir}/%{name}
%{_bindir}/%{name}-launcher
%{_bindir}/%{name}-iniimporter
%{_bindir}/%{name}-essimporter
%{_bindir}/%{name}-wizard
%{_bindir}/%{name}-cs
%{_bindir}/esmtool
%{_bindir}/bsatool
%{_libdir}/Plugin_MyGUI_OpenMW_Resources.so
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}-cs.desktop
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/openmw-cs.png
%{_datadir}/pixmaps/openmw.png
%config(noreplace) %{_sysconfdir}/openmw/


%changelog
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
