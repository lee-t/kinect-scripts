import freenect    
import frame_convert   
import time   
import cv2 as cv
import numpy as np   

cv.namedWindow('Depth')
cv.namedWindow('RGB')
keep_running = True

def display_depth(dev, data, timestamp):   
    global keep_running   
    cv.ShowImage('Depth', frame_convert.pretty_depth_cv(data))  
    #time.sleep(1)   
    if cv.WaitKey(10) == 27:  
       keep_running = False   


def display_rgb(dev, data, timestamp):  
    global keep_running  
    cv.Image= frame_convert.video_cv(data)   
    img = cv.CreateImage(cv.GetSize(cv.Image), cv.IPL_DEPTH_16S, 3)   
    cv.ShowImage('RGB',cv.Image)   
    for x in range(1,5):   
     name= "img%d" %(x)   
     cv.SaveImage('name.png',cv.Image);   
     time.sleep(1)   
    if cv.WaitKey(10) == 27:   
        keep_running = False   

def body(*args):   
    if not keep_running:    
        raise freenect.Kill   

print('Streaming from Kinnect... Please wait...Press ESC in window to stop') 
freenect.runloop(depth=display_depth,
                 video=display_rgb,
                 body=body)
