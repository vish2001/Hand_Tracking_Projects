import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
#################################
wcam=640
hcam=480

#################################
cap = cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)
ptime =0
detector = htm.handdetector(detectconf=0.8)
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volrange = volume.GetVolumeRange()
volmin = volrange[0]
volmax = volrange[1]
volbar=0
volper=0
while True:
    success, img = cap.read()
    detector.findhands(img)
    lmlist, bbox = detector.findposition(img,draw=False)
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

        #hand range : 50 - 300
        #volume range :-65 - 0
        vol = np.interp(length,[50,300],[volmin,volmax])
        volbar = np.interp(length, [50, 300], [400, 150])
        volper = np.interp(length, [50, 300], [0, 100])
        #print(int(length),vol)
        volume.SetMasterVolumeLevel(vol, None)
        if length<50:
            cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
    cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
    cv2.rectangle(img, (50, int(volbar)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f': {int(volper)}%', (40, 450), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
    ctime= time.time()
    fps = 1/(ctime - ptime)
    ptime = ctime
    cv2.putText(img,f'FPS: {int(fps)}',(40,70),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),3)
    cv2.imshow("img",img)
    cv2.waitKey(1)