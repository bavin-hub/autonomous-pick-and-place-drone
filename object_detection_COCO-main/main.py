import cv2
thres = 0.45

cap = cv2.VideoCapture(1)
cap.set(3, 1280)
cap.set(4, 720)
cap.set(10, 70)

classnames = []
with open('C:\drone\object_detection_COCO-main\labels.txt', 'rt') as file:
    classnames = file.read().rstrip('\n').split('\n')

configPath = 'object_detection_COCO-main/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'object_detection_COCO-main/frozen_inference_graph.pb'

net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320, 320)
net.setInputScale(1.0/127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

while True:
    _, img = cap.read()
    classIds, confs, bbox = net.detect(img, confThreshold=thres)
    print(classIds, bbox)

    if len(classIds) !=0 :
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
            xmin = box[0]
            ymin = box[1]
            xmax = box[2]
            ymax = box[3]
            x = (xmin+xmax)//2
            y = (ymin+ymax)//2
            cv2.rectangle(img, box, color=(250, 0, 0), thickness=2)
            cv2.putText(img,classnames[classId-1].upper(),(box[0]+10,box[1]+30),
            cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
            cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
            cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
            cv2.circle(img, (x,y), 2, (255,0,0), 2)
    
    cv2.imshow('OUTPUT', img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()