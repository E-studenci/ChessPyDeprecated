import tensorflow.keras.callbacks as callbacks
from NeuralNetwork.Helpers import get_dataset


def train(model, model_save_path, optimizer, loss, dataset_name):
    x_train, y_train = get_dataset(dataset_name)
    model.compile(optimizer=optimizer, loss=loss)
    model.summary()
    model.fit(x_train, y_train,
              batch_size=2048,
              epochs=1000,
              verbose=1,
              validation_split=0.1,
              callbacks=[callbacks.ReduceLROnPlateau(monitor='loss', patience=10),
                         callbacks.EarlyStopping(monitor='loss', patience=10, min_delta=1e-5)])

    model.save(f'{model_save_path}.h5')


def start_training(model, model_save_path, optimizer, loss_method, dataset_path):
    train(model, model_save_path, optimizer, loss_method, dataset_path)
