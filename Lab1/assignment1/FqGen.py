from Generator import Generator
import string
import random

class FqGen(Generator):
    def __init__(self, file_name, num_reads, probabilities, seed):
        super().__init__(file_name, num_reads, probabilities, seed)

    def generate_read(self):
        read_id = f"read_id{self.id}"
        sequence = super().generate_sequence()

        read = "@"+read_id + "\n" + sequence + "\n" + "+"+read_id + "\n" + self.bps_quality()
        self.reads.append(read)

        self.id += 1

    def bps_quality(self):
        characters = string.ascii_letters + string.digits + string.punctuation
        quality = ''.join(random.choice(characters) for i in range(self.LEN_SEQUENCE))
        return quality

