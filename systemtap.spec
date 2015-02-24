#
# Conditional build:
%bcond_without	doc		# documentation build
%bcond_with	publican	# publican guides build (requires functional publican+wkhtmltopdf)
%bcond_without	crash		# crash extension
%bcond_without	dyninst		# dyninst support
%bcond_without	java		# Java runtime support
#
%ifnarch %{ix86} %{x8664} alpha arm ia64 ppc64 s390 s390x
%undefine	with_crash
%endif
%ifnarch %{ix86} %{x8664} ppc ppc64
%undefine	with_dyninst
%endif
Summary:	Instrumentation System
Summary(pl.UTF-8):	System oprzyrządowania
Name:		systemtap
Version:	2.6
Release:	3
License:	GPL v2+
Group:		Base
Source0:	http://sourceware.org/systemtap/ftp/releases/%{name}-%{version}.tar.gz
# Source0-md5:	65e6745f0ec103758c711dd1d12fb6bf
Source1:	systemtap.tmpfiles
Source2:	stap-server.tmpfiles
Patch0:		%{name}-configure.patch
Patch1:		%{name}-build.patch
Patch2:		%{name}-rpm5-support.patch
Patch3:		%{name}-dtrace-flexibility.patch
Patch4:		format-security.patch
URL:		http://sourceware.org/systemtap/
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake
BuildRequires:	avahi-devel
BuildRequires:	boost-devel
%{?with_crash:BuildRequires:	crash-devel}
BuildRequires:	docbook-dtd412-xml
%{?with_dyninst:BuildRequires:	dyninst-devel >= 8.0}
BuildRequires:	elfutils-devel >= 0.148
BuildRequires:	gettext-tools >= 0.18.2
BuildRequires:	glib2-devel
%{?with_java:BuildRequires:	jdk}
%if %{with dyninst} || %{with java}
BuildRequires:	libselinux-devel
%endif
BuildRequires:	libstdc++-devel
BuildRequires:	libvirt-devel >= 1.0.2
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	mysql-devel
BuildRequires:	nss-devel >= 3
BuildRequires:	rpm-devel
BuildRequires:	sqlite3-devel >= 3
BuildRequires:	xmlto
%if %{with doc}
BuildRequires:	latex2html
%{?with_publican:BuildRequires:	publican}
BuildRequires:	texlive-dvips
BuildRequires:	texlive-fonts-bitstream
BuildRequires:	texlive-fonts-type1-bitstream
BuildRequires:	texlive-latex
%endif
# let base mean client+local development package
Requires:	%{name}-client = %{version}-%{release}
Requires:	%{name}-devel = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SystemTap is an instrumentation system for systems running Linux 2.6.
Developers can write instrumentation to collect data on the operation
of the system. The base systemtap package provides the components
needed to locally develop and execute systemtap script.

%description -l pl.UTF-8
SystemTap to system oprzyrządowania dla systemów opartych na Linuksie
2.6. Programiści mogą pisać narzędzia do zbierania danych dotyczących
operacji w systemie. Główny pakiet dostarcza komponenty niezbędne do
lokalnego tworzenia i wykonywania skryptów systemtap.

%package runtime
Summary:	Programmable system-wide instrumentation system - runtime
Summary(pl.UTF-8):	Programowalny systemowy system oprzyrządowania - środowisko uruchomieniowe
Group:		Applications/System

%description runtime
SystemTap runtime contains the components needed to execute a
systemtap script that was already compiled into a module using a local
or remote systemtap-devel installation.

%description runtime -l pl.UTF-8
Środowisko uruchomieniowe SystemTap zawiera komponenty niezbędne do
uruchomienia skryptu systemtap, który został już wkompilowany do
modułu przy użyciu lokalnej lub zdalnej instalacji systemtap-devel.

%package runtime-java
Summary:	SystemTap Java runtime support
Summary(pl.UTF-8):	Obsługa Javy dla środowiska uruchomieniowego SystemTap
Group:		Libraries
Requires:	%{name}-runtime = %{version}-%{release}
Requires:	byteman > 2.0

%description runtime-java
This package includes support files needed to run systemtap scripts
that probe Java processes running on the OpenJDK 1.6 and OpenJDK 1.7
runtimes using Byteman.

%description runtime-java -l pl.UTF-8
Ten pakiet zawiera pliki niezbędne do uruchamiania skryptów systemtap
sondujące procesy Javy działające w środowiskach OpenJDK 1.6 i OpenJDK
1.7 przy użyciu Bytemana.

%package client
Summary:	Programmable system-wide instrumentation system - client
Summary(pl.UTF-8):	Programowalny systemowy system oprzyrządowania - klient
Group:		Applications/System
Requires:	%{name}-runtime = %{version}-%{release}
Requires:	coreutils
Requires:	grep
Requires:	libvirt >= 1.0.2
Requires:	openssh-clients
Requires:	sed
Requires:	unzip
Requires:	zip

