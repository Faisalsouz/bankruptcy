

# imports needed for observing an experiment
from sacred import Experiment
from sacred.observers import MongoObserver
from sacred.utils import apply_backspaces_and_linefeeds

# other imports
import numpy as np
import keras
import matplotlib.pyplot as plt
from keras.models import Sequential
from sklearn.metrics import confusion_matrix
from keras.layers import *
from keras.optimizers import Adam
from keras.callbacks import Callback
from keras.preprocessing.sequence import TimeseriesGenerator

# importing utility functions
from utilities import load_data

# now let us set up the experiment
ex = Experiment('LSTM')
# and add the observe to the experiment -> this will store the data in the cloud
ex.observers.append(MongoObserver(url='51.136.77.253:27017', db_name='bankruptcy'))
# prevent that everything that is shown in the console is logged
ex.captured_out_filter = apply_backspaces_and_linefeeds

PREDICTION_HORIZON = 5

@ex.config  # Configuration is defined through local variables.
def cfg():
    units = 16
    optimizer = 'adam'
    loss = keras.losses.binary_crossentropy
    metrics = ['accuracy']
    epochs= 10
    batch_size = 32
    input_shape = (5,36)


@ex.capture # if this method is called and some values are not filled, sacred tries to fill them
def get_model(units, optimizer, loss, metrics, input_shape):
    model = Sequential()    
    model.add(LSTM(units, input_shape=input_shape, return_sequences=True))
    model.add(Flatten())
    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer=optimizer,
                  loss=loss,
                  metrics=metrics)

    return model


@ex.capture
def log_performance(_run, logs):
    _run.log_scalar("loss", float(logs.get('loss')))
    _run.log_scalar("accuracy", float(logs.get('accuracy')))


# class for logging on the end of an epoch
class LogPerformance(Callback):
    def on_batch_end(self, _, logs={}):
        log_performance(logs=logs)


@ex.automain  # Using automain to enable command line integration.
def run(epochs, batch_size, _run):
    # Load the data.
    train_data, train_labels, test_data, test_labels = load_data('../../data/NO_SHUFFLE.csv', 0.33)

    # additional processing of the data

    # create time series generators
    train_generator = TimeseriesGenerator(train_data, train_labels, length=PREDICTION_HORIZON, batch_size=batch_size, stride=PREDICTION_HORIZON+1)
    test_generator = TimeseriesGenerator(test_data, test_labels, length=PREDICTION_HORIZON, stride=PREDICTION_HORIZON+1)

    # Get the model.
    model = get_model()

    # Train the model.
    model.fit_generator(
      train_generator,
      epochs=epochs,
      callbacks=[LogPerformance()]
    ) 

    return model.evaluate_generator(test_generator)[1]








