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
%if "%{_alt_kernel}" != "%{nil}"
%undefine	with_userspace
%endif
%if %{without userspace}
# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0
%endif
#
%define		rel	0.2
%define		pname	npreal2
Summary:	Moxa NPort Linux Real TTY driver
Summary(pl.UTF-8):	Sterownik Real TTY dla Linuksa do urządzeń Moxa NPort
Name:		%{pname}%{_alt_kernel}
Version:	1.16.15
Release:	%{rel}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://mtsc.moxa.com:8888/Software/DN/NPort/Driver/RealTTY/ver%{version}/%{pname}_%{version}_Build_10053117.tgz
# Source0-md5:	c1a22cd0d7a17ac8d883ad159bc684fc
Source1:	%{pname}.init
Source2:	%{pname}-modprobe.conf
Patch0:		%{pname}-paths.patch
Patch1:		%{pname}-pld.patch
URL:		http://www.moxa.com/
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.14}
BuildRequires:	rpmbuild(macros) >= 1.330
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Moxa NPort Linux Real TTY driver, which maps NPort serial port to host
tty port.

%description -l pl.UTF-8
Sterownik Real TTY dla Linuksa do urządzeń Moxa NPort. Pozwala
przypisać port szeregowy urządzenia NPort do portu tty w systemie.

%package -n kernel%{_alt_kernel}-char-npreal2
Summary:	Linux Real TTY driver for Moxa NPort devices
Summary(pl.UTF-8):	Sterownik Real TTY dla Linuksa do urządzeń Moxa NPort
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel}
Requires(post,postun):	/sbin/depmod

%description -n kernel%{_alt_kernel}-char-npreal2
Moxa NPort Linux Real TTY driver, which maps NPort serial port to host
tty port.

This package contains Linux module.

%description -n kernel%{_alt_kernel}-char-npreal2 -l pl.UTF-8
Sterownik Real TTY dla Linuksa do urządzeń Moxa NPort. Pozwala
przypisać port szeregowy urządzenia NPort do portu tty w systemie.

Ten pakiet zawiera modul jadra Linuksa.

%prep
%setup -q -n tmp/moxa
%patch0 -p2
%patch1 -p2

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
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_sharedstatedir}/%{pname}/driver,%{_sysconfdir}/rc.d/init.d}
install mxaddsvr	$RPM_BUILD_ROOT%{_bindir}
install mxdelsvr	$RPM_BUILD_ROOT%{_bindir}
install mxcfmat		$RPM_BUILD_ROOT%{_bindir}
install mxloadsvr	$RPM_BUILD_ROOT%{_bindir}
install mxsetsec	$RPM_BUILD_ROOT%{_bindir}
install mxmknod		$RPM_BUILD_ROOT%{_sharedstatedir}/%{pname}/driver
install mxrmnod		$RPM_BUILD_ROOT%{_sharedstatedir}/%{pname}/driver
install npreal2d.cf	$RPM_BUILD_ROOT%{_sharedstatedir}/%{pname}
install npreal2d	$RPM_BUILD_ROOT%{_sbindir}/npreal2d
install %{SOURCE1}	$RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/npreal2
%endif

%if %{with kernel}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d
%install_kernel_modules -m npreal2 -d kernel/drivers/char -n npreal2 -s current
cat %{SOURCE2} >> $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/%{_kernel_ver}/npreal2.conf
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-char-npreal2
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-char-npreal2
%depmod %{_kernel_ver}

%post
/sbin/chkconfig --add npreal2

%preun
if [ "$1" = "0" ]; then
	%service -q npreal2 stop
	/sbin/chkconfig --del npreal2
fi


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
%dir %{_sharedstatedir}/%{pname}
%dir %{_sharedstatedir}/%{pname}/driver
%attr(755,root,root) %{_sharedstatedir}/%{pname}/driver/mxmknod
%attr(755,root,root) %{_sharedstatedir}/%{pname}/driver/mxrmnod
%attr(755,root,root) %{_sbindir}/npreal2d
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sharedstatedir}/%{pname}/npreal2d.cf

%attr(754,root,root) /etc/rc.d/init.d/npreal2
%endif
