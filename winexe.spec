#
# Conditional build:
%bcond_with	sqlite3
%bcond_with	python
%bcond_with	sqlite3
%bcond_with	pthreads
%bcond_with	setproctitle
%bcond_with	incpopt
%bcond_with	wmic
%bcond_with	wmis
#
Summary:	winexe - remotely executes commands on WindowsNT/2000/XP/2003 systems from GNU/Linux
Summary(pl.UTF-8):	winexe - zdalne wywołanie polecń na WindowsNT/2000/XP/2003 spod systemu GNU/Linux
Name:		winexe
Version:	071026
Release:	1
Epoch:		0
License:	GPL/GPL v2/GPL v3
Group:		Applications
Source0:	http://eol.ovh.org/winexe/%{name}-source-%{version}.tar.bz2
# Source0-md5:	4eb7bc95014e6db7cd930513139f915f
URL:		http://eol.ovh.org/winexe/
BuildRequires:	autoconf >= 2.53
BuildRequires:	crossmingw32-binutils
BuildRequires:	crossmingw32-gcc
BuildRequires:	crossmingw32-gcc-c++
BuildRequires:	crossmingw32-w32api
BuildRequires:	dmapi-devel
BuildRequires:	libnscd-devel
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	openldap-devel >= 2.4.6
BuildRequires:	pam-devel >= 0.99.8.1
BuildRequires:	popt-devel
%if %{with python}
BuildRequires:	python-devel >= 2.3
BuildRequires:	rpm-pythonprov
BuildRequires:	swig >= 1.3
%endif
BuildRequires:	rpmbuild(macros) >= 1.304
BuildRequires:	readline-devel >= 4.2
BuildRequires:	samba-devel
Requires:	samba
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This implementation of DCOM/WMI client is based on Samba4 sources. It
uses RPC/DCOM mechanism to interact with WMI services on Windows
2000/XP/2003 machines. It contains also winexe - program to remote
execution Windows commands remotely from Linux box.

%description -l pl.UTF-8
Implementacja klienta DCOM/WMI na bazie kodu Samba4. Używa
mechanizmuRPC/DCOM do komunikacji z usługą WMI na komputerach z
Windows 2000/XP/2003. Zawiera winexe program ktory zdalnie wywołuje
polecenia na WindowsNT/2000/XP/2003 spod systemu GNU/Linux,
odpowiednik psexec.

%prep
%setup -q -n %{name}-source-%{version}

%build
#http://dev.zenoss.com/trac/browser/trunk/wmi/README
./autogen.sh
%configure \
	--with-fhs \
	%{?with_sqlite3:--with-sqlite3} \
	%{?with_pthreads:--with-pthreads} \
	%{?with_setproctitle:--with-pthreads} \
	%{?with_python:--with-python} \
	%{?with_incpopt:--with-included-popt} \

#	--enable-reg-gconf

%{__make} proto \
	bin/winexe \
	%{?with_wmic: bin/wmic} \
	%{?with_wmis: bin/wmis} \
	%{?with_python: wmi/_pywmi.dylib}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
install bin/{winexe,wmic,wmis} $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
