from reads_statistics import FileStats
import os
import sys


def main(argv: list):
    input_path = argv[0]

    dirname = os.path.abspath(os.getcwd())
    file_dir = os.path.join(dirname, "..", "assignment1", input_path)
    with open(file_dir, 'r')as f:
        fasta = f.read().splitlines()

    statistics = FileStats(fasta, 'fa', 2)
    bp_counter_dict = statistics.count_bases()
    complex_seq_occurrences = statistics.complex_seq_counter() # 7
    gc_seq_reads_counter, gc_seq_reads_id = statistics.gc_statistics()
    print(gc_seq_reads_counter)
    print(gc_seq_reads_id)


if __name__ == '__main__':
    main(sys.argv[1:])
