# -*- coding: utf-8 -*-
"""NN_Templates_02.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TKiwhrXd9RoGGKyT6ixu3qcsC1DlUmRM

### Imports
"""

# Commented out IPython magic to ensure Python compatibility.
# TODO: Update for tf 2.0
# %tensorflow_version 1.x
import numpy as np
import pandas as pd
# import tensorflow as tf
import matplotlib.pyplot as plt
from keras.models import Sequential
from sklearn.metrics import confusion_matrix
from imblearn.over_sampling import ADASYN
from keras.layers import *
from keras.optimizers import Adam
from keras.preprocessing.sequence import TimeseriesGenerator

"""### Global Variables"""

# The batch size by which the training data is fed into the network.
BATCH_TRAINING = 2

# The function used to evaluate performace of the model and tune the parameters.
LOSS_FUNCTION = 'binary_crossentropy'

# The function by which your models parameters are adjusted to seek a local minimum.
# OPTIMIZER = adjusted within the network functions

# The rate at which the optimizer seeks the local minimum.
LEARNING_RATE = 1

# The number of iterations for which the model is trained.
EPOCHS = 1

"""### Load the Dataset"""

# Import dataset from relevant source(s).
# TODO: Load full dataset, including embedding features.
bankrupt = 'https://raw.githubusercontent.com/shrnkm/bankruptcy/master/data/Eikon/small_test_sets/data_test_bankrupt.csv?token=AMBTQIDCC3ZC4ECD7ASS3C255YSKE'
healthy = 'https://raw.githubusercontent.com/shrnkm/bankruptcy/master/data/Eikon/small_test_sets/data_test_healthy.csv?token=AMBTQIDK3IT5NIWOZN6ULUC55YSLW'
df_mixed = pd.concat([pd.read_csv(bankrupt), pd.read_csv(healthy)])
np.random.seed(0)

# Normalize the dataset per Cora and Fatimah.
data = np.array(df_mixed.drop(['Instrument', 'Bankrupt'], axis=1).values)
labels = np.array(df_mixed['Bankrupt'])
data_res, labels_res = ADASYN(n_neighbors = 3).fit_sample(data, labels)

# # Split data based on years (80% of all years for training, 20% for testing).
split = 20 * 0.8
print("\nSplit after year {}".format(split))
train_data = []
train_labels = []
test_data = []
test_labels = []

idx = 0
for i in range(len(data_res)):
    if (idx <= split):
        train_data.append(data_res[i])
        train_labels.append(labels_res[i])
    else:
        test_data.append(data_res[i])
        test_labels.append(labels_res[i])
        if idx == split + 3:
            idx = 0
            continue
    idx += 1

# Old Split.
# split = 20 * 0.8
# split_idx = 2000 + split
# train_data = np.array(df_mixed.loc[df_mixed['Year'] <= split_idx].values)
# train_labels = np.array(df_mixed.loc[df_mixed['Year'] <= split_idx]['Bankrupt'].values)
# test_data = np.array(df_mixed.loc[df_mixed['Year'] > split_idx].values)
# test_labels = np.array(df_mixed.loc[df_mixed['Year'] > split_idx]['Bankrupt'].values)
# print("\nSplit after year {}".format(split))

# Drop irrelevant columns (years, instrument).
train_data = np.delete(train_data, 0, axis=1)
train_data = np.delete(train_data, -2, axis=1)

test_data = np.delete(test_data, 0, axis=1)
test_data = np.delete(test_data, -2, axis=1)
print("Length train data: {}, Length test data: {}".format(len(train_data), len(test_data)))

"""### Investigate the Dataset"""

# Print relevant information about the dataset(s) structure.
print("Number of training instruments: {}\nNumber of test instruments:{}".format(len(train_data), len(test_data)))
print("Shape of one instrument datapoint: {}".format(train_data[0].shape))

"""### Visualize the Dataset"""

# Visualize specific examples from the dataset to gain understanding of what each datapoint is composed.
print("Example instrument:\n\n{}".format(df_mixed.loc[0]))

"""### Build the TensorFlow Dataset"""

# Network variables.
num_features = train_data[0].shape[0]
num_inputs = int(split)

# Initialize the time-series generators.
train_generator = TimeseriesGenerator(train_data, train_labels, length=num_inputs, batch_size=BATCH_TRAINING, stride=num_inputs+1, shuffle=True)
test_generator = TimeseriesGenerator(test_data, test_labels, length=num_inputs)

