from Chess.Pieces.Piece import Piece


class King(Piece):

    def __init__(self, color: bool, position: int):
        super().__init__(color, position)
        self.castle: bool = True
        self.move_set = [1, 1, 1, 1, 1, 1, 1, 1]

    def calculate_legal_moves(self, board):
        return super().calculate_legal_moves(board)


