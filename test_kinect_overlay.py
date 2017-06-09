import freenect
import cv2
import numpy as np
import datetime
import imutils
 
#function to get RGB image from kinect
def get_video():
	array,_ = freenect.sync_get_video()
	array = cv2.cvtColor(array,cv2.COLOR_RGB2BGR)
	return array


#function to get depth array from kinect
def get_depth_array():
    array,_ = freenect.sync_get_depth()
    return array    	

	
widthframe = 400 
 
if __name__ == "__main__":
	while 1:
		
		#get a frame from RGB camera
		
		frame = get_video()
		frame = imutils.resize(frame, widthframe)
		#get a frame from depth sensor
		depth = get_depth_array()
		valid_data_indices = depth < 2047
		ret, mask = cv2.threshold(depth, 255, 255, cv2.THRESH_BINARY)

		depth = cv2.applyColorMap(depth, cv2.COLORMAP_JET)
		depth = imutils.resize(depth, widthframe)

		#display RGB image
		#cv2.imshow('RGB image',frame)
		#display depth image
		#cv2.imshow('Depth image',depth)
 
		final = cv2.addWeighted(frame,0.5,depth,0.5,0)
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
