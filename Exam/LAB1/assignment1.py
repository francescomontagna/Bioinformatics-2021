import string
import sys
import numpy as np


def generate_file(output_path, num_reads, sequence_len, probs, fastq = False):

    bases = ['A', 'T', 'C', 'G']
    file_list = []
    ascii_chars = [c for c in string.printable[:-10]]

    with open(output_path, 'w+') as f:
        for i in range(num_reads):
            if fastq:
                read_id = '@read_' + str(i) + '\n'
            else:
                read_id = '>read_' + str(i) + '\n'
            f.write(read_id)
            np_sequence = np.random.choice(bases,
                                        size=(sequence_len, ),
                                        p=probs)

            sequence = ''.join(np_sequence)
            f.write(sequence + '\n')

            if fastq:
                score_id = '+read_' + str(i) + '\n'
                f.write(score_id)
                np_score = np.random.choice(ascii_chars,
                                         size=(sequence_len, ))
                score = ''.join(np_score)
                f.write(score + '\n')

                file_list.append(read_id + sequence + '\n' + score_id + score)

            else:
                file_list.append(read_id + sequence + '\n')


    return file_list



if __name__ == '__main__':
    args = sys.argv[1:]

    out_path = args[0]
    num_reads = int(args[1])
    SEQUENCE_LEN = 50
    probs = list(map(lambda x: float(x)/100, args[2:]))

    if out_path.endswith('fa'):
        fastq = False
    elif out_path.endswith('fq'):
        fastq = True
    else:
        assert 'Error'

    file_list = generate_file(out_path, num_reads, SEQUENCE_LEN, probs, fastq)

    with open('test_write.txt', 'w+') as f:
        for line in file_list:
            f.write(line)