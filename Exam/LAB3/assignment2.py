import sys
import os

from collections import Counter


def gtf_line_parser(line):
    # BASTA FARE LINE.SPLIT
    line_split = line.split('\t')
    last_element = line_split[-1]
    line_split = line_split[0:-1]
    line_split.extend(last_element.split(' '))

    parsed_line = [int(line_split[3]),  # start
                   int(line_split[4]),  # end
                   line_split[13][1:-2],  # human readable name
                   ]

    return parsed_line


def sam_line_parser(line):
    line_split = line.split()  # split whitespace (tab, space, new_line, ...)
    alignment_start = int(line_split[3])
    alignment_end = alignment_start + len(line_split[9])
    parsed_line = [alignment_start,
                   alignment_end
                   ]

    return parsed_line


def reduce_gtf(filename, output_path):
    def check_validity(line):

        if line.startswith('#'):
            return False

        line_split = line.split('\t')
        last_element = line_split[-1]
        line_split = line_split[0:-1]
        line_split.extend(last_element.split(' '))

        if line_split[0] in ['10', '18'] and \
                line_split[2] == 'gene' and \
                line_split[17][1:-3] == 'protein_coding':
            return True

        return False

    with open(filename, 'r') as gtf_file, open(output_path, 'w+') as out_file:

        reduced_gtf = list(filter(check_validity, gtf_file))
        out_file.writelines(reduced_gtf)


def main(args):
    gtf_filename = args[0]
    sam_filename = args[1]
    reduced_gtf_path = args[2]

    if not os.path.isfile(reduced_gtf_path):
        reduce_gtf(gtf_filename, reduced_gtf_path)

    # Filter out unmapped reads (bit 2) and supplementary alignments (bit 11) from input.sam
    # This is done from command line, to produce unique_aligned.sam

    with open(sam_filename, 'r') as sam_file:
        # reduced_sam has info about uniquely aligned reads
        reduced_sam = list(map(sam_line_parser, sam_file))

    with open(reduced_gtf_path, 'r') as gtf_file:
        # reduced_gtf have info about genes, with protein coding function
        reduced_gtf = list(map(gtf_line_parser, gtf_file))

    selected_genes = []
    for start, end in reduced_sam:
        for gene in reduced_gtf:
            if start >= gene[0] and end <= gene[1]:
                selected_genes.append(gene[2])
                break

    gene_counter = Counter(selected_genes)
    print(gene_counter)

    # Solution providing zero count
    alternative_sol = dict()
    for start, end in reduced_sam:
        for gene_start, gene_end, name in reduced_gtf:

            # Check if key already present
            if alternative_sol.get(name) is None:
                alternative_sol[name] = 0
            if start >= gene_start and end <= gene_end:
                selected_genes.append(name)
                break

    # print(alternative_sol)


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
