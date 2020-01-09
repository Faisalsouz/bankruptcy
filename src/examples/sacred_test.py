# imports needed for observing an experiment
from sacred import Experiment
from sacred.observers import MongoObserver
from sacred.utils import apply_backspaces_and_linefeeds

# other imports
import numpy as np
import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical
from keras.callbacks import Callback

# now let us set up the experiment
ex = Experiment('MNIST')
# and add the observe to the experiment -> this will store the data in the cloud
ex.observers.append(MongoObserver(url='51.136.77.253:27017', db_name='dummy_test'))
# prevent that everything that is shown in the console is logged
ex.captured_out_filter = apply_backspaces_and_linefeeds

@ex.config  # Configuration is defined through local variables.
def cfg():
    activation_first_layer = 'relu'
    activation_second_layer = 'relu'
    neurons_first_layer = 64
    neurons_second_layer = 64
    optimizer = 'adam'
    loss = 'categorical_crossentropy'
    metrics = ['accuracy']
    epochs = 5
    batch_size = 32

@ex.capture # if this method is called and some values are not filled, sacred tries to fill them
def get_model(activation_first_layer, activation_second_layer, neurons_first_layer, neurons_second_layer, optimizer, loss, metrics):
    model = Sequential([
        Dense(neurons_first_layer, activation=activation_first_layer, input_shape=(784,)),
        Dense(neurons_second_layer, activation=activation_second_layer),
        Dense(10, activation='softmax'),
    ])
    model.compile(
      optimizer=optimizer,
      loss=loss,
      metrics=metrics,
    )
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
    train_images = mnist.train_images()
    train_labels = mnist.train_labels()
    test_images = mnist.test_images()
    test_labels = mnist.test_labels()

    # Normalize the images.
    train_images = (train_images / 255) - 0.5
    test_images = (test_images / 255) - 0.5

    # Flatten the images.
    train_images = train_images.reshape((-1, 784))
    test_images = test_images.reshape((-1, 784))

    # Get the model.
    model = get_model() # the parameters are automatically injected

    # Train the model.
    model.fit(
      train_images,
      to_categorical(train_labels),
      epochs=epochs,
      batch_size=batch_size,
      callbacks=[LogPerformance()]
    ) 

    return model.evaluate(test_images, to_categorical(test_labels))[1]