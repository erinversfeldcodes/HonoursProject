@echo off
set /p participant_file="Participant (filename): ":
python create_order.py "%participant_file%"
set /p list=<"%participant_file%"
echo "%list%"
for %%x in (%list%) do (
    echo PERFORM GESTURE %%x
    ECHO Enter to start recording for 3 seconds, enter 'm' for manual termination
    set /p choice1="Decide: ":
    if "%choice1%"=="m" (
      START .\\Myo\\MyoDataCapture
      ECHO Myo data gatherer is running
      START .\\Kinect\\kinectv2_viewer %%x
      ECHO Kinect data gatherer is running
      START py -2 .\\Leap\\Sample.py meow%%x.txt
      ECHO Leap data gatherer is running
      set /p choice2="Enter to terminate... "
      taskkill /IM py.exe
      taskkill /IM MyoDataCapture.exe
      taskkill /IM kinectv2_viewer.exe
      timeout 1
    ) else (
      START .\\Myo\\MyoDataCapture
      ECHO Myo data gatherer is running
      START .\\Kinect\\kinectv2_viewer %%x
      ECHO Kinect data gatherer is running
      START py -2 .\\Leap\\Sample.py meow%%x.txt
      ECHO Leap data gatherer is running
      timeout 3
      taskkill /IM py.exe
      taskkill /IM MyoDataCapture.exe
      taskkill /IM kinectv2_viewer.exe
      timeout 1
    )
)
