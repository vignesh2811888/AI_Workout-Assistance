import cv2
import mediapipe as mp
import numpy as np
import time
import pyttsx3
import tkinter as tk
from tkinter import ttk
import csv
import os
import matplotlib.pyplot as plt
# Initialize Mediapipe, TTS, etc.
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
engine = pyttsx3.init()
DATA_FILE = "workout_history.csv"
# Speak function
def speak(text):
 engine.say(text)
 engine.runAndWait()
# Calculate joint angle
def calculate_angle(a, b, c): a, b, c = np.array(a), np.array(b), np.array(c)
 radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
 angle = np.abs(radians * 180.0 / np.pi)
 return 360 - angle if angle > 180 else angle
# Load data
journey_data = []
best_squat = 0
best_pushup = 0
if os.path.exists(DATA_FILE):
 with open(DATA_FILE, "r") as f:
 reader = csv.DictReader(f)
 for row in reader:
 journey_data.append((row["Exercise"], row["Time"], int(row["Reps"]),
row["Date"]))
 if row["Exercise"] == "Squat":
 best_squat = max(best_squat, int(row["Reps"]))
 elif row["Exercise"] == "Pushup":
 best_pushup = max(best_pushup, int(row["Reps"]))
def run_exercise(exercise_name):
 global best_squat, best_pushup, journey_data
 cap = cv2.VideoCapture(0)
 counter = 0
 stage = None
 duration = 60
 start_time = time.time()
 speak(f"Starting your {exercise_name} session for one minute.")
 with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as
pose:
 while cap.isOpened():
 ret, frame = cap.read()if not ret:
 break
 frame = cv2.flip(frame, 1)
 image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
 results = pose.process(image)
 image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
 try:
 landmarks = results.pose_landmarks.landmark
 if exercise_name == "Squat":
 hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
 knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
 ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
 angle = calculate_angle(hip, knee, ankle)
 else:
 shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
 elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
 wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
 angle = calculate_angle(shoulder, elbow, wrist)
 if angle > 160:
 stage = "up"
 if angle < 90 and stage == "up":
 stage = "down"
 counter += 1
 speak(str(counter))
expect:
pass
 elapsed = int(time.time() - start_time)
 remaining = max(0, duration - elapsed)
 cv2.rectangle(image, (0, 0), (260, 80), (255, 255, 255), -1)
 cv2.putText(image, f'{exercise_name}', (10, 25), cv2.FONT_HERSHEY_SIMPLEX,
0.8, (0, 0, 0), 2)
 cv2.putText(image, f'Reps: {counter}', (10, 55), cv2.FONT_HERSHEY_SIMPLEX,
0.7, (0, 128, 255), 2)
 cv2.putText(image, f'Time: {remaining}s', (150, 55),
cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 128, 255), 2)
 mp_drawing.draw_landmarks(image,results.pose_landmarks,
mp_pose.POSE_CONNECTIONS)
 cv2.imshow('AI Workout Assistant', image)
 if cv2.waitKey(10) & 0xFF == ord('q') or remaining == 0:
 break
 cap.release()
 cv2.destroyAllWindows()
 timestamp = time.strftime("%d/%m/%Y %I:%M:%S %p")
 journey_data.append((exercise_name, "1 Minute", counter, timestamp))
 if exercise_name == "Squat":
 best_squat = max(best_squat, counter)
 elif exercise_name == "Pushup":
 best_pushup = max(best_pushup, counter)
 speak(f"{exercise_name} session completed. You did {counter} repetitions.")
def save_data():
 with open(DATA_FILE, "w", newline="") as f:writer = csv.writer(f)
 writer.writerow(["Exercise", "Time", "Reps", "Date"])
 writer.writerows(journey_data)
def show_feedback():
 window = tk.Tk()
 window.title("AI Workout Feedback")
 window.geometry("600x400")
 window.configure(bg="#f2f2f2")
 tk.Label(window, text="Journey", font=("Arial", 16, "bold"), bg="#f2f2f2").pack(pady=5)
 tree = ttk.Treeview(window, columns=("Exercise", "Time", "Reps", "Date"),
show="headings", height=6)
 tree.pack(pady=5)
 for col in ("Exercise", "Time", "Reps", "Date"):
 tree.heading(col, text=col)
 tree.column(col, anchor="center", width=140)
 for data in journey_data:
 tree.insert("", "end", values=data)
 tk.Label(window, text="Best Scores", font=("Arial", 16, "bold"),
bg="#f2f2f2").pack(pady=10)
 tk.Label(window, text=f"Squat: {best_squat} reps", font=("Arial", 13),
bg="#f2f2f2").pack()
 tk.Label(window, text=f"Pushup: {best_pushup} reps", font=("Arial", 13),
bg="#f2f2f2").pack()
 def show_graph():
 squats, pushups, dates = [], [], []
 for ex, _, reps, date in journey_data:
 if ex == "Squat":
squats.append(reps)
 dates.append(date)
 elif ex == "Pushup":
 pushups.append(reps)
 plt.figure(figsize=(8, 5))
 plt.plot(dates[:len(squats)], squats, 'o-', label='Squat Reps')
 plt.plot(dates[:len(pushups)], pushups, 's-', label='Pushup Reps')
 plt.title("Workout Progress Over Time")
 plt.xlabel("Date")
 plt.ylabel("Repetitions")
 plt.xticks(rotation=45)
 plt.legend()
 plt.tight_layout()
 plt.show()
 ttk.Button(window, text="View Progress Graph", command=show_graph).pack(pady=10)
 ttk.Button(window, text="OK", command=lambda: [save_data(),
window.destroy()]).pack(pady=10)
 window.mainloop()
# Run workout
run_exercise("Squat")
run_exercise("Pushup")
show_feedback()