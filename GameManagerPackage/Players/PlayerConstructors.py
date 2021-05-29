import os
from functools import partial

import tensorflow

from GameManagerPackage.Players.Player import Player
from GameManagerPackage.Players.PlayerSelectMoveMethods import *
import Engine.Evaluation as eval_methods

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
model = tensorflow.keras.models.load_model('../../Engine/model.h5')

human = partial(Player, is_bot=False, select_move_method=select_move_human)
random_bot = partial(Player, is_bot=True, select_move_method=random_move)
alpha_beta_handcrafted_bot = partial(Player,
                                     is_bot=True,
                                     select_move_method=
                                     partial(evaluated_move,
                                             evaluation_method=
                                             partial(eval_methods.alpha_beta,
                                                     alpha=-10000,
                                                     beta=10000,
                                                     depthleft=3,
                                                     last_moved_piece=-1,
                                                     eval_function=
                                                     partial(eval_methods.evaluate,
                                                             PESTO=True,
                                                             evaluate_pawns=False),
                                                     PESTO=True)))
alpha_beta_neural_bot = partial(Player,
                                is_bot=True,
                                select_move_method=
                                partial(evaluated_move,
                                        evaluation_method=
                                        partial(eval_methods.alpha_beta,
                                                alpha=-10000,
                                                beta=10000,
                                                depthleft=3,
                                                last_moved_piece=-1,
                                                eval_function=
                                                partial(eval_methods.eval_model,
                                                        model=model),
                                                PESTO=True)))
