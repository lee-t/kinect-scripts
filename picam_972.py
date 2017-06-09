import picamera
import datetime
import time

timer = 60 * 10

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
    camera.start_preview()
    camera.start_recording("10min_1296x972.h264")
    
    print "started recording"
    camera.wait_recording(timer)
    camera.stop_recording()
    print "stopped recording"
