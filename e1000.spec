# conditional build
# _without_dist_kernel          without distribution kernel

%define		_orig_name	e1000

Summary:	Intel(R) PRO/1000 driver for Linux
Summary(pl):	Sterownik do karty Intel(R) PRO/1000
Name:		kernel-net-%{_orig_name}
Version:	4.3.15
%define	_rel	6
Release:	%{_rel}@%{_kernel_ver_str}
License:	BSD
Vendor:		Intel Corporation
Group:		Base/Kernel
Source0:	ftp://aiedownload.intel.com/df-support/2897/eng/%{_orig_name}-%{version}.tar.gz
# Source0-md5:	d1b09d0210c27f8aa931601980da5b56
%{!?_without_dist_kernel:BuildRequires:         kernel-headers }
BuildRequires:	%{kgcc_package}
URL:		http://support.intel.com/support/network/adapter/pro100/
Obsoletes:	e1000
Obsoletes:	linux-net-e1000
Provides:	kernel(e1000)
Prereq:		/sbin/depmod
%{!?_without_dist_kernel:%requires_releq_kernel_up}
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
Prereq:		/sbin/depmod
%{!?_without_dist_kernel:%requires_releq_kernel_smp}
Obsoletes:	e1000
Obsoletes:	linux-net-e1000
Provides:	kernel(e1000)

%description -n kernel-smp-net-%{_orig_name}
This package contains the Linux SMP driver for the Intel(R) PRO/1000
family of 10/100/1000 Ethernet network adapters.

%description -n kernel-smp-net-%{_orig_name} -l pl
Ten pakiet zawiera sterownik dla Linuksa SMP do kart sieciowych
10/100/1000Mbit z rodziny Intel(R) PRO/1000.

%prep
%setup -q -n %{_orig_name}-%{version}

%build
%{__make} -C src SMP=1 CC="%{kgcc} -DCONFIG_X86_LOCAL_APIC -DSTB_WA" KSRC=%{_kernelsrcdir}
mv -f src/%{_orig_name}.o src/%{_orig_name}-smp.o
%{__make} -C src clean KSRC=%{_kernelsrcdir}
%{__make} -C src CC="%{kgcc} -DSTB_WA" KSRC=%{_kernelsrcdir}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc
install src/%{_orig_name}-smp.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/%{_orig_name}.o
install src/%{_orig_name}.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/%{_orig_name}.o

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/depmod -a

%postun
/sbin/depmod -a

%post -n kernel-smp-net-%{_orig_name}
/sbin/depmod -a

%postun -n kernel-smp-net-%{_orig_name}
/sbin/depmod -a

%files
%defattr(644,root,root,755)
%doc %{_orig_name}.7 README ldistrib.txt
/lib/modules/%{_kernel_ver}/misc/*

%files -n kernel-smp-net-%{_orig_name}
%defattr(644,root,root,755)
%doc %{_orig_name}.7 README ldistrib.txt
/lib/modules/%{_kernel_ver}smp/misc/*
