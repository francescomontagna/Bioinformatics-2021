import sys
import time
import numpy as np


def pad_alignments(alignments):
    """

    :param alignments: lis tof lists. Internal is [read_id, sequence, reference_pos:str]
    alignments are already sorted by reference position.
    :return: padded alignments such that they all cover whole reference genome length.
    Padding is done with '_' character.
    """
    sequence_length = len(alignments[0][1])  # length of a single sequence
    last_reference =  int(alignments[-1][-1])  # length of reference genome

    sequences = []
    for i, el in enumerate(alignments):
        start = int(el[-1])
        if start != 0:
            left_padding = '_'*start
        else:
            left_padding = ''

        if start != last_reference:
            right_padding = '_'*(last_reference-start)
        else:
            right_padding = ''

        padded_seq = left_padding + el[1] + right_padding

        sequences.append(padded_seq)  # append padded_sequence and reference

    return sequences

def majority_voting(padded_alignments):
    """

    :param padded_alignments: list of padded sequences
    :return:
    """

    ref_genome_length = len(padded_alignments[0])

    reference_genome = ''
    variations = dict()
    for i in range(ref_genome_length):
        letters = dict()
        for alignment in padded_alignments:
            bp = alignment[i]
            if bp != '_':
                try:
                    letters[bp] = letters[bp] + 1
                except KeyError:
                    letters[bp]  = 1

        if len(letters) > 0:
            max_value = max(letters.values())
            max_bps = list(filter(lambda key: letters[key] == max_value, letters.keys()))
            reference_genome += max_bps[0]

        else:
            max_bps = []
            reference_genome += '_'

        if len(max_bps) > 1:
            current_variation = []
            for el in max_bps[1:]:
                current_variation.append(el)
            variations[i] = current_variation

    return reference_genome, variations


def main(args):
    start = time.time()
    input_path = 'alignments.txt'

    with open(input_path, 'r') as f:
        alignments = []
        _ = f.readline()  # Drop header
        for line in f:
            fields = line.split(' ')
            fields[-1] = fields[-1][:-1]  # Remove '\n'
            alignments.append(fields)

    alignments = np.array(alignments)

    # Sort by position in the reference. Ascending order
    indices = np.argsort(alignments[:, -1])
    sorted_alignments = alignments[indices]

    padded_alignments = pad_alignments(sorted_alignments)

    reference_genome, variations = majority_voting(padded_alignments)

    print(reference_genome)
    print(variations)
    print(time.time() - start)



if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)