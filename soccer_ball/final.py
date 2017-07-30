# KRITI 2016 GAME OF BOTS

#THE MAIN CODE

#blue camera with lights on 

import cv2
import run_motor  as rm  # Change value of arduino port if required
import numpy as np
from math import *
from color_tracking import hsv_image,centroid
ball_lower=[0,0,125] #white;
ball_upper=[179,96,255]     

ar_lower=[9,104,126]   #yellow
ar_upper=[47,255,126]


botcol1_lower=[97,145,187]    #light_blue(bp)
botcol1_upper=[123,255,255]

botcol2_lower=[136,109,131]   #pink(bp)
botcol2_upper=[166,255,255]

oppar_lower=[101,0,40]   
oppar_upper=[142,109,190]

opp1col_lower=[43,84,101]    #green(og)
opp1col_upper=[87,255,255]

opp2col_lower1=[176,147,205]
opp2col_upper1=[179,168,255] #orange1
opp2col_lower2=[0,147,205]
opp2col_upper2=[3,168,255] #orange2
#camera blue
p=[30,285]# centerline 
q=[460,260]
x=[160,450] # my yellow goal line
y=[370,430]
'''
x=[155,55]         #my blue goal line
y=[350,55]
'''
#camera black
'''
p=[]      
q=[]
x=[]    #my yellow goal line                                               change
y=[]
#x=[]  #my blue goal line   
#y=[]

'''
def defend():
    print ("defend mode")
    move_To(bot_centroid,((x[0]+y[0])/2,(x[1]+y[1])/2),jersey_vector,1)
    allign_opp(bot_centroid,ctr_opp)
line2_vect=(x[0]-y[0],x[1]-y[1])    #Nearer to my goal post
line1_vect=(p[0]-q[0],p[1]-q[1])    #  near to arena line
case=None
# height =480 width =640
# case 1: defend when the ball on the opponent side 



def attack(image):
    print("attack mode")
    
    ctr_ball= centroid(ball_mask,image)

    botball_vector=(ctr_ball[0]-bot_centroid[0],ctr_ball[1]-bot_centroid[1])
    #Align the bot to the bot-ball vector and pick the ball
    pick_error=20   # keep distance for picking ball                                    # change
    diff=0
    diff=move_To(bot_centroid,ctr_ball,jersey_vector,pick_error)
    print(diff)
    if diff<0:

        pick()   #Modify according need
        #Move to line_1(arena centre line) and kick the ball
        dif=move_To(bot_centroid,((p[0]+q[0])/2,(p[1]+q[1])/2),jersey_vector,5)         # change pick error
        if dif<0:
            kick(jersey_vector,bot_centroid,ctr_opp)
    


def move_To(bot_ctr,dest,jer_vect,pk_error):
    botdest_vect= (dest[0]-bot_ctr[0],dest[1]-bot_ctr[1])
    cp=allign_To(jer_vect,botdest_vect)
    print cp
    d=dist(bot_ctr,dest)
    if cp<10:   # CHANGE ACCORDING TO NEED
        #print("move_forward")
        rm.move_forward()
        if d<=pk_error:
            stop()
    return (d-pk_error)

def allign_To(jer_vect,botdest_vect):
    cp=cross_pdt(jer_vect,botdest_vect)
    #dp=dot_pdt(jer_vect,botdest_vect)
    if cp>=0 and cp<=0.1:                                                      # cp range
        cp=cross_pdt(jer_vect,botdest_vect)
    if cp<0:
            #print("move_right")
            rm.move_left()
    elif cp>0:
            
        #print("move_right")
        rm.move_right()
    return cp

def dist(p,q):
    d=(p[1]-q[1])**2+(p[0]-q[0])**2
    return d/mean

def cross_pdt(a,b):
    return (a[0]*b[1]-a[1]*b[0])/(((a[0]**2+a[1]**2)**0.5)*(b[0]**2+b[1]**2)**0.5)

