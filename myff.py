"""This shows a comparison in using an hamming distance on a 
couple of strings of the same length. When strings are long,
it is easy to see how the conversion from strings to list is inefficient.

Usage:
    python myff.py
"""

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

@np.vectorize
def _f3(i, j):
    return (np.fromstring(i, np.uint8) != np.fromstring(j, np.uint8)).mean()
	
def f3():
    t = time()	
    _f3(*np.meshgrid(l1, l2, sparse=True))
    print "vect:", time()-t

f4()	# is actually slower than f2
