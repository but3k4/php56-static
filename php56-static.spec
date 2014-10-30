# Define if it's a locaweb package
%bcond_with locaweb

# Build a static package
%bcond_with static

%if %{with static}
# Package suffix
%global _suffix 56
%endif

# API/ABI check
%global apiver      20131106
%global zendver     20131226
%global pdover      20080721
# Extension version
%global opcachever  7.0.4-dev

# Use for first build of PHP (before pecl/zip and pecl/jsonc)
%global php_bootstrap   1

# Adds -z now to the linker flags
%global _hardened_build 1

# version used for php embedded library soname
%global embed_version 5.6

%global mysql_sock %(mysql_config --socket 2>/dev/null || echo /var/lib/mysql/mysql.sock)

# Build for LiteSpeed Web Server (LSAPI)
%global with_lsws     1

# Regression tests take a long time, you can skip 'em with this
%if %{php_bootstrap}
%global runselftest 0
%else
%{!?runselftest: %global runselftest 1}
%endif

# Use the arch-specific mysql_config binary to avoid mismatch with the
# arch detection heuristic used by bindir/mysql_config.
%global mysql_config %{_bindir}/mysql_config

# Build mysql/mysqli/pdo extensions using libmysqlclient or only mysqlnd
%global with_libmysql 1
 
%if 0%{?rhel} >= 7
%global with_libpcre	1
%else
%global with_libpcre	0
%endif

%if 0%{?rhel} < 6
%global  with_vpx  0
%else
%global  with_vpx  1
%endif

# Build ZTS extension or only NTS
%global with_zts      1

# Debuild build
%global with_debug    %{?_with_debug:1}%{!?_with_debug:0}

# /usr/sbin/apsx with httpd < 2.4 and defined as /usr/bin/apxs with httpd >= 2.4
%{!?_httpd_apxs:       %{expand: %%global _httpd_apxs       %%{_sbindir}/apxs}}
%{!?_httpd_mmn:        %{expand: %%global _httpd_mmn        %%(cat %{_includedir}/httpd/.mmn 2>/dev/null || echo 0-0)}}
%{!?_httpd_confdir:    %{expand: %%global _httpd_confdir    %%{_sysconfdir}/httpd/conf.d}}
# /etc/httpd/conf.d with httpd < 2.4 and defined as /etc/httpd/conf.modules.d with httpd >= 2.4
%{!?_httpd_modconfdir: %{expand: %%global _httpd_modconfdir %%{_sysconfdir}/httpd/conf.d}}
%{!?_httpd_moddir:     %{expand: %%global _httpd_moddir     %%{_libdir}/httpd/modules}}
%{!?_httpd_contentdir: %{expand: %%global _httpd_contentdir /var/www}}

%if %{with locaweb}
%global _httpd_user webserver
%else
%global _httpd_user apache
%endif

%global macrosdir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

# systemd to manage the service
%if 0%{?rhel} >= 7
%global with_systemd 1
%else
%global with_systemd 0
%endif

# systemd with notify mode
%if 0%{?rhel} >= 7
%global with_systemdfull 1
%else
%global with_systemdfull 0
%endif
# systemd with additional service config
%if 0%{?rhel} >= 7
%global with_systemdmax 1
%else
%global with_systemdmax 0
%endif

%if 0%{?rhel} >= 6
%global with_dtrace 1
%else
%global with_dtrace 0
%endif
%if 0%{?rhel} < 5
%global with_libgd   0
%else
%global with_libgd   1
%endif

%if 0%{?rhel} < 7
%global with_libzip  0
%else
%global with_libzip  1
%endif
%global with_zip     1

%if 0%{?rhel} < 7
%global db_devel  db4-devel
%else
%global db_devel  libdb-devel
%endif

Summary: PHP scripting language for creating dynamic web sites
Name: php%{?_suffix}
Version: 5.6.2
%if %{with locaweb}
Release: 1.lw
%else
Release: 1%{?dist}
%endif
# All files licensed under PHP version 3.01, except
# Zend is licensed under Zend
# TSRM is licensed under BSD
License: PHP and Zend and BSD
Group: Development/Languages
URL: http://www.php.net/
Source0: php-%{version}.tar.bz2
Source1: php56.conf
Source2: php56.ini
Source3: macros56.php
Source4: php56-fpm.conf
Source5: php56-fpm-www.conf
Source6: php56-fpm.service
Source7: php56-fpm.logrotate
Source8: php56-fpm.sysconfig
Source9: php56.modconf
Source10: php56.ztsmodconf
#Source11: strip.sh
# Configuration files for some extensions
Source50: opcache56.ini
Source51: opcache56-default.blacklist
Source99: php56-fpm.init

# Build fixes
Patch5: php-5.2.0-includedir.patch
Patch6: php-5.2.4-embed.patch
Patch7: php-5.3.0-recode.patch
Patch8: php-5.4.7-libdb.patch

# Fixes for extension modules
# https://bugs.php.net/63171 no odbc call during timeout
Patch21: php-5.4.7-odbctimer.patch

# Functional changes
Patch40: php-5.4.0-dlopen.patch
Patch42: php-5.3.1-systzdata-v11.patch
# See http://bugs.php.net/53436
Patch43: php-5.4.0-phpize.patch
# Use -lldap_r for OpenLDAP
Patch45: php-5.4.8-ldap_r.patch
# Make php_config.h constant across builds
Patch46: php-5.4.9-fixheader.patch
# drop "Configure command" from phpinfo output
Patch47: php-5.4.9-phpinfo.patch

Patch48: php-5.5.0-icuconfig.patch

# Upstream fixes (100+)
Patch100: php-bug68074.patch

# Security fixes (200+)

# Locaweb static patch
Patch212: php56-locaweb-static.patch

# Fixes for tests (300+)
# Revert changes for pcre < 8.34
Patch301: php-5.6.0-oldpcre.patch
# see https://bugzilla.redhat.com/971416
Patch302: php-5.6.0-noNO.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: bzip2-devel, curl-devel >= 7.9
BuildRequires: httpd-devel >= 2.0.46-1, pam-devel
BuildRequires: libstdc++-devel, openssl-devel
%if 0%{?rhel} >= 6
# For Sqlite3 extension
BuildRequires: sqlite-devel >= 3.6.0
%else
BuildRequires: sqlite-devel >= 3.0.0
%endif
BuildRequires: zlib-devel, smtpdaemon, libedit-devel
%if %{with_libpcre}
BuildRequires: pcre-devel >= 8.20
%endif
BuildRequires: bzip2, perl, libtool >= 1.4.3, gcc-c++
BuildRequires: libtool-ltdl-devel
%if %{with_libzip}
BuildRequires: libzip-devel >= 0.11
%endif
%if %{with_dtrace}
BuildRequires: systemtap-sdt-devel
%endif

%if %{with_zts}
Provides: %{name}-zts = %{version}-%{release}
%endif

Requires: httpd-mmn = %{_httpd_mmn}
Provides: mod_php = %{version}-%{release}
Requires: %{name}-common = %{version}-%{release}
# For backwards-compatibility, require php-cli for the time being:
Requires: %{name}-cli = %{version}-%{release}
# To ensure correct /var/lib/php/session ownership:
Requires(pre): httpd
# php engine for Apache httpd webserver
Provides: php(httpd)

%if 0%{?rhel} < 7
# Don't provides extensions, which are not shared library, as .so
%{?filter_provides_in: %filter_provides_in %{_libdir}/php%{?_suffix}/modules/.*\.so$}
%if %{with_zts}
%{?filter_provides_in: %filter_provides_in %{_libdir}/php%{?_suffix}-zts/modules/.*\.so$}
%endif
%{?filter_provides_in: %filter_provides_in %{_httpd_moddir}/.*\.so$}
%{?filter_setup}
%endif

%description
PHP is an HTML-embedded scripting language. PHP attempts to make it
easy for developers to write dynamically generated web pages. PHP also
offers built-in database integration for several commercial and
non-commercial database management systems, so writing a
database-enabled webpage with PHP is fairly simple. The most common
use of PHP coding is probably as a replacement for CGI scripts.

The php package contains the module (often referred to as mod_php)
which adds support for the PHP language to Apache HTTP Server.

%package cli
Group: Development/Languages
Summary: Command-line interface for PHP
Requires: %{name}-common = %{version}-%{release}
Provides: php-cgi = %{version}-%{release}
Provides: php-pcntl
Provides: php-readline

%description cli
The php-cli package contains the command-line interface
executing PHP scripts, /usr/bin/php, and the CGI interface.

%package dbg
Group: Development/Languages
Summary: The interactive PHP debugger
Requires: %{name}-common = %{version}-%{release}

%description dbg
The php-dbg package contains the interactive PHP debugger.

%package fpm
Group: Development/Languages
Summary: PHP FastCGI Process Manager
# All files licensed under PHP version 3.01, except
# Zend is licensed under Zend
# TSRM and fpm are licensed under BSD
License: PHP and Zend and BSD
Requires(pre): %{_sbindir}/useradd
Requires: %{name}-common = %{version}-%{release}
%if %{with_systemdfull}
BuildRequires: systemd-devel
%endif
%if %{with_systemd}
BuildRequires: systemd-units
Requires: systemd-units
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
# This is actually needed for the %%triggerun script but Requires(triggerun)
# is not valid.  We can use %%post because this particular %%triggerun script
# should fire just after this package is installed.
Requires(post): systemd-sysv
%else
# This is for /sbin/service
Requires(preun): initscripts
Requires(postun): initscripts
# php engine for Apache httpd webserver
Provides: php(httpd)
%endif

%description fpm
PHP-FPM (FastCGI Process Manager) is an alternative PHP FastCGI
implementation with some additional features useful for sites of
any size, especially busier sites.

%if %{with_lsws}
%package litespeed
Summary: LiteSpeed Web Server PHP support
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}

%description litespeed
The php-litespeed package provides the %{_bindir}/lsphp command
used by the LiteSpeed Web Server (LSAPI enabled PHP).
%endif

%package common
Group: Development/Languages
Summary: Common files for PHP
# All files licensed under PHP version 3.01, except
# fileinfo is licensed under PHP version 3.0
# regex, libmagic are licensed under BSD
# main/snprintf.c, main/spprintf.c and main/rfc1867.c are ASL 1.0
License: PHP and BSD and ASL 1.0
# ABI/API check - Arch specific
Provides: php(api) = %{apiver}
Provides: php(zend-abi) = %{zendver}
Provides: php(language) = %{version}
# Provides for all builtin/shared modules:
Provides: php-bz2
Provides: php-calendar
Provides: php-core = %{version}
Provides: php-ctype
Provides: php-curl
Provides: php-date
Provides: php-ereg
Provides: php-exif
Provides: php-fileinfo
Provides: php-filter
Provides: php-ftp
Provides: php-gettext
Provides: php-hash
Provides: php-mhash = %{version}
Provides: php-iconv
Provides: php-libxml
Provides: php-openssl
Provides: php-phar
Provides: php-pcre
Provides: php-reflection
Provides: php-session
Provides: php-sockets
Provides: php-spl
Provides: php-standard = %{version}
Provides: php-tokenizer
%if ! %{php_bootstrap}
Requires: %{name}-pecl-jsonc
%endif
%if %{with_zip}
Provides: php-zip
%else
%if ! %{php_bootstrap}
Requires: %{name}-pecl-zip
%endif
%endif
Provides: php-zlib

%description common
The php-common package contains files used by both the php
package and the php-cli package.

%package devel
Group: Development/Libraries
Summary: Files needed for building PHP extensions
Requires: %{name}-cli = %{version}-%{release}, autoconf, automake
%if %{with_libpcre}
Requires: pcre-devel
%endif
%if %{with_zts}
Provides: %{name}-zts-devel = %{version}-%{release}
%endif
%if ! %{php_bootstrap}
Requires: %{name}-pecl-jsonc-devel
%endif

%description devel
The php-devel package contains the files needed for building PHP
extensions. If you need to compile your own PHP extensions, you will
need to install this package.

%package opcache
Summary: The Zend OPcache
Group: Development/Languages
License: PHP
Requires: %{name}-common = %{version}-%{release}
Provides: php-pecl-zendopcache = %{opcachever}
Provides: php-pecl(opcache) = %{opcachever}

%description opcache
The Zend OPcache provides faster PHP execution through opcode caching and
optimization. It improves PHP performance by storing precompiled script
bytecode in the shared memory. This eliminates the stages of reading code from
the disk and compiling it on future access. In addition, it applies a few
bytecode optimization patterns that make code execution faster.

%package imap
Summary: A module for PHP applications that use IMAP
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{name}-common = %{version}-%{release}
BuildRequires: krb5-devel, openssl-devel, libc-client-devel

%description imap
The php-imap module will add IMAP (Internet Message Access Protocol)
support to PHP. IMAP is a protocol for retrieving and uploading e-mail
messages on mail servers. PHP is an HTML-embedded scripting language.

