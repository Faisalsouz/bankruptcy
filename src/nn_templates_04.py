# -*- coding: utf-8 -*-
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, roc_auc_score
from imblearn.over_sampling import ADASYN

from keras.layers import *
from keras.metrics import *
from keras.callbacks import Callback
from keras.models import Sequential
from keras.optimizers import Adam
from keras.preprocessing.sequence import TimeseriesGenerator


# Global Variables

np.random.seed(0)  # NEVER CHANGE THIS

# The batch size by which the training data is fed into the network.
BATCH_TRAINING = 2

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
    model.add(Conv1D(filters=8, kernel_size=3, input_shape=input_shape))
    # model.add(Dense(4, input_shape=input_shape))
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
# TODO: Load full dataset, including embedding features.
bankrupt = 'https://raw.githubusercontent.com/shrnkm/bankruptcy/master/data/Eikon/small_test_sets/data_test_bankrupt.csv?token=AMBTQIEDX3Y6THOUJCBWE5C57D2BI'
healthy = 'https://raw.githubusercontent.com/shrnkm/bankruptcy/master/data/Eikon/small_test_sets/data_test_healthy.csv?token=AMBTQIDFPLUT2BGKOBNM2GK57D2EK'
df_mixed = pd.concat([pd.read_csv(bankrupt), pd.read_csv(healthy)])

# Balance the dataset using adasyn
data = np.array(df_mixed.drop(['Instrument', 'Bankrupt'], axis=1).values)
labels = np.array(df_mixed['Bankrupt'])
data_res, labels_res = ADASYN(n_neighbors=3).fit_sample(data, labels)

# TODO: normalize?

# # Split data based on years (80% of all years for training, 20% for testing).
split = 20 * 0.8
print("\nSplit after year {}".format(split))

train_data = []
train_labels = []
test_data = []
test_labels = []

idx = 0
for i in range(len(data_res)):
    if idx <= split:
        train_data.append(data_res[i])
        train_labels.append(labels_res[i])
    else:
        test_data.append(data_res[i])
        test_labels.append(labels_res[i])
        if idx == split + 3:
            idx = 0
            continue
    idx += 1

# Drop irrelevant columns (years, instrument).
train_data = np.delete(train_data, 0, axis=1)
train_data = np.delete(train_data, -2, axis=1)
test_data = np.delete(test_data, 0, axis=1)
test_data = np.delete(test_data, -2, axis=1)
print("Length train data: {}, Length test data: {}".format(len(train_data), len(test_data)))


# Investigate the Dataset

# Print relevant information about the dataset(s) structure.
print("Number of training instruments: {}\nNumber of test instruments:{}".format(len(train_data), len(test_data)))
print("Shape of one instrument datapoint: {}".format(train_data[0].shape))
print("Example instrument:\n\n{}".format(df_mixed.loc[0]))

# TODO:
# Visualize the Dataset
# Visualize specific examples from the dataset to gain understanding of what each datapoint is composed.


# Build the dataset

num_features = train_data[0].shape[0]
num_inputs = int(split)

# Initialize the time-series generators
train_generator = TimeseriesGenerator(train_data, train_labels, length=num_inputs, batch_size=BATCH_TRAINING, stride=num_inputs+1)
# TODO: fix length as the input for the test gen is only 3 and not 16! (year 2017-2019!)
test_generator = TimeseriesGenerator(test_data, test_labels, length=num_inputs)

# Inspect the generator
print('Number of samples: {}'.format(len(train_generator)))
print('Number of samples in first input pass: {}'.format(len(train_generator[0])))
print("Length of test generator: {}".format(len(test_generator.data)))


# Train and build the models
models = [
  Model(NN_Standard((num_inputs, num_features)), 'Default Network'),
  Model(NN_Deep((num_inputs, num_features)), 'Deep Network'),
  Model(NN_Wide((num_inputs, num_features)), 'Wide Network'),
  Model(NN_LSTM((num_inputs, num_features)), 'LSTM Network'),
  Model(NN_CRNN((num_inputs,num_features)), 'CRNN Network')
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
