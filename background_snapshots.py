import numpy as np
import time
import freenect
import cv2
from scipy.stats import mode
import datetime

#function to get depth array from kinect
def get_depth_array():
	array,_ = freenect.sync_get_depth()
	array = array.astype('float')
	return array    


minute = 0

while minute < 5:
    starttime = time.time()
    count = 0
    snapshot = np.empty(shape=(480, 640, 10))
    while count < 10:
		
        snapshot[:, :, count] = get_depth_array()
        snapshot[snapshot==2047]= np.nan
        count = count + 1
        print count
        print 'count'
    
    valid = np.nanmean(snapshot, 2)
    st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S')
    np.save(st, valid)
    
    minute += 5
    print minute
    print 'min'
    newtime = time.time()
    waittime = 300 - (newtime - starttime)
    time.sleep(waittime)

freenect.sync_stop()

