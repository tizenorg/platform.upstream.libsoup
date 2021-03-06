dnl *******************************************
dnl *** Initialize automake and set version ***
dnl *******************************************

m4_define([soup_major_version], [2])
m4_define([soup_minor_version], [46])
m4_define([soup_micro_version], [0])

AC_PREREQ(2.63)
AC_INIT([libsoup],[soup_major_version.soup_minor_version.soup_micro_version],[http://bugzilla.gnome.org/enter_bug.cgi?product=libsoup])
AC_CONFIG_SRCDIR([libsoup-2.4.pc.in])
AC_CONFIG_MACRO_DIR([m4])
AC_CONFIG_AUX_DIR([build-aux])

AM_INIT_AUTOMAKE([1.11 foreign no-dist-gzip dist-xz -Wno-portability])
m4_ifdef([AM_SILENT_RULES],[AM_SILENT_RULES([yes])],)

AC_PROG_MAKE_SET

SOUP_MAJOR_VERSION=soup_major_version
SOUP_MINOR_VERSION=soup_minor_version
SOUP_MICRO_VERSION=soup_micro_version
AC_SUBST(SOUP_MAJOR_VERSION)
AC_SUBST(SOUP_MINOR_VERSION)
AC_SUBST(SOUP_MICRO_VERSION)

SOUP_API_VERSION=2.4
AC_SUBST(SOUP_API_VERSION)

# Increment on interface addition. Reset on removal.
SOUP_AGE=7

# Increment on interface add, remove, or change.
SOUP_CURRENT=8

# Increment on source change. Reset when CURRENT changes.
SOUP_REVISION=0

AC_SUBST(SOUP_CURRENT)
AC_SUBST(SOUP_REVISION)
AC_SUBST(SOUP_AGE)

dnl ***************************
dnl *** Set debugging flags ***
dnl ***************************

debug_default=minimum

# Declare --enable-* args and collect ac_help strings
AC_ARG_ENABLE(debug, 
	      AS_HELP_STRING([--enable-debug=[no/minimum/yes]],
			     [turn on debugging (default=$debug_default)]),,
	      enable_debug=$debug_default)

# Set the debug flags
if test "x$enable_debug" = "xyes"; then
	test "$cflags_set" = set || CFLAGS="$CFLAGS -g"
	SOUP_DEBUG_FLAGS="-DG_ENABLE_DEBUG"
else
	if test "x$enable_debug" = "xno"; then
		SOUP_DEBUG_FLAGS="-DG_DISABLE_ASSERT -DG_DISABLE_CHECKS"
	fi
fi

AC_SUBST(SOUP_DEBUG_FLAGS)

dnl ***************************
dnl *** Checks for programs ***
dnl ***************************

AC_PROG_CC
AC_PROG_INSTALL

# Initialize libtool
LT_INIT([win32-dll])

dnl ***********************
dnl *** Checks for glib ***
dnl ***********************

GLIB_REQUIRED=2.38.0
AM_PATH_GLIB_2_0($GLIB_REQUIRED,,,gobject gio)
if test "$GLIB_LIBS" = ""; then
   AC_MSG_ERROR(GLIB $GLIB_REQUIRED or later is required to build libsoup)
fi
GLIB_CFLAGS="$GLIB_CFLAGS -DGLIB_VERSION_MIN_REQUIRED=GLIB_VERSION_2_38"

GLIB_MAKEFILE='$(top_srcdir)/Makefile.glib'
AC_SUBST(GLIB_MAKEFILE)

GLIB_TESTS

PKG_CHECK_MODULES(XML, libxml-2.0)
AC_SUBST(XML_CFLAGS)
AC_SUBST(XML_LIBS)

PKG_CHECK_MODULES(SQLITE, sqlite3)
AC_SUBST(SQLITE_CFLAGS)
AC_SUBST(SQLITE_LIBS)

dnl ***********************
dnl *** Check for Win32 ***
dnl ***********************

AC_MSG_CHECKING([for Win32])
case "$host" in
  *-*-mingw*)
    os_win32=yes
    CFLAGS="$CFLAGS -D_REENTRANT"
    ;;
  *)
    os_win32=no
    ;;
