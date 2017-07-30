#!/usr/bin/env python



import cv2
import numpy as np

# For OpenCV2 image display
WINDOW_NAME1 = 'PinkBallTracker'
# Write a function 'filter' that implements a multi-
# dimensional Kalman Filter for the example given
arrx=[]
arry=[]
from math import *

class matrix:
    
    # implements basic operations of a matrix class
    
    def __init__(self, value):
        self.value = value
        self.dimx = len(value)
        self.dimy = len(value[0])
        if value == [[]]:
            self.dimx = 0
    
    def zero(self, dimx, dimy):
        # check if valid dimensions
        if dimx < 1 or dimy < 1:
            raise ValueError, "Invalid size of matrix"
        else:
            self.dimx = dimx
            self.dimy = dimy
            self.value = [[0 for row in range(dimy)] for col in range(dimx)]
    
    def identity(self, dim):
        # check if valid dimension
        if dim < 1:
            raise ValueError, "Invalid size of matrix"
        else:
            self.dimx = dim
            self.dimy = dim
            self.value = [[0 for row in range(dim)] for col in range(dim)]
            for i in range(dim):
                self.value[i][i] = 1
    
    def show(self):
        for i in range(self.dimx):
            print self.value[i]
        print ' '
    
    def __add__(self, other):
        # check if correct dimensions
        if self.dimx != other.dimx or self.dimy != other.dimy:
            raise ValueError, "Matrices must be of equal dimensions to add"
        else:
            # add if correct dimensions
            res = matrix([[]])
            res.zero(self.dimx, self.dimy)
            for i in range(self.dimx):
                for j in range(self.dimy):
                    res.value[i][j] = self.value[i][j] + other.value[i][j]
            return res
    
    def __sub__(self, other):
        # check if correct dimensions
        if self.dimx != other.dimx or self.dimy != other.dimy:
            raise ValueError, "Matrices must be of equal dimensions to subtract"
        else:
            # subtract if correct dimensions
            res = matrix([[]])
            res.zero(self.dimx, self.dimy)
            for i in range(self.dimx):
                for j in range(self.dimy):
                    res.value[i][j] = self.value[i][j] - other.value[i][j]
            return res
    
    def __mul__(self, other):
        # check if correct dimensions
        if self.dimy != other.dimx:
            raise ValueError, "Matrices must be m*n and n*p to multiply"
        else:
            # subtract if correct dimensions
            res = matrix([[]])
            res.zero(self.dimx, other.dimy)
            for i in range(self.dimx):
                for j in range(other.dimy):
                    for k in range(self.dimy):
                        res.value[i][j] += self.value[i][k] * other.value[k][j]
            return res
    
    def transpose(self):
        # compute transpose
        res = matrix([[]])
        res.zero(self.dimy, self.dimx)
        for i in range(self.dimx):
            for j in range(self.dimy):
                res.value[j][i] = self.value[i][j]
        return res
    
    # Thanks to Ernesto P. Adorio for use of Cholesky and CholeskyInverse functions
    
    def Cholesky(self, ztol=1.0e-5):
        # Computes the upper triangular Cholesky factorization of
        # a positive definite matrix.
        res = matrix([[]])
        res.zero(self.dimx, self.dimx)
        
        for i in range(self.dimx):
            S = sum([(res.value[k][i])**2 for k in range(i)])
            d = self.value[i][i] - S
            if abs(d) < ztol:
                res.value[i][i] = 0.0
            else:
                if d < 0.0:
                    raise ValueError, "Matrix not positive-definite"
                res.value[i][i] = sqrt(d)
            for j in range(i+1, self.dimx):
                S = sum([res.value[k][i] * res.value[k][j] for k in range(self.dimx)])
                if abs(S) < ztol:
                    S = 0.0
                res.value[i][j] = (self.value[i][j] - S)/res.value[i][i]
        return res
    
    def CholeskyInverse(self):
        # Computes inverse of matrix given its Cholesky upper Triangular
        # decomposition of matrix.
        res = matrix([[]])
        res.zero(self.dimx, self.dimx)
        
        # Backward step for inverse.
        for j in reversed(range(self.dimx)):
            tjj = self.value[j][j]
            S = sum([self.value[j][k]*res.value[j][k] for k in range(j+1, self.dimx)])
            res.value[j][j] = 1.0/tjj**2 - S/tjj
            for i in reversed(range(j)):
                res.value[j][i] = res.value[i][j] = -sum([self.value[i][k]*res.value[k][j] for k in range(i+1, self.dimx)])/self.value[i][i]
        return res
    
    def inverse(self):
        aux = self.Cholesky()
        res = aux.CholeskyInverse()
        return res
    
    def __repr__(self):
        return repr(self.value)

