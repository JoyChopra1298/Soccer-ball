import serial
import time
ser = serial.Serial('/dev/ttyACM0',9600)

def move_left():
	print('left')
	ser.write('L')
	return 0

def move_right():
	print('right ')
	ser.write('R')
	return 0

def pick_ball():
	print('pick')
	ser.write('P')
	return 0

def hit():
	print('hit')
	ser.write('H')
	ser.write('H')
	return 0

def move_forward():
	print('forward ')
	ser.write('F')
	return 0
	
def move_backward():
	print('backward ')
	ser.write('B')
	return 0

def stop():
	print('stop')
	ser.write('S')
	ser.write ('S')
	return 0

if __name__=='__main__':


	#hit()   
	move_forward()
	
	#move_right()
	stop()
	#move_forward()