esac
AC_MSG_RESULT([$os_win32])
AM_CONDITIONAL(OS_WIN32, [test $os_win32 = yes])

dnl ************************
dnl *** gettext/intltool ***
dnl ************************
IT_PROG_INTLTOOL([0.35.0])
GETTEXT_PACKAGE=libsoup
AC_SUBST([GETTEXT_PACKAGE])
AC_DEFINE_UNQUOTED([GETTEXT_PACKAGE],["$GETTEXT_PACKAGE"],[The gettext domain name])

dnl *******************
dnl *** Misc checks ***
dnl *******************
AC_CHECK_FUNCS(gmtime_r)

dnl *************************
dnl *** SQL Lite support independently of gnome for Tizen  ***
dnl *************************

AC_ARG_ENABLE(sqlite,
         AS_HELP_STRING([--enable-sqlite], [Enable SQL lite support ]),        ,
         enable_sqlite=no)

if test "$enable_sqlite" != "no"; then
   PKG_CHECK_MODULES(SQLITE, sqlite3, :, [AC_MSG_ERROR(dnl
[Could not find sqlite3 devel files:

$SQLITE_PKG_ERRORS

Pass "--without-sqlite" to configure if you want to build libsoup
without sql lite support.])])

fi

AC_SUBST(SQLITE_CFLAGS)
AC_SUBST(SQLITE_LIBS)

AM_CONDITIONAL(SQLITE_SUPPORT, [test $enable_sqlite = yes])

dnl *********************
dnl *** GNOME support ***
dnl *********************
AC_MSG_CHECKING(whether to build libsoup-gnome)
AC_ARG_WITH(gnome,
	    AS_HELP_STRING([--without-gnome], [Do not build libsoup-gnome]),
	    :, [if test $os_win32 = yes; then with_gnome=no; else with_gnome=yes; fi])
AC_MSG_RESULT($with_gnome)

AM_CONDITIONAL(BUILD_LIBSOUP_GNOME, test $with_gnome != no)

if test $with_gnome != no; then
	AC_DEFINE(HAVE_GNOME, 1, [Defined if GNOME support is enabled])
fi
AC_SUBST(HAVE_GNOME)


dnl ***************
dnl *** gtk-doc ***
dnl ***************
dnl GTK_DOC_CHECK([1.10])

dnl *****************************
dnl *** gobject-introspection ***
dnl *****************************
GOBJECT_INTROSPECTION_CHECK([0.9.5])

