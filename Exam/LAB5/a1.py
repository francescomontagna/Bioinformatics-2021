import sys
import string
import random
import numpy as np

from scipy.stats import ttest_ind


def header_to_common(header, length = 8):
    random.seed(42)
    uppercase = string.ascii_uppercase
    numbers = list(map(lambda x: str(x), [i for i in range(10)]))
    common_header = ['label']
    for _ in range(len(header)):
        common_name = ''
        for i in range(length):
            if i < 2:
                common_name += random.choice(uppercase)
            else:
                common_name += random.choice(numbers)
        common_header.append(common_name)

    return common_header


if __name__ == '__main__':
    luminal_path = 'dataset.csv'
    reduced_path = 'reduced_dataset.csv'
    ALPHA = 0.05
    bonferroni = 1

    luminalA = []
    luminalB = []
    with open(luminal_path, 'r') as f:
        header = f.readline().split(',')[1:]
        bonferroni = len(header)
        for line in f:
            sample = list(map(lambda x: float(x), line.split(',')[1:]))  # each position in the sample correspond to a gene
            if line.startswith('Luminal A'):
                luminalA.append(sample)
            else:
                luminalB.append(sample)

    # Reformat dataset to put genes in the rows. lumnialA and luminalB will share same number of rows
    luminalA = np.transpose(luminalA)
    luminalB = np.transpose(luminalB)

    print(f'Luminal A shape {luminalA.shape}')
    print(f'Luminal B shape {luminalA.shape}')
    print(f'Header length {len(header)}')

    # Create a reduced Datasets
    reducedA = []
    reducedB = []
    reduced_header = []
    for i in range(len(luminalA)):
        _, p_val = ttest_ind(luminalA[i], luminalB[i])
        if p_val > ALPHA/bonferroni:
            reducedA.append(luminalA[i])
            reducedB.append(luminalB[i])
            reduced_header.append(header[i])

    reducedA = np.transpose(reducedA)
    reducedB = np.transpose(reducedB)
    with open(reduced_path, 'w+') as f:
        common_header = header_to_common(header)
        f.write(','.join(common_header) + '\n')
        for sample in reducedA:
            sample = list(map(lambda el: str(el), sample))
            line = 'Luminal A,' + ','.join(sample) + '\n'
            f.write(line)
        for sample in reducedB:
            sample = list(map(lambda el: str(el), sample))
            line = 'Luminal B,' + ','.join(sample) + '\n'
            f.write(line)
