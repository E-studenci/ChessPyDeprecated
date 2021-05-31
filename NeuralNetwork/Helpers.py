import numpy
from NeuralNetwork.Models import *
import tensorflow.keras.optimizers as optimizers
import tensorflow.keras.losses as losses

HELP_FLAG = '-h'
HELP_FULL = '--help'
VALIDATE_FLAG = '-v'
VALIDATE_FULL = '--validate'
TRAIN_FLAG = '-t'
TRAIN_FULL = '--train'
DATA_FLAG = '-d'
DATA_FULL = '--data'

HELP_MESSAGE = "Usage: network.exe [MODE]...\n" \
               "                            \n" \
               "    parameter(value) <- optional parameter, the value in bracket is the default value\n" \
               "                            \n" \
               "    1. network.exe [-h/--help]\n" \
               "       Shows help message.\n" \
               "                            \n" \
               "    2. network.exe [-d/--data] [parameters]\n" \
               "       Parses fen dataset into acceptable type of data for neural network to train on.\n" \
               "       Parameters:\n" \
               "        raw_dataset_path - fen dataset that will be parsed into acceptable type\n" \
               "        final_dataset_save_path - path where the final dataset will be saved\n" \
               "        starting_point(0) - at which line the process of parsing should start\n" \
               "        ending_point(100000) - at which line the process of parsing should end\n" \
               "        evaluation_depth(10) - the depth at witch boards should be evaluated\n" \
               "                                                \n" \
               "    3. network.exe [-t/--train] [parameters]\n" \
               "       Trains model with a given dataset.\n" \
               "       Parameters:\n" \
               "        model_type - type of the model you want to train.\n" \
               "            - convolutional\n" \
               "            - residual\n" \
               "        layer_size - layer size\n" \
               "        number_of_layers - amount of hidden layers you want to have.\n" \
               "        finished_model_save_path - path where the trained model should be saved\n" \
               "        optimizer - the type of the optimizer the model will be optimized by\n" \
               "            - Adams\n" \
               "            - SGD\n" \
               "        learning_rate - length of the training step\n" \
               "        loss_function - the type of function, that will calculate the loss of each comparision\n" \
               "            - mean_square_error\n" \
               "            - mean_absolute_error\n" \
               "        dataset_path - path of a dataset that will be used to train the model\n" \
               "                                                                               \n" \
               "    4. network.exe [-v/--validate] [parameters]\n" \
               "       Tests model to anticipate how good it is.\n" \
               "       Parameters:\n" \
               "        model_path - path where the tested model is stored\n" \
               "        dataset_path - path where the validation data is stored\n"


MODELS = {'convolutional': build_model, 'residual': build_model_residual}
OPTIMIZERS = {'Adams': optimizers.Adam, 'SGD': optimizers.SGD}
LOSSES = {'mean_square_error': losses.mean_squared_error, 'mean_absolute_error': losses.mean_absolute_error}


def get_dataset(dataset_name):
    container = numpy.load(dataset_name)
    x, y = container['x'], container['y']
    y = numpy.asarray(y / abs(y).max() / 2 + 0.5, dtype=numpy.float32)  # normalization (0 - 1)
    import multiprocessing
    multiprocessing.current_process()
    return x, y
