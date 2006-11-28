# TODO:
# - fix --as-needed build
%define	snap	20061111
Summary:	Instrumentation System
Summary(pl):	System oprzyrz±dowania
Name:		systemtap
Version:	0.5.11
Release:	0.%{snap}.1
License:	GPL
Group:		Base
Source0:	ftp://sourceware.org/pub/systemtap/snapshots/%{name}-%{snap}.tar.bz2
# Source0-md5:	fea372489a6db07592846f2be1c386f0
URL:		http://sourceware.org/systemtap/
BuildRequires:	elfutils-devel
BuildRequires:	glib2-devel
BuildRequires:	mysql-devel
Requires:	gcc
Requires:	make
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		filterout_ld	-Wl,--as-needed

%description
SystemTap is an instrumentation system for systems running Linux 2.6.
Developers can write instrumentation to collect data on the operation
of the system.

%description -l pl
SystemTap to system oprzyrz±dowania dla systemów opartych na Linuksie
2.6. Programi¶ci mog± pisaæ narzêdzia do zbierania danych dotycz±cych
operacji w systemie.

%prep
%setup -q -c

%build
cd src
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C src install \
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
