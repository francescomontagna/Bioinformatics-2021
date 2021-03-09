import re

class FileStats():
    def __init__(self, file:list, type:str, threshold:int):
        """
        :param file: list of strings. For each read we have 2 consecutive items: [">read Id", "sequence"]
        :param threshold: threshold for GC couples. For CG couple higher than threshold, report read_id
                          and number of GC couples
        :param type: if the file is fq or fa type
        """

        self.type = type
        self.reads = self.format_reads(file) # dictionary {read_id\n: sequence\n}
        self.GC_THRESHOLD = threshold

    def format_reads(self, file):
        if self.type == 'fa':
            keys = file[0::2]
            values = file[1::2]
            return {k:v for k,v in zip(keys, values)}

    def count_bases(self):
        counter_dict = dict.fromkeys(self.reads.keys())
        basis = ["A", "T", "C", "G"]
        for id, seq in self.reads.items():
            letter_counter = {k:0 for k in basis}
            for bp in basis:
                letter_counter[bp] = len(re.findall(bp, seq)) # for each base pair, store the number of occurrences
            counter_dict[id] = letter_counter

        return counter_dict

    def complex_seq_counter(self):
        counter = 0
        complex_pattern = "AAAAAA|TTTTTT|CCCCCC|GGGGGG"

        for seq in self.reads.values():
            if re.search(complex_pattern, seq):
                counter += 1

        return counter

    # count num reads with "GC" occurrences above threshold
    # return selected reads id
    def gc_statistics(self):
        above_threshold_reads = dict()
        regex = re.compile("GC")
        for read,seq in self.reads.items():
            gc_occurrences = len(regex.findall(seq))
            if gc_occurrences > self.GC_THRESHOLD:
                above_threshold_reads[read] = gc_occurrences

        return len(above_threshold_reads), above_threshold_reads
