import sys
import os
import pickle as pkl
import pandas as pd


class FusionManager():

    def __init__(self, reference, breakpoints):
        self.reference = reference
        self.breakpoints = breakpoints
        self.reverse_schema = {
            'A': 'T',
            'C': 'G',
            'G': 'C',
            'T': 'A',
            'N': 'N'
        }

    def reverse_sequence(self, sequence):
        reversed = sequence[::-1]
        complement = ''

        # map to complementary representation with reversed schema
        for base in reversed:
            complement += self.reverse_schema[base]

        return complement

    def gene_sequence(self, chr, breakpoint, strand, type):
        """
        :param type: '3p' or '5p'
        :return:
        """
        # promoter sequence
        if type == '5p':
            if strand == '+':
                sequence = self.reference[chr][0:breakpoint]
            elif strand == '-':
                sequence = self.reverse_sequence(self.reference[chr][breakpoint:])

        # end sequence
        elif type == '3p':
            if strand == '+':
                sequence = self.reference[chr][breakpoint:]
            elif strand == '-':
                sequence = self.reverse_sequence(self.reference[chr][0:breakpoint])

        return sequence

    def gene_fusion(self, breakpoint_data):
        """
        :param breakpoint_data: pd.Series with data of a single fusion
        :return:
        """
        chr5p = breakpoint_data.chr5p
        breakpoint5p = breakpoint_data.breakpoint5p
        strand5p = breakpoint_data.strand5p
        promoter_seq = self.gene_sequence(chr5p, breakpoint5p, strand5p, '5p')

        chr3p = breakpoint_data.chr3p
        breakpoint3p = breakpoint_data.breakpoint3p
        strand3p = breakpoint_data.strand3p
        end_seq = self.gene_sequence(chr3p, breakpoint3p, strand3p, '3p')

        fusion_name = breakpoint_data.Gene5p + "-" + breakpoint_data.Gene3p
        fusion_gene = promoter_seq + end_seq

        return (fusion_name, fusion_gene)

    def fusion_sequences(self):
        fusion_genes = dict()
        for _, bp in self.breakpoints.iterrows():
            name, sequence = (self.gene_fusion(bp))
            fusion_genes[name] = sequence

        with open('fusions.txt', 'w') as f:
            step = 50
            for k, v in fusion_genes.items():
                j = 0
                iterations = len(v)
                f.write('>' + k + '\n')
                while j < iterations:
                    f.write(v[j * step:(j + 1) * step] + '\n')
                    j += step


def read_inputs(breakpoints_path, reference_path):
    reference = dict()

    if not os.path.exists('processed_breakpoints.txt'):
        with open(breakpoints_path, 'r') as r, open('processed_breakpoints.txt', 'w') as w:
            for line in r:
                w.write('\t'.join(line.split()) + '\n')

    breakpoints = pd.read_csv('processed_breakpoints.txt', header=0, sep='\t')

    with open(reference_path, 'r') as f:
        j = 0
        chromosome = ''
        chromosome_id = int(f.readline()[1:3])
        for line in f:
            # drop new line
            line = line[:-1]
            if line.startswith('>'):
                j += 1
                reference[chromosome_id] = chromosome
                chromosome_id = int(line[1:3])
                chromosome = ''
            else:
                chromosome += line  # remove new line
        reference[chromosome_id] = chromosome

        # save ref as pkl
        with open('reference.pkl', 'wb') as f:
            pkl.dump(reference, f, protocol=pkl.HIGHEST_PROTOCOL)

        # save breakpoints as pkl
        with open('breakpoints.pkl', 'wb') as f:
            pkl.dump(breakpoints, f, protocol=pkl.HIGHEST_PROTOCOL)


def main(args):
    # read input files
    breakpoints_path = args[0]
    reference_path = args[1]

    if not os.path.exists('reference.pkl'):
        read_inputs(breakpoints_path, reference_path)

    # load reference
    with open('reference.pkl', 'rb') as f:
        reference = pkl.load(f)

    # load breakpoints
    with open('breakpoints.pkl', 'rb') as f:
        breakpoints = pkl.load(f)

    fm = FusionManager(reference, breakpoints)
    fm.fusion_sequences()


if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)
