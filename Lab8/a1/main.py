import argparse
import numpy as np
import pandas as pd

from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
from imblearn.over_sampling import SMOTE

from early_integration import EarlyIntegrator
from late_integration import LateIntegrator

# GaussianNB and MLPClassifier can both be used for late integration

"""
Resources to handle dataset unbalancement
- https://towardsdatascience.com/handling-imbalanced-datasets-in-machine-learning-7a0e84220f28
- https://www.kaggle.com/rafjaa/resampling-strategies-for-imbalanced-datasets
- https://www.geeksforgeeks.org/ml-handling-imbalanced-data-with-smote-and-near-miss-algorithm-in-python/#:~:text=SMOTE%20(synthetic%20minority%20oversampling%20technique)%20is%20one%20of%20the%20most,instances%20between%20existing%20minority%20instances.
"""

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--clusters',
                        type =str,
                        default='../clusters.txt')
    parser.add_argument('--meth',
                        type=str,
                        default='../meth.txt')
    parser.add_argument('--mRNA',
                        type=str,
                        default='../mRNA.txt')
    parser.add_argument('--prot',
                        type=str,
                        default='../prot.txt')

    return parser.parse_args()

def main(args):

    # Very high since predictions are sure
    SM_THRESHOLD = 0.995
    SI_THRESHOLD = 0.995

    # Read dataset and labels
    clusters = pd.read_csv(args.clusters, delimiter = '\t', header = 0)
    meth_data = pd.read_csv(args.meth, delimiter = '\t', header = 0).transpose().iloc[:, 1:] # from bio to ML format
    mrna_data = pd.read_csv(args.mRNA, delimiter = '\t', header = 0).transpose().iloc[:, 1:]
    proteom_data = pd.read_csv(args.prot, delimiter = '\t', header = 0).transpose().iloc[:, 1:]
    omic_datasets = [meth_data, mrna_data, proteom_data]

    # Reformat datasets. Use subject as index
    clusters = clusters.iloc[:, [1, 2]]
    clusters.columns = ['subject', 'label']
    for dataset in omic_datasets: # modify inplace
        dataset.drop(dataset.index[0], inplace=True) # drop the name of the feature

    # Explore labels
    ground_truth = clusters.label.to_numpy()
    unique_labels, labels_frequency = np.unique(ground_truth, return_counts = True)
    fig, ax = plt.subplots()
    ax.bar(unique_labels, labels_frequency, 0.35)
    plt.show()

    # Handling dataset unbalancement with SMOTE oversampling
    sm = SMOTE(random_state=2)
    omic_datasets_res = []
    for dataset in omic_datasets:
        data_res, y_res = sm.fit_sample(dataset, clusters.label)
        omic_datasets_res.append(data_res)

    # Train test split for each omic dataset
    y = clusters.iloc[:, 1]
    omic_splits = []
    for dataset in omic_datasets_res:
        X = dataset.to_numpy()
        y = y_res.to_numpy()
        split = train_test_split(X, y, test_size=0.2, random_state=12, stratify=y)
        omic_splits.append(split)

    # Define 4 classifiers
    classifiers = [RandomForestClassifier(), SVC()]
    classifiers_name = ["Random Forest", "SVM"]
    prob_classifiers = [MLPClassifier(), GaussianNB()] # classifiers returning probability score: used for late integration
    prob_classifiers_name = ["Multi-layer Perceptron", "Naive Bayes Classifier"]

    early_integrator = EarlyIntegrator(omic_splits)
    for clf, name in zip(classifiers, classifiers_name):
        early_integrator.set_classifier(clf, name)
        early_integrator.train()
        _ = early_integrator.test()

    late_integrator = LateIntegrator(omic_splits, SM_THRESHOLD, SI_THRESHOLD)
    for clf, name in zip(prob_classifiers, prob_classifiers_name):
        late_integrator.set_classifier(clf, name)
        late_integrator.train_eval()


if __name__ == '__main__':
    args = get_args()
    main(args)
