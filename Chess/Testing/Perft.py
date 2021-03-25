import copy
import time
from Chess.Board.Board import Board
from Chess.Board.Converters.FenDecoder import initialize_list_from_FEN
from Chess.Board.PrintMatrixToConsole import print_matrix_to_console


def count_legal_moves_recursive(chess_board, depth):
    all_legal_moves = 0
    if depth > 0:
        current_all_legal_moves = chess_board.calculate_all_legal_moves(chess_board.turn)
        for piece in current_all_legal_moves:
            for move in current_all_legal_moves[piece]:
                if depth == 1:
                    all_legal_moves += 1
                temp_board = copy.deepcopy(chess_board)
                temp_board.make_move(piece.position, move)
                all_legal_moves += count_legal_moves_recursive(temp_board, depth - 1)
    return all_legal_moves


def count_legal_moves(chess_board, depth):
    all_legal_moves = 0
    current_depth = 0
    queue = [(chess_board, current_depth)]
    while queue:
        pop_board, current_depth = queue.pop(0)
        if current_depth < depth:
            current_all_legal_moves = pop_board.calculate_all_legal_moves(pop_board.turn)
            for piece in current_all_legal_moves:
                for move in current_all_legal_moves[piece]:
                    if depth == current_depth + 1:
                        all_legal_moves += 1
                    temp_board = copy.deepcopy(pop_board)
                    temp_board.make_move(piece.position, move)
                    queue.append((temp_board, current_depth + 1))
    return all_legal_moves


if __name__ == '__main__':
    board = Board()
    board.board, board.turn, board.fifty_move_rule, board.move_count \
        = initialize_list_from_FEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    start_time = time.time()
    print(count_legal_moves_recursive(board, 4))
    print("--- %s seconds ---" % (time.time() - start_time))