x1 = matrix([[0.], [0.]]) # initial state (location and velocity)
P = matrix([[1000., 0.], [0., 1000.]]) # initial uncertainty
u = matrix([[0.], [0.]]) # external motion
F = matrix([[1., 1.], [0, 1.]]) # next state function
H = matrix([[1., 0.]]) # measurement function
R = matrix([[1.]]) # measurement uncertainty
Q=matrix([[100., 0.], [0., 100.]])#covariance of process noise
I = matrix([[1., 0.], [0., 1.]]) # identity matrix
x2 = matrix([[0.], [0.]]) # initial state (location and velocity)
P1 = matrix([[1000., 0.], [0., 1000.]]) # initial uncertainty
u1 = matrix([[0.], [0.]]) # external motion
F1 = matrix([[1., 1.], [0, 1.]]) # next state function
H1 = matrix([[1., 0.]]) # measurement function
R1 = matrix([[1.]]) # measurement uncertainty



def track(image):


    # Blur the image to reduce noise
    blur1 = cv2.GaussianBlur(image, (5,5),0)
    blur2 = cv2.GaussianBlur(image, (5,5),0)

    # Convert BGR to HSV
    hsv1 = cv2.cvtColor(blur1, cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(blur2, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image for only green colors
    lower_pink = np.array([120,120,100])
    upper_pink = np.array([240,240,255])
    lower_green = np.array([40,0,70])
    upper_green = np.array([80,200,200])

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
	cv2.circle(image,(int(x1.value[0][0]),int(x2.value[0][0])),  4, (255,0,0))
    # Display full-color image
    cv2.imshow(WINDOW_NAME1, image)

    # Force image display, setting centroid to None on ESC key input
    if cv2.waitKey(1) & 0xFF == 27:
       # ctr1 = None
        ctr2 = None
    
    # Return coordinates of centroid
    return ctr1,ctr2
#easurements=[]

def bot(ctr1,ctr2):
   # move the bot to ctr1[0]
    return 0


def kalman_filterx1():
    #for i in range(len(measurements)):
    global arrx
    for i in range(len(arrx)):        
	z=matrix([[arrx[i]]])
	
        # measurement update
	global S,K,x1,P
        y=z-H*x1
        S=H*P*H.transpose()+R
        K=P*H.transpose()*S.inverse()
        x1=x1+K*y
        P=(I-K*H)*P+I
        
        # prediction
        x1=u+F*x1
        P=F*P*F.transpose()+Q
    return 0
def kalman_filterx2():
    for i in range(len(arry)):
	z=matrix([[arry[i]]])
        # measurement update
	global x2,s1,K1,P1
        y=z-H1*x2
        S1=H1*P1*H1.transpose()+R1
        K1=P1*H1.transpose()*S1.inverse()
        x2=x2+K1*y
        P1=(I-K1*H1)*P1
        
        # prediction
        x2=u+F*x2
        P1=F1*P1*F1.transpose() +Q
    return 0




# Test with input from camera
if  __name__ == '__main__':

    capture = cv2.VideoCapture(0)

    while True:

        okay, image = capture.read()

    	if okay:
	    #for i in range(100):
            ctr1,ctr2=track(image)
	    arrx.append(ctr1[0])
	    arry.append(ctr1[1])
	    #if (len(arrx)>=50):
		#arrx=[]
		#x1 = matrix([[0.], [0.]]) # initial state (location and velocity)
		#P = matrix([[1000., 0.], [0., 1000.]]) # initial uncertainty
		#u = matrix([[0.], [0.]]) # external motion
		#F = matrix([[1., 1.], [0, 1.]]) # next state function
		#H = matrix([[1., 0.]]) # measurement function
		#R = matrix([[1.]]) # measurement uncertainty
	    #if (len(arry)>=50):
		#arry=[]
		#x2 = matrix([[0.], [0.]]) # initial state (location and velocity)
		#P1 = matrix([[1000., 0.], [0., 1000.]]) # initial uncertainty
		#u1 = matrix([[0.], [0.]]) # external motion
		#F1 = matrix([[1., 1.], [0, 1.]]) # next state function
		#H1 = matrix([[1., 0.]]) # measurement function
		#R1 = matrix([[1.]]) # measurement uncertainty
	
	    kalman_filterx1()
	    
	    kalman_filterx2()
	    
	   # print kalman_filter(x,P)
	    
            if not ctr1:
                break
          
            if cv2.waitKey(1) & 0xFF == 27:
                break

        else:

           print('Capture failed')
           break


