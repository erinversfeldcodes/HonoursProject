echo off
set letter=%1
START py -2 .\\Leap\\Sample.py Leap_%letter%
ECHO Leap data gatherer is running
TIMEOUT 3
TASKKILL /IM py.exe
TIMEOUT 1
