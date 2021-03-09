import sys
import string
import random
import numpy as np

from collections import Counter

# Quality of the read for fq file
def bps_quality(sequence_length):
    characters = string.ascii_letters + string.digits + string.punctuation
    quality = ''.join(random.choice(characters) for i in range(sequence_length))
    return quality


def main(args):
    # file name
    output_path = args[0]
    number_samples = int(args[1])
    # Probabilities and base mapping
    probs = [float(p)/100 for p in args[2:]]  # A, T, C, G in order
    base_pairs = ['A', 'T', 'C', 'G']

    # Initialize read_id counter, sequence length value
    seq_length = 50
    current_id = 0

    type_file = output_path[-2:]  # "fa" or "fq"

    # Append mode. '+' sign to create file if does not exist
    with open(output_path, 'a+') as f:
        for _ in range(number_samples):
            read_id = ">read_" + str(current_id)
            current_id += 1
            sequence_list = np.random.choice(base_pairs, seq_length, probs)
            sequence = ''.join(sequence_list)
            f.write(read_id + '\n')
            f.write(sequence + '\n')

            if type_file == "fq":
                f.write(read_id + '\n')
                f.write(bps_quality(seq_length) + '\n')


def file_statistics(file_path):
    type_file = file_path[-2:]  # "fa" or "fq"

    reads = []

    if type_file == 'fa':
        with open(file_path, 'r') as f:
            for i, line in enumerate(f):
                if (i - 1) % 2 == 0:  # a read each 2 lines
                    reads.append(line)

    else:
        with open(file_path, 'r') as f:
            for i, line in enumerate(f):
                if (i - 1) % 4 == 0:  # a read each 4 lines
                    reads.append(line)

    bp_counter = Counter()

    for read in reads:
        list_read = list(read)
        bp_counter.update(list_read)

if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
