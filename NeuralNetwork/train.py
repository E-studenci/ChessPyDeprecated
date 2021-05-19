import numpy
import tensorflow.keras.optimizers as optimizers
import tensorflow.keras.callbacks as callbacks
import tensorflow.keras.utils as utils
from NeuralNetwork.models import *


def get_dataset():
    container = numpy.load('Data/dataset.npz')
    x, v = container['b'], container['v']
    v = numpy.asarray(v / abs(v).max() / 2 + 0.5, dtype=numpy.float32)  # normalization (0 - 1)
    return x, v


def train(picked_model, model_name, optimizer, loss, ):
    model = picked_model
    # utils.plot_model(model, to_file='model_plot.png', show_shapes=True, show_layer_names=False)

    x_train, y_train = get_dataset()
    print(x_train.shape)
    print(y_train.shape)
    model.compile(optimizer=optimizer, loss=loss)
    model.summary()
    model.fit(x_train, y_train,
              batch_size=2048,
              epochs=1000,
              verbose=1,
              validation_split=0.1,
              callbacks=[callbacks.ReduceLROnPlateau(monitor='loss', patience=10),
                         callbacks.EarlyStopping(monitor='loss', patience=15, min_delta=1e-4)])

    model.save(f'{model_name}.h5')


if __name__ == '__main__':
    train(build_model_residual(32, 4), 'new_model', optimizers.Adam(5e-4), 'mean_squared_error')
