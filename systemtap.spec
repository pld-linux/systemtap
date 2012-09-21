#
# TODO: - enable server
#	- BRs
#	- more configure options
#
%bcond_with	doc
Summary:	Instrumentation System
Summary(pl.UTF-8):	System oprzyrządowania
Name:		systemtap
Version:	1.8
Release:	0.1
License:	GPL v2+
Group:		Base
Source0:	http://sources.redhat.com/systemtap/ftp/releases/%{name}-%{version}.tar.gz
# Source0-md5:	5b7ab0ae0efc520f0b19f9dbf11977c9
Source1:	systemtap.tmpfiles
Patch0:		%{name}-configure.patch
Patch1:		%{name}-build.patch
Patch2:		%{name}-rpm5-support.patch
Patch3:		%{name}-no-Werror.patch
URL:		http://sourceware.org/systemtap/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	xmlto
BuildRequires:	avahi-devel
BuildRequires:	elfutils-devel
BuildRequires:	glib2-devel
BuildRequires:	mysql-devel
BuildRequires:	nss-devel
BuildRequires:	sqlite3-devel
BuildRequires:	texlive-latex
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SystemTap is an instrumentation system for systems running Linux 2.6.
Developers can write instrumentation to collect data on the operation
of the system.

%description -l pl.UTF-8
SystemTap to system oprzyrządowania dla systemów opartych na Linuksie
2.6. Programiści mogą pisać narzędzia do zbierania danych dotyczących
operacji w systemie.

%package server
Summary:	Instrumentation System Server
License:	GPL v2+
Group:		Applications/System
URL:		http://sourceware.org/systemtap/
Requires:	/bin/mktemp
Requires:	systemtap-devel = %{version}-%{release}
Requires:	unzip
Requires:	zip
Requires(post):	/sbin/chkconfig
Requires(preun):	/sbin/chkconfig

%description server
This is the remote script compilation server component of systemtap.
It announces itself to nearby clients with avahi (if available), and
compiles systemtap scripts to kernel objects on their demand.


%package devel
Summary:	Programmable system-wide instrumentation system - development headers, tools
License:	GPL v2+
Group:		Development/Libraries
URL:		http://sourceware.org/systemtap/
Requires:	gcc
Requires:	linux-libc-headers
Requires:	make

%description devel
This package contains the components needed to compile a systemtap
script from source form into executable (.ko) forms. It may be
installed on a self-contained developer workstation (along with the
systemtap-client and systemtap-runtime packages), or on a dedicated
remote server (alongside the systemtap-server package). It includes a
copy of the standard tapset library and the runtime library C files.

%package runtime
Summary:	Programmable system-wide instrumentation system - runtime
License:	GPL v2+
Group:		Base
URL:		http://sourceware.org/systemtap/

%description runtime
SystemTap runtime contains the components needed to execute a
systemtap script that was already compiled into a module using a local
or remote systemtap-devel installation.

%package client
Summary:	Programmable system-wide instrumentation system - client
License:	GPL v2+
Group:		Base
URL:		http://sourceware.org/systemtap/
Requires:	coreutils
Requires:	grep
Requires:	openssh-clients
Requires:	sed
Requires:	systemtap-runtime = %{version}-%{release}
Requires:	unzip
Requires:	zip

%description client
This package contains/requires the components needed to develop
systemtap scripts, and compile them using a local systemtap-devel or a
remote systemtap-server installation, then run them using a local or
remote systemtap-runtime. It includes script samples and
documentation, and a copy of the tapset library for reference.


%package initscript
Summary:	Systemtap Initscripts
License:	GPL v2+
Group:		Base
URL:		http://sourceware.org/systemtap/
Requires:	systemtap = %{version}-%{release}
Requires(post):	/sbin/chkconfig
Requires(preun):	/sbin/chkconfig
Requires(preun):	rc-scripts
Requires(postun):	rc-scripts

%description initscript
Sysvinit scripts to launch selected systemtap scripts at system
startup.

%package sdt-devel
Summary:	Static probe support tools
License:	GPLv2+ and Public Domain
Group:		Development/Libraries
URL:		http://sourceware.org/systemtap/

%description sdt-devel
This package includes the <sys/sdt.h> header file used for static
instrumentation compiled into userspace programs and libraries, along
with the optional dtrace-compatibility preprocessor to process related
.d files into tracing-macro-laden .h headers.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
cd runtime/staprun
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
cd -
%configure \
	--disable-silent-rules \
	--enable-pie \
	--enable-sqlite \
	--%{?with_doc:en}%{!?with_doc:dis}able-docs \
	--enable-server
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/var/cache/%{name},%{systemdtmpfilesdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/stap-server.conf

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS HACKING NEWS README*
%doc %{_docdir}
%attr(755,root,root) %{_bindir}/stap
%attr(755,root,root) %{_bindir}/stap-merge
%attr(755,root,root) %{_bindir}/stap-report
%attr(755,root,root) %{_bindir}/staprun
%attr(755,root,root) %{_bindir}/stapsh
%{_datadir}/%{name}
%{_libexecdir}/%{name}
%dir /var/cache/%{name}
%{_mandir}/man1/stap.1*
%{_mandir}/man1/stap-merge.1*
%{_mandir}/man3/*.3*
%{_mandir}/man7/*.7*
%{_mandir}/man8/staprun.8*

%files sdt-devel -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/dtrace
%{_includedir}/sys/sdt.h
%{_includedir}/sys/sdt-config.h
%{_mandir}/man1/dtrace.1*
