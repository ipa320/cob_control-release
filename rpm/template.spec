Name:           ros-melodic-cob-cartesian-controller
Version:        0.7.7
Release:        1%{?dist}
Summary:        ROS cob_cartesian_controller package

Group:          Development/Libraries
License:        Apache 2.0
Source0:        %{name}-%{version}.tar.gz

Requires:       boost-devel
Requires:       boost-python2-devel
Requires:       boost-python3-devel
Requires:       ros-melodic-actionlib
Requires:       ros-melodic-actionlib-msgs
Requires:       ros-melodic-cob-frame-tracker
Requires:       ros-melodic-cob-srvs
Requires:       ros-melodic-cob-twist-controller
Requires:       ros-melodic-geometry-msgs
Requires:       ros-melodic-message-runtime
Requires:       ros-melodic-robot-state-publisher
Requires:       ros-melodic-roscpp
Requires:       ros-melodic-rospy
Requires:       ros-melodic-rviz
Requires:       ros-melodic-std-msgs
Requires:       ros-melodic-std-srvs
Requires:       ros-melodic-tf
Requires:       ros-melodic-topic-tools
Requires:       ros-melodic-visualization-msgs
Requires:       ros-melodic-xacro
BuildRequires:  boost-devel
BuildRequires:  boost-python2-devel
BuildRequires:  boost-python3-devel
BuildRequires:  ros-melodic-actionlib
BuildRequires:  ros-melodic-actionlib-msgs
BuildRequires:  ros-melodic-catkin
BuildRequires:  ros-melodic-cob-srvs
BuildRequires:  ros-melodic-geometry-msgs
BuildRequires:  ros-melodic-message-generation
BuildRequires:  ros-melodic-roscpp
BuildRequires:  ros-melodic-roslint
BuildRequires:  ros-melodic-std-msgs
BuildRequires:  ros-melodic-std-srvs
BuildRequires:  ros-melodic-tf
BuildRequires:  ros-melodic-visualization-msgs

%description
This package provides nodes that broadcast tf-frames along various (model-based)
Cartesian paths (e.g. Linear, Circular). The tf-frames are interpolated using a
given velocity profile (e.g. Ramp, Sinoid) and can be used as targets for the
cob_frame_tracker/cob_twist_controller.

%prep
%setup -q

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/melodic/setup.sh" ]; then . "/opt/ros/melodic/setup.sh"; fi
mkdir -p obj-%{_target_platform} && cd obj-%{_target_platform}
%cmake .. \
        -UINCLUDE_INSTALL_DIR \
        -ULIB_INSTALL_DIR \
        -USYSCONF_INSTALL_DIR \
        -USHARE_INSTALL_PREFIX \
        -ULIB_SUFFIX \
        -DCMAKE_INSTALL_LIBDIR="lib" \
        -DCMAKE_INSTALL_PREFIX="/opt/ros/melodic" \
        -DCMAKE_PREFIX_PATH="/opt/ros/melodic" \
        -DSETUPTOOLS_DEB_LAYOUT=OFF \
        -DCATKIN_BUILD_BINARY_PACKAGE="1" \

make %{?_smp_mflags}

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/melodic/setup.sh" ]; then . "/opt/ros/melodic/setup.sh"; fi
cd obj-%{_target_platform}
make %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
/opt/ros/melodic

%changelog
* Tue Aug 06 2019 Felix Messmer <felixmessmer@gmail.com> - 0.7.7-1
- Autogenerated by Bloom

