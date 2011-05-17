Summary:	Instrumentation System
Summary(pl.UTF-8):	System oprzyrządowania
Name:		systemtap
Version:	1.4
Release:	0.1
License:	GPL v2+
Group:		Base
Source0:	http://sources.redhat.com/systemtap/ftp/releases/%{name}-%{version}.tar.gz
# Source0-md5:	c5c9c2087c2aa0459b90e690a5ca95d0
Patch0:		%{name}-configure.patch
URL:		http://sourceware.org/systemtap/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	elfutils-devel
BuildRequires:	glib2-devel
BuildRequires:	mysql-devel
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
%patch0 -p1

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/var/cache/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS HACKING NEWS README*
%doc %{_docdir}
%attr(755,root,root) %{_bindir}/stap
%attr(755,root,root) %{_bindir}/stap-merge
%attr(755,root,root) %{_bindir}/stap-report
%attr(755,root,root) %{_bindir}/stapgraph
%attr(755,root,root) %{_bindir}/staprun
%attr(755,root,root) %{_bindir}/dtrace
%{_datadir}/%{name}
%{_libexecdir}/%{name}
%dir /var/cache/%{name}
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*
%{_mandir}/man7/*.7*
%{_mandir}/man8/*.8*
