import datetime
import cv2
import numpy as np
from math import atan2, degrees
import time

mavi_alt_sinir=np.array([85,100,80])    #   https://cvexplained.wordpress.com/2020/04/28/color-detection-hsv/#:~:text=The%20HSV%20values%20for%20true,10%20and%20160%20to%20180.
mavi_ust_sinir=np.array([132,255,255])  #   detection of blue HSV numbers by using that website

def logofcircle(centerx,centery,cx,cy): # save detected circle's datas
    file=open('flightlogs.txt','a')
    file.write(f"Camera Active Time:{datetime.datetime.now()}\n")
    file.write("The X value of Blue circle's: {} , the Y value of Blue circle's: {},the angle between origin and circle center: {}\n".format(cx,cy,get_angle(centerx,centery,cx,cy)))
    file.close

def get_angle(centerx,centery,cx,cy):  # angle of origin point and blue circle center
    angle = -atan2(cy - centery, cx - centerx)  # multiply by (-) to make the angle counterclockwise with respect to x-axis
    angle = degrees(angle)      #   https://www.codegrepper.com/code-examples/python/python+get+angle+between+two+points
    return angle

def find_blue_circle():
    kamera=cv2.VideoCapture(0)
    #https://stackoverflow.com/questions/39953263/get-video-dimension-in-python-opencv
    width  = kamera.get(cv2.CAP_PROP_FRAME_WIDTH)   # float width
    height = kamera.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float height
    # It gives width and height of file or camera as float (so you may have to convert to integer)
    centerx=(int(width))/2
    centery=(int(height))/2  # center coordinates of camera
    start_time=time.time()  # start time of camera 
    while True:
        ret,goruntu=kamera.read()
        goruntu = cv2.flip(goruntu, 1)  # to escape of inverse view
        goruntu_hsv=cv2.cvtColor(goruntu,cv2.COLOR_BGR2HSV) # change of color space format to detect by color difference
        mask=cv2.inRange(goruntu_hsv,mavi_alt_sinir,mavi_ust_sinir) # detection of blue object
        #https://www.geeksforgeeks.org/python-morphological-operations-in-image-processing-opening-set-1/
        # defining the kernel
        kernel = np.ones((5, 5), np.uint8)
        # defining the opening function over the image and kernel
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)    # Opening operation is used for removing internal noise in an image.
        contours, __ = cv2.findContours(opening, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE) # find edge points
        for cnt in contours:  # https://www.codimp.com/python-opencv-sekil-tespiti
            approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True),True)
            if len(approx) > 8 : # if edge lines are more than 8 , it seems circle
                M = cv2.moments(cnt)    #  The function computes moments.
                cx = int(M["m10"]/M["m00"])
                cy = int(M["m01"]/M["m00"])
                cv2.putText(goruntu, "X: {} - Y: {}".format(cx, cy), (15, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                cv2.putText(goruntu, f'Angle: {get_angle(centerx,centery,cx,cy)}', (15, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                goruntu = cv2.drawContours(goruntu, contours, -1, (0, 0, 255), 3) # draw all the contours found by method  
                cv2.circle(goruntu, (cx, cy), 5, (0, 0, 255), -1) # highlighted center of circle
                logofcircle(centerx,centery,cx,cy) # if there is a circle then save datas
        cv2.imshow("Searching circle", goruntu)
        finish_time=time.time() # finish time of countors
        if cv2.waitKey(10) and (finish_time-start_time)>=10: # controlling of camera for 10 seconds execution
                kamera.release()
                cv2.destroyAllWindows()
                print("Camera deactivated")  # report to terminal that camera was closed.
                file=open('flightlogs.txt','a')
                file.write(f"Camera Deactivated Time:{datetime.datetime.now()}\n") # log of camera closing time
                file.close()
                break

