from Chess.Pieces.Piece import Piece


class King(Piece):

    def __init__(self, color: bool, position: int):
        super().__init__(color, position)
        self.castle: bool = True
        self.possible_moves = [1, 1, 1, 1, 1, 1, 1, 1]

