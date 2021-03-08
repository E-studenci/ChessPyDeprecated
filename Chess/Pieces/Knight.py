from Chess.Pieces.Piece import Piece


class Knight(Piece):

    def __init__(self, color: bool, position: int):
        super().__init__(color, position)
        self.move_set = [0]*8+[1]*8

