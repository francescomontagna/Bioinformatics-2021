import sys

def valid_snp(filename):

    def check_validity(line):
        splitted_line = line.split('\t')

        if splitted_line[4] != '<*>':
            return True

        return False


    with open(filename, 'r') as f:

        # Drop first lines of the file
        while f.readline().startswith('##'):
            continue

        # VCF processing. We assume one read per line
        snp_file = list(filter(check_validity, f))

    return snp_file


def indel_detection(filename):

    def check_indel(line):
        splitted_line = line.split('\t')

        if splitted_line[7].startswith('INDEL'):
            return True

        return False


    with open(filename, 'r') as f:

        # Drop first lines of the file
        while f.readline().startswith('##'):
            continue

        # VCF processing. We assume one read per line
        indel_file = list(filter(check_indel, f))

    return indel_file


def main(args):
    filename = args[0]
    output1 = args[1]
    output2 = args[2]

    snp_file = valid_snp(filename)
    with open(output1, 'w+') as f:
        f.writelines(snp_file)

    indel_file = indel_detection(filename)
    with open(output2, 'w+') as f:
        f.writelines(indel_file)


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)