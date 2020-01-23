# imports needed for observing an experiment
from sacred import Experiment
from sacred.observers import MongoObserver
from sacred.utils import apply_backspaces_and_linefeeds

# other imports
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from sklearn.metrics import confusion_matrix
from tensorflow.keras.layers import *
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import Callback

# now let us set up the experiment
ex = Experiment('Standard')
# and add the observe to the experiment -> this will store the data in the cloud
ex.observers.append(MongoObserver(url='51.136.77.253:27017', db_name='dummy_test'))
# prevent that everything that is shown in the console is logged
ex.captured_out_filter = apply_backspaces_and_linefeeds

@ex.config  # Configuration is defined through local variables.
def cfg():
    neurons_first_layer = 16
    stride_first_layer = 3
    neurons_second_layer = 16
    optimizer = 'adam'
    loss = tf.keras.losses.BinaryCrossentropy()
    metrics = ['accuracy']
    epochs= 10
    batch_size = 2
    input_shape = (16,20)

@ex.capture # if this method is called and some values are not filled, sacred tries to fill them
def get_model(neurons_first_layer, stride_first_layer, neurons_second_layer, optimizer, loss, metrics, input_shape):
    model = Sequential()    
    model.add(Conv1D(neurons_first_layer, stride_first_layer, input_shape=input_shape))
    model.add(LSTM(neurons_second_layer))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer=optimizer,
                  loss=loss,
                  metrics=metrics)

    return model

@ex.capture
def log_performance(_run, logs):
    _run.log_scalar("loss", float(logs.get('loss')))
    _run.log_scalar("accuracy", float(logs.get('acc')))

# class for logging on the end of an epoch
class LogPerformance(Callback):
    def on_batch_end(self, _, logs={}):
        log_performance(logs=logs)

@ex.automain  # Using automain to enable command line integration.
def run(epochs, batch_size, _run):
    # Load the images.
    train_data, train_labels, test_data, test_labels = load_data()

    # additional processing of the data

    # Get the model.
    model = get_model()

    # Train the model.
    model.fit(
      train_data,
      to_categorical(train_labels),
      epochs=epochs,
      batch_size=batch_size,
      callbacks=[LogPerformance()]
    ) 

    return model.evaluate(test_data, to_categorical(test_labels))[1]