%package ldap
Summary: A module for PHP applications that use LDAP
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{name}-common = %{version}-%{release}
BuildRequires: cyrus-sasl-devel, openldap-devel, openssl-devel

%description ldap
The php-ldap package adds Lightweight Directory Access Protocol (LDAP)
support to PHP. LDAP is a set of protocols for accessing directory
services over the Internet. PHP is an HTML-embedded scripting
language.

%package pdo
Summary: A database access abstraction module for PHP applications
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{name}-common = %{version}-%{release}
# ABI/API check - Arch specific
Provides: php-pdo-abi = %{pdover}
Provides: php(pdo-abi) = %{pdover}
Provides: php-sqlite3
Provides: php-pdo_sqlite

%description pdo
The php-pdo package contains a dynamic shared object that will add
a database access abstraction layer to PHP.  This module provides
a common interface for accessing MySQL, PostgreSQL or other
databases.

%if %{with_libmysql}
%package mysql
Summary: A module for PHP applications that use MySQL databases
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{name}-pdo = %{version}-%{release}
Provides: php_database
Provides: php-mysqli = %{version}-%{release}
Provides: php-pdo_mysql
%if %{with locaweb}
BuildRequires: Percona-Server-devel-51
%else
BuildRequires: mysql-devel >= 4.1.0
%endif
Conflicts: %{name}-mysqlnd

%description mysql
The php-mysql package contains a dynamic shared object that will add
MySQL database support to PHP. MySQL is an object-relational database
management system. PHP is an HTML-embeddable scripting language. If
you need MySQL support for PHP applications, you will need to install
this package and the php package.
%endif

%package mysqlnd
Summary: A module for PHP applications that use MySQL databases
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{name}-pdo = %{version}-%{release}
Provides: php_database
Provides: php-mysql = %{version}-%{release}
Provides: php-mysqli = %{version}-%{release}
Provides: php-pdo_mysql
%if ! %{with_libmysql}
Obsoletes: php-mysql < %{version}
%endif

%description mysqlnd
The php-mysqlnd package contains a dynamic shared object that will add
MySQL database support to PHP. MySQL is an object-relational database
management system. PHP is an HTML-embeddable scripting language. If
you need MySQL support for PHP applications, you will need to install
this package and the php package.

This package use the MySQL Native Driver

%package pgsql
Summary: A PostgreSQL database module for PHP
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{name}-pdo = %{version}-%{release}
Provides: php_database
Provides: php-pdo_pgsql
BuildRequires: krb5-devel, openssl-devel, postgresql-devel

%description pgsql
The php-pgsql package add PostgreSQL database support to PHP.
PostgreSQL is an object-relational database management
system that supports almost all SQL constructs. PHP is an
HTML-embedded scripting language. If you need back-end support for
PostgreSQL, you should install this package in addition to the main
php package.

%package process
Summary: Modules for PHP script using system process interfaces
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{name}-common = %{version}-%{release}
Provides: php-posix
Provides: php-shmop
Provides: php-sysvsem
Provides: php-sysvshm
Provides: php-sysvmsg

%description process
The php-process package contains dynamic shared objects which add
support to PHP using system interfaces for inter-process
communication.

%package odbc
Summary: A module for PHP applications that use ODBC databases
Group: Development/Languages
# All files licensed under PHP version 3.01, except
# pdo_odbc is licensed under PHP version 3.0
License: PHP
Requires: %{name}-pdo = %{version}-%{release}
Provides: php_database
Provides: php-pdo_odbc
BuildRequires: unixODBC-devel

%description odbc
The php-odbc package contains a dynamic shared object that will add
database support through ODBC to PHP. ODBC is an open specification
which provides a consistent API for developers to use for accessing
data sources (which are often, but not always, databases). PHP is an
HTML-embeddable scripting language. If you need ODBC support for PHP
applications, you will need to install this package and the php
package.

%package soap
Summary: A module for PHP applications that use the SOAP protocol
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{name}-common = %{version}-%{release}
BuildRequires: libxml2-devel

%description soap
The php-soap package contains a dynamic shared object that will add
support to PHP for using the SOAP web services protocol.

%package interbase
Summary: A module for PHP applications that use Interbase/Firebird databases
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
BuildRequires: firebird-devel
Requires: %{name}-pdo = %{version}-%{release}
Provides: php_database
Provides: php-firebird
Provides: php-pdo_firebird

%description interbase
The php-interbase package contains a dynamic shared object that will add
database support through Interbase/Firebird to PHP.

InterBase is the name of the closed-source variant of this RDBMS that was
developed by Borland/Inprise.

Firebird is a commercially independent project of C and C++ programmers,
technical advisors and supporters developing and enhancing a multi-platform
relational database management system based on the source code released by
Inprise Corp (now known as Borland Software Corp) under the InterBase Public
License.

%package snmp
Summary: A module for PHP applications that query SNMP-managed devices
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{name}-common = %{version}-%{release}, net-snmp
BuildRequires: net-snmp-devel

%description snmp
The php-snmp package contains a dynamic shared object that will add
support for querying SNMP devices to PHP.  PHP is an HTML-embeddable
scripting language. If you need SNMP support for PHP applications, you
will need to install this package and the php package.

%package xml
Summary: A module for PHP applications which use XML
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{name}-common = %{version}-%{release}
Provides: php-dom
Provides: php-domxml
Provides: php-simplexml
Provides: php-wddx
Provides: php-xmlreader
Provides: php-xmlwriter
Provides: php-xsl
BuildRequires: libxslt-devel >= 1.0.18-1, libxml2-devel >= 2.4.14-1

%description xml
The php-xml package contains dynamic shared objects which add support
to PHP for manipulating XML documents using the DOM tree,
and performing XSL transformations on XML documents.

%package xmlrpc
Summary: A module for PHP applications which use the XML-RPC protocol
Group: Development/Languages
# All files licensed under PHP version 3.01, except
# libXMLRPC is licensed under BSD
License: PHP and BSD
Requires: %{name}-common = %{version}-%{release}

%description xmlrpc
The php-xmlrpc package contains a dynamic shared object that will add
support for the XML-RPC protocol to PHP.

%package mbstring
Summary: A module for PHP applications which need multi-byte string handling
Group: Development/Languages
# All files licensed under PHP version 3.01, except
# libmbfl is licensed under LGPLv2
# onigurama is licensed under BSD
# ucgendat is licensed under OpenLDAP
License: PHP and LGPLv2 and BSD and OpenLDAP
Requires: %{name}-common = %{version}-%{release}

%description mbstring
The php-mbstring package contains a dynamic shared object that will add
support for multi-byte string handling to PHP.

%package gd
Summary: A module for PHP applications for using the gd graphics library
Group: Development/Languages
# All files licensed under PHP version 3.01
%if %{with_libgd}
License: PHP
%else
# bundled libgd is licensed under BSD
License: PHP and BSD
%endif
Requires: %{name}-common = %{version}-%{release}
BuildRequires: t1lib-devel
%if %{with_libgd}
BuildRequires: gd-devel >= 2.1.0
%endif
# Required to build the bundled GD library
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: freetype-devel
BuildRequires: libXpm-devel
%if %{with_vpx}
BuildRequires: libvpx-devel
%endif

%description gd
The php-gd package contains a dynamic shared object that will add
support for using the gd graphics library to PHP.

%package bcmath
Summary: A module for PHP applications for using the bcmath library
Group: Development/Languages
# All files licensed under PHP version 3.01, except
# libbcmath is licensed under LGPLv2+
License: PHP and LGPLv2+
Requires: %{name}-common = %{version}-%{release}

%description bcmath
The php-bcmath package contains a dynamic shared object that will add
support for using the bcmath library to PHP.

%package gmp
Summary: A module for PHP applications for using the GNU MP library
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
BuildRequires: gmp-devel
Requires: %{name}-common = %{version}-%{release}

%description gmp
These functions allow you to work with arbitrary-length integers
using the GNU MP library.

%package dba
Summary: A database abstraction layer module for PHP applications
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
BuildRequires: %{db_devel}, gdbm-devel, tokyocabinet-devel
Requires: %{name}-common = %{version}-%{release}

%description dba
The php-dba package contains a dynamic shared object that will add
support for using the DBA database abstraction layer to PHP.

%package mcrypt
Summary: Standard PHP module provides mcrypt library support
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{name}-common = %{version}-%{release}
BuildRequires: libmcrypt-devel

%description mcrypt
The php-mcrypt package contains a dynamic shared object that will add
support for using the mcrypt library to PHP.

%package tidy
Summary: Standard PHP module provides tidy library support
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{name}-common = %{version}-%{release}
BuildRequires: libtidy-devel

%description tidy
The php-tidy package contains a dynamic shared object that will add
support for using the tidy library to PHP.

%package mssql
Summary: MSSQL database module for PHP
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{name}-pdo = %{version}-%{release}
BuildRequires: freetds-devel
Provides: php-pdo_dblib

%description mssql
The php-mssql package contains a dynamic shared object that will
add MSSQL database support to PHP.  It uses the TDS (Tabular
DataStream) protocol through the freetds library, hence any
database server which supports TDS can be accessed.

%package embedded
Summary: PHP library for embedding in applications
Group: System Environment/Libraries
Requires: %{name}-common = %{version}-%{release}
# doing a real -devel package for just the .so symlink is a bit overkill
Provides: php-embedded-devel = %{version}-%{release}

%description embedded
The php-embedded package contains a library which can be embedded
into applications to provide PHP scripting language support.
 
%package pspell
Summary: A module for PHP applications for using pspell interfaces
Group: System Environment/Libraries
# All files licensed under PHP version 3.01
License: PHP
Requires: %{name}-common = %{version}-%{release}
BuildRequires: aspell-devel >= 0.50.0

%description pspell
The php-pspell package contains a dynamic shared object that will add
support for using the pspell library to PHP.

%package recode
Summary: A module for PHP applications for using the recode library
Group: System Environment/Libraries
# All files licensed under PHP version 3.01
License: PHP
Requires: %{name}-common = %{version}-%{release}
BuildRequires: recode-devel

%description recode
The php-recode package contains a dynamic shared object that will add
support for using the recode library to PHP.

%package intl
Summary: Internationalization extension for PHP applications
Group: System Environment/Libraries
# All files licensed under PHP version 3.01
License: PHP
Requires: %{name}-common = %{version}-%{release}
%if 0%{?rhel} >= 6
BuildRequires: libicu-devel >= 4.0
%else
BuildRequires: libicu4-devel >= 4.0
%endif

%description intl
The php-intl package contains a dynamic shared object that will add
support for using the ICU library to PHP.

%package enchant
Summary: Enchant spelling extension for PHP applications
Group: System Environment/Libraries
# All files licensed under PHP version 3.0
License: PHP
Requires: %{name}-common = %{version}-%{release}
BuildRequires: enchant-devel >= 1.2.4

%description enchant
The php-enchant package contains a dynamic shared object that will add
support for using the enchant library to PHP.

%prep
echo CIBLE = %{name}-%{version}-%{release} libzip=%{with_libzip}

# ensure than current httpd use prefork MPM.
httpd -V  | grep -q 'threaded:.*yes' && exit 1

%setup -q -n php-%{version}

%patch5 -p1 -b .includedir
%patch6 -p1 -b .embed
%patch7 -p1 -b .recode
%patch8 -p1 -b .libdb

%patch21 -p1 -b .odbctimer

%patch40 -p1 -b .dlopen
%if 0%{?rhel} >= 5
%patch42 -p1 -b .systzdata
%endif
%patch43 -p1 -b .headers
%if 0%{?rhel} >= 7
%patch45 -p1 -b .ldap_r
%endif
%patch46 -p1 -b .fixheader
%patch47 -p1 -b .phpinfo
%patch48 -p1 -b .icuconfig

# upstream patches
%patch100 -p1 -b .bug68074

# security patches

%if %{with static}
%patch212 -p1 -b .locaweb
%endif

# Fixes for tests
%if %{with_libpcre}
%if 0%{?rhel} < 6
# Only apply when system libpcre < 8.34
%patch301 -p1 -b .pcre834
%endif
%endif
%patch302 -p0 -b .971416

# Prevent %%doc confusion over LICENSE files
cp Zend/LICENSE Zend/ZEND_LICENSE
cp TSRM/LICENSE TSRM_LICENSE
cp ext/ereg/regex/COPYRIGHT regex_COPYRIGHT
%if ! %{with_libgd}
cp ext/gd/libgd/README libgd_README
cp ext/gd/libgd/COPYING libgd_COPYING
%endif
cp sapi/fpm/LICENSE fpm_LICENSE
cp ext/mbstring/libmbfl/LICENSE libmbfl_LICENSE
cp ext/mbstring/oniguruma/COPYING oniguruma_COPYING
cp ext/mbstring/ucgendat/OPENLDAP_LICENSE ucgendat_LICENSE
cp ext/fileinfo/libmagic/LICENSE libmagic_LICENSE
cp ext/phar/LICENSE phar_LICENSE
cp ext/bcmath/libbcmath/COPYING.LIB libbcmath_COPYING

