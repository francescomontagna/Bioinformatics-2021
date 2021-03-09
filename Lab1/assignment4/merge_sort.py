from math import floor
import numpy as np

def merge(ary1, ary2):
    queue = []
    while len(ary1) > 0 and len(ary2) > 0:

        min_val = min(ary1[0][-1], ary2[0][-1])
        if min_val == ary1[0][-1]:
            queue.append(ary1[0]) # append index of the smallest
            flag1 = 1
        else:
            queue.append(ary2[0]) # append index of the smallest
            flag1 = 2

        # delete the number just added to the queue
        if flag1 == 1:
            del ary1[0]
        else:
            del ary2[0]

    # if one array is empty, just extend queue with the remaining sorted portion of the other array
    if len(ary1) > 0:
        queue.extend(ary1)
    else:
        queue.extend(ary2)

    return queue


def mergesort(alignments: list): # list of tuple, each tuple formatted as (read_id, 'sequence')

    if len(alignments) == 1:
        return alignments

    else:  # split and apply double recursion
        n = floor(len(alignments) / 2)
        return merge(mergesort(alignments[:n]), mergesort(alignments[n:]))
