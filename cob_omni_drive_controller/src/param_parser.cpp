#include <cob_omni_drive_controller/UndercarriageCtrlGeomROS.h>
#include <urdf/model.h>
#include <angles/angles.h>
#include <XmlRpcException.h>

class MergedXmlRpcStruct : public XmlRpc::XmlRpcValue{
    MergedXmlRpcStruct(const XmlRpc::XmlRpcValue& a) :XmlRpc::XmlRpcValue(a){ assertStruct(); }
public:
    MergedXmlRpcStruct(){ assertStruct(); }
    MergedXmlRpcStruct(const XmlRpc::XmlRpcValue& a, const MergedXmlRpcStruct &b, bool recursive= true) :XmlRpc::XmlRpcValue(a){
        assertStruct();

        for(ValueStruct::const_iterator it = b._value.asStruct->begin(); it != b._value.asStruct->end(); ++it){
            std::pair<XmlRpc::XmlRpcValue::iterator,bool> res =  _value.asStruct->insert(*it);

            if(recursive && !res.second && res.first->second.getType() == XmlRpc::XmlRpcValue::TypeStruct && it->second.getType() == XmlRpc::XmlRpcValue::TypeStruct){
                res.first->second = MergedXmlRpcStruct(res.first->second, it->second); // recursive struct merge with implicit cast
            }
        }


    }
};

template<typename T> T read_typed(XmlRpc::XmlRpcValue &val){
    return val;
}
template<> double read_typed(XmlRpc::XmlRpcValue &val){
    if(val.getType() ==  XmlRpc::XmlRpcValue::TypeInt) return read_typed<int>(val);
    return val;
}

template<typename T> bool read_optional(T& val, const std::string &name, XmlRpc::XmlRpcValue &wheel){
    try{
        if(wheel.hasMember(name)){
           val = read_typed<T>(wheel[name]);
           return true;
        }
    }catch(XmlRpc::XmlRpcException &e){
        ROS_ERROR_STREAM("Could not access '" << name << "', reason: " << e.getMessage());
    }
    return false;
}

template<typename T> bool read_with_default(T& val, const std::string &name, XmlRpc::XmlRpcValue &wheel, const T& def){
    if(!read_optional(val, name, wheel)){
        val = def;
        return false;
    }
    return true;
}

template<typename T> bool read(T& val, const std::string &name, XmlRpc::XmlRpcValue &wheel){
    if(!read_optional(val, name, wheel)){
        ROS_ERROR_STREAM("Parameter not found: " << name);
        return false;
    }
    return true;
}

bool parseCtrlParams(CtrlParams & params, XmlRpc::XmlRpcValue &wheel){
    double deg;
    read_with_default(deg, "steer_neutral_position", wheel, 0.0);
    params.dWheelNeutralPos = angles::from_degrees(deg);

    read_with_default(params.dMaxSteerRateRadpS, "max_steer_rate", wheel, 0.0);
    read_with_default(params.dMaxDriveRateRadpS, "max_drive_rate", wheel, 0.0);
    
    return true;
}

bool parsePosCtrlParams(PosCtrlParams & params, XmlRpc::XmlRpcValue &wheel){
    if(!wheel.hasMember("steer_ctrl")){
        ROS_ERROR_STREAM("steer_ctrl not found");
        return false;
    }
    XmlRpc::XmlRpcValue &steer = wheel["steer_ctrl"];

    return read(params.dSpring, "spring", steer)
        && read(params.dDamp, "damp", steer)
        && read(params.dVirtM, "virt_mass", steer)
        && read(params.dDPhiMax, "d_phi_max", steer)
        && read(params.dDDPhiMax, "dd_phi_max", steer);
}

