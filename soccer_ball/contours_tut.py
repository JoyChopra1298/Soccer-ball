import cv2
import numpy as np
from math import *

from color_tracking import hsv_image,centroid
cap=cv2.VideoCapture(0)

lower_val=[43,52,99]
upper_val=[115,244,201]

while(cap.isOpened()):
    ret,frame = cap.read()

    a=hsv_image(frame,lower_val,upper_val)
    
    cv2.imshow('a',a)

    #findContours modifies the final image So make a copy if u want the original image
    im2, contours, hierarchy = cv2.findContours(a,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(a, contours, -1, (0,255,0), 3)

    cv2.drawContours(frame, contours, -1, (0,255,0), 3)
    #cv2.imshow('frame',frame)
    
    #cv2.imshow('a',a)
    #print (contours)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break
cap.release()
cv2.destroyAllWindows()
