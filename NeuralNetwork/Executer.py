from NeuralNetwork.Helpers import *
from NeuralNetwork.DataMaker import start_making_data
from NeuralNetwork.Train import start_training
from NeuralNetwork.Test import start_testing
import sys


def _help_check(parameters):
    if HELP_FLAG == parameters[0] or HELP_FULL == parameters[0]:
        print(HELP_MESSAGE)
        return True
    return False


def _data_check(parameters):
    if DATA_FLAG == parameters[0] or DATA_FULL == parameters[0]:
        start_making_data(*parameters[1:])
        return True
    return False


def _train_check(parameters):
    if TRAIN_FLAG == parameters[0] or TRAIN_FULL == parameters[0]:
        if len(parameters) != 9:
            return False
        start_training(MODELS[parameters[1]](int(parameters[2]), int(parameters[3])),
                       parameters[4],
                       OPTIMIZERS[parameters[5]](float(parameters[6])),
                       LOSSES[parameters[7]],
                       parameters[8])
        return True
    return False


def _test_check(parameters):
    if VALIDATE_FLAG == parameters[0] or VALIDATE_FULL == parameters[0]:
        if len(parameters) != 3:
            return False
        start_testing(*parameters[1:])
        return True
    return False


def main(parameters):
    if len(parameters) == 0:
        print('No parameters.')
        return 0
    if _help_check(parameters):
        return 0
    if _data_check(parameters):
        return 0
    if _train_check(parameters):
        return 0
    if _test_check(parameters):
        return 0
    return -1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
