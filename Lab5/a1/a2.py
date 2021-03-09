import sys
from scipy import stats
import numpy as np

def main(args):
    file_name = args[0]
    luminal_a = []
    luminal_b = []
    with open(file_name, 'r') as f:
        names = f.readline()

        for line in f:
            fields = line.split(',')

            data = list(map(lambda x: float(x), fields[1:]))
            if fields[0].startswith('Luminal A'):
                luminal_a.append(data)
            else:
                luminal_b.append(data)

    luminal_a = np.transpose(luminal_a)
    luminal_b = np.transpose(luminal_b)

    print(luminal_a.shape)

    t_value, p_value = stats.ttest_ind(luminal_a,luminal_b, axis=1)

    print(p_value.shape)

    pass


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
