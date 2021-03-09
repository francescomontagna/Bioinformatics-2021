import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE

def read_dataset(path, labels):
    dataset = []
    with open(path, 'r') as f:
        _ = f.readline()
        for line in f:
            sample = [float(x) for x in line.split('\t')[1:]]
            dataset.append(sample)

    # Important to have same random state for each omic
    X_train, X_test, y_train, y_test = \
        train_test_split(np.array(dataset), labels, test_size=0.2,
                         stratify=labels, random_state = 42)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    X = (X_train, X_test)
    y = (y_train, y_test)

    return X, y


def classify(classifier, X_train, y_train, X_test, y_test, clf_name):
    pass


if __name__ == '__main__':
    labels_path = 'clusters.txt'
    mRNA_path = 'mRNA.txt'
    prot_path = 'prot.txt'
    meth_path = 'meth.txt'

    labels = []
    with open(labels_path, 'r') as f:
        _ = f.readline()
        for line in f:
            labels.append(int(line.split('\t')[-1]))
    labels = np.array(labels)

    # Labels are always the same
    mrna_data, _ = read_dataset(mRNA_path, labels)
    prot_data, _ = read_dataset(prot_path, labels)
    meth_data, train_test_labels = read_dataset(meth_path)

    # Early intergation
    X_train = np.transpose(np.concatenate([mrna_data[0], prot_data[0], meth_data[0]], axis = 0))
    X_test = np.transpose(np.concatenate([mrna_data[1], prot_data[1], meth_data[1]], axis = 0))
    y_train = train_test_labels[0]
    y_test = train_test_labels[1]

    # Over sampling on train data
    smote = SMOTE()
    X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

    # Dimensionality reduction
    pca = PCA(n_components=0.8, svd_solver='full')
    X_train_res_pca = pca.fit_transform(X_train_res)
    X_test_pca = pca.transform(X_test)

