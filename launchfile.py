# Author: Anoop Aroor
# This is a python launch file to control and launch ros nodes for Semaforr project
# Each ros node must has a launch file containing parameters that remain constant though different experiments
# Dynamic parameters that changes with different experiments are added here

import rospy
import time
import subprocess

def experiment():
    project_home = "/home/anoop/catkin_ws/src"
    menge_path = project_home+"/examples/core"
    semaforr_path = project_home+"/semaforr"

    map_folder = menge_path+"/"+map_name
    map_xml = menge_path+"/"+map_name+".xml"

    #menge files for semaforr
    map_config = map_folder+"/"+map_name+"S.xml"
    map_dimensions = map_folder+"/dimensions.conf"
    target_set = map_folder+"/targets/" + target_file_name

    print target_set
    print map_config
    print map_xml
    print map_dimensions
    print log_name
    #start roscore
    roscore = subprocess.Popen(['roscore'])
    time.sleep(1)

    # start menge simulator
    menge_sim_process = subprocess.Popen(['rosrun','menge_sim','menge_sim','-p',map_xml])
    print "waiting,,"
    time.sleep(10)

    log_file = open(log_name,"w")
    log_process = subprocess.Popen(['rostopic','echo','/decision_log'],stdout=log_file)

    # start semaforr
    semaforr_process = subprocess.Popen(['rosrun','semaforr','semaforr', semaforr_path, target_set, map_config, map_dimensions])
    print "waiting,,"

   
    # Wait till semaforr completes the process
    while semaforr_process.poll() is None:
        print "Semaforr process still running ..."
        time.sleep(1)
   
    print "Semaforr process has ended ..."
    print "Terminating the simulator"

    menge_sim_process.terminate()
    while menge_sim_process.poll() is None:
        print "Menge process still running ..."
    time.sleep(1)

    print "Menge terminated!"

    log_process.terminate()
    log_file.close()
    #why_process.terminate()
    #print "Why terminated!"

    roscore.terminate()
    time.sleep(10)
    print "roscore terminated!"

map_name = "moma-5"
for i in range(1,2):
    target_file_name = "target" + str(i) + ".conf"
    log_name = map_name + "_" + target_file_name + ".txt"
    experiment()




