'''import cv2
from multiprocessing import Process, Queue
from Queue import Empty



def image_display(tasks):
	while(1):
		image=tasks.get()
		cv2.imshow('image_display',image)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			cap.release()
		
			cv2.destroyAllWindows()
			break



if __name__=='__main__':

	tasks=Queue()
	cv2.namedWindow("image_display")
	cap = cv2.VideoCapture(0)
	p=Process(target=image_display,args=(tasks))
	p.start()

	while cap.isOpened():
		ret,frame=cap.read()
		if ret==0:
			break

		tasks.put(frame)
			
	p.join()
	cv2.DestroyAllWindows()'''




	
#TRYING MULTIPROCESSING

from multiprocessing import Process, Queue
from Queue import Empty
from PIL import Image
import cv2

import numpy as np

def image_display(taskqueue):
   #cv2.namedWindow ('image_display', cv2.CV_WINDOW_AUTOSIZE)
   a=0
   while a!=2:
      a=2
      print(a)
      image = taskqueue.get()              # Added
      if image is None:
         print 3
         break             # Added
      cv2.imshow ('image_display3', image)  # Added
      if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break
        '''
      if taskqueue.get()==None:
         continue
      else:
         image = taskqueue.get()
         im = Image.fromstring(image['mode'], image['size'], image['pixels'])
         num_im = np.asarray(im)
         cv2.imshow ('image_display3', num_im)
         '''

if __name__ == '__main__':
   taskqueue = Queue()
   vidFile = cv2.VideoCapture(0)
   p = Process(target=image_display, args=(taskqueue,))
   p.start()
   while vidFile.isOpened():
      print 1
      flag, image=vidFile.read()
      taskqueue.put(image)  # Added
      image_display(taskqueue)
      print 4
      import time           # Added
      time.sleep(0.010)     # Added
      continue              # Added

      if flag == 0:
         break
      im = Image.fromarray(image)
      im_dict = {
      'pixels': im.tostring(),
      'size': im.size,
      'mode': im.mode,
      }
      taskqueue.put(im_dict)

taskqueue.put(None)
p.join()
cv2.DestroyAllWindows()