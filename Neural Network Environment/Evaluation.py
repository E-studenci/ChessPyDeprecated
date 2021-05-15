from datetime import datetime

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


def evaluate(board, current_turn, all_legal_moves, PESTO=True):
    global leaf_count
    leaf_count += 1
    if moves_count(all_legal_moves) == 0:
        if board.king_pos[board.turn] in board.attacked_fields:
            return -20000
        else:
            return 0

    string_board = convert_board_to_string_board(board.board)
    endgame = is_endgame(string_board)
    score, doubled_pawns, isolated_pawns, blocked_pawns = eval(string_board, current_turn, endgame, PESTO)
    score = PIECE_POINT_VALUE * score
    score -= DOUBLED_BLOCKED_ISOLATED_PAWNS_VALUE * (doubled_pawns + isolated_pawns + blocked_pawns)

    return score


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


def piece_value(point_dictionary, piece, endgame, PESTO, multiplier, position):
    piece_points = point_dictionary[piece[1]][[0, 1][PESTO]][0][[0, 1][endgame]]
    piece_position = point_dictionary[piece[1]][[0, 1][PESTO]][1][[0, 1][endgame]][-multiplier * position]
    return piece_points + piece_position


def eval(board, current_turn, endgame=False, PESTO=True):
    score = 0
    doubled_pawns = 0
    isolated_pawns = 0
    blocked_pawns = 0
    columns = [{}, {}]
    for position in board.keys():
        piece = board[position]
        piece_is_current_color = (current_turn and piece[0] == 'w') or (not current_turn and piece[0] == 'b')
        multiplier = [-1, 1][piece_is_current_color]
        score += multiplier * piece_value(POINT_DICTIONARY, piece, endgame, PESTO, multiplier, position)
        if piece[1] == 'p':
            # count doubled pawns
            if position % 8 in columns[[0, 1][piece_is_current_color]]:
                columns[[0, 1][piece_is_current_color]][position % 8] += 1
            else:
                columns[[0, 1][piece_is_current_color]][position % 8] = 1
            # count blocked pawns
            if (position + 8 * [-1, 1][board[position][0] == 'w']) in board:
                blocked_pawns += multiplier
            # count isolated pawns
            surrounding_pawns = False
            for direction in [-1, 7, 8, 9, 1, -7, -8, -9]:
                if (position + direction) in board and board[position + direction] == board[position]:
                    surrounding_pawns = True
            if not surrounding_pawns:
                isolated_pawns += multiplier
    for count_opposite, count_current in zip(columns[0].values(), columns[1].values()):
        doubled_pawns += count_current if count_current > 1 else 0
        doubled_pawns -= count_opposite if count_opposite > 1 else 0
    return score, doubled_pawns, isolated_pawns, blocked_pawns


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


def alpha_beta_max(alpha, beta, depthleft, board, PESTO, last_moved_piece):
    if depthleft == 0:
        return evaluate(board, board.turn, PESTO)
    endgame = is_endgame_2(board)
    current_all_legal_moves = order_moves(board, board.calculate_all_legal_moves(),
                                          PESTO, endgame, last_moved_piece, True)
    for move in current_all_legal_moves:
        board.make_move(move[0], move[1])
        score = alpha_beta_min(alpha, beta, depthleft - 1, board, PESTO, move[1][0])
        board.unmake_move()
        if score >= beta:
            return beta
        if score > alpha:
            alpha = score
    return alpha


def alpha_beta(board, alpha, beta, depthleft, PESTO, last_moved_piece):
    bestscore = -9999
    if depthleft <= 0:
        return evaluate(board, board.turn, board.calculate_all_legal_moves(), PESTO)
    endgame = is_endgame_2(board)
    current_all_legal_moves = order_moves(board, board.calculate_all_legal_moves(),
                                          PESTO, endgame, last_moved_piece, True)
    for move in current_all_legal_moves:
        board.make_move(move[0], move[1])
        score = -alpha_beta(board, -beta, -alpha, depthleft - 1, PESTO, move[1][0])
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


def alpha_beta_min(alpha, beta, depthleft, board, PESTO, last_moved_piece):
    if depthleft == 0:
        return -evaluate(board, board.turn, PESTO)
    endgame = is_endgame_2(board)
    current_all_legal_moves = order_moves(board, board.calculate_all_legal_moves(),
                                          PESTO, endgame, last_moved_piece, True)
    for move in current_all_legal_moves:
        board.make_move(move[0], move[1])
        score = alpha_beta_max(alpha, beta, depthleft - 1, board, PESTO, move[1][0])
        board.unmake_move()
        if score <= alpha:
            return alpha
        if score < beta:
            beta = score
    return beta


def alpha_beta_score(depth, board, PESTO):
    return alpha_beta_max(float("-inf"), float("inf"), depth, board, PESTO, 0)


leaf_count = 0
if __name__ == '__main__':
    board = Board()
    board.initialize_board("r3k2r/pb2qpbp/1pn1pnp1/2PpP3/2B2B2/2N2N2/PPPQ1PPP/R3K2R w KQkq - 0 1")
    moves = board.calculate_all_legal_moves()
    # moves_sorted = order_moves_2(board, moves, True, False, None, True)

    # start = datetime.now()
    # for _ in range(100000):
    #     _ = order_moves_2(board, moves, True, False, None, True)
    # end = datetime.now()
    # print(end - start)
    # start = datetime.now()
    # for _ in range(1000):
    #     _ = order_moves(board, moves, True, False, None, True)
    # end = datetime.now()
    # print(end - start)

    print("r3k2r/pb2qpbp/1pn1pnp1/2PpP3/2B2B2/2N2N2/PPPQ1PPP/R3K2R w KQkq - 0 1")
    for i in range(20):
        move_count = 0
        start = datetime.now()
        print(-alpha_beta(board, -100000, -100000, i - 1, True, 0))
        end = datetime.now()
        print(i, end - start, move_count, leaf_count)
        leaf_count = 0
    # for i in range(20):
    #     move_count = 0
    #     start = datetime.now()
    #     print(alpha_beta_score(i, board, True))
    #     end = datetime.now()
    #     print(i, end - start, move_count)

    order_moves(board, board.calculate_all_legal_moves(), True, True)
