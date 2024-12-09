
import cv2
import math

config_file = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
frozen_model = 'frozen_inference_graph.pb'

model = cv2.dnn_DetectionModel(frozen_model, config_file)

classLabels = []
filename = 'labels.txt'
with open(filename, 'rt') as spt:
    classLabels = spt.read().rstrip('\n').split('\n')
    
    
model.setInputSize(320, 320)  #greater this value better the reults but slower. Tune it for best results
model.setInputScale(1.0/127.5)
model.setInputMean((127.5, 127.5, 127.5))
model.setInputSwapRB(True)

    
cap = cv2.VideoCapture(0)
ret, frame = cap.read()

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter('video.avi', fourcc, 25, (frame.shape[1], frame.shape[0]))  #25 is the frame rate of output video you can change it as required


font = cv2.FONT_HERSHEY_PLAIN

try:
    while(True):

        ret, frame = cap.read()
        ht, wd, c = frame.shape
        cv2.circle(frame, (wd//2, ht//2), 2, (255,0,0), 2)

        classIndex, confidence, bbox = model.detect(frame , confThreshold=0.40)  #tune the confidence  as required
        if(len(classIndex) != 0):
            for classInd, boxes in zip(classIndex.flatten(), bbox):
                # xmin, ymin, xmax, ymax = boxes
                # cv2.circle(frame, (xmax/2, ymax/2), 2, (255,0,0), 2)
                xmin = boxes[0]
                ymin = boxes[1]
                xmax = boxes[2]
                ymax = boxes[3]
                x = (xmin + xmax)//2
                y = (ymin + ymax)//2
                # d = math.dist([wd, ht], [xmax, ymax])
                # print(d)
                cv2.rectangle(frame, boxes, (255, 0, 0), 2)
                cv2.putText(frame, classLabels[classInd-1], (boxes[0] + 10, boxes[1] + 40), font, fontScale = 1, color=(0, 255, 0), thickness=2)
                cv2.circle(frame, (x, y), 2, (0,255,0), 2)

        video.write(frame)
        cv2.imshow('result', frame)
        cv2.waitKey(2)

except:
    cap.release()
    video.release()
    cv2.destroyAllWindows()

