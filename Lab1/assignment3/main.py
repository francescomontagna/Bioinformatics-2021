import os
import sys
from merge_sort import mergesort
from math import floor

def read_fasta(path):
    # TODO: try with harder fasta
    with open(path, 'r')as f:
        fasta = f.read().splitlines()
    keys = fasta[::2]
    values = fasta[1::2]

    return [(k, v) for k,v in zip(keys,values)]

def read_fq(path):
    # TODO: debug
    with open(path, 'r')as f:
        fasta = f.read().splitlines()
    keys = fasta[::4]
    values = fasta[1::4]

    return [(k, v) for k, v in zip(keys, values)]

def compare_fasta(fasta:list):
    """

    :param fasta: each fasta is a list of tuuples formatted as (read_id, sequence)
                  fasta[1] is sorted by sequence
    :return: list of tuple, each tuple contains read_id from the 2 files of matching sequences
    """
    matching_reads = []
    for read in fasta[0]:
        matching_tuple = compare(read, fasta[1])
        if matching_tuple is not None:
            matching_reads.append(matching_tuple)

    return matching_reads

def compare(read:tuple, fasta:list):
    """

    :param read: read to match in fasta
    :param fasta: list of tuples formatted as (read_id, sequence), from second fasta,
                  sorted by sequence value
    :return: tuple of matching reads when possible, else None
    """
    index = floor(len(fasta)/2)
    if read[1] == fasta[-1][1]:
        return (read[0], fasta[-1][0]) # tuple of reads
    elif read[1] > fasta[-1][1] and len(fasta) > 1:
        index = floor(len(fasta) / 2)
        return compare(read, fasta[index:])
    elif len(fasta) > 1:
        index = floor(len(fasta) / 2)
        return compare(read, fasta[:index])

    return None




def main(argv:list):
    file_dirs = argv # argv contains the 2 file directories in a list

    fasta = []
    fasta.append(read_fasta(file_dirs[0]))
    fasta.append(read_fasta(file_dirs[1]))
    fasta[1] = mergesort(fasta[1])

    matching_reads = compare_fasta(fasta)
    print(matching_reads)

if __name__ == '__main__':
    main(sys.argv[1:])