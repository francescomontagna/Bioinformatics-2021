from sklearn.metrics import confusion_matrix, accuracy_score
import numpy as np

if __name__ == '__main__':

    y_true = np.array([2, 0, 2, 2, 0, 1])
    y_pred = np.array([0, 0, 2, 2, 0, 2])
    matrix = confusion_matrix(y_true, y_pred)
    print(matrix.diagonal()/matrix.sum(axis=1))
    print(matrix)

    for label in np.unique(y_true):
        mask = y_true == label
        accuracy = accuracy_score(y_true[mask], y_pred[mask])
        print(f'Accuracy for label {label}: {accuracy}')