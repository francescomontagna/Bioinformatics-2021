import sys

def vcf_complete(input_path, output_path):

    reduced = []
    with open(input_path, 'r') as input,\
        open(output_path, 'w+') as output:

        for line in input:
            if line.startswith('#'):
                continue
            fields = line.split('\t')
            aligned = fields[4]
            if aligned != '<*>':

                # Write and append only if alignment is associate to complete information
                output.write(line)
                reduced.append(line)

    return reduced


def vcf_indel(reduced_vcf, output_path):

    indel_vcf = []
    with open(output_path, 'w+') as f:
        for line in reduced_vcf:
            fields = line.split('\t')
            if fields[7].startswith('INDEL'):
                indel_vcf.append(line)
                f.write(line)


if __name__ == '__main__':
    args = sys.argv[1:]
    input_path = args[0]
    reduced_output = args[1]
    indel_output = args[2]

    reduced_vcf = vcf_complete(input_path, reduced_output)
    indel_vcf = vcf_indel(reduced_vcf, indel_output)
