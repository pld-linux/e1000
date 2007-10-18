#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_with	verbose		# verbose build (V=1)
#
%define		_rel	1
%define		_mod_name	e1000
#
Summary:	Intel(R) PRO/1000 driver for Linux
Summary(pl.UTF-8):	Sterownik do karty Intel(R) PRO/1000
Name:		kernel%{_alt_kernel}-net-e1000
Version:	7.6.9.1
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://dl.sourceforge.net/e1000/%{_mod_name}-%{version}.tar.gz
# Source0-md5:	84ef95f4eae5106c91efec2b2e42ba91
URL:		http://sourceforge.net/projects/e1000/
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Provides:	kernel(e1000)
Obsoletes:	e1000
Obsoletes:	linux-net-e1000
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the Linux driver for the Intel(R) PRO/1000
family of 10/100/1000 Ethernet network adapters.

%description -l pl.UTF-8
Ten pakiet zawiera sterownik dla Linuksa do kart sieciowych
10/100/1000Mbit z rodziny Intel(R) PRO/1000.

%prep
%setup -q -n %{_mod_name}-%{version}
cat > src/Makefile <<'EOF'
obj-m := e1000.o
e1000-objs := e1000_main.o e1000_82540.o e1000_82542.o e1000_82571.o e1000_82541.o \
e1000_82543.o e1000_ich8lan.o e1000_80003es2lan.o e1000_mac.o e1000_nvm.o e1000_phy.o \
e1000_manage.o e1000_param.o e1000_ethtool.o kcompat.o e1000_api.o
EOF

%build
%build_kernel_modules -C src -m %{_mod_name}

%install
rm -rf $RPM_BUILD_ROOT
%install_kernel_modules -m src/%{_mod_name} -d kernel/drivers/net -n %{_mod_name} -s current

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%files
%defattr(644,root,root,755)
%doc e1000.7 README ldistrib.txt
/etc/modprobe.d/%{_kernel_ver}/%{_mod_name}.conf
/lib/modules/%{_kernel_ver}/kernel/drivers/net/%{_mod_name}*.ko*
