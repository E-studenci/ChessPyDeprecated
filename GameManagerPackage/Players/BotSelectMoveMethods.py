import random

from Chess.Board.Board import Board


def random_move(all_legal_moves):
    start_pos = random.choice(list(all_legal_moves.keys()))
    while not all_legal_moves[start_pos]:
        start_pos = random.choice(list(all_legal_moves.keys()))
    return start_pos, random.choice(all_legal_moves[start_pos])


def alpha_beta(board, all_legal_moves, evaluation_method, *args):
    best_move = (float("inf"), None)
    for piece in all_legal_moves.keys():
        for move in all_legal_moves[piece]:
            board.make_move(piece, move)
            move_value = evaluation_method(board, *args)
            board.unmake_move()
            if move_value < best_move[0]:
                best_move = (move_value, (piece, move))
    return best_move[1]


if __name__ == '__main__':
    board = Board()
    board.initialize_board("r3k2r/pb2qpbp/1pn1pnp1/8/8/2N5/PPPQ1PPP/R3K1NR b kq - 0 1")


    def eval(*unused):
        return random.randint(-1, 1)


    alpha_beta(board, board.calculate_all_legal_moves(), eval, 1123123)
