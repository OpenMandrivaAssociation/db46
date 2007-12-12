# compatibility with legacy rpm
%{!?_lib:%define _lib	lib}

%define	__soversion	4.6
%define	_libdb_a	libdb-%{__soversion}.a
%define	_libcxx_a	libdb_cxx-%{__soversion}.a

%define libname_orig	%mklibname db
%define libname		%{libname_orig}%{__soversion}
%define libnamedev	%{libname}-devel
%define libnamestatic	%{libname}-static-devel

%define libdbcxx	%{libname_orig}cxx%{__soversion}
%define libdbtcl	%{libname_orig}tcl%{__soversion}
%define libdbjava	%{libname_orig}java%{__soversion}

%define libdbnss	%{libname_orig}nss%{__soversion}
%define libdbnssdev	%{libdbnss}-devel

# Define Mandriva Linux version we are building for
%{?!mdkversion:%define mdkversion	%(perl -pe '/(\\d+)\\.(\\d)\\.?(\\d)?/; $_="$1$2".($3||0)' /etc/mandriva-release)}

# Define to build Java bindings (does not work)
%global build_java	1

# Allow --with[out] JAVA rpm command line build
%{?_with_java: %global build_java 1}
%{?_without_java: %global build_java 0}

# Define to build a stripped down version to use for nss libraries
%define build_nss	1

# Allow --with[out] nss rpm command line build
%{?_with_nss: %{expand: %%define build_nss 1}}
%{?_without_nss: %{expand: %%define build_nss 0}}

# Define to rename utilities and allow parallel installation
%define build_parallel	1

# Allow --with[out] parallel rpm command line build
%{?_with_parallel: %{expand: %%define build_parallel 1}}
%{?_without_parallel: %{expand: %%define build_parallel 0}}

# mutexes defaults to POSIX/pthreads/library
%define build_asmmutex 0

%{?_with_asmmutex: %global build_asmmutex 1}
%{?_without_asmmutex: %global build_asmmutex 0}

Summary:	The Berkeley DB database library for C
Name:		db46
Version:	4.6.21
Release:	%mkrel 1
Source:		http://download.oracle.com/berkeley-db/db-%{version}.tar.gz
# statically link db1 library
Patch0:		db-4.2.52-db185.patch
# fedora patches
Patch100:	db-4.6.18-glibc.patch
Patch101:	db-4.5.20-jni-include-dir.patch
URL:		http://www.oracle.com/technology/software/products/berkeley-db/
License:	BSD
Group:		System/Libraries
BuildRequires:	%{!?_without_tcl:tcl-devel} %{!?_without_db1:db1-devel} ed libtool
%if %{build_java}
BuildRequires:	gcc-java
BuildRequires:	java-1.4.2-gcj-compat
BuildRequires:	java-1.4.2-gcj-compat-devel
%endif
BuildRoot:	%{_tmppath}/%{name}-root

%description
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB is used by many applications, including Python and Perl, so this
should be installed on all systems.

%package -n %{libname}
Summary: The Berkeley DB database library for C
Group: System/Libraries

%description -n %{libname}
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB is used by many applications, including Python and Perl, so this
should be installed on all systems.

%package -n %{libdbcxx}
Summary: The Berkeley DB database library for C++
Group: System/Libraries

%description -n %{libdbcxx}
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB is used by many applications, including Python and Perl, so this
should be installed on all systems.

This package contains the files needed to build C++ programs which use
Berkeley DB.

%package -n %{libdbjava}
Summary: The Berkeley DB database library for C++
Group: System/Libraries

%description -n %{libdbjava}
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB is used by many applications, including Python and Perl, so this
should be installed on all systems.

This package contains the files needed to build Java programs which use
Berkeley DB.

%if %{!?_without_tcl:1}%{?_without_tcl:0}
%package -n %{libdbtcl}
Summary: The Berkeley DB database library for TCL
Group: System/Libraries

