import picamera
import datetime
import time
import logging
import argparse

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--timer", type=int, default=60,
	help="timer in seconds")
ap.add_argument("-l", "--log", type=str, default="log.txt",
	help="path to output log file")
args = vars(ap.parse_args())

timer = args["timer"]

# todo: improve loggging, intergrationwith kinect? class?

# open the logging file
logging.basicConfig(filename=args["log"], level=logging.DEBUG)
 
# initialize the video stream and allow the cammera sensor to
# warmup
logging.info("[{}] waiting for camera to warmup".format(
	datetime.datetime.now()))

with picamera.PiCamera() as camera:
    camera.resolution = (1280, 720)
    videoname = datetime.datetime.now().strftime("%a-%d-%b-%Y-%H_%M_%S")
    time.sleep(2)
    
    camera.start_recording(videoname +".h264")
    
    logging.info () "started recording"
    camera.wait_recording(timer)
    camera.stop_recording()
    print "stopped recording"
