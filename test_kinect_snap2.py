import freenect
import cv2
import numpy as np
import datetime


#freenect.set_depth_mode(, freenect.RESOLUTION_MEDIUM, freenect.DEPTH_MM)


#function to get RGB image from kinect
def get_video():
    array,_ = freenect.sync_get_video()
    array = cv2.cvtColor(array,cv2.COLOR_RGB2BGR)
    return array
 
#function to get depth image from kinect
def get_depth():
    array,_ = freenect.sync_get_depth(0,format=freenect.DEPTH_MM)
    #array = array.astype(np.uint16)
    #array = array * 32
    return array

#function to get depth array from kinect
def get_depth_array():
    array,_ = freenect.sync_get_depth()
    return array    
 
 
if __name__ == "__main__":
    while 1:
        #get a frame from RGB camera
        frame = get_video()
        #get a frame from depth sensor
        depth = get_depth()
        #get an array from depth
        darray = get_depth_array()
        
        #display RGB image
        cv2.imshow('RGB image',frame)
        #display depth image
        cv2.imshow('Depth image',depth)
 
 
        # quit program when 'esc' key is pressed
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
        elif k == 100:
			print '"d" key pressed, saving depth image to npy binary'
			ts = datetime.datetime.now()
			filenamed = "{}DEPTHMM".format(ts.strftime("%H_%M_%S"))
			np.save(filenamed,depth,allow_pickle=False)
			print 'DONE - npy'
			print 'saving RGB image to file RGB.png'
			filenamer = "{}RGB.png".format(ts.strftime("%H_%M_%S"))
			cv2.imwrite( filenamer, frame)		
			print 'DONE - RGB'
    cv2.destroyAllWindows()