# Multiple builds for multiple SAPIs
mkdir build-cgi build-apache build-embedded \
%if %{with_zts}
    build-zts build-ztscli \
%endif
    build-fpm

# ----- Manage known as failed test -------
# affected by systzdata patch
rm ext/date/tests/timezone_location_get.phpt
# fails sometime
rm ext/sockets/tests/mcast_ipv?_recv.phpt
# cause stack exhausion
rm Zend/tests/bug54268.phpt

# Safety check for API version change.
pver=$(sed -n '/#define PHP_VERSION /{s/.* "//;s/".*$//;p}' main/php_version.h)
if test "x${pver}" != "x%{version}"; then
   : Error: Upstream PHP version is now ${pver}, expecting %{version}.
   : Update the version/rcver macros and rebuild.
   exit 1
fi

vapi=`sed -n '/#define PHP_API_VERSION/{s/.* //;p}' main/php.h`
if test "x${vapi}" != "x%{apiver}"; then
   : Error: Upstream API version is now ${vapi}, expecting %{apiver}.
   : Update the apiver macro and rebuild.
   exit 1
fi

vzend=`sed -n '/#define ZEND_MODULE_API_NO/{s/^[^0-9]*//;p;}' Zend/zend_modules.h`
if test "x${vzend}" != "x%{zendver}"; then
   : Error: Upstream Zend ABI version is now ${vzend}, expecting %{zendver}.
   : Update the zendver macro and rebuild.
   exit 1
fi

# Safety check for PDO ABI version change
vpdo=`sed -n '/#define PDO_DRIVER_API/{s/.*[ 	]//;p}' ext/pdo/php_pdo_driver.h`
if test "x${vpdo}" != "x%{pdover}"; then
   : Error: Upstream PDO ABI version is now ${vpdo}, expecting %{pdover}.
   : Update the pdover macro and rebuild.
   exit 1
fi

ver=$(sed -n '/#define PHP_ZENDOPCACHE_VERSION /{s/.* "//;s/".*$//;p}' ext/opcache/ZendAccelerator.h)
if test "$ver" != "%{opcachever}"; then
   : Error: Upstream OPCACHE version is now ${ver}, expecting %{opcachever}.
   : Update the opcachever macro and rebuild.
   exit 1
fi

# https://bugs.php.net/63362 - Not needed but installed headers.
# Drop some Windows specific headers to avoid installation,
# before build to ensure they are really not needed.
rm -f TSRM/tsrm_win32.h \
      TSRM/tsrm_config.w32.h \
      Zend/zend_config.w32.h \
      ext/mysqlnd/config-win.h \
      ext/standard/winver.h \
      main/win32_internal_function_disabled.h \
      main/win95nt.h

# Fix some bogus permissions
find . -name \*.[ch] -exec chmod 644 {} \;
chmod 644 README.*

# php-fpm configuration files for tmpfiles.d
# TODO echo "d /run/php-fpm 755 root root" >php-fpm.tmpfiles

# Some extensions have their own configuration file
cp %{SOURCE50} 10-opcache.ini

# Regenerated bison files
# to force, rm Zend/zend_{language,ini}_parser.[ch]
if [ ! -f Zend/zend_language_parser.c ]; then
  ./genfiles
fi

%build
%if 0%{?rhel} >= 6
# aclocal workaround - to be improved
cat `aclocal --print-ac-dir`/{libtool,ltoptions,ltsugar,ltversion,lt~obsolete}.m4 >>aclocal.m4
%endif

# Force use of system libtool:
libtoolize --force --copy
%if 0%{?rhel} >= 6
cat `aclocal --print-ac-dir`/{libtool,ltoptions,ltsugar,ltversion,lt~obsolete}.m4 >build/libtool.m4
%else
cat `aclocal --print-ac-dir`/libtool.m4 > build/libtool.m4
%endif

# Regenerate configure scripts (patches change config.m4's)
touch configure.in
./buildconf --force
%if %{with_debug}
LDFLAGS="-fsanitize=address"
export LDFLAGS
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -Wno-pointer-sign -fsanitize=address -ggdb"
%else
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -Wno-pointer-sign"
%endif
export CFLAGS

# Install extension modules in %{_libdir}/php/modules.
EXTENSION_DIR=%{_libdir}/php%{?_suffix}/modules; export EXTENSION_DIR

# Set PEAR_INSTALLDIR to ensure that the hard-coded include_path
# includes the PEAR directory even though pear is packaged
# separately.
PEAR_INSTALLDIR=%{_datadir}/pear%{?_suffix}; export PEAR_INSTALLDIR

# Shell function to configure and build a PHP tree.
build() {
# Old/recent bison version seems to produce a broken parser;
# upstream uses GNU Bison 2.3. Workaround:
# Only provided in official tarball (not in snapshot)
if [ -f ../Zend/zend_language_parser.c ]; then
mkdir Zend && cp ../Zend/zend_{language,ini}_{parser,scanner}.[ch] Zend
fi

# Always static:
# date, ereg, filter, libxml, reflection, spl: not supported
# hash: for PHAR_SIG_SHA256 and PHAR_SIG_SHA512
# session: dep on hash, used by soap and wddx
# pcre: used by filter, zip
# pcntl, readline: only used by CLI sapi
# openssl: for PHAR_SIG_OPENSSL
# zlib: used by image

ln -sf ../configure
%configure \
    --cache-file=../config.cache \
    --with-libdir=%{_lib} \
    --libdir=%{_libdir}/php%{?_suffix} \
    --includedir=%{_includedir}/php%{?_suffix} \
    --datadir=%{_datadir}/php%{?_suffix} \
    --with-config-file-path=%{_sysconfdir}/php%{?_suffix}.d \
    --with-config-file-scan-dir=%{_sysconfdir}/php%{?_suffix}.d \
    --disable-debug \
    --with-pic \
    --disable-rpath \
    --without-pear \
    --with-exec-dir=%{_bindir} \
    --with-freetype-dir=%{_prefix} \
    --with-png-dir=%{_prefix} \
    --with-xpm-dir=%{_prefix} \
%if %{with_vpx}
    --with-vpx-dir=%{_prefix} \
%endif
    --enable-gd-native-ttf \
    --with-t1lib=%{_prefix} \
    --without-gdbm \
    --with-jpeg-dir=%{_prefix} \
    --with-openssl \
    --with-system-ciphers \
%if %{with_libpcre}
    --with-pcre-regex=%{_prefix} \
%endif
    --with-zlib \
    --with-layout=GNU \
    --with-kerberos \
    --with-libxml-dir=%{_prefix} \
%if 0%{?rhel} >= 5
    --with-system-tzdata \
%endif
    --with-mhash \
%if %{with_dtrace}
    --enable-dtrace \
%endif
%if %{with_debug}
    --enable-debug \
%endif
    $*
if test $? != 0; then
  tail -500 config.log
  : configure failed
  exit 1
fi

make %{?_smp_mflags}
}

# Build /usr/bin/php-cgi with the CGI SAPI, and most shared extensions
pushd build-cgi

build --libdir=%{_libdir}/php%{?_suffix} \
      --includedir=%{_includedir}/php%{?_suffix} \
      --datadir=%{_datadir}/php%{?_suffix} \
      --enable-pcntl \
      --enable-opcache \
      --enable-phpdbg \
      --with-imap=shared --with-imap-ssl \
      --enable-mbstring=shared \
      --enable-mbregex \
%if %{with_libgd}
      --with-gd=shared,%{_prefix} \
%else
      --with-gd=shared \
%endif
      --with-gmp=shared \
      --enable-calendar=shared \
      --enable-bcmath=shared \
      --with-bz2=shared \
      --enable-ctype=shared \
      --enable-dba=shared --with-db4=%{_prefix} \
                          --with-gdbm=%{_prefix} \
                          --with-tcadb=%{_prefix} \
      --enable-exif=shared \
      --enable-ftp=shared \
      --with-gettext=shared \
      --with-iconv=shared \
      --enable-sockets=shared \
      --enable-tokenizer=shared \
      --with-xmlrpc=shared \
      --with-ldap=shared --with-ldap-sasl \
      --enable-mysqlnd=shared \
      --with-mysql=shared,mysqlnd \
      --with-mysqli=shared,mysqlnd \
      --with-mysql-sock=%{mysql_sock} \
      --with-interbase=shared,%{_libdir}/firebird \
      --with-pdo-firebird=shared,%{_libdir}/firebird \
      --enable-dom=shared \
      --with-pgsql=shared \
      --enable-simplexml=shared \
      --enable-xml=shared \
      --enable-wddx=shared \
      --with-snmp=shared,%{_prefix} \
      --enable-soap=shared \
      --with-xsl=shared,%{_prefix} \
      --enable-xmlreader=shared --enable-xmlwriter=shared \
      --with-curl=shared,%{_prefix} \
      --enable-pdo=shared \
      --with-pdo-odbc=shared,unixODBC,%{_prefix} \
      --with-pdo-mysql=shared,mysqlnd \
      --with-pdo-pgsql=shared,%{_prefix} \
      --with-pdo-sqlite=shared,%{_prefix} \
%if 0%{?rhel} >= 6
      --with-sqlite3=shared,%{_prefix} \
%else
      --without-sqlite3 \
%endif
%if %{with_zip}
      --enable-zip=shared \
%endif
%if %{with_libzip}
      --with-libzip \
%endif
      --without-readline \
      --with-libedit \
      --with-pspell=shared \
      --enable-phar=shared \
      --with-mcrypt=shared,%{_prefix} \
      --with-tidy=shared,%{_prefix} \
      --with-mssql=shared,%{_prefix} \
      --with-pdo-dblib=shared,%{_prefix} \
      --enable-sysvmsg=shared --enable-sysvshm=shared --enable-sysvsem=shared \
      --enable-shmop=shared \
      --enable-posix=shared \
      --with-unixODBC=shared,%{_prefix} \
      --enable-fileinfo=shared \
      --enable-intl=shared \
%if 0%{?rhel} >= 6
      --with-icu-dir=%{_prefix} \
%else
      --with-icu-config=%{_bindir}/icu4-config \
%endif
      --with-enchant=shared,%{_prefix} \
      --with-recode=shared,%{_prefix}
popd

without_shared="--without-gd \
      --disable-dom --disable-dba --without-unixODBC \
      --disable-opcache \
      --disable-xmlreader --disable-xmlwriter \
      --without-sqlite3 --disable-phar --disable-fileinfo \
      --without-pspell --disable-wddx \
      --without-curl --disable-posix --disable-xml \
      --disable-simplexml --disable-exif --without-gettext \
      --without-iconv --disable-ftp --without-bz2 --disable-ctype \
      --disable-shmop --disable-sockets --disable-tokenizer \
      --disable-sysvmsg --disable-sysvshm --disable-sysvsem"

# Build Apache module, and the CLI SAPI, /usr/bin/php
pushd build-apache
build --with-apxs2=%{_httpd_apxs} \
      --libdir=%{_libdir}/php%{?_suffix} \
      --datadir=%{_datadir}/php%{?_suffix} \
      --includedir=%{_includedir}/php%{?_suffix} \
      --enable-pdo=shared \
%if %{with_lsws}
      --with-litespeed \
%endif
%if %{with_libmysql}
      --with-mysql=shared,%{_prefix} \
      --with-mysqli=shared,%{mysql_config} \
      --with-pdo-mysql=shared,%{mysql_config} \
      --without-pdo-sqlite \
%else
      --without-mysql \
      --disable-pdo \
%endif
      ${without_shared}
popd

# Build php-fpm
pushd build-fpm
build --enable-fpm \
%if %{with_systemdfull}
      --with-fpm-systemd \
%endif
      --libdir=%{_libdir}/php%{?_suffix} \
      --datadir=%{_datadir} \
      --without-mysql \
      --disable-pdo \
      ${without_shared}
popd

# Build for inclusion as embedded script language into applications,
# /usr/lib[64]/libphp5.so
pushd build-embedded
build --enable-embed \
      --libdir=%{_libdir} \
      --without-mysql --disable-pdo \
      ${without_shared}
popd

%if %{with_zts}
# Build a special thread-safe (mainly for modules)
pushd build-ztscli

EXTENSION_DIR=%{_libdir}/php%{?_suffix}-zts/modules
build --includedir=%{_includedir}/php%{?_suffix}-zts \
      --libdir=%{_libdir}/php%{?_suffix}-zts \
      --datadir=%{_datadir}/php%{?_suffix}-zts \
      --enable-maintainer-zts \
      --program-prefix=zts- \
      --disable-cgi \
      --with-config-file-scan-dir=%{_sysconfdir}/php%{?_suffix}-zts.d \
      --enable-pcntl \
      --enable-opcache \
      --with-imap=shared --with-imap-ssl \
      --enable-mbstring=shared \
      --enable-mbregex \
