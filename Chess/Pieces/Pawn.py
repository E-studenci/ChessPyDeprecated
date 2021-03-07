from Chess.Pieces.Piece import Piece


class Pawn(Piece):

    def __init__(self, color: bool, position: int):
        super().__init__(color, position)
        self.en_passant: bool = False
        self.move_set = [1]
