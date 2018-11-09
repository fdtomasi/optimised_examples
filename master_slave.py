#!/usr/bin/env python
# This program uses a master slave approach to consume a queue
# of elaborations


import time
import datetime

from glob import glob
from mpi4py import MPI
from collections import deque
from subprocess import Popen

# constants to use as tags in communications
DO_WORK = 100
EXIT = 200

# VERBOSITY
VERBOSITY = 1


def get_input_names(string):
    """
    get all the input files which name starts with the string "string"
    Returns the list containing the file names
    """
    return glob(string+'*')


def master(inputs):
    """
    dispatch the work among processors.
    queue is a list of input
    return a list of timings
    """
    procs_ = comm.Get_size()
    queue = deque(inputs)  # deque to enable popping from the left

    import numpy as np
    timings = np.zeros(procs_)
    count = 0
    # seed the slaves by sending work to each processor
    for rank in range(1, procs_):
        input_file = queue.popleft()
        comm.send(input_file, dest=rank, tag=DO_WORK)

    # loop until there's no more work to do. If queue is empty skips the loop.
    while queue:
        input_file = queue.popleft()
        # receive result from slave
        status = MPI.Status()
        elapsed_time = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
        timings[status.source] += elapsed_time
        count += 1
        # send to the same slave new work
        comm.send(input_file, dest=status.source, tag=DO_WORK)

    # there's no more work to do, so receive all the results from the slaves
    for rank in range(1, procs_):
        status = MPI.Status()
        elapsed_time = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
        timings[status.source] += elapsed_time
        count += 1

    # tell all the slaves to exit by sending an empty message with the EXIT_TAG
    for rank in range(1, procs_):
        comm.send(0, dest=rank, tag=EXIT)

    return count, timings


def slave():
    """
    slave will spawn the work processes
    """
    while True:
        status_ = MPI.Status()
        input_name = comm.recv(source=0, tag=MPI.ANY_TAG, status=status_)
        # check the tag of the received message
        if status_.tag == EXIT:
            return
        # do the work
        result = worker(input_name)  # result contains the times required for execution
        comm.send(result, dest=0, tag=0)


def worker(input_file):
    """
    spawn the work process
    """
    my_rank_ = comm.Get_rank()
    # import time
    t1_ = time.time()
    # if VERBOSITY:
    #     print "./cash_flow.x %s executed by rank: %s" % (input_file, my_rank_)
    # execution_string = "./cash_flow.x %s" % input_file
    # file_out = open(input_file+".out", "w")
    # process_ = Popen(execution_string.split(), stdout=file_out)
    # process_.wait()
    time.sleep(2)
    t2_ = time.time()
    if VERBOSITY:
        print ' ---> processor %s has calculated for %s' % (my_rank_, t2_-t1_)
    return t2_ - t1_


###############################################################################
#                                                                             #
# --------------------------------- main ------------------------------------ #
#                                                                             #
###############################################################################


if __name__ == '__main__':
    """Run with
    ```mpirun -np 4 python master_slave.py```
    """
    import sys

    comm = MPI.COMM_WORLD
    procs = comm.Get_size()
    my_rank = comm.Get_rank()

    t1 = time.time()
    # timing
    if my_rank == 0:
        print '*'*80
        print '%s -- Calculation started' % datetime.datetime.utcnow()
        print '*'*80
        print procs

    elapsed_times = None
    if my_rank == 0:
        # get the input list
        # input_files = get_input_names(sys.argv[1])
        input_files = ['arg' + str(i) for i in range(10)]
        print 'Number of elaborations: %d' % len(input_files)
        number_of_elaborations, elapsed_times = master(input_files)
        print 'Number of elaborations: %d' % number_of_elaborations
    else:
        slave()

    comm.Barrier()

    if my_rank == 0:
        t2 = time.time()

        for i, time in enumerate(elapsed_times):
            print i, time

        print '*'*80
        print '%s -- Calculation ended after %s seconds' % (datetime.datetime.utcnow(), t2-t1)
        print '*'*80
