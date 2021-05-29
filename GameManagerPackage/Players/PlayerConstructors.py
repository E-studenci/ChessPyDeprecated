import os
import sys
from functools import partial

import tensorflow

from GameManagerPackage.Players.Player import Player
from GameManagerPackage.Players.PlayerSelectMoveMethods import *
import Engine.Evaluation as EvalMethods


def get_number_of_threads():
    if sys.platform == 'win32':
        return int(os.environ['NUMBER_OF_PROCESSORS'])
    else:
        return int(os.popen('grep -c cores /proc/cpuinfo').read())


available_threads = get_number_of_threads() - 1
# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
model = tensorflow.keras.models.load_model('../../Engine/model.h5')

human = partial(Player, is_bot=False, select_move_method=select_move_human)
random_bot = partial(Player, is_bot=True, select_move_method=random_move)
alpha_beta_handcrafted_bot = partial(Player,
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
                                                             evaluate_pawns=False),
                                                     PESTO=True),
                                             number_of_processes=available_threads))
alpha_beta_neural_bot = partial(Player,
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
                                                partial(EvalMethods.eval_model,
                                                        model=1),
                                                PESTO=True),
                                        number_of_processes=available_threads))
