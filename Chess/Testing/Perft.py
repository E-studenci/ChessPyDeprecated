from Chess.Board.Board import Board
from Chess.Board.Converters.FenDecoder import initialize_list_from_FEN


def count_legal_moves(boaard, depth):
    moves = 0
    while board.move_count <= depth:
        temp = boaard.calculate_all_legal_moves(board.turn)
        moves += count_vals(temp)
        for piece in temp:
            for move in temp[piece]:
                boaard.make_move(piece.position, move)
                moves += count_legal_moves(boaard, depth - 1)
    return moves


def count_vals(temp):
    count = 0
    for piece in temp:
        for move in temp[piece]:
            count += 1
    return count


if __name__ == '__main__':
    board = Board()
    board.board, board.turn, board.fifty_move_rule, board.move_count \
        = initialize_list_from_FEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    print(count_legal_moves(board, 6))
