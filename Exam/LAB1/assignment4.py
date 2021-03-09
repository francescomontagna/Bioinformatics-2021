import sys
import numpy as np

from collections import Counter


if __name__ == '__main__':
    args = sys.argv[1:]
    INPUT_PATH = 'test_alignments.txt'

    consensus_dictionary = {}
    max_end = 0

    with open(INPUT_PATH, 'r') as f:
        _ = f.readline()  # remove header

        for line in f:
            read_id, seq, start = line.split()
            start = int(start)
            end = start + len(seq)

            if end > max_end:
                max_end = end  # final sequence length

            for i in range(start, end):
                index = i - start
                if consensus_dictionary.get(i) is None:
                    consensus_dictionary[i] = [seq[index]]
                else:
                    consensus_dictionary[i].append(seq[index])


    consensus = ''
    variations = dict()
    for i in range(max_end):
        if consensus_dictionary.get(i) is None:
            consensus += '_'

        else:
            bases = consensus_dictionary[i]
            counter = Counter(bases)

            # sort counter by value
            sorted_counter = sorted(counter.items(), key=lambda x: x[1],
                                    reverse = True)
            max_occurrences = sorted_counter[0][1]
            consensus += sorted_counter[0][0]

            pos_variations = []
            j=1
            try:
                while sorted_counter[j][1] == max_occurrences:
                    pos_variations.append(sorted_counter[j][0])
                    j += 1
            except IndexError:
                pass

            if len(pos_variations) > 0:
                variations[i] = pos_variations

    print(consensus)
    print(variations)

