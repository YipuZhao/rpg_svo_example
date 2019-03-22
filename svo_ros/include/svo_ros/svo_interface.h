#pragma once

#include <thread>

#include <ros/ros.h>
#include <std_msgs/String.h>    // user-input
#include <sensor_msgs/Image.h>
#include <sensor_msgs/Imu.h>


#include <svo/common/types.h>
#include <svo/common/camera_fwd.h>
#include <svo/common/transformation.h>

#include <vector>

using namespace std;


// #define LOGGING_LMK_LIFE


namespace svo {

// forward declarations
class FrameHandlerBase;
class Visualizer;
class ImuHandler;
class BackendInterface;
class BackendVisualizer;

enum class PipelineType {
  kMono,
  kStereo,
  kArray
};



class timeLog {
public:
  timeLog(const double &t0, const double &t1, const double &t2) {
    time_stamp = t0;
    time_proc = t1;
    time_total = t2;
  };
  
  timeLog(const double &t0, const double &t1, const double &t2, const size_t &n1, const size_t &n2) {
    time_stamp = t0;
    time_proc = t1;
    time_total = t2;
    num_poses = n1;
    num_lmks = n2;
  };

  double time_stamp;
  double time_proc;
  double time_total;
  //
  size_t num_poses;
  size_t num_lmks;
};

class trackLog {
public:
  trackLog(const double &timeStamp_, const double &Tx_, const double &Ty_, const double &Tz_, 
	   const double &Qx_, const double &Qy_, const double &Qz_, const double &Qw_) {
    //
    time_stamp = timeStamp_;
    position(0) = Tx_;
    position(1) = Ty_;
    position(2) = Tz_;
    orientation(0) = Qx_;
    orientation(1) = Qy_;
    orientation(2) = Qz_;
    orientation(3) = Qw_;
  };

  double time_stamp;
    // Orientation
  // Take a vector from the world frame to
  // the IMU (body) frame.
  Eigen::Vector4d orientation;

  // Position of the IMU (body) frame
  // in the world frame.
  Eigen::Vector3d position;
};


/// SVO Interface
class SvoInterface
{
public:

  // ROS subscription and publishing.
  ros::NodeHandle nh_;
  ros::NodeHandle pnh_;
  PipelineType pipeline_type_;
  ros::Subscriber sub_remote_key_;
  std::string remote_input_;
  std::unique_ptr<std::thread> imu_thread_;
  std::unique_ptr<std::thread> image_thread_;

  // SVO modules.
  std::shared_ptr<FrameHandlerBase> svo_;
  std::shared_ptr<Visualizer> visualizer_;
  std::shared_ptr<ImuHandler> imu_handler_;
  std::shared_ptr<BackendInterface> backend_interface_;
  std::shared_ptr<BackendVisualizer> backend_visualizer_;

  CameraBundlePtr ncam_;

  // Parameters
  bool set_initial_attitude_from_gravity_ = true;

  // System state.
  bool quit_ = false;
  bool idle_ = false;
  bool automatic_reinitialization_ = false;

  SvoInterface(const PipelineType& pipeline_type,
          const ros::NodeHandle& nh,
          const ros::NodeHandle& private_nh);

  virtual ~SvoInterface();

  // Processing
  void processImageBundle(
      const std::vector<cv::Mat>& images,
      int64_t timestamp_nanoseconds);

  void setImuPrior(const int64_t timestamp_nanoseconds);

  void publishResults(
      const std::vector<cv::Mat>& images,
      const int64_t timestamp_nanoseconds);

  // Subscription and callbacks
  void monoCallback(const sensor_msgs::ImageConstPtr& msg);
  void stereoCallback(
      const sensor_msgs::ImageConstPtr& msg0,
      const sensor_msgs::ImageConstPtr& msg1);
  void imuCallback(const sensor_msgs::ImuConstPtr& imu_msg);
  void inputKeyCallback(const std_msgs::StringConstPtr& key_input);


  // These functions are called before and after monoCallback or stereoCallback.
  // a derived class can implement some additional logic here.
  virtual void imageCallbackPreprocessing(int64_t timestamp_nanoseconds) {}
  virtual void imageCallbackPostprocessing() {}

  void subscribeImu();
  void subscribeImage();
  void subscribeRemoteKey();

  void imuLoop();
  void monoLoop();
  void stereoLoop();


  //
  
  void saveLmkLog(const std::string &filename);
  
  // save the time cost of SVO2
  vector<timeLog> logTimeCost;

  void saveTimeLog(const std::string &filename);
  
  std::vector<trackLog> logFramePose;

  void saveAllFrameTrack(const std::string &filename);

};

} // namespace svo