bool parseWheelGeom(WheelGeom & geom, XmlRpc::XmlRpcValue &wheel, MergedXmlRpcStruct &merged, urdf::Model* model){

    read_with_default(geom.steer_name, "steer", wheel, std::string());
    read_with_default(geom.drive_name, "drive", wheel, std::string());
    read_with_default(geom.dSteerDriveCoupling, "steer_drive_coupling", wheel, 0.0);

    boost::shared_ptr<const urdf::Joint> steer_joint;
    urdf::Vector3 steer_pos;

    if(model && !geom.steer_name.empty()){
        steer_joint = model->getJoint(geom.steer_name);
        if(steer_joint){
            steer_pos = steer_joint->parent_to_joint_origin_transform.position;
        }
    }

    if(!read_optional(steer_pos.x, "x_pos", wheel) && !steer_joint){
        ROS_ERROR_STREAM("Could not parse x_pos");
        return false;
    }

    if(!read_optional(steer_pos.y, "y_pos", wheel) && !steer_joint){
        ROS_ERROR_STREAM("Could not parse y_pos");
        return false;
    }

    if(!read_optional(steer_pos.z, "wheel_radius", merged) && !steer_joint){
        ROS_ERROR_STREAM("Could not parse wheel_radius");
        return false;
    }

    if(steer_pos.z == 0){
        ROS_ERROR_STREAM("wheel_radius must be non-zero");
        return false;
    }

    geom.dWheelXPosMM = steer_pos.x * 1000;
    geom.dWheelYPosMM = steer_pos.y * 1000;
    geom.dRadiusWheelMM = fabs(steer_pos.z * 1000);

    double offset = 0;

    if(!read_optional(offset, "wheel_offset", merged)){
        boost::shared_ptr<const urdf::Joint> drive_joint;
        if(model && !geom.drive_name.empty()){
            drive_joint = model->getJoint(geom.drive_name);
        }
        if(drive_joint){
            const urdf::Vector3& pos = drive_joint->parent_to_joint_origin_transform.position;
            offset = sqrt(pos.x*pos.x + pos.y * pos.y);
        }else{
            ROS_ERROR_STREAM("Could not parse wheel_offset");
            return false;
        }
    }
    geom.dDistSteerAxisToDriveWheelMM = offset * 1000;
    return true;
}

template<typename W> bool parseWheel(W & params, XmlRpc::XmlRpcValue &wheel, MergedXmlRpcStruct &merged, urdf::Model* model);

template<> bool parseWheel(UndercarriageGeom::WheelParams & params, XmlRpc::XmlRpcValue &wheel, MergedXmlRpcStruct &merged, urdf::Model* model){
    return parseWheelGeom(params.geom, wheel, merged, model);
}

template<> bool parseWheel(UndercarriageDirectCtrl::WheelParams & params, XmlRpc::XmlRpcValue &wheel, MergedXmlRpcStruct &merged, urdf::Model* model){
    return parseWheelGeom(params.geom, wheel, merged, model) && parseCtrlParams(params.ctrl, merged);
}

template<> bool parseWheel(UndercarriageCtrl::WheelParams & params, XmlRpc::XmlRpcValue &wheel, MergedXmlRpcStruct &merged, urdf::Model* model){
    return parseWheelGeom(params.geom, wheel, merged, model) && parseCtrlParams(params.ctrl, merged) && parsePosCtrlParams(params.pos_ctrl, merged);
}

bool make_wheel_struct(XmlRpc::XmlRpcValue &wheel_list){
    if(wheel_list.getType() ==  XmlRpc::XmlRpcValue::TypeArray){
        XmlRpc::XmlRpcValue new_stuct;
        for(size_t i = 0; i < wheel_list.size(); ++i){
            new_stuct[boost::lexical_cast<std::string>(i)] = wheel_list[i];
        }
        wheel_list = new_stuct;
    }else if(wheel_list.getType() !=  XmlRpc::XmlRpcValue::TypeStruct){
        return false;
    }

    return wheel_list.size() > 0;
}

template<typename W> bool parseWheels(std::vector<W> &wheel_params, const ros::NodeHandle &nh, bool read_urdf){

    urdf::Model model;

    std::string description_name;
    bool has_model = read_urdf && nh.searchParam("robot_description", description_name) &&  model.initParam(description_name);

    MergedXmlRpcStruct defaults;
    nh.getParam("defaults", defaults);

    // clear vector in case of reinititialization
    wheel_params.clear();

    XmlRpc::XmlRpcValue wheel_list;
    if (!nh.getParam("wheels", wheel_list)){
        ROS_ERROR("List of wheels not found");
        return false;
    }

    if (!make_wheel_struct(wheel_list)){
        ROS_ERROR("List of wheels is invalid");
        return false;
    }

    for(XmlRpc::XmlRpcValue::iterator it = wheel_list.begin(); it != wheel_list.end(); ++it){

        W params;
        MergedXmlRpcStruct merged(it->second, defaults);

        if(!parseWheel(params, it->second, merged, has_model?&model:0)){
            return false;
        }

        wheel_params.push_back(params);
    }
    return !wheel_params.empty();
}

namespace cob_omni_drive_controller{

bool parseWheelParams(std::vector<UndercarriageGeom::WheelParams> &params, const ros::NodeHandle &nh, bool read_urdf /* = true*/){
    return parseWheels(params, nh, read_urdf);
}
bool parseWheelParams(std::vector<UndercarriageDirectCtrl::WheelParams> &params, const ros::NodeHandle &nh, bool read_urdf /* = true*/){
    return parseWheels(params, nh, read_urdf);
}
bool parseWheelParams(std::vector<UndercarriageCtrl::WheelParams> &params, const ros::NodeHandle &nh, bool read_urdf /* = true*/){
    return parseWheels(params, nh, read_urdf);
}


}
