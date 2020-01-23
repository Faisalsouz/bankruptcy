
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import metrics
from collections import Counter
# Import the model we are using
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, roc_curve
#from imblearn.over_sampling import ADASYN
from sklearn.linear_model import SGDClassifier
from sklearn.svm import SVC
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

#base_path = '/Users/Cora/Documents/UniOS/BP/'

df_mixed = pd.read_csv('data.csv')


#print('\nExample Entry of a healthy company:\n', df_healthy.loc[0])


temp_labels = df_mixed['Bankrupt']
#temp_cik = df_mixed['Instrument']
#temp_time = df_mixed['Year']
temp_data = df_mixed.drop(['Bankrupt'], axis=1)


labels = []
#cik = []
data = []
#data.extend((temp_data.values[0],temp_data.values[25], temp_data.values[51], temp_data.values[68]))
#labels.extend((temp_labels.values[1],temp_labels.values[26], temp_labels.values[52], temp_labels.values[69]))
print(temp_labels[17243:])

# Extracts data and labels of year 5 so we can predict the 7th
for i in range(0, len(df_mixed.index), 5):
    labels.append(temp_labels.values[i])
    data.append(temp_data.values[i])

# Convert to numpy array
data = np.array(data)
labels = np.array(labels)
#print('\nExample Entry of data:\n', data[196])
print('Original dataset shape %s' % Counter(labels))
# resample to get more bankrupt samples
#X_res, y_res = ADASYN(n_neighbors = 5, random_state = 0).fit_sample(data, labels)


#print('Resampled dataset shape %s' % Counter(y_res))

#train_data, test_data, train_labels, test_labels = train_test_split(X_res, y_res,
 #                                                                   test_size = 0.25,
 #                                                                   random_state = 0)

train_data, test_data, train_labels, test_labels = train_test_split(data, labels,
                                                                    test_size = 0.25,
                                                                    random_state = 0)

# Random forests
def rf(x_train, y_train, x_test):
    # Instantiate model with 1000 decision trees
    # Create a Gaussian Classifier
    crf = RandomForestClassifier(n_estimators=100)
    # Train the model on training data
    crf.fit(x_train, y_train)
    label_pred = crf.predict(x_test)

    # Model Accuracy, how often is the classifier correct?
    print("Forest Accuracy:", metrics.accuracy_score(test_labels, label_pred, 1))
    print("Forest Precision:", metrics.precision_score(test_labels, label_pred, 1))
    print("Forest ROC:", metrics.roc_curve(test_labels, label_pred, 1))

# Support Vector Machine
def svm(x_train, y_train, x_test):
    csvm = SVC(kernel='linear')
    csvm.fit(x_train, y_train)
    label_pred = csvm.predict(x_test)
    # Model Accuracy, how often is the classifier correct?
    print("SVM Accuracy:", metrics.accuracy_score(test_labels, label_pred, 1))
    print("SVM Precision:", metrics.precision_score(test_labels, label_pred, 1))
    print("SVM ROC:", metrics.roc_curve(test_labels, label_pred, 1))
# Linear Regression
def linReg(x_train, y_train, x_test):
    clr = SGDClassifier()
    # fit (train) the classifier
    clr.fit(x_train, y_train)
    label_pred = clr.predict(x_test)
    # Model Accuracy, how often is the classifier correct?
    print("Lin Reg Accuracy:", metrics.accuracy_score(test_labels, label_pred, 1))
    print("Lin Reg Precision:", metrics.precision_score(test_labels, label_pred, 1))
    print("Lin Reg ROC:", metrics.roc_curve(test_labels, label_pred, 1))
# MDA
def mda(x_train, y_train, x_test):
    cmda = LinearDiscriminantAnalysis()
    cmda.fit(x_train, y_train)
    label_pred = cmda.predict(x_test)
    # Model Accuracy, how often is the classifier correct?
    print("MDA Accuracy:", metrics.accuracy_score(test_labels, label_pred, 1))
    print("MDA Precision:", metrics.precision_score(test_labels, label_pred, 1))
    print("MDA ROC:", metrics.roc_curve(test_labels, label_pred, 1))

mda(train_data, train_labels, test_data)
svm(train_data, train_labels, test_data)
linReg(train_data, train_labels, test_data)
rf(train_data, train_labels, test_data)
