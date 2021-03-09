import scipy.stats as stats
import numpy as np
import csv
import copy

print("\nLAB 5 ASSIGNMENT 1\n")

filepath = ""
filename = "dataset_LUMINAL_A_B.csv"
alpha = 0.05

header = ""
data = []
with open(filepath+filename, "r") as f:
    reader = csv.reader(f, delimiter=",")
    for i, row in enumerate(reader):
        buffer = []
        for col in row:
            if i == 0:
                # print(col[0:15])
                buffer.append(col[0:15])    # ignore character after "." and "."
            else:
                buffer.append(col.strip())
        if i == 0:
            header = copy.deepcopy(buffer)  # store header
        else:
            data.append(buffer)             # add row

for i, row in enumerate(data):
    print(row)
    if i == 30:
        break

print("\nN_rows: "+str(len(data))+"    N_columns: "+str(len(data[0]))+"\n")

lumA_X = np.array([i[1:] for i in data[0:50]], dtype=float)       # extract lumA info
lumA_Y = np.array([i[0] for i in data[0:50]])
lumB_X = np.array([i[1:] for i in data[50:100]], dtype=float)     # extract lumB info
lumB_Y = np.array([i[0] for i in data[50:100]])

G = 1022     # n_features
b_adj_alpha = alpha/G     # bonferroni adjustment

feature_stats = []
for i in range(len(data[0])-1):
    lumA_vec = np.array(lumA_X[:, i], dtype=float)
    lumB_vec = np.array(lumB_X[:, i], dtype=float)
    # print(f"lumA_vec shape = {lumA_vec.shape}")
    # print(f"lumA_vec shape = {lumB_vec.shape}")
    t_value, p_value = stats.ttest_ind(lumA_vec, lumB_vec, equal_var=False)     # compute statistics
    if p_value < b_adj_alpha:                                                   # filter features
        feature_stats.append([i, t_value, p_value])

print(f"P value shape: {len(p_value)}")

print(f"\nN selected features = {len(feature_stats)}")
for i, row in enumerate(feature_stats):
    print(row)
    if i == 30:
        break


filepath = ""
filename = "ensembl_to_common.txt"
ensToCom = dict()
with open(filepath+filename, "r") as f:
    reader = csv.reader(f, delimiter=",")
    for i, row in enumerate(reader):
        buffer = []
        for j, col in enumerate(row):
            buffer.append(col)
        ensToCom[buffer[0]] = buffer[1].strip()                  # create dictionary from file

# print(ensToCom)

print(header)
selected_feature_names = []
for feature in feature_stats:
    print(feature[0])
    ens = header[feature[0]+1]
    com = ensToCom[str(ens)]
    selected_feature_names.append(com)
print(selected_feature_names)

oneHot = {"Luminal A":0, "Luminal B":1}
newHeader  = ["l"]
newHeader += selected_feature_names
newDataSet = np.array([oneHot[i[0]] for i in data], dtype=float)        # oneHot encoding of labels
# print(newDataSet)
# print(newDataSet.shape)
newDataSet = np.expand_dims(newDataSet, axis=1)     # create reduced dataset
# print(newDataSet)
# print(newDataSet.shape)
for feature in feature_stats:
    newFeature = np.array([i[feature[0]+1] for i in data], dtype=float)
    newFeature = np.expand_dims(newFeature, axis=1)
    newDataSet = np.concatenate((newDataSet, newFeature), axis=1)

# print(newDataSet)
# print(newDataSet.shape)

print("\nStart writing...")         # store reduced dataset
outpath = ""
outfilename = "newDataSet.csv"
f = open(outpath+outfilename, "w")
for i, row in enumerate(newHeader):
    if i != len(newHeader)-1:
        f.write(f"{str(row)}, ")
    else:
        f.write(f"{str(row)}\n")
for i, row in enumerate(newDataSet):
    if i % 10 == 0:
        print(f"percentage... {i/len(data)*100}")
    for j, col in enumerate(row):
        if j != len(row)-1:
            f.write(f"{col}, ")
        else:
            f.write(f"{col}\n")
f.close()
print("End!\n")

