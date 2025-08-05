import cv2
import mediapipe
import pyautogui
import time
import numpy as np

# Initialize FaceMesh and external camera
face_mesh_landmarks = mediapipe.solutions.face_mesh.FaceMesh(refine_landmarks=True)
cam = cv2.VideoCapture(1)  # Change this index if the external webcam is not detected

if not cam.isOpened():
    print("Error: Could not access external webcam.")
    exit()

screen_w, screen_h = pyautogui.size()

# Variables for click mode and visual feedback
click_mode = 'single'  # Options: 'single', 'double', 'right'
last_click_time = 0
click_delay = 0.5  # Delay for double click
feedback_text = ""
blink_detected = False
blink_start_time = 0
blink_duration = 0.2  # Duration to consider as a blink
previous_eye_y = None  # To track previous eye position for scrolling

def eye_aspect_ratio(eye):
    A = np.linalg.norm(np.array([eye[1].x, eye[1].y]) - np.array([eye[5].x, eye[5].y]))
    B = np.linalg.norm(np.array([eye[2].x, eye[2].y]) - np.array([eye[4].x, eye[4].y]))
    C = np.linalg.norm(np.array([eye[0].x, eye[0].y]) - np.array([eye[3].x, eye[3].y]))
    return (A + B) / (2.0 * C)

EAR_THRESHOLD = 0.2  # Threshold for blink detection

while True:
    _, image = cam.read()
    if image is None:
        print("Error: Could not read frame from webcam.")
        break
    
    image = cv2.flip(image, 1)
    window_h, window_w, _ = image.shape
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    processed_image = face_mesh_landmarks.process(rgb_image)
    all_face_landmark_points = processed_image.multi_face_landmarks

    if all_face_landmark_points:
        one_face_landmark_points = all_face_landmark_points[0].landmark
        for id, landmark_point in enumerate(one_face_landmark_points[474:478]):
            x = int(landmark_point.x * window_w)
            y = int(landmark_point.y * window_h)

            if id == 1:
                mouse_x = int(screen_w / window_w * x)
                mouse_y = int(screen_h / window_h * y)
                pyautogui.moveTo(mouse_x, mouse_y)

            cv2.circle(image, (x, y), 3, (0, 0, 255), -1)

        left_eye = [one_face_landmark_points[i] for i in [33, 160, 158, 133, 153, 144]]
        right_eye = [one_face_landmark_points[i] for i in [362, 385, 387, 263, 373, 380]]

        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)
        avg_ear = (left_ear + right_ear) / 2.0

        # Check if the eyes are closed (blink detection)
        if avg_ear < EAR_THRESHOLD:
            if not blink_detected:
                blink_detected = True
                blink_start_time = time.time()
                feedback_text = "Blink detected! Selecting text..."
                pyautogui.mouseDown()
        else:
            if blink_detected:
                if time.time() - blink_start_time < blink_duration:
                    feedback_text = "Text selected!"
                else:
                    pyautogui.mouseUp()
                blink_detected = False

        # Detect upward eye movement for scrolling
        current_eye_y = (left_eye[1].y + left_eye[2].y) / 2
        if previous_eye_y is not None:
            if current_eye_y < previous_eye_y - 0.01:
                pyautogui.scroll(10)
                feedback_text = "Scrolling up..."
            elif current_eye_y > previous_eye_y + 0.01:
                pyautogui.scroll(-10)
                feedback_text = "Scrolling down..."

        previous_eye_y = current_eye_y

        # Display feedback text
        cv2.putText(image, feedback_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        feedback_text = ""

    cv2.imshow("Eye Controlled Mouse", image)

    # Press 'q' or 'Esc' to quit
    key = cv2.waitKey(1) & 0xFF  
    if key == 27 or key == ord('q'):
        print("Exiting...")
        break

cam.release()
cv2.destroyAllWindows()