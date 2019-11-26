# -*- coding: utf-8 -*-
"""ANN_BP_NN01.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1m40Q7-Rc384_dfwQmV_vJfsG8fa3qKoR

** Keras Documentation**
https://www.tensorflow.org/api_docs/python/tf/keras
"""

import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from keras.layers import *
from keras.optimizers import Adam
from keras.models import Sequential
from keras.models import Model

warnings.filterwarnings("ignore",category=FutureWarning)
warnings.filterwarnings("ignore",category=DeprecationWarning)

np.random.seed(0)


# TODO: ADJUST ARCHITECTURE
def cnn_wide_model(input_data):
    '''
    TODO: OPTI
    '''

    model = Sequential()
    model.add(Dense(16, input_shape=(22,)))
    model.add(Dense(2, activation='softmax'))

    # initialise model
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model


# TODO: MODEL FOR DEEP ARCHITECTURE

bankrupt = 'https://raw.githubusercontent.com/shrnkm/bankruptcy/master/data/Eikon/small_test_sets/data_test_bankrupt.csv?token=AMBTQIEV7VWAY2KAK6GZV7S53OPL6'
healthy = 'https://raw.githubusercontent.com/shrnkm/bankruptcy/master/data/Eikon/small_test_sets/data_test_healthy.csv?token=AMBTQIFF3U567WU6RETK7DK53OPNO'

df_bankrupt = pd.read_csv(bankrupt)
df_healthy = pd.read_csv(healthy)
df_mixed = pd.concat([df_bankrupt, df_healthy])

print('\nExample Entry of a healthy company:\n\n', df_bankrupt.loc[0])

temp_data = df_mixed.drop(['Instrument', 'Bankrupt'], axis=1)
temp_labels = df_mixed['Bankrupt']
temp_cik = df_mixed['Instrument']

labels = []
cik = []
data = []

for i in range(0,len(df_mixed.index),20):
  labels.append(temp_labels.values[i])
  cik.append(temp_cik.values[i])
  data.append(temp_data.values[i])

# TODO: Normalize the data.
# data_norm = (data - np.mean(data)) / np.std(data)

# TODO: Visualize the normalized data.
# TODO: Handle the different years for each company.

# Split the data
split = int(len(data) * 0.8)
print("Split: {}, Length: {}".format(split, len(data)))
train_data = np.array(data[:split])
train_labels = np.array(labels[:split])
test_data = np.array(data[split:])
test_labels = np.array(labels[split:])

print("Length train: {}, Length test: {}".format(len(train_data), len(test_data)))


# TODO: read in textual data
# df_b['Mean Embedding'] = pd.Series(DATA, index=df_b.index)

# TODO: Test a deep network.
# TODO: Test a wide network.

# TODO: Decide optimizer.
# TODO: Decide loss function.
# TODO: Decide number of training epochs.

# model = cnn_wide_model(train_data)


# define model's architecture
model = Sequential()
model.add(Dense(16, input_shape=(22,)))
model.add(Dense(2, activation='softmax'))

# initialise model
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# print overview
model.summary()

# train and save results in history
history = model.fit(train_data, train_labels, batch_size=32, epochs=20)

# test_loss, test_acc = model.evaluate(test_data,  test_labels, verbose=2)

# print('\nTest accuracy:', test_acc)

# PLOTTING
# list all data in history
print(history.history.keys())

# summarize history for accuracy
plt.plot(history.history['acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.ylim(0, 1)
plt.legend(['accuracy'], loc='upper right')
plt.show()

# summarize history for loss
'''plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()'''

# predictions = model.predict(test_data)
# for i in predictions:
#   print[i]