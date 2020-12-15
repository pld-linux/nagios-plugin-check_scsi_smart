%define		plugin	check_scsi_smart
Summary:	Nagios plugin to check the state of disk using SMART data
Name:		nagios-plugin-%{plugin}
Version:	1.2.3
Release:	1
License:	GPL v2
Group:		Base
Source0:	https://github.com/spjmurray/nagios-plugin-check-scsi-smart/archive/v%{version}.tar.gz
# Source0-md5:	6a9694a20fe3eb8ea380c81fbba62de8
URL:		https://github.com/spjmurray/nagios-plugin-check-scsi-smart
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		plugindir	%{_libdir}/nagios/plugins
%define		_sysconfdir	/etc/nagios/plugins

%description
Uses SCSI commands to tunnel SMART checks to ATA hard drives. Unlike
the venerable check_ide_smart check this will work on all modern
devices even those behind SAS HBAs or expanders. It will also monitor
for SMART error logs which may indicate failure when base SMART
attributes do not.

%prep
%setup -q -n nagios-plugin-check-scsi-smart-%{version}

%build
%{__make} all \
	CXX="%{__cxx}" \
	CXXFLAGS="%{rpmcppflags} %{rpmcxxflags}" \
	LDFLAGS="%{rpmldflags}"

cat > nagios.cfg <<'EOF'
# Usage:
# %{plugin}
define command {
	command_name	%{plugin}
	command_line	%{plugindir}/%{plugin}
}

define service {
	use			generic-service
	name			SCSI S.M.A.R.T.
	service_description	scsi_smart
	register		0

	normal_check_interval   15
	notification_interval   300

	check_command		check_scsi_smart
}
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{plugindir}}

cp -p %{plugin} $RPM_BUILD_ROOT%{plugindir}/%{plugin}
cp -a nagios.cfg $RPM_BUILD_ROOT%{_sysconfdir}/%{plugin}.cfg

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{plugin}.cfg
%attr(755,root,root) %{plugindir}/%{plugin}
