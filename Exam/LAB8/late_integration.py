import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier


class LateIntegration:
    """
    - Rescale the data separately
    - Upsampling
    - Features selection / Dim reduction-
    """

    def __init__(self, meth_path, mrna_path, prot_path, labels_path):
        meth_data = self.read_data(meth_path)
        mrna_data = self.read_data(mrna_path)
        prot_data = self.read_data(prot_path)

        self.omic_datasets = {'meth': meth_data,
                              'mrna': mrna_data,
                              'prot': prot_data}
        self.y = self.read_labels(labels_path)


    def read_labels(self, path):
        labels = []
        with open(path, 'r') as f:
            _ = f.readline()
            for line in f:
                labels.append(int(line.split()[-1]))

        return labels


    def read_data(self, path):
        """
        Read the dataset from file and perform a scaling
        """
        dataset = []
        with open(path, 'r') as f:
            _ = f.readline()  # drop header

            for line in f:
                cast = lambda x: float(x)
                fields = map(cast, line.split()[1:])
                dataset.append(list(fields))

        dataset = np.transpose(dataset)
        # features_mean = np.mean(dataset, axis=0)
        # features_std = np.std(dataset, axis=0)
        #
        # scaled_dataset = (dataset - features_mean) / features_std

        return dataset


    def train_eval(self, classifier_name):

        if classifier_name == 'MLP':
            classifiers = {k:MLPClassifier() for k in self.omic_datasets.keys()}
        elif classifier_name == 'NB':
            classifiers = {k:GaussianNB() for k in self.omic_datasets.keys()}
        else:
            raise Exception('Classifier not available. ' +
                            'Please select one between \'MLP\' ' +
                            'and \'NB\'')

        # Train a classifier for each dataset
        probability_matrix = []
        for key in self.omic_datasets.keys():
            X_train, X_test, y_train, y_test =\
                train_test_split(self.omic_datasets[key], random_state=42, test_size=0.2)
            classifiers[key].fit(X_train, y_train)

            probs = classifiers[key].predict_proba(X_test)

        probability_matrix = np.array(probability_matrix)
            S_i = probs.sum(axis=1)
            S_a = np.sum(S_i)
            S_m = S_i / len(self.omic_datasets)
