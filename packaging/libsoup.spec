Name:           libsoup
Version:        2.40.1
Release:        0
License:        LGPL-2.1+
Summary:        HTTP client/server library for GNOME
Url:            http://www.gnome.org
Group:          Development/Libraries/GNOME
Source:         http://download.gnome.org/sources/libsoup/2.40/%{name}-%{version}.tar.xz
Source99:       baselibs.conf
BuildRequires:  gettext-tools
BuildRequires:  glib-networking
BuildRequires:  gobject-introspection-devel
BuildRequires:  gtk-doc
BuildRequires:  intltool >= 0.35.0
BuildRequires:  sqlite3-devel
BuildRequires:  pkgconfig(glib-2.0) >= 2.31.7
BuildRequires:  pkgconfig(libxml-2.0)

%description
Libsoup is an HTTP client/server library for GNOME. It uses GObjects
and the glib main loop, to integrate well with GNOME applications.

Features:
  * Both asynchronous (GMainLoop and callback-based) and synchronous APIs
  * Automatically caches connections
  * SSL Support using GnuTLS
  * Proxy support, including authentication and SSL tunneling
  * Client support for Digest, NTLM, and Basic authentication
  * Server support for Digest and Basic authentication
  * XML-RPC support

%package -n typelib-Soup
Summary:        HTTP client/server library for GNOME -- Introspection bindings
Group:          System/Libraries

%description -n typelib-Soup
Libsoup is an HTTP client/server library for GNOME. It uses GObjects
and the glib main loop, to integrate well with GNOME applications.

This package provides the GObject Introspection bindings for libsoup.

%package devel
Summary:        HTTP client/server library for GNOME - Development Files
Group:          Development/Libraries/GNOME
Requires:       %{name} = %{version}
Requires:       typelib-Soup = %{version}

%description devel
Libsoup is an HTTP client/server library for GNOME. It uses GObjects
and the glib main loop, to integrate well with GNOME applications.

Features:
  * Both asynchronous (GMainLoop and callback-based) and synchronous APIs
  * Automatically caches connections
  * SSL Support using GnuTLS
  * Proxy support, including authentication and SSL tunneling
  * Client support for Digest, NTLM, and Basic authentication
  * Server support for Digest and Basic authentication
  * XML-RPC support

%prep
%setup -q

%build
%autogen
%configure\
    --disable-static \
    --enable-introspection \
    --without-gnome --enable-sqllite=yes --disable-tls-check
make %{?_smp_mflags}

%install
%make_install

%find_lang %{name}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%lang_package

%files
%defattr(-, root, root)
%license COPYING
%{_libdir}/*.so.*

%files -n typelib-Soup
%defattr(-,root,root)
%{_libdir}/girepository-1.0/Soup-2.4.typelib
%{_libdir}/girepository-1.0/SoupGNOME-2.4.typelib

%files devel
%defattr(-,root,root)
%{_includedir}/libsoup-2.4
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/libsoup-gnome-2.4
%{_datadir}/gtk-doc/html/libsoup-2.4
%{_datadir}/gir-1.0/Soup-2.4.gir
%{_datadir}/gir-1.0/SoupGNOME-2.4.gir
