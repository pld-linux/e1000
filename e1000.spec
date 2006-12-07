#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)
#
%define		_rel	3
Summary:	Intel(R) PRO/1000 driver for Linux
Summary(pl):	Sterownik do karty Intel(R) PRO/1000
Name:		kernel%{_alt_kernel}-net-e1000
Version:	7.2.9
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL v2
Group:		Base/Kernel
Source0:	ftp://aiedownload.intel.com/df-support/9180/eng/e1000-%{version}.tar.gz
# Source0-md5:	cb9f601df6c60f889aaabec475ba2089
URL:		http://support.intel.com/support/network/adapter/index.htm#PRO/1000
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.7}
BuildRequires:	rpmbuild(macros) >= 1.330
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif
Provides:	kernel(e1000)
Obsoletes:	e1000
Obsoletes:	linux-net-e1000
# gcc fails on AC
ExcludeArch:	ppc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the Linux driver for the Intel(R) PRO/1000
family of 10/100/1000 Ethernet network adapters.

%description -l pl
Ten pakiet zawiera sterownik dla Linuksa do kart sieciowych
10/100/1000Mbit z rodziny Intel(R) PRO/1000.

%package -n kernel%{_alt_kernel}-smp-net-e1000
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

%description -n kernel%{_alt_kernel}-smp-net-e1000
This package contains the Linux SMP driver for the Intel(R) PRO/1000
family of 10/100/1000 Ethernet network adapters.

%description -n kernel%{_alt_kernel}-smp-net-e1000 -l pl
Ten pakiet zawiera sterownik dla Linuksa SMP do kart sieciowych
10/100/1000Mbit z rodziny Intel(R) PRO/1000.

%prep
%setup -q -n e1000-%{version}
cat > src/Makefile <<'EOF'
obj-m := e1000.o
e1000-objs := e1000_main.o e1000_hw.o e1000_param.o e1000_ethtool.o kcompat.o
EOF

%build
%build_kernel_modules -C src -m e1000

%install
rm -rf $RPM_BUILD_ROOT
%install_kernel_modules -m src/e1000 -d kernel/drivers/net -n e1000 -s current

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-smp-net-e1000
%depmod %{_kernel_ver}smp

%postun -n kernel%{_alt_kernel}-smp-net-e1000
%depmod %{_kernel_ver}smp

%files
%defattr(644,root,root,755)
%doc e1000.7 README ldistrib.txt
/etc/modprobe.d/%{_kernel_ver}/e1000.conf
/lib/modules/%{_kernel_ver}/kernel/drivers/net/e1000*.ko*

%if %{with smp} && %{with dist_kernel}
%files -n kernel%{_alt_kernel}-smp-net-e1000
%defattr(644,root,root,755)
%doc e1000.7 README ldistrib.txt
/etc/modprobe.d/%{_kernel_ver}smp/e1000.conf
/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/e1000*.ko*
%endif
