import sys
import time
from collections import  Counter

def main(args):
    start = time.time()
    file_path = 'alignments.txt'

    alignments_dict = dict()
    alignment = ''
    max_len = 0  # max length of a sequence

    with open(file_path, 'r') as f:
        _ = f.readline()
        for line in f:
            fields = line.split()
            seq = fields[1]
            pos = int(fields[2])
            seq_len = len(seq)
            if pos+seq_len > max_len:
                max_len = pos + seq_len

            for i, letter in enumerate(seq):
                current_pos = pos+i
                if alignments_dict.get(current_pos) is None:
                    alignments_dict[current_pos] = letter
                else:
                    alignments_dict[current_pos] += letter

    # Iterate over the whole alignment length
    for i in range(max_len):
        candidates = alignments_dict.get(i)
        if candidates is None:
            alignment += '_'
        else:
            occurrences = Counter(candidates)
            max_key = max(occurrences, key = occurrences.get)  # sort by value
            alignment += max_key

    print(alignment)
    print(time.time() - start)


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)