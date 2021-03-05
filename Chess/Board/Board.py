from Chess.Pieces.Piece import Piece


class Board:

    SIZE = 8

    def __init__(self):
        self.board: list
        self.turn
        self.legal_moves = []

    def get_board(self):
        return self.board


    def calculate_all_legal_moves(self):
        for piece in board:
            if piece is not None:
                if piece.get_color() == turn:
                    calculate_legal_moves


if __name__ == '__main__':
    pass