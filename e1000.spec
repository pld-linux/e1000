#
# Conditional build:
# _without_dist_kernel          without distribution kernel
#
%define		_orig_name	e1000

%{!?_without_dist_kernel:%define	_mod_name %{_orig_name}_intel }
%{?_without_dist_kernel:%define		_mod_name %{_orig_name} }

Summary:	Intel(R) PRO/1000 driver for Linux
Summary(pl):	Sterownik do karty Intel(R) PRO/1000
Name:		kernel-net-%{_orig_name}
Version:	5.2.30.1
%define	_rel	1
Release:	%{_rel}@%{_kernel_ver_str}
License:	BSD
Vendor:		Intel Corporation
Group:		Base/Kernel
Source0:	ftp://aiedownload.intel.com/df-support/2897/eng/%{_orig_name}-%{version}.tar.gz
# Source0-md5:	c2e66550ab7213df1b1fe26b8a4b5f9a
%{!?_without_dist_kernel:BuildRequires:	kernel-headers >= 2.4.20 }
BuildRequires:	%{kgcc_package}
BuildRequires:	rpmbuild(macros) >= 1.118
URL:		http://support.intel.com/support/network/adapter/pro100/
%{!?_without_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
Provides:	kernel(e1000)
Obsoletes:	e1000
Obsoletes:	linux-net-e1000
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the Linux driver for the Intel(R) PRO/1000
family of 10/100/1000 Ethernet network adapters.

%description -l pl
Ten pakiet zawiera sterownik dla Linuksa do kart sieciowych
10/100/1000Mbit z rodziny Intel(R) PRO/1000.

%package -n kernel-smp-net-%{_orig_name}
Summary:	Intel(R) PRO/1000 driver for Linux SMP
Summary(pl):	Sterownik do karty Intel(R) PRO/1000
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{!?_without_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
Provides:	kernel(e1000)
Obsoletes:	e1000
Obsoletes:	linux-net-e1000

%description -n kernel-smp-net-%{_orig_name}
This package contains the Linux SMP driver for the Intel(R) PRO/1000
family of 10/100/1000 Ethernet network adapters.

%description -n kernel-smp-net-%{_orig_name} -l pl
Ten pakiet zawiera sterownik dla Linuksa SMP do kart sieciowych
10/100/1000Mbit z rodziny Intel(R) PRO/1000.

%prep
%setup -q -n %{_orig_name}-%{version}

%build
rm -rf build-done 
install -d build-done/{UP,SMP}
cd src
rm -rf include
ln -sf %{_kernelsrcdir}/config-up .config
install -d include/{linux,config}
ln -sf %{_kernelsrcdir}/include/linux/autoconf.h include/linux/autoconf.h
ln -sf %{_kernelsrcdir}/include/asm-%{_arch} include/asm
touch include/config/MARKER
echo 'obj-m := e1000.o'>Makefile
echo 'e1000-objs := e1000_main.o e1000_hw.o e1000_param.o e1000_ethtool.o kcompat.o'>>Makefile

%{__make} -C %{_kernelsrcdir} SUBDIRS=$PWD O=$PWD V=1 modules

mv e1000.ko ../build-done/UP/

%{__make} -C %{_kernelsrcdir} SUBDIRS=$PWD O=$PWD V=1 mrproper


ln -sf %{_kernelsrcdir}/config-smp .config
rm -rf include
install -d include/{linux,config}
ln -sf %{_kernelsrcdir}/include/linux/autoconf.h include/linux/autoconf.h
ln -sf %{_kernelsrcdir}/include/asm-%{_arch} include/asm
touch include/config/MARKER
echo 'obj-m := e1000.o'>Makefile
echo 'e1000-objs := e1000_main.o e1000_hw.o e1000_param.o e1000_ethtool.o kcompat.o'>>Makefile

%{__make} -C %{_kernelsrcdir} SUBDIRS=$PWD O=$PWD V=1 modules
mv e1000.ko ../build-done/SMP/

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/misc
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/drivers/net/misc
install build-done/SMP/* $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/misc/%{_mod_name}.o
install build-done/UP/* $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/drivers/net/misc/%{_mod_name}.o

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%post	-n kernel-smp-net-%{_orig_name}
%depmod %{_kernel_ver}smp

%postun -n kernel-smp-net-%{_orig_name}
%depmod %{_kernel_ver}smp

%files
%defattr(644,root,root,755)
%doc %{_orig_name}.7 README ldistrib.txt
/lib/modules/%{_kernel_ver}/kernel/drivers/net/misc/*

%files -n kernel-smp-net-%{_orig_name}
%defattr(644,root,root,755)
%doc %{_orig_name}.7 README ldistrib.txt
/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/misc/*
