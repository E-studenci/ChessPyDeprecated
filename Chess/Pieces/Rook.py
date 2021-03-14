from Chess.Pieces.Piece import Piece
from Chess.Pieces.King import King


class Rook(Piece):

    def __init__(self, color: bool, position: int):
        super().__init__(color, position)
        self.move_set = [8, 8, 0, 8, 0, 0, 8, 0]

    def make_move(self, board, start_pos, end_pos):
        # check if king/queen side, for now it is hacked
        king_index = board.find_piece(King(self.color, -1))
        if king_index != -1:
            if start_pos % len(board.board) == 0:
                board.board[king_index].castle_queen_side = False
            elif start_pos % len(board.board) == len(board.board) - 1:
                board.board[king_index].castle_king_side = False
        return super().make_move(board, start_pos, end_pos)
