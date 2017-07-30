


import cv2
import numpy as np
import time
from Arduino import Arduino


def track(image):


    # Blur the image to reduce noise
    blur1 = cv2.GaussianBlur(image, (5,5),0)
    blur2 = cv2.GaussianBlur(image, (5,5),0)

    # Convert BGR to HSV
    hsv1 = cv2.cvtColor(blur1, cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(blur2, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image for only green colors
    lower_pink = np.array([49,35,28])
    upper_pink = np.array([76,255,225])
    lower_green = np.array([154,43,81])
    upper_green = np.array([179,255,255])

    # Threshold the HSV image to get only green colors
    mask1 = cv2.inRange(hsv1, lower_pink, upper_pink)
    mask2 = cv2.inRange(hsv2, lower_green, upper_green)
    
    # Blur the mask
    bmask1 = cv2.GaussianBlur(mask1, (5,5),0)
    bmask2 = cv2.GaussianBlur(mask2, (5,5),0)

    # Take the moments to get the centroid
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

    # Assume no centroid
    ctr1 = (-1,-1)
    ctr2 = (-1,-1)

    # Use centroid if it exists
    if centroid_x1 != None and centroid_y1 != None and centroid_x2 != None and centroid_y2!=None:

        ctr1 = (centroid_x1, centroid_y1)
        ctr2 = (centroid_x2, centroid_y2)
        if ctr1[1] in range(375):
            if ctr1[0] in range(160):
                bot(ctr1,ctr2)
            elif ctr1[0] in range(160,320):
                bot(ctr1,ctr2)
            elif ctr1[0] in range(320,480):
                bot(ctr1,ctr2)
            else:
                bot(ctr1,ctr2)

        #print ctr1

        # Put black circle in at centroid in image
        cv2.circle(image, ctr1, 4, (0,0,255))
        cv2.circle(image, ctr2, 4, (0,255,0))
	#cv2.circle(image,(int(x1.value[0][0]),int(x2.value[0][0])),  4, (255,0,0))
    # Display full-color image
    cv2.imshow('WINDOW_NAME1', image)
    # cv2.imshow('mask1',mask1)
    # cv2.imshow('mask2',mask2)

    # Force image display, setting centroid to None on ESC key input
    if cv2.waitKey(1) & 0xFF == 27:
       # ctr1 = None
        ctr2 = None
    
    # Return coordinates of centroid
    return ctr1,ctr2


def bot(ctr1,ctr2):
   # move the bot to ctr1[0]
    return 0


