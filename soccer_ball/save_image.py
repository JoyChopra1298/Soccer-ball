import cv2
cap = cv2.VideoCapture(0)
picName = 'watch5050.jpeg'
while(cap.isOpened()):
	s, img = cap.read()
	k = cv2.waitKey(33)
	if k==ord('a'):
		cv2.imwrite(picName, img)
		break

