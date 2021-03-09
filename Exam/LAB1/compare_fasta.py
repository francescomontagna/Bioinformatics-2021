import sys
import numpy as np

def compare(fasta_files: list, output_path: str):
    read1, seq1 = list(fasta_files[0].keys()), list(fasta_files[0].values())
    read2, seq2 = list(fasta_files[1].keys()), list(fasta_files[1].values())

    with open(output_path, 'a+') as f:
        for read, seq in zip(read1, seq1):
            try:
                matching_index = seq2.index(seq)
                read_id = '<read_' + read + "," + 'read_' + read2[matching_index]  # read is is the concatenation of the 2 reads

                f.write(read_id)
                f.write('\n')
                f.write(seq)
                f.write('\n')

            except ValueError:
                pass


def main(args):
    input_paths = [el for el in args[0:2]]  # path of the 2 fasta files to compare
    output_path = args[2]

    fasta_files = []
    for path in input_paths:
        with open(path, 'r') as f:
            file_string = f.read()  # list of strings
            file_list = file_string.split('>read_')[1:]  # handle sequences on more than one line

            fasta_file = dict()
            for el in file_list:
                splitted_el = el.split('\n')
                read_id = splitted_el[0]
                sequence = ''.join(splitted_el[1:])
                fasta_file[read_id] = sequence

            fasta_files.append(fasta_file)

    # Write in a fasta file the matching sequences and corresponding ids
    compare(fasta_files, output_path)


if __name__ == '__main__':
    # args = sys.argv[1:]
    # main(args)

    test = np.array([['a', 1], ['b', 2]])
    print(test[:, 1])