AC_MSG_CHECKING([for glib-networking (glib TLS implementation)])
save_CFLAGS="$CFLAGS"
save_LIBS="$LIBS"
CFLAGS="$CFLAGS $GLIB_CFLAGS"
LIBS="$LIBS $GLIB_LIBS"
AC_RUN_IFELSE([AC_LANG_PROGRAM([#include <gio/gio.h>],
			       [return !g_tls_backend_supports_tls (g_tls_backend_get_default ());])],
	      [have_glib_networking=yes],
	      [have_glib_networking=no],
	      [have_glib_networking="unknown (cross-compiling)"])
CFLAGS="$save_CFLAGS"
LIBS="$save_LIBS"
AC_MSG_RESULT($have_glib_networking)

AC_ARG_ENABLE(tls-check,
	      AS_HELP_STRING([--disable-tls-check], [Don't error out if glib-networking is unavailable]))
if test "$enable_tls_check" != "no" -a "$have_glib_networking" = "no"; then
	AC_MSG_ERROR([libsoup requires glib-networking for TLS support.

If you are building a package, you can pass --disable-tls-check to
allow building libsoup anyway (since glib-networking is not actually
required at compile time), but you should be sure to add a runtime
dependency on it.])
fi

dnl *************************
dnl *** Tizen dlog support  ***
dnl *************************

AC_ARG_ENABLE(tizen-dlog,
         AS_HELP_STRING([--disable-tizen-dlog], [Disable Tizen dlog support ]),
         enable_tizen_dlog=no,
         enable_tizen_dlog=yes)

AC_MSG_CHECKING([for Tizen dlog])
if test $enable_tizen_dlog != no;then
	AC_DEFINE(ENABLE_TIZEN_DLOG, 1, [Add new feature, which prints logs via Tizen log system named dlog.])
	PKG_CHECK_MODULES(TIZEN_DLOG, dlog)
	AC_SUBST(TIZEN_DLOG_CFLAGS)
	AC_SUBST(TIZEN_DLOG_LIBS)
fi
AC_MSG_RESULT($enable_tizen_dlog)

AM_CONDITIONAL(TIZEN_DLOG, [test $enable_tizen_dlog = yes])

dnl *************************
dnl *** Tizen client certificate support  ***
dnl *************************

AC_ARG_ENABLE(tizen-client-certificate,
	AS_HELP_STRING([--enable-tizen-client-certificate], [Enable Tizen client certificate support ]),        ,
	enable_tizen_client_certificate=no)

AC_MSG_CHECKING([for Tizen client certificate])
if test $enable_tizen_client_certificate != no;then
        AC_DEFINE(ENABLE_TIZEN_TV_CLIENT_CERTIFICATE, 1, [Add new feature, which implement HTTPS connection with client certificate feature])
fi
AC_MSG_RESULT($enable_tizen_client_certificate)

AM_CONDITIONAL(TIZEN_TV_CLIENT_CERTIFICATE, [test $enable_tizen_client_certificate = yes])

dnl *************************
dnl *** Tizen certificate handling  ***
dnl *************************

AC_ARG_ENABLE(tizen-certificate-handling,
	AS_HELP_STRING([--enable-tizen-certificate-handling], [Enable Support for certificate handling( support signal: ACCEPT_CERTIFICATE )]),        ,
	enable_tizen_certificate_handling=no)

AC_MSG_CHECKING([for Tizen certificate handling])
if test $enable_tizen_certificate_handling != no;then
	AC_DEFINE(ENABLE_TIZEN_TV_CERTIFICATE_HANDLING, 1, [Add new feature, which support for certificate handling( signal: ACCEPT_CERTIFICATE )])
fi
AC_MSG_RESULT($enable_tizen_certificate_handling)

AM_CONDITIONAL(TIZEN_TV_CERTIFICATE_HANDLING, [test $enable_tizen_certificate_handling = yes])

dnl ********************************************
dnl *** Tizen support text storage of cookie ***
dnl ********************************************

AC_ARG_ENABLE(tizen-text-storage-mode-of-cookie,
        AS_HELP_STRING([--enable-tizen-text-storage-mode-of-cookie], [Enable Tizen support text storage of cookie]),
        ,
        enable_tizen_text_storage_mode_of_cookie=no)

AC_MSG_CHECKING([for Tizen support text storage of cookie])
if test $enable_tizen_text_storage_mode_of_cookie != no;then
        AC_DEFINE(ENABLE_TIZEN_TV_FIX_TEXT_STORAGE_MODE_OF_COOKIE, 1, [Fix document.cookie get/set cookie not working issue, in case of file:// protocol.])
fi
AC_MSG_RESULT($enable_tizen_text_storage_mode_of_cookie)

AM_CONDITIONAL(ENABLE_TIZEN_TV_FIX_TEXT_STORAGE_MODE_OF_COOKIE, [test $enable_tizen_text_storage_mode_of_cookie = yes])

dnl *******************************************************
dnl *** Tizen support soup cache clean leaked resources ***
dnl *******************************************************

AC_ARG_ENABLE(tizen-soup-cache-clean-leaked-resources,
	AS_HELP_STRING([--enable-tizen-soup-cache-clean-leaked-resources], [Enable Tizen soup cache clean leaked resources ]),        ,
	enable_tizen_soup_cache_clean_leaked_resources=no)

AC_MSG_CHECKING([for Tizen soup cache clean leaked resources])
if test $enable_tizen_soup_cache_clean_leaked_resources != no;then
        AC_DEFINE(ENABLE_TIZEN_TV_SOUP_CACHE_CLEAN_LEAKED_RESOURCES, 1, [Add new feature, which supports soup cache clean leaked resources])
fi
AC_MSG_RESULT($enable_tizen_soup_cache_clean_leaked_resources)

AM_CONDITIONAL(TIZEN_TV_SOUP_CACHE_CLEAN_LEAKED_RESOURCES, [test $enable_tizen_soup_cache_clean_leaked_resources = yes])

dnl *******************************************************
dnl *** Tizen support soup cache optimise load time ***
dnl *******************************************************

AC_ARG_ENABLE(tizen-tv-soup-cache-optimise-load-time,
	AS_HELP_STRING([--enable-tizen-tv-soup-cache-optimise-load-time], [Enable Tizen soup cache optimise load time ]),        ,
	enable_tizen_tv_soup_cache_optimise_load_time=no)

AC_MSG_CHECKING([for Tizen soup cache optimise load time])
if test $enable_tizen_tv_soup_cache_optimise_load_time != no;then
        AC_DEFINE(ENABLE_TIZEN_TV_SOUP_CACHE_OPTIMISE_LOAD_TIME, 1, [Add new feature, which supports soup cache optimised load time])
fi
AC_MSG_RESULT($enable_tizen_tv_soup_cache_optimise_load_time)

AM_CONDITIONAL(TIZEN_TV_SOUP_CACHE_OPTIMISE_LOAD_TIME, [test $enable_tizen_tv_soup_cache_optimise_load_time = yes])

dnl *************************************************************
dnl *** Tizen doesn't cache video and audio resources on disk ***
dnl *************************************************************

AC_ARG_ENABLE(tizen-tv-no-cache-about-video-and-audio,
    AS_HELP_STRING([--enable-tizen-tv-no-cache-about-video-and-audio], [Enable Tizen doesn't cache video and audio resources on disk]),
    ,
    enable_tizen_tv_no_cache_about_video_and_audio=no)

AC_MSG_CHECKING([for Tizen doesn't cache video and audio])
if test $enable_tizen_tv_no_cache_about_video_and_audio != no;then
        AC_DEFINE(ENABLE_TIZEN_TV_NO_CACHE_ABOUT_VIDEO_AND_AUDIO, 1, [Add new feature, which doesn't cache video and audio resources on disk])
fi
AC_MSG_RESULT($enable_tizen_tv_no_cache_about_video_and_audio)

AM_CONDITIONAL(TIZEN_TV_NO_CACHE_ABOUT_VIDEO_AND_AUDIO, [test $enable_tizen_tv_no_cache_about_video_and_audio = yes])

dnl *************************
dnl *** Tizen use expanded response block ***
dnl *************************

AC_ARG_ENABLE(tizen-use-expanded-response-block,
	AS_HELP_STRING([--enable-tizen-use-expanded-response-block], [Enable Tizen use expanded response block ]),	,
	enable_tizen_use_expanded_response_block=no)

AC_MSG_CHECKING([for Tizen use expanded response block])
if test $enable_tizen_use_expanded_response_block != no;then
	AC_DEFINE(ENABLE_TIZEN_USE_EXPANDED_RESPONSE_BLOCK, 1, [Add new feature, which implement HTTPS connection with client certificate feature])
fi
AC_MSG_RESULT($enable_tizen_use_expanded_response_block)

AM_CONDITIONAL(TIZEN_USE_EXPANDED_RESPONSE_BLOCK, [test $enable_tizen_use_expanded_response_block = yes])

dnl ***********************************************
dnl *** Tizen support create idle tcp connection ***
dnl ***********************************************

AC_ARG_ENABLE(tizen-create-idle-tcp-connection,
        AS_HELP_STRING([--enable-tizen-create-idle-tcp-connection], [Enable Tizen create idle tcp connection ]),        ,
        enable_tizen_create_idle_tcp_connection=no)

AC_MSG_CHECKING([for Tizen create idle tcp connection])
if test $enable_tizen_create_idle_tcp_connection != no;then
        AC_DEFINE(ENABLE_TIZEN_TV_CREATE_IDLE_TCP_CONNECTION, 1, [Add new feature, which supports Create Idle tcp connections for pre-connection])
fi
AC_MSG_RESULT($enable_tizen_create_idle_tcp_connection)

AM_CONDITIONAL(TIZEN_TV_CREATE_IDLE_TCP_CONNECTION, [test $enable_tizen_create_idle_tcp_connection = yes])

dnl *************************
dnl *** Tizen disable mime  sniff  ***
dnl *************************

AC_ARG_ENABLE(tizen-disable-mime-sniff,
        AS_HELP_STRING([--enable-tizen-disable-mime-sniff], [Enable Tizen disable mime  sniff support ]),        ,
        enable_tizen_disable_mime_sniff=no)

AC_MSG_CHECKING([for Tizen disable mime  sniff])
if test $enable_tizen_disable_mime_sniff != no;then
        AC_DEFINE(ENABLE_TIZEN_TV_DISABLE_MIME_SNIFF, 1, [Provide an interface for Webkit to disable MIME sniff when content-type is unknown.])
fi
AC_MSG_RESULT($enable_tizen_disable_mime_sniff)

AM_CONDITIONAL(TIZEN_TV_DISABLE_MIME_SNIFF, [test $enable_tizen_disable_mime_sniff = yes])

dnl ****************************
dnl *** Tizen soup store dns ***
dnl ****************************

AC_ARG_ENABLE(tizen-soup-store-dns,
        AS_HELP_STRING([--enable-tizen-soup-store-dns], [Enable Tizen soup store dns ]),        ,
        enable_tizen_soup_store_dns=no)

AC_MSG_CHECKING([for Tizen soup store dns])
if test $enable_tizen_soup_store_dns != no;then
        AC_DEFINE(ENABLE_TIZEN_TV_SOUP_STORE_DNS, 1, [Maintain a DNS cache in soup library  to reduce DNS request time])
fi
AC_MSG_RESULT($enable_tizen_soup_store_dns)

AM_CONDITIONAL(TIZEN_TV_SOUP_STORE_DNS, [test $enable_tizen_soup_store_dns = yes])

dnl ***********************************************
dnl *** Tizen support soup immediate requesting ***
dnl ***********************************************

AC_ARG_ENABLE(tizen-immediate-requesting,
	AS_HELP_STRING([--enable-tizen-immediate-requesting], [Enable Tizen soup immediate requesting ]),        ,
	enable_tizen_immediate_requesting=no)

AC_MSG_CHECKING([for Tizen soup immediate requesting])
if test $enable_tizen_immediate_requesting != no;then
        AC_DEFINE(ENABLE_TIZEN_TV_IMMEDIATE_REQUESTING, 1, [Add new feature, which supports soup immediate requesting])
fi
AC_MSG_RESULT($enable_tizen_immediate_requesting)

AM_CONDITIONAL(TIZEN_TV_IMMEDIATE_REQUESTING, [test $enable_tizen_immediate_requesting = yes])

dnl ***********************************************
dnl *** Tizen support computing disk cache size ***
dnl ***********************************************

AC_ARG_ENABLE(tizen-computing-disk-cache-size,
	AS_HELP_STRING([--enable-tizen-computing-disk-cache-size], [Enable Tizen computing disk cache size support ]),        ,
	enable_tizen_computing_disk_cache_size=no)

AC_MSG_CHECKING([for Tizen computing disk cache size])
if test $enable_tizen_computing_disk_cache_size != no;then
        AC_DEFINE(ENABLE_TIZEN_TV_COMPUTING_DISK_CACHE_SIZE, 1, [Add new feature, which supports entry length as disk cache size])
fi
AC_MSG_RESULT($enable_tizen_computing_disk_cache_size)

AM_CONDITIONAL(TIZEN_TV_COMPUTING_DISK_CACHE_SIZE, [test $enable_tizen_computing_disk_cache_size = yes])

dnl ***********************************************
dnl *** Tizen support force preload tlsdb***
dnl ***********************************************
AC_ARG_ENABLE(tizen-tv-force-preload-tlsdb,
        AS_HELP_STRING([--enable-tizen-tv-force-preload-tlsdb], [Enable Tizen force preload tlsdb ]),        ,
        enable_tizen_tv_force_preload_tlsdb=no)

AC_MSG_CHECKING([for Tizen force preload tlsdb])
if test $enable_tizen_tv_force_preload_tlsdb != no;then
        AC_DEFINE(ENABLE_TIZEN_TV_FORCE_PRELOAD_TLSDB, 1, [Add new feature, which supports to pre load TLS database])
fi
AC_MSG_RESULT($enable_tizen_tv_force_preload_tlsdb)

AM_CONDITIONAL(TIZEN_TV_FORCE_PRELOAD_TLSDB, [test $enable_tizen_tv_force_preload_tlsdb = yes])

dnl ****************************************
dnl *** Tizen add x soup message headers ***
dnl ****************************************

AC_ARG_ENABLE(tizen-add-x-soup-message-headers,
        AS_HELP_STRING([--enable-tizen-add-x-soup-message-headers], [Enable Tizen add X-From-Cache and X-Entry-Length soup message headers]),
        ,
        enable_tizen_add_x_soup_message_headers=no)

AC_MSG_CHECKING([for Tizen support text storage of cookie])
if test $enable_tizen_add_x_soup_message_headers != no;then
        AC_DEFINE(ENABLE_TIZEN_TV_ADD_X_SOUP_MESSAGE_HEADERS, 1, [Add X-From-Cache and X-Entry-Length header.])
fi
AC_MSG_RESULT($enable_tizen_add_x_soup_message_headers)

AM_CONDITIONAL(ENABLE_TIZEN_TV_ADD_X_SOUP_MESSAGE_HEADERS, [test $enable_tizen_add_x_soup_message_headers = yes])

dnl ******************************************
dnl *** Tizen dynamic certificate loading  ***
dnl ******************************************

AC_ARG_ENABLE(tizen-dynamic-certificate-loading,
	AS_HELP_STRING([--enable-tizen-dynamic-certificate_loading], [Enable dynamic SSL Certificate loading support]),        ,
	enable_tizen_dynamic_certificate_loading=no)

AC_MSG_CHECKING([for Tizen dynamic certificate loading])
if test $enable_tizen_dynamic_certificate_loading != no;then
        AC_DEFINE(ENABLE_TIZEN_TV_DYNAMIC_CERTIFICATE_LOADING, 1, [Add new feature, which implement support dynamic SSL Certificate Loading])
fi
AC_MSG_RESULT($enable_tizen_dynamic_certificate_loading)

AM_CONDITIONAL(TIZEN_TV_DYNAMIC_CERTIFICATE_LOADING, [test $enable_tizen_dynamic_certificate_loading = yes])

dnl ***************************************************
dnl *** Tizen checking deleted entry files support  ***
dnl ***************************************************

AC_ARG_ENABLE(tizen-tv-checking-deleted-entry-file,
	AS_HELP_STRING([--enable-tizen-tv-checking-deleted-entry-file], [Enable Tizen checking deleted entry files support ]),        ,
	enable_tizen_tv_checking_deleted_entry_file=no)

AC_MSG_CHECKING([for Tizen checking deleted entry files])
if test $enable_tizen_tv_checking_deleted_entry_file != no;then
        AC_DEFINE(ENABLE_TIZEN_TV_CHECKING_DELETED_ENTRY_FILE, 1, [Checking deleted entry files before soup_cache_load()])
fi
AC_MSG_RESULT($enable_tizen_tv_checking_deleted_entry_file)

AM_CONDITIONAL(TIZEN_TV_CHECKING_DELETED_ENTRY_FILE, [test $enable_tizen_tv_checking_deleted_entry_file = yes])

dnl *******************************
dnl *** Tizen performance test  ***
dnl *******************************

AC_ARG_ENABLE(tizen-performance-test-log,
	AS_HELP_STRING([--enable-tizen-performance-test-log], [Enable Tizen performance test log]),        ,
	enable_tizen_performance_test_log=no)

AC_MSG_CHECKING([for Tizen performance test log])
if test $enable_tizen_performance_test_log != no;then
	AC_DEFINE(ENABLE_TIZEN_PERFORMANCE_TEST_LOG, 1, [Add performance test log])
fi
AC_MSG_RESULT($enable_tizen_performance_test_log)

AM_CONDITIONAL(TIZEN_PERFORMANCE_TEST_LOG, [test $enable_tizen_performance_test_log = yes])

dnl ************************************************************************
dnl *** Use soupTimeOffset to adjust time for certificate or cookie case ***
dnl ************************************************************************

AC_ARG_ENABLE(tizen-tv-adjust-time,
    AS_HELP_STRING([--enable-tizen-tv-adjust-time], [Enable Tizen use soupTimeOffset to adjust time for certificate or cookie case]),        ,
    enable_tizen_tv_adjust_time=no)

AC_MSG_CHECKING([for Tizen use soupTimeOffset to adjust time for certificate or cookie case])
if test $enable_tizen_tv_adjust_time != no;then
        AC_DEFINE(ENABLE_TIZEN_TV_ADJUST_TIME, 1, [Add new feature, which use soupTimeOffset to adjust time for certificate or cookie case])
fi
AC_MSG_RESULT($enable_tizen_tv_adjust_time)

AM_CONDITIONAL(TIZEN_TV_ADJUST_TIME, [test $enable_tizen_tv_adjust_time = yes])

dnl ******************************
dnl *** Stuff for regression tests
dnl ******************************
AC_MSG_NOTICE([checking for programs needed for regression tests])

AC_ARG_WITH(apache-httpd,
	    AS_HELP_STRING([--with-apache-httpd], [Path to apache httpd (for tests)]),
	    APACHE_HTTPD="$withval",
	    [AC_PATH_PROGS(APACHE_HTTPD, httpd2 httpd apache2 apache, no, ${PATH}:/usr/sbin)])
if test "$APACHE_HTTPD" != "no"; then
    AC_MSG_CHECKING([Apache version])
    apache_version=`$APACHE_HTTPD -v 2>/dev/null | sed -ne 's/Server version: Apache\///p'`
    case $apache_version in
    2.2.*)
	AC_MSG_RESULT([$apache_version (ok)])
 	apache_version=2.2
	;;
    2.4.*)
	AC_MSG_RESULT([$apache_version (ok)])
 	apache_version=2.4
	;;
    *)
	AC_MSG_RESULT([$apache_version (ignoring)])
	APACHE_HTTPD="no"
	;;
    esac
fi
AC_SUBST(APACHE_HTTPD)
AC_DEFINE_UNQUOTED(APACHE_HTTPD, "$APACHE_HTTPD", [Apache httpd])

if test "$APACHE_HTTPD" != "no"; then
    AC_MSG_CHECKING([for Apache module directory])
    AC_ARG_WITH(apache-module-dir,
		AS_HELP_STRING([--with-apache-module-dir], [Apache modules dirs (for tests)]),
		apache_module_dirs="$withval",
		[apache_prefix=`dirname \`dirname $APACHE_HTTPD\``
		mpm=`$APACHE_HTTPD -V -C "ServerName localhost" | sed -ne 's/^Server MPM: */-/p' | tr 'A-Z' 'a-z'`
		# This only works with bash, but should fail harmlessly in sh
		apache_module_dirs=`echo $apache_prefix/lib{64,}/{apache,apache2,http,http2,httpd}{$mpm,}{/modules,}`])
    for dir in $apache_module_dirs; do
        if test -f $dir/mod_auth_digest.so; then
	    APACHE_MODULE_DIR="$dir"
        fi
        if test -f $dir/mod_ssl.so; then
	    APACHE_SSL_MODULE_DIR="$dir"
	    IF_HAVE_APACHE_SSL=""
        fi
        if test -f $dir/mod_php5.so; then
	    APACHE_PHP_MODULE_DIR="$dir"
	    APACHE_PHP_MODULE=mod_php5.so
        fi
        if test -f $dir/libphp5.so; then
	    APACHE_PHP_MODULE_DIR="$dir"
	    APACHE_PHP_MODULE=libphp5.so
        fi
    done
    AC_MSG_RESULT($APACHE_MODULE_DIR)
    AC_SUBST(APACHE_MODULE_DIR)
    AC_SUBST(APACHE_SSL_MODULE_DIR)
    AC_SUBST(APACHE_PHP_MODULE_DIR)
    AC_SUBST(APACHE_PHP_MODULE)
fi

if test "$APACHE_HTTPD" != "no" -a -n "$APACHE_MODULE_DIR" -a -n "$APACHE_SSL_MODULE_DIR"; then
    AC_DEFINE(HAVE_APACHE, 1, [Whether or not apache can be used for tests])
    if test $apache_version = 2.2; then
        AC_DEFINE(HAVE_APACHE_2_2, 1, [Apache is 2.2.x])
    else
        AC_DEFINE(HAVE_APACHE_2_4, 1, [Apache is 2.4.x])
    fi
    have_apache=1
else
    have_apache=0
fi
AM_CONDITIONAL(HAVE_APACHE, test "$have_apache" = 1)
AM_CONDITIONAL(HAVE_APACHE_2_2, test "$apache_version" = 2.2)
AM_CONDITIONAL(HAVE_APACHE_2_4, test "$apache_version" = 2.4)

if test "$have_apache" = 1; then
    AC_CHECK_PROGS(PHP, php php5)

    AC_MSG_CHECKING([for Apache PHP module])
    if test -f $APACHE_PHP_MODULE_DIR/$APACHE_PHP_MODULE; then
	have_php=yes
	IF_HAVE_PHP=""
    else
	have_php=no
	IF_HAVE_PHP="\#"
    fi
    AC_MSG_RESULT($have_php)
    AC_SUBST(IF_HAVE_PHP)

    if test "$have_php" = yes; then
	AC_MSG_CHECKING([for php-xmlrpc])
	if $PHP --rf xmlrpc_server_create | grep -q "does not exist"; then
	    have_php_xmlrpc=no
	else
	    have_php_xmlrpc=yes
	    AC_DEFINE(HAVE_PHP_XMLRPC, 1, [Have php-xmlrpc])
	fi
	AC_MSG_RESULT($have_php_xmlrpc)
    fi
fi

AC_PATH_PROG(CURL, curl, no)
if test "$CURL" != no; then
    AC_DEFINE(HAVE_CURL, 1, [Whether or not curl can be used for tests])
fi

dnl **********************************************************
dnl *** path of NTLM single-sign-on helper ntlm_auth
dnl **********************************************************
AC_ARG_WITH(ntlm-auth,
	    AC_HELP_STRING([--with-ntlm-auth=PATH],[Where to look for ntlm_auth, path points to ntlm_auth installation (default: /usr/bin/ntlm_auth)]),
	    ntlm_auth="$withval",
	    [if test $os_win32 = yes; then ntlm_auth="no"; else ntlm_auth="/usr/bin/ntlm_auth"; fi])
if test "$ntlm_auth" != "no"; then
    AC_DEFINE(USE_NTLM_AUTH, 1, [Whether or not use Samba's 'winbind' daemon helper 'ntlm_auth' for NTLM single-sign-on])
    if test "$ntlm_auth" = "yes"; then
	dnl --with-ntlm-auth (without path) used, use default path
	ntlm_auth="/usr/bin/ntlm_auth"
    fi
fi
AC_SUBST(ntlm_auth)
AC_DEFINE_UNQUOTED(NTLM_AUTH, "$ntlm_auth", [Samba's 'winbind' daemon helper 'ntlm_auth' which can be used for NTLM single-sign-on])

dnl ****************************************************
dnl *** Warnings to show if using GCC                ***
dnl *** (do this last so -Werror won't mess up tests ***
dnl ****************************************************

AC_ARG_ENABLE(more-warnings,
	      AS_HELP_STRING([--disable-more-warnings], [Inhibit compiler warnings]),
	      set_more_warnings=no)

if test "$GCC" = "yes" -a "$set_more_warnings" != "no"; then
	CFLAGS="$CFLAGS \
		-Wall -Wstrict-prototypes -Werror=missing-prototypes \
		-Werror=implicit-function-declaration \
		-Werror=pointer-arith -Werror=init-self -Werror=format=2 \
		-Wno-format-zero-length \
		-Werror=missing-include-dirs -Werror=aggregate-return \
		-Werror=declaration-after-statement"
fi

dnl *************************
dnl *** Output Everything ***
dnl *************************

AC_CONFIG_HEADERS([config.h])
AC_CONFIG_FILES([
	libsoup-2.4.pc
	libsoup-gnome-2.4.pc
	Makefile
	libsoup-zip
	libsoup/Makefile
	po/Makefile.in
	po/Makefile
	tests/Makefile
	examples/Makefile
	docs/Makefile
	docs/reference/Makefile
	libsoup/soup-version.h
	])
AC_OUTPUT
