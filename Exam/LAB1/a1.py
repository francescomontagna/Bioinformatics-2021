import sys
import string
import numpy as np


class ReadsGenerator:
    def __init__(self, probs, num_reads):
        probs = list(map(lambda x: float(x), probs))
        norm_factor = sum(probs)
        self.probabilities = {'A': probs[0]/norm_factor,
                              'C': probs[1]/norm_factor,
                              'G': probs[2]/norm_factor,
                              'T': probs[3]/norm_factor}
        self.num_reads = int(num_reads)  # number of reads for a single file
        self.sequence_length = 50
        self.ascii_chars = [c for c in string.printable[:-10]]

    def __call__(self, output_file, fasta = True):
        with open(output_file, 'w+') as f:
            for i in range(self.num_reads):
                if fasta:
                    read_id = '>read_{}'.format(i)
                else:
                    read_id = '@read_{}'.format(i)
                f.write(read_id)
                f.write('\n')

                sequence_list = np.random.choice(list(self.probabilities.keys()),
                                                 size=(self.sequence_length, ),
                                                 p=list(self.probabilities.values()))
                sequence = ''.join(sequence_list)
                f.write(sequence + '\n')

                if not fasta:
                    f.write('+read_{}'.format(i) + '\n')
                    quality_score_list = np.random.choice(self.ascii_chars,
                                                     size = (self.sequence_length, ))
                    quality_score = ''.join(quality_score_list)
                    f.write(quality_score + '\n')


def main(args):
    probs = args[0:4]
    num_reads = args[4]
    filename = args[5]

    if filename[-1] == 'a':
        fasta = True
    else:
        fasta = False
    generator = ReadsGenerator(probs, num_reads)
    generator(filename, fasta)


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
