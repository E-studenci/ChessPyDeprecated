from Chess.Pieces.Piece import Piece


class Bishop(Piece):

    def __init__(self, color: bool, position: int):
        super().__init__(color, position)
        self.possible_moves = [0, 8, 0, 8, 0, 8, 0, 8]
