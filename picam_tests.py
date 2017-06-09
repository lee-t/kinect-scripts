#!/usr/bin/python

import os
import time
import picamera


# Test list of Exposure and White Balance options. 9 photos.
list_ex  = ['1','2','3','4','5','6','7']
list_res = ['1920x1080','2592x1944','2592x1944','1296x972','1296x730','640x480','640x480']

# Photo dimensions and rotation
#photo_width  = 1920
#photo_height = 1080
#photo_rotate = 180

photo_interval = 0.5 # Interval between photos (seconds)
photo_counter  = 0   # Photo counter

total_photos = len(list_ex)

# Delete all previous image files
try:
  os.remove("vid_*.h264")
except OSError:
  pass



# Lets start taking photos!
try:
	print("Starting video")
	for ex in list_ex:
		mode = int(ex)
		res_num = list_res[photo_counter]
		filename = 'vid_mode_' + ex + '_' + res_num + '.h264'
		print(' [' + str(photo_counter) + ' of ' + str(total_photos) + '] ' + filename) 
		camera = picamera.PiCamera(sensor_mode= mode )
		camera.rotation=photo_rotate
		camera.annotate_background = picamera.Color('black')
		camera.annotate_foreground = picamera.Color('white')
		camera.start_preview()
		time.sleep(2)
		camera.annotate_text = filename
		camera.start_recording (filename)
		camera.wait_recording(60)
		camera.stop_recording()
		photo_counter = photo_counter + 1
		camera.close()
		print "done"
		time.sleep(photo_interval)
  
	print("Finished video sequence")
  
except KeyboardInterrupt:
  # User quit
  print("\nGoodbye!")
