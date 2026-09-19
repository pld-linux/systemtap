# TODO:
# - package jupyter files
#
# Conditional build:
%bcond_without	doc		# documentation build
%bcond_with	publican	# publican guides build [as of 3.0 not rebuilt automatically, PDFs are included]
%bcond_without	crash		# crash extension
%bcond_without	dyninst		# dyninst support
%bcond_without	java		# Java runtime support
%bcond_without	python3		# Python 3.x runtime support

%ifnarch %{ix86} %{x8664} x32 alpha %{arm} ia64 ppc64 s390 s390x
%undefine	with_crash
%endif
%ifnarch %{ix86} %{x8664} x32 ppc ppc64 aarch64
%undefine	with_dyninst
%endif

%{?use_default_jdk}

Summary:	Instrumentation System
Summary(pl.UTF-8):	System oprzyrządowania
Name:		systemtap
Version:	5.6
Release:	1
License:	GPL v2+
Group:		Base
Source0:	https://sourceware.org/pub/systemtap/releases/%{name}-%{version}.tar.gz
# Source0-md5:	14da9933ae257da020179b2ac869fd2d
Source1:	%{name}.tmpfiles
Source2:	stap-server.tmpfiles
Patch0:		%{name}-dyninst.patch
Patch1:		%{name}-systemd.patch
Patch2:		%{name}-staprun-version-flush.patch
Patch3:		%{name}-onboot-slog.patch
Patch4:		%{name}-types.patch
URL:		https://sourceware.org/systemtap/
BuildRequires:	autoconf >= 2.71
BuildRequires:	automake
BuildRequires:	avahi-devel
BuildRequires:	boost-devel
%{?with_crash:BuildRequires:	crash-devel}
BuildRequires:	docbook-dtd412-xml
%{?with_dyninst:BuildRequires:	dyninst-devel >= 8.0}
BuildRequires:	elfutils-debuginfod-devel >= 0.179
BuildRequires:	elfutils-devel >= 0.179
BuildRequires:	gettext-devel >= 0.19.4
BuildRequires:	gettext-tools >= 0.19.4
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	json-c-devel >= 0.13
BuildRequires:	libbpf-devel >= 1.0
%{?with_java:%buildrequires_jdk}
%if %{with dyninst} || %{with java}
BuildRequires:	libselinux-devel
%endif
BuildRequires:	libstdc++-devel >= 6:4.5
BuildRequires:	libvirt-devel >= 1.0.2
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	mysql-devel
BuildRequires:	ncurses-devel
BuildRequires:	ncurses-ext-devel
BuildRequires:	nss-devel >= 3
BuildRequires:	pkgconfig
BuildRequires:	python3 >= 1:3.2
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.6
BuildRequires:	python3-pip
# bdist_wheel is built into setuptools since 70.1, so python3-wheel is not needed
BuildRequires:	python3-setuptools >= 70.1
%endif
BuildRequires:	readline-devel
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-devel
%{?with_java:BuildRequires:	rpm-javaprov}
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.021
BuildRequires:	sqlite3-devel >= 3.7
BuildRequires:	xmlto
BuildRequires:	zlib-devel
%if %{with doc}
BuildRequires:	latex2html
%{?with_publican:BuildRequires:	publican}
BuildRequires:	texlive-dvips
BuildRequires:	texlive-fonts-bitstream
BuildRequires:	texlive-fonts-type1-bitstream
BuildRequires:	texlive-latex
BuildRequires:	texlive-latex-psnfss
BuildRequires:	texlive-xetex
%endif
# let base mean client+local development package
Requires:	%{name}-client = %{version}-%{release}
Requires:	%{name}-devel = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		filterout_cpp	-DNDEBUG

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
Requires:	json-c >= 0.13
Requires:	uname(release) >= 3.10

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
sondujących procesy Javy działające w środowiskach OpenJDK 1.6 i
OpenJDK 1.7 przy użyciu Bytemana.

%package runtime-python3
Summary:	SystemTap Python 3 Runtime Support
Summary(pl.UTF-8):	Obsługa Pythona 3 dla środowiska uruchomieniowego SystemTap
Group:		Development/Tools
Requires:	%{name}-runtime = %{version}-%{release}
Requires:	python3-modules >= 1:3.6

%description runtime-python3
This package includes support files needed to run systemtap scripts
that probe Python 3 processes.

%description runtime-python3 -l pl.UTF-8
Ten pakiet zawiera pliki niezbędne do uruchamiania skryptów systemtap
sondujących procesy Pythona 3.

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

