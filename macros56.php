#
# Interface versions exposed by PHP:
# 
%php_core_api @PHP_APIVER@
%php_zend_api @PHP_ZENDVER@
%php_pdo_api  @PHP_PDOVER@
%php_version  @PHP_VERSION@

%php_extdir   @LIBDIR@/php56/modules

%php_inidir   @ETCDIR@/php56.d

%php_incldir  @INCDIR@/php56

%__php        @BINDIR@/php56
