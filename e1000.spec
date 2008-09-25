#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	smp		# don't build SMP module
%bcond_without	up		# don't build UP module
%bcond_with	verbose		# verbose build (V=1)

%ifarch sparc
%undefine	with_smp
%endif

%if %{without kernel}
%undefine	 with_dist_kernel
%endif
%if "%{_alt_kernel}" != "%{nil}"
%undefine	with_userspace
%endif
# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0

%define		rel		2
%define		pname	e1000
Summary:	Intel(R) PRO/1000 driver for Linux
Summary(pl.UTF-8):	Sterownik do karty Intel(R) PRO/1000
Name:		%{pname}%{_alt_kernel}
Version:	8.0.3.1
Release:	%{rel}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://dl.sourceforge.net/e1000/%{pname}-%{version}.tar.gz
# Source0-md5:	2988cb6e296e9b2fa2eb5141a0baadd9
URL:		http://sourceforge.net/projects/e1000/
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.7}
BuildRequires:	rpmbuild(macros) >= 1.330
# gcc fails on AC
ExcludeArch:	ppc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the Linux driver for the Intel(R) PRO/1000
adapters with 8254x chipsets.

%description -l pl.UTF-8
Ten pakiet zawiera sterownik dla Linuksa do kart sieciowych z rodziny
Intel(R) PRO/1000 opartych o układy 8254x.

%package -n kernel%{_alt_kernel}-net-e1000
Summary:	Intel(R) PRO/1000 driver for Linux
Summary(pl.UTF-8):	Sterownik do karty Intel(R) PRO/1000
Release:	%{rel}@%{_kernel_vermagic}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%{?with_dist_kernel:Requires:	kernel%{_alt_kernel}(vermagic) = %{_kernel_ver}}
Obsoletes:	e1000
Obsoletes:	linux-net-e1000

%description -n kernel%{_alt_kernel}-net-e1000
This package contains the Linux driver for the Intel(R) PRO/1000
adapters with 8254x chipsets.

%description -n kernel%{_alt_kernel}-net-e1000 -l pl.UTF-8
Ten pakiet zawiera sterownik dla Linuksa SMP do kart sieciowych
10/100/1000Mbit z rodziny Intel(R) PRO/1000.

%package -n kernel%{_alt_kernel}-smp-net-e1000
Summary:	Intel(R) PRO/1000 driver for Linux SMP
Summary(pl.UTF-8):	Sterownik do karty Intel(R) PRO/1000
Release:	%{rel}@%{_kernel_vermagic}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%{?with_dist_kernel:Requires:	kernel%{_alt_kernel}-smp(vermagic) = %{_kernel_ver}}
Obsoletes:	e1000
Obsoletes:	linux-net-e1000

%description -n kernel%{_alt_kernel}-smp-net-e1000
This package contains the Linux driver for the Intel(R) PRO/1000
adapters with 8254x chipsets.

%description -n kernel%{_alt_kernel}-smp-net-e1000 -l pl.UTF-8
Ten pakiet zawiera sterownik dla Linuksa SMP do kart sieciowych
10/100/1000Mbit z rodziny Intel(R) PRO/1000.

%prep
%setup -q -n %{pname}-%{version}
cat > src/Makefile <<'EOF'
obj-m := e1000.o
e1000-objs := e1000_main.o e1000_82540.o e1000_82542.o e1000_82541.o e1000_82543.o \
e1000_mac.o e1000_nvm.o e1000_phy.o e1000_manage.o e1000_param.o e1000_ethtool.o \
kcompat.o e1000_api.o

EXTRA_CFLAGS=-DDRIVER_E1000
EOF

%build
%build_kernel_modules -C src -m %{pname}

%install
rm -rf $RPM_BUILD_ROOT
%install_kernel_modules -m src/%{pname} -d kernel/drivers/net -n %{pname} -s current
# blacklist kernel module
cat > $RPM_BUILD_ROOT/etc/modprobe.d/%{_kernel_ver}/%{pname}.conf <<'EOF'
blacklist e1000
alias e1000 e1000-current
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-net-e1000
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-net-e1000
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-smp-net-e1000
%depmod %{_kernel_ver}smp

%postun -n kernel%{_alt_kernel}-smp-net-e1000
%depmod %{_kernel_ver}smp

%if %{with kernel}
%if %{with up}
%files -n kernel%{_alt_kernel}-net-e1000
%defattr(644,root,root,755)
%doc e1000.7 README
/etc/modprobe.d/%{_kernel_ver}/%{pname}.conf
/lib/modules/%{_kernel_ver}/kernel/drivers/net/%{pname}*.ko*
%endif

%if %{with smp} && %{with dist_kernel}
%files -n kernel%{_alt_kernel}-smp-net-e1000
%defattr(644,root,root,755)
%doc e1000.7 README
/etc/modprobe.d/%{_kernel_ver}smp/%{pname}.conf
/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/%{pname}*.ko*
%endif
%endif
