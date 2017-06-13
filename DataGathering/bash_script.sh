#!/bin/bash

gesture_num=0

# run programs
while [ $gesture_num -lt 26 ]
do
echo "Enter 's' to record for 3 seconds"
echo "Enter 'm' to record for an indeterminate number of seconds"
read -r input
if [ "$input" = "s" ]
#then python hello_world.py & export MYO_PID=$!
then python ../../LEAP/Sample.py & export MYO_PID=$!
#.\\Myo\\MyoDataCapture & export MYO_PID=$!
echo $MYO_PID
echo "Myo data gatherer is running"
sleep 3s
kill $MYO_PID
elif [ "$input" = "m" ]
then python hello_world.py & export MYO_PID=$!
echo $MYO_PID
echo "Myo data gatherer is running, enter 'n' to stop"
read -r input2
if [ "$input2" = "n" ]
then kill $MYO_PID
fi
fi
#read -r input
#if [ "$input" = "n" ]
#then kill $MYO_PID
#fi
gesture_num=$[$gesture_num+1]
done
