## case of intra-distance

x = np.array([1,2,3]) # list 1 and 2, they are the same
B = np.fromfunction(lambda i, j: i < j, (x.shape[0],x.shape[0])) #element for which to calculate distances

def dist_func(a, b):
    return (a+b)*.5

av, bv = np.meshgrid(x,x, sparse=True)
f_vect = np.vectorize(dist_func)
## divide between processors


np.where(B, dist_func(av, bv), None) #slice B, av and bv for each processors

def my_func(i, x, B):
    av, bv = np.meshgrid(x[i], x[i+1:], sparse=True)
    return f_vect(av, bv) ## then convert to sparse. Note that the array of i needs a_i += i when combining with others, while a_j += i + 1


def f(r, x, q):
    for _ in r:
        data = f_vect(*np.meshgrid(x[_+1:], x[_], sparse=True))
	# get indexes where data not 0, argwhere?
        q.put((data[data > 0], _, _+1+indexes)))

import cython
from cython.parallel import prange
for i in prange(B.shape[0]-1, nogil=True):
    my_func(i, x, B)
print(res)

import multiprocessing as mp
#initialise s_d, s_i, s_j as shared arrays of length x.shape[0]*x.shape[0]
#set all in s_d = 0
q = mp.Queue()
for i in range(nproc):
    p = mp.Process(target=f, args=(xrange(i,x.shape[0],nproc), x, q))
    p.start()

