import freenect
import cv2
import numpy as np
import datetime
import time

from picamera.array import PiRGBArray
from picamera import PiCamera
from imutils.video.pivideostream import PiVideoStream


 
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

# initialize the camera and grab a reference to the raw camera capture
    
stream = PiVideoStream()
stream.start()
#camera = PiCamera()
#camera.resolution = (640, 480)
#camera.framerate = 32
#rawCapture = PiRGBArray(camera, size=(640, 480))
 
# allow the camera to warmup
time.sleep(1)
     
 
 
if __name__ == "__main__":
    while 1:
        #get a frame from RGB camera
        #frame = get_video()
        #get a frame from depth sensor
        depth = get_depth()
        #display RGB image
        #cv2.imshow('RGB image',frame)
        #display depth image
        cv2.imshow('Depth image',depth)
       
        frame = stream.read()
        cv2.imshow('pi camera', frame)
		
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
    stream.stop()
