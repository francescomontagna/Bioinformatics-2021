from math import floor


# Hp: n%2 = 0 ==> n is even
# Later, we'll define not even problem

def merge(ary1, ary2):
    queue = []
    while len(ary1) > 0 and len(ary2) > 0:

        min_val = min(ary1[0][1], ary2[0][1])
        if min_val == ary1[0][1]:
            queue.append(ary1[0]) # append index of the smallest
            flag1 = 1
        else:
            queue.append(ary2[0]) # append index of the smallest
            flag1 = 2

        # delete the number ust added to the queue
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


def mergesort(reads_tuples): # list of tuple, each tuple formatted as (read_id, 'sequence')
    if len(reads_tuples) == 1:
        return reads_tuples

    else:  # split and apply double recursion
        n = floor(len(reads_tuples) / 2)
        return merge(mergesort(reads_tuples[:n]), mergesort(reads_tuples[n:]))