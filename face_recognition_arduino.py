import face_recognition
import cv2
import numpy as np
from picamera2 import Picamera2
import time
import pickle
import serial

# --------Load known encodings from pickle----------------
print("[INFO] loading encodings...")
with open("encodings.pickle", "rb") as f:
    data = pickle.loads(f.read())
known_face_encodings = data["encodings"]
known_face_names = data["names"]

# -------------Initialize PiCamera-----------------
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (1920, 1080)}))
picam2.start()

# -----------Initialize Serial (Arduino)-------------
arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # Adjust if needed (Run command in terminal: ls /dev/ttyACM* /dev/ttyUSB* to find the correct port Arudino is plugged into.)
time.sleep(3.5)  # Give Arduino time to boot
print("Arduino Connected")
# ------Variables--------
cv_scaler = 4  # Downscale factor for performance
face_locations = []
face_encodings = []
face_names = []
frame_count = 0
start_time = time.time()
fps = 0
last_result = None  # Keep track of last result to prevent spamming commands to Arduino

# Authorized names list (case-sensitive)
authorized_names = ["nat", "nehemiah", "logan"]  # Must match pickle names 

#------Face detection and Arduino trigger logic----------
def process_frame(frame):
    global face_locations, face_encodings, face_names, last_result

    resized_frame = cv2.resize(frame, (0, 0), fx=(1/cv_scaler), fy=(1/cv_scaler))
    rgb_resized_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_resized_frame)
    face_encodings = face_recognition.face_encodings(rgb_resized_frame, face_locations, model='large')

    face_names = []
    authorized_face_detected = False

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            if name in authorized_names:
                authorized_face_detected = True

        face_names.append(name)

    #-------Only send result if a face was detected---------
    if len(face_encodings) > 0:
        result = 'pass' if authorized_face_detected else 'fail'
        if result != last_result:
            arduino.write((result + '\n').encode())
            print(f"[INFO] Sent '{result}' to Arduino.")
            last_result = result

    return frame

#------Draw bounding boxes and names-------
def draw_results(frame):
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= cv_scaler
        right *= cv_scaler
        bottom *= cv_scaler
        left *= cv_scaler

        # Draw face box
        cv2.rectangle(frame, (left, top), (right, bottom), (244, 42, 3), 3)
        cv2.rectangle(frame, (left - 3, top - 35), (right + 3, top), (244, 42, 3), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, top - 6), font, 1.0, (255, 255, 255), 1)

        if name in authorized_names:
            cv2.putText(frame, "Authorized", (left + 6, bottom + 23), font, 0.6, (0, 255, 0), 1)

    return frame

#-----FPS calculation-------
def calculate_fps():
    global frame_count, start_time, fps
    frame_count += 1
    elapsed_time = time.time() - start_time
    if elapsed_time > 1:
        fps = frame_count / elapsed_time
        frame_count = 0
        start_time = time.time()
    return fps

#----Main loop-----
while True:
    frame = picam2.capture_array()
    processed_frame = process_frame(frame)
    display_frame = draw_results(processed_frame)
    current_fps = calculate_fps()

    cv2.putText(display_frame, f"FPS: {current_fps:.1f}", (display_frame.shape[1] - 150, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Video', display_frame)

    if cv2.waitKey(1) == ord("q"):
        break

#----END----
cv2.destroyAllWindows()
picam2.stop()
arduino.close()
