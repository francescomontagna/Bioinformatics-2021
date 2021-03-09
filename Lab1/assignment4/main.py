import sys
import pandas as pd
import numpy as np
from merge_sort import mergesort

# TODO handle multiple consensus regions
def majority_voting(sequences, pad_character = '_'):
    occurrences_counter = dict()
    for el in sequences:

        # Do not count for pad character
        if el != pad_character:
            try:
                occurrences_counter[el] += 1
            except KeyError:
                occurrences_counter[el] = 1

    if len(occurrences_counter) > 0:
        max_key = max(occurrences_counter, key=occurrences_counter.get) # should handle 2 keys associated with max
    else:
        max_key = '_'

    return max_key

def pad_alignments(alignments:list):
    sorted_alignments = mergesort(alignments) # sorted by  reference_position

    # Reference length = last reference_position + last read length
    len_reference = sorted_alignments[-1][-1] + len(sorted_alignments[-1][0])

    sequences = []
    for el in sorted_alignments: # el = [sequence, start_index]
        start = el[-1]
        end = el[-1]+len(el[0])

        # Pad all position left to start index
        if start != 0:
            sx_pad = '_'*start
        else:
            sx_pad = ''

        # pad all positions right to end index
        if end != len_reference:
            dx_pad = '_'*(len_reference-end)
        else:
            dx_pad = ''

        sequences.append(sx_pad + el[0] + dx_pad)

    return sequences, len_reference

def main(path):
    alignments = pd.read_csv(path, sep=' ', header=0).drop('read_id', axis=1)
    alignments = np.array(alignments)
    alignments = alignments.tolist() # [[id:int, sequence:str, start_index:int], ...]
    padded_sequences, len_reference = pad_alignments(alignments)
    consensus_region = ''
    for i in range(len_reference):
        sequences = [row[i] for row in padded_sequences]
        consensus_region += majority_voting(sequences)
    print("Consensus region:")
    print(consensus_region)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    path = sys.argv[1]
    main(path)
