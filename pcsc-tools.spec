#
# Conditional build:
%bcond_without	gtk	# don't build GTK+ tools
#
Summary:	Some tools to be used with smart cards and PC/SC
Summary(pl.UTF-8):	Narzędzia do używania z czytnikami Smart Card i PC/SC
Name:		pcsc-tools
Version:	1.7.1
Release:	1
License:	GPL v2+
Group:		Applications
Source0:	https://pcsc-tools.apdu.fr/%{name}-%{version}.tar.bz2
# Source0-md5:	5bc5e648c740720fea640ce5fc287ce5
# broken builder script, original url:
# https://pcsc-tools.apdu.fr/smartcard_list.txt
Source1:	smartcard_list.txt
# NoSource1-md5:	b053d7168d1da04719cc67b7cd1e4cc8
URL:		https://pcsc-tools.apdu.fr/
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake >= 1:1.8
BuildRequires:	pcsc-lite-devel >= 1.6.0
BuildRequires:	perl-PCSC >= 1.2.0
BuildRequires:	pkgconfig
BuildRequires:	rpm-perlprov
BuildRequires:	sed >= 4.0
Requires:	pcsc-lite-libs >= 1.6.0
Requires:	perl-PCSC >= 1.2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Some tools to be used with smart cards and PC/SC.

%description -l pl.UTF-8
Narzędzia do używania z czytnikami Smart Card i PC/SC.

%package gtk
Summary:	Some tools for smart cards and PC/SC with GTK+ GUI
Summary(pl.UTF-8):	Narzędzia dla czytników Smart Card i PC/SC z GUI w GTK+
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	perl-PCSC >= 1.2.0

%description gtk
Some tools for smart cards and PC/SC with GTK+ GUI.

%description gtk -l pl.UTF-8
Narzędzia dla czytników Smart Card i PC/SC z GUI w GTK+.

%prep
%setup -q

# paranoid check whether smartcard_list.txt in _sourcedir isn't too old
if [ "`wc -l < %{SOURCE1}`" -lt "`wc -l < smartcard_list.txt`" ] ; then
	echo "smartcard_list.txt needs to be updated"
	exit 1
fi
cp -f %{SOURCE1} .

%{__sed} -i -e '1s,/usr/bin/env perl,/usr/bin/perl,' ATR_analysis.in gscriptor scriptor

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

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc Changelog README
%attr(755,root,root) %{_bindir}/ATR_analysis
%attr(755,root,root) %{_bindir}/pcsc_scan
%attr(755,root,root) %{_bindir}/scriptor
%dir %{_datadir}/pcsc
%{_datadir}/pcsc/smartcard_list.txt
%{_mandir}/man1/ATR_analysis.1p*
%{_mandir}/man1/pcsc_scan.1*
%{_mandir}/man1/scriptor.1p*

%if %{with gtk}
%files gtk
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gscriptor
%{_desktopdir}/gscriptor.desktop
%{_datadir}/pcsc/gscriptor.png
%{_mandir}/man1/gscriptor.1p*
%endif