%if %{with_libgd}
      --with-gd=shared,%{_prefix} \
%else
      --with-gd=shared \
%endif
      --with-gmp=shared \
      --enable-calendar=shared \
      --enable-bcmath=shared \
      --with-bz2=shared \
      --enable-ctype=shared \
      --enable-dba=shared --with-db4=%{_prefix} \
                          --with-gdbm=%{_prefix} \
                          --with-tcadb=%{_prefix} \
      --with-gettext=shared \
      --with-iconv=shared \
      --enable-sockets=shared \
      --enable-tokenizer=shared \
      --enable-exif=shared \
      --enable-ftp=shared \
      --with-xmlrpc=shared \
      --with-ldap=shared --with-ldap-sasl \
      --enable-mysqlnd=shared \
      --with-mysql=shared,mysqlnd \
      --with-mysqli=shared,mysqlnd \
      --with-mysql-sock=%{mysql_sock} \
      --enable-mysqlnd-threading \
      --with-interbase=shared,%{_libdir}/firebird \
      --with-pdo-firebird=shared,%{_libdir}/firebird \
      --enable-dom=shared \
      --with-pgsql=shared \
      --enable-simplexml=shared \
      --enable-xml=shared \
      --enable-wddx=shared \
      --with-snmp=shared,%{_prefix} \
      --enable-soap=shared \
      --with-xsl=shared,%{_prefix} \
      --enable-xmlreader=shared --enable-xmlwriter=shared \
      --with-curl=shared,%{_prefix} \
      --enable-pdo=shared \
      --with-pdo-odbc=shared,unixODBC,%{_prefix} \
      --with-pdo-mysql=shared,mysqlnd \
      --with-pdo-pgsql=shared,%{_prefix} \
      --with-pdo-sqlite=shared,%{_prefix} \
      --with-pdo-dblib=shared,%{_prefix} \
%if 0%{?rhel} >= 6
      --with-sqlite3=shared,%{_prefix} \
%else
      --without-sqlite3 \
%endif
%if %{with_zip}
      --enable-zip=shared \
%if %{with_libzip}
      --with-libzip \
%endif
%endif
      --without-readline \
      --with-libedit \
      --with-pspell=shared \
      --enable-phar=shared \
      --with-mcrypt=shared,%{_prefix} \
      --with-tidy=shared,%{_prefix} \
      --with-mssql=shared,%{_prefix} \
      --enable-sysvmsg=shared --enable-sysvshm=shared --enable-sysvsem=shared \
      --enable-shmop=shared \
      --enable-posix=shared \
      --with-unixODBC=shared,%{_prefix} \
      --enable-fileinfo=shared \
      --enable-intl=shared \
%if 0%{?rhel} >= 6
      --with-icu-dir=%{_prefix} \
%else
      --with-icu-config=%{_bindir}/icu4-config \
%endif
      --with-enchant=shared,%{_prefix} \
      --with-recode=shared,%{_prefix}
popd

# Build a special thread-safe Apache SAPI
pushd build-zts
build --with-apxs2=%{_httpd_apxs} \
      --includedir=%{_includedir}/php%{?_suffix}-zts \
      --libdir=%{_libdir}/php%{?_suffix}-zts \
      --datadir=%{_datadir}/php%{?_suffix}-zts \
      --enable-maintainer-zts \
      --with-config-file-scan-dir=%{_sysconfdir}/php%{?_suffix}-zts.d \
      --enable-pdo=shared \
%if %{with_libmysql}
      --with-mysql=shared,%{_prefix} \
      --with-mysqli=shared,%{mysql_config} \
      --with-pdo-mysql=shared,%{mysql_config} \
      --without-pdo-sqlite \
%else
      --without-mysql \
      --disable-pdo \
%endif
      ${without_shared}
popd

### NOTE!!! EXTENSION_DIR was changed for the -zts build, so it must remain
### the last SAPI to be built.
%endif

%check
%if %runselftest
cd build-apache

# Run tests, using the CLI SAPI
export NO_INTERACTION=1 REPORT_EXIT_STATUS=1 MALLOC_CHECK_=2
export SKIP_ONLINE_TESTS=1
unset TZ LANG LC_ALL
if ! make test; then
  set +x
  for f in $(find .. -name \*.diff -type f -print); do
    if ! grep -q XFAIL "${f/.diff/.phpt}"
    then
      echo "TEST FAILURE: $f --"
      cat "$f"
      echo -e "\n-- $f result ends."
    fi
  done
  set -x
  #exit 1
fi
unset NO_INTERACTION REPORT_EXIT_STATUS MALLOC_CHECK_
%endif

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%if %{with_zts}
# Install the extensions for the ZTS version
make -C build-ztscli install \
     INSTALL_ROOT=$RPM_BUILD_ROOT

# rename extensions build with mysqlnd
mv $RPM_BUILD_ROOT%{_libdir}/php%{?_suffix}-zts/modules/mysql.so \
   $RPM_BUILD_ROOT%{_libdir}/php%{?_suffix}-zts/modules/mysqlnd_mysql.so
mv $RPM_BUILD_ROOT%{_libdir}/php%{?_suffix}-zts/modules/mysqli.so \
   $RPM_BUILD_ROOT%{_libdir}/php%{?_suffix}-zts/modules/mysqlnd_mysqli.so
mv $RPM_BUILD_ROOT%{_libdir}/php%{?_suffix}-zts/modules/pdo_mysql.so \
   $RPM_BUILD_ROOT%{_libdir}/php%{?_suffix}-zts/modules/pdo_mysqlnd.so

%if %{with_libmysql}
# Install the extensions for the ZTS version modules for libmysql
make -C build-zts install-modules \
     INSTALL_ROOT=$RPM_BUILD_ROOT
%endif

%endif

# Install the version for embedded script language in applications + php_embed.h
make -C build-embedded install-sapi install-headers \
     INSTALL_ROOT=$RPM_BUILD_ROOT

# rename files to locaweb standard
mv $RPM_BUILD_ROOT%{_libdir}/libphp5-%{embed_version}.so \
     $RPM_BUILD_ROOT%{_libdir}/libphp%{?_suffix}-%{embed_version}.so
rm -f $RPM_BUILD_ROOT%{_libdir}/libphp5.so
(cd $RPM_BUILD_ROOT%{_libdir}; ln -sfn libphp%{?_suffix}-%{embed_version}.so libphp%{?_suffix}.so)

# Install the php-fpm binary
make -C build-fpm install-fpm \
     INSTALL_ROOT=$RPM_BUILD_ROOT

# Install everything from the CGI SAPI build
make -C build-cgi install \
     INSTALL_ROOT=$RPM_BUILD_ROOT

# rename extensions build with mysqlnd
mv $RPM_BUILD_ROOT%{_libdir}/php%{?_suffix}/modules/mysql.so \
   $RPM_BUILD_ROOT%{_libdir}/php%{?_suffix}/modules/mysqlnd_mysql.so
mv $RPM_BUILD_ROOT%{_libdir}/php%{?_suffix}/modules/mysqli.so \
   $RPM_BUILD_ROOT%{_libdir}/php%{?_suffix}/modules/mysqlnd_mysqli.so
mv $RPM_BUILD_ROOT%{_libdir}/php%{?_suffix}/modules/pdo_mysql.so \
   $RPM_BUILD_ROOT%{_libdir}/php%{?_suffix}/modules/pdo_mysqlnd.so

%if %{with_libmysql}
# Install the mysql extension build with libmysql
make -C build-apache install-modules \
     INSTALL_ROOT=$RPM_BUILD_ROOT
%endif

# Install the default configuration file and icons
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/php%{?_suffix}.d
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/php%{?_suffix}.d/php.ini
%if %{without static}
sed -i "s/php56/php/g" $RPM_BUILD_ROOT%{_sysconfdir}/php%{?_suffix}.d/php.ini
%endif
install -m 755 -d $RPM_BUILD_ROOT%{_httpd_contentdir}/icons
install -m 644 php.gif $RPM_BUILD_ROOT%{_httpd_contentdir}/icons/php%{?_suffix}.gif

# For third-party packaging:
install -m 755 -d $RPM_BUILD_ROOT%{_datadir}/php%{?_suffix}

# install the DSO
install -m 755 -d $RPM_BUILD_ROOT%{_httpd_moddir}
install -m 755 build-apache/libs/libphp5.so $RPM_BUILD_ROOT%{_httpd_moddir}/libphp%{?_suffix}.so

%if %{with_zts}
# install the ZTS DSO
install -m 755 build-zts/libs/libphp5.so $RPM_BUILD_ROOT%{_httpd_moddir}/libphp%{?_suffix}-zts.so
%endif

# Apache config fragment
%if "%{_httpd_modconfdir}" == "%{_httpd_confdir}"
# Single config file with httpd < 2.4 (RHEL <= 6)
install -D -m 644 %{SOURCE9} $RPM_BUILD_ROOT%{_httpd_confdir}/php%{?_suffix}.conf
%if %{with_zts}
cat %{SOURCE10} >>$RPM_BUILD_ROOT%{_httpd_confdir}/php%{?_suffix}.conf
%endif
cat %{SOURCE1} >>$RPM_BUILD_ROOT%{_httpd_confdir}/php%{?_suffix}.conf
%if %{without static}
sed -i -e 's/php56_module/php5_module/g' -e 's/libphp56/libphp5/g' \
    -e 's/php56/php/g' $RPM_BUILD_ROOT%{_httpd_confdir}/php%{?_suffix}.conf
%endif
%else
# Dual config file with httpd >= 2.4 (RHEL >= 7)
install -D -m 644 %{SOURCE9} $RPM_BUILD_ROOT%{_httpd_modconfdir}/10-php%{?_suffix}.conf
install -D -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_httpd_confdir}/php%{?_suffix}.conf
%if %{with_zts}
cat %{SOURCE10} >>$RPM_BUILD_ROOT%{_httpd_modconfdir}/10-php%{?_suffix}.conf
%endif
install -D -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_httpd_confdir}/php%{?_suffix}.conf
%if %{without static}
sed -i -e "s/php56_module/php5_module/g" -e "s/libphp56/libphp5/g" \
    "s/php56/php/g" $RPM_BUILD_ROOT%{_httpd_modconfdir}/10-php%{?_suffix}.conf \
    $RPM_BUILD_ROOT%{_httpd_confdir}/php%{?_suffix}.conf
%endif
%endif

install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/php%{?_suffix}.d
%if %{with_zts}
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/php%{?_suffix}-zts.d
%endif
install -m 755 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php%{?_suffix}
install -m 700 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php%{?_suffix}/session
install -m 700 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php%{?_suffix}/wsdlcache

%if %{with_lsws}
install -m 755 build-apache/sapi/litespeed/php $RPM_BUILD_ROOT%{_bindir}/lsphp%{?_suffix}
%endif

# PHP-FPM stuff
# Log
install -m 755 -d $RPM_BUILD_ROOT%{_localstatedir}/log/php%{?_suffix}-fpm
# Config
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/php%{?_suffix}-fpm.d
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/php%{?_suffix}-fpm.conf
install -m 644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/php%{?_suffix}-fpm.d/www.conf
mv $RPM_BUILD_ROOT%{_sysconfdir}/php%{?_suffix}-fpm.conf.default .
# LogRotate
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/php%{?_suffix}-fpm
# Environment file
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -m 644 %{SOURCE8} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/php%{?_suffix}-fpm
%if %{without static}
sed -i "s/php56/php/g" $RPM_BUILD_ROOT%{_sysconfdir}/php%{?_suffix}-fpm.conf \
    $RPM_BUILD_ROOT%{_sysconfdir}/php%{?_suffix}-fpm.d/www.conf \
    $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/php%{?_suffix}-fpm \
    $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/php%{?_suffix}-fpm
%endif
%if %{with_systemd}
install -m 755 -d $RPM_BUILD_ROOT/run/php%{?_suffix}-fpm
# tmpfiles.d
install -m 755 -d $RPM_BUILD_ROOT%{_prefix}/lib/tmpfiles.d
install -m 644 php-fpm.tmpfiles $RPM_BUILD_ROOT%{_prefix}/lib/tmpfiles.d/php%{?_suffix}-fpm.conf
# install systemd unit files and scripts for handling server startup
%if %{with_systemdmax}
# this folder requires systemd >= 204
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system/php%{?_suffix}-fpm.service.d
%endif
install -m 755 -d $RPM_BUILD_ROOT%{_unitdir}
install -m 644 %{SOURCE6} $RPM_BUILD_ROOT%{_unitdir}/
%if ! %{with_systemdfull}
# PrivateTmp and Notif mode only work on fedora >= 16
sed -e '/^PrivateTmp/s/true/false/' \
    -e '/^Type/s/notify/simple/' \
    -i ${RPM_BUILD_ROOT}%{_unitdir}/php%{?_suffix}-fpm.service
