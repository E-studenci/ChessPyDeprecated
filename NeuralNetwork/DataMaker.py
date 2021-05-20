from Chess.Board.Board import Board
from Chess.Board.Board import Board
from Chess.Pieces.Bishop import Bishop
from Chess.Pieces.King import King
from Chess.Pieces.Knight import Knight
from Chess.Pieces.Pawn import Pawn
from Chess.Pieces.Queen import Queen
from Chess.Pieces.Rook import Rook
import time
import chess
import chess.engine
import random
import numpy
import os

piece_dict = {
    (Pawn, 1):   0,
    (Knight, 1): 1,
    (Bishop, 1): 2,
    (Rook, 1):   3,
    (Queen, 1):  4,
    (King, 1):   5,
    (Pawn, 0):   6,
    (Knight, 0): 7,
    (Bishop, 0): 8,
    (Rook, 0):   9,
    (Queen, 0):  10,
    (King, 0):   11,
}

squares_index = {
    'a': 0,
    'b': 1,
    'c': 2,
    'd': 3,
    'e': 4,
    'f': 5,
    'g': 6,
    'h': 7
}


def random_board(max_depth=100):
    board = Board()
    depth = random.randrange(0, max_depth)

    for _ in range(depth):
        all_moves = board.calculate_all_legal_moves()
        random_piece = random.choice(all_moves)
        random_move = random.choice(random_piece)
        board.make_move(random_move.position, random_move)
        # if board.is_game_over():
        #     break

    return board


def convert_fen_data(read_file_path, write_file_path, board_evaluation_depth=10):
    x_train = []
    boards = []

    read_file = open(read_file_path)
    if not os.path.exists(write_file_path):
        write_file = open(write_file_path, mode='w')
    i = 1
    while True:
        line = read_file.readline()
        if line == '' or i > 3000000:
            print("End of file")
            break
        if i % 100000 == 0:
            print(f"{i} line")
        i += 1
        fen = line.split(',')[0]
        board = Board()
        if not board.initialize_board(fen):
            print(f"Incorrect fen: {fen}")
        else:
            better_board = chess.Board(fen=fen)
            board_array = convert_board(board)
            x_train.append(board_array)
            boards.append(better_board)
    y_train = stockfish(boards, board_evaluation_depth)
    x_train, y_train = remove_none(x_train, y_train)
    numpy.savez(write_file_path, x=x_train, y=y_train)
    read_file.close()


def remove_none(x_train, y_train):
    result_1 = []
    result_2 = []
    for i in range(len(y_train)):
        if y_train[i] is not None:
            result_1.append(x_train[i])
            result_2.append(int(y_train[i]))
    return result_1, result_2


def stockfish(boards, depth):
    results = []
    with chess.engine.SimpleEngine.popen_uci('Stockfish/stockfish.exe') as sf:
        for board in boards:
            result = sf.analyse(board, chess.engine.Limit(depth=depth))
            score = result['score'].white().score()
            results.append(score)
        return results


def convert_board(board):
    ret_array = numpy.zeros((14, 8, 8))
    attacked_fields_ = attacked_fields(board)
    ret_array[12] = numpy.flip(numpy.reshape(attacked_fields_[1], (-1, 8)), 1)
    ret_array[13] = numpy.flip(numpy.reshape(attacked_fields_[0], (-1, 8)), 1)
    for i, piece in enumerate(board.board):
        if piece is not None:
            row, col = (7 - i // 8), i % 8
            ret_array[piece_dict[(type(piece), piece.color)]][row][col] = 1

    # ret_array = numpy.expand_dims(ret_array, 0)
    return ret_array


def attacked_fields(board):
    attacked_fields = [None, None]
    attacked_fields[1 - board.turn] = board.attacked_fields[::-1]
    board.turn = not board.turn
    board.calculate_all_attacked_fields()
    attacked_fields[1 - board.turn] = board.attacked_fields[::-1]
    board.turn = not board.turn
    return attacked_fields


if __name__ == '__main__':
    import os
    xd = os.path.join('Data', 'chessData.csv')
    convert_fen_data('Data/chessData.csv', 'Data/new_data.npz')

