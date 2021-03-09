import sys
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score, f1_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier


if __name__ == '__main__':
    reduced_path = 'reduced_dataset.csv'
    luminal_path = 'dataset_LUMINAL_A_B.csv'

    X_red = []
    y_red = []
    with open(reduced_path, 'r') as f:
        header = f.readline()
        for line in f:
            fields = line.split(',')
            label = fields[0]
            sample = list(map(lambda x: float(x), fields[1:]))
            X_red.append(sample)
            y_red.append(label)

    X_red = np.array(X_red)
    y_red = np.array(y_red)

    X = []
    y = []
    with open(luminal_path, 'r') as f:
        header = f.readline()
        for line in f:
            fields = line.split(',')
            label = fields[0]
            sample = list(map(lambda x: float(x), fields[1:]))
            X.append(sample)
            y.append(label)

    X = np.array(X)
    y = np.array(y)

    X_train_r , X_test_r, y_train_r, y_test_r = train_test_split(X_red, y_red,\
                                                                 test_size=0.2, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y,\
                                                        test_size=0.2, random_state=42)

    # Standardize to remove mean and have unit variance
    # TODO mi accerto sia corretto
    scaler_r = StandardScaler()
    scaler = StandardScaler()
    X_train_r = scaler_r.fit_transform(X_train_r)
    X_train = scaler.fit_transform(X_train)
    X_test_r = scaler_r.transform(X_test_r)
    X_test = scaler.transform(X_test)

    # PCA
    pca = PCA(n_components=0.8, svd_solver='full')
    X_train_pca = pca.fit_transform(X_train)
    X_test_pca = pca.transform(X_test)

    # KNN on luminal
    knn = KNeighborsClassifier()
    knn.fit(X_train_pca, y_train)
    knn_preds = knn.predict(X_test_pca)
    knn_accuracy = accuracy_score(y_test, knn_preds)
    # knn_f1 = precision_recall_fscore_support(y_test, knn_preds)
    # print(f'KNN precision, recall, f1 score on luminal dataset: {knn_f1}')
    print(f'KNN accuracy score on luminal dataset: {knn_accuracy}')

    # KNN on reduced luminal
    knn = KNeighborsClassifier()
    knn.fit(X_train_r, y_train_r)
    knn_preds = knn.predict(X_test_r)
    knn_accuracy = accuracy_score(y_test_r, knn_preds)
    # knn_f1 = precision_recall_fscore_support(y_test, knn_preds)
    # print(f'KNN precision, recall, f1 score on reduced luminal dataset: {knn_f1}')
    print(f'KNN accuracy score on reduced luminal dataset: {knn_accuracy}')

    # SVM on luminal
    svm = SVC()
    svm.fit(X_train_pca, y_train)
    svm_preds = svm.predict(X_test_pca)
    svm_accuracy = accuracy_score(y_test, svm_preds)
    # svm_f1 = precision_recall_fscore_support(y_test, svm_preds)
    # print(f'SVM precision, recall, f1 score on luminal dataset: {svm_f1}')
    print(f'SVM accuracy score on luminal dataset: {svm_accuracy}')

    # SVM on reduced luminal
    svm = SVC()
    svm.fit(X_train_r, y_train_r)
    svm_preds = svm.predict(X_test_r)
    svm_accuracy = accuracy_score(y_test_r, svm_preds)
    # svm_f1 = precision_recall_fscore_support(y_test, svm_preds)
    # print(f'SVM precision, recall, f1 score on reduced luminal dataset: {svm_f1}')
    print(f'SVM accuracy score on reduced luminal dataset: {svm_accuracy}')

    # Random Forest on luminal
    rf = RandomForestClassifier()
    rf.fit(X_train_pca, y_train)
    rf_preds = rf.predict(X_test_pca)
    rf_accuracy = accuracy_score(y_test, rf_preds)
    # rf_f1 = precision_recall_fscore_support(y_test, rf_preds)
    # print(f'Random Forest precision, recall, f1 score on luminal dataset: {rf_f1}')
    print(f'Random Forest accuracy score on luminal dataset: {rf_accuracy}')

    # Random Forest on reduced luminal
    rf = RandomForestClassifier()
    rf.fit(X_train_r, y_train_r)
    rf_preds = rf.predict(X_test_r)
    rf_accuracy = accuracy_score(y_test_r, rf_preds)
    # rf_f1 = precision_recall_fscore_support(y_test, rf_preds)
    # print(f'Random Forest precision, recall, f1 score on reduced luminal dataset: {rf_f1}')
    print(f'Random Forest accuracy score on reduced luminal dataset: {rf_accuracy}')

    # GaussianNB on luminal
    naive_bayes = GaussianNB()
    naive_bayes.fit(X_train_pca, y_train)
    nb_preds = naive_bayes.predict(X_test_pca)
    nb_accuracy = accuracy_score(y_test, nb_preds)
    nb_f1 = f1_score(y_test, nb_preds, pos_label='Luminal A    ')
    print(f'GaussianNB f1 score on luminal dataset: {nb_f1}')
    print(f'GaussianNB accuracy score on luminal dataset: {nb_accuracy}')

    # GaussianNB on reduced luminal
    naive_bayes = GaussianNB()
    naive_bayes.fit(X_train_r, y_train)
    nb_preds = naive_bayes.predict(X_test_r)
    nb_accuracy = accuracy_score(y_test_r, nb_preds)

    print(f'GaussianNB accuracy score on reduced luminal dataset: {nb_accuracy}')
