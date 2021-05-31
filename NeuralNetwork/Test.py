import sys

from tensorflow.keras.models import load_model
from NeuralNetwork.Helpers import get_dataset


def model_test(model_path, dataset_path):
    x_test, y_test = get_dataset(dataset_path)
    model = load_model(model_path)
    model.summary()
    test_loss = model.evaluate(x_test, y_test, verbose=1)
    print('Test accuracy:', test_loss, file=sys.stdout)


def start_testing(model_path, dataset_path):
    model_test(model_path, dataset_path)
