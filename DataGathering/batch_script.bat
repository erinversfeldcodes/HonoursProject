@echo off
set "choice1="
set "participant_file="
set "list="
setlocal EnableDelayedExpansion
setlocal
set /p participant_file="Participant number: "
set /p list=<orders\%participant_file%.txt
echo %list%
for %%x in (%list%) do (
    echo PERFORM GESTURE %%x
    setlocal
    set /p choice1="Enter to start recording for 3 seconds, enter m for manual termination: "
    if "!choice1!"=="m" (
      START .\\Myo\\MyoDataCapture
      ECHO Myo data gatherer is running
      START .\\Kinect\\kinectv2_viewer %%x
      ECHO Kinect data gatherer is running
      START py -2 .\\Leap\\Sample.py Leap_%%x
      ECHO Leap data gatherer is running
      set /p choice2="Enter to terminate... "
      TASKKILL /IM MyoDataCapture.exe
      TASKKILL /IM kinectv2_viewer.exe
      TASKKILL /IM py.exe
      TIMEOUT 1
    ) else (
      START .\\Myo\\MyoDataCapture
      ECHO Myo data gatherer is running
      START .\\Kinect\\kinectv2_viewer %%x
      ECHO Kinect data gatherer is running
      START py -2 .\\Leap\\Sample.py Leap_%%x
      ECHO Leap data gatherer is running
      TIMEOUT 3
      TASKKILL /IM MyoDataCapture.exe
      TASKKILL /IM kinectv2_viewer.exe
      TASKKILL /IM py.exe
      TIMEOUT 1
    )
    endlocal
)
endlocal
