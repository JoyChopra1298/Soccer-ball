#!/usr/bin/env python



import cv2
import numpy as np

# For OpenCV2 image display
WINDOW_NAME1 = 'frame'
# Write a function 'filter' that implements a multi-
# dimensional Kalman Filter for the example given
arrx=[]
arry=[]
from math import *
bmask3=None
cap=cv2.VideoCapture(1)

# returns hsv image of a particular color
def track(image):


    # Blur the image to reduce noise
    blur1 = cv2.GaussianBlur(image, (5,5),0)
    blur2 = cv2.GaussianBlur(image, (5,5),0)
    blur3 = cv2.GaussianBlur(image, (5,5),0)
    # Convert BGR to HSV
    hsv1 = cv2.cvtColor(blur1, cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(blur2, cv2.COLOR_BGR2HSV)
    hsv3 = cv2.cvtColor(blur3, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image for only green colors
    lower_ball = np.array([0,73,118])
    upper_ball = np.array([16,255,255])
    lower_botcol1 = np.array([59,128,73])
    upper_botcol1 = np.array([97,204,170])
    lower_botcol2=np.array([138,155,64])
    upper_botcol2=np.array([179,218,227])



    # Threshold the HSV image to get only green colors
    mask1 = cv2.inRange(hsv1, lower_ball,upper_ball)
    mask2 = cv2.inRange(hsv2,lower_botcol1,upper_botcol1)
    mask3 =cv2.inRange(hsv3,lower_botcol2,upper_botcol2)
    
    # Blur the mask
    bmask1 = cv2.GaussianBlur(mask1, (5,5),0)
    bmask2 = cv2.GaussianBlur(mask2, (5,5),0)
    
    bmask3 = cv2.GaussianBlur(mask3, (5,5),0)
    
    return bmask1,bmask2,bmask3

    # Take the moments to get the centroid
# calculate centroid
def centroid(bmask1,bmask2,bmask3,image):

    moments1 = cv2.moments(bmask1)
    m001 = moments1['m00']
    centroid_x1, centroid_y1 = None, None
    if m001 != 0:
        centroid_x1 = int(moments1['m10']/m001)
        centroid_y1 = int(moments1['m01']/m001)
        
    moments2 = cv2.moments(bmask2)
    m002 = moments2['m00']
    centroid_x2, centroid_y2 = None, None
    if m002 != 0:
        centroid_x2 = int(moments2['m10']/m002)
        centroid_y2 = int(moments2['m01']/m002)

    moments3 = cv2.moments(bmask3)
    m003 = moments3['m00']
    centroid_x3, centroid_y3 = None, None
    if m003 != 0:
        centroid_x3 = int(moments3['m10']/m003)
        centroid_y3 = int(moments3['m01']/m003)

    # Assume no centroid
    ctr_ball = (-1,-1)
    ctr_botcol1= (-1,-1)
    ctr_botcol2 = (-1 -1)

    # Use centroid if it exists
    if centroid_x1 != None and centroid_y1 != None and centroid_x2 != None and centroid_y2!=None and centroid_y3!=None:

        ctr_ball = (centroid_x1, centroid_y1)
        ctr_botcol1 = (centroid_x2, centroid_y2)
        ctr_botcol2= (centroid_x3,centroid_y3)

        

       

        # Put black circle in at centroid in image
        cv2.circle(image, ctr_ball, 5, (0,0,255))    
        cv2.circle(image, ctr_botcol1, 5, (0,255,0)) 
        cv2.circle(image, ctr_botcol2,5,(255,0,0))
	#cv2.circle(image,(int(x1.value[0][0]),int(x2.value[0][0])),  4, (255,0,0))
    # Display full-color image
    cv2.imshow(WINDOW_NAME1, image)
    cv2.imshow('test', bmask2)

    # Force image display, setting centroid to None on ESC key input
    if cv2.waitKey(1) & 0xFF == 27:
        ctr_botcol1 = None
        ctr_ball = None
        ctr_botcol2= None
    
    # Return coordinates of centroid
    return ctr_ball,ctr_botcol1,ctr_botcol2

while(cap.isOpened()):
    

    ret,frame = cap.read()
    x,y,z=track(frame)
    a,b,c=centroid(x,y,z,frame)
    print (a,b,c)
    cv2.imshow('frame',frame)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break
   
cap.release()
cv2.destroyAllWindows()





 