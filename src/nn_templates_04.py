# -*- coding: utf-8 -*-
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from imblearn.over_sampling import ADASYN, SMOTE

from sklearn.metrics import confusion_matrix, roc_auc_score

from keras.layers import *
from keras.metrics import *
from keras.callbacks import Callback
from keras.models import Sequential
from keras.optimizers import Adam
from keras.preprocessing.sequence import TimeseriesGenerator


# Global Variables

np.random.seed(0)  # NEVER CHANGE THIS

# split ratio
SPLIT_RATIO = 0.8

# how many years should be used to predict the outcome
PREDICTION_HORIZON = 5

# The batch size by which the training data is fed into the network.
BATCH_TRAINING = 10

# The function used to evaluate performace of the model and tune the parameters.
LOSS_FUNCTION = 'binary_crossentropy'

# The function by which your models parameters are adjusted to seek a local minimum.
# OPTIMIZER = adjusted within the network functions

# The rate at which the optimizer seeks the local minimum.
LEARNING_RATE = 0.1

# The number of iterations for which the model is trained.
EPOCHS = 3


class Model:
    # class to store the properties of a model
    def __init__(self, history, name):
        self.name = name
        self.history = history[0]
        self.roc_values = history[1]


class ROCCallback(Callback):
    # class to calculate the ROC metrics
    # as this can only be used AFTER an epoch, we have to
    # set a callback for ON_EPOCH_END
    def __init__(self, generator):
        self.gen = generator
        self.results = []

    def on_epoch_end(self, epoch, logs={}):
        # specify steps to account for the batch size
        y_pred = self.model.predict_generator(self.gen, len(self.gen.data) // BATCH_TRAINING)
        try:
            val_roc = roc_auc_score(self.gen.targets, y_pred)
            self.results.append(val_roc)
        except ValueError:
            # ROC_AUC_score func can't handle epochs where only one class is present
            # to catch those, use ValueError
            # TODO: replacement value?
            self.results.append(-1)
            pass


def NN_Standard(input_shape):
    # TODO: original paper uses Convolutional layer or Fully connected/Dense?
    model = Sequential()
    # model.add(Conv1D(filters=8, kernel_size=3, input_shape=input_shape))
    model.add(Dense(4, input_shape=input_shape))
    model.add(Flatten())
    model.add(Dense(1, activation='sigmoid'))

    opt = Adam(lr=LEARNING_RATE)
    model.compile(optimizer=opt,
                  loss=LOSS_FUNCTION,
                  metrics=['accuracy', Precision()])

    model.summary()
    roc_callback = ROCCallback(train_generator)
    history = model.fit_generator(train_generator, epochs=EPOCHS,
                                  callbacks=[roc_callback])

    return (history, roc_callback.results)


def NN_Deep(input_shape):
    model = Sequential()
    model.add(Dense(16, input_shape=input_shape))
    model.add(Dense(16, input_shape=input_shape))
    model.add(Dense(16, input_shape=input_shape))
    model.add(Dense(16, input_shape=input_shape))
    model.add(Flatten())
    model.add(Dense(1, activation='sigmoid'))

    opt = Adam(lr=LEARNING_RATE)
    model.compile(optimizer=opt,
                  loss=LOSS_FUNCTION,
                  metrics=['accuracy', Precision()])

    model.summary()
    roc_callback = ROCCallback(train_generator)
    history = model.fit_generator(train_generator, epochs=EPOCHS,
                                  callbacks=[roc_callback])

    return (history, roc_callback.results)



def NN_Wide(input_shape):
    model = Sequential()
    model.add(Dense(22, input_shape=input_shape))
    model.add(Flatten())
    model.add(Dense(1, activation='sigmoid'))

    opt = Adam(lr=LEARNING_RATE)
    model.compile(optimizer=opt,
                  loss=LOSS_FUNCTION,
                  metrics=['accuracy', Precision()])

    model.summary()
    roc_callback = ROCCallback(train_generator)
    history = model.fit_generator(train_generator, epochs=EPOCHS,
                                  callbacks=[roc_callback])

    return (history, roc_callback.results)


def NN_LSTM(input_shape):
    model = Sequential()
    # LSTMs expect different shape, hence:
    model.add(LSTM(16, input_shape=input_shape, return_sequences=True))
    model.add(Flatten())
    model.add(Dense(1, activation='sigmoid'))

    opt = Adam(lr=LEARNING_RATE)
    model.compile(optimizer=opt,
                  loss=LOSS_FUNCTION,
                  metrics=['accuracy', Precision()])

    model.summary()

    # UNCOMMENT IF USING COLAB
    # config = tf.ConfigProto(
    #   device_count={'GPU': 1},
    #   intra_op_parallelism_threads=1,
    #   allow_soft_placement=True
    #   )
    # config.gpu_options.allow_growth = True
    # config.gpu_options.per_process_gpu_memory_fraction = 0.6
    # session = tf.Session(config=config)
    # with session.as_default():
    #     with session.graph.as_default():
    #           history = model.fit_generator(train_generator, epochs=EPOCHS,
    #                                   metrics=['accuracy', Precision()],
    #                                   callbacks=[roc_callback(train_generator)])
    #      score, acc = model.evaluate(test_generator)

    roc_callback = ROCCallback(train_generator)
    history = model.fit_generator(train_generator, epochs=EPOCHS,
                                  callbacks=[roc_callback])
    return (history, roc_callback.results)


def NN_CRNN(input_shape):
    model = Sequential()
    model.add(Conv1D(16, 3, input_shape=input_shape))
    model.add(LSTM(16))
    # model.add(Flatten())
    model.add(Dense(1, activation='sigmoid'))

    opt = Adam(lr=LEARNING_RATE)
    model.compile(optimizer=opt,
                  loss=LOSS_FUNCTION,
                  metrics=['accuracy', Precision()])

    model.summary()
    # UNCOMMENT IF USING COLAB
    # config = tf.ConfigProto(
    #   device_count={'GPU': 1},
    #   intra_op_parallelism_threads=1,
    #   allow_soft_placement=True
    #   )
    # config.gpu_options.allow_growth = True
    # config.gpu_options.per_process_gpu_memory_fraction = 0.6
    # session = tf.Session(config=config)
    # with session.as_default():
    #     with session.graph.as_default():
    #       history = model.fit_generator(train_generator, epochs=EPOCHS)
    #      score, acc = model.evaluate(test_generator)

    roc_callback = ROCCallback(train_generator)
    history = model.fit_generator(train_generator, epochs=EPOCHS,
                                  callbacks=[roc_callback])

    return (history, roc_callback.results)


# Load the Dataset

# Import dataset from relevant source(s)
# data_path = 'https://raw.githubusercontent.com/shrnkm/bankruptcy/master/data/processed/data.csv?token=AGV7MS4OJ76A77JF5FM5SBS6EVLSK'
data_path = '/Users/Anna/GitHub/bankruptcy/data/processed/data2.csv'
data = pd.read_csv(data_path)

labels = np.array(data.loc[:, "Bankrupt"])
data = data.drop(['Bankrupt'], axis=1)

print("\nNumber of data samples: {}\n Example entry: \n".format(len(data)))
print("{} => Label: {}".format(data.loc[0], labels[0]))

# transform pd dataframe to numpy array
data = np.array(data)


# Balance the dataset
# ADASYN throws runtime error:
# RuntimeError: Not any neigbours belong to the majority class. This case will induce a NaN case with a division by
# zero. ADASYN is not suited for this specific dataset. Use SMOTE instead.
# data_res, labels_res = ADASYN(n_neighbors=3).fit_sample(data, labels)
# passing 'minority' arg to only resample the minority class instead of both
# data_res, labels_res = SMOTE('minority').fit_sample(data, labels)

# print("\nLength after re-sampling: {}\n".format(len(data_res)))
# print("{} => Label: {}".format(data_res[0], labels_res[0]))

unique_ciks, indices = np.unique(data[:, 0], return_index=True)

new_data = []
new_labels = []
prev_idx = 0
for idx in indices:
    entries = range(prev_idx, idx)
    # only append most recent entries
    for entry in entries[-PREDICTION_HORIZON:]:
        new_data.append(data[entry])
        new_labels.append(labels[entry])
    prev_idx = idx

new_data = np.asarray(new_data)
new_labels = np.asarray(new_labels)

# get index where to split based on the unique CIKs
cik_split_idx = unique_ciks[int(len(unique_ciks) * SPLIT_RATIO)]

# find the CIK in data
# np.where returns first occurrence of index (= first entry of company)
overall_split_idx = np.where(new_data[:, 0].astype(int) == cik_split_idx)[0][0]

# Drop irrelevant columns (years, CIK)
new_data = np.delete(new_data, [0, 1], axis=1)

train_data = new_data[:overall_split_idx]
train_labels = new_labels[:overall_split_idx]
test_data = new_data[overall_split_idx:]
test_labels = new_labels[overall_split_idx:]

# print("Len train data: ", len(train_data), " last sample: ", train_data[-1])
# print("Len test data: ", len(test_data), " first sample: ", test_data[0])

# Investigate the Dataset

# Print relevant information about the dataset(s) structure.
print("Training samples: {}. Test samples: {}".format(len(train_data), len(test_data)))
print("Shape of one data point: {}".format(train_data[0].shape))
# print("Example data entry:\n\n{}".format(train_data[0]))


# Build the dataset

num_features = train_data[0].shape[0]

print("\n\n Generating Time Series Generator..")
# Initialize the time-series generators
# length = how many years to use for one target (use LENGTH inputs to predict Y)
# batch size = how many companies to pass during one forward pass
# stride = NEVER overlap companies since this would result in wrong labels
# hence, start next time series input AFTER the last one
train_generator = TimeseriesGenerator(train_data, train_labels, length=PREDICTION_HORIZON,
                                      batch_size=BATCH_TRAINING, stride=PREDICTION_HORIZON+1)
test_generator = TimeseriesGenerator(test_data, test_labels, length=PREDICTION_HORIZON)

# Inspect the generator
# train_generator.targets = labels
print('Number of samples: {}'.format(len(train_generator.data)))
# corresponds to batch size
print('Number of companies in first input pass: {}'.format(len(train_generator[0])))
print('Number of years to use for one output: '.format(train_generator.length))

# Train and build the models
models = [
  Model(NN_Standard((PREDICTION_HORIZON, num_features)), 'Default Network'),
  Model(NN_Deep((PREDICTION_HORIZON, num_features)), 'Deep Network'),
  Model(NN_Wide((PREDICTION_HORIZON, num_features)), 'Wide Network'),
  Model(NN_LSTM((PREDICTION_HORIZON, num_features)), 'LSTM Network'),
  Model(NN_CRNN((PREDICTION_HORIZON,num_features)), 'CRNN Network')
]


# Visualize the Training Process

fig, axs = plt.subplots(len(models), 4, figsize=(25, 30), facecolor='w', edgecolor='k')
fig.subplots_adjust(hspace=0.5, wspace=0.1)

for i in range(len(models)):
    axs[i][0].plot(models[i].history.history['loss'])
    axs[i][0].set_title('Training Loss: {}'.format(models[i].name))
    axs[i][0].set_ylabel('Loss')
    axs[i][0].set_xlabel('Epoch')

    axs[i][1].plot(models[i].history.history['accuracy'], 'tab:red')
    axs[i][1].set_title('Training Accuracy: {}'.format(models[i].name))
    axs[i][1].set_ylabel('Accuracy')
    axs[i][1].set_xlabel('Epoch')

    axs[i][2].plot(models[i].history.history['precision_{}'.format(i+1)], 'tab:red')
    axs[i][2].set_title('Training Precision: {}'.format(models[i].name))
    axs[i][2].set_ylabel('Precision')
    axs[i][2].set_xlabel('Epoch')

    axs[i][3].plot(models[i].roc_values, 'tab:red')
    axs[i][3].set_title('Training ROC: {}'.format(models[i].name))
    axs[i][3].set_ylabel('ROC')
    axs[i][3].set_xlabel('Epoch')


# Evaluate Models on Test Data
# val_score returns the scores as a list: loss, acc, precision
for m in models:
    val_score = m.history.model.evaluate_generator(test_generator)
    print("{} - ROC values: {}".format(m.name, m.roc_values))
    print('{} - Scores on test dataset: {}'.format(m.name, val_score))

# Additional Tasks

# TODO: Visualize test data accuracy in the same plot as the training data.
# TODO: Plot precision and ROC.
# TODO: Resolve confusion matrix for assessing test data results.
# TODO: Make sure benchmarks and network models are evaluated on same metrics.
# TODO: Test different network architectures and layer types. Compare results.
# TODO: Test different optimizers.
# Optimization

# Batch normalization.
# Adjust the learning rate.
# Dropout.
# Add a plot of the test learning and accuracy atop the training data plots.
# Learning rate schedule keras.optimizers.schedules.ExponentialDecay()
