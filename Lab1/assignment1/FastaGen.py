from Generator import Generator

class FastaGen(Generator):
    def __init__(self, file_name, num_reads, probabilities, seed, len_sequence):
        super().__init__(file_name, num_reads, probabilities, seed, len_sequence)

    def generate_read(self):
        read_id = f">read_{self.id}"
        sequence = super().generate_sequence()

        read = read_id + "\n" + sequence
        self.reads.append(read)

        self.id += 1