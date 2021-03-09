from FastaGen import FastaGen
from FqGen import FqGen
import sys

def main(argv):
    file_name = argv[0]
    seed = int(argv[1])
    num_reads = int(argv[2])
    len_sequence = int(argv[3])
    probabilities = [int(p) / 100 for p in argv[4:]]
    generator = None

    if file_name.endswith("fa"):
        generator = FastaGen(file_name, num_reads, probabilities, seed, len_sequence)

    elif file_name.endswith("fq"):
        generator = FqGen(file_name, num_reads, probabilities, seed, len_sequence)

    generator.generate_reads()


if __name__ == "__main__":
    main(sys.argv[1:])