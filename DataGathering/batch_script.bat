@echo off
for /l %%x in (1, 1, 26) do (
    ECHO Enter to start recording for 3 seconds, enter 'm' for manual termination
    set /p choice1="Decide: ":
    if "%choice1%"=="m" (
      START py -2 .\\Leap\\Sample.py meow%%x.txt
      ECHO Leap data gatherer is running
      START .\\Myo\\MyoDataCapture
      ECHO Myo data gatherer is running
      START .\\Kinect\\KinectApplication\\kinectv2_viewer
      ECHO Kinect data gatherer is running
      set /p choice2="Enter to terminate... "
      taskkill /IM py.exe
      taskkill /IM MyoDataCapture.exe
      taskkill /IM kinectv2_viewer.exe
    ) else (
      START py -2 .\\Leap\\Sample.py meow%%x.txt
      ECHO Leap data gatherer is running
      START .\\Myo\\MyoDataCapture
      ECHO Myo data gatherer is running
      START .\\Kinect\\KinectApplication\\kinectv2_viewer
      ECHO Kinect data gatherer is running
      timeout 3
      taskkill /IM py.exe
      taskkill /IM MyoDataCapture.exe
      taskkill /IM kinectv2_viewer.exe
    )
)