#
# Conditional build:
%bcond_without	gtk	# don't build GTK+ tools
#
%include	/usr/lib/rpm/macros.perl
Summary:	Some tools to be used with smart cards and PC/SC
Summary(pl.UTF-8):	Narzędzia do używania z czytnikami Smart Card i PC/SC
Name:		pcsc-tools
Version:	1.4.18
Release:	1
License:	GPL v2+
Group:		Applications
Source0:	http://ludovic.rousseau.free.fr/softwares/pcsc-tools/%{name}-%{version}.tar.gz
# Source0-md5:	647ec2779cec69c910906fe5496f4e6c
# broken builder script, original url:
# http://ludovic.rousseau.free.fr/softwares/pcsc-tools/smartcard_list.txt
Source1:	http://ludovic.rousseau.free.fr/softwares/pcsc-tools/smartcard_list.txt
# NoSource1-md5:	c3ad02c80c856e89fa2629d6fbb41419
URL:		http://ludovic.rousseau.free.fr/softwares/pcsc-tools/
BuildRequires:	pcsc-lite-devel >= 1.6.0
BuildRequires:	perl-PCSC >= 1.2.0
%{?with_gtk:BuildRequires:	perl-Gtk2}
BuildRequires:	pkgconfig
BuildRequires:	rpm-perlprov
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

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -Wall -DVERSION=\\\"%{version}\\\" -I/usr/include/PCSC"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT%{_prefix} \
	MAN="ATR_analysis.1p gscriptor.1p pcsc_scan.1 scriptor.1p"

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changelog README TODO
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
%{_mandir}/man1/gscriptor.1p*
%endif
