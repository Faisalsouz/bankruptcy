# imports needed for observing an experiment
from sacred import Experiment
from sacred.observers import MongoObserver
from sacred.utils import apply_backspaces_and_linefeeds

# other imports
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.callbacks import Callback
from keras.metrics import Precision, AUC
from keras.preprocessing.sequence import TimeseriesGenerator

# importing utility functions
from utilities import load_data

# now let us set up the experiment
ex = Experiment('Standard')
# and add the observe to the experiment -> this will store the data in the cloud
ex.observers.append(MongoObserver(url='51.136.77.253:27017', db_name='bankruptcy'))
# prevent that everything that is shown in the console is logged
ex.captured_out_filter = apply_backspaces_and_linefeeds


@ex.config  # Configuration is defined through local variables.
def cfg():
    neurons_first_layer = 16
    optimizer = 'adam'
    loss = 'binary_crossentropy'
    activation = 'sigmoid'
    epochs = 10
    batch_size = 32
    test_ratio = 0.2
    # TODO: remove from config?
    input_shape = (5, 36)


@ex.capture # if this method is called and some values are not filled, sacred tries to fill them
def get_model(neurons_first_layer, optimizer, loss, activation, input_shape):
    model = Sequential()
    model.add(Dense(neurons_first_layer, input_shape=input_shape))
    model.add(Flatten())
    model.add(Dense(1, activation=activation))
    model.compile(
      optimizer=optimizer,
      loss=loss,
      metrics=['accuracy', Precision(), AUC()],
    )
    return model


@ex.capture
def log_performance(_run, logs):
    _run.log_scalar("loss", float(logs.get('loss')))
    _run.log_scalar("accuracy", float(logs.get('accuracy')))
    _run.log_scalar("precision", float(logs.get('precision_1')))
    _run.log_scalar("auc", float(logs.get('auc_1')))


# class for logging on the end of an epoch
class LogPerformance(Callback):
    def on_batch_end(self, _, logs=None):
        log_performance(logs=logs)


@ex.automain  # Using automain to enable command line integration.
def run(epochs, input_shape, batch_size, test_ratio, _run):
    # Load the data
    train_data, train_labels, test_data, test_labels = load_data(test_ratio=test_ratio)

    prediction_horizon = input_shape[0]

    # create time series generators
    train_generator = TimeseriesGenerator(train_data, train_labels, length=prediction_horizon, batch_size=batch_size,
                                          stride=prediction_horizon+1)
    test_generator = TimeseriesGenerator(test_data, test_labels, length=prediction_horizon, stride=prediction_horizon+1)

    # Get the model
    model = get_model()

    # Train the model
    model.fit_generator(
      train_generator,
      epochs=epochs,
      callbacks=[LogPerformance()]
    ) 

    return model.evaluate_generator(test_generator)[1]
