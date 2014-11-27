%bcond_with gnome
%bcond_with introspection

Name:           libsoup
Version:        2.46.0
Release:        0
License:        LGPL-2.1+
Summary:        HTTP client/server library for GNOME
Url:            http://www.gnome.org
Group:          System/Libraries
Source:         http://download.gnome.org/sources/libsoup/2.41/%{name}-%{version}.tar.xz
Source99:       baselibs.conf
Source1001: 	libsoup.manifest
Requires:       glib-networking
BuildRequires:  gettext-tools
BuildRequires:  glib-networking
%if %{with introspection}
BuildRequires:  gobject-introspection-devel
%endif
%if %{with gnome}
BuildRequires:  pkgconfig(gnome-keyring-1)
%endif
BuildRequires:  intltool >= 0.35.0
BuildRequires:  sqlite3-devel
BuildRequires:  pkgconfig(glib-2.0) >= 2.35.0
BuildRequires:  gnome-common
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
Group:          Social & Content/GNOME
Requires:       %{name} = %{version}
%if %{with gnome}
Requires:       typelib-Soup = %{version}
%endif

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
cp %{SOURCE1001} .

%build
chmod +x autogen.sh
%autogen\
%if %{with introspection}
    --enable-introspection \
%endif
%if %{with gnome}
    --with-gnome \
%else
    --without-gnome \
    --enable-sqlite=yes \
    --disable-tls-check \
%endif
    --disable-static 
make %{?_smp_mflags}

%install
%make_install

%find_lang %{name}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%lang_package

%files
%manifest %{name}.manifest
%defattr(-, root, root)
%license COPYING
%{_libdir}/*.so.*

%if %{with introspection}
%files -n typelib-Soup
%manifest %{name}.manifest
%defattr(-,root,root)
%{_libdir}/girepository-1.0/Soup-2.4.typelib
%if %{with gnome}
%{_libdir}/girepository-1.0/SoupGNOME-2.4.typelib
%endif
%endif

%files devel
%manifest %{name}.manifest
%defattr(-,root,root)
%{_includedir}/libsoup-2.4
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%if %{with introspection}
%{_datadir}/gir-1.0/Soup-2.4.gir
%if %{with gnome}
%{_datadir}/gir-1.0/SoupGNOME-2.4.gir
%{_includedir}/libsoup-gnome-2.4
%endif
%endif
