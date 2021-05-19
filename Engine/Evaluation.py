from Chess.Board.Board import Board
from Chess.Pieces.Bishop import Bishop
from Chess.Pieces.King import King
from Chess.Pieces.Knight import Knight
from Chess.Pieces.Pawn import Pawn
from Chess.Pieces.Queen import Queen
from Chess.Pieces.Rook import Rook
from SquareTables import *

PIECE_DICTIONARY = {Pawn:   ["bp", "wp"],
                    Bishop: ["bb", "wb"],
                    Knight: ["bn", "wn"],
                    Rook:   ["br", "wr"],
                    Queen:  ["bq", "wq"],
                    King:   ["bk", "wk"]}

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
                    "k": (([0] * 2, [KING_SQUARE_TABLE_MIDDLE_GAME, KING_SQUARE_TABLE_END_GAME]),
                          ((0, 0), [KING_SQUARE_TABLE_MID_GAME_PASTA, KING_SQUARE_TABLE_END_GAME_PASTA]))}

POINT_DICTIONARY_TYPES = {Pawn:   (([100] * 2, [PAWN_SQUARE_TABLE] * 2),
                                   ((82, 94), [PAWN_SQUARE_TABLE_MID_GAME_PASTA, PAWN_SQUARE_TABLE_END_GAME_PASTA])),
                          Knight: (([320] * 2, [KNIGHT_SQUARE_TABLE] * 2),
                                   ((337, 281),
                                    [KNIGHT_SQUARE_TABLE_MID_GAME_PASTA, KNIGHT_SQUARE_TABLE_END_GAME_PASTA])),
                          Bishop: (([330] * 2, [BISHOP_SQUARE_TABLE] * 2),
                                   ((365, 297),
                                    [BISHOP_SQUARE_TABLE_MID_GAME_PASTA, BISHOP_SQUARE_TABLE_END_GAME_PASTA])),
                          Rook:   (([500] * 2, [ROOK_SQUARE_TABLE] * 2),
                                   ((477, 512), [ROOK_SQUARE_TABLE_MID_GAME_PASTA, ROOK_SQUARE_TABLE_END_GAME_PASTA])),
                          Queen:  (([900] * 2, [QUEEN_SQUARE_TABLE] * 2),
                                   ((1025, 936),
                                    [QUEEN_SQUARE_TABLE_MID_GAME_PASTA, QUEEN_SQUARE_TABLE_END_GAME_PASTA])),
                          King:   (([0] * 2, [KING_SQUARE_TABLE_MIDDLE_GAME, KING_SQUARE_TABLE_END_GAME]),
                                   ((0, 0), [KING_SQUARE_TABLE_MID_GAME_PASTA, KING_SQUARE_TABLE_END_GAME_PASTA]))}


def evaluate(board, all_legal_moves, PESTO=True, evaluate_pawns=False):
    if moves_count(all_legal_moves) == 0:
        if board.king_pos[board.turn] in board.attacked_fields:
            return -20000
        else:
            return 0

    string_board = convert_board_to_string_board(board.board)
    endgame = is_endgame(string_board)
    score, doubled_pawns, isolated_pawns, blocked_pawns = eval_white_black(string_board, endgame, PESTO, evaluate_pawns)
    score = PIECE_POINT_VALUE * score
    score -= DOUBLED_BLOCKED_ISOLATED_PAWNS_VALUE * (doubled_pawns + isolated_pawns + blocked_pawns)

    return score * [-1, 1][board.turn]


def moves_count(legal_moves):
    ret = 0
    for piece in legal_moves:
        ret += len(legal_moves[piece])
    return ret


def convert_board_to_string_board(board):
    ret_board = {}
    for piece in board:
        if piece is not None:
            ret_board[piece.position] = PIECE_DICTIONARY[type(piece)][piece.color]
    return ret_board


def is_endgame(board):
    minor_pieces = 0
    for position in board.keys():
        if board[position][1] in ["b", "n", "r", "q"]:
            minor_pieces += 1
    return minor_pieces <= ENDGAME_PIECES


def is_endgame_2(board):
    minor_pieces = 0
    for piece in board.board:
        if piece is not None:
            if type(piece) in [Pawn, Knight, Rook, Queen]:
                minor_pieces += 1
    return minor_pieces <= ENDGAME_PIECES


def piece_value(point_dictionary, piece, endgame, PESTO, color, position):
    piece_lists = point_dictionary[piece[1]][[0, 1][PESTO]]
    endgame_index = [0, 1][endgame]
    relative_piece_position_index = [1, -1][color] * position + [0, -1][color]
    piece_value = piece_lists[0][endgame_index]
    position_value = piece_lists[1][endgame_index][relative_piece_position_index]
    return piece_value + position_value


