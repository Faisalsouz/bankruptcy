# imports needed for observing an experiment
from sacred import Experiment
from sacred.observers import MongoObserver
from sacred.utils import apply_backspaces_and_linefeeds

# other imports
import os
import pickle
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Flatten, Dense
from keras.callbacks import Callback
from keras.optimizers import Adam, SGD, Adagrad, Adadelta, RMSprop, Nadam, Adamax
from keras.metrics import Precision, AUC
from keras.preprocessing.sequence import TimeseriesGenerator

# importing utility functions
from utilities import *

np.random.seed(0)
# now let us set up the experiment
ex = Experiment('LSTM')
# and add the observe to the experiment -> this will store the data in the cloud
ex.observers.append(MongoObserver(url='51.136.77.253:27017', db_name='bankruptcy'))
# prevent that everything that is shown in the console is logged
ex.captured_out_filter = apply_backspaces_and_linefeeds


@ex.config  # Configuration is defined through local variables.
def cfg():
    units = 256
    optimizer = 'nadam'
    loss = 'binary_crossentropy'  # mean_squared_error
    activation = 'tanh'
    recurrent_activation = 'tanh'  # sigmoid
    kernel_initializer = 'lecun_uniform' # glorot_uniform
    recurrent_initializer = 'orthogonal' # orthogonal
    # dropout = 0.05
    epochs = 200
    batch_size = 64
    learning_rate = 0.0001
    test_ratio = 0.2
    val_ratio = 0.1
    class_ratio = (1.0, 3.5)
    input_shape = (5, 36)


@ex.capture  # if this method is called and some values are not filled, sacred tries to fill them
def get_model(units, optimizer, loss, activation, learning_rate, input_shape, kernel_initializer, recurrent_initializer, recurrent_activation):
    model = Sequential()    
    model.add(LSTM(units, 
        input_shape=input_shape, 
        activation=activation, recurrent_activation=recurrent_activation, 
        kernel_initializer=kernel_initializer, recurrent_initializer = recurrent_initializer,
        # dropout=dropout,
        return_sequences=True))
    model.add(Flatten())
    model.add(Dense(2, activation='softmax'))

    if optimizer == 'sgd' or optimizer == 'SGD':
        opti = SGD(lr=learning_rate)
    elif optimizer == 'rmsprop' or optimizer == 'RMSprop':
        opti = RMSprop(lr=learning_rate)
    elif optimizer == 'adam' or optimizer == 'Adam':
        opti = Adam(lr=learning_rate)
    elif optimizer == 'adagrad' or optimizer == 'Adagrad':
        opti = Adagrad(lr=learning_rate)
    elif optimizer == 'adadelta' or optimizer == 'Adadelta':
        opti = Adadelta(lr=learning_rate)
    elif optimizer == 'nadam' or optimizer == 'Nadam':
        opti = Nadam(lr=learning_rate, beta_1=0.9, beta_2=0.999)  # beta_1=0.9, beta_2=0.999
    elif optimizer == 'adamax' or optimizer == 'Adamax':
        opti = Adamax(lr=learning_rate, beta_1=0.9, beta_2=0.999)  # beta_1=0.9, beta_2=0.999

    model.compile(optimizer=opti,
                  loss=loss,
                  metrics=['accuracy', AUC(), custom_precision])

    return model


@ex.capture
def log_performance(_run, logs):
    _run.log_scalar("loss", float(logs.get('loss')))
    _run.log_scalar("accuracy", float(logs.get('accuracy')))
    _run.log_scalar("precision", float(logs.get('precision_1')))
    _run.log_scalar("auc", float(logs.get('auc_1')))


# class for logging on the end of an epoch
class LogPerformance(Callback):
    def on_epoch_end(self, epoch, logs=None):
        log_performance(logs=logs)


@ex.automain  # Using automain to enable command line integration.
def run(epochs, input_shape, batch_size, test_ratio, val_ratio, class_ratio, _run):

    # Load the data
    data_path = os.getcwd() + '/../../data/Data{}_{}.pickle'.format(int(test_ratio*100), int(val_ratio*100))

    if not os.path.isfile(data_path):
        print('Loading data.. ')                                                                       
        load_data(test_ratio=test_ratio, val_ratio=val_ratio)     
    train_data, train_labels, test_data, test_labels, val_data, val_labels = pickle.load(open(data_path, 'rb'))   
    
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
      validation_data=test_generator,
      validation_freq=1,
      class_weight={0: class_ratio[0], 1: class_ratio[1]},
      epochs=epochs,
      callbacks=[LogPerformance()],
      verbose = 2
    )

    predictions = model.predict_generator(test_generator)
    targets = test_generator.targets[5::5]

    # calculate confusion matrix values and the weighted accuracy
    tp, fp, tn, fn, weighted_acc = evaluate_test_predictions(targets, predictions)


    return weighted_acc









