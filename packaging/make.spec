%define release_prefix 154

#
# spec file for package make
#
# Copyright (c) 2012 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Name:           make
Url:            http://www.gnu.org/software/make/make.html
Provides:       gmake
Version:        3.82
Release:        %{release_prefix}
Summary:        GNU make
License:        GPL-2.0+
Group:          Development/Tools/Building
Source:         make-%version.tar.bz2
Patch2:         make-slowdown-parallelism.diff
Patch3:         make-disable-broken-tests.diff
Patch4:         make-savannah-bug30723-expand_makeflags_before_reexec.diff
Patch5:         make-savannah-bug30612-handling_of_archives.diff
Patch6:         make-fix_whitespace_tokenization.diff
Patch7:         make-glob-faster.patch
Patch64:        make-library-search-path.diff
Patch100:       make-Force-intermediate-targets-to-be-considered-if-their.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
The GNU make command with extensive documentation.

%prep
%setup -q
%patch2
%patch3 -p1
%patch4
%patch5
%patch6 -p1
%patch7 -p0
if [ %_lib == lib64 ]; then
%patch64
fi
%patch100 -p1

%build
CFLAGS=$RPM_OPT_FLAGS \
./configure --prefix=/usr --mandir=/usr/share/man --infodir=/usr/share/info
make %{?_smp_mflags}

%check
%ifarch %{ix86}
make check
%endif

%install
make DESTDIR=$RPM_BUILD_ROOT install
ln -s make $RPM_BUILD_ROOT/usr/bin/gmake
%find_lang %name

%files -f %name.lang
%defattr(-,root,root)
/usr/bin/make
/usr/bin/gmake
%doc /usr/share/info/make.info-*.gz
%doc /usr/share/info/make.info.gz
%doc /usr/share/man/man1/make.1.gz

%clean
rm -rf $RPM_BUILD_ROOT

%post
%install_info --info-dir=%{_infodir} %{_infodir}/%{name}.info.gz

%postun
%install_info_delete --info-dir=%{_infodir} %{_infodir}/%{name}.info.gz

%changelog
* Tue Apr 10 2012 meissner@suse.de
- Faster globbing support from upstream to speed up
  some large make projects like libreoffice. bnc#753323
* Tue Oct 11 2011 mhrusecky@suse.cz
- reverting previous change (qemu binfmt was fixed)
* Fri Sep 30 2011 mhrusecky@suse.cz
- using full ar path in tests on arm (fixes build)
* Tue Apr 19 2011 mhopf@novell.com
- make-fix_whitespace_tokenization.diff
  Fix Savannah bug #33125 (bnc #681108):
  Memory corruption during build of android build system.
* Tue Sep  7 2010 mhopf@novell.com
- make-savannah-bug30612-handling_of_archives.diff
  Fix Savannah bug #30612: handling of archive references with >1 object..
  Add oneshell to $(.FEATURES).
  Fix the NEWS file to be accurate.
- make-savannah-bug30723-expand_makeflags_before_reexec.diff
  Fix Savannah bug #30723: expand MAKEFLAGS before we re-exec after rebuilding
  makefiles.
* Mon Aug 30 2010 mhopf@novell.com
- Disable some inherrently broken test cases.
* Mon Aug 23 2010 mhopf@novell.com
- Update to 3.82
  - Bug fixes
  - Backwards Incompatibilities:
  - Makefiles with .POSIX target: shells called with -e
  - $? contains prerequisites even if not existent
  - Prerequisite with '=' cannot be backslash escaped any more
    (use variable with '=' instead)
  - Variable names may not contain whitespaces any more
  - Mixture of explicit and pattern targets didn't always fail
  - Pattern specific rules application order changed
  - Library search behavior now compatible with standard linker
  - New features
  - --eval=STRING: Evaluate makefile syntax string before makefile
  - Variable .RECIPEPREFIX: Exchange TAB character
  - Variable .SHELLFLAGS:   Options passed to shells
  - Target   .ONESHELL:     Single instance of shell for recipe
  - Modifier  private:      Suppresses inheritance of variables
  - Directive undefine:     Undefine variable
  - Changed features
  - Multiple modifiers for variables allowed now.
  - Directive define:       Allow variable assignment operator.
