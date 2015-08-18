SPEC := $(shell ls *.spec)
TOPDIR := $(shell dirname $(CURDIR))/rpmbuild

all: build clean

build:
	mkdir -p ${TOPDIR}/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
	cp -a *.blacklist *.bz2 *.conf *.ini* *.logrotate *.modconf *.patch *.php *.service *.sysconfig *.ztsmodconf ${TOPDIR}/SOURCES/
	cp -a *.spec  ${TOPDIR}/SPECS/
	rpmbuild -ba --define "_topdir ${TOPDIR}" --clean ${TOPDIR}/SPECS/${SPEC}
	find ${TOPDIR}/ -type f -iname \*.rpm -exec cp -a {} ../ \;

.PHONY: clean

clean:
	rm -rf ${TOPDIR}


