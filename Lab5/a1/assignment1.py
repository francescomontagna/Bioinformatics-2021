import pandas as pd
import numpy as np
import sys
import re

from scipy.stats import ttest_ind


class DatasetReducer():
    """
    Class to test equality of the mean of 2 populations
    Store a copy of the resulting reduce dataset
    """

    def __init__(self,
                 dataset: pd.DataFrame,
                 alpha: float,
                 reduced_path: str,
                 dataset_path: str,
                 gtf_file='Homo_sapiens.GRCh38.95.gtf'):
        self.dataset = self.preprocess_dataset(dataset)
        self.luminalA, self.luminalB = self.split_dataset()

        bonferroni_factor = len(self.dataset.columns) - 1
        self.alpha_adjusted = alpha / bonferroni_factor

        self.reduced_path = reduced_path
        self.dataset_path = dataset_path
        self.gtf_file = gtf_file

    def preprocess_dataset(self, dataset):
        dataset.iloc[:, 0] = dataset.iloc[:, 0].str.strip()
        dataset = dataset.replace(0, np.nan)

        pattern = re.compile("[^.]*")
        format_id = lambda x: "".join(pattern.findall(x))
        correct_header = dict()
        for col in dataset.columns:
            correct_header[col] = format_id(col)

        correct_header['l'] = 'l'
        dataset = dataset.rename(correct_header, axis=1)

        return dataset

    def split_dataset(self):
        mask_A = self.dataset.iloc[:, 0] == 'Luminal A'
        mask_B = self.dataset.iloc[:, 0] == 'Luminal B'
        luminalA = self.dataset[mask_A]
        luminalB = self.dataset[mask_B]

        return luminalA.iloc[:, 1:], luminalB.iloc[:, 1:]  # could drop the label column

    def t_test(self, colA, colB):
        """
        T test for a single gene
        :param colA: single gene sample population with label Luminal A
        :param colB: single gene sample population with label Luminal A
        :return: True if the null H0 is accepted, else False
        """
        t_value, p_value = ttest_ind(colA, colB, equal_var=False, nan_policy='omit')

        # compare p_value with alpha
        if p_value < self.alpha_adjusted:
            return True  # Accept the null
        else:
            return False  # reject the null

    def build_genes_map(self):

        ensemble_to_common = dict()

        dtypes = {k: 'object' for k in range(9)}
        dtypes[3] = 'int64'
        dtypes[4] = 'int64'

        hs_gtf = pd.read_csv(self.gtf_file, sep='\t', skiprows=5, header=None, dtype=dtypes)

        pattern = re.compile("gene_id [^;]*")
        select_id = lambda x: "".join(pattern.findall(x)).split()[1][1:-1]
        gene_id = hs_gtf.iloc[:, 8].apply(select_id).to_numpy()

        pattern = re.compile("gene_name [^;]*")
        select_name = lambda x: "".join(pattern.findall(x)).split()[1][1:-1]
        gene_name = hs_gtf.iloc[:, 8].apply(select_name).to_numpy()

        for id,name in zip(gene_id, gene_name):
            ensemble_to_common[id] = name

        ensemble_to_common['l'] = 'l' # retain the label

        return ensemble_to_common

    def reduce_dataset(self):
        header = self.luminalA.columns
        differential_genes = ['l']  # select also label clumn
        i = 0
        for gene in header:
            colA = self.luminalA[gene]
            colB = self.luminalB[gene]
            test = self.t_test(colA, colB)
            if test:
                i += 1
                differential_genes.append(gene)

        print(f"Number of selected features: {i}")
        self.reduced_dataset = self.dataset[differential_genes]

        ensemble_to_common = self.build_genes_map()
        print(ensemble_to_common)

        dataset_header = []
        for col in self.dataset.columns:
            new_col = ensemble_to_common[col]
            dataset_header.append(new_col)
        self.dataset.columns = dataset_header

        reduced_dataset_header = []
        for col in self.reduced_dataset.columns:
            new_col = ensemble_to_common[col]
            reduced_dataset_header.append(new_col)
        self.reduced_dataset.columns = reduced_dataset_header

        # print(self.reduced_dataset.head())
        # print(self.dataset.head())

        self.reduced_dataset.to_csv(self.reduced_path, header=True, index=False)
        self.dataset.to_csv(self.dataset_path, header=True, na_rep=np.nan, index=False)


if __name__ == '__main__':
    dataset = pd.read_csv(sys.argv[1], header=0)
    dr = DatasetReducer(dataset, 0.05, sys.argv[2], sys.argv[3])
    dr.reduce_dataset()
