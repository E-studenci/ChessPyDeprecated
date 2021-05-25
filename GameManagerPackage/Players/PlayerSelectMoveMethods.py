import random

from Chess.Board.Board import Board


def select_move_human(moves, args):
    """
    :param moves: the legal moves to be put into args[1]
    :param args: (q1,q2) queues for storing moves
    :return: puts [moves] into q2, returns move from q1
    """
    args[1].put(moves)
    move = args[0].get()
    args[0].task_done()
    return move


def random_move(unused, all_legal_moves):
    """
    Finds a random move to make
    :param unused: unused
    :param all_legal_moves: all legal moves for current player
    :return: start_pos, move
    """
    start_pos = random.choice(list(all_legal_moves.keys()))
    while not all_legal_moves[start_pos]:
        start_pos = random.choice(list(all_legal_moves.keys()))
    return start_pos, random.choice(all_legal_moves[start_pos])


def evaluated_move(board, all_legal_moves, evaluation_method):
    """
    checks every possible move and selects the best one
    :param board: the board on which the game is played
    :param all_legal_moves: all legal moves for current player
    :param evaluation_method: method used to evaluate the board
    :return: start_pos, move
    """
    best_move = (float("inf"), None)
    for piece in all_legal_moves.keys():
        for move in all_legal_moves[piece]:
            board.make_move(piece, move)
            move_value = evaluation_method(board)
            board.unmake_move()
            if move_value < best_move[0]:
                best_move = (move_value, (piece, move))
    return best_move[1]
