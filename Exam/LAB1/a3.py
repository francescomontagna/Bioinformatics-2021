import sys
import numpy as np

def read_file(file_path):
    reads = []
    sequences = []
    with open(file_path, 'r') as f:
        reads.append(f.readline()[:-1])
        seq = ''

        for line in f:
            if line.startswith('>'):
                sequences.append(seq)
                reads.append(line[:-1])
                seq = ''

            else:
                seq += line[:-1]

    return sequences, reads


def main(args):
    file1 = args[0]
    file2 = args[1]
    output_path = args[2]

    fasta1 = list(read_file(file1))
    fasta2 = list(read_file(file2))


    with open(output_path, 'w+') as f:
        for i in range(len(fasta1[0])):
            seq1, read1 = fasta1[0][i
                          ], fasta1[1][i]
            for j in range(len(fasta2[0])):
                seq2, read2 = fasta2[0][j], fasta2[1][j]
                print(read2)
                if seq1 == seq2:
                    f.write(read1 + read2 + '\n')
                    f.write(seq1 + '\n')
                    break




if __name__ == '__main__':
    args = sys.argv[1:]
    # main(args)