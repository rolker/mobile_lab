#!/bin/bash

# called from cron @reboot using field's user crontab
# inspired by: https://answers.ros.org/question/140426/issues-launching-ros-on-startup/

DAY=$(date "+%Y-%m-%d")
NOW=$(date "+%Y-%m-%dT%H.%M.%S.%N")
LOGDIR="/home/field/project11/log/${DAY}"
mkdir -p "$LOGDIR"
LOG_FILE="${LOGDIR}/autostart_${NOW}.txt"

{

echo ""
echo "#############################################"
echo "Running autostart_mobius.bash"
/bin/date
echo "#############################################"
echo ""
echo "Logs:"

source /opt/ros/noetic/setup.bash
source /home/field/project11/catkin_ws/devel/setup.bash

set -v

while ! ping -c 1 -W 1 mobius; do
    echo "Waiting for ping to mobius..."
    sleep 1
done

export ROS_WORKSPACE=/home/field/project11/catkin_ws
export ROS_IP=192.168.50.195

echo "running tmux..."

/usr/bin/tmux new -d -s roscore

/usr/bin/tmux send-keys "roscore" C-m

/usr/bin/tmux new -d -s project11

/usr/bin/tmux send-keys "rosrun rosmon rosmon --name=rosmon_molab molab_hardware mobile_lab.launch logDirectory:=${LOGDIR}" C-m

} >> "${LOG_FILE}" 2>&1
