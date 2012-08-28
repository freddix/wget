Summary:	A utility for retrieving files using the HTTP or FTP protocols
Name:		wget
Version:	1.14
Release:	1
License:	GPL v3
Group:		Networking/Utilities
Source0:	ftp://ftp.gnu.org/gnu/wget/%{name}-%{version}.tar.xz
# Source0-md5:	316f6f59292c9098ad81fd54f658c579
URL:		http://wget.sunsite.dk/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	libtool
BuildRequires:	openssl-devel
BuildRequires:	texinfo
BuildRequires:	perl-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNU Wget is a file retrieval utility which can use either the HTTP or
FTP protocols. Wget features include the ability to work in the
background while you're logged out, recursive retrieval of
directories, file name wildcard matching, remote file timestamp
storage and comparison, use of Rest with FTP servers and Range with
HTTP servers to retrieve files over slow or unstable connections,
support for Proxy servers, and configurability.

%prep
%setup -q

rm -f doc/wget.info doc/sample.wgetrc.munged_for_texi_inclusion
sed -i -e 's|/usr/local/etc/wgetrc|/etc/wgetrc|g' doc/*

%build
%{__libtoolize}
%{__gettextize}
%{__aclocal} -I m4
%{__autoheader}
%{__autoconf}
%configure \
	--with-ssl=openssl
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	GETTEXT_PACKAGE=wget

cat > $RPM_BUILD_ROOT%{_sysconfdir}/wgetrc <<EOF
# certs location
ca_certificate = /etc/certs/ca-certificates.crt

EOF

rm -f $RPM_BUILD_ROOT%{_mandir}/README*

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	-p /usr/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README MAILING-LIST
%verify(not md5 mtime size) %config(noreplace) %{_sysconfdir}/wgetrc
%attr(755,root,root) %{_bindir}/wget
%{_mandir}/man1/*.1*
%{_infodir}/*.info*

