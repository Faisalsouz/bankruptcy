# imports needed for observing an experiment
from sacred import Experiment
from sacred.observers import MongoObserver
from sacred.utils import apply_backspaces_and_linefeeds

# other imports
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.callbacks import Callback
from keras.optimizers import Adam, SGD
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
    activation = 'linear'
    epochs = 3
    batch_size = 32
    learning_rate = 0.1
    test_ratio = 0.2
    val_ratio = 0.1
    class_ratio = (1.0, 2.0)
    input_shape = (5, 36)


@ex.capture  # if this method is called and some values are not filled, sacred tries to fill them
def get_model(neurons_first_layer, optimizer, loss, activation, learning_rate, input_shape):
    model = Sequential()
    model.add(Dense(neurons_first_layer, activation=activation, input_shape=input_shape))
    model.add(Flatten())
    model.add(Dense(1, activation='softmax'))

    opti = Adam(lr=learning_rate) if optimizer == 'adam' else SGD(lr=learning_rate)
    model.compile(
      optimizer=opti,
      loss=loss,
      metrics=['accuracy', Precision(), AUC()])

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
def run(epochs, input_shape, batch_size, test_ratio, val_ratio, class_ratio, _run):
    # Load the data
    train_data, train_labels, test_data, test_labels, val_data, val_labels = load_data(test_ratio=test_ratio,
                                                                                       val_ratio=val_ratio)
    prediction_horizon = input_shape[0]

    # create time series generators
    train_generator = TimeseriesGenerator(train_data, train_labels, length=prediction_horizon, batch_size=batch_size, stride=prediction_horizon)
    test_generator = TimeseriesGenerator(test_data, test_labels, length=prediction_horizon, stride=prediction_horizon)
    val_generator = TimeseriesGenerator(val_data, val_labels, length=prediction_horizon, stride=prediction_horizon)

    # Get the model
    model = get_model()

    # Train the model
    # validation_freq: validate against test generator every validation_freq epoch
    # class_weight: fight imbalance by telling model to take care of under-represented classes
    # e.g. this means model should treat class 1 as 50x more 'important' as class 0
    # this effects the loss function and hence becomes weighted
    model.fit_generator(
        train_generator,
        validation_data=test_generator,
        validation_freq=1,
        class_weight={0: class_ratio[0], 1: class_ratio[1]},
        epochs=epochs,
        callbacks=[LogPerformance()]
    )

    # make predictions (returns array)
    predictions = model.predict_generator(val_generator).astype(int)

    print("\nExample predictions in the form of Ground-Truth => Prediction")
    for i in range(10):
        # TODO: maybe something like this (see TODO below for possible reason)?
        # print('{} => {}'.format(val_generator.targets[i*5:i*5+5], predictions[i]))
        print('{} => {}'.format(val_generator.targets[i], predictions[i]))

    # TODO: unequal length, probably because of sequences of 5 yield one (the final) prediction
    # len(targets) = 2890, len(predictions) = 481
    # how to check for correctness?
    # np.equal returns boolean array
    e = np.equal(val_generator.targets, predictions)
    # return percentage of correctness
    # if everything was predicted correctly, this should return 1
    # TODO: len(e) = 481, np.sum(e) > 28000. WHY??
    return np.sum(e) / len(predictions)

