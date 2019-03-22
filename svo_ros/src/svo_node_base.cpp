#include "svo_ros/svo_node_base.h"

#include <gflags/gflags.h>
#include <glog/logging.h>
#include <ros/ros.h>
#include <svo/common/logging.h>
#include <vikit/params_helper.h>

namespace svo_ros {

void SvoNodeBase::initThirdParty(int argc, char **argv)
{
  google::InitGoogleLogging(argv[0]);
  google::ParseCommandLineFlags(&argc, &argv, true);
  google::InstallFailureSignalHandler();

  ros::init(argc, argv, "svo");
}

SvoNodeBase::SvoNodeBase()
: node_handle_(), private_node_handle_("~"), type_(
    vk::param<bool>(private_node_handle_, "pipeline_is_stereo", false) ?
        svo::PipelineType::kStereo : svo::PipelineType::kMono),
        svo_interface_(type_, node_handle_, private_node_handle_)
{
  if (svo_interface_.imu_handler_)
  {
    svo_interface_.subscribeImu();
  }
  svo_interface_.subscribeImage();
  svo_interface_.subscribeRemoteKey();
}

void SvoNodeBase::run()
{
  ros::spin();
  SVO_INFO_STREAM("SVO quit");

  //
      // Added by Yipu
  std::cout << "terminated! saving the time cost log!" << std::endl;
  svo_interface_.saveTimeLog("/mnt/DATA/svo_tmpLog.txt");
  std::cout << "move on saving the track log!" << std::endl;
  svo_interface_.saveAllFrameTrack("/mnt/DATA/svo_tmpTrack.txt");
  
  //
#ifdef LOGGING_LMK_LIFE
  std::cout << "move on saving the lmk log!" << std::endl;
  svo_interface_.saveLmkLog("/mnt/DATA/svo_tmpLog_lmk.txt");
#endif
  //
  
  svo_interface_.quit_ = true;
  SVO_INFO_STREAM("SVO terminated.\n");
}

}  // namespace svo_ros
