import freenect
import cv2
import numpy as np
import datetime
import time
 
#timer: in seconds
timeout= time.time() + 60 * 10

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
      
 
#deine the codec and create videowriter obj
fourcc = cv2.VideoWriter_fourcc('X','2','6','4')
out_d = cv2.VideoWriter('/media/pi/WDpassport/Kinect/10m_4fdepth.h264',fourcc,4.0,(640,480),False)    
out_RGB = cv2.VideoWriter('/media/pi/WDpassport/Kinect/10m_4fRGB.h264',fourcc,4.0,(640,480))    

if __name__ == "__main__":
	while time.time() < timeout:
		#get a frame from RGB camera
		frame = get_video()
		#get a frame from depth sensor
		depth = get_depth_arrayEncode()
		#record depth to file
		out_d.write(depth)
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
	out_RGB.release()
	cv2.destroyAllWindows()

