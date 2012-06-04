%define _noautoprov ^devel
%define _noautoreq ^devel

Summary:	The Roadsend PCC Compiler for PHP
Name:		roadsend-php
Version:	2.9.8
Release:	7
Group:		Development/PHP
License:	GPLv2+
URL:		http://code.roadsend.com/pcc/
Source0:	http://code.roadsend.com/snaps/%{name}-%{version}.tar.bz2
BuildRequires:	bigloo-devel >= 3.0c
BuildRequires:	curl-devel >= 7.15.1
BuildRequires:	indent
BuildRequires:	libfcgi-devel
BuildRequires:	libxml2-devel
BuildRequires:	mysql-devel
BuildRequires:	openssl-devel
BuildRequires:	pcre-devel
BuildRequires:	sqlite3-devel >= 3.0.0
BuildRequires:	texinfo
Requires:	bigloo >= 3.0c
Requires:	indent

%description
Roadsend Compiler for PHP produces optimized stand alone applications,
libraries, and Web applications from standard PHP source code. The compiler
produces native machine code, not PHP byte code, so no interpreter is
required. It is a new implementation of the PHP language and runtime
environment compatible with Zend PHP. It does not share any code with the
original PHP implementation.

%prep
%setup -q

%build
%configure2_5x \
    --libdir=%{_libdir}/pcc \
    --mandir=%{_mandir}/man1 \
    --with-pcre \
    --with-fcgi \
    --with-xml \
    --with-mysql \
    --with-sqlite3 \
    --with-gtk=no \
    --with-gtk2=no

export LD_LIBRARY_PATH=`pwd`/libs
make

# make the manual
pushd doc/manual
    make
popd

%install
rm -rf %{buildroot}

export LD_LIBRARY_PATH=`pwd`/libs
%makeinstall_std

pushd %{buildroot}%{_libdir}
for i in pcc/*.so; do
    f=`basename $i`
    mv $i .
    chmod 755 $f
    ln -sf ../$f pcc/$f
done
popd

# cleanup
rm -f %{buildroot}%{_libdir}/pcc/*.a
rm -f %{buildroot}%{_libdir}/pcc/*.h

# prepare the manual
rm -rf html-manual
install -d html-manual/resources
install -m0644 doc/manual/html/*.html html-manual/
install -m0644 doc/resources/* html-manual/resources/

%files
%doc html-manual/* doc/COMPILER-LICENSE doc/RUNTIME-LICENSE README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/pcc.conf
%attr(0755,root,root) %dir %{_libdir}/pcc
%attr(0755,root,root) %{_libdir}/*.so
%attr(0644,root,root) %{_libdir}/pcc/*.heap
%attr(0755,root,root) %{_libdir}/pcc/*.so
%attr(0644,root,root) %{_libdir}/pcc/*.sch
%attr(0644,root,root) %{_libdir}/pcc/*.init
%attr(0755,root,root) %{_bindir}/pcc
%attr(0755,root,root) %{_bindir}/pcc.fcgi
%attr(0755,root,root) %{_bindir}/pcctags
%attr(0755,root,root) %{_bindir}/pdb

