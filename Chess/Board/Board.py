from Chess.Pieces.Piece import Piece


class Board:

    SIZE = 8

    def __init__(self):
        self.board: list
        self.fifty_move_rule = 0
        self.move_count = 0
