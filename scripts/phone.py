import cv2
import numpy as np

cap = cv2.VideoCapture(0)
address = "https://192.168.1.6:8080/video"
cap.open(address)

while True:
    _, frame = cap.read()
    cv2.imshow("img", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()