import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

import pandas as pd
import numpy as np
# from adasyn import ADASYN
import matplotlib.pyplot as plt

from keras.layers import *
from keras.optimizers import Adam
from keras.models import Sequential
from keras.models import Model
from keras.preprocessing.sequence import TimeseriesGenerator

from tensorflow import py_function
from tensorflow import unique as tunqiue
from tensorflow import double as tdouble

from sklearn.metrics import roc_auc_score, precision_score

np.random.seed(0)


def cnn_standard_model(input_shape):
    """
    Implements the wide CNN architecture proposed by Mai et. al
    :param input_shape: Data Sequence's shape (tuple)
    :return: compiled/init model
    """
    print('Shape: ', input_shape)
    model = Sequential()
    model.add(Dense(16, input_shape=input_shape))
    model.add(Flatten()) # avoid dim error
    model.add(Dense(1, activation='sigmoid'))  # sigmoid for binary

    # init step
    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  # TODO: ROC Score
                  metrics=['accuracy', precision])

    return model


def precision(y_true, y_pred):
    """
    Function to calculate the precision metric
    :param y_true: ground truth labels
    :param y_pred: prediction
    :return: precision value
    """
    # TODO: fix 0 return due to UndefinedMetricWarning: Precision is ill-defined and being set to 0.0 due to no predicted samples
    # fix of passing tf.unique(y_pred) did not work
    return py_function(precision_score, (y_true, y_pred), tdouble)


def roc_score(y_true, y_pred):
    """
    Function to calculate the ROC score metric
    :param y_true: ground truth labels
    :param y_pred: prediction
    :return: ROC score
    """
    return py_function(roc_auc_score, (y_true, y_pred), tdouble)


# read in the dataset
bankrupt = 'https://raw.githubusercontent.com/shrnkm/bankruptcy/master/data/Eikon/small_test_sets/data_test_bankrupt.csv?token=AGV7MSYDPC5VTFWFYCHH2NC54TTUU'
healthy = 'https://raw.githubusercontent.com/shrnkm/bankruptcy/master/data/Eikon/small_test_sets/data_test_healthy.csv?token=AGV7MS4YUG4JXQ34EHSXNV254TTYO'

df_mixed = pd.concat([pd.read_csv(bankrupt), pd.read_csv(healthy)])
# TODO: Visualize the normalized data.
print('Number of samples in dataset: ' + str(len(df_mixed)))
print('\nExample Entry of a company:\n\n', df_mixed.loc[0])

# TODO: Normalize the data.
# data_norm = (data - np.mean(data)) / np.std(data)
# or to use keras: keras.utils.normalize(x, axis=-1, order=2)
# where order 2 means use L2 norm


# Split data based on years (80% of all years for training, 20% for testing)
split = 20 * 0.8
split_idx = 2000 + split
print("\nSplit after year {}".format(split))

train_data = np.array(df_mixed.loc[df_mixed['Year'] <= split_idx].values)
train_labels = np.array(df_mixed.loc[df_mixed['Year'] <= split_idx]['Bankrupt'].values)
test_data = np.array(df_mixed.loc[df_mixed['Year'] > split_idx].values)
test_labels = np.array(df_mixed.loc[df_mixed['Year'] > split_idx]['Bankrupt'].values)

# drop irrelevant columns (years, instrument)
# print("Before: ", train_data.shape)
train_data = np.delete(train_data, 0, axis=1)
train_data = np.delete(train_data, -2, axis=1)
# print("After: ", train_data.shape)
print("Length train data: {}, Length test data: {}".format(len(train_data), len(test_data)))


# TRAINING
# network settings
num_features = train_data[0].shape[0]
num_inputs = int(split)

# one company consists of 20 entries (as 20 years of data) -> length = 20
# BUT: split at year 2016, which means 4 years are put to the test_data -> length = 16
# the next input pass uses by default the data with index +1 , meaning the company data will overlap
# hence, set stride to 17
train_generator = TimeseriesGenerator(train_data, train_labels, length=num_inputs, batch_size=2, stride=num_inputs+1)
test_generator = TimeseriesGenerator(test_data, test_labels, length=num_inputs)

print('Num Samples: {}'.format(len(train_generator)))
print('Num Samples in first input pass: {}'.format(len(train_generator[0])))

# print sample
# x, y = train_generator[0]
# print('%s => %s' % (x, y))

# initialise model
default_model = cnn_standard_model((num_inputs, num_features))

# print overview
default_model.summary()

# TRAIN
history = default_model.fit_generator(train_generator, epochs=2)

# test_loss, test_acc = model.evaluate(test_data,  test_labels, verbose=2)
# print('\nTest accuracy:', test_acc)

# list all data in history
print(history.history.keys())

# summarize history for accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['precision'])
plt.title('model performance')
plt.ylabel('metric')
plt.xlabel('epoch')
plt.ylim(0, 1)
plt.legend(['accuracy'], loc='upper right')
plt.show()

# summarize history for loss
plt.plot(history.history['loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper right')
plt.show()
