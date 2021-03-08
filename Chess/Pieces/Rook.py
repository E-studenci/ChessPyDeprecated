from Chess.Pieces.Piece import Piece


class Rook(Piece):

    def __init__(self, color: bool, position: int):
        super().__init__(color, position)
        self.move_set = [8,8,0,8,0,0,8,0]