%description -n %{libdbtcl}
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB is used by many applications, including Python and Perl, so this
should be installed on all systems.

This package contains the header files, libraries, and documentation for
building tcl programs which use Berkeley DB.
%endif

%package utils
Summary: Command line tools for managing Berkeley DB databases
Group: Databases
%if !%{build_parallel}
Conflicts: db3-utils
%endif

%description utils
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB includes B+tree, Extended Linear Hashing, Fixed and Variable-length
record access methods, transactions, locking, logging, shared memory caching
and database recovery. DB supports C, C++, Java and Perl APIs.

This package contains command line tools for managing Berkeley DB databases.

%package -n %{libnamedev}
Summary: Development libraries/header files for the Berkeley DB library
Group: Development/Databases
Requires: %{libname} = %{version}-%{release}
Requires: %{libdbtcl} = %{version}-%{release}
Requires: %{libdbcxx} = %{version}-%{release}
Provides: db%{__soversion}-devel = %{version}-%{release}
Provides: libdb%{__soversion}-devel = %{version}-%{release}
Conflicts: %{libname_orig}3.3-devel %{libname_orig}4.0-devel
Conflicts: %{libname_orig}4.1-devel %{libname_orig}4.2-devel
Conflicts: %{libname_orig}4.3-devel %{libname_orig}4.4-devel
Conflicts: %{libname_orig}4.5-devel

%description -n %{libnamedev}
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB includes B+tree, Extended Linear Hashing, Fixed and Variable-length
record access methods, transactions, locking, logging, shared memory caching
and database recovery. DB supports C, C++, Java and Perl APIs.

This package contains the header files, libraries, and documentation for
building programs which use Berkeley DB.

%package -n %{libnamestatic}
Summary: Development static libraries files for the Berkeley DB library
Group: Development/Databases
Requires: db%{__soversion}-devel = %{version}-%{release}
Provides: db%{__soversion}-static-devel = %{version}-%{release}
Provides: libdb%{__soversion}-static-devel = %{version}-%{release}
Conflicts: %{libname_orig}3.3-static-devel %{libname_orig}4.0-static-devel
Conflicts: %{libname_orig}4.1-static-devel %{libname_orig}4.2-static-devel
Conflicts: %{libname_orig}4.3-static-devel %{libname_orig}4.4-static-devel
Conflicts: %{libname_orig}4.5-static-devel

%description -n %{libnamestatic}
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB includes B+tree, Extended Linear Hashing, Fixed and Variable-length
record access methods, transactions, locking, logging, shared memory caching
and database recovery. DB supports C, C++, Java and Perl APIs.

This package contains the static libraries for building programs which
use Berkeley DB.

%if %{build_nss}
%package -n %{libdbnss}
Summary: The Berkeley DB database library for NSS modules
Group: System/Libraries

%description -n %{libdbnss}
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB includes B+tree, Extended Linear Hashing, Fixed and Variable-length
record access methods, transactions, locking, logging, shared memory caching
and database recovery. DB supports C, C++, Java and Perl APIs.

This package contains the shared library required by some nss modules
that use Berkeley DB.

%package -n %{libdbnssdev}
Summary: Development libraries/header files for building nss modules with Berkeley DB
Group: Development/Databases
Requires: %{libdbnss} = %{version}-%{release}
Provides: libdbnss-devel = %{version}-%{release}
Provides: %{_lib}dbnss-devel = %{version}-%{release}
Provides: db_nss-devel = %{version}-%{release}
Provides: libdb_nss-devel = %{version}-%{release}

%description -n %{libdbnssdev}
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB includes B+tree, Extended Linear Hashing, Fixed and Variable-length
record access methods, transactions, locking, logging, shared memory caching
and database recovery. DB supports C, C++, Java and Perl APIs.

This package contains the header files and libraries for building nss
modules which use Berkeley DB.
%endif

%prep
%setup -q -n db-%{version}
%patch0 -p1 -b .db185

