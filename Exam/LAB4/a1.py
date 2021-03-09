import sys


def parse_gtf(line):
    line_split = line.split()

    gene_limits = [int(line_split[3]),  # start
                   int(line_split[4])  # end
                   ]

    return gene_limits


def reverse_complement(sequence):
    """
    Reverse order and complement the sequence
    :return: reversed and complemented line
    """
    complement_encoding = {'A': 'T',
                           'G': 'C',
                           'T': 'A',
                           'C': 'G',
                           'N': 'N'}

    reversed = sequence[::-1]

    complemented = ''
    for letter in reversed:
        complemented += complement_encoding[letter]

    return complemented


def gene_fusion(parsed_line, chr10, chr18, gene_positions):
    gene5p, chr5p, bp5p, strand5p, \
    gene3p, chr3p, bp3p, strand3p = parsed_line

    # cast bp to int
    bp3p = int(bp3p)
    bp5p = int(bp5p)

    fusion = ''

    # Find start and end positions of the genes involved
    for start, end in gene_positions:
        if start <= bp5p <= end:
            start5p = start
            end5p = end

        if start <= bp3p <= end:
            start3p = start
            end3p = end

    # Handle 4 possible cases
    if strand5p == '+':
        if chr5p == '10':
            fusion += chr10[start5p: bp5p]
        else:
            fusion += chr18[start5p: bp5p]

    else:
        if chr5p == '10':
            fusion += reverse_complement(chr10[bp5p:end5p])
        else:
            fusion += reverse_complement(chr18[bp5p:end5p])

    if strand3p == '+':
        if chr3p == '10':
            fusion += chr10[bp3p:end3p]
        else:
            fusion += chr18[bp3p:end3p]

    else:
        if chr3p == '10':
            fusion += reverse_complement(chr10[start3p:bp3p])
        else:
            fusion += reverse_complement(chr18[start3p:bp3p])

    return fusion


def main(args):
    bp_filename = args[0]
    fa_filename = args[1]
    out_filename = args[2]
    gtf_filename = args[3]

    # Read gtf file
    with open(gtf_filename, 'r') as f:
        gtf_file = f.readlines()

    gene_positions = []
    for line in gtf_file:
        if not line.startswith('#'):
            gene_positions.append(parse_gtf(line))

    # Read fa file
    with open(fa_filename, 'r') as f:
        # Drop first line
        _ = f.readline()
        gtf_file = f.readlines()

    chr10 = ''
    chr18 = ''
    i = 0
    while not gtf_file[i].startswith('>'):
        chr10 += gtf_file[i][:-1]
        i += 1

    for line in gtf_file[i + 1:]:
        chr18 += line[:-1]

    with open(bp_filename, 'r') as f:
        # Drop header
        _ = f.readline()
        breakpoints = f.readlines()

    detected_fusions = []
    for line in breakpoints:
        parsed_line = line.split()
        fusion_id = '>' + parsed_line[0] + '>' + parsed_line[4] + '\n'
        fusion = fusion_id + gene_fusion(parsed_line, chr10, chr18, gene_positions) + '\n'
        detected_fusions.append(fusion)

    with open(out_filename, 'w+') as f:
        f.writelines(detected_fusions)


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
