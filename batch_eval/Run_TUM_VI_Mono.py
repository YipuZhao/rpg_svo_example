# This script is to run all the experiments in one program

import os
import subprocess
import time
import signal

# SeqNameList = ['room1_512_16', 'not_exist'];
SeqNameList = ['room1_512_16', 'room2_512_16', 'room3_512_16', 'room4_512_16', 'room5_512_16', 'room6_512_16', 'not_exist'];

Result_root = '/mnt/DATA/tmp/TUM_VI/SVO2_Mono_Baseline/'

Number_GF_List = [400, 600, 800, 1000, 1500, 2000]; # [400]; # 

Num_Repeating = 10 # 20 #  5 # 
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

for ri, num_gf in enumerate(Number_GF_List):
    
    Experiment_prefix = 'ObsNumber_' + str(int(num_gf))

    for iteration in range(0, Num_Repeating):

        Experiment_dir = Result_root + Experiment_prefix + '_Round' + str(iteration + 1)
        cmd_mkdir = 'mkdir ' + Experiment_dir
        subprocess.call(cmd_mkdir, shell=True)

        for sn, sname in enumerate(SeqNameList):
            
            print bcolors.ALERT + "====================================================================" + bcolors.ENDC

            SeqName = SeqNameList[sn] #+ '_blur_9'
            print bcolors.ALERT + "Round: " + str(iteration + 1) + "; Seq: " + SeqName

            File_rosbag  = '/mnt/DATA/Datasets/TUM_VI/BagFiles/dataset-' + SeqName + '_small_chunks.bag'

            # rosrun ORB_SLAM2 Mono PATH_TO_VOCABULARY PATH_TO_SETTINGS_FILE
            cmd_slam   = str('LD_PRELOAD=~/svo_install_ws/install/lib/libgflags.so.2.2.1 roslaunch svo_ros tum_vi_mono_only.launch ' \
                + 'num_tracks_per_frame:=' + str(int(num_gf)))
            cmd_timelog = str('cp /home/yipuzhao/svo_install_overlay_ws/tmpLog.txt ' + Experiment_dir + '/' + SeqName + '_Log.txt')
            cmd_tracklog = str('cp /home/yipuzhao/svo_install_overlay_ws/tmpTrack.txt ' + Experiment_dir + '/' + SeqName + '_AllFrameTrajectory.txt')
            cmd_rosbag = 'rosbag play ' + File_rosbag # + ' -u 30' # + ' -r 0.3'
            print bcolors.WARNING + "cmd_slam: \n"   + cmd_slam   + bcolors.ENDC
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
            subprocess.call('rosnode kill /svo', shell=True)
            # subprocess.call('pkill roslaunch', shell=True)
            # subprocess.call('pkill svo_node', shell=True)

            print bcolors.OKGREEN + "Sleeping for a few secs to wait for svo to quit" + bcolors.ENDC
            time.sleep(SleepTime)
            print bcolors.OKGREEN + "Copy the time log to result folder" + bcolors.ENDC
            subprocess.call(cmd_timelog, shell=True)
            print bcolors.OKGREEN + "Copy the track to result folder" + bcolors.ENDC
            subprocess.call(cmd_tracklog, shell=True)
