🏋️ AI Workout Assistant

A Python-based AI workout assistant that uses computer vision to track basic exercises like squats and push-ups using a webcam. It counts repetitions, gives voice feedback, and stores workout history for later review.


🚀 Features
🎥 Real-time webcam tracking using OpenCV
🤖 Pose detection powered by MediaPipe
🔢 Repetition counter for:
Squats
Push-ups
🔊 Voice feedback using pyttsx3 (announces rep count)
⏱️ 1-minute workout sessions per exercise
💾 Workout history storage in a CSV file
📊 Basic progress visualization using Matplotlib
🖥️ Simple GUI interface with Tkinter to:
View workout history
Display best scores
Show progress graph
🛠️ Technologies Used
Python
OpenCV
MediaPipe
NumPy
pyttsx3
Tkinter
Matplotlib
CSV & OS modules
⚙️ How It Works
The webcam captures live video input
MediaPipe detects body landmarks
Joint angles are calculated using NumPy
Repetitions are counted based on angle thresholds
Voice feedback announces each rep
Results are saved and displayed in a GUI window
▶️ Usage
Install required libraries:
pip install opencv-python mediapipe numpy pyttsx3 matplotlib
Run the script:
python main.py
The program will:
Run a Squat session (1 minute)
Then a Push-up session (1 minute)
Finally display workout feedback in a GUI
📁 Data Storage
Workout data is saved in:
workout_history.csv
Each record includes:
Exercise name
Time duration
Repetitions
Date & time
⚠️ Limitations
Tracks only left-side body joints
Limited to Squats and Push-ups
Basic angle-based detection (no advanced form correction)
GUI and plotting are simple and may not handle large datasets well
Code formatting and error handling are minimal
💡 Future Improvements
Add more exercises
Improve accuracy of rep counting
Add posture/form correction
Enhance UI/UX
Optimize performance
Tkinter – GUI interface
Matplotlib – Data visualization
CSV – Data storage
