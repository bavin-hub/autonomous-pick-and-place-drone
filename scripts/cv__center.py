import cv2
import numpy as np

video = cv2.VideoCapture(1)

while True:
    _, frame = video.read()
    
    x, y, c = frame.shape
    print(frame.shape)
    frame_circle = cv2.circle(frame, (320, 240), 2, (255,0,0), 2)
    cv2.imshow("vid", frame_circle)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

video.release()
cv2.destroyAllWindows()