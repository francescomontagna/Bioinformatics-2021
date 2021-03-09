import numpy as np

class Generator():
    def __init__(self, file_name, num_reads, probabilities, seed, len_sequence):
        self.id = 0
        self.LEN_SEQUENCE = len_sequence
        self.file_name = file_name
        self.num_reads = num_reads
        self.probabilities = probabilities  # [A,T,C,G]
        self.bases = ["A", "T", "C", "G"]
        self.reads = list()

        np.random.seed(seed = seed)

    def generate_sequence(self):
        sequence = ""
        for _ in range(self.LEN_SEQUENCE):
            bp = np.random.choice(4, 1, p=self.probabilities)[0]
            sequence += self.bases[bp]
        return sequence

    def generate_read(self):
        pass

    def generate_reads(self):
        for _ in range(self.num_reads):
            self.generate_read()
        self.write_reads()

    def write_reads(self):
        # Open the file in append & read mode ('a+')
        with open(self.file_name, 'a+') as f:
            appendEOL = False
            # Move read cursor to the start of file.
            f.seek(0)
            # Check if file is not empty
            data = f.read(100)
            if len(data) > 0:
                appendEOL = True
            # Iterate over each string in the list
            for read in self.reads:
                # If file is not empty then append '\n' before first line for
                # other lines always append '\n' before appending line
                if appendEOL:
                    f.write("\n")
                else:
                    appendEOL = True
                # Append element at the end of file
                f.write(read)
