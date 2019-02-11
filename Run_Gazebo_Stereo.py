# This script is to run all the experiments in one program

import os
import subprocess
import time
import signal

SeqNameList = ['brick_wall_0.01', 'hard_wood_0.01', 'wood_wall_0.01'];
Result_root = '/mnt/DATA/tmp/Gazebo/SVO2/'
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


for iteration in range(0, Num_Repeating):

    # Experiment_dir = Result_root + Experiment_prefix + '_Round' + str(iteration + 1)
    Experiment_dir = Result_root + 'Round' + str(iteration + 1)
    cmd_mkdir = 'mkdir ' + Experiment_dir
    subprocess.call(cmd_mkdir, shell=True)

    FirstLoop = True
    for sn, sname in enumerate(SeqNameList):
        
        print bcolors.ALERT + "====================================================================" + bcolors.ENDC

        SeqName = SeqNameList[sn]
        print bcolors.ALERT + "Round: " + str(iteration + 1) + "; Seq: " + SeqName

        File_rosbag  = '/mnt/DATA/Datasets/GazeboMaze/' + SeqName + '.bag'

        # rosrun ORB_SLAM2 Mono PATH_TO_VOCABULARY PATH_TO_SETTINGS_FILE
        # cmd_slam   = str('LD_PRELOAD=/home/yipuzhao/svo_install_ws/install/lib/libgflags.so.2.2.0 roslaunch svo_ros gazebo_stereo_only.launch')
        cmd_slam   = str('roslaunch svo_ros gazebo_stereo_only.launch')
        cmd_record = str('rosbag record -O ' + Experiment_dir + '/' + SeqName + '_tf /tf __name:=rec_bag')
        cmd_rosbag = 'rosbag play ' + File_rosbag # + ' -r 0.3'
        print bcolors.WARNING + "cmd_slam: \n"   + cmd_slam   + bcolors.ENDC
        print bcolors.WARNING + "cmd_record: \n" + cmd_record + bcolors.ENDC
        print bcolors.WARNING + "cmd_rosbag: \n" + cmd_rosbag + bcolors.ENDC

        print bcolors.OKGREEN + "Launching SLAM" + bcolors.ENDC
        proc_slam = subprocess.Popen(cmd_slam, shell=True)
        # proc_slam = subprocess.Popen("exec " + cmd_slam, stdout=subprocess.PIPE, shell=True)

        print bcolors.OKGREEN + "Recording tf" + bcolors.ENDC
        proc_rec = subprocess.Popen(cmd_record, shell=True)
        # proc_rec = subprocess.Popen("exec " + cmd_record, stdout=subprocess.PIPE, shell=True)

        print bcolors.OKGREEN + "Sleeping for a few secs to wait for svo init" + bcolors.ENDC
        time.sleep(SleepTime)

        print bcolors.OKGREEN + "Launching rosbag" + bcolors.ENDC
        proc_bag = subprocess.call(cmd_rosbag, shell=True)

        print bcolors.OKGREEN + "Finished rosbag playback, kill the process" + bcolors.ENDC
        subprocess.call('rosnode kill /rec_bag', shell=True)