%package exporter
Summary:	Systemtap-Prometheus interoperation mechanism
Summary(pl.UTF-8):	Mechanizm współpracy Systemtap-Prometheus
Group:		Applications/System
Requires:	%{name}-runtime = %{version}-%{release}

%description exporter
This package includes files for a systemd service that manages
systemtap sessions and relays Prometheus metrics from the sessions to
remote requesters on demand.

%description exporter -l pl.UTF-8
Ten pakiet zawiera pliki usługi systemd zarządzającej sesjami
systemtap i przekazującej na żądanie metryki Prometheusa z sesji do
zdalnych klientów.

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
Summary:	SystemTap service units
Summary(pl.UTF-8):	Jednostki usług SystemTap
Group:		Base
Requires(post,preun,postun):	systemd-units >= 38
Requires:	%{name} = %{version}-%{release}
Requires:	systemd-units >= 38

%description initscript
Systemd service templates to launch selected systemtap scripts at
system startup (stap@.service compiles and runs scripts from
/etc/systemtap/script.d, staprun@.service runs precompiled modules),
along with a dracut module and the stap-onboot tool for embedding
scripts into initramfs.

%description initscript -l pl.UTF-8
Szablony usług systemd do uruchamiania wybranych skryptów systemtap w
trakcie startu systemu (stap@.service kompiluje i uruchamia skrypty z
/etc/systemtap/script.d, staprun@.service uruchamia wcześniej
skompilowane moduły), a także moduł dracuta i narzędzie stap-onboot do
osadzania skryptów w initramfs.

%package server
Summary:	Instrumentation System Server
Summary(pl.UTF-8):	Serwer systemu oprzyrządowania
Group:		Applications/System
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	%{name}-devel = %{version}-%{release}
Requires:	/bin/mktemp
Requires:	unzip
Requires:	zip
Provides:	group(stap-server)
Provides:	user(stap-server)

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
Requires:	python3-modules >= 1:3.2
Requires:	python3-pyparsing

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

%package jupyter
Summary:	ISystemtap Jupyter kernel and examples
Summary(pl.UTF-8):	Jądro Jupyter i przykłady ISystemtap
Group:		Libraries/Python
Requires:	%{name}-client = %{version}-%{release}

%description jupyter
This package includes files needed to build and run the interactive
systemtap Jupyter kernel, either locally or within a container.

%description jupyter -l pl.UTF-8
Ten pakiet zawiera pliki potrzebne do zbudowania i uruchomienia
interaktywnego jądra Jupyter, zarówno lokalnie, jak i w kontenerze.

%package doc
Summary:	SystemTap guides and tutorials
Summary(pl.UTF-8):	Przewodniki i dokumentacja wprowadzająca do SystemTap
Group:		Documentation
BuildArch:	noarch

%description doc
SystemTap guides and tutorials.

%description doc -l pl.UTF-8
Przewodniki i dokumentacja wprowadzająca do SystemTap.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1

%{__sed} -E -i -e '1s,#!\s*/usr/bin/python(\s|$),#!%{__python3}\1,' \
	testsuite/systemtap.examples/general/pyexample.py

find testsuite/systemtap.examples/ -name '*.stp' -print0 | xargs -0 \
	%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+stap(\s|$),#!%{_bindir}/stap\1,'

%build
%{__gettextize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	PYTHON3=%{__python3} \
	%{?with_java:have_javac="%{java_home}/bin/javac"} \
	%{?with_java:have_jar="%{java_home}/bin/jar"} \
	--disable-silent-rules \
	%{?with_crash:--enable-crash} \
	--enable-docs%{!?with_doc:=no} \
	--enable-pie \
	--enable-server \
	--enable-sqlite \
	--with-dracutstap=%{_prefix}/lib/dracut/modules.d/99stap \
	--with-dyninst%{!?with_dyninst:=no} \
	--with-java=%{?with_java:%{java_home}}%{!?with_java:no} \
	--with-libbpf \
	--with-python3 \
	%{!?with_python3:--without-python3-probes}

%{__make} \
	%{?with_java:JAVAC="%{java_home}/bin/javac"} \
	%{?with_java:JAR="%{java_home}/bin/jar"}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/var/{cache,run}/%{name},%{systemdtmpfilesdir},%{systemdunitdir}} \
	$RPM_BUILD_ROOT{%{_sysconfdir}/stap-server/conf.d,/etc/{sysconfig,logrotate.d,rc.d/init.d}} \
	$RPM_BUILD_ROOT{/var/log/stap-server,%{_prefix}/lib/dracut/modules.d/99stap}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/systemtap.conf
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/stap-server.conf

