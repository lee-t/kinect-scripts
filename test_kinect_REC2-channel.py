import freenect
import cv2
import numpy as np
import datetime
import time
 
#timer: in seconds
timeout= time.time() + 60 

count =0
 
#function to get RGB image from kinect
def get_video():
	array,_ = freenect.sync_get_video()
	array = cv2.cvtColor(array,cv2.COLOR_RGB2BGR)
	return array
 
#function to get depth image from kinect raw
def get_depth_array():
	array,_ = freenect.sync_get_depth()
	#array = array.astype(np.uint8)
	#array = array * 32
	return array
	
#function to get depth array from kinect for video
def get_depth_arrayEncode():
	array,timestamp = freenect.sync_get_depth()
	# constrain from less than
	np.clip(array,245,500,array)
	array = array - 245
	array = array.astype(np.uint8)
	return array     

def get_depth_array32():
	array,timestamp = freenect.sync_get_depth()
	# constrain from less than
	c = (array >> 8) & 0xff
	f = array & 0xff
	z = np.zeros(array.shape)
	c = c.astype(np.float)
	f = f.astype(np.float)
	arrayn = cv2.merge([c, f, z])
	return arrayn    
      
d= '/home/pi/Videos/testdepth4.h264'
rgb = '/home/pi/Videos/testRGB4.h264'
#deine the codec and create videowriter obj
fourcc = cv2.VideoWriter_fourcc('X','2','6','4')
out_d = cv2.VideoWriter(d,fourcc,5.0,(640,480))    
out_RGB = cv2.VideoWriter(rgb,fourcc,5.0,(640,480))    

if __name__ == "__main__":
	while time.time() < timeout:
		#get a frame from RGB camera
		frame = get_video()
		#get a frame from depth sensor
		depth = get_depth_array32()
		#record depth to file
		
		out_d.write(np.uint8(depth))
		out_RGB.write(frame)
		
		#display RGB image
		#cv2.imshow('RGB image',frame)
		#display depth image
		#cv2.imshow('Depth image',depth)
		
		count = count+1
		print count
		#stop if timeout
		#if time.time() > timeout:
		#	break    
		# quit program when 'esc' key is pressed
		k = cv2.waitKey(5) & 0xFF
		if k == 27:
			break


	#Stop all data streams from kinect
	freenect.sync_stop()
	
	out_d.release()
	#out_RGB.release()
	cv2.destroyAllWindows()

