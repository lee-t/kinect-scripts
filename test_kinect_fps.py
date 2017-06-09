import freenect
import cv2
import numpy as np
import datetime
import time
from imutils.video import FPS
import argparse
import imutils

# USAGE
# python picamera_fps_demo.py
# python picamera_fps_demo.py --display 1
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames", type=int, default=100,
	help="# of frames to loop over for FPS test")
ap.add_argument("-d", "--display", type=int, default=-1,
	help="Whether or not frames should be displayed")
args = vars(ap.parse_args())
 
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

print("[INFO] sampling kinect frames...")
fps = FPS().start()      
# loop over some frames...this time using the threaded stream
while fps._numFrames < args["num_frames"]:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	frame = get_depth_arrayEncode()
	frame = imutils.resize(frame, width=400)

	# check to see if the frame should be displayed to our screen
	if args["display"] > 0:
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

	# update the FPS counter
	fps.update()

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))


# do a bit of cleanup
cv2.destroyAllWindows()
freenect.sync_stop()