# Visualize the newly created generator.
print('Number of samples: {}'.format(len(train_generator)))
print('Number of samples in first input pass: {}'.format(len(train_generator[0])))

print(len(test_generator.data))

"""### Build the Model(s)"""

# Instantiate functions for each desired network architecture.

# TODO: Test different network architectures and layer types. Compare results.
# TODO: Test different optimizers.

# Standard NN based on Mai et al.
def NN_Standard(input_shape):
    print('Shape: ', input_shape)
    model = Sequential()
    model.add(Dense(4, input_shape=input_shape))
    model.add(Flatten())
    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer='adam',
                  loss=LOSS_FUNCTION,
                  # TODO: ROC Score
                  metrics=['accuracy'])

    model.summary()

    return model


# A deep NN.
def NN_Deep(input_shape):
    print('Shape: ', input_shape)
    model = Sequential()
    model.add(Dense(4, input_shape=input_shape))
    model.add(Dense(4, input_shape=input_shape))
    model.add(Dense(4, input_shape=input_shape))
    model.add(Dense(4, input_shape=input_shape))
    model.add(Flatten())
    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer='adam',
                  loss=LOSS_FUNCTION,
                  # TODO: ROC Score
                  metrics=['accuracy'])

    model.summary()

    return model

# A wide NN.
def NN_Wide(input_shape):
    print('Shape: ', input_shape)
    model = Sequential()
    model.add(Dense(22, input_shape=input_shape))
    model.add(Flatten())
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer='adam',
                  loss=LOSS_FUNCTION,
                  # TODO: ROC Score
                  metrics=['accuracy'])

    model.summary()

    return model


def lstm_model(input_shape):
    """
    Implements a network with LSTM architecture
    :param input_shape: Data Sequence's shape (tuple)
    :return: compiled/init model
    """
    model = Sequential()
    model.add(LSTM(16, input_shape=input_shape))
    model.add(Flatten())
    model.add(Dense(1, activation='sigmoid'))  # sigmoid for binary

    # init step
    model.compile(optimizer='adam',
                  loss=LOSS_FUNCTION,
                  # TODO: ROC Score
                  metrics=['accuracy'])

    model.summary()

    return model


def crnn_model(input_shape):
    """
    Implements a network with CRNN architecture
    :param input_shape: Data Sequence's shape (tuple)
    :return: compiled/init model
    """
    model = Sequential()
    model.add(Conv1D(16, 3, input_shape=input_shape))
    model.add(LSTM(16))
    model.add(Flatten())
    model.add(Dense(1, activation='sigmoid'))  # sigmoid for binary

    # init step
    model.compile(optimizer='adam',
                  loss=LOSS_FUNCTION,
                  # TODO: ROC Score
                  metrics=['accuracy'])

    model.summary()

    return model



"""### Train the model."""

# Clear the session.
# keras.backend.clear_session()

# Initialize the selected model.
# model = NN_Standard((num_inputs, num_features))
# model = NN_Deep((num_inputs, num_features))
models = [NN_Standard((num_inputs, num_features)),
          NN_Wide((num_inputs, num_features)),
          NN_Deep((num_inputs, num_features))]
# models.append(lstm_model((num_inputs, num_features)))
# models.append(crnn_model((num_inputs, num_features)))

# Print details of the model.

# Train for appropriate number of epochs.
histories = []
for i in range(len(models)):
    histories.append(models[i].fit_generator(train_generator, epochs=EPOCHS))


"""### Visualize the Training Process"""

# Visualize evaluation measures for training and test data. 
# TODO: Plot precision and ROC.

fig, ax = plt.subplots(len(models), 2, figsize=(15, 70))
for i in range(len(models)):
    for j in range(2):
        if j == 0:
            ax[i][j].set_title("Accuracy")
            ax[i][j].plot(histories[i].history['accuracy'])
            ax[i][j].set_ylim([0, 1])
        elif j == 1:
            ax[i][j].set_title("Loss")
            ax[i][j].plot(histories[i].history['loss'])
        ax[i][j].axis('off')

"""### Evaluate Models on Test Data"""

# Evaluate model on test dataset.
for m in models:
    score, acc = m.evaluate(test_generator)
    print("Model: ", acc)

# TODO: Resolve confusion matrix for assessing test data results.
# TODO: Make sure benchmarks and network models are evaluated on same metrics.