# fedora patches
%patch100 -p1 -b .glibc
%patch101 -p1 -b .4.5.20.jni

pushd dist
libtoolize --copy --force
cat %{_datadir}/aclocal/libtool.m4 >> aclocal.m4
popd

# Remove tags files which we don't need.
find . -name tags | xargs rm -f
# Define a shell function for fixing HREF references in the docs, which
# would otherwise break when we split the docs up into subpackages.
fixup_href() {
    for doc in $@ ; do
        chmod u+w ${doc}
        sed -e 's,="../api_c/,="../../%{name}-devel-%{version}/api_c/,g' \
            -e 's,="api_c/,="../%{name}-devel-%{version}/api_c/,g' \
            -e 's,="../api_cxx/,="../../%{name}-devel-%{version}/api_cxx/,g' \
            -e 's,="api_cxx/,="../%{name}-devel-%{version}/api_cxx/,g' \
            -e 's,="../api_tcl/,="../../%{name}-devel-%{version}/api_tcl/,g' \
            -e 's,="api_tcl/,="../%{name}-devel-%{version}/api_tcl/,g' \
            -e 's,="../java/,="../../%{name}-devel-%{version}/java/,g' \
            -e 's,="java/,="../%{name}-devel-%{version}/java/,g' \
            -e 's,="../examples_c/,="../../%{name}-devel-%{version}/examples_c/,g' \
            -e 's,="examples_c/,="../%{name}-devel-%{version}/examples_c/,g' \
            -e 's,="../examples_cxx/,="../../%{name}-devel-%{version}/examples_cxx/,g' \
            -e 's,="examples_cxx/,="../%{name}-devel-%{version}/examples_cxx/,g' \
            -e 's,="../ref/,="../../%{name}-devel-%{version}/ref/,g' \
            -e 's,="ref/,="../%{name}-devel-%{version}/ref/,g' \
            -e 's,="../images/,="../../%{name}-devel-%{version}/images/,g' \
            -e 's,="images/,="../%{name}-devel-%{version}/images/,g' \
            -e 's,="../utility/,="../../%{name}-utils-%{version}/utility/,g' \
            -e 's,="utility/,="../%{name}-utils-%{version}/utility/,g' ${doc} > ${doc}.new
        touch -r ${doc} ${doc}.new
        cat ${doc}.new > ${doc}
        touch -r ${doc}.new ${doc}
        rm -f ${doc}.new
    done
}

set +x	# XXX painful to watch
# Fix all of the HTML files.
fixup_href `find . -name "*.html"`
set -x	# XXX painful to watch

cd dist
./s_config

%build
CFLAGS="$RPM_OPT_FLAGS"
%ifarch ppc
CFLAGS="$CFLAGS -D_GNU_SOURCE -D_REENTRANT"
%endif
export CFLAGS

%if %{build_java}
ENABLE_JAVA="--enable-java"
%endif

pushd build_unix
CONFIGURE_TOP="../dist" %configure2_5x \
	--enable-shared --enable-static --enable-rpc \
%if %{?!_without_db1:1}%{?_without_db1:0}
	--enable-compat185 --enable-dump185 \
%endif
%if %{?!_without_tcl:1}%{?_without_tcl:0}
	--enable-tcl --with-tcl=%{_libdir} --enable-test \
%endif
	--enable-cxx $ENABLE_JAVA \
%if %{build_asmmutex}
%ifarch %{ix86}
	--disable-posixmutexes --with-mutex=x86/gcc-assembly
%endif
%ifarch x86_64
	--disable-posixmutexes --with-mutex=x86_64/gcc-assembly
%endif
%ifarch alpha
	--disable-posixmutexes --with-mutex=ALPHA/gcc-assembly
%endif
%ifarch ia64
	--disable-posixmutexes --with-mutex=ia64/gcc-assembly
%endif
%ifarch ppc
	--disable-posixmutexes --with-mutex=PPC/gcc-assembly
