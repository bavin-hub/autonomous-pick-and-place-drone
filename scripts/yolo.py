import cv2
import numpy as np

# net = cv2.dnn.readNet("dnn_model/yolov4-tiny.weights", "dnn_model/yolov4-tiny.cfg")
model = cv2.dnn_DetectionModel("dnn_model/yolov4-tiny.weights", "dnn_model/yolov4-tiny.cfg")
model.setInputSize(320,320)

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    (class_ids, scores, bboxes) = model.detect(frame, confThreshold=0.4)
    for class_id, score, bbox in zip(class_ids, scores, bboxes):
        (x,y,w,h) = bbox
        print(x, y, w, h)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (250,0,0), 3)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key==ord("q"):
        break

cap.release()
cv2.destroyAllWindows()