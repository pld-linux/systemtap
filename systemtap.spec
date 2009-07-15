Summary:	Instrumentation System
Summary(pl.UTF-8):	System oprzyrządowania
Name:		systemtap
Version:	0.9.8
Release:	0.1
License:	GPL
Group:		Base
Source0:	http://sources.redhat.com/systemtap/ftp/releases/%{name}-%{version}.tar.gz
# Source0-md5:	42128f0d5a92cc23b1565b829fed3b6f
URL:		http://sourceware.org/systemtap/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	elfutils-devel
BuildRequires:	glib2-devel
BuildRequires:	libtool
BuildRequires:	mysql-devel
Requires:	gcc
Requires:	make
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SystemTap is an instrumentation system for systems running Linux 2.6.
Developers can write instrumentation to collect data on the operation
of the system.

%description -l pl.UTF-8
SystemTap to system oprzyrządowania dla systemów opartych na Linuksie
2.6. Programiści mogą pisać narzędzia do zbierania danych dotyczących
operacji w systemie.

%prep
%setup -q 

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/var/cache/%{name}

%files
%defattr(644,root,root,755)
%doc {README,AUTHORS,NEWS,COPYING}
%doc %{_docdir}
%attr(755,root,root) %{_bindir}/stap
%attr(755,root,root) %{_bindir}/stap-*
%attr(755,root,root) %{_bindir}/staprun
%attr(755,root,root) %{_bindir}/dtrace
%{_datadir}/%{name}
%{_libexecdir}/%{name}
%dir /var/cache/%{name}
%{_mandir}/man*/*