%endif
%ifarch %{sunsparc}
	--disable-posixmutexes --with-mutex=Sparc/gcc-assembly
%endif
%else
	--with-mutex=POSIX/pthreads/library
%endif

%make
popd
%if %{build_nss}
mkdir build_nss
pushd build_nss
CONFIGURE_TOP="../dist" %configure2_5x \
	--enable-shared --disable-static \
	--disable-tcl --disable-cxx --disable-java \
	--with-uniquename=_nss \
	--enable-compat185 \
	--disable-cryptography --disable-queue \
        --disable-replication --disable-verify \
%ifarch %{ix86}
	--disable-posixmutexes --with-mutex=x86/gcc-assembly
%endif
%ifarch x86_64
	--disable-posixmutexes --with-mutex=x86_64/gcc-assembly
%endif
%ifarch alpha
	--disable-posixmutexes --with-mutex=ALPHA/gcc-assembly
%endif
%ifarch ia64
	--disable-posixmutexes --with-mutex=ia64/gcc-assembly
%endif
%ifarch ppc
	--disable-posixmutexes --with-mutex=PPC/gcc-assembly
%endif
%ifarch %{sunsparc}
	--disable-posixmutexes --with-mutex=Sparc/gcc-assembly
%endif

%make libdb_base=libdb_nss libso_target=libdb_nss-%{__soversion}.la libdir=/%{_lib}
popd
%endif

%install
rm -rf %{buildroot}
make -C build_unix install_setup install_include install_lib install_utilities \
	DESTDIR=%{buildroot} includedir=%{_includedir}/db4 \
	emode=755

%if %{build_nss}
make -C build_nss install_include install_lib libdb_base=libdb_nss \
	DESTDIR=%{buildroot} includedir=%{_includedir}/db_nss \
	LIB_INSTALL_FILE_LIST=""

mkdir -p %{buildroot}/%{_lib}
mv %{buildroot}/%{_libdir}/libdb_nss-%{__soversion}.so %{buildroot}/%{_lib}
ln -s  /%{_lib}/libdb_nss-%{__soversion}.so %{buildroot}%{_libdir}
%endif

ln -sf db4/db.h %{buildroot}%{_includedir}/db.h

