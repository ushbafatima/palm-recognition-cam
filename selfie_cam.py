import cv2 as cv
import os
import time
import mediapipe as mp

import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)


FRAME_HEIGHT = 480
FRAME_WIDTH = 640

RED = (0, 0, 255)

capture = cv.VideoCapture(0)
if not capture.isOpened():
    print("Error: Could not open camera.")
    exit()

photos_folder = "photos"
if not os.path.exists(photos_folder):
    os.makedirs(photos_folder)

def capture_photo(frame, photo_count):
    """Handles the logic for capturing and saving a photo."""
    photo_path = os.path.join(photos_folder, f"photo_{photo_count}.jpg")
    cv.imwrite(photo_path, frame)
    print(f"Photo saved: {photo_path}")

def recognize_hand(frame):
    """Detects hands using MediaPipe and draws landmarks."""
    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        return True  # At least one hand detected
    return False  # No hand detected

def cam():
    """Handles the camera feed and user interaction."""
    photo_count = 0
    timer_active = False
    timer_start = 0
    countdown = 3
    selected_countdown = 3

    while True:
        ret, frame = capture.read()
        if not ret:
            break

        frame = cv.flip(frame, 1)
        h, w = frame.shape[:2]

        # Detect and draw hands
        hand_detected = recognize_hand(frame)

        if timer_active:
            elapsed = time.time() - timer_start
            remaining = max(0, countdown - int(elapsed))
            
            if remaining > 0:
                cv.putText(
                    frame,
                    str(remaining),
                    (w//2 - 30, h//2),
                    cv.FONT_HERSHEY_SIMPLEX,
                    3,
                    RED,
                    3
                )
            else:
                capture_photo(frame, photo_count)
                photo_count += 1
                timer_active = False

        cv.imshow("ushbi cam", frame)

        key = cv.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('3'):
            selected_countdown = 3
        elif key == ord('5'):
            selected_countdown = 5
        elif key == ord('1'):
            selected_countdown = 10
        elif key == ord('0'):
            selected_countdown = 0
            print("Timer disabled.")
        elif key == ord('c'):
            if selected_countdown == 0:
                capture_photo(frame, photo_count)
                photo_count += 1
            else:
                countdown = selected_countdown
                timer_active = True
                timer_start = time.time()

    capture.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    cam()