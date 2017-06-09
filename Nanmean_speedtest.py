import numpy as np
import time

Array = np.random.randint(0, 1023, size=(480, 640, 500))
#print(Array)

Start=time.time()
Average=np.nanmean(Array, 2)
end=time.time()
print(end-Start)