# XXX This is needed for parallel install with db4.2
%if %{build_parallel}
for F in %{buildroot}%{_bindir}/*db_* ; do
   mv $F `echo $F | sed -e 's,db_,%{name}_,'`
done
%endif

# Move db.jar file to the correct place, and version it
%if %{build_java}
mkdir -p %{buildroot}%{_datadir}/java
mv %{buildroot}%{_libdir}/db.jar %{buildroot}%{_datadir}/java/db-%{__soversion}.jar
%endif

#symlink the short libdb???.a name
ln -sf %{_libdb_a} %{buildroot}%{_libdir}/libdb.a
ln -sf %{_libcxx_a} %{buildroot}%{_libdir}/libdb_cxx.a
ln -sf libdb_tcl-%{__soversion}.a %{buildroot}%{_libdir}/libdb_tcl.a
ln -sf %{_libdb_a} %{buildroot}%{_libdir}/libdb-4.a
ln -sf %{_libcxx_a} %{buildroot}%{_libdir}/libdb_cxx-4.a
ln -sf libdb_tcl-%{__soversion}.a %{buildroot}%{_libdir}/libdb_tcl-4.a
%if %{build_java}
ln -sf libdb_java-%{__soversion}.a %{buildroot}%{_libdir}/libdb_java.a
ln -sf libdb_java-%{__soversion}.a %{buildroot}%{_libdir}/libdb_java-4.a
%endif

%clean
rm -rf %{buildroot}

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%post -n %{libdbcxx} -p /sbin/ldconfig
%postun -n %{libdbcxx} -p /sbin/ldconfig

%if %{build_java}
%post -n %{libdbjava} -p /sbin/ldconfig
%postun -n %{libdbjava} -p /sbin/ldconfig
%endif

%if %{?!_without_tcl:1}%{?_without_tcl:0} 
%post -n %{libdbtcl} -p /sbin/ldconfig
%postun -n %{libdbtcl} -p /sbin/ldconfig
%endif

%if %{build_nss}
%post -n %{libdbnss} -p /sbin/ldconfig
%postun -n %{libdbnss} -p /sbin/ldconfig
%endif

%files -n %{libname}
%defattr(644,root,root,755)
%doc LICENSE README
%attr(755,root,root) %{_libdir}/libdb-%{__soversion}.so

%files -n %{libdbcxx}
%defattr(755,root,root) 
%{_libdir}/libdb_cxx-%{__soversion}.so

%if %{build_java}
%files -n %{libdbjava}
%defattr(644,root,root,755) 
%doc docs/java
%doc examples_java
%attr(755,root,root) %{_libdir}/libdb_java-%{__soversion}.so
%attr(755,root,root) %{_libdir}/libdb_java-%{__soversion}_g.so
%{_datadir}/java/db-%{__soversion}.jar
%endif

%if %{?!_without_tcl:1}%{?_without_tcl:0} 
%files -n %{libdbtcl}
%defattr(755,root,root)
%{_libdir}/libdb_tcl-%{__soversion}.so
%endif

%files utils
%defattr(-,root,root)
%doc	docs/utility
%{_bindir}/berkeley_db*_svc
%{_bindir}/db*_archive
%{_bindir}/db*_checkpoint
%{_bindir}/db*_deadlock
%{_bindir}/db*_dump*
%{_bindir}/db*_load
%{_bindir}/db*_printlog
%{_bindir}/db*_recover
%{_bindir}/db*_stat
%{_bindir}/db*_upgrade
%{_bindir}/db*_verify
%{_bindir}/db*_hotbackup
%{_bindir}/db*_codegen

%files -n %{libnamedev}
%defattr(644,root,root,755)
%doc	docs/api_c docs/api_cxx docs/api_tcl docs/index.html
%doc	docs/ref docs/images
%doc	examples_c examples_cxx
%dir %{_includedir}/db4
%{_includedir}/db4/db.h
%if %{?!_without_db1:1}%{?_without_db1:0} 
%{_includedir}/db4/db_185.h
%endif
%{_includedir}/db4/db_cxx.h
%{_includedir}/db.h
%{_libdir}/libdb.so
%{_libdir}/libdb-4.so
%{_libdir}/libdb-%{__soversion}.la
%{_libdir}/libdb_cxx.so
%{_libdir}/libdb_cxx-4.so
%{_libdir}/libdb_cxx-%{__soversion}.la
%if %{?!_without_tcl:1}%{?_without_tcl:0} 
%{_libdir}/libdb_tcl.so
%{_libdir}/libdb_tcl-4.so
%{_libdir}/libdb_tcl-%{__soversion}.la
%endif
%if %build_java
%{_libdir}/libdb_java.so
%{_libdir}/libdb_java-4.so
%{_libdir}/libdb_java-%{__soversion}.la
%endif

%files -n %{libnamestatic}
%defattr(644,root,root,755)
%{_libdir}/*.a

%if %{build_nss}
%files -n %{libdbnss}
%defattr(755,root,root) 
/%{_lib}/libdb_nss-%{__soversion}.so

%files -n %{libdbnssdev}
%defattr(644,root,root,755)
%dir %{_includedir}/db_nss
%{_includedir}/db_nss/db.h
%if %{?!_without_db1:1}%{?_without_db1:0} 
%{_includedir}/db_nss/db_185.h
%endif
%exclude %{_includedir}/db_nss/db_cxx.h
%{_libdir}/libdb_nss.so
%{_libdir}/libdb_nss-4.so
%{_libdir}/libdb_nss-%{__soversion}.la
%{_libdir}/libdb_nss-%{__soversion}.so
%endif
