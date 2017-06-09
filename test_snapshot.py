import numpy as np
import time
import freenect
import cv2
from scipy.stats import mode
import datetime


minute = 1

while minute < 3:
    starttime = time.time()
    count = 1
    snapshot = np.empty(shape=(480, 640, 10))
    while count < 10:
        snapshot[:, :, count] = freenect.sync_get_depth()
        count += 
        l
    minute += 1
    newtime = time.time()
    waittime = 60 - (newtime - starttime)
    time.sleep(waittime)
