from Chess.Pieces.Piece import Piece


class Rook(Piece):
    """
        Sub class of Piece, it represents the bishop piece

        methods
            make_move(board, start_pos, end_pos) moves the rook
    """

    def __init__(self, color: bool, position: int):
        super().__init__(color, position)
        self.move_set = [8, 8, 0, 8, 0, 0, 8, 0]

    def make_move(self, board, start_pos, move):
        """
        :param board: an object of type(Chess.Board.Board) the board on which the king is standing
        :param start_pos: the starting pos of the rook to move
        :param move: (end_pos, promotion_type) the end pos of the move, and promotion flag
        :return:
            besides moving the rook, it sets the flag
            for the corresponding side castling in the player's king to False
        """
        from Chess.Pieces.King import King
        king_position = board.king_pos[self.color]
        if king_position != -1:
            if start_pos == king_position + 3:
                board.board[king_position].castle_king_side = False
            elif start_pos == king_position - 4:
                board.board[king_position].castle_queen_side = False
        return super().make_move(board, start_pos, move)
