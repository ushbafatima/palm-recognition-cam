import cv2 as cv

FRAME_HEIGHT = 480
FRAME_WIDTH = 640
 
# Initialize video capture
capture = cv.VideoCapture(0)

def cam():
    while True:
        ret, frame = capture.read()
        if not ret:
            break
        frame = cv.flip(frame, 1)
        # Display the frame
        cv.imshow("Camera", frame)
        
        
        # Break the loop if 'q' is pressed
        if cv.waitKey(1) & 0xFF == ord('q') or cv.getWindowProperty("Camera", cv.WND_PROP_VISIBLE) < 1:
            break
    
    capture.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    cam()