# imports needed for observing an experiment
from sacred import Experiment
from sacred.observers import MongoObserver
from sacred.utils import apply_backspaces_and_linefeeds

# other imports
import numpy as np
from keras.models import Sequential
from keras.metrics import Precision, AUC
from keras.layers import Dense, Flatten
from keras.callbacks import Callback
from keras.optimizers import Adam, SGD
from keras.preprocessing.sequence import TimeseriesGenerator
import keras.backend as K

# importing utility functions
from utilities import load_data, evaluate_test_predictions, custom_precision


# now let us set up the experiment
ex = Experiment('Deep')
# and add the observe to the experiment -> this will store the data in the cloud
ex.observers.append(MongoObserver(url='51.136.77.253:27017', db_name='bankruptcy'))
# prevent that everything that is shown in the console is logged
ex.captured_out_filter = apply_backspaces_and_linefeeds


@ex.config  # Configuration is defined through local variables
def cfg():
    neurons_first_layer = 128
    neurons_second_layer = 64
    neurons_third_layer = 32
    neurons_fourth_layer = 16
    optimizer = 'adam'
    loss = 'binary_crossentropy'
    activation_first_layer = 'tanh'
    activation_second_layer = 'tanh'
    activation_third_layer = 'tanh'
    activation_fourth_layer = 'tanh'
    epochs = 10
    batch_size = 32
    learning_rate = 0.001
    test_ratio = 0.2
    val_ratio = 0.1
    class_ratio = (1.0, 3.0)
    input_shape = (5, 36)


@ex.capture  # if this method is called and some values are not filled, sacred tries to fill them
def get_model(neurons_first_layer, neurons_second_layer, neurons_third_layer, neurons_fourth_layer,
              activation_first_layer, activation_second_layer, activation_third_layer, activation_fourth_layer,
              optimizer, loss, input_shape, learning_rate):
    model = Sequential()
    model.add(Dense(neurons_first_layer, activation=activation_first_layer, input_shape=input_shape))
    model.add(Dense(neurons_second_layer, activation=activation_second_layer))
    model.add(Dense(neurons_third_layer, activation=activation_third_layer))
    model.add(Dense(neurons_fourth_layer, activation=activation_fourth_layer))
    model.add(Flatten())
    model.add(Dense(2, activation='softmax'))

    opti = Adam(lr=learning_rate) if optimizer == 'adam' else SGD(lr=learning_rate)
    model.compile(optimizer=opti, loss=loss, metrics=['accuracy', Precision(), AUC(), custom_precision])

    return model


@ex.capture
def log_performance(_run, logs):
    _run.log_scalar("loss", float(logs.get('loss')))
    _run.log_scalar("accuracy", float(logs.get('accuracy')))
    _run.log_scalar("precision", float(logs.get('precision_1')))
    _run.log_scalar("auc", float(logs.get('auc_1')))


# class for logging at the end of an epoch
class LogPerformance(Callback):
    def on_epoch_end(self, epoch, logs=None):
        log_performance(logs=logs)


@ex.automain  # Using automain to enable command line integration
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
    model.fit_generator(
        train_generator,
        validation_data=val_generator,
        validation_freq=1,
        class_weight={0: class_ratio[0], 1: class_ratio[1]},
        epochs=epochs,
        callbacks=[LogPerformance()]
    ) 

    # Evaluation
    scores = model.evaluate_generator(test_generator)
    print(scores)
    predictions = model.predict_generator(test_generator)
    targets = test_generator.targets[5::5]
    tp, fp, tn, fn, weighted_acc= evaluate_test_predictions(targets, predictions)
    # log test results
    _run.log_scalar('test_tp', tp)
    _run.log_scalar('test_fp', fp)
    _run.log_scalar('test_tn', tn)
    _run.log_scalar('test_fn', fn)
    _run.log_scalar('test_weighted_acc', weighted_acc)

    return weighted_acc
