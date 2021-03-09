from Chess.Pieces import Bishop, King, Knight, Piece, Queen, Rook


class Pawn(Piece.Piece):

    def __init__(self, color: bool, position: int):
        super().__init__(color, position)
        self.en_passant: bool = False
        self.move_set = [1]

    # add taking for a pawn

    def make_move(self, board, start_pos, end_pos):
        super().make_move(board, start_pos, end_pos)
        # Promotion, for now it is hard coded for queen
        if 56 <= end_pos <= 63 \
                or 0 <= end_pos <= 7:
            board.board[end_pos] = None
            board.board[end_pos] = Queen.Queen(self.color, end_pos)
