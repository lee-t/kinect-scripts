import picamera
import datetime
import time

timer = 60 * 60 * (6)

with picamera.PiCamera() as camera:
    camera.resolution = (1920, 1080)
    videoname = datetime.datetime.now().strftime("%a-%d-%b-%Y-%H_%M_%S")
    time.sleep(2)
    camera.start_preview()
    camera.start_recording("/media/pi/WDpassport/Videos/6h_1080P_" + videoname + ".h264")
    
    print "started recording"
    camera.wait_recording(timer)
    camera.stop_recording()
    print "stopped recording"
