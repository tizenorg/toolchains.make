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
Release:        %{?release_prefix:%{release_prefix}.}154.39.%{?dist}%{!?dist:tizen}
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
* Fri Jun 14 2013 UkJung Kim <ujkim@samsung.com> - None 
- PROJECT: external/make
- COMMIT_ID: d006c265dd3245b068a186c01563b40fe5d165f9
- PATCHSET_REVISION: d006c265dd3245b068a186c01563b40fe5d165f9
- CHANGE_OWNER: \"UkJung Kim\" <ujkim@samsung.com>
- PATCHSET_UPLOADER: \"UkJung Kim\" <ujkim@samsung.com>
- CHANGE_SUBMITTER: \"UkJung Kim\" <ujkim@samsung.com>
- CHANGE_URL: http://slp-info.sec.samsung.net/gerrit/223145
- PATCHSET_REVISION: d006c265dd3245b068a186c01563b40fe5d165f9
- TAGGER: UkJung Kim <ujkim@samsung.com>
- Gerrit patchset approval info:
- UkJung Kim <ujkim@samsung.com> Verified : 1
- Inkyo Jung <inkyo.jung@samsung.com> Code Review : 2
- CHANGE_SUBJECT: Fixed systemd parallel build break
- Fixed systemd parallel build break
