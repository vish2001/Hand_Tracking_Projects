import cv2
import mediapipe as mp
import time
import math
import numpy as np

class handdetector():
    def __init__(self,mode=False,maxhands=2,detectconf=0.5,trackconf=0.5):
        self.mode = mode
        self.maxhands = maxhands
        self.detectconf = detectconf
        self.trackconf = trackconf
        self.mphands = mp.solutions.hands
        self.mpdraw =  mp.solutions.drawing_utils
        self.hands = self.mphands.Hands(self.mode,self.maxhands,self.detectconf)
        self.tipIds = [4, 8, 12, 16, 20]

    def findhands(self,img,draw=True):
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpdraw.draw_landmarks(img,handLms,self.mphands.HAND_CONNECTIONS)
        return img
    def findposition(self,img,handno = 0,draw =True):
        xlist = []
        ylist = []
        bbox = []
        self.lmlist = []
        if self.results.multi_hand_landmarks:
            myhand = self.results.multi_hand_landmarks[handno]
            for id,lm in enumerate(myhand.landmark):
                h,w,c = img.shape
                cx,cy = int(lm.x*w),int(lm.y*h)
                #print(id,cx,cy)
                xlist.append(cx)
                ylist.append(cy)
                self.lmlist.append([id,cx,cy])
                if draw:
                    cv2.circle(img, (cx, cy),5, (255, 0, 255), cv2.FILLED)
        if len(self.lmlist) != 0:
            xmin, xmax = min(xlist), max(xlist)
            ymin, ymax = max(xlist), max(xlist)
            bbox = xmin,ymin,xmax,ymax
            if draw:
                cv2.rectangle(img, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20), (0, 255, 0), 2)
        return self.lmlist,bbox

    def fingersUp(self):
        fingers = []
        if len(self.lmlist) != 0:
            # Thumb
            if self.lmlist[self.tipIds[0]][1] > self.lmlist[self.tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            # Fingers
            for id in range(1, 5):
                if self.lmlist[self.tipIds[id]][2] < self.lmlist[self.tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        # totalFingers = fingers.count(1)

        return fingers

    def findDistance(self, p1, p2, img, draw=True, r=15, t=3):
        x1, y1 = self.lmlist[p1][1:]
        x2, y2 = self.lmlist[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
            length = math.hypot(x2 - x1, y2 - y1)

        return length, img, [x1, y1, x2, y2, cx, cy]


def main():
        pTime = 0
        cTime = 0
        cap = cv2.VideoCapture(0)
        detector = handdetector()
        while True:
            success, img = cap.read()
            img = detector.findhands(img)
            lmlist, bbox = detector.findposition(img)
            if len(lmlist) != 0 :
                print(lmlist[4])
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            #cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
            cv2.imshow("Image", img)
            cv2.waitKey(1)
if __name__ == "__main__":
    main()