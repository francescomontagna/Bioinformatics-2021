import numpy as np

from imblearn.over_sampling import SMOTE
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


class EarlyIntegration:
    """
    - Rescale the data separately
    - Up-sampling
    - Features selection / Dim reduction-
    """

    def __init__(self, meth_path, mrna_path, prot_path, labels_path):
        meth_data = self.read_data(meth_path)
        mrna_data = self.read_data(mrna_path)
        prot_data = self.read_data(prot_path)

        X = np.concatenate([mrna_data,
                            meth_data,
                            prot_data], axis=1)
        y = self.read_labels(labels_path)

        # Oversample and apply PCA
        X, y = self.preprocessing(X, y)

        self.X_train, self.X_test, \
        self.y_train, self.y_test = train_test_split(X, y, shuffle=True, random_state=42)

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
        features_mean = np.mean(dataset, axis=0)
        features_std = np.std(dataset, axis=0)

        scaled_dataset = (dataset - features_mean) / features_std

        return scaled_dataset

    def preprocessing(self, X, y):
        smote = SMOTE(random_state=42)
        X_res, y_res = smote.fit_resample(X, y)

        pca = PCA(n_components=0.8, svd_solver='full')  # Explain at least 80% of the variance
        X = pca.fit_transform(X_res)

        print(f"Number components retained: {pca.n_components_}")
        print(f"Explained variance: {sum(pca.explained_variance_ratio_)}")
        print()

        return X, y_res

    def train_eval(self, classifier):

        classifier.fit(self.X_train, self.y_train)
        preds = classifier.predict(self.X_test)

        accuracy = accuracy_score(self.y_test, preds)

        # We might be interested in accuracy by label
        return accuracy
