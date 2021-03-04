from Chess.Pieces.Piece import Piece


class Queen(Piece):

    def __init__(self, color: bool, position: int):
        super().__init__(color, position)
        self.move_set = [8, 8, 8, 8, 8, 8, 8, 8]
