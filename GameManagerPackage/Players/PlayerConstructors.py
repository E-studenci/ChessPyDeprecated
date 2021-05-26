from functools import partial

import tensorflow

from GameManagerPackage.Players.Bot import Bot
from GameManagerPackage.Players.Human import Human
from GameManagerPackage.Players.PlayerSelectMoveMethods import *
import Engine.Evaluation as eval_methods

# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
model = tensorflow.keras.models.load_model('../../Engine/model.h5')

human = partial(Human, select_move_method=select_move_human)
random_bot = partial(Bot, select_move_method=random_move)
alpha_beta_handcrafted_bot = partial(Bot,
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
                                                     PESTO=True),
                                             number_of_processes=8))
alpha_beta_neural_bot = partial(Bot,
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
                                                        model=1),
                                                PESTO=True),
                                        number_of_processes=8))
