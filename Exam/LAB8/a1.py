import sys
import numpy as np


from early_integration import EarlyIntegration
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier


def early_integration(args):
    meth_path = args[0]
    rna_path = args[1]
    prot_path = args[2]
    labels_path = args[3]

    early_int = EarlyIntegration(meth_path,
                                 rna_path,
                                 prot_path,
                                 labels_path)

    classifiers = [SVC(), MLPClassifier(),\
                   RandomForestClassifier(), GaussianNB()]
    names = ['SVM', 'MultiLayer Perceptron',\
             'Random Forest', 'Naive Bayes']

    print('#'*len('EARLY INTEGRATION'))
    print('EARLY INTEGRATION')
    print('#'*len('EARLY INTEGRATION'))
    print()
    for clf, name in zip(classifiers, names):
        eval_accuracy = early_int.train_eval(clf)
        print(name + ' evaluation accuracy score: {}'.format(eval_accuracy))


def late_integration(args):
    meth_path = args[0]
    rna_path = args[1]
    prot_path = args[2]
    labels_path = args[3]


if __name__ == '__main__':
    args = sys.argv[1:]
    if args[0] == 'ei':
        early_integration(args[1:])

    else:
        late_integration(args[1:])