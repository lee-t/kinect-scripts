import freenect
import cv2
import numpy as np
import datetime
import time
import threading

from picamera.array import PiRGBArray
from picamera import PiCamera
from imutils.video.pivideostream import PiVideoStream

#timer: in seconds
#timeout= time.time() + 60 * 60 * 12

timerclock =60*60*3
 
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
    
#function to get depth array from kinect every 60 sec
def get_depth_snapshot():
	array,_ = freenect.sync_get_depth()
	ts = datetime.datetime.now()
	filenamed = "{}DEPTH11bit".format(ts.strftime("%H_%M_%S"))
	print '[INFO] Saving depth Data at' + filenamed
	np.save(filenamed,array,allow_pickle=False)
	threading.Timer(60, get_depth_snapshot).start()         

# initialize the camera and grab a reference to the raw camera capture

#res = '(640, 480)'    
#stream = PiVideoStream(resolution=(640,480)).start()
#stream.start()
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
 
# allow the camera to warmup
time.sleep(1)

#deine the codec and create videowriter obj
#fourcc = cv2.VideoWriter_fourcc('X','2','6','4')
#out_d = cv2.VideoWriter('/media/pi/WDpassport/Kinect/kinect.h264',fourcc,10.0,(640,480),False)    
#out_RGB = cv2.VideoWriter('/media/pi/WDpassport/Kinect/pi.h264',fourcc,8.0,(640,480))         
 
#get timestamp
st= datetime.datetime.now().strftime("%a-%d-%b-%Y-%H_%M_%S")

#record to .h264
print ("start recording " + st )
camera.start_recording("/media/pi/WDpassport/picam+kinect" + st + ".h264", bitrate=7500000)
get_depth_snapshot()
#time(seconds)
#camera.wait_recording(24 * 60 * 60)
camera.wait_recording(timerclock)
camera.stop_recording()
print "ended recording" 
sys.exit(0)



