#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)
#
Summary:	Intel(R) PRO/1000 driver for Linux
Summary(pl):	Sterownik do karty Intel(R) PRO/1000
Name:		kernel-net-e1000
Version:	6.2.15
%define		_rel	1
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL v2
Vendor:		Intel Corporation
Group:		Base/Kernel
Source0:	ftp://aiedownload.intel.com/df-support/9180/eng/e1000-%{version}.tar.gz
# Source0-md5:	83f16b6b3f255730e0649f23cfc01509
URL:		http://support.intel.com/support/network/adapter/index.htm#PRO/1000
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 2.6.7}
BuildRequires:	rpmbuild(macros) >= 1.211
%ifarch sparc
BuildRequires:	crosssparc64-gcc
%endif
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif
Provides:	kernel(e1000)
Obsoletes:	e1000
Obsoletes:	linux-net-e1000
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%ifarch sparc
%define         _target_base_arch       sparc64
%define         _target_cpu             sparc64
%endif

%description
This package contains the Linux driver for the Intel(R) PRO/1000
family of 10/100/1000 Ethernet network adapters.

%description -l pl
Ten pakiet zawiera sterownik dla Linuksa do kart sieciowych
10/100/1000Mbit z rodziny Intel(R) PRO/1000.

%package -n kernel-smp-net-e1000
Summary:	Intel(R) PRO/1000 driver for Linux SMP
Summary(pl):	Sterownik do karty Intel(R) PRO/1000
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif
Provides:	kernel(e1000)
Obsoletes:	e1000
Obsoletes:	linux-net-e1000

%description -n kernel-smp-net-e1000
This package contains the Linux SMP driver for the Intel(R) PRO/1000
family of 10/100/1000 Ethernet network adapters.

%description -n kernel-smp-net-e1000 -l pl
Ten pakiet zawiera sterownik dla Linuksa SMP do kart sieciowych
10/100/1000Mbit z rodziny Intel(R) PRO/1000.

%prep
%setup -q -n e1000-%{version}

%build
cd src
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	rm -rf include
	install -d include/{linux,config}
	ln -sf %{_kernelsrcdir}/config-$cfg .config
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h include/linux/autoconf.h
%ifarch ppc
	if [ -d "%{_kernelsrcdir}/include/asm-powerpc" ]; then
		install -d include/asm
		cp -a %{_kernelsrcdir}/include/asm-%{_target_base_arch}/* include/asm
		cp -a %{_kernelsrcdir}/include/asm-powerpc/* include/asm
	else
		ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} include/asm
	fi
%else
	ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} include/asm
%endif
	ln -sf %{_kernelsrcdir}/Module.symvers-$cfg Module.symvers
	touch include/config/MARKER

cat >Makefile <<EOF
obj-m := e1000i.o
e1000i-objs := e1000_main.o e1000_hw.o e1000_param.o e1000_ethtool.o kcompat.o
EOF

	%{__make} -C %{_kernelsrcdir} clean \
		RCS_FIND_IGNORE="-name '*.ko' -o" \
		M=$PWD O=$PWD \
		%{?with_verbose:V=1}
	%{__make} -C %{_kernelsrcdir} modules \
%if "%{_target_base_arch}" != "%{_arch}"
                ARCH=%{_target_base_arch} \
                CROSS_COMPILE=%{_target_cpu}-pld-linux- \
%endif
                HOSTCC="%{__cc}" \
		EXTRA_CFLAGS='-DE1000_NAPI' \
		M=$PWD O=$PWD \
		%{?with_verbose:V=1}

	mv e1000i{,-$cfg}.ko
done

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/kernel/drivers/net
cd src
install e1000i-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/drivers/net/e1000i.ko
%if %{with smp} && %{with dist_kernel}
install e1000i-smp.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/e1000i.ko
%endif
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%post	-n kernel-smp-net-e1000
%depmod %{_kernel_ver}smp

%postun -n kernel-smp-net-e1000
%depmod %{_kernel_ver}smp

%files
%defattr(644,root,root,755)
%doc e1000.7 README ldistrib.txt
/lib/modules/%{_kernel_ver}/kernel/drivers/net/*

%if %{with smp} && %{with dist_kernel}
%files -n kernel-smp-net-e1000
%defattr(644,root,root,755)
%doc e1000.7 README ldistrib.txt
/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/*
%endif
