from Chess.Board.Board import Board
from Chess.Pieces.Bishop import Bishop
from Chess.Pieces.King import King
from Chess.Pieces.Knight import Knight
from Chess.Pieces.Pawn import Pawn
from Chess.Pieces.Queen import Queen
from Chess.Pieces.Rook import Rook
from SquareTables import *

PIECE_DICTIONARY = {Pawn:   ["p", "P"],
                    Bishop: ["b", "B"],
                    Knight: ["n", "N"],
                    Rook:   ["r", "R"],
                    Queen:  ["q", "Q"],
                    King:   ["k", "K"]}

ENDGAME_PIECES = 4
PIECE_POINT_VALUE = 0.01
MOBILITY_VALUE = 0.1
DOUBLED_BLOCKED_ISOLATED_PAWNS_VALUE = 0.5

POINT_DICTIONARY = {"p": (([100] * 2, [PAWN_SQUARE_TABLE] * 2),
                          ((82, 94), [PAWN_SQUARE_TABLE_MID_GAME_PASTA, PAWN_SQUARE_TABLE_END_GAME_PASTA])),
                    "n": (([320] * 2, [KNIGHT_SQUARE_TABLE] * 2),
                          ((337, 281), [KNIGHT_SQUARE_TABLE_MID_GAME_PASTA, KNIGHT_SQUARE_TABLE_END_GAME_PASTA])),
                    "b": (([330] * 2, [BISHOP_SQUARE_TABLE] * 2),
                          ((365, 297), [BISHOP_SQUARE_TABLE_MID_GAME_PASTA, BISHOP_SQUARE_TABLE_END_GAME_PASTA])),
                    "r": (([500] * 2, [ROOK_SQUARE_TABLE] * 2),
                          ((477, 512), [ROOK_SQUARE_TABLE_MID_GAME_PASTA, ROOK_SQUARE_TABLE_END_GAME_PASTA])),
                    "q": (([900] * 2, [QUEEN_SQUARE_TABLE] * 2),
                          ((1025, 936), [QUEEN_SQUARE_TABLE_MID_GAME_PASTA, QUEEN_SQUARE_TABLE_END_GAME_PASTA])),
                    "k": (([20000] * 2, [KING_SQUARE_TABLE_MIDDLE_GAME, KING_SQUARE_TABLE_END_GAME]),
                          ((20000, 20000), [KING_SQUARE_TABLE_MID_GAME_PASTA, KING_SQUARE_TABLE_END_GAME_PASTA]))}


def evaluate(board, current_turn, PASTA=False):
    string_board = convert_board_to_string_board(board.board)
    endgame = is_endgame(string_board)
    score = PIECE_POINT_VALUE * evaluate_material(string_board, current_turn, endgame, PASTA)
    score += PIECE_POINT_VALUE * evaluate_piece_positions(string_board, current_turn, endgame, PASTA)

    score -= DOUBLED_BLOCKED_ISOLATED_PAWNS_VALUE * count_doubled_pawns(string_board, current_turn)
    score -= DOUBLED_BLOCKED_ISOLATED_PAWNS_VALUE * count_isolated_pawns(string_board, current_turn)
    score -= DOUBLED_BLOCKED_ISOLATED_PAWNS_VALUE * count_blocked_pawns(string_board, current_turn)

    score += MOBILITY_VALUE * evaluate_mobility(board)

    return score


def convert_board_to_string_board(board):
    ret_board = {}
    for piece in board:
        if piece is not None:
            ret_board[piece.position] = PIECE_DICTIONARY[type(piece)][piece.color]
    return ret_board


def is_endgame(board):
    minor_pieces = 0
    for position in board.keys():
        if board[position] in ["b", "B", "n", "N", "r", "R", "q", "Q"]:
            minor_pieces += 1
    return minor_pieces <= ENDGAME_PIECES


def evaluate_material(board, current_turn, endgame, PASTA):
    score_current = 0
    score_opposite = 0
    for position in board.keys():
        piece_points = POINT_DICTIONARY[board[position].lower()][[0, 1][PASTA]][0][[0, 1][endgame]]
        if (current_turn and board[position].isupper()) or (not current_turn and board[position].islower()):
            score_current += piece_points
        else:
            score_opposite += piece_points
    return score_current - score_opposite


def evaluate_piece_positions(board, current_turn, endgame, PASTA):
    score = 0
    for position in board.keys():
        multiplier = [-1, 1][(current_turn and board[position].isupper()) or
                             (not current_turn and board[position].islower())]
        position_points_table = POINT_DICTIONARY[board[position].lower()][[0, 1][PASTA]][1][[0, 1][endgame]]
        score += multiplier * position_points_table[-multiplier * position]
    return score


def evaluate_mobility(board):
    score = count_moves(board.calculate_all_legal_moves())
    board.turn = not board.turn
    score -= count_moves(board.calculate_all_legal_moves())
    board.turn = not board.turn
    return score


def count_moves(moves):
    count = 0
    for move_list in moves.values():
        count += len(move_list)
    return count


def count_doubled_pawns(board, current_turn):
    score = 0
    dict_opposite = {}
    dict_current = {}
    for i in range(8):
        dict_opposite[i] = 0
        dict_current[i] = 0
    columns = [dict_opposite, dict_current]
    for position in board.keys():
        if board[position] in ["p", "P"]:
            columns[[0, 1][board[position].isupper() == current_turn]][position % 8] += 1

    for count_opposite, count_current in zip(dict_opposite.values(), dict_current.values()):
        score += count_current if count_current > 1 else 0
        score -= count_opposite if count_opposite > 1 else 0
    return score


def count_isolated_pawns(board, current_turn):
    score = 0
    skip = []
    for position in board.keys():
        if board[position] in ["p", "P"]:
            if position not in skip:
                surrounding_pawns_count = 0
                for direction in [-1, 7, 8, 9, 1, -7, -8, -9]:
                    if (position + direction) in board.keys() and board[position + direction] == board[position]:
                        skip.append(position + direction)
                        surrounding_pawns_count += 1
                if surrounding_pawns_count == 0:
                    multiplier = [-1, 1][(current_turn and board[position].isupper()) or
                                         (not current_turn and board[position].islower())]
                    score += multiplier
    return score


def count_blocked_pawns(board, current_turn):
    score = 0
    for position in board.keys():
        if board[position] in ["p", "P"]:
            if (position + 8 * [-1, 1][board[position].isupper()]) in board.keys():
                score += [-1, 1][(current_turn and board[position].isupper()) or
                                 (not current_turn and board[position].islower())]
    return score


if __name__ == '__main__':
    board = Board()
    board.initialize_board("r6r/pppppppp/8/8/8/8/PPPPPPPP/R6R w - - 0 1")
    temp = convert_board_to_string_board(board.board)
    print(evaluate(board, board.turn, False))