def allign_opp(bot_ctr,opp_ctr):
    allign_To(jersey_vector,line2_vect)
    line2_vect_perp = -line2_vect[0]/line2_vect[1]        #vector perpendicular to line_2
    #Calculate distance(scaled) of opp_ctr from line passing thorugh bot_ctr and slope line2_vect_perp
    d = (opp_ctr[1] - bot_ctr[1]) - line2_vect_perp*(opp_ctr[0] - bot_ctr[0])
    safe_distance = 0           #need to change it later
    while abs(d)>=safe_distance:
        if d>0:               #might need to interchange forward and backward
            #print("move_forward")
            rm.move_forward()
        else:
            #print("move_backward")


            rm.move_backward()

def kick(jersey_vector,bot_ctr,opp_ctr):
    #align along line1 and move away from opponent
    allign_To(jersey_vector,line1_vect)
    line1_vect_perp = (-line1_vect[1],line1_vect[0])        #vector perpendicular to line_2
    #Calculate distance(scaled) of opp_ctr from line passing thorugh bot_ctr and slope line1_vect_perp
    d = (opp_ctr[1] - bot_ctr[1]) - line1_vect_perp*(opp_ctr[0] - bot_ctr[0])



    safe_distance = 25                                                             #change it


    if  abs(d)<=safe_distance:
        if d>0:
            #might need to interchange forward and backward
            #print("move_forward")
            rm.move_forward()
        else:
            #print("move_backward")
            rm.move_backward()   
    #now since away from opponent so shoot after aligning correctly
    
    else :
        allign_To(jersey_vector,line1_vect_perp)
        #print("hit")
        rm.hit()


cap=cv2.VideoCapture(0)

while (cap.isOpened()):

    ret,frame = cap.read()


    height, width=frame.shape[:2]
    global mean
    mean=(height+width)/2   
    global ball_mask
    ball_mask=hsv_image(frame,ball_lower,ball_upper)
    # Assuming arena line is parallel to x-axis
    ball_ctr=centroid(ball_mask,frame)
    ctr_botcol1=centroid(hsv_image(frame,botcol1_lower,botcol1_upper),frame)
    ctr_botcol2=centroid(hsv_image(frame,botcol2_lower,botcol2_upper),frame)
    global bot_centroid
    bot_centroid=((ctr_botcol1[0]+ctr_botcol2[0])/2,(ctr_botcol1[1]+ctr_botcol2[1]))
    opp1= centroid(hsv_image(frame,opp1col_lower,opp1col_upper),frame)
    opp2= centroid(hsv_image(frame,opp2col_lower,opp2col_upper),frame)
    global ctr_opp
    ctr_opp=(0,0)
    ctr_opp=((opp1[0]+opp2[0])/2,(opp1[1]+opp2[1])/2)
    global jersey_vector
    jersey_vector=(0,0)
    jersey_vector=((ctr_botcol2[0]-ctr_botcol1[0]),(ctr_botcol2[1]-ctr_botcol1[1]))
    k=0
    #cv2.line(cv2.line(frame,(ctr_botcol1[0],ctr_botcol1[1]),(ctr_botcol2[0],ctr_botcol2[1]),(255,0,0),5))
    #cv2.line(frame,(opp1[0],opp1[1]),(opp2[0],opp2[1]),(0,180,0),5)
    cv2.line(frame,(p[0],p[1]),(q[0],q[1]),(0,0,255),5)
    cv2.line(frame,(x[0],x[1]),(y[0],y[1]),(255,0,0),5)
    cv2.imshow('frame',frame)
    
    if cv2.waitKey(30) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break
    k=ball_ctr[1]-p[1]-(y[0]-p[1])*(ball_ctr[0]-p[0])/(x[0]-p[0])
    if k<0:
        c='attack'    
    else:
        c='defend'

    #switch case in python with default case
    if c=='attack':
        attack(frame)
    elif c=='defend':
        defend()

    
        
cap.release()
cv2.destroyAllWindows()
















''' attack case
1.Move towards ball
jersey_vector
bot-ball vector
rotating jersey vextor  || to bot-ball then move towars ball and stop at fixed changeable distance from the ball

2. Catch the ball- servo movement 
check ball is inside bot

3.orient and move the ball for kick

4.kick

defend case ---the easy one
1. move and orient to a predefined line
2.detect enemy jersey center
3. orient parallel to arena line
4. align your one coordinate wrt enemy and block'''




