# This script is to run all the experiments in one program

import os
import subprocess
import time
import signal


SeqStartTime = [60] 
SeqDuration = [130]
SeqNameList = ['2019-01-25-17-30_stereo'];

# * Batch Eval
# SeqStartTime = [0, 60, 230] 
# SeqDuration = [300, 130, 999]
# SeqNameList = ['2019-01-25-15-10_stereo', '2019-01-25-17-30_stereo', '2019-01-24-18-09_stereo'];

Result_root = '/mnt/DATA/tmp/Hololens/SVO2_Stereo_Speedx'

Playback_Rate_List = [1.0] # [1.0, 2.0, 3.0, 4.0, 5.0]; # 

# Optimal param for svo
Number_GF_List = [600];
# Number_GF_List =  [200, 300, 400, 600, 800, 1000, 1500, 2000];

Num_Repeating = 10 # 20 # 1 # 
SleepTime = 5

#----------------------------------------------------------------------------------------------------------------------
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ALERT = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

for pi, rate in enumerate(Playback_Rate_List):
    for ri, num_gf in enumerate(Number_GF_List):
    
        Experiment_prefix = 'ObsNumber_' + str(int(num_gf))

        for iteration in range(0, Num_Repeating):

            Experiment_dir = Result_root + str(rate) + '/' \
             + Experiment_prefix + '_Round' + str(iteration + 1)
            cmd_mkdir = 'mkdir -p ' + Experiment_dir
            subprocess.call(cmd_mkdir, shell=True)

            for sn, sname in enumerate(SeqNameList):
                
                subprocess.call('clear all', shell=True)
                print bcolors.ALERT + "====================================================================" + bcolors.ENDC

                SeqName = SeqNameList[sn] #+ '_blur_9'
                print bcolors.ALERT + "Round: " + str(iteration + 1) + "; Seq: " + SeqName

                File_rosbag  = '/mnt/DATA/Datasets/Hololens/BagFiles/' + SeqName + '.bag'
           
                # rosrun ORB_SLAM2 Mono PATH_TO_VOCABULARY PATH_TO_SETTINGS_FILE
                # cmd_slam     = str('LD_PRELOAD=~/svo_install_ws/install/lib/libgflags.so.2.2.0 roslaunch svo_ros ' + 'euroc_mono_lmk' + str(int(num_gf)) + '.launch')
                cmd_slam     = str('LD_PRELOAD=~/svo_install_ws/install/lib/libgflags.so.2.2.0 roslaunch svo_ros ' \
                    + ' general_stereo_only.launch num_tracks_per_frame:=' + str(int(num_gf)) \
                    + ' calib_prefix:=' + 'hololens' + ' cam0_topic:=' + '/left_cam/image_raw' \
                    + ' cam1_topic:=' + '/right_cam/image_raw' + ' cam_config:=' + 'vga')
                cmd_lmklog   = str('cp /mnt/DATA/svo_tmpLog_lmk.txt ' + Experiment_dir + '/' + SeqName + '_Log_lmk.txt')
                cmd_timelog  = str('cp /mnt/DATA/svo_tmpLog.txt ' + Experiment_dir + '/' + SeqName + '_Log.txt')
                cmd_tracklog = str('cp /mnt/DATA/svo_tmpTrack.txt ' + Experiment_dir + '/' + SeqName + '_AllFrameTrajectory.txt')
                cmd_rosbag = 'rosbag play ' + File_rosbag + ' -r ' + str(rate) # + ' -u 20' 

                print bcolors.WARNING + "cmd_slam: \n"   + cmd_slam   + bcolors.ENDC
                print bcolors.WARNING + "cmd_lmklog: \n" + cmd_lmklog + bcolors.ENDC
                print bcolors.WARNING + "cmd_rosbag: \n" + cmd_rosbag + bcolors.ENDC
                print bcolors.WARNING + "cmd_timelog: \n" + cmd_timelog + bcolors.ENDC
                print bcolors.WARNING + "cmd_tracklog: \n" + cmd_tracklog + bcolors.ENDC

                print bcolors.OKGREEN + "Launching SLAM" + bcolors.ENDC
                proc_slam = subprocess.Popen(cmd_slam, shell=True)
                # proc_slam = subprocess.Popen("exec " + cmd_slam, stdout=subprocess.PIPE, shell=True)

                print bcolors.OKGREEN + "Sleeping for a few secs to wait for svo init" + bcolors.ENDC
                time.sleep(SleepTime)

                print bcolors.OKGREEN + "Launching rosbag" + bcolors.ENDC
                proc_bag = subprocess.call(cmd_rosbag, shell=True)

                print bcolors.OKGREEN + "Finished rosbag playback, kill the process" + bcolors.ENDC
                # subprocess.call('rosnode kill /rec_bag', shell=True)
                subprocess.call('rosnode kill /svo', shell=True)
                # subprocess.call('pkill roslaunch', shell=True)
                # subprocess.call('pkill svo_node', shell=True)

                print bcolors.OKGREEN + "Sleeping for a few secs to wait for svo to quit" + bcolors.ENDC
                time.sleep(SleepTime)
                print bcolors.OKGREEN + "Copy the lmk log to result folder" + bcolors.ENDC
                subprocess.call(cmd_lmklog, shell=True)
                print bcolors.OKGREEN + "Copy the time log to result folder" + bcolors.ENDC
                subprocess.call(cmd_timelog, shell=True)
                print bcolors.OKGREEN + "Copy the track to result folder" + bcolors.ENDC
                subprocess.call(cmd_tracklog, shell=True)
