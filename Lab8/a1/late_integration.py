import numpy as np

class LateIntegrator:
    def __init__(self, omic_splits, sm_threshold, si_threshold):
        """
        :param omic_split: a list of omic numpy datasets, each one of shape (number samples, number omic features)
        """
        self.sm_threshold = sm_threshold
        self.si_threshold = si_threshold
        self.y_train, self.y_test = omic_splits[0][2], omic_splits[0][3]
        self.X_train_list, self.X_test_list = self.integrate_dataset(omic_splits)
        self.num_omic_datasets = len(omic_splits)


    def set_classifier(self, classifier, name):
        self.name = name
        self.classifiers = [classifier for _ in range(self.num_omic_datasets)]


    def integrate_dataset(self, omic_splits):
        X_train_list = []
        X_test_list = []

        for split in omic_splits:
            X_train, X_test, _, _ = split
            X_train_list.append(X_train)
            X_test_list.append(X_test)

        return X_train_list, X_test_list


    def integrate_predictions(self, probabilities):
        """
        :param probabilities: list of probabilities on all omic datasets. Global shape is [# omic, # samples, # classes]
        :return:
        """
        probabilities = np.transpose(probabilities, (1, 0, 2)) # each element is the matrix over which perform our computations
        preds = []
        for mat in probabilities:
            S_i = np.sum(mat, axis=0) # shape = (num_classes, )
            S_a = np.sum(S_i)
            S_m = S_i/self.num_omic_datasets

            if np.max(S_m) < self.sm_threshold or np.max(S_i/S_a) < self.si_threshold:
                preds.append(None) # Unknown

            else:
                preds.append(np.argmax(S_i) + 1) # index start from 0, classes start from 1

        return preds


    def compute_accuracy(self, preds, train=False):
        """
        :param train: whether to use y_train or y_test as ground truth
        """

        if train:
            ground_truth = self.y_train
        else:
            ground_truth = self.y_test

        # Consider None as a missed prediction
        accuracy = np.sum(ground_truth == preds) / len(ground_truth)

        return accuracy


    def train_eval(self):
        train_proba = []
        test_proba = []
        for clf, X_train, X_test in zip(self.classifiers, self.X_train_list, self.X_test_list):
            clf.fit(X_train, self.y_train)
            train_proba.append(clf.predict_proba(X_train))
            test_proba.append(clf.predict_proba(X_test))

        train_preds = self.integrate_predictions(train_proba)
        test_preds = self.integrate_predictions(test_proba)

        train_accuracy = self.compute_accuracy(train_preds, train=True)
        test_accuracy = self.compute_accuracy(test_preds, train=False)

        print(self.name + " train accuracy: {}".format(train_accuracy))
        print(self.name + " test accuracy: {}".format(test_accuracy))