# not installed by make
install -p stap-prep $RPM_BUILD_ROOT%{_bindir}/stap-prep

cp -p initscript/stap@.service initscript/staprun@.service $RPM_BUILD_ROOT%{systemdunitdir}
install -p initscript/99stap/{check,install,module-setup.sh,start-staprun.sh} \
	$RPM_BUILD_ROOT%{_prefix}/lib/dracut/modules.d/99stap

install -p initscript/stap-server $RPM_BUILD_ROOT/etc/rc.d/init.d
cp -p initscript/config.stap-server $RPM_BUILD_ROOT/etc/sysconfig/stap-server
cp -p initscript/logrotate.stap-server $RPM_BUILD_ROOT/etc/logrotate.d/stap-server
cp -p stap-server.service $RPM_BUILD_ROOT%{systemdunitdir}

install -d $RPM_BUILD_ROOT%{_sysconfdir}/systemtap/{conf.d,script.d}
install -d $RPM_BUILD_ROOT/var/lib/stap-server/.systemtap

%if %{with doc}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/systemtap docs-installed
%endif

# pl catalog has no translated messages, find_lang skips such empty .mo files
%{__rm} $RPM_BUILD_ROOT%{_datadir}/locale/pl/LC_MESSAGES/%{name}.mo

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
%attr(755,root,root) %{_bindir}/stapbpf
%{?with_dyninst:%attr(755,root,root) %{_bindir}/stapdyn}
%attr(755,root,root) %{_bindir}/stapsh
# XXX: %attr(4754,root,stapusr) staprun ?
%attr(755,root,root) %{_bindir}/staprun
%dir %{_libexecdir}/%{name}
%attr(755,root,root) %{_libexecdir}/%{name}/stap-authorize-cert
%attr(755,root,root) %{_libexecdir}/%{name}/stapio
%if %{with crash}
%if "%{_libdir}" != "%{_libexecdir}"
%dir %{_libdir}/%{name}
%endif
%attr(755,root,root) %{_libdir}/%{name}/staplog.so
%endif
%{_mandir}/man1/stap-merge.1*
%{_mandir}/man1/stap-report.1*
%{_mandir}/man1/stapref.1*
%{_mandir}/man3/stapex.3stap*
%{_mandir}/man3/stapfuncs.3stap*
%{_mandir}/man3/stapprobes.3stap*
%{_mandir}/man3/stapvars.3stap*
%if %{with doc}
%{_mandir}/man3/function::*.3stap*
%{_mandir}/man3/macro::*.3stap*
%{_mandir}/man3/probe::*.3stap*
%{_mandir}/man3/tapset::*.3stap*
%endif
%{_mandir}/man7/error::*.7stap*
%{_mandir}/man7/stappaths.7*
%{_mandir}/man7/warning::buildid.7stap*
%{_mandir}/man7/warning::debuginfo.7stap*
%{_mandir}/man7/warning::pass5.7stap*
%{_mandir}/man7/warning::symbols.7stap*
%{_mandir}/man8/stapbpf.8*
%{?with_dyninst:%{_mandir}/man8/stapdyn.8*}
%{_mandir}/man8/staprun.8*
%{_mandir}/man8/stapsh.8*
%lang(cs) %{_mandir}/cs/man1/stap-merge.1*
%lang(cs) %{_mandir}/cs/man1/stap-report.1*
%lang(cs) %{_mandir}/cs/man1/stapref.1*
%lang(cs) %{_mandir}/cs/man3/stapex.3stap*
%lang(cs) %{_mandir}/cs/man3/stapfuncs.3stap*
%lang(cs) %{_mandir}/cs/man3/stapprobes.3stap*
%lang(cs) %{_mandir}/cs/man3/stapvars.3stap*
%lang(cs) %{_mandir}/cs/man7/error::*.7stap*
%lang(cs) %{_mandir}/cs/man7/stappaths.7*
%lang(cs) %{_mandir}/cs/man7/warning::buildid.7stap*
%lang(cs) %{_mandir}/cs/man7/warning::debuginfo.7stap*
%lang(cs) %{_mandir}/cs/man7/warning::symbols.7stap*
%lang(cs) %{_mandir}/cs/man8/stapsh.8*
%lang(cs) %{_mandir}/cs/man8/systemtap.8*

%if %{with java}
%files runtime-java
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/%{name}/stapbm
%attr(755,root,root) %{_libexecdir}/%{name}/libHelperSDT.so
%{_libexecdir}/%{name}/HelperSDT.jar
%endif

