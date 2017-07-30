import cv2    #9954245078 harshit
import numpy
cv2.namedWindow('track')
def nothing(x):
    pass
cv2.createTrackbar('lowH','track',0,179,nothing)
cv2.createTrackbar('highH','track',179,179,nothing)
cv2.createTrackbar('lowS','track',0,255,nothing)
cv2.createTrackbar('highS','track',49,255,nothing)
cv2.createTrackbar('lowV','track',94,255,nothing)
cv2.createTrackbar('highV','track',255,255,nothing)

cap=cv2.VideoCapture(0)

while cap.isOpened():
    ret,frame=cap.read()
    lH=cv2.getTrackbarPos('lowH','track')
    hH=cv2.getTrackbarPos('highH','track')
    lS=cv2.getTrackbarPos('lowS','track')
    hS=cv2.getTrackbarPos('highS','track')
    lV=cv2.getTrackbarPos('lowV','track')
    hV=cv2.getTrackbarPos('highV','track')
    lower=numpy.array([lH,lS,lV])
    upper=numpy.array([hH,hS,hV])

    blur=cv2.GaussianBlur(frame, (5,5),0) # blur to reduce noise
    hsv1=cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    #hsv2 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #Convert BGR to HSv
    #Masking to get thresholded image
    mask = cv2.inRange(hsv1,lower,upper)

#Blur the mask
    bmask = cv2.GaussianBlur(mask, (5,5),0)
    
    #res=cv2.bitwise_and(frame,frame,mask=bmask)
    cv2.imshow('frame',frame)
    cv2.imshow('masked',bmask)
    k=cv2.waitKey(5)& 0xFF
    if k==27:
        break
release()
destroyAllWindows()