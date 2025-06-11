import cv2 as cv
import os
import time

FRAME_HEIGHT = 480
FRAME_WIDTH = 640

# Button dimensions and positions
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 40
BUTTON_MARGIN = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (0, 0, 255)
GREEN = (0, 255, 0)

# Initialize video capture
capture = cv.VideoCapture(0)
if not capture.isOpened():
    print("Error: Could not open camera.")
    exit()

photos_folder = "photos"
if not os.path.exists(photos_folder):
    os.makedirs(photos_folder)

def create_button(frame, text, x, y, width, height, color):
    """Creates a button with text on the frame."""
    # Draw button background
    cv.rectangle(frame, (x, y), (x + width, y + height), color, -1)
    # Draw button border
    cv.rectangle(frame, (x, y), (x + width, y + height), BLACK, 2)
    
    # Calculate text position to center it
    text_size = cv.getTextSize(text, cv.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
    text_x = x + (width - text_size[0]) // 2
    text_y = y + (height + text_size[1]) // 2
    
    # Draw text
    cv.putText(frame, text, (text_x, text_y), cv.FONT_HERSHEY_SIMPLEX, 0.7, BLACK, 2)
    
    return x, y, x + width, y + height

def capture_photo(frame, photo_count):
    """Handles the logic for capturing and saving a photo."""
    photo_path = os.path.join(photos_folder, f"photo_{photo_count}.jpg")
    cv.imwrite(photo_path, frame)
    print(f"Photo saved: {photo_path}")

def cam():
    """Handles the camera feed and user interaction."""
    photo_count = 0  # Counter for saved photos
    timer_active = False
    timer_start = 0
    countdown = 3  # Default countdown

    while True:
        ret, frame = capture.read()
        if not ret:
            break

        frame = cv.flip(frame, 1)
        h, w = frame.shape[:2]
        
        # Create buttons
        button_y = h - BUTTON_HEIGHT - BUTTON_MARGIN
        button3 = create_button(frame, "3s", BUTTON_MARGIN, button_y, 
                              BUTTON_WIDTH, BUTTON_HEIGHT, WHITE)
        button5 = create_button(frame, "5s", BUTTON_MARGIN * 2 + BUTTON_WIDTH, button_y,
                              BUTTON_WIDTH, BUTTON_HEIGHT, WHITE)
        button10 = create_button(frame, "10s", BUTTON_MARGIN * 3 + BUTTON_WIDTH * 2, button_y,
                               BUTTON_WIDTH, BUTTON_HEIGHT, WHITE)
        
        # Create capture button (red)
        capture_button = create_button(frame, "Capture", w - BUTTON_WIDTH - BUTTON_MARGIN, button_y,
                                     BUTTON_WIDTH, BUTTON_HEIGHT, RED)

        # Handle timer logic
        if timer_active:
            elapsed = time.time() - timer_start
            remaining = max(0, countdown - int(elapsed))
            
            if remaining > 0:
                # Display countdown
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
                # Take the photo
                capture_photo(frame, photo_count)
                photo_count += 1
                timer_active = False

        # Display the frame
        cv.imshow("Camera", frame)

        # Handle keyboard input
        key = cv.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('3'):
            countdown = 3
            timer_active = True
            timer_start = time.time()
        elif key == ord('5'):
            countdown = 5
            timer_active = True
            timer_start = time.time()
        elif key == ord('1'):  # For 10 seconds
            countdown = 10
            timer_active = True
            timer_start = time.time()
        elif key == ord('c'):  # Capture button
            capture_photo(frame, photo_count)
            photo_count += 1
    
    capture.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    cam()