- Nuke memory-hog-2.diff which didn't apply since 3.81
- Addapt make-slowdown-parallelism.diff to new parallelization tests
- Separate make checks into %%checks section
* Mon Jun 28 2010 jengelh@medozas.de
- use %%_smp_mflags
* Mon May 24 2010 coolo@novell.com
- fix test case
* Fri Jan  8 2010 ro@suse.de
- enable parallel build
* Mon May 14 2007 coolo@suse.de
- use %%find_lang
* Tue Oct 31 2006 mhopf@suse.de
- Reducing race probability in test case features/parallelism even more.
* Wed Jun  7 2006 mhopf@suse.de
- Improving occasional build failures due to races in test cases.
* Mon May 29 2006 mhopf@suse.de
- Update to 3.81
  - Bug fixes
  - New functions: lastword, abspath, realpath, info, flavor, or, and
  - New variables: .INCLUDE_DIRS, .FEATURES, .DEFAULT_GOAL, MAKE_RESTARTS, $|
  - Some new features
  - More POSIX compatibility
- memory-hog-2.diff doesn't apply any longer
* Wed Feb  1 2006 kssingvo@suse.de
- fix for memory-hog.diff (bugzilla#147229)
* Wed Feb  1 2006 kssingvo@suse.de
- disabled memory-hog.diff due to crashes (bugzilla#147229)
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Thu Jan 19 2006 aj@suse.de
- Reduce memory usage.
* Fri Jan  9 2004 adrian@suse.de
- do not strip binaries during install
* Tue Sep 30 2003 stepan@suse.de
- fix "virtual memory exhausted" bug (backport from mainline)
* Thu Apr 24 2003 ro@suse.de
- fix install_info --delete call and move from preun to postun
* Wed Apr 16 2003 coolo@suse.de
- use BuildRoot
* Fri Feb  7 2003 ro@suse.de
- added install_info macros
* Mon Dec 30 2002 aj@suse.de
- Update to version 3.80:
  - number of bug fixes
  - new features as mentioned in the NEWS file:
  * New functions $(value ...), $(eval ...)
  * New feature: order-only prerequesites.
  * Argument to ifdef can now be a variable.
  * new option --always-make
* Tue Sep 17 2002 ro@suse.de
- removed bogus self-provides
* Thu May 23 2002 meissner@suse.de
- Made %%_lib fix generic, do not use ifarch.
* Mon Apr 22 2002 meissner@suse.de
- x86_64 needs /*/lib64 as search path too.
* Fri Apr 19 2002 ke@suse.de
- Update German translation from
  http://www.iro.umontreal.ca/contrib/po/teams/PO/de/ [# 15851].
* Tue Dec 11 2001 froh@suse.de
- s390x, sparc64 and ia64: extended the 'Dynamic Library Search'
  default path to search /lib64 and /usr/lib64 as well.
* Wed Nov 28 2001 fehr@suse.de
- add mo-files for translations of messages
* Wed May  9 2001 cstein@suse.de
- repacked source files with bzip2
* Fri Nov 17 2000 fehr@suse.de
- set group tag
* Mon Jun 26 2000 fehr@suse.de
- change to new version 3.79.1
* Wed Apr 19 2000 fehr@suse.de
- change to new version 3.79
* Mon Feb 14 2000 fehr@suse.de
- add compatibility link gmake -> make, needed for oracle install
* Thu Jan 20 2000 fehr@suse.de
- security fix for files created in /tmp when using -j
* Mon Jan 17 2000 schwab@suse.de
- Update to 3.78.1.
- Get rid of Makefile.Linux.
- Run testsuite.
* Fri Jan 14 2000 schwab@suse.de
- Fix glob problem.
* Wed Oct 13 1999 schwab@suse.de
- Fix file list.
- Add autoconf to needforbuild
* Mon Sep 13 1999 bs@suse.de
- ran old prepare_spec on spec file to switch to new prepare_spec.
* Tue Feb 23 1999 ro@suse.de
- updated to 3.77 using fixes by c. gafton
* Wed Sep 23 1998 ro@suse.de
- downgrade to 3.76.1 (works at least)
* Tue Sep 22 1998 ro@suse.de
- update to 3.77
* Thu Oct  9 1997 florian@suse.de
- prepare for autobuild
  Mon Sep  2 02:48:35 MET DST 1996
  update to version 3.75
