"""This shows a comparison in using an hamming distance on a 
couple of strings of the same length. When strings are long,
it is easy to see how the conversion from strings to list is inefficient.

Usage:
    python myff.py
"""

import numpy as np
from time import time

def f0(l1,l2):
    """Version 1: two loops over the two lists.
    Each string in lists is converted to a list, then it is computed the
    Hamming distance between the single chars.
    """
    t = time()
    for i in l1:
        for j in l2:
            (np.array(list(i)) != np.array(list(j))).mean()
    print "Converting to list then array:", time()-t

def f1(l1, l2, ntype=np.int8):
    """Version 2: two loops over the two lists.
    Now each string in the lists is converted into a numpy array
    with the np.fromstring function, with type ntype."""
    t = time()
    for i in l1:
        for j in l2:
            (np.fromstring(i, ntype) != np.fromstring(j, ntype)).mean()
    print ntype, ":", time()-t


@np.vectorize
def _f2(i, j):
    return (np.fromstring(i, np.uint8) != np.fromstring(j, np.uint8)).mean()
	
def f2(l1, l2):
    t = time()	
    _f2(*np.meshgrid(l1, l2, sparse=True))
    print "vect:", time()-t


if __name__ == '__main__':
    n = 1000
    l1 = ['AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHHHHHHHHHBBBBS']*n
    l2 = ['AAAAAAAAAAAAAffffffffffffffAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHHHHHHHHHBBBBS']*n
    f0(l1,l2)
    f1(l1,l2)
    f1(l1,l2,np.uint8)
    f2(l1,l2)	# is actually slower than f1