%if %{with python3}
%files runtime-python3
%defattr(644,root,root,755)
%dir %{py3_sitedir}/HelperSDT
%attr(755,root,root) %{py3_sitedir}/HelperSDT/_HelperSDT.cpython-*.so
%{py3_sitedir}/HelperSDT/*.py
%{py3_sitedir}/HelperSDT/__pycache__
%{py3_sitedir}/helpersdt-0.1.0.dist-info
%endif

%files client
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/stap
%attr(755,root,root) %{_bindir}/stap-prep
%attr(755,root,root) %{_bindir}/stapvirt
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/examples
%{_datadir}/%{name}/tapset
%{_mandir}/man1/stap.1*
%{_mandir}/man1/stap-prep.1*
%{_mandir}/man1/stapvirt.1*
%lang(cs) %{_mandir}/cs/man1/stap.1*
%lang(cs) %{_mandir}/cs/man1/stap-prep.1*
%lang(cs) %{_mandir}/cs/man1/stapvirt.1*

%files exporter
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/stap-exporter
%{_sysconfdir}/stap-exporter
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/stap-exporter
%{systemdunitdir}/stap-exporter.service
%{_mandir}/man8/stap-exporter.8*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/stap-profile-annotate
%{_datadir}/%{name}/runtime
%if %{with python3}
%dir %{_libexecdir}/%{name}
%dir %{_libexecdir}/%{name}/python
%attr(755,root,root) %{_libexecdir}/systemtap/python/stap-resolve-module-function.py
%endif

%pre server
%groupadd -g 359 stap-server
%useradd -u 359 -d /var/lib/stap-server -s /bin/false -c "SystemTap compile server" -g stap-server stap-server

%postun server
if [ "$1" = "0" ]; then
	%userremove stap-server
	%groupremove stap-server
fi

%post initscript
%systemd_reload

%postun initscript
%systemd_reload

%files initscript
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/stap-onboot
%attr(755,root,root) %{_libexecdir}/%{name}/stap-service-prepare
%dir %{_sysconfdir}/systemtap
%dir %{_sysconfdir}/systemtap/conf.d
%dir %{_sysconfdir}/systemtap/script.d
%{systemdunitdir}/stap@.service
%{systemdunitdir}/staprun@.service
%{systemdtmpfilesdir}/systemtap.conf
%dir %{_prefix}/lib/dracut/modules.d/99stap
%attr(755,root,root) %{_prefix}/lib/dracut/modules.d/99stap/check
%attr(755,root,root) %{_prefix}/lib/dracut/modules.d/99stap/install
%attr(755,root,root) %{_prefix}/lib/dracut/modules.d/99stap/module-setup.sh
%attr(755,root,root) %{_prefix}/lib/dracut/modules.d/99stap/start-staprun.sh
%{_mandir}/man8/stap-onboot.8*
%dir /var/cache/%{name}
%dir /var/run/%{name}

%files server
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/stap-server
%attr(755,root,root) %{_libexecdir}/%{name}/stap-env
%attr(755,root,root) %{_libexecdir}/%{name}/stap-gen-cert
%attr(755,root,root) %{_libexecdir}/%{name}/stap-serverd
%attr(755,root,root) %{_libexecdir}/%{name}/stap-sign-module
%attr(755,root,root) %{_libexecdir}/%{name}/stap-start-server
%attr(755,root,root) %{_libexecdir}/%{name}/stap-stop-server
%dir %{_sysconfdir}/stap-server
%dir %{_sysconfdir}/stap-server/conf.d
%attr(754,root,root) /etc/rc.d/init.d/stap-server
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/stap-server
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/stap-server
%{systemdunitdir}/stap-server.service
%{systemdtmpfilesdir}/stap-server.conf
%attr(750,stap-server,stap-server) %dir /var/lib/stap-server
%attr(700,stap-server,stap-server) %dir /var/lib/stap-server/.systemtap
%attr(755,stap-server,stap-server) %dir /var/log/stap-server
%{_mandir}/man8/stap-server.8*
%lang(cs) %{_mandir}/cs/man8/stap-server.8*

%files sdt-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/dtrace
%{_includedir}/sys/sdt.h
%{_includedir}/sys/sdt-config.h
%{_mandir}/man1/dtrace.1*
%lang(cs) %{_mandir}/cs/man1/dtrace.1*

%files jupyter
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/stap-jupyter-container
%attr(755,root,root) %{_bindir}/stap-jupyter-install
%{_datadir}/%{name}/interactive-notebook
%{_mandir}/man1/stap-jupyter.1*

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%doc doc/{langref,tutorial}.pdf doc/beginners/SystemTap_Beginners_Guide.pdf docs-installed/tapsets.pdf
%endif
