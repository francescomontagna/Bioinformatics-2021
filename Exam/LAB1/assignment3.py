import sys
import numpy as np

def compare(read_id, sequence, list_sequences):
    try:
        index = list_sequences.index(sequence)
        complementary_id = '>read_' + str(index)
        return read_id + '_' + complementary_id
    except ValueError:
        return None

if __name__ == '__main__':
    args = sys.argv[1:]
    file1 = args[0]
    file2 = args[1]

    matching_pairs = []

    with  open(file2, 'r') as f2:
        sequences = []
        for line in f2:
            if not line.startswith('>'):
                sequences.append(line.rstrip('\n'))

    with open(file1, 'r') as f1:
        for line in f1:
            if line.startswith('>'):
                read_id = line.rstrip('\n')

            else:
                match = compare(read_id, line.rstrip('\n'), sequences)
                if match is not None:
                    matching_pairs.append(match)
