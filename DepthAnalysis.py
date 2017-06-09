# Import Block
import numpy as np
import time
import datetime
import cv2
import freenect

# Variable Block (all variables are coded in seconds)
frame_rate = 0.5
total_time = 720


def mode(ndarray, axis=0):
    if ndarray.size == 1:
        return (ndarray[0], 1)
    elif ndarray.size == 0:
        raise Exception('Attempted to find mode on an empty array!')
    try:
        axis = [i for i in range(ndarray.ndim)][axis]
    except IndexError:
        raise Exception('Axis %i out of range for array with %i dimension(s)' % (axis, ndarray.ndim))
    srt = np.sort(ndarray, axis=axis)
    dif = np.diff(srt, axis=axis)
    shape = [i for i in dif.shape]
    shape[axis] += 2
    indices = np.indices(shape)[axis]
    index = tuple([slice(None) if i != axis else slice(1, -1) for i in range(dif.ndim)])
    indices[index][dif == 0] = 0
    indices.sort(axis=axis)
    bins = np.diff(indices, axis=axis)
    location = np.argmax(bins, axis=axis)
    mesh = np.indices(bins.shape)
    index = tuple([slice(None) if i != axis else 0 for i in range(dif.ndim)])
    index = [mesh[i][index].ravel() if i != axis else location.ravel() for i in range(bins.ndim)]
    counts = bins[tuple(index)].reshape(location.shape)
    index[axis] = indices[tuple(index)]
    modals = srt[tuple(index)].reshape(location.shape)
    return (modals, counts)

# Object Block
class DepthMap(object):
    """The current depth map received via the freenect.get_sync_video command. Used to split data into different fields and validate behavior.
    Also used to run different functions on easily.

    Attributes:
        Timestamp: time when the object was created. Useful for sanity checking
        DataMap: Actual array of numbers for every pixel in the frame
        Background: Most recently generated background, used to segment out objects and their changes. Class is the new 'Background' class
        FishCheck: Logical Array identfifying which pixels belong to a fish, for easy analysis information
        BadCheck: Logical Array identifying pixels who are being thrown out (either out of range and not fish, entropic noise, etc...)
        BackgroundCheck: Logical Array, true where the DataMap pixels represent the background and false where they don't
    """

    def __init__(self, Background):
        # Creates the DepthMap object for us to later muck around with
        self.bad_data = 2047
        self.update_rate = 60
        self.bad_thresh = 1000
        self.fish_thresh = 30
        self.lower_edge = 20
        self.upper_edge = 100
        self.DataMap, self.Timestamp = freenect.sync_get_depth()
        self.Background = Background
        self.BadCheck = self.FindBad()
        self.FishCheck = self.FindFish()
        self.BackgroundCheck = self.FindBackground()
        self.AnalyzeFish()

    def FindBad(self):
        DummyBad = np.zeros(shape=(480, 640))
        DummyBad[self.DataMap == self.bad_data] = 1
        DummyBad[(self.DataMap - self.Background.Map) > self.bad_thresh] = 1
        return DummyBad

    def FindFish(self):
        # Run image analysis on the DepthMap, generate the FishCheck array to identify fish pixels
        DummyFish = np.zeros(shape=(480, 640))
        DummyFish[(self.DataMap - self.Background.Map) > self.fish_thresh] = 1
        DummyFish[self.BadCheck == 1] = 0
        Outlines = cv2.Canny(self.DataMap, self.upper_edge, self.lower_edge)
        strel = cv2.getStructuringElement(cv2.MORPH_CIRCLE, (3, 3))
        Outlines = cv2.dilate(Outlines, strel, iterations=1)
        LabelInfo = cv2.connectedComponentsWithStats(Outlines, 8, cv2.CV_32S)
        Labeled = LabelInfo[1]
        for Line in range(1, max(Labeled)):
            if sum(DummyFish == 1 & Labeled == Line) > 0:  # Possibly need to change to and instead of &
                DummyFish[Labeled == Line] = 1
        # Now fill in the holes
        floodfill = DummyFish.copy()
        h, w = DummyFish.shape[:2]
        mask = np.zeros((h + 2, w + 2), np.uint8)
        cv2.floodFill(floodfill, mask, (0, 0), 255)
        InvFloodfill = cv2.bitwise_not(floodfill)
        DummyFish = DummyFish | InvFloodfill
        return DummyFish

    def FindBackground(self):
        DummyBack = np.ones(shape=(480, 640))
        DummyBack[self.BadCheck == 1] = 0
        DummyBack[self.FishCheck == 1] = 0
        self.Background.TotalColorValues += np.multiply(DummyBack, self.DataMap)
        self.Background.ValidPixelCount += DummyBack
        self.Background.TotalUpdateCount += 1
        # Include block about triggering update code here
        if self.Background.TotalUpdateCount >= self.update_rate:
            self.Background.update()
        return DummyBack

    def AnalyzeFish(self):
        # Include the saving step here perhaps, to keep from needing more noise in the DepthMap attributes
        output = cv2.connectedComponentsWithStats(self.FishCheck, 4, cv2.CV_32S)
        stats = output[2]
        np.save(NAME, stats)
        copy = self.FindFish()
        for Line in range(1, output[0]):
            copy = cv2.rectangle(copy, (stats[Line, 1], stats[Line, 2]), ((stats[Line, 1] + stats[Line, 3]), (stats[Line, 2] + stats[Line, 4])), (255,255,255), 3)
        cv2.imshow("Bounded Fish", copy)
        cv2.waitKey(1)




class Background(object):
    """
        Attributes:
        Timestamp
        Map
        TotalColorValues
        ValidPixelCount
        TotalUpdateCount
        """

    def __init__(self, delay, THRESH):
        self.Timestamp = time.time()
        #   Use try/catch outside to see if error
        #   Grab 100 frames, check validity.
        count = 1
        frames = np.empty(shape=(480, 640, 100))
        while count < 100:
            frames[:, :, count] = freenect.sync_get_depth()
            count += 1
        check, _ = mode(frames, 2)
        stat, validation = Background.validate(check, delay, THRESH)
        if stat:
            self.Map = validation
        else:
            raise ValueError('Initial Background included fish')

    @staticmethod
    def validate(check, delay, difference_thresh):
        time.sleep(delay)
        count = 1
        frames = np.empty(shape=(480, 640, 100))
        while count < 100:
            frames[:, :, count] = freenect.sync_get_depth()
            count += 1
        validation, _ = mode(frames, 2)
        comparison = abs(check - validation)
        if sum(comparison) < difference_thresh:
            return 1, validation
        else:
            return 0, validation

    def update(self):
        new_background = np.divide(self.TotalColorValues, self.ValidPixelCount)
        self.Map = new_background
        self.TotalColorValues = np.zeros(shape=(480, 640))
        self.ValidPixelCount = np.zeros(shape=(480, 640))
        self.TotalUpdateCount = 0

    #   possibly roll the saving into the update code
    def save(self):
        name = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H-%M-%S')
        np.save(name, self.Map)

#Code Block
Bower = 0
while not Bower:
    try:
        Bower = Background(300, 50)
    except ValueError as err:
        print(err.args)
        continue

ct = 1
empty = np.zeros(shape=(480, 640))
cv2.imshow('Bounded Fish', empty)
cv2.waitKey(1)
while ct < total_time:
    start = time.time()
    DepthMap(Bower)
    ct += 1
    end = time.time()
    waittime = frame_rate - (end - start)
    time.sleep(waittime)