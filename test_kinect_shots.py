import freenect
import cv2
import numpy as np
import datetime
import time

#timer count down
timeout= time.time() + 20

count =0

#freenect.set_depth_mode(, freenect.RESOLUTION_MEDIUM, freenect.DEPTH_MM)


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

#function to get depth array from kinect
def get_depth_array():
	array,_ = freenect.sync_get_depth()
	return array    
	
def get_depth_arrayMM():
	array,_ = freenect.sync_get_depth(0,format=freenect.DEPTH_MM)
	return array    

 
 
if __name__ == "__main__":
	while count < 20:
		#get a frame from RGB camera
		frame = get_video()
		#get a frame from depth sensor
		#depth = get_depth()
		#get an array from depth
		darray = get_depth_array()
		#darray_MM = get_depth_array()
		
		#display RGB image
		cv2.imshow('RGB image',frame)
		#display depth image
		cv2.imshow('Depth image',darray)
 
		#timetime
		if time.time()
		ts = datetime.datetime.now()
		filenamed = "{}DEPTH11bit".format(ts.strftime("%H_%M_%S"))
		
		# quit program when 'esc' key is pressed
		k = cv2.waitKey(5) & 0xFF
		if k == 27:
			break
		time.sleep(5)
		count = count +1
	cv2.destroyAllWindows()
	
 
