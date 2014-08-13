Name:		ivi-sanity-suite
Summary:	Sanity suite for Tizen IVI
Version:	1.1
Release:	0
License:	GPL-2.0
Group:		Development/Testing
Source:		%{name}-%{version}.tar.gz
Source1001:	%{name}.manifest
BuildArch:	noarch
Requires:	testkit-lite
Requires:	common-suite-launcher

%description
The ivi-sanity-suite is the acceptance test to validate the Tizen IVI image

%package -n %{name}-GUI
Summary:        GUI Sanity Case
Group:          Development/Testing
Requires:	testkit-lite
Requires:	fMBT


%description -n %{name}-GUI
IVI sanity GUI testing case to validate launch of homescreen and key apps.


%prep
%setup -q
cp %{SOURCE1001} .


%build


%install
install -d %{buildroot}/%{_datadir}/tests/%{profile}/%{name}
install -m 0755 runtest %{buildroot}/%{_datadir}/tests/%{profile}/%{name}
install -m 0755 process_check/prs_checker %{buildroot}/%{_datadir}/tests/%{profile}/%{name}
install -m 0644 process_check/testkit.xml %{buildroot}/%{_datadir}/tests/%{profile}/%{name}
install -m 0644 LICENSE %{buildroot}/%{_datadir}/tests/%{profile}/%{name}
install -m 0644 process_check/README %{buildroot}/%{_datadir}/tests/%{profile}/%{name}

install -d %{buildroot}/%{_datadir}/tests/ivi/%{name}/GUI
install -m 0755 GUI/runtest.sh %{buildroot}/%{_datadir}/tests/ivi/%{name}/GUI
install -m 0755 GUI/ivi_apps.py %{buildroot}/%{_datadir}/tests/ivi/%{name}/GUI
install -m 0755 GUI/ivi_tests.py %{buildroot}/%{_datadir}/tests/ivi/%{name}/GUI
install -m 0644 GUI/testkit.xml %{buildroot}/%{_datadir}/tests/ivi/%{name}/GUI
install -m 0644 GUI/README %{buildroot}/%{_datadir}/tests/ivi/%{name}/GUI
install -m 0644 LICENSE %{buildroot}/%{_datadir}/tests/ivi/%{name}/GUI
cp -r GUI/ivi-tests_pics %{buildroot}/%{_datadir}/tests/ivi/%{name}/GUI


%files
%manifest %{name}.manifest
%defattr(-,root,root)
%{_datadir}/tests/ivi/%{name}/runtest
%{_datadir}/tests/ivi/%{name}/prs_checker
%{_datadir}/tests/ivi/%{name}/testkit.xml
%{_datadir}/tests/ivi/%{name}/LICENSE
%{_datadir}/tests/ivi/%{name}/README


%files -n %{name}-GUI
%{_datadir}/tests/ivi/%{name}/GUI
