import freenect
import cv2
import numpy as np
import datetime
import time
import threading

from picamera.array import PiRGBArray
from picamera import PiCamera
from imutils.video.pivideostream import PiVideoStream
import imutils

#timer: in seconds
#timeout= time.time() + 60 * 60 * 12

timer =60*60*4
 
#function to get RGB image from kinect
def get_video():
	array,_ = freenect.sync_get_video()
	array = cv2.cvtColor(array,cv2.COLOR_RGB2BGR)
	return array
 
#function to get depth image from kinect
def get_depth():
	array,_ = freenect.sync_get_depth()
	array = array.astype(np.uint8)
	#array = array * 32
	return array
#nitialize the camera and grab a reference to the raw camera capture

#res = '(640, 480)'    
stream = PiVideoStream(resolution=(640,480)).start()
stream.start()
#camera = PiCamera()
#camera.resolution = (640, 480)
#camera.framerate = 30
 
# allow the camera to warmup
time.sleep(1)

if __name__ == "__main__":
	while 1:
		#get a frame from RGB camera
		frame = stream.read()
		#get a frame from depth sensor
		depth = get_depth()

		
		#display RGB image
				

		frame = imutils.resize(frame, 350)
		cv2.imshow('pi image',frame)
		#get a frame from depth sensor
		depth = get_depth()
		#depth = cv2.applyColorMap(depth, cv2.COLORMAP_JET)
		depth = imutils.resize(depth, 350)
		cv2.imshow('depth',depth)
		
	
		#stop if timeout
		#if time.time() > timeout:
		#	break    
		# quit program when 'esc' key is pressed
		k = cv2.waitKey(5) & 0xFF
		if k == 27:
			break
	cv2.destroyAllWindows()
	#Stop all data streams from kinect
	freenect.sync_stop()
	stream.stop()
