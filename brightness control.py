import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
import screen_brightness_control as sbc

#################################
wcam=640
hcam=480

#################################
cap = cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)
ptime =0
detector = htm.handdetector(detectconf=0.8)
brightness = sbc.get_brightness()
bbar = 0
while True:
    success, img = cap.read()
    detector.findhands(img)
    lmlist,bbox = detector.findposition(img,draw=False)

    if len(lmlist) !=0:
        #print(lmlist[4],lmlist[8])
        x1, y1 = lmlist[4][1],lmlist[4][2]
        x2, y2 = lmlist[8][1],lmlist[8][2]
        cx, cy = (x1 + x2)//2,(y1 + y2)//2
        cv2.circle(img,(x1,y1),10,(255,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),10,(255,0,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        cv2.circle(img,(cx,cy),10,(255,0,255),cv2.FILLED)
        length = math.hypot(x2-x1,y2-y1)
        bmin = 0
        bmax = 100
        brightness = np.interp(length, [50, 300], [bmin, bmax])
        bbar = np.interp(length,[50,300],[400,150])

        sbc.set_brightness(int(brightness))
        if length<50:
            cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(img, (50, int(bbar)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img,f': {int(brightness)}%',(40,450),cv2.FONT_HERSHEY_SIMPLEX,2, (255, 0, 0), 3)
    ctime= time.time()
    fps = 1/(ctime - ptime)
    ptime = ctime
    cv2.putText(img,f'FPS: {int(fps)}',(40,70),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),3)
    cv2.imshow("img",img)
    cv2.waitKey(1)