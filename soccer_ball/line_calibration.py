import cv2
import numpy as np 
from math import *
cap=cv2.VideoCapture(1)
ret,frame = cap.read();
height,width = frame.shape[:2]

left=[]
right=[]
p=0
q=height/2
x=width
y=height/2
n=5
a=''
print (height,width)
while(cap.isOpened()):
	ret,frame = cap.read();
	height,width = frame.shape[:2]
	a=raw_input("give inst ")
	if a=='d':
		p=p+n
	elif a=='a':
		p=p-n
	elif a=='s':
		q=q-n
	elif a=='w':
		q=q+n
	elif a=='1':
		x=x-n
	elif a=='3':
		x=x+n
	elif a=='5':
		y=y+n
	elif a=='2':
		y=y-n
	if (p>width or p<0):
		p= abs(width-abs(p))
	if (q>height or q<0):
		q= abs(height-abs(q))
	if (x>width or x<0):
		x= abs(width - abs(x))
	if (y>height or y<0):
		y= abs(height-abs(y))
	print(p,q,x,y)
	'''if q<(height-30) or s>30:
		s=5
	else:
		s=25'''

	cv2.circle(frame,(p,q),10,(0,255,0))
	cv2.circle(frame,(x,y),10,(0,0,255))
	#cv2.line (frame,())
	cv2.line(frame,(p,q),(x,y),(255,0,0),5)

	cv2.imshow('frame',frame)
	if (cv2.waitKey(30) & 0xff==ord('q')):
		cap.release()
		cv2.destroyAllWindows()
		break


cap.release()
cv2.destroyAllWindows()


