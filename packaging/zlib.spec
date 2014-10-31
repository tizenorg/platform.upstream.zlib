%define keepstatic 1
Name:           zlib
Provides:       libz
Obsoletes:      libz
Version:        1.2.8
Release:        0
Summary:        Data Compression Library
License:        Zlib
Group:          Base/Libraries
Url:            http://www.zlib.net/
#X-Vcs-Url:     https://github.com/madler/zlib.git
Source:         http://zlib.net/zlib-%{version}.tar.bz2
Source1:        LICENSE
Source2:        baselibs.conf
Source1001:     zlib.manifest
BuildRequires:  pkgconfig

%description
ftp://ds.internic.net/rfc/rfc1950.txt (zlib format), rfc1951.txt
(deflate format) and rfc1952.txt (gzip format). These documents are
also available in other formats from
ftp://ftp.uu.net/graphics/png/documents/zlib/zdoc-index.html.

%package devel
Summary:        Include Files and Libraries mandatory for Development
Group:          Development/Libraries
Requires:       glibc-devel
Requires:       zlib = %{version}
Provides:       libz:/usr/include/zlib.h

%description devel
This package contains all necessary include files and libraries needed
to develop applications that require the provided includes and
libraries.

%package devel-static
Summary:        Include Files and Libraries mandatory for Development
Group:          Development/Libraries
Requires:       %{name}-devel = %{version}
Provides:       %{name}-devel:%{_libdir}/libz.a

%description devel-static
This package contains all necessary include files and libraries needed
to develop applications that require the provided includes and
libraries.

%package -n minizip
Summary:    Manipulates files from a .zip archive
Group:      System/Libraries
Requires:   %{name} = %{version}-%{release}

%description -n minizip
Minizip is a tool to manipulates files from a .zip archive.

%package -n minizip-devel
Summary:    Development files for the minizip library
Group:      Development/Libraries
Requires:   minizip = %{version}-%{release}

%description -n minizip-devel
This package contains the libraries and header files needed for
developing applications which use minizip.

%prep
%setup -q
cp %{SOURCE1001} .

%build
export LDFLAGS="-Wl,-z,relro,-z,now"
%define do_profiling 0
%if %{do_profiling}
profiledir=$(mktemp -d)
trap "rm -rf $profiledir" EXIT
CC="gcc" ./configure --shared --prefix=%{_prefix} --libdir=/%{_lib}
%__make CFLAGS="%{optflags} %{cflags_profile_generate}=$profiledir" %{?_smp_mflags}
time %__make check
%__make clean
%__make CFLAGS="%{optflags} %{cflags_profile_feedback}=$profiledir" %{?_smp_mflags}
%else
export CFLAGS="%{optflags}"
CC="gcc" ./configure --shared --prefix=%{_prefix} --libdir=/%{_lib}
%__make %{?_smp_mflags}
%endif

cd contrib/minizip
%reconfigure
%__make %{?_smp_mflags}

%check
time %__make check

%install
#mkdir -p %%{buildroot}%%{_mandir}/man3
mkdir -p %{buildroot}%{_libdir}
%make_install
ln -sf -v /%{_lib}/$(readlink %{buildroot}/%{_lib}/libz.so) %{buildroot}%{_libdir}/libz.so
rm -v %{buildroot}/%{_lib}/libz.so
# static lib
mv %{buildroot}/%{_lib}/libz.a %{buildroot}%{_libdir}
# Move .pc file to %%{_libdir}
mv %{buildroot}/%{_lib}/pkgconfig %{buildroot}%{_libdir}
# manpage
install -m 644 zlib.3 %{buildroot}%{_mandir}/man3
install -m 644 zutil.h %{buildroot}%{_includedir}

pushd contrib/minizip
%make_install
rm -rf %{buildroot}%{_libdir}/libminizip.a
rm -rf %{buildroot}%{_libdir}/libminizip.la
popd

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post -n minizip -p /sbin/ldconfig

%postun -n minizip -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root)
/%{_lib}/libz.so.1.2.*
/%{_lib}/libz.so.1

%files devel
%manifest %{name}.manifest
%defattr(-,root,root)
%doc README
%license README
%{_mandir}/man3/zlib.3.gz
%{_includedir}/zlib.h
%{_includedir}/zconf.h
%{_includedir}/zutil.h
%{_libdir}/libz.so
%{_libdir}/pkgconfig/zlib.pc

%files devel-static
%manifest %{name}.manifest
%defattr(-,root,root)
%{_libdir}/libz.a

%files -n minizip
%manifest %{name}.manifest
%{_libdir}/libminizip.so.*

%files -n minizip-devel
%manifest %{name}.manifest
%{_includedir}/minizip/*.h
%{_libdir}/libminizip.so
%{_libdir}/pkgconfig/minizip.pc
