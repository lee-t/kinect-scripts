import freenect
import cv2
import numpy as np
import datetime

#function to get RGB image from kinect
def get_video():
    array,_ = freenect.sync_get_video()
    array = cv2.cvtColor(array,cv2.COLOR_RGB2BGR)
    return array
 
#function to get IR image from kinect
def get_IRvideo():
    array,_ = freenect.sync_get_video(0,format=freenect.VIDEO_IR_8BIT)
    #array = cv2.cvtColor(array,cv2.COLOR_RGB2BGR)
    return array
 
#function to get depth image from kinect
def get_depth():
    array,_ = freenect.sync_get_depth()
    #array = array.astype(np.uint16)
    array = array * 32
    return array
    
 
 
if __name__ == "__main__":
    while 1:
        #get a frame from RGB camera
        #frame = get_video()
        #display RGB image
        #cv2.imshow('RGB image',frame)
        
        #get a frame from depth sensor
        depth = get_depth()
        #display depth image
        cv2.imshow('Depth image',depth)
        #get a frame from IR camera
        IRframe = get_IRvideo()
        #display depth image
        cv2.imshow('IR image',IRframe)
 
        # quit program when 'esc' key is pressed
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
        elif k == 115:
			print '"s" key pressed, saving RGB image to file RGB.jpg'
			ts = datetime.datetime.now()
			filename = "IR.png".format(ts.strftime("%H_%M_%S"))
			cv2.imwrite( filename, IRframe)
        elif k == 100:
			print '"d" key pressed, saving depth image to file DEPTH.jpg'
			ts = datetime.datetime.now()
			filename = "{}DEPTH.png".format(ts.strftime("%H_%M_%S"))			
			cv2.imwrite( filename, depth)
    cv2.destroyAllWindows()
    #Stop all data streams from kinect
    freenect.sync_stop()
