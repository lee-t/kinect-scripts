import numpy as np
import time

x=250
array = (np.random.rand(x,480,640)*2047).astype('float16')
st = time.time()
val = np.std(array, axis=0)
et=time.time()
print(et-st)