from Chess.Pieces.Piece import Piece
from Chess.Pieces.King import King


class Rook(Piece):
    """
        Sub class of Piece, it represents the bishop piece

        methods
            make_move(board, start_pos, end_pos) moves the rook
    """
    def __init__(self, color: bool, position: int):
        super().__init__(color, position)
        self.move_set = [8, 8, 0, 8, 0, 0, 8, 0]

    def make_move(self, board, start_pos, end_pos):
        """
        :param board: an object of type(Chess.Board.Board) the board on which the king is standing
        :param start_pos: the starting pos of the rook to move
        :param end_pos: the destination of the move
        :return:
            besides moving the rook, it sets the flag
            for the corresponding side castling in the player's king to False
        """
        # check if king/queen side, for now it is hacked
        king_index = board.find_piece(King(self.color, -1))
        if king_index != -1:
            if start_pos % len(board.board) == 0:
                board.board[king_index].castle_queen_side = False
            elif start_pos % len(board.board) == len(board.board) - 1:
                board.board[king_index].castle_king_side = False
        return super().make_move(board, start_pos, end_pos)
