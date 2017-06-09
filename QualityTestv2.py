from freenect import sync_get_depth as get_depth, sync_get_video as get_video
import cv2
import numpy as np
import time

def qualtest(integer):
    warm_up, _ = get_depth()
    time.sleep(5)
    cf0, _ = get_depth()
    all_data = cf0[np.newaxis, ...]
    ts0=time.time()
    ts=ts0
    count=0
    while ts-ts0 < 60:
        cf, _ = get_depth()
        ts = time.time()
        if ts > count * 0.4 + ts0:
            all_data = np.vstack([all_data, cf[np.newaxis, ...]])
            count+=1
    #all_data[all_data == 0] = np.nan
    np.save('bower_test_tank42_depth'+str(integer), all_data)

integer=1
warm_up, _ = get_depth()
warm_up, _ = get_video()
time.sleep(5)
Color=get_video()
time.sleep(2)
np.save('bower_test_tank42_color',Color)
while integer<=20:
    ts=time.time()
    qualtest(integer)
    integer+=1
    to=time.time()
    time.sleep(300-(to-ts))
