%include	/usr/lib/rpm/macros.perl
Summary:	Some tools to be used with smart cards and PC/SC
Summary(pl):	Narzêdzia do u¿ywania z czytnikami Smart Card i PC/SC
Name:		pcsc-tools
Version:	1.3.3
Release:	1
License:	GPL v2+
Group:		Applications
Source0:	http://ludovic.rousseau.free.fr/softwares/pcsc-tools/%{name}-%{version}.tar.gz
# Source0-md5:	896ee8fe05337948e476962aef6ad846
Source1:	http://ludovic.rousseau.free.fr/softwares/pcsc-tools/smartcard_list.txt
URL:		http://ludovic.rousseau.free.fr/softwares/pcsc-tools/
BuildRequires:	pcsc-lite-devel
BuildRequires:	perl-PCSC >= 1.2.0
BuildRequires:	perl-gtk
BuildRequires:	rpm-perlprov
Requires:	perl-PCSC >= 1.2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Some tools to be used with smart cards and PC/SC.

%description -l pl
Narzêdzia do u¿ywania z czytnikami Smart Card i PC/SC.

%package gtk
Summary:	Some tools for smart cards and PC/SC with GTK+ GUI
Summary(pl):	Narzêdzia dla czytników Smart Card i PC/SC z GUI w GTK+
Group:		X11/Applications

%description gtk
Some tools for smart cards and PC/SC with GTK+ GUI.

%description gtk -l pl
Narzêdzia dla czytników Smart Card i PC/SC z GUI w GTK+.

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
	CFLAGS="%{rpmcflags} -Wall -DVERSION=\\\"%{version}\\\""

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT%{_prefix} \
	MAN="ATR_analysis.1p gscriptor.1p pcsc_scan.1 scriptor.1p"

mv -f $RPM_BUILD_ROOT%{_prefix}/pcsc $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changelog README TODO
%attr(755,root,root) %{_bindir}/ATR_analysis
%attr(755,root,root) %{_bindir}/pcsc_scan
%attr(755,root,root) %{_bindir}/scriptor
%dir %{_libdir}/pcsc
%{_libdir}/pcsc/smartcard_list.txt
%{_mandir}/man1/ATR_analysis.1*
%{_mandir}/man1/pcsc_scan.1*
%{_mandir}/man1/scriptor.1*

%files gtk
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gscriptor
%{_mandir}/man1/gscriptor.1*
