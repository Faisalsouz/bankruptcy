import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import collections
from sklearn import metrics
from collections import Counter
# Import the model we are using
from sklearn.ensemble import RandomForestClassifier
from matplotlib import pyplot as plt
from sklearn.metrics import precision_score, recall_score, roc_curve
from imblearn.over_sampling import ADASYN
from sklearn.linear_model import SGDClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

base_path = '/Users/Cora/Documents/UniOS/BP/'

df_bankrupt = pd.read_csv(base_path+'data_test_bankrupt.csv')
df_healthy = pd.read_csv(base_path+'data_test_healthy.csv')

#print('\nExample Entry of a healthy company:\n', df_healthy.loc[0])

df_mixed = pd.concat([df_bankrupt, df_healthy])
temp_data = df_mixed.drop(['Instrument', 'Bankrupt'], axis=1)
temp_labels = df_mixed['Bankrupt']
temp_cik = df_mixed['Instrument']


labels = []
cik = []
data = []
data.extend((temp_data.values[0],temp_data.values[25], temp_data.values[51], temp_data.values[68]))
labels.extend((temp_labels.values[1],temp_labels.values[26], temp_labels.values[52], temp_labels.values[69]))



# Extracts data and labels of year 2018 so we can predict 2019
for i in range(81, len(df_mixed.index), 20):
    labels.append(temp_labels.values[i+1])
    cik.append(temp_cik.values[i])
    data.append(temp_data.values[i])

# Convert to numpy array
data = np.array(data)
labels = np.array(labels)
print('\nExample Entry of data:\n', data[196])  # 197 Samples
#ada = ADASYN(ratio={1: 4, 0: 193}, n_neighbors = 4)
print('Original dataset shape %s' % Counter(labels))
X_res, y_res = ADASYN(n_neighbors = 3).fit_sample(data, labels)

print('Resampled dataset shape %s' % Counter(y_res))

train_data, test_data, train_labels, test_labels = train_test_split(X_res, y_res,
                                                                    test_size = 0.25,
                                                                    random_state = 0)
#print('Training Data Shape:', train_data.shape)
#print('Training Labels Shape:', train_labels.shape)
#print('Testing data Shape:', test_data.shape)
#print('Testing Labels Shape:', test_labels.shape)

# Check number of bankrupt companies in test data
#print('Number of healthy and bankrupt in test data: ', collections.Counter(labels))

def rf(x_train, y_train, x_test):
    # Instantiate model with 1000 decision trees
    # Create a Gaussian Classifier
    crf = RandomForestClassifier(n_estimators=100)
    # Train the model on training data
    crf.fit(x_train, y_train)
    label_pred = crf.predict(x_test)

    # Model Accuracy, how often is the classifier correct?
    print("Accuracy:", metrics.accuracy_score(test_labels, label_pred, 1))
    print("Precision:", metrics.precision_score(test_labels, label_pred, 1))

def svm(x_train, y_train, x_test):
    csvm = SVC(kernel='linear')
    csvm.fit(x_train, y_train)
    label_pred = csvm.predict(x_test)
    # Model Accuracy, how often is the classifier correct?
    print("Accuracy:", metrics.accuracy_score(test_labels, label_pred, 1))
    print("Precision:", metrics.precision_score(test_labels, label_pred, 1))

def LinReg(x_train, y_train, x_test):
    clf = SGDClassifier()
    # fit (train) the classifier
    clf.fit(x_train, y_train)
    label_pred = clf.predict(x_test)
    # Model Accuracy, how often is the classifier correct?
    print("Accuracy:", metrics.accuracy_score(test_labels, label_pred, 1))
    print("Precision:", metrics.precision_score(test_labels, label_pred, 1))
    
def mda(x_train, y_train, x_test):
    cmda = LinearDiscriminantAnalysis()
    cmda.fit(x_train, y_train)
    label_pred = cmda.predict(x_test)
    # Model Accuracy, how often is the classifier correct?
    print("MDA Accuracy:", metrics.accuracy_score(test_labels, label_pred, 1))
    print("MDA Precision:", metrics.precision_score(test_labels, label_pred, 1))


print(rf(train_data, train_labels, test_data))
print(svm(train_data, train_labels, test_data))
print(LinReg(train_data, train_labels, test_data))
