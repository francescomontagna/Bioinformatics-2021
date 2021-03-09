import numpy as np
from sklearn.metrics import accuracy_score

class EarlyIntegrator:
    def __init__(self, omic_splits: list):
        """
        :param omic_split: a list of omic numpy datasets, each one of shape (number samples, number omic features)
        """
        self.y_train, self.y_test = omic_splits[0][2], omic_splits[0][3]
        self.X_train, self.X_test = self.integrate(omic_splits)

    def set_classifier(self, classifier, name):
        self.name = name
        self.classifier = classifier

    def integrate(self, omic_splits):
        X_train_list = []
        X_test_list = []

        for split in omic_splits:
            X_train, X_test, _, _ = split
            X_train_list.append(X_train)
            X_test_list.append(X_test)

        X_train = np.concatenate(X_train_list, axis=1)
        X_test = np.concatenate(X_test_list, axis=1)

        return X_train, X_test

    def train(self):
        """
        :return: train accuracy score
        """
        self.classifier.fit(self.X_train, self.y_train)
        train_preds = self.classifier.predict(self.X_train)
        accuracy = np.sum(train_preds == self.y_train)/train_preds.shape[0]
        print(self.name + " train accuracy: {}".format(accuracy))

    def test(self):
        test_preds = self.classifier.predict(self.X_test)
        accuracy = accuracy_score(self.y_test, test_preds)
        print(self.name + " test accuracy: {}".format(accuracy))

        return test_preds