using LightBuzz.Vitruvius.FingerTracking;
using Microsoft.Kinect;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;
using Microsoft.VisualBasic;
using Leap;


namespace KinectFingerTracking
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private Controller leapController = null;
        private LeapListener leapListener = null;
        private KinectSensor _sensor = null;
        private InfraredFrameReader _infraredReader = null;
        private DepthFrameReader _depthReader = null;
        private BodyFrameReader _bodyReader = null;
        private IList<Body> _bodies;
        private Body _body;
        private bool recording = false;
        private bool HandsDetected = false;
        private int counter = 1;
        private Stopwatch timer = new Stopwatch();
        private string gesture;
        private string gesturepath;
        private int gestureindex = 0;
        private string participant = "";
        private string round = "";
        private int participantNumber;
        private int roundNumber;
        List<string> gestures = new List<string>();
        BitmapImage img = new BitmapImage();

        // Create a new reference of a HandsController.
        private HandsController _handsController = null;

        /// <summary>
        /// The main window of the app.
        /// </summary>
        public MainWindow()
        {
            // get participant number
            participant = Interaction.InputBox("Please enter participant number: ", "HANDGR Data Gatherer", "");
            while (!int.TryParse(participant, out participantNumber) || participantNumber < 0 || participantNumber > 49)
                participant = Interaction.InputBox("Invalid participant number entered. Please enter a VALID participant number (between 0 and 49): ", "HANDGR Data Gatherer", "");
            // get round number 
            round = Interaction.InputBox("Participant " + participant + ": \n   Please enter round number: ", "HANDGR Data Gatherer", "");
            while (!int.TryParse(round, out roundNumber)|| roundNumber < 0 || roundNumber > 26)
                round = Interaction.InputBox("Participant " + participant + ": \n    Invalid round number entered. Please enter a VALID round number (between 0 and 25): ", "HANDGR Data Gatherer", "");

            InitializeComponent();
            _sensor = KinectSensor.GetDefault();
            leapController = new Controller();
            controller.SetPolicy(Controller.PolicyFlag.POLICY_BACKGROUND_FRAMES);
            leapListener = new LeapListener();
            leapController.AddListener(leapListener);

            this.details.Text = "Participant Number: " + participant + "\nRound Number: " + round;
            gestureImage.Source = new BitmapImage(new Uri(Directory.GetCurrentDirectory() + "\\images\\blank.png"));

            //read in order of gestures
            using (var reader = new StreamReader(@"./orders/" + participant + "-" + round + ".txt"))
            {
                while (!reader.EndOfStream)
                {
                    var line = reader.ReadLine();
                    var values = line.Split(',');
                    for (int i=0; i<10; ++i)
                    {
                        gestures.Add(values[i]);
                    }
                }
            }
            
            if (_sensor != null)
            {
                
                _depthReader = _sensor.DepthFrameSource.OpenReader();
                _depthReader.FrameArrived += DepthReader_FrameArrived;

                _infraredReader = _sensor.InfraredFrameSource.OpenReader();
                _infraredReader.FrameArrived += InfraredReader_FrameArrived;

                _bodyReader = _sensor.BodyFrameSource.OpenReader();
                _bodyReader.FrameArrived += BodyReader_FrameArrived;
                _bodies = new Body[_sensor.BodyFrameSource.BodyCount];

                // Initialize the HandsController and subscribe to the HandsDetected event.
                _handsController = new HandsController();
                _handsController.HandsDetected += HandsController_HandsDetected;

                this.KeyDown += new System.Windows.Input.KeyEventHandler(OnEnter);
                
                _sensor.Open();

            }
        }

        

        private void OnEnter(object sender, System.Windows.Input.KeyEventArgs e)
        {
            if (e.Key == Key.Enter && HandsDetected)
            {
                if (gestureindex < gestures.Count)
                { 
                    //for each gesture, set recording boolean to true and start timer
                    recording = true;
                    gesture = gestures[gestureindex];
                    leapListener.filename = "Leap_" + gesture + "_" + leapController.Now();
                    leapListener.recording = true;
                    timer.Start();
                    gesturepath = gesture + " " + DateTime.Now.ToString("ddMMyy HHmmss");
                    System.IO.Directory.CreateDirectory(gesturepath);
                    
                    //start Myo and Leap processes
                    Process.Start("..\\Myo\\MyoDataCapture");
                    ProcessStartInfo python = new ProcessStartInfo();
                    python.FileName = "python";
                    python.Arguments = "..\\Leap\\Sample.py " + gesture;
                    Process.Start(python);
                    gestureindex++;
                    
                }

            }
        }

        private void DepthReader_FrameArrived(object sender, DepthFrameArrivedEventArgs e)
        {
            if (recording)
            {
                //record each gesture frame
                SaveBitmap(gesturepath + "\\" + counter.ToString() + ".png");
                ++counter;
                //reset timer if 3 seconds reached
                if (timer.Elapsed.TotalSeconds > 3)
                {
                    timer.Reset();
                    recording = false;
                    leapListener.recording = false;
                    counter = 0;

                    //kill Myo and Leap processes
                    var myo = Process.GetProcesses().Where(pr => (pr.ProcessName == "MyoDataCapture") || (pr.ProcessName == "python"));
                    foreach (var process in myo)
                    {
                        process.Kill();
                    }
                }
            }
            //update gesture information
            else {
                if (gestureindex < gestures.Count)
                {
                    textBox1.Text = "Next gesture: " + gestures[gestureindex];
                    gestureImage.Source = new BitmapImage(new Uri(Directory.GetCurrentDirectory() + "\\images\\" + gestures[gestureindex] + ".gif"));
                }
                else {
                    textBox1.Text = "Completed round!";
                    gestureImage.Source = new BitmapImage(new Uri(Directory.GetCurrentDirectory() + "\\images\\blank.png"));
                }
            }

            canvas.Children.Clear();

            using (DepthFrame frame = e.FrameReference.AcquireFrame())
            {
                if (frame != null)
                {
                    // 2) Update the HandsController using the array (or pointer) of the depth depth data, and the tracked body.
                    using (KinectBuffer buffer = frame.LockImageBuffer())
                    {
                        _handsController.Update(buffer.UnderlyingBuffer, _body);
                    }
                }
            }
        }

        private void InfraredReader_FrameArrived(object sender, InfraredFrameArrivedEventArgs e)
        {
            using (var frame = e.FrameReference.AcquireFrame())
            {
                if (frame != null)
                {
                    camera.Source = frame.ToBitmap();
                }
            }
        }

        private void BodyReader_FrameArrived(object sender, BodyFrameArrivedEventArgs e)
        {
            using (var bodyFrame = e.FrameReference.AcquireFrame())
            {
                if (bodyFrame != null)
                {
                    bodyFrame.GetAndRefreshBodyData(_bodies);

                    _body = _bodies.Where(b => b.IsTracked).FirstOrDefault();
                }
            }
        }

        private void HandsController_HandsDetected(object sender, HandCollection e)
        {
            //// Display the results!

            //if (e.HandLeft != null)
            //{
            //    // Draw contour.
            //    foreach (var point in e.HandLeft.ContourDepth)
            //    {
            //        DrawEllipse(point, Brushes.Green, 2.0);
            //    }

            //    // Draw fingers.
            //    foreach (var finger in e.HandLeft.Fingers)
            //    {
            //        DrawEllipse(finger.DepthPoint, Brushes.White, 4.0);
            //    }
            //}

            if (e.HandRight != null)
            {
                HandsDetected = true;
                // Draw contour.
                foreach (var point in e.HandRight.ContourDepth)
                {
                    if (recording)
                        DrawEllipse(point, Brushes.Red, 2.0);
                    else
                        DrawEllipse(point, Brushes.Blue, 2.0);
                }

                // Draw fingers.
                //foreach (var finger in e.HandRight.Fingers)
                //{
                //    DrawEllipse(finger.DepthPoint, Brushes.Red, 4.0);
                //}
            }
            else
                HandsDetected = false;

        }

        private void SaveBitmap(string filename)
        {
            FileStream fs = new FileStream(filename, FileMode.Create);
            RenderTargetBitmap bmp = new RenderTargetBitmap((int)canvas.ActualWidth, (int)canvas.ActualHeight, 
                1 / 96, 1 / 96, PixelFormats.Pbgra32);
            bmp.Render(canvas);
            BitmapEncoder encoder = new TiffBitmapEncoder();
            encoder.Frames.Add(BitmapFrame.Create(bmp));
            encoder.Save(fs);
            fs.Close();
        }

        private void Window_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            if (_bodyReader != null)
            {
                _bodyReader.Dispose();
                _bodyReader = null;
            }

            if (_depthReader != null)
            {
                _depthReader.Dispose();
                _depthReader = null;
            }

            if (_infraredReader != null)
            {
                _infraredReader.Dispose();
                _infraredReader = null;
            }

            if (_sensor != null)
            {
                _sensor.Close();
                _sensor = null;
            }

            if (leapListener != null)
            {
                leapController.RemoveListener(leapListener);
                leapListener = null;
            }

            if (leapController != null)
            {
                leapController.Dispose();
                leapController = null;
            }
        }

        private void DrawEllipse(DepthSpacePoint point, Brush brush, double radius)
        {
            Ellipse ellipse = new Ellipse
            {
                Width = radius,
                Height = radius,
                Fill = brush
            };

            canvas.Children.Add(ellipse);

            Canvas.SetLeft(ellipse, point.X - radius / 2.0);
            Canvas.SetTop(ellipse, point.Y - radius / 2.0);

        }
    }
    
    public class LeapListener : Listener
    {
        private Object thisLock = new Object();
        public string filename { get; set; }
        public bool recording { get; set; }

        private void SafeWriteLine(String line)
        {
            lock (thisLock)
            {
                Console.WriteLine(line);
            }
        }

        public override void OnInit(Controller controller)
        {
            SafeWriteLine("Initialized");
        }

        public override void OnConnect(Controller controller)
        {
            SafeWriteLine("Connected");
        }

        public override void OnDisconnect(Controller controller)
        {
            //Note: not dispatched when running in a debugger.
            SafeWriteLine("Disconnected");
        }

        public override void OnExit(Controller controller)
        {
            SafeWriteLine("Exited");
        }

        public override void OnFrame(Controller controller)
        {
            // Get the most recent frame and report some basic information
            Frame frame = controller.Frame();

            if (frame.Hands.Count == 1 && recording)
            {
                SafeWriteLine("Frame id: " + frame.Id
                                                + ", timestamp: " + frame.Timestamp
                                                + ", hands: " + frame.Hands.Count
                                                + ", fingers: " + frame.Fingers.Count
                                                + ", tools: " + frame.Tools.Count
                                                + ", gestures: " + frame.Gestures().Count);
            }
            else {
                SafeWriteLine(frame.Id.ToString());
            }

            if (recording)
            {
                string f_name = filename + "\\" + frame.Timestamp + ".data";
                System.IO.FileInfo file = new System.IO.FileInfo(f_name);
                file.Directory.Create();
                byte[] serializedFrame = frame.Serialize;
                System.IO.File.WriteAllBytes(file.FullName, serializedFrame);
            }



        }
    }
}
}
