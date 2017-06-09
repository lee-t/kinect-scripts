import numpy as np
import timeit
from scipy import stats

 
 
def mode(ndarray,axis=0):
		if ndarray.size == 1:
			return (ndarray[0],1)
		elif ndarray.size == 0:
			raise Exception('Attempted to find mode on an empty array!')
		try:
			axis = [i for i in range(ndarray.ndim)][axis]
		except IndexError:
			raise Exception('Axis %i out of range for array with %i dimension(s)' % (axis,ndarray.ndim))
		srt = numpy.sort(ndarray,axis=axis)
		dif = numpy.diff(srt,axis=axis)
		shape = [i for i in dif.shape]
		shape[axis] += 2
		indices = numpy.indices(shape)[axis]
		index = tuple([slice(None) if i != axis else slice(1,-1) for i in range(dif.ndim)])
		indices[index][dif == 0] = 0
		indices.sort(axis=axis)
		bins = numpy.diff(indices,axis=axis)
		location = numpy.argmax(bins,axis=axis)
		mesh = numpy.indices(bins.shape)
		index = tuple([slice(None) if i != axis else 0 for i in range(dif.ndim)])
		index = [mesh[i][index].ravel() if i != axis else location.ravel() for i in range(bins.ndim)]
		counts = bins[tuple(index)].reshape(location.shape)
		index[axis] = indices[tuple(index)]
		modals = srt[tuple(index)].reshape(location.shape)
		return (modals, counts)

# generate array with random int		
a = np.random.random((640, 480, 100))

#create timer objs
#for scipy
ta = timeit.Timer("lambda: stats.mode(a)")
#for def mode
tb = timeit.Timer("lambda: mode(a)")

print 'SCIPYs MODE:'
#iterations
print ta.timeit(1)

print 'DIFFERENT MODE:'
print tb.timeit(1)
