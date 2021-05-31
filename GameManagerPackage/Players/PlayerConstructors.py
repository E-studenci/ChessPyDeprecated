import os
import sys
from functools import partial
from GameManagerPackage.Players.PlayerSelectMoveMethods import *
from GameManagerPackage.Players.Player import Player
import Engine.Evaluation as EvalMethods

from Paths import FOLDER_PATHS

model = available_threads = None
constructors = {}


def initialize_player_constructors():
    os.environ['TF_CPP_MIN_VLOG_LEVEL'] = '3'
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    import tensorflow

    model = tensorflow.keras.models.load_model(f'{FOLDER_PATHS["TrainedModels"]}/convolutional_model_v2-64-2.h5')

    def get_number_of_threads():
        if sys.platform == 'win32':
            return int(os.environ['NUMBER_OF_PROCESSORS'])
        else:
            return int(os.popen('grep -c cores /proc/cpuinfo').read())

    available_threads = get_number_of_threads() - 1

    constructors["human"] = partial(Player, is_bot=False, select_move_method=select_move_human)
    constructors["random_bot"] = partial(Player, is_bot=True, select_move_method=random_move)
    constructors["alpha_beta_handcrafted_bot"] = partial(Player,
                                                         is_bot=True,
                                                         select_move_method=
                                                         partial(evaluated_move,
                                                                 evaluation_method=
                                                                 partial(EvalMethods.alpha_beta,
                                                                         alpha=-10000,
                                                                         beta=10000,
                                                                         depthleft=3,
                                                                         last_moved_piece=-1,
                                                                         eval_function=
                                                                         partial(EvalMethods.evaluate,
                                                                                 PESTO=True,
                                                                                 evaluate_pawns=True),
                                                                         PESTO=True),
                                                                 number_of_processes=available_threads))
    constructors["alpha_beta_neural_bot"] = partial(Player,
                                                    is_bot=True,
                                                    select_move_method=
                                                    partial(evaluated_move,
                                                            evaluation_method=
                                                            partial(EvalMethods.alpha_beta,
                                                                    alpha=-10000,
                                                                    beta=10000,
                                                                    depthleft=0,
                                                                    last_moved_piece=-1,
                                                                    eval_function=
                                                                    partial(EvalMethods.eval_model,
                                                                            model=model),
                                                                    PESTO=True),
                                                            number_of_processes=1))
