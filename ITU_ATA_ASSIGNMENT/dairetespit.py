import cv2
import numpy as np
from math import atan2, degrees, radians
import time


mavi_alt_sinir=np.array([85,100,80])
mavi_ust_sinir=np.array([132,255,255])

def logofcircle(centerx,centery,cx,cy):
    file=open('flightlogs.txt','a')
    file.write(f"The X value of Blue circle's: {cx} , the Y value of Blue circle's: {cy},the angle between origin and circle center: {get_angle(centerx,centery,cx,cy)}\n")
    file.close

def get_angle(centerx,centery,cx,cy):
    angle = -atan2(cy - centery, cx - centerx)
    angle = degrees(angle)
    return angle

def find_blue_circle():
    sayac=0
    kamera=cv2.VideoCapture(0)
    centerx = int(kamera.get(cv2.CAP_PROP_FRAME_WIDTH)/2)
    centery = int(kamera.get(cv2.CAP_PROP_FRAME_HEIGHT)/2)
    starting=time.time()
    while True:
        sayac+=1
        ret,goruntu=kamera.read()
        goruntu = cv2.flip(goruntu, 1)
        goruntu_hsv=cv2.cvtColor(goruntu,cv2.COLOR_BGR2HSV)
        mask=cv2.inRange(goruntu_hsv,mavi_alt_sinir,mavi_ust_sinir)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)   # saçımdaki contourların gitmesi
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True),True)
            area = cv2.contourArea(cnt)
            if len(approx)  > 8  and area>1000 :
                    
                #using moments to calc center of shape
                M = cv2.moments(cnt)
                cx = int(M["m10"]/M["m00"])
                cy = int(M["m01"]/M["m00"])
                cv2.line(goruntu, (centerx, centery), (cx, cy), (0, 0, 255), 3)
                cv2.putText(goruntu, "X: {} - Y: {}".format(cx, cy), (15, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                cv2.putText(goruntu, f'Angle: {get_angle(centerx,centery,cx,cy)}', (15, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                cv2.circle(goruntu, (cx, cy), 5, (0, 0, 255), -1)
                goruntu = cv2.drawContours(goruntu, contours, -1, (0, 0, 255), 3)
                logofcircle(centerx,centery,cx,cy)
    

        cv2.imshow("Searching circle", goruntu)
        
        ending=time.time()
        if ending-starting>8:
            print(ending-starting)
            print(sayac)
            kamera.release()
            cv2.destroyAllWindows()
            break
            
    
