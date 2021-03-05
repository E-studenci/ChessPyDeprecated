from Chess.Pieces.Piece import Piece


class King(Piece):

    def __init__(self, color: bool, position: int):
        super().__init__(color, position)
        self.castle_king_side: bool = True
        self.castle_queen_side: bool = True
        self.move_set = [1, 1, 1, 1, 1, 1, 1, 1]