%endif
%if %{without static}
sed -i "s/php56/php/g" ${RPM_BUILD_ROOT}%{_unitdir}/php%{?_suffix}-fpm.service
%endif
%else
sed  -ne '1,2p' -i $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/php%{?_suffix}-fpm
install -m 755 -d $RPM_BUILD_ROOT%{_localstatedir}/run/php%{?_suffix}-fpm
sed -i -e 's:/run:/var/run:' $RPM_BUILD_ROOT%{_sysconfdir}/php%{?_suffix}-fpm.conf
sed -i -e 's:/run:/var/run:' $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/php%{?_suffix}-fpm
# Service
install -m 755 -d $RPM_BUILD_ROOT%{_initrddir}
install -m 755 %{SOURCE99} $RPM_BUILD_ROOT%{_initrddir}/php%{?_suffix}-fpm
%if %{without static}
sed -i "s/php56/php/g" $RPM_BUILD_ROOT%{_initrddir}/php%{?_suffix}-fpm
%endif
%endif

# Fix the link
(cd $RPM_BUILD_ROOT%{_bindir}; ln -sfn phar%{?_suffix}.phar phar%{?_suffix})

# Generate files lists and stub .ini files for each subpackage
for mod in pgsql odbc ldap snmp xmlrpc imap \
    mysqlnd mysqlnd_mysql mysqlnd_mysqli pdo_mysqlnd \
%if %{with_libmysql}
    mysql mysqli pdo_mysql \
%endif
    mbstring gd dom xsl soap bcmath dba xmlreader xmlwriter \
    simplexml bz2 calendar ctype exif ftp gettext gmp iconv \
    sockets tokenizer opcache \
    pdo pdo_pgsql pdo_odbc pdo_sqlite \
%if %{with_zip}
    zip \
%endif
    interbase pdo_firebird \
%if 0%{?rhel} >= 6
    sqlite3 \
%endif
    enchant phar fileinfo intl \
    mcrypt tidy pdo_dblib mssql pspell curl wddx \
    posix shmop sysvshm sysvsem sysvmsg recode xml \
    ; do
    case $mod in
      opcache)
        # Zend extensions
        ini=10-${mod}.ini;;
      pdo_*|mysql|mysqli|wddx|xmlreader|xmlrpc)
        # Extensions with dependencies on 20-*
        ini=30-${mod}.ini;;
      *)
        # Extensions with no dependency
        ini=20-${mod}.ini;;
    esac
    # some extensions have their own config file
    if [ -f ${ini} ]; then
      cp -p ${ini} $RPM_BUILD_ROOT%{_sysconfdir}/php%{?_suffix}.d/${ini}
%if %{with_zts}
      cp -p ${ini} $RPM_BUILD_ROOT%{_sysconfdir}/php%{?_suffix}-zts.d/${ini}
%endif
    else
      cat > $RPM_BUILD_ROOT%{_sysconfdir}/php%{?_suffix}.d/${ini} <<EOF
; Enable ${mod} extension module
extension=${mod}.so
EOF
%if %{with_zts}
      cat > $RPM_BUILD_ROOT%{_sysconfdir}/php%{?_suffix}-zts.d/${ini} <<EOF
; Enable ${mod} extension module
extension=${mod}.so
EOF
%endif
    fi
    cat > files.${mod} <<EOF
%attr(755,root,root) %{_libdir}/php%{?_suffix}/modules/${mod}.so
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/php%{?_suffix}.d/${ini}
%if %{with_zts}
%attr(755,root,root) %{_libdir}/php%{?_suffix}-zts/modules/${mod}.so
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/php%{?_suffix}-zts.d/${ini}
%endif
EOF
done

# The dom, xsl and xml* modules are all packaged in php-xml
cat files.dom files.xsl files.xml{reader,writer} files.wddx \
    files.simplexml >> files.xml

# The mysql and mysqli modules are both packaged in php-mysql
%if %{with_libmysql}
cat files.mysqli >> files.mysql
cat files.pdo_mysql >> files.mysql
%endif
# mysqlnd
cat files.mysqlnd_mysql \
    files.mysqlnd_mysqli \
    files.pdo_mysqlnd \
    >> files.mysqlnd

# Split out the PDO modules
cat files.pdo_dblib >> files.mssql
cat files.pdo_pgsql >> files.pgsql
cat files.pdo_odbc >> files.odbc
cat files.pdo_firebird >> files.interbase

# sysv* and posix in packaged in php-process
cat files.shmop files.sysv* files.posix > files.process

# Package sqlite3 and pdo_sqlite with pdo; isolating the sqlite dependency
# isn't useful at this time since rpm itself requires sqlite.
cat files.pdo_sqlite >> files.pdo
%if 0%{?rhel} >= 6
cat files.sqlite3 >> files.pdo
%endif

# Package zip, curl, phar and fileinfo in -common.
cat files.curl files.phar files.fileinfo \
    files.exif files.gettext files.iconv files.calendar \
    files.ftp files.bz2 files.ctype files.sockets \
    files.tokenizer > files.common
%if %{with_zip}
cat files.zip >> files.common
%endif

# The default Zend OPcache blacklist file
install -m 644 %{SOURCE51} $RPM_BUILD_ROOT%{_sysconfdir}/php%{?_suffix}.d/opcache-default.blacklist
%if %{with_zts}
install -m 644 %{SOURCE51} $RPM_BUILD_ROOT%{_sysconfdir}/php%{?_suffix}-zts.d/opcache-default.blacklist
sed -e '/blacklist_filename/s/php%{?_suffix}.d/php%{?_suffix}-zts.d/' \
    -i $RPM_BUILD_ROOT%{_sysconfdir}/php%{?_suffix}-zts.d/10-opcache.ini
%endif

%if %{without static}
sed -i "s/php56/php/g" $RPM_BUILD_ROOT%{_sysconfdir}/php%{?_suffix}.d/10-opcache.ini \
    $RPM_BUILD_ROOT%{_sysconfdir}/php%{?_suffix}-zts.d/10-opcache.ini
%endif

# Install the macros file:
sed -e "s/@PHP_APIVER@/%{apiver}/" \
    -e "s/@PHP_ZENDVER@/%{zendver}/" \
    -e "s/@PHP_PDOVER@/%{pdover}/" \
    -e "s/@PHP_VERSION@/%{version}/" \
%if ! %{with_zts}
    -e "/zts/d" \
%endif
    < %{SOURCE3} > macros%{?_suffix}.php
install -m 644 -D macros%{?_suffix}.php \
           $RPM_BUILD_ROOT%{macrosdir}/macros%{?_suffix}.php

%if %{without static}
sed -i "s/php56/php/g" $RPM_BUILD_ROOT%{macrosdir}/macros%{?_suffix}.php
%endif

# Remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{_libdir}/php%{?_suffix}/modules/*.a \
%if %{with_zts}
       $RPM_BUILD_ROOT%{_libdir}/php%{?_suffix}-zts/modules/*.a \
%endif
       $RPM_BUILD_ROOT%{_bindir}/{phptar} \
       $RPM_BUILD_ROOT%{_datadir}/pear \
       $RPM_BUILD_ROOT%{_libdir}/libphp5.la

%if %{with static}
# PHP 5.4/5.5 compatibility mode (Locaweb Shared Hosting)
mv $RPM_BUILD_ROOT%{_bindir}/php $RPM_BUILD_ROOT%{_bindir}/php%{?_suffix}
mv $RPM_BUILD_ROOT%{_bindir}/php-cgi $RPM_BUILD_ROOT%{_bindir}/php%{?_suffix}-cgi
mv $RPM_BUILD_ROOT%{_bindir}/php-config $RPM_BUILD_ROOT%{_bindir}/php%{?_suffix}-config
mv $RPM_BUILD_ROOT%{_bindir}/phpize $RPM_BUILD_ROOT%{_bindir}/phpize%{?_suffix}
mv $RPM_BUILD_ROOT%{_mandir}/man1/php.1 $RPM_BUILD_ROOT%{_mandir}/man1/php%{?_suffix}.1
mv $RPM_BUILD_ROOT%{_mandir}/man1/php-config.1 $RPM_BUILD_ROOT%{_mandir}/man1/php%{?_suffix}-config.1
mv $RPM_BUILD_ROOT%{_mandir}/man1/php-cgi.1 $RPM_BUILD_ROOT%{_mandir}/man1/php%{?_suffix}-cgi.1
mv $RPM_BUILD_ROOT%{_mandir}/man1/phpize.1 $RPM_BUILD_ROOT%{_mandir}/man1/phpize%{?_suffix}.1

mv $RPM_BUILD_ROOT%{_bindir}/phar $RPM_BUILD_ROOT%{_bindir}/phar%{?_suffix}
mv $RPM_BUILD_ROOT%{_bindir}/phar.phar $RPM_BUILD_ROOT%{_bindir}/phar%{?_suffix}.phar
mv $RPM_BUILD_ROOT%{_mandir}/man1/phar.1 $RPM_BUILD_ROOT%{_mandir}/man1/phar%{?_suffix}.1
mv $RPM_BUILD_ROOT%{_mandir}/man1/phar.phar.1 $RPM_BUILD_ROOT%{_mandir}/man1/phar%{?_suffix}.phar.1
sed -i 's/phar.1/phar%{?_suffix}.1/g' $RPM_BUILD_ROOT%{_mandir}/man1/phar%{?_suffix}.phar.1

%if %{with_zts}
mv $RPM_BUILD_ROOT%{_bindir}/zts-php $RPM_BUILD_ROOT%{_bindir}/zts-php%{?_suffix}
mv $RPM_BUILD_ROOT%{_bindir}/zts-phpize $RPM_BUILD_ROOT%{_bindir}/zts-phpize%{?_suffix}
mv $RPM_BUILD_ROOT%{_bindir}/zts-php-config $RPM_BUILD_ROOT%{_bindir}/zts-php%{?_suffix}-config
mv $RPM_BUILD_ROOT%{_mandir}/man1/zts-php.1 $RPM_BUILD_ROOT%{_mandir}/man1/zts-php%{?_suffix}.1
mv $RPM_BUILD_ROOT%{_mandir}/man1/zts-phpize.1 $RPM_BUILD_ROOT%{_mandir}/man1/zts-phpize%{?_suffix}.1
mv $RPM_BUILD_ROOT%{_mandir}/man1/zts-php-config.1 $RPM_BUILD_ROOT%{_mandir}/man1/zts-php%{?_suffix}-config.1
%endif

# Fix php binary name and php include dir name
sed -i -e '/^include_dir=/s/\/php\"$/\"/g' \
     -e '/php_cli_binary=/s/}php\${/}php%{?_suffix}\${/g' \
     -e '/php_cgi_binary=/s/}php-cgi\${/}php%{?_suffix}-cgi\${/g' \
     $RPM_BUILD_ROOT%{_bindir}/php%{?_suffix}-config \
%if %{with_zts}
     $RPM_BUILD_ROOT%{_bindir}/zts-php%{?_suffix}-config
%endif
%endif

# Remove irrelevant docs
rm -f README.{Zeus,QNX,CVS-RULES}

%pre fpm
# Add the "%{_httpd_user}" user as we don't require httpd
getent group %{_httpd_user} >/dev/null || \
  groupadd -g 48 -r %{_httpd_user}
getent passwd %{_httpd_user} >/dev/null || \
  useradd -r -u 48 -g %{_httpd_user} -s /sbin/nologin \
    -d %{_httpd_contentdir} -c "Apache" %{_httpd_user}
exit 0

%preun
%if %{with static}
if [ -f %{_httpd_confdir}/php%{?_suffix}.conf.des ]; then
	mv %{_httpd_confdir}/php%{?_suffix}.conf.des %{_httpd_confdir}/php%{?_suffix}.conf
fi
%endif

%post fpm
%if 0%{?systemd_post:1}
%systemd_post php%{?_suffix}-fpm.service
%else
if [ $1 = 1 ]; then
    # Initial installation
%if %{with_systemd}
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
%else
    /sbin/chkconfig --add php%{?_suffix}-fpm
%endif
fi
%endif

%preun fpm
%if 0%{?systemd_preun:1}
%systemd_preun php%{?_suffix}-fpm.service
%else
if [ $1 = 0 ]; then
    # Package removal, not upgrade
%if %{with_systemd}
    /bin/systemctl --no-reload disable php%{?_suffix}-fpm.service >/dev/null 2>&1 || :
    /bin/systemctl stop php%{?_suffix}-fpm.service >/dev/null 2>&1 || :
%else
    /sbin/service php%{?_suffix}-fpm stop >/dev/null 2>&1
    /sbin/chkconfig --del php%{?_suffix}-fpm
%endif
fi
%endif

%postun fpm
%if 0%{?systemd_postun_with_restart:1}
%systemd_postun_with_restart php%{?_suffix}-fpm.service
%else
%if %{with_systemd}
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ]; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart php%{?_suffix}-fpm.service >/dev/null 2>&1 || :
fi
%else
if [ $1 -ge 1 ]; then
    /sbin/service php%{?_suffix}-fpm condrestart >/dev/null 2>&1 || :
fi
%endif
%endif

# Handle upgrading from SysV initscript to native systemd unit.
# We can tell if a SysV version of php-fpm was previously installed by
# checking to see if the initscript is present.
%triggerun fpm -- php%{?_suffix}-fpm
%if %{with_systemd}
if [ -f /etc/rc.d/init.d/php%{?_suffix}-fpm ]; then
    # Save the current service runlevel info
    # User must manually run systemd-sysv-convert --apply php-fpm
    # to migrate them to systemd targets
    /usr/bin/systemd-sysv-convert --save php%{?_suffix}-fpm >/dev/null 2>&1 || :

    # Run these because the SysV package being removed won't do them
    /sbin/chkconfig --del php%{?_suffix}-fpm >/dev/null 2>&1 || :
    /bin/systemctl try-restart php%{?_suffix}-fpm.service >/dev/null 2>&1 || :
fi
%endif

%post
%if %{with static}
if [ -f %{_httpd_confdir}/php%{?_suffix}.conf ]; then
	mv %{_httpd_confdir}/php%{?_suffix}.conf %{_httpd_confdir}/php%{?_suffix}.conf.des
fi
%endif

%post embedded -p /sbin/ldconfig
%postun embedded -p /sbin/ldconfig

%{!?_licensedir:%global license %%doc}

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
rm files.* macros*.php
rm -rf %{_builddir}/php-%{version}

%files
%defattr(-,root,root)
%{_httpd_moddir}/libphp%{?_suffix}.so
%if %{with_zts}
%{_httpd_moddir}/libphp%{?_suffix}-zts.so
%endif
%attr(1771,root,root) %dir %{_localstatedir}/lib/php%{?_suffix}/session
%attr(1771,root,root) %dir %{_localstatedir}/lib/php%{?_suffix}/wsdlcache
%config(noreplace) %{_httpd_confdir}/php%{?_suffix}.conf
%if "%{_httpd_modconfdir}" != "%{_httpd_confdir}"
%config(noreplace) %{_httpd_modconfdir}/10-php%{?_suffix}.conf
%endif
%{_httpd_contentdir}/icons/php%{?_suffix}.gif

%files common -f files.common
%defattr(-,root,root)
%doc CODING_STANDARDS CREDITS EXTENSIONS NEWS README*
%license LICENSE Zend/ZEND_* TSRM_LICENSE regex_COPYRIGHT
%license libmagic_LICENSE
%license phar_LICENSE
%doc php.ini-*
%config(noreplace) %{_sysconfdir}/php%{?_suffix}.d/php.ini
%dir %{_sysconfdir}/php%{?_suffix}.d
%dir %{_libdir}/php%{?_suffix}
%dir %{_libdir}/php%{?_suffix}/modules
%if %{with_zts}
%dir %{_sysconfdir}/php%{?_suffix}-zts.d
%dir %{_libdir}/php%{?_suffix}-zts
%dir %{_libdir}/php%{?_suffix}-zts/modules
%endif
%dir %{_localstatedir}/lib/php%{?_suffix}
%dir %{_datadir}/php%{?_suffix}

%files cli
%defattr(-,root,root)
%{_bindir}/php%{?_suffix}
# provides phpize here (not in -devel) for pecl command
%{_bindir}/phpize%{?_suffix}
%if %{with_zts}
%{_bindir}/zts-php%{?_suffix}
%{_bindir}/zts-phpize%{?_suffix}
%{_mandir}/man1/zts-php%{?_suffix}.1*
%{_mandir}/man1/zts-phpize%{?_suffix}.1*
%endif
%{_bindir}/php%{?_suffix}-cgi
%{_bindir}/phar%{?_suffix}.phar
%{_bindir}/phar%{?_suffix}
%{_mandir}/man1/php%{?_suffix}.1*
%{_mandir}/man1/php%{?_suffix}-cgi.1*
%{_mandir}/man1/phar%{?_suffix}.1*
%{_mandir}/man1/phar%{?_suffix}.phar.1*
%{_mandir}/man1/phpize%{?_suffix}.1*
%doc sapi/cgi/README* sapi/cli/README

%files dbg
%defattr(-,root,root)
%{_bindir}/phpdbg
%{_mandir}/man1/phpdbg.1*
%doc sapi/phpdbg/{README.md,CREDITS}

%files fpm
%defattr(-,root,root)
%doc php%{?_suffix}-fpm.conf.default
%license fpm_LICENSE
%attr(1777,root,root) %dir %{_localstatedir}/lib/php%{?_suffix}/session
%attr(1777,root,root) %dir %{_localstatedir}/lib/php%{?_suffix}/wsdlcache
%config(noreplace) %{_sysconfdir}/php%{?_suffix}-fpm.conf
%config(noreplace) %{_sysconfdir}/php%{?_suffix}-fpm.d/www.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/php%{?_suffix}-fpm
%config(noreplace) %{_sysconfdir}/sysconfig/php%{?_suffix}-fpm
%if %{with_systemd}
%{_prefix}/lib/tmpfiles.d/php%{?_suffix}-fpm.conf
%{_unitdir}/php%{?_suffix}-fpm.service
%if %{with_systemdmax}
%dir %{_sysconfdir}/systemd/system/php%{?_suffix}-fpm.service.d
%endif
%dir /run/php%{?_suffix}-fpm
%else
%{_initrddir}/php%{?_suffix}-fpm
%attr(770,webserver,root) %dir %{_localstatedir}/run/php%{?_suffix}-fpm
%endif
%{_sbindir}/php%{?_suffix}-fpm
%dir %{_sysconfdir}/php%{?_suffix}-fpm.d
# log owned by webserver for log
%attr(770,webserver,root) %dir %{_localstatedir}/log/php%{?_suffix}-fpm
%{_mandir}/man8/php%{?_suffix}-fpm.8*
%if %{with static}
%dir %{_datadir}/php%{?_suffix}-fpm
%{_datadir}/php%{?_suffix}-fpm/status.html
%else
%dir %{_datadir}/fpm
%{_datadir}/fpm/status.html
%endif

%if %{with_lsws}
%files litespeed
%defattr(-,root,root)
%{_bindir}/lsphp%{?_suffix}
%endif

%files devel
%defattr(-,root,root)
%{_bindir}/php%{?_suffix}-config
%{_includedir}/php%{?_suffix}
%{_libdir}/php%{?_suffix}/build
%if %{with_zts}
%{_bindir}/zts-php%{?_suffix}-config
%{_includedir}/php%{?_suffix}-zts
%{_libdir}/php%{?_suffix}-zts/build
%{_mandir}/man1/zts-php%{?_suffix}-config.1*
%endif
%{_mandir}/man1/php%{?_suffix}-config.1*
%{macrosdir}/macros%{?_suffix}.php

%files embedded
%defattr(-,root,root,-)
%{_libdir}/libphp%{?_suffix}.so
%{_libdir}/libphp%{?_suffix}-%{embed_version}.so

%files pgsql -f files.pgsql
%if %{with_libmysql}
%files mysql -f files.mysql
%endif
%files odbc -f files.odbc
%files imap -f files.imap
%files ldap -f files.ldap
%files snmp -f files.snmp
%files xml -f files.xml
%files xmlrpc -f files.xmlrpc
%files mbstring -f files.mbstring
%license libmbfl_LICENSE
%license oniguruma_COPYING
%license ucgendat_LICENSE
%files gd -f files.gd
%defattr(-,root,root,-)
%if ! %{with_libgd}
%license libgd_README
%license libgd_COPYING
%endif
%files soap -f files.soap
%files bcmath -f files.bcmath
%license libbcmath_COPYING
%files gmp -f files.gmp
%files dba -f files.dba
%files pdo -f files.pdo
%files mcrypt -f files.mcrypt
%files tidy -f files.tidy
%files mssql -f files.mssql
%files pspell -f files.pspell
%files intl -f files.intl
%files process -f files.process
%files recode -f files.recode
%files interbase -f files.interbase
%files enchant -f files.enchant
%files mysqlnd -f files.mysqlnd
%files opcache -f files.opcache
%config(noreplace) %{_sysconfdir}/php%{?_suffix}.d/opcache-default.blacklist
%config(noreplace) %{_sysconfdir}/php%{?_suffix}-zts.d/opcache-default.blacklist

%changelog
* Thu Oct 24 2014 Claudio Filho <claudio.filho@locaweb.com.br> 5.6.2-1
- Merged with Remi changes:
  Update to PHP 5.6.2
  http://php.net/releases/5_6_2.php

* Mon Oct 13 2014 Claudio Filho <claudio.filho@locaweb.com.br> 5.6.1-1
- Merged with Remi changes:
  Update to PHP 5.6.1
  http://php.net/releases/5_6_1.php
  use default system cipher list by Fedora policy
  http://fedoraproject.org/wiki/Changes/CryptoPolicy

* Thu Sep 11 2014 Claudio Filho <claudio.filho@locaweb.com.br> 5.6.0-2
- Remove oci8 and fedora support
- Enable php_bootstrap
- Fix mysql_config
- Add locaweb and static conditional package builds
- Add with_libmysql
- Remove isasuffix, snapdate and rcver
- Remove with_httpd2410
- Add with_libzip and enable with_zip
- Add _suffix 56 for enable suffix on all files
- Add icuconfig patch
- Add locaweb static patch
- Remove Obsoletes
- Downgrade libicu-devel
- Fix %configure to include --datadir and --includedir
- Fix pear install dir
- Fix %configure to remove --with-exec-dir and --enable-mysqlnd-threading
- Fix permissions of the session directory.
- Fix Mysql BuildRequires to use Percona-Server-devel-51 instead mysql-devel
- Fix intl BuildRequires to use libicu4-devel or libicu-devel
- Fix apache username on %pre fpm
- Add %preun and %post to rename php56.conf
- Add %clean session
- Rebuilt for locaweb

* Wed Sep  3 2014 Remi Collet <remi@fedoraproject.org> 5.6.0-1.2
- ensure gd-last 2.1.0-3, with libvpx support, is used

* Fri Aug 29 2014 Remi Collet <remi@fedoraproject.org> 5.6.0-1.1
- enable libvpx on EL 6 (with libvpx 1.3.0)

* Thu Aug 28 2014 Remi Collet <remi@fedoraproject.org> 5.6.0-1
- PHP 5.6.0 is GA
- fix ZTS man pages, upstream patch for 67878

* Wed Aug 20 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.22.RC4
- backport rawhide stuff for F21+ and httpd-filesystem
  with support for SetHandler to proxy_fcgi

* Thu Aug 14 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.21.RC4
- php 5.6.0RC4

* Wed Jul 30 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.20.RC3
- php 5.6.0RC3
- fix license handling
- fix zts-php-config --php-binary output #1124605
- cleanup with_libmysql
- add php-litespeed subpackage (/usr/bin/lsphp)

* Fri Jul 25 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.18.RC2
- dont display timezone version in phpinfo (tzdata patch v11)

* Sat Jul 19 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.17.RC2
- test build for #67635

* Mon Jul  7 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.16.RC2
- php 5.6.0RC2

* Mon Jun 23 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.15.RC1
- add workaround for unserialize/mock issue from 5.4/5.5

* Mon Jun 23 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.14.RC1
- fix phpdbg with libedit https://bugs.php.net/67499

* Thu Jun 19 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.13.RC1
- php 5.6.0RC1

* Mon Jun 16 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.12.beta4
- test build for serialize

* Tue Jun 10 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.11.beta4
- test build for bug 67410, 67411, 67412, 67413
- fix 67392, dtrace breaks argument unpack

* Thu Jun  5 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.10.beta4
- fix regression introduce in fix for #67118

* Wed Jun  4 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.9.beta4
- php 5.6.0beta4

* Wed May 14 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.8.beta3
- php 5.6.0beta3

* Tue May  6 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.8.201405061030
- new snapshot php5.6-201405061030

* Sat May  3 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.7.beta2
- php 5.6.0beta2

* Thu Apr 10 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.6.beta1
- php 5.6.0beta1

* Wed Apr  9 2014 Remi Collet <rcollet@redhat.com> 5.6.0-0.5.201404090430
- new snapshot php5.6-201404090430
- add numerical prefix to extension configuration files
- prevent .user.ini files from being viewed by Web clients
- load php directives only when mod_php is active

* Wed Mar 26 2014 Remi Collet <remi@fedoraproject.org> 5.6.0-0.4.201403261230
- new snapshot php5.6-201403261230
- oci8 version 2.0.9
- opcache version 7.0.4-dev

* Mon Mar 17 2014 Remi Collet <remi@fedoraproject.org> 5.6.0-0.4.201403170630
- new snapshot php5.6-201403170630

* Wed Mar 12 2014 Remi Collet <remi@fedoraproject.org> 5.6.0-0.3.201403120830
- new snapshot php5.6-201403120830
- rebuild against gd-last without libvpx on EL < 7
- oci8 version 2.0.8

* Fri Feb 28 2014 Remi Collet <remi@fedoraproject.org> 5.6.0-0.2.alpha3
- php 5.6.0alpha3
- add php-dbg subpackage
- update php.ini from upstream production template
- move /usr/bin/zts-php to php-cli subpackage

* Wed Feb 26 2014 Remi Collet <rcollet@redhat.com> 5.5.10-0.4.RC1
- php-fpm should own /var/lib/php/session and wsdlcache

* Tue Feb 25 2014 Remi Collet <rcollet@redhat.com> 5.5.10-0.3.RC1
- test build for https://bugs.php.net/66762

* Fri Feb 21 2014 Remi Collet <rcollet@redhat.com> 5.5.10-0.2.RC1
- another test build of 5.5.10RC1
- fix memleak in fileinfo ext
- revert test changes for pcre 8.34

* Thu Feb 20 2014 Remi Collet <rcollet@redhat.com> 5.5.10-0.1.RC1
- test build of 5.5.10RC1

* Tue Feb 18 2014 Remi Collet <rcollet@redhat.com> 5.5.9-2
- upstream patch for https://bugs.php.net/66731

* Tue Feb 11 2014 Remi Collet <remi@fedoraproject.org> 5.5.9-1
- Update to 5.5.9
  http://www.php.net/ChangeLog-5.php#5.5.9
- Install macros to /usr/lib/rpm/macros.d where available.
- Add configtest option to php-fpm ini script (EL)

* Thu Jan 23 2014 Remi Collet <rcollet@redhat.com> 5.5.9-0.1.RC1
- test build of 5.5.9RC1

* Thu Jan 23 2014 Joe Orton <jorton@redhat.com> - 5.5.8-2
- fix _httpd_mmn expansion in absence of httpd-devel

* Mon Jan 20 2014 Remi Collet <rcollet@redhat.com> 5.5.8-2
- test build for https://bugs.php.net/66412

* Wed Jan  8 2014 Remi Collet <rcollet@redhat.com> 5.5.8-1
- update to 5.5.8
- drop conflicts with other opcode caches as both can
  be used only for user data cache

* Wed Jan  8 2014 Remi Collet <rcollet@redhat.com> 5.5.8-0.2.RC1
- another test build of 5.5.8RC1

* Sat Dec 28 2013 Remi Collet <rcollet@redhat.com> 5.5.8-0.1.RC1
- test build of 5.5.8RC1

* Fri Dec 20 2013 Remi Collet <rcollet@redhat.com> 5.5.7-1.1
- test build for https://bugs.php.net/66331

* Wed Dec 11 2013 Remi Collet <rcollet@redhat.com> 5.5.7-1
- update to 5.5.7, fix for CVE-2013-6420
- fix zend_register_functions breaks reflection, php bug 66218
- fix Heap buffer over-read in DateInterval, php bug 66060
- fix fix overflow handling bug in non-x86

* Tue Dec 10 2013 Remi Collet <rcollet@redhat.com> 5.5.7-0.4.RC1
- test build

* Wed Dec 04 2013 Remi Collet <rcollet@redhat.com> 5.5.7-0.3.RC1
- test build

* Mon Dec 02 2013 Remi Collet <rcollet@redhat.com> 5.5.7-0.2.RC1
- test build for https://bugs.php.net/66218
  zend_register_functions breaks reflection

* Thu Nov 28 2013 Remi Collet <rcollet@redhat.com> 5.5.7-0.1.RC1
- test build of 5.5.7RC1

* Wed Nov 13 2013 Remi Collet <remi@fedoraproject.org> 5.5.6-1
- update to 5.5.6

* Tue Nov 12 2013 Remi Collet <remi@fedoraproject.org> 5.5.6-0.7
- update to 5.5.6, test build

* Fri Nov  8 2013 Remi Collet <remi@fedoraproject.org> 5.5.6-0.6.RC1
- add --with debug option for debug build

* Wed Nov  6 2013 Remi Collet <remi@fedoraproject.org> 5.5.6-0.5.RC1
- test buid with opcache changes reverted

* Mon Nov  4 2013 Remi Collet <remi@fedoraproject.org> 5.5.6-0.4.RC1
- test build opcache with phar build shared
  https://github.com/zendtech/ZendOptimizerPlus/issues/147

* Mon Nov  4 2013 Remi Collet <remi@fedoraproject.org> 5.5.6-0.3.RC1
- build phar shared, opcache loaded with RTLD_LAZY

* Sat Nov  2 2013 Remi Collet <remi@fedoraproject.org> 5.5.6-0.2.RC1
- build phar static for opcache dep.

* Sat Nov  2 2013 Remi Collet <remi@fedoraproject.org> 5.5.6-0.1.RC1
- test build of 5.5.6RC1

* Sun Oct 27 2013 Remi Collet <remi@fedoraproject.org> 5.5.5-2
- rebuild using libicu-last 50.1.2

* Tue Oct 15 2013 Remi Collet <rcollet@redhat.com> - 5.5.5-1
- update to 5.5.5

* Mon Sep 23 2013 Remi Collet <rcollet@redhat.com> - 5.5.4-2
- test build

* Thu Sep 19 2013 Remi Collet <rcollet@redhat.com> - 5.5.4-1
- update to 5.5.4
- improve security, use specific soap.wsdl_cache_dir
  use /var/lib/php/wsdlcache for mod_php and php-fpm
- sync short_tag comments in php.ini with upstream

* Fri Aug 30 2013 Remi Collet <rcollet@redhat.com> - 5.5.4.0.1-201308300430
- test build with -fsanitize=address
- test build for https://bugs.php.net/65564

* Wed Aug 21 2013 Remi Collet <rcollet@redhat.com> - 5.5.3-1
- update to 5.5.3
- build without zip extension, requires php-pecl-zip
- fix typo and add missing entries in php.ini

* Tue Aug 20 2013 Remi Collet <rcollet@redhat.com> - 5.5.3-0
- update to 5.5.3
- test build without zip extension
- fix typo and add missing entries in php.ini

* Mon Aug 19 2013 Remi Collet <rcollet@redhat.com> - 5.5.2-1
- update to 5.5.2

* Thu Aug  8 2013 Remi Collet <remi@fedoraproject.org> - 5.5.2-0.2.RC1
- improve system libzip patch

* Thu Aug  1 2013 Remi Collet <remi@fedoraproject.org> - 5.5.2-0.1.RC1
- 5.5.2RC1

* Fri Jul 26 2013 Remi Collet <remi@fedoraproject.org> - 5.5.1-2
- test build with oracle instantclient 12.1

* Mon Jul 22 2013 Remi Collet <rcollet@redhat.com> - 5.5.1-1
- update to 5.5.1
- add Provides: php(pdo-abi), for consistency with php(api)
  and php(zend-abi)
- improved description for mod_php
- fix opcache ZTS configuration (blacklists in /etc/php-zts.d)
- add missing man pages (phar, php-cgi)
- fix php-enchant summary and description

* Fri Jul 12 2013 Remi Collet <rcollet@redhat.com> - 5.5.0-2
- add security fix for CVE-2013-4113
- add missing ASL 1.0 license
- 32k stack size seems ok for tests on both 32/64bits build

* Mon Jun 24 2013 Remi Collet <rcollet@redhat.com> 5.5.1-0.1.201306240630
- test build (bundled libgd)

* Thu Jun 20 2013 Remi Collet <rcollet@redhat.com> 5.5.0-1
- update to 5.5.0 final

* Fri Jun 14 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.11.RC3
- also drop JSON from sources
- clean conditional for JSON (as removed from the sources)
- clean conditional for FPM (always build)

* Fri Jun 14 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.36.RC3.1
- EL-5 rebuild with gd-last

* Thu Jun 13 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.36.RC3
- drop JSON extension
- build with system GD when 2.1.0 is available

* Thu Jun  6 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.35.RC3
- update to 5.5.0RC3

* Mon May 27 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.34.201305271230.
-test build with systemd gd

* Thu May 23 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.33.RC2
- update to 5.5.0RC2
- add missing options in php-fpm.conf
- improved systemd configuration, documentation about
  /etc/sysconfig/php-fpm being deprecated

* Wed May 22 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.32.201305220430
- test build for https://bugs.php.net/64895

* Sat May 18 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.32.201305181030
- test build with systemd integration (type=notify)

* Wed May  8 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.31.RC1
- update to 5.5.0RC1

* Sat Apr 27 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.30.201305041230
- test build for libgd

* Sat Apr 27 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.29.201304291030
- new snapshot
- review some sub-packages description
- add option to disable json extension

* Thu Apr 25 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.28.beta4
- update to 5.5.0beta4, rebuild with new sources

* Thu Apr 25 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.27.beta4
- update to 5.5.0beta4

* Mon Apr 22 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.27-201304221230
- new snapshot
- try build with system gd 2.1.0

* Thu Apr 18 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.26-201304181030
- new snapshot
- zend_extension doesn't requires full path
- refresh system libzip patch
- drop opcache patch merged upstream

* Thu Apr 11 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.25.beta3
- allow wildcard in opcache.blacklist_filename and provide
  default /etc/php.d/opcache-default.blacklist

* Wed Apr 10 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.24.beta3
- update to 5.5.0beta3

* Thu Apr  4 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.23-201304040630
- new snapshot
- clean old deprecated options

* Thu Mar 28 2013 Remi Collet <rcollet@redhat.com> 5.5.0-0.22.beta2
- update to 5.5.0beta2
- Zend Optimizer+ renamed to Zend OPcache
- sync provided configuration with upstream

* Mon Mar 25 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.21-201303251230
- new snapshot
- generated parser using system bison, test for https://bugs.php.net/64503

* Wed Mar 20 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.20-201303201430
- new snapshot (beta1)

* Mon Mar 18 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.19-201303180830
- new snapshot
- temporary disable dtrace
- new extension opcache in php-opccache sub-package

* Thu Mar 14 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.18-201303141230
- new snapshot
- hardened build (links with -z now option)
- remove %%config from /etc/rpm/macros.php

* Fri Mar  8 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.17-201303081230
- new snapshot (post alpha 6)
- make php-mysql package optional (and disabled)
- make ZTS build optional (still enabled)

* Thu Feb 28 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.16-201302281430
- new snapshot

* Thu Feb 21 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.16-201302211230
- new snapshot (post alpha 5)

* Wed Feb 13 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.16-201302131030
- enable tokyocabinet and gdbm dba handlers

* Tue Feb 12 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.15-201302121230
- new snapshot

* Mon Feb  4 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.14-201302040630
- new snapshot

* Fri Feb  1 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.14-201302010630
- new snapshot

* Mon Jan 28 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.13-201301281030
- new snapshot
- don't display XFAIL tests in report

* Wed Jan 23 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.12-201301230630
- new snapshot, alpha4

* Thu Jan 17 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.11-201301170830
- new snapshot
- fix php.conf to allow MultiViews managed by php scripts

* Thu Jan 10 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.10-201301100830
- new snapshot, alpha3

* Wed Jan  2 2013 Remi Collet <remi@fedoraproject.org> 5.5.0-0.10-201301021430
- new snapshot

* Mon Dec 24 2012 Remi Collet <remi@fedoraproject.org> 5.5.0-0.9.201212241030
- new snapshot (post alpha2)
- use xz compressed tarball

* Tue Dec 18 2012 Remi Collet <remi@fedoraproject.org> 5.5.0-0.9.201212181230
- new snapshot

* Wed Dec 12 2012 Remi Collet <remi@fedoraproject.org> 5.5.0-0.8.201212121430
- new snapshot

* Tue Dec 11 2012 Remi Collet <remi@fedoraproject.org> 5.5.0-0.8.201212110630
- patch for unpack

* Tue Dec 11 2012 Remi Collet <remi@fedoraproject.org> 5.5.0-0.7.201212110630
- prevent php_config.h changes across (otherwise identical) rebuilds
- drop "Configure Command" from phpinfo output

* Tue Dec 11 2012 Remi Collet <remi@fedoraproject.org> 5.5.0-0.6.201212110630
- new snapshot
- move gmp in new sub-package

* Mon Dec 10 2012 Remi Collet <remi@fedoraproject.org> 5.5.0-0.6.201212100830
- build sockets, tokenizer extensions shared

* Mon Dec 10 2012 Remi Collet <remi@fedoraproject.org> 5.5.0-0.5.201212100830
- new snapshot
- enable dtrace

* Tue Dec  4 2012 Remi Collet <remi@fedoraproject.org> 5.5.0-0.4.201211301534
- build simplexml and xml extensions shared (in php-xml)
- build bz2, calendar, ctype, exif, ftp, gettext and iconv
  extensions shared (in php-common)
- build gmp extension shared (in php-bcmath)
- build shmop extension shared (in php-process)

* Mon Dec  3 2012 Remi Collet <remi@fedoraproject.org> 5.5.0-0.3.201211301534
- drop some old compatibility provides (php-api, php-zend-abi, php-pecl-*)
- obsoletes php55-*

* Fri Nov 30 2012 Remi Collet <remi@fedoraproject.org> 5.5.0-0.2.201211301534
- update to have zend_execute_ex for xDebug

* Fri Nov 30 2012 Remi Collet <remi@fedoraproject.org> 5.5.0-0.1.201211300857
- Initial work on 5.5.0-dev

* Fri Nov 23 2012 Remi Collet <remi@fedoraproject.org> 5.4.9-2
- add patch for https://bugs.php.net/63588
  duplicated implementation of php_next_utf8_char

* Thu Nov 22 2012 Remi Collet <remi@fedoraproject.org> 5.4.9-1
- update to 5.4.9

* Thu Nov 15 2012 Remi Collet <rcollet@redhat.com> 5.4.9-0.5.RC1
- switch back to upstream generated scanner/parser

* Thu Nov 15 2012 Remi Collet <rcollet@redhat.com> 5.4.9-0.4.RC1
- use _httpd_contentdir macro and fix php.gif path

* Wed Nov 14 2012 Remi Collet <rcollet@redhat.com> 5.4.9-0.3.RC1
- improve system libzip patch to use pkg-config

* Wed Nov 14 2012 Remi Collet <rcollet@redhat.com> 5.4.9-0.2.RC1
- use _httpd_moddir macro

* Wed Nov 14 2012 Remi Collet <rcollet@redhat.com> 5.4.9-0.1.RC1
- update to 5.4.9RC1
- improves php.conf (use FilesMatch + SetHandler)
- improves filter (httpd module)
- apply ldap_r patch on fedora >= 18 only

* Fri Nov  9 2012 Remi Collet <remi@fedoraproject.org> 5.4.9-0.2.RC1
- sync with rawhide

* Fri Nov  9 2012 Remi Collet <rcollet@redhat.com> 5.4.8-6
- clarify Licenses
- missing provides xmlreader and xmlwriter
- modernize spec

* Thu Nov  8 2012 Remi Collet <remi@fedoraproject.org> 5.4.9-0.1.RC1
- update to 5.4.9RC1
- change php embedded library soname version to 5.4

* Tue Nov  6 2012 Remi Collet <rcollet@redhat.com> 5.4.8-5
- fix _httpd_mmn macro definition

* Mon Nov  5 2012 Remi Collet <rcollet@redhat.com> 5.4.8-4
- fix mysql_sock macro definition

* Thu Oct 25 2012 Remi Collet <rcollet@redhat.com> 5.4.8-3
- fix installed headers

* Tue Oct 23 2012 Joe Orton <jorton@redhat.com> - 5.4.8-2
- use libldap_r for ldap extension

* Thu Oct 18 2012 Remi Collet <remi@fedoraproject.org> 5.4.8-1
- update to 5.4.8
- define both session.save_handler and session.save_path
- fix possible segfault in libxml (#828526)
- php-fpm: create apache user if needed
- use SKIP_ONLINE_TEST during make test
- php-devel requires pcre-devel and php-cli (instead of php)

* Fri Oct  5 2012 Remi Collet <remi@fedoraproject.org> 5.4.8-0.3.RC1
- provides php-phar

* Thu Oct  4 2012 Remi Collet <RPMS@famillecollet.com> 5.4.8-0.2.RC1
- update systzdata patch to v10, timezone are case insensitive

* Thu Oct  4 2012 Remi Collet <RPMS@famillecollet.com> 5.4.8-0.1.RC1
- update to 5.4.8RC1

* Mon Oct  1 2012 Remi Collet <remi@fedoraproject.org> 5.4.7-10
- fix typo in systemd macro

* Mon Oct  1 2012 Remi Collet <remi@fedoraproject.org> 5.4.7-9
- php-fpm: enable PrivateTmp
- php-fpm: new systemd macros (#850268)
- php-fpm: add upstream patch for startup issue (#846858)

* Fri Sep 28 2012 Remi Collet <rcollet@redhat.com> 5.4.7-8
- systemd integration, https://bugs.php.net/63085
- no odbc call during timeout, https://bugs.php.net/63171
- check sqlite3_column_table_name, https://bugs.php.net/63149

* Mon Sep 24 2012 Remi Collet <rcollet@redhat.com> 5.4.7-7
- most failed tests explained (i386, x86_64)

* Wed Sep 19 2012 Remi Collet <rcollet@redhat.com> 5.4.7-6
- fix for http://bugs.php.net/63126 (#783967)

* Wed Sep 19 2012 Remi Collet <RPMS@famillecollet.com> 5.4.7-6
- add --daemonize / --nodaemonize options to php-fpm
  upstream RFE: https://bugs.php.net/63085

* Wed Sep 19 2012 Remi Collet <RPMS@famillecollet.com> 5.4.7-5
- sync with rawhide
- patch to report libdb version https://bugs.php.net/63117

* Wed Sep 19 2012 Remi Collet <rcollet@redhat.com> 5.4.7-5
- patch to ensure we use latest libdb (not libdb4)

* Wed Sep 19 2012 Remi Collet <rcollet@redhat.com> 5.4.7-4
- really fix rhel tests (use libzip and libdb)

* Tue Sep 18 2012 Remi Collet <rcollet@redhat.com> 5.4.7-3
- fix test to enable zip extension on RHEL-7

* Mon Sep 17 2012 Remi Collet <remi@fedoraproject.org> 5.4.7-2
- remove session.save_path from php.ini
  move it to apache and php-fpm configuration files

* Fri Sep 14 2012 Remi Collet <remi@fedoraproject.org> 5.4.7-1
- update to 5.4.7
  http://www.php.net/releases/5_4_7.php
- php-fpm: don't daemonize

* Thu Sep 13 2012 Remi Collet <RPMS@famillecollet.com> 5.4.7-1
- update to 5.4.7

* Mon Sep  3 2012 Remi Collet <RPMS@famillecollet.com> 5.4.7-0.2.RC1
- obsoletes php53* and php54*

* Fri Aug 31 2012 Remi Collet <RPMS@famillecollet.com> 5.4.7-0.1.RC1
- update to 5.4.7RC1

* Mon Aug 20 2012 Remi Collet <remi@fedoraproject.org> 5.4.6-2
- enable php-fpm on secondary arch (#849490)

* Thu Aug 16 2012 Remi Collet <remi@fedoraproject.org> 5.4.6-1
- update to 5.4.6

* Thu Aug 02 2012 Remi Collet <RPMS@famillecollet.com> 5.4.6-0.1.RC1
- update to 5.4.6RC1

* Fri Jul 20 2012 Remi Collet <RPMS@famillecollet.com> 5.4.5-1
- update to 5.4.5

* Sat Jul 07 2012 Remi Collet <RPMS@famillecollet.com> 5.4.5-0.2.RC1
- update patch for system libzip

* Wed Jul 04 2012 Remi Collet <RPMS@famillecollet.com> 5.4.5-0.1.RC1
- update to 5.4.5RC1 with bundled libzip.

* Mon Jul 02 2012 Remi Collet <RPMS@famillecollet.com> 5.4.4-4
- use system pcre only on fedora >= 14 (version 8.10)
- drop BR for libevent (#835671)
- provide php(language) to allow version check
- define %%{php_version}

* Thu Jun 21 2012 Remi Collet <RPMS@famillecollet.com> 5.4.4-2
- clean spec, sync with rawhide
- add missing provides (core, ereg, filter, standard)

* Wed Jun 13 2012 Remi Collet <Fedora@famillecollet.com> 5.4.4-1
- update to 5.4.4 finale
- fedora >= 15: use /usr/lib/tmpfiles.d instead of /etc/tmpfiles.d
- fedora >= 15: use /run/php-fpm instead of /var/run/php-fpm

* Thu May 31 2012 Remi Collet <Fedora@famillecollet.com> 5.4.4-0.2.RC2
- update to 5.4.4RC2

* Thu May 17 2012 Remi Collet <Fedora@famillecollet.com> 5.4.4-0.1.RC1
- update to 5.4.4RC1

* Wed May 09 2012 Remi Collet <Fedora@famillecollet.com> 5.4.3-1
- update to 5.4.3 (CVE-2012-2311, CVE-2012-2329)

* Thu May 03 2012 Remi Collet <remi@fedoraproject.org> 5.4.2-1
- update to 5.4.2 (CVE-2012-1823)

* Fri Apr 27 2012 Remi Collet <remi@fedoraproject.org> 5.4.1-1
- update to 5.4.1
- use libdb in fedora >= 18 instead of db4

* Fri Apr 13 2012 Remi Collet <remi@fedoraproject.org> 5.4.1-0.3.RC2
- update to 5.4.1RC2

* Sat Mar 31 2012 Remi Collet <remi@fedoraproject.org> 5.4.1-0.2.RC1
- rebuild

* Sat Mar 31 2012 Remi Collet <remi@fedoraproject.org> 5.4.1-0.1.RC1
- update to 5.4.1RC1, split php conf when httpd 2.4

* Tue Mar 27 2012 Remi Collet <remi@fedoraproject.org> 5.4.0-1.1
- sync with rawhide (httpd 2.4 stuff)

* Mon Mar 26 2012 Joe Orton <jorton@redhat.com> - 5.4.0-2
- rebuild against httpd 2.4
- use _httpd_mmn, _httpd_apxs macros
- fix --without-system-tzdata build for Debian et al

* Fri Mar 02 2012 Remi Collet <remi@fedoraproject.org> 5.4.0-1
- update to PHP 5.4.0 finale

* Sat Feb 18 2012 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.16.RC8
- update to 5.4.0RC8

* Sat Feb 04 2012 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.15.RC7
- update to 5.4.0RC7

* Fri Jan 27 2012 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.14.RC6
- build against system libzip (fedora >= 17), patch from spot

* Thu Jan 26 2012 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.13.RC6
- add /etc/sysconfig/php-fpm environment file (#784770)

* Wed Jan 25 2012 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.12.RC6
- keep all ZTS binaries in /usr/bin (with zts prefix)

* Thu Jan 19 2012 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.11.RC6
- update to 5.4.0RC6

* Wed Jan 18 2012 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.10.RC5
- add some fedora patches back (dlopen, easter, phpize)

* Mon Jan 16 2012 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.9.RC5
- improves mysql.sock default path

* Fri Jan 13 2012 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.8.RC5
- update to 5.4.0RC5
- patch for https://bugs.php.net/60748 (mysql.sock hardcoded)
- move session.path from php.ini to httpd/conf.d/php.conf
- provides both ZTS mysql extensions (libmysql/mysqlnd)
- build php cli ZTS binary, in -devel, mainly for test

* Wed Jan 04 2012 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.7.201201041830
- new snapshot (5.4.0RC5-dev) with fix for https://bugs.php.net/60627

* Fri Dec 30 2011 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.6.201112300630
- new snapshot (5.4.0RC5-dev)

* Mon Dec 26 2011 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.6.201112261030
- new snapshot (5.4.0RC5-dev)

* Sat Dec 17 2011 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.5.201112170630
- new snapshot (5.4.0RC4-dev)

* Mon Dec 12 2011 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.4.201112121330
- new snapshot (5.4.0RC4-dev)
- switch to systemd

* Fri Dec 09 2011 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.3.201112091730
- new snapshot (5.4.0RC4-dev)
- removed patch merged upstream for https://bugs.php.net/60392
- clean ini (from upstream production default)

* Sun Nov 13 2011 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.3.201111260730
- new snapshot (5.4.0RC3-dev)
- patch for https://bugs.php.net/60392 (old libicu on EL-5)

* Sun Nov 13 2011 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.3.201111130730
- new snapshot (5.4.0RC2-dev)
- sync with latest changes in 5.3 spec

* Thu Sep 08 2011 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.2.201109081430
- new snapshot
- build mysql/mysqli against both libmysql and mysqlnd (new mysqlnd sub-package)

* Sat Sep 03 2011 Remi Collet <Fedora@famillecollet.com> 5.4.0-0.1.201109031230
- first work on php 5.4
- remove -sqlite subpackage
- move php/modules-zts to php-zts/modules

