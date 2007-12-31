#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	userspace	# don't build userspace programs
%bcond_with	verbose		# verbose build (V=1)
#

%if %{without kernel}
%undefine	with_dist_kernel
%endif

%define		rel	0.5
Summary:	Moxa
Name:		npreal2
Version:	1.14
Release:	%{rel}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://www.moxa.com/drivers/Nport/Admin/Linux/V1.14/%{name}_%{version}_Build_07062310.tgz
# Source0-md5:	fe81633814731d27dcc9d36e30343ab4
Patch0:		%{name}-paths.patch
URL:		http://www.moxa.com/
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.14}
BuildRequires:	rpmbuild(macros) >= 1.330
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
desc

%description -l pl
desc

%package -n kernel%{_alt_kernel}-char-npreal2
Summary:	Linux driver for npreal2
Summary(pl.UTF-8):	Sterownik dla Linuksa do npreal2
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel}
Requires(post,postun):	/sbin/depmod

%description -n kernel%{_alt_kernel}-char-npreal2
This is driver for npreal2 for Linux.

This package contains Linux module.

%description -n kernel%{_alt_kernel}-char-npreal2 -l pl.UTF-8
Sterownik dla Linuksa do npreal2.

Ten pakiet zawiera modul jadra Linuksa.

%prep
%setup -q -n tmp/moxa
%patch0 -p2

%build
%if %{with userspace}
%{__make} npreal2d tools \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -D_DEBUG_PRINT"
%endif

%if %{with kernel}
%build_kernel_modules -m npreal2
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sharedstatedir}/%{name}/driver}
install mxaddsvr	$RPM_BUILD_ROOT%{_bindir}
install mxdelsvr	$RPM_BUILD_ROOT%{_bindir}
install mxcfmat		$RPM_BUILD_ROOT%{_bindir}
install mxloadsvr	$RPM_BUILD_ROOT%{_bindir}
install mxsetsec	$RPM_BUILD_ROOT%{_bindir}
install mxmknod		$RPM_BUILD_ROOT%{_sharedstatedir}/%{name}/driver
install mxrmnod		$RPM_BUILD_ROOT%{_sharedstatedir}/%{name}/driver
install npreal2d	$RPM_BUILD_ROOT%{_sharedstatedir}/%{name}/driver
install npreal2d.cf	$RPM_BUILD_ROOT%{_sharedstatedir}/%{name}/driver
%endif

%if %{with kernel}
%install_kernel_modules -m npreal2 -d kernel/drivers/char -n npreal2 -s current
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-char-npreal2
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-char-npreal2
%depmod %{_kernel_ver}

%if %{with kernel}
%files -n kernel%{_alt_kernel}-char-npreal2
%defattr(644,root,root,755)
/etc/modprobe.d/%{_kernel_ver}/npreal2.conf
/lib/modules/%{_kernel_ver}/kernel/drivers/char/*.ko*
%endif

%if %{with userspace}
%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%dir %{_sharedstatedir}/%{name}
%dir %{_sharedstatedir}/%{name}/driver
%attr(755,root,root) %{_sharedstatedir}/%{name}/driver/mxmknod
%attr(755,root,root) %{_sharedstatedir}/%{name}/driver/mxrmnod
%attr(755,root,root) %{_sharedstatedir}/%{name}/driver/npreal2d
%{_sharedstatedir}/%{name}/driver/npreal2d.cf
%endif
