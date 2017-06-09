import picamera
import datetime
import time

timer = 60 

with picamera.PiCamera() as camera:
    camera.resolution = (2592, 1944)
    camera.framerate = 10
    videoname = datetime.datetime.now().strftime("%a-%d-%b-%Y-%H_%M_%S")
    time.sleep(2)
    camera.start_preview()
    camera.start_recording("/media/pi/WDpassport/Videos/30m_superres_" + videoname + ".mjpeg", format=mjpeg
    
    print "started recording"
    camera.wait_recording(timer)
    camera.stop_recording()
    print "stopped recording"