%description client
This package provides the components needed to develop systemtap
scripts and compile them using a local systemtap-devel or a remote
systemtap-server installation, then run them using a local or remote
systemtap-runtime. It includes script samples and documentation, and a
copy of the tapset library for reference.

%description client -l pl.UTF-8
Ten pakiet dostarcza komponenty niezbędne do tworzenia skryptów
systemtap i kompilowania ich przy użyciu lokalnej instalacji
systemtap-devel lub zdalnej instalacji systemtap-server, a następnie
uruchamiania ich przy użyciu lokalnej lub zdalnej instalacji
systemtap-runtime. Zawiera przykłady skryptów oraz dokumentację, a
także kopię biblioteki tapset.

%package devel
Summary:	Programmable system-wide instrumentation system - development headers, tools
Summary(pl.UTF-8):	Programowalny systemowy system oprzyrządowania - pliki nagłówkowe, narzędzia
Group:		Development/Tools
Requires:	%{name}-client = %{version}-%{release}
Requires:	gcc
Requires:	kernel-module-build
Requires:	make

%description devel
This package provides the components needed to compile a systemtap
script from source form into executable (.ko) forms. It may be
installed on a self-contained developer workstation (along with the
systemtap-client and systemtap-runtime packages), or on a dedicated
remote server (alongside the systemtap-server package). It includes a
copy of the standard tapset library and the runtime library C files.

%description devel -l pl.UTF-8
Ten pakiet dostarcza komponenty niezbędne do kompilowania skryptów
systemtap z postaci źródłowej do wykonywalnej (.ko). Może być
zainstalowany na samodzielnej stacji roboczej programisty (wraz z
pakietami systemtap-client i systemtap-runtime) lub dedykowanym
zdalnym serwerze (wraz z pakietem systemtap-server). Zawiera kopię
standardowej biblioteki tapset oraz pliki biblioteki uruchomieniowej
C.

%package initscript
Summary:	SystemTap Initscripts
Summary(pl.UTF-8):	Skrypty startowe SystemTap
Group:		Base
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name} = %{version}-%{release}
Requires:	rc-scripts

%description initscript
SysVinit scripts to launch selected systemtap scripts at system
startup.

%description initscript -l pl.UTF-8
Skrypty SysVinit do uruchamiania wybranych skryptów systemtap w
trakcie startu systemu.

%package server
Summary:	Instrumentation System Server
Summary(pl.UTF-8):	Serwer systemu oprzyrządowania
Group:		Applications/System
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-devel = %{version}-%{release}
Requires:	/bin/mktemp
Requires:	unzip
Requires:	zip

%description server
This is the remote script compilation server component of systemtap.
It announces itself to nearby clients with avahi (if available), and
compiles systemtap scripts to kernel objects on their demand.

%description server -l pl.UTF-8
Ten pakiet zawiera komponent serwera do zdalnej kompilacji skryptów
systemtap. Rozgłasza się pobliskim klientom przy użyciu avahi (jeśli
jest dostępny) i na żądanie kompiluje skrypty systemtap do obiektów
jądra.

%package sdt-devel
Summary:	Static probe support tools
Summary(pl.UTF-8):	Narzędzia do obsługi sond statycznych
License:	GPL v2+ and Public Domain
Group:		Development/Libraries

%description sdt-devel
This package includes the <sys/sdt.h> header file used for static
instrumentation compiled into userspace programs and libraries, along
with the optional dtrace-compatibility preprocessor to process related
.d files into tracing-macro-laden .h headers.

%description sdt-devel -l pl.UTF-8
Ten pakiet zawiera plik nagłówkowy <sys/sdt.h> służący do
wkompilowywania statycznego oprzyrządowania do programów i bibliotek
przestrzeni użytkownika, wraz z opcjonalnym preprocesorem zgodności z
dtrace, który przetwarza pliki .d na pliki nagłówkowe .h z makrami
śledzącymi.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch3 -p1
%patch4 -p1
%if "%{_rpmversion}" >= "5.0"
%patch2 -p1
%endif

%build
%{__gettextize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{?with_crash:--enable-crash} \
	--enable-docs%{!?with_doc:=no} \
	--enable-pie \
	--enable-publican%{!?with_publican:=no} \
	--enable-server \
	--enable-sqlite \
	--with-dyninst%{!?with_dyninst:=no} \
	--with-java=%{?with_java:%{_jvmdir}/java}%{!?with_java:no}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/var/{cache,run}/%{name},%{systemdtmpfilesdir},%{systemdunitdir}} \
	$RPM_BUILD_ROOT{%{_sysconfdir}/stap-server/conf.d,/etc/{sysconfig,logrotate.d,rc.d/init.d}} \
	$RPM_BUILD_ROOT/var/log/stap-server

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/systemtap.conf
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/stap-server.conf

# not installed by make
install stap-prep $RPM_BUILD_ROOT%{_bindir}/stap-prep

