# TODO:
# - fix --as-needed build
%define       filterout_ld    -Wl,--as-needed
%define	snap	20061111
Summary:	Instrumentation System
Name:		systemtap
Version:	0.1
Release:	0.%{snap}.1
License:	GPL
Group:		Base
URL:		http://sourceware.org/systemtap/
Source0:	ftp://sourceware.org/pub/systemtap/snapshots/%{name}-%{snap}.tar.bz2
# Source0-md5:	fea372489a6db07592846f2be1c386f0
BuildRequires:	elfutils-devel
BuildRequires:	glib2-devel
BuildRequires:	mysql-devel
Requires:	gcc
Requires:	make
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SystemTap is an instrumentation system for systems running Linux 2.6.
Developers can write instrumentation to collect data on the operation
of the system.

%prep
%setup -q -c

%build
cd src
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
cd src
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/var/cache/systemtap

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(644,root,root,755)
%doc src/{README,AUTHORS,NEWS,COPYING}
%attr(755,root,root) %{_bindir}/*
%{_libexecdir}/systemtap
%{_datadir}/systemtap
%dir /var/cache/systemtap
%{_mandir}/man*/*
