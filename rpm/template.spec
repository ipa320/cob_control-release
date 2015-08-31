Name:           ros-indigo-cob-trajectory-controller
Version:        0.6.10
Release:        0%{?dist}
Summary:        ROS cob_trajectory_controller package

Group:          Development/Libraries
License:        LGPL
URL:            http://ros.org/wiki/cob_trajectory_controller
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-indigo-actionlib
Requires:       ros-indigo-cob-srvs
Requires:       ros-indigo-control-msgs
Requires:       ros-indigo-dynamic-reconfigure
Requires:       ros-indigo-roscpp
Requires:       ros-indigo-sensor-msgs
Requires:       ros-indigo-std-msgs
Requires:       ros-indigo-std-srvs
Requires:       ros-indigo-trajectory-msgs
BuildRequires:  ros-indigo-actionlib
BuildRequires:  ros-indigo-catkin
BuildRequires:  ros-indigo-cob-srvs
BuildRequires:  ros-indigo-control-msgs
BuildRequires:  ros-indigo-dynamic-reconfigure
BuildRequires:  ros-indigo-roscpp
BuildRequires:  ros-indigo-sensor-msgs
BuildRequires:  ros-indigo-std-msgs
BuildRequires:  ros-indigo-std-srvs
BuildRequires:  ros-indigo-trajectory-msgs

%description
This package provides a trajectory controller which controlls velocities for a
chain of joints. This controller can be used e.g. with
[[schunk_powercube_chain]].

%prep
%setup -q

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/indigo/setup.sh" ]; then . "/opt/ros/indigo/setup.sh"; fi
mkdir -p obj-%{_target_platform} && cd obj-%{_target_platform}
%cmake .. \
        -UINCLUDE_INSTALL_DIR \
        -ULIB_INSTALL_DIR \
        -USYSCONF_INSTALL_DIR \
        -USHARE_INSTALL_PREFIX \
        -ULIB_SUFFIX \
        -DCMAKE_INSTALL_PREFIX="/opt/ros/indigo" \
        -DCMAKE_PREFIX_PATH="/opt/ros/indigo" \
        -DSETUPTOOLS_DEB_LAYOUT=OFF \
        -DCATKIN_BUILD_BINARY_PACKAGE="1" \

make %{?_smp_mflags}

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/indigo/setup.sh" ]; then . "/opt/ros/indigo/setup.sh"; fi
cd obj-%{_target_platform}
make %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
/opt/ros/indigo

%changelog
* Mon Aug 31 2015 Alexander Bubeck <aub@ipa.fhg.de> - 0.6.10-0
- Autogenerated by Bloom

* Tue Aug 25 2015 Alexander Bubeck <aub@ipa.fhg.de> - 0.6.9-0
- Autogenerated by Bloom

* Mon Jun 22 2015 Alexander Bubeck <aub@ipa.fhg.de> - 0.6.8-5
- Autogenerated by Bloom

* Sun Jun 21 2015 Alexander Bubeck <aub@ipa.fhg.de> - 0.6.8-4
- Autogenerated by Bloom

* Sat Jun 20 2015 Alexander Bubeck <aub@ipa.fhg.de> - 0.6.8-3
- Autogenerated by Bloom

* Sat Jun 20 2015 Alexander Bubeck <aub@ipa.fhg.de> - 0.6.8-2
- Autogenerated by Bloom

* Wed Jun 17 2015 Alexander Bubeck <aub@ipa.fhg.de> - 0.6.8-1
- Autogenerated by Bloom

* Wed Jun 17 2015 Alexander Bubeck <aub@ipa.fhg.de> - 0.6.8-0
- Autogenerated by Bloom

* Wed Jun 17 2015 Alexander Bubeck <aub@ipa.fhg.de> - 0.6.7-0
- Autogenerated by Bloom

* Thu Dec 18 2014 Alexander Bubeck <aub@ipa.fhg.de> - 0.6.6-0
- Autogenerated by Bloom

* Thu Dec 18 2014 Alexander Bubeck <aub@ipa.fhg.de> - 0.6.5-0
- Autogenerated by Bloom

* Tue Dec 16 2014 Alexander Bubeck <aub@ipa.fhg.de> - 0.6.4-0
- Autogenerated by Bloom

