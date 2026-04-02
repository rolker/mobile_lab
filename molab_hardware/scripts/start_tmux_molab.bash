#!/bin/bash

tmux new -d -s molab
tmux send-keys "rosrun rosmon rosmon --name=rosmon_molab molab_hardware operator_mobile_lab.launch" C-m
tmux a -t molab
