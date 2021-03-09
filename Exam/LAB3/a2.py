import sys


def process_gtf(input_path, output_path):
    chromosomes = []
    starts = []
    ends = []
    gene_names = []
    with open(input_path, 'r') as f, open(output_path, 'w+') as out:
        for line in f:
            if line.startswith('#'):
                continue
            else:
                fields = line.split('\t')
                chr = fields[0]
                feature = fields[2]

                # True for biotype = protein coding
                biotype = fields[8].split(';')[4].find('protein_coding') != -1

                if feature == 'gene' and biotype and chr in ['10', '18']:
                    chromosomes.append(chr)
                    starts.append(fields[3])
                    ends.append(fields[4])
                    name = fields[8].split(';')[2].split()[-1]
                    gene_names.append(name)

                    # write reduced GTF
                    out.write(line)

    return chromosomes, starts, ends, gene_names


if __name__ == '__main__':
    args = sys.argv[1:]
    sam_input = args[0]
    gtf_input = args[1]
    gtf_output = args[2]
    output_path = args[3]

    chromosomes, starts, ends, gene_names = process_gtf(gtf_input, gtf_output)

    counter = {k:0 for k in gene_names}
    with open(sam_input, 'r') as sam:
        for line in sam:
            fields = line.split("\t")
            pos = fields[3]

            for i in range(len(chromosomes)):
                if starts[i] <= pos <= ends[i]:
                    counter[gene_names[i]] += 1


    with open(output_path, 'w+') as f:
        for k, v in counter.items():
            f.write(k.strip("\"") + ':' + str(v) + '\n')