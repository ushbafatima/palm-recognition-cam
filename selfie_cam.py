import cv2 as cv
import os

FRAME_HEIGHT = 480
FRAME_WIDTH = 640

# Initialize video capture
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
    photo_count = 0  # Counter for saved photos

    while True:
        ret, frame = capture.read()
        if not ret:
            break
        frame = cv.flip(frame, 1)
        # Display the frame
        cv.imshow("Camera", frame)

         # Capture photo if 'c' is pressed
        key = cv.waitKey(1) & 0xFF
        if key == ord('c'):
            capture_photo(frame, photo_count)
            photo_count += 1
                
        # Break the loop if 'q' is pressed
        if cv.waitKey(1) & 0xFF == ord('q') or cv.getWindowProperty("Camera", cv.WND_PROP_VISIBLE) < 1:
            break
       
    
    capture.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    cam()