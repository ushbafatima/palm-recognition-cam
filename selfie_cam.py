import cv2 as cv
import os
import time
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