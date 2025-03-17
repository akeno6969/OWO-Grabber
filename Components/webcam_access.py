# This code is only for the main code to work with
import cv2

def capture_webcam_image():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite("webcam_image.jpg", frame)
    cap.release()

capture_webcam_image()