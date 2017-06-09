import freenect
import cv2
import numpy as np
import datetime
import imutils

import argparse
import time

 
#function to get RGB image from kinect
def get_video():
	array,_ = freenect.sync_get_video()
	array = cv2.cvtColor(array,cv2.COLOR_RGB2BGR)
	return array


#function to get depth array from kinect
def get_depth_array():
    array,_ = freenect.sync_get_depth()
    return array    	

def get_depth_pretty():
	array,_ = freenect.sync_get_depth()
	np.clip(array, 0,2**10-1,array)
	array >>=2
	array = array.astype(np.uint8)
	return array    

	
widthframe = 400 
 
if __name__ == "__main__":
	while 1:
		
		#get a frame from RGB camera
		
		frame = get_video()
		frame = imutils.resize(frame, widthframe)
		#get a frame from depth sensor
		depth = get_depth_pretty()
		#valid_pixels = depth < 255
		#ret, mask = cv2.threshold(depth, 255, 255, cv2.THRESH_BINARY)
		#bad_pixels = np.zeros(shape=(480,640))
		bad_pixels = np.ma.masked_equal(depth, 255)
		count_bad = bad_pixels.count()
		percent_bad = (float(count_bad) / depth.size) *100
		text = str(percent_bad)
		
		#bad_pixels_inv =cv2.bitwise_not(bad_mask)
		#cv2.imshow('Bad Pixels', bad_pixels)
		
		

		depth = cv2.applyColorMap(depth, cv2.COLORMAP_JET)
		cv2.putText(frame, "bad pixels: {}".format(text), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
		depth = imutils.resize(depth, widthframe)
		depth_bad = imutils.resize(bad_pixels, widthframe)
		depth_mask = cv2.bitwise_not(depth_bad)
		#display RGB image
		#cv2.imshow('RGB image',frame)
		#display depth image
		#cv2.imshow('Depth image',depth)
 
		final = cv2.bitwise_and(frame,frame, mask =depth_mask)
		cv2.imshow('merge', final)
 
		# quit program when 'esc' key is pressed
		k = cv2.waitKey(5) & 0xFF
		if k == 27:
			break
		elif k == 115:
			print '"s" key pressed, saving RGB image to file RGB.jpg'
			ts = datetime.datetime.now()
			filename = "{}RGB.png".format(ts.strftime("%H_%M_%S"))
			cv2.imwrite( filename, frame)
		elif k == 100:
			print '"d" key pressed, saving depth image to file DEPTH.jpg'
			ts = datetime.datetime.now()
			filename = "{}DEPTH.png".format(ts.strftime("%H_%M_%S"))			
			cv2.imwrite( filename, depth)
	cv2.destroyAllWindows()
	#Stop all data streams from kinect
	freenect.sync_stop()
