from Chess.Pieces.Piece import Piece


class King(Piece):

    def __init__(self, color: bool, position: int):
        super().__init__(color, position)
        self.castle_king_side: bool = True
        self.castle_queen_side: bool = True
        self.move_set = [1, 1, 1, 1, 1, 1, 1, 1]

    def calculate_legal_moves(self, board):
        return super().calculate_legal_moves(board)

    def make_move(self, board, start_pos, end_pos):
        super().make_move(board, start_pos, end_pos)
        self.castle_king_side = False
        self.castle_queen_side = False
