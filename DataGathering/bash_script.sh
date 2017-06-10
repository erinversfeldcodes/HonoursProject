#!/bin/bash

# run programs
.\\Myo\\MyoDataCapture & export MYO_PID=$!
echo $MYO_PID
read -r input
if $input = "n"; then kill $MYO_PID fi