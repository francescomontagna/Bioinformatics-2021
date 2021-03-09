import sys


def reverse_complement(sequence):
    encoding = {'A': 'T',
                'T': 'A',
                'C': 'G',
                'G': 'C',
                'N': 'N'}
    rev_sequence = sequence[::-1]

    comp_sequence = ''
    for letter in rev_sequence:
        comp_sequence += encoding[letter]

    return comp_sequence


def build_fusion(fields, gtf, reference):
    chr5p, bp5p = list(map(lambda x: int(x), fields[1:3]))
    strand5p = fields[3]
    chr3p, bp3p = list(map(lambda x: int(x), fields[5:-1]))
    strand3p = fields[-1]

    if strand5p == '+':
        for start, end in gtf:
            if start <= bp5p <= end:
                start5p = start
                end5p = bp5p
                break
        prom_seq = reference[chr5p][start5p:end5p]

    elif strand5p == '-':
        for start, end in gtf:
            if start <= bp5p <= end:
                start5p = bp5p
                end5p = end
                break
        prom_seq = reverse_complement(reference[chr5p][start5p:end5p])

    if strand3p == '+':
        for start, end in gtf:
            if start <= bp3p <= end:
                start3p = bp3p
                end3p = end
                break
        end_seq = reference[chr3p][start3p:end3p]

    elif strand3p == '-':
        for start, end in gtf:
            if start <= bp3p <= end:
                start3p = start
                end3p = bp3p
                break
        end_seq = reverse_complement(reference[chr3p][start3p:end3p])

    return prom_seq + end_seq


if __name__ == '__main__':
    args = sys.argv[1:]
    reference_path = 'reference_chr10_chr18.fa'
    breakpoint_path = 'breakpoints.txt'
    gtf_path = 'Homo_sapiens.GRCh38.95.gtf'

    # Read reference file. Read separately the 2 chromosomes
    with open(reference_path, 'r') as f:
        print("Reading reference sequences... ")
        references = dict()
        sequence = ''
        chromosome = int(f.readline()[1:3])
        for line in f:
            if line.startswith('>'):
                references[chromosome] = sequence
                sequence = ''
                chromosome = int(line[1:3])
            else:
                sequence += line.rstrip('\n')
        references[chromosome] = sequence

    gtf = []
    with open(gtf_path, 'r') as f:
        print("Reading gtf file... ")
        for line in f:
            if line.startswith('#'):
                continue
            fields = line.split('\t')
            start = int(fields[3])
            end = int(fields[4])
            gtf.append((start, end))

    # Breakpoint file
    with open(breakpoint_path, 'r') as f,\
        open('fusions.fa', 'w+') as out:
        print('Building gene fusions...')
        _ = f.readline()
        for line in f:
            fields = line.split()
            fusion = build_fusion(fields, gtf, references)
            id = '>' + fields[0] + '>' + fields[4]
            out.write(id + '\n')
            out.write(fusion + '\n')
    print('Done')
