#!/bin/bash

gesture_num=0

# run programs
while [ $gesture_num -lt 26 ]
do
python hello_world.py & export MYO_PID=$!
#python ../../LEAP/Sample.py & export MYO_PID=$!
#.\\Myo\\MyoDataCapture & export MYO_PID=$!
echo $MYO_PID
echo "Myo data gatherer is running"
read -r input
if [ "$input" = "n" ]
then kill $MYO_PID
fi
gesture_num=$[$gesture_num+1]
done