install initscript/systemtap $RPM_BUILD_ROOT/etc/rc.d/init.d
install initscript/config.systemtap $RPM_BUILD_ROOT%{_sysconfdir}/systemtap/config

install initscript/stap-server $RPM_BUILD_ROOT/etc/rc.d/init.d
install initscript/config.stap-server $RPM_BUILD_ROOT/etc/sysconfig/stap-server
install initscript/logrotate.stap-server $RPM_BUILD_ROOT/etc/logrotate.d/stap-server
install stap-server.service $RPM_BUILD_ROOT%{systemdunitdir}

install -d $RPM_BUILD_ROOT%{_sysconfdir}/systemtap/{conf.d,script.d}
install -d $RPM_BUILD_ROOT/var/lib/stap-server/.systemtap
install -d $RPM_BUILD_ROOT/var/log/stap-server

%{__mv} $RPM_BUILD_ROOT%{_docdir}/systemtap docs-installed

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)

%files runtime -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README*
%attr(755,root,root) %{_bindir}/stap-merge
%attr(755,root,root) %{_bindir}/stap-report
%{?with_dyninst:%attr(755,root,root) %{_bindir}/stapdyn}
%attr(755,root,root) %{_bindir}/stapsh
# XXX: %attr(4754,root,stapusr) staprun ?
%attr(755,root,root) %{_bindir}/staprun
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/stap-authorize-cert
%attr(755,root,root) %{_libdir}/%{name}/stapio
%{?with_crash:%attr(755,root,root) %{_libdir}/%{name}/staplog.so}
%{_mandir}/man1/stap-merge.1*
%{_mandir}/man1/stap-report.1*
%{_mandir}/man3/function::*.3stap*
%{_mandir}/man3/probe::*.3stap*
%{_mandir}/man3/stapex.3stap*
%{_mandir}/man3/stapfuncs.3stap*
%{_mandir}/man3/stapprobes.3stap*
%{_mandir}/man3/stapvars.3stap*
%{_mandir}/man3/tapset::*.3stap*
%{_mandir}/man7/error::*.7stap*
%{_mandir}/man7/stappaths.7*
%{_mandir}/man7/warning::debuginfo.7stap*
%{_mandir}/man7/warning::symbols.7stap*
%{?with_dyninst:%{_mandir}/man8/stapdyn.8*}
%{_mandir}/man8/staprun.8*
%{_mandir}/man8/stapsh.8*
%{_mandir}/man8/systemtap.8*

%if %{with java}
%files runtime-java
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/stapbm
%attr(755,root,root) %{_libdir}/%{name}/libHelperSDT_*.so
%{_libdir}/%{name}/HelperSDT.jar
%endif

%files client
%defattr(644,root,root,755)
%doc docs-installed/examples %{?with_docs:docs-installed/{tapsets,langref.pdf,tutorial.pdf}}
%attr(755,root,root) %{_bindir}/stap
%attr(755,root,root) %{_bindir}/stap-prep
%attr(755,root,root) %{_bindir}/stapvirt
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/tapset
%{_mandir}/man1/stap.1*
%{_mandir}/man1/stap-prep.1*
%{_mandir}/man1/stapvirt.1*

%files devel
%defattr(644,root,root,755)
%{_datadir}/%{name}/runtime

%files initscript
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/systemtap
%dir %{_sysconfdir}/systemtap
%dir %{_sysconfdir}/systemtap/conf.d
%dir %{_sysconfdir}/systemtap/script.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/systemtap/config
%{systemdtmpfilesdir}/systemtap.conf
%dir /var/cache/%{name}
%dir /var/run/%{name}

%files server
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/stap-server
%attr(755,root,root) %{_libdir}/%{name}/stap-env
%attr(755,root,root) %{_libdir}/%{name}/stap-gen-cert
%attr(755,root,root) %{_libdir}/%{name}/stap-serverd
%attr(755,root,root) %{_libdir}/%{name}/stap-sign-module
%attr(755,root,root) %{_libdir}/%{name}/stap-start-server
%attr(755,root,root) %{_libdir}/%{name}/stap-stop-server
%dir %{_sysconfdir}/stap-server
%dir %{_sysconfdir}/stap-server/conf.d
%attr(754,root,root) /etc/rc.d/init.d/stap-server
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/stap-server
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/stap-server
%{systemdunitdir}/stap-server.service
%{systemdtmpfilesdir}/stap-server.conf
# TODO: create user/group
#%attr(750,stap-server,stap-server) %dir /var/lib/stap-server
#%attr(700,stap-server,stap-server) %dir /var/lib/stap-server/.systemtap
#%attr(755,stap-server,stap-server) %dir /var/log/stap-server
#%attr(755,stap-server,stap-server) %dir /var/run/stap-server
%{_mandir}/man8/stap-server.8*

%files sdt-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/dtrace
%{_includedir}/sys/sdt.h
%{_includedir}/sys/sdt-config.h
%{_mandir}/man1/dtrace.1*
