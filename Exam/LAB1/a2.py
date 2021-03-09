import sys
import numpy as np

from collections import Counter


class StatsCounter:
    def __init__(self, reads_id, sequences, output_path, threshold):
        self.reads_id = reads_id
        self.sequences = sequences
        self.output_path = output_path
        self.threshold = threshold

    def count_basis(self):
        assembled_sequence = [letter for letter in ''.join(self.sequences)]
        stats = Counter(assembled_sequence)

        with open(self.output_path, 'a+') as f:
            f.write('Single basis number of occurrences\n')
            f.write(str(dict(stats)) + '\n')

    def low_complex_count(self):
        low_complexity_seqs = ['AAA', 'TTT', 'CCC', 'GGG']
        counter = 0
        for seq in self.sequences:
            for val in low_complexity_seqs:
                if seq.find(val) > -1:
                    counter += 1
                    break

        with open(self.output_path, 'a+') as f:
            f.write('Number of sequences with at least one low complexity sub sequence: {}\n'.format(counter))

    def gc_counter(self):
        counter = dict()

        for seq, read in zip(self.sequences, self.reads_id):
            num_occurrences = 0
            for i in range(0, len(seq)-2):
                if seq[i:i+2] == 'GC':
                    num_occurrences += 1

            if num_occurrences > self.threshold:
                counter[read] = num_occurrences

        with open(self.output_path, 'a+') as f:
            f.write('Number of \'GC\' pairs for read:\n')
            f.write(str(counter))






def main(args):
    input_path = args[0]
    output_path = args[1]
    threshold = int(args[2])

    # Process to get only the sequences of interest
    sequences = []
    reads = []
    with open(input_path, 'r') as f:
        reads.append(f.readline())
        seq = ''
        for line in f:
            # Detect new read - the last sequence is concluded
            if line.startswith('>'):
                reads.append(line[1:-1])
                sequences.append(seq)
                seq = ''
            else:
                seq += line[:-1]  # to handle sequences on more than one line

    stats_counter = StatsCounter(reads, sequences, output_path, threshold)

    stats_counter.count_basis()
    stats_counter.low_complex_count()
    stats_counter.gc_counter()



if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)