import cv2
import numpy as np
from math import *

WINDOW_NAME1 = 'frame'


lower_val=[97,145,187]
upper_val=[123,255,255]#light blue

def hsv_image(image,lower_val,upper_val):
    blur = cv2.GaussianBlur(image, (5,5),0) # blur to reduce noise
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV) #Convert BGR to HSV

#Threshold of HSV for a particular color as np array
    lower = np.array(lower_val)
    upper = np.array(upper_val)
    #Masking to get thresholded image
    mask = cv2.inRange(hsv,lower,upper)

#Blur the mask
    bmask = cv2.GaussianBlur(mask, (5,5),0)

    return bmask



def centroid(bmask,image):
    ctr=(-1,-1)
    moments1 = cv2.moments(bmask)
    m001 = moments1['m00']
    centroid_x1, centroid_y1 = None, None
    if m001 != 0:
        centroid_x1 = int(moments1['m10']/m001)
        centroid_y1 = int(moments1['m01']/m001)
    # Assume no centroid
    

    if centroid_x1!=None and centroid_y1!=None:
        
        ctr=(centroid_x1, centroid_y1)
        cv2.circle(image, ctr, 5, (0,0,255))
        cv2.circle (image,(0,0),5,(255,0,0))
    '''cv2.imshow(WINDOW_NAME1, image)
    if cv2.waitKey(1) & 0xFF == 27:
        ctr = None'''

    return ctr
#CHANGE THE FUNCTION IF CIRCLE IS NOT REQUIRED


# its important to give double underscore 
if __name__=='__main__':
    cap=cv2.VideoCapture(1)
    while(cap.isOpened()):
        k=(0,0) 
        ret,frame = cap.read()
        a=hsv_image(frame,[176,147,205],[179,168,255])
        b=hsv_image(frame,[0,147,205],[3,168,255])
        d=a
        e=b
        res=cv2.bitwise_or(a,b)
        
        k=centroid(a,frame)
        print(k)
        cv2.imshow('a',a)
        cv2.imshow('b',b)
        cv2.imshow('c',res)
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break
    cap.release()
    cv2.destroyAllWindows()