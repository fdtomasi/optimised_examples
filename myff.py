import numpy as np
from time import time

n = 1000
l1 = ['AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHHHHHHHHHBBBBS']*n
l2 = ['AAAAAAAAAAAAAffffffffffffffAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHHHHHHHHHBBBBS']*n
def f():
	t = time()
	for i in l1:
		for j in l2:
			(np.array(list(i)) != np.array(list(j))).mean()
	print "Converting to list then array:", time()-t

def f2(ntype=np.int8):
	t = time()
	for i in l1:
		for j in l2:
			(np.fromstring(i, ntype) != np.fromstring(j, ntype)).mean()
	print ntype, ":", time()-t


f()
f2()
f2(np.uint8)
f2(np.short)

	