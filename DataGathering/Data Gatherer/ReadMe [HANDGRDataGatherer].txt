This data gathering program is compatible with the Microsoft Kinect V2, Leap Motion Controller, and Myo Armband. 
External application dependancies are as follows:

- For the Kinect V2: The Kinect 2.0 SDK must be installed. This can be found at https://www.microsoft.com/en-us/download/details.aspx?id=44561.
- For the Leap Motion Controller:
- For the Myo Armband:

The program file is HANDGRDataGatherer\HANDGRDataGatherer\bin\Debug\HANDGRDataGatherer.exe. 
Before opening the program, ensure the Kinect V2, Leap Motion Controller and Myo Armband are all connected to the computer. 

Upon opening the program, participant and round numbers will be requested.
Following this, specific gestures will be displayed on the screen and can be recorded by the user by triggering the Enter key. Note that the program will only record gestures under the conditions that:
- A contour is picked up by the Kinect (and should be highlighted on screen in real-time, when picked up); and
- The Leap Motion Controller senses exactly ONE hand in its field of view.
Following gesture recording, data can be found in the directory of the .exe file (HANDGRDataGatherer\HANDGRDataGatherer\bin\Debug\).
