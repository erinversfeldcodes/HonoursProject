#!/bin/bash

gesture_num = 0

# run programs
while [$gesture_num -lt 26]
do
.\\Myo\\MyoDataCapture & export MYO_PID=$!
echo $MYO_PID
echo "Myo data gatherer is running"
read -r input
if then $input = "n"; then kill $MYO_PID fi
gesture_num = $[$gesture_num+1]
done