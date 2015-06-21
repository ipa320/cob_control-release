Name:           ros-indigo-cob-twist-controller
Version:        0.6.8
Release:        4%{?dist}
Summary:        ROS cob_twist_controller package

Group:          Development/Libraries
License:        LGPL
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-indigo-dynamic-reconfigure
Requires:       ros-indigo-geometry-msgs
Requires:       ros-indigo-kdl-conversions
Requires:       ros-indigo-kdl-parser
Requires:       ros-indigo-nav-msgs
Requires:       ros-indigo-orocos-kdl
Requires:       ros-indigo-roscpp
Requires:       ros-indigo-rospy
Requires:       ros-indigo-sensor-msgs
Requires:       ros-indigo-tf
Requires:       ros-indigo-tf-conversions
Requires:       ros-indigo-visualization-msgs
BuildRequires:  ros-indigo-catkin
BuildRequires:  ros-indigo-cmake-modules
BuildRequires:  ros-indigo-dynamic-reconfigure
BuildRequires:  ros-indigo-geometry-msgs
BuildRequires:  ros-indigo-kdl-conversions
BuildRequires:  ros-indigo-kdl-parser
BuildRequires:  ros-indigo-nav-msgs
BuildRequires:  ros-indigo-orocos-kdl
BuildRequires:  ros-indigo-roscpp
BuildRequires:  ros-indigo-sensor-msgs
BuildRequires:  ros-indigo-tf
BuildRequires:  ros-indigo-tf-conversions
BuildRequires:  ros-indigo-visualization-msgs

%description
The cob_twist_controller package

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
* Sun Jun 21 2015 Felix Messmer <fxm@ipa.fhg.de> - 0.6.8-4
- Autogenerated by Bloom

* Sat Jun 20 2015 Felix Messmer <fxm@ipa.fhg.de> - 0.6.8-3
- Autogenerated by Bloom

* Sat Jun 20 2015 Felix Messmer <fxm@ipa.fhg.de> - 0.6.8-2
- Autogenerated by Bloom

* Wed Jun 17 2015 Felix Messmer <fxm@ipa.fhg.de> - 0.6.8-1
- Autogenerated by Bloom

* Wed Jun 17 2015 Felix Messmer <fxm@ipa.fhg.de> - 0.6.8-0
- Autogenerated by Bloom

* Wed Jun 17 2015 Felix Messmer <fxm@ipa.fhg.de> - 0.6.7-0
- Autogenerated by Bloom

* Thu Dec 18 2014 Felix Messmer <fxm@ipa.fhg.de> - 0.6.6-0
- Autogenerated by Bloom

* Thu Dec 18 2014 Felix Messmer <fxm@ipa.fhg.de> - 0.6.5-0
- Autogenerated by Bloom

* Tue Dec 16 2014 Felix Messmer <fxm@ipa.fhg.de> - 0.6.4-0
- Autogenerated by Bloom