def eval_white_black(board, endgame=False, PESTO=True, evaluate_pawns=False):
    score = [0] * 2
    doubled_pawns = [0] * 2
    isolated_pawns = [0] * 2
    blocked_pawns = [0] * 2
    columns = [[0] * 8, [0] * 8]
    for position in board.keys():
        piece = board[position]
        piece_color = piece[0] == "w"
        score[piece_color] += piece_value(POINT_DICTIONARY, piece, endgame, PESTO, piece_color, position)
        if evaluate_pawns:
            if piece[1] == 'p':
                # count doubled pawns
                columns[piece_color][position % 8] += 1
                # count blocked pawns
                if position + 8 * [-1, 1][piece_color] in board:
                    blocked_pawns[piece_color] += 1
                # count isolated pawns
                surrounding_pawns = False
                for direction in [-1, 7, 8, 9, 1, -7, -8, -9]:
                    if (position + direction) in board and board[position + direction] == board[position]:
                        surrounding_pawns = True
                if not surrounding_pawns:
                    isolated_pawns[piece_color] += 1
    for count_black, count_white in zip(columns[0], columns[1]):
        doubled_pawns[0] += [0, count_black][count_black > 1]
        doubled_pawns[1] += [0, count_white][count_white > 1]
    return score[1] - score[0], \
           doubled_pawns[1] - doubled_pawns[0], \
           isolated_pawns[1] - isolated_pawns[0], \
           blocked_pawns[1] - blocked_pawns[0]


# _________________________ALPHA-BETA-PRUNING____________________________


def move_value(board, start, move, endgame, PESTO, last_moved_piece):
    if move[1] != 0:
        return float('inf')
    piece_moved = board.board[start]
    before_value = piece_value(POINT_DICTIONARY_TYPES, (0, type(piece_moved)), endgame, PESTO,
                               [-1, 1][board.turn], start)
    after_value = piece_value(POINT_DICTIONARY_TYPES, (0, type(piece_moved)), endgame, PESTO,
                              [-1, 1][board.turn], move[0])
    position_change = after_value - before_value

    capture_value = 0
    if board.board[move[0]] is not None:
        captured_piece_value = piece_value(POINT_DICTIONARY_TYPES, (0, type(board.board[move[0]])), endgame, PESTO,
                                           [-1, 1][not board.turn], move[0])
        capture_value += [0, 1000][move[0] == last_moved_piece]
        capture_value += captured_piece_value - before_value

    return capture_value + position_change


def convert_moves_to_list(moves):
    ret = []
    for piece in moves:
        for move in moves[piece]:
            ret.append((piece, move))
    return ret


def order_moves(board, legal_moves, PESTO, endgame, last_moved_piece, reverse):
    moves = convert_moves_to_list(legal_moves)

    def move_order(move):
        return move_value(board, move[0], move[1], endgame, PESTO, last_moved_piece)

    sorted_moves = sorted(moves, key=move_order, reverse=reverse)

    return sorted_moves


def alpha_beta(board, alpha, beta, depthleft, PESTO, last_moved_piece, eval_funtion, evaluate_pawns=False):
    all_legal_moves = board.calculate_all_legal_moves()
    bestscore = float("-inf")
    if depthleft <= 0:
        return eval_funtion(board, all_legal_moves, PESTO, evaluate_pawns)
    endgame = is_endgame_2(board)
    current_all_legal_moves = order_moves(board, all_legal_moves,
                                          PESTO, endgame, last_moved_piece, True)
    for move in current_all_legal_moves:
        board.make_move(move[0], move[1])
        score = -alpha_beta(board, -beta, -alpha, depthleft - 1, PESTO, move[1][0], eval_funtion, evaluate_pawns)
        board.unmake_move()
        if score >= beta:
            return score
        if score > bestscore:
            bestscore = score
        if score > alpha:
            alpha = score
    return bestscore


def quiesce(board, alpha, beta, PESTO):
    moves = board.calculate_all_legal_moves()
    stand_pat = evaluate(board, board.turn, moves, PESTO)
    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat
    for piece in moves:
        for move in moves[piece]:
            if board.board[move[0]] is not None:
                board.make_move(piece, move)
                score = -quiesce(board, -beta, -alpha, PESTO)
                board.unmake_move()
                if score >= beta:
                    return beta
                if score > alpha:
                    alpha = score
    return alpha
