from functools import partial

from GameManagerPackage.Players.Bot import Bot
from GameManagerPackage.Players.Human import Human
from GameManagerPackage.Players.PlayerSelectMoveMethods import *
import Engine.Evaluation as eval_methods

human = partial(Human, select_move_method=select_move_human)
random_bot = partial(Bot, select_move_method=random_move)
alpha_beta_handcrafted_bot = partial(Bot,
                                     select_move_method=
                                     partial(evaluated_move,
                                             evaluation_method=
                                             partial(eval_methods.evaluated_move,
                                                     alpha=-10000,
                                                     beta=10000,
                                                     depth_left=3,
                                                     last_moved_piece=-1,
                                                     eval_function=
                                                     partial(eval_methods.evaluate,
                                                             PESTO=True,
                                                             evaluate_pawns=True))))
