import sys
import numpy as np

from collections import Counter


def number_reads(input_path):

    with open(input_path, 'r') as f:
        global_counter = Counter(A=0, T=0, C=0, G=0)
        for line in f:
            if line.startswith('>'):
                continue

            local_counter = Counter(line[:-1])
            global_counter.update(local_counter)

    return dict(global_counter)


def complex_counter(input_path):
    complex_seqs = ['AAAAA', 'TTTTT', 'CCCCC', 'GGGGG']
    counter = 0

    with open(input_path, 'r') as f:

        for line in f:
            if line.startswith('>'):
                continue

            for el in complex_seqs:
                # suboptimal but fine, still same 'big O' complexity
                finder = max([line.find(seq) for seq in complex_seqs])
            if finder > -1:
                counter += 1

    return counter


def gc_counter(input_path, threshold):

    reads_counter = 0

    with open(input_path, 'r') as f:
        for line in f:
            if line.startswith('>'):
                continue

            gc_counter = line.count('GC')

            if gc_counter > threshold:
                reads_counter += 1

    return reads_counter


# Esame
def gc_regions(input_path, min_len = 5):
    regions_bounds = []

    with open(input_path, 'r') as f:
        for line in f:
            if line.startswith('>'):
                read_id = line.rstrip('\n')
                continue

            regions = []
            start = 0
            for i, base in enumerate(line):

                if base == 'C' or base == 'G':
                    continue
                else:
                    end = i-1

                    if end - start >= min_len:
                        regions.append((start, end))

                    start = i

            if len(regions) > 0:
                regions_bounds.append({read_id:regions})

    return regions_bounds



if __name__ == '__main__':
    args = sys.argv[1:]
    input_path = args[0]
    output_path = args[1]
    threshold = int(args[2])
    min_len = int(args[3])

    reads_counter = number_reads(input_path)
    counter = complex_counter(input_path)
    gc_counter = gc_counter(input_path, threshold)
    gc_groups = gc_regions(input_path, min_len)

    # with open(output_path, 'w+') as f:
    #     ...