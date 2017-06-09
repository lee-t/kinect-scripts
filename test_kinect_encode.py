import freenect
import cv2
import numpy as np
import datetime
 
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
    
 
#function to get depth array from kinect for video
def get_depth_arrayEncode():
	array,timestamp = freenect.sync_get_depth()
	# constrain from less than 2feet(495) to 3' 1/2 
	np.clip(array,495,750,array)
	array = array - 495
	array = array.astype(np.uint8)
	return array     
 
 
if __name__ == "__main__":
    while 1:
        #get a frame from RGB camera
        frame = get_video()
        #get a frame from depth sensor
        depth = get_depth_arrayEncode()
        #display RGB image
        cv2.imshow('RGB image',frame)
        #display depth image
        cv2.imshow('Depth image',depth)
 
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
			filename = "{}DEPTH".format(ts.strftime("%H_%M_%S"))			
			np.save(filename,depth,allow_pickle=False)
			#cv2.imwrite( filename, depth)
    cv2.destroyAllWindows()
    #Stop all data streams from kinect
    freenect.sync_stop()
