import sys
from collections import Counter

def main(args):
    file_path = args[0]
    gc_threshold = int(args[1])

    type_file = file_path[-2:]  # "fa" or "fq"

    with open(file_path, 'r') as f:
        file_string = f.read()  # list of strings
        file_list = file_string.split('\n')
        if type_file == 'fa':
            keys = file_list[0::2]  # reads ids
            values = file_list[1::2]  # sequences

        else:
            keys = file_list[0::4]  # reads ids
            values = file_list[1::4]  # sequences

    reads_dict = {key: val for key, val in zip(keys, values)}

    # Number of base pairs occurrences over all reads
    bp_counter = Counter()
    for read in reads_dict.values():
        list_read = list(read)
        bp_counter.update(list_read)

    # Number of reads with low complexity sequence
    lc_counter = 0
    low_compl_sequences =  ["AAAA",
                            "TTTT",
                            "CCCC",
                            "GGGG"]

    for read in reads_dict.values():
        for seq in low_compl_sequences:
            if seq in read:
                lc_counter += 1
                break  # go to next read


    # Number of reads having GC occurrences higher than threshold
    gc_reads = dict()
    for read_id, sequence in reads_dict.items():
        read_gc_counter = 0
        for i in range(len(sequence)-2):  # length 2 sliding window
            if sequence[i: i+2] == 'GC':
                read_gc_counter += 1
        if read_gc_counter > gc_threshold:
            gc_reads[read_id] = read_gc_counter

    print(bp_counter)
    print(lc_counter)

if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)