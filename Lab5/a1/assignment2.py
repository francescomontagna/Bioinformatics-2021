import pandas as pd
import numpy as np

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier as KNN
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

def metrics(preds, ground_truth, labels):

    tp = np.sum(np.array(preds == ground_truth) & np.array(preds == labels[0]))
    tn = np.sum(np.array(preds == ground_truth) & np.array(preds == labels[1]))
    fp = np.sum(np.array(preds != ground_truth) & np.array(preds == labels[0]))
    fn = np.sum(np.array(preds != ground_truth) & np.array(preds == labels[1]))

    accuracy = (tp+tn)/(tp+tn+fp+fn)

    precision = tp/(fp+tp)
    recall = tp/(tp+fn)
    F1 = 2*recall*precision/(recall + precision)

    return accuracy, F1


def main():
    DATA_PATH = 'dataset.csv'
    REDUCED_DATA_PATH = 'reduced_dataset.csv'

    dataset = pd.read_csv(DATA_PATH, header=0)
    reduced_dataset = pd.read_csv(REDUCED_DATA_PATH, header=0)

    # Process dataset
    dataset = dataset.replace(np.nan, 0)
    X = dataset.iloc[:, 1:]
    y = dataset.iloc[:, 0]

    # Unique labels
    labels = y.unique()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Scale and reduce training data
    scaler = StandardScaler()
    X_train_std = scaler.fit_transform(X_train)
    pca = PCA(0.8, svd_solver='full', random_state=42)  # retain first 80 principal components
    X_train_pca = pca.fit_transform(X_train_std)

    # Scale and reduce test data
    X_test_std= scaler.transform(X_test)
    X_test_pca = pca.transform(X_test_std)

    # Train KNN
    model = KNN(5)
    model.fit(X_train_pca, y_train)
    preds = model.predict(X_test_pca)
    accuracy, F1 = metrics(preds, y_test, labels)
    f1 = f1_score(y_test, preds, pos_label='Luminal A')
    print(f'sklearn F1 score: {f1}')
    print(f"KNN dataset accuracy: {accuracy}")
    print(f"KNN dataset F1:{F1}")

    # Train SVM
    model = SVC()
    model.fit(X_train_pca, y_train)
    preds = model.predict(X_test_pca)
    accuracy, F1 = metrics(preds, y_test, labels)
    print(f"SVM dataset accuracy: {accuracy}")
    print(f"SVM dataset F1:{F1}")

    # Train Random Forest
    model = RandomForestClassifier()
    model.fit(X_train_pca, y_train)
    preds = model.predict(X_test_pca)
    accuracy, F1 = metrics(preds, y_test, labels)
    print(f"RFC dataset accuracy: {accuracy}")
    print(f"RFC dataset F1:{F1}")

    print()

    # Classifier on reduced_dataset
    reduced_dataset = reduced_dataset.replace(np.nan, 0)
    X = reduced_dataset.iloc[:, 1:]
    y = reduced_dataset.iloc[:, 0]

    # Unique labels
    labels = y.unique()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Scale and reduce training data
    scaler = StandardScaler()
    X_train_std = scaler.fit_transform(X_train)

    # Scale and reduce test data
    X_test_std = scaler.transform(X_test)

    # Train KNN
    model = KNN(5)
    model.fit(X_train_std, y_train)
    preds = model.predict(X_test_std)
    accuracy, F1 = metrics(preds, y_test, labels)
    f1
    print(f"KNN reduced dataset accuracy: {accuracy}")
    print(f"KNN reduced dataset F1:{F1}")

    # Train SVM
    model = SVC()
    model.fit(X_train_std, y_train)
    preds = model.predict(X_test_std)
    accuracy, F1 = metrics(preds, y_test, labels)
    print(f"SVM reduced dataset accuracy: {accuracy}")
    print(f"SVM reduced dataset F1:{F1}")

    # Train Random Forest
    model = RandomForestClassifier()
    model.fit(X_train_std, y_train)
    preds = model.predict(X_test_std)
    accuracy, F1 = metrics(preds, y_test, labels)
    print(f"RFC reduced dataset accuracy: {accuracy}")
    print(f"RFC reduced dataset F1:{F1}")


if __name__ == '__main__':
    main()
