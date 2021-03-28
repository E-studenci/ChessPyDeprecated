from Chess.Pieces import Rook
from Chess.Pieces.Piece import Piece


class King(Piece):
    """
        Sub class of Piece, it represents the king piece

        Attributes
            castle_king_side: bool
            castle_queen_side: bool
                flags for queen and king side castling, if true, the king can castle
        methods
            calculate_legal_moves(chess_board)
                other than super() functionality, it calculates castling
            make_move(board, start_pos, end_pos)
                other than super() functionality, it moves the rook to complete castling
    """

    def __init__(self, color: bool, position: int):
        super().__init__(color, position)
        self.castle_king_side: bool = True
        self.castle_queen_side: bool = True
        self.move_set = [1, 1, 1, 1, 1, 1, 1, 1]

    def calculate_legal_moves(self, board, calculate_checks=True):
        """
        :param calculate_checks: should the moves that will leave the [self.color] player's king in check be removed
        :param board: list the board on which the pawn is standing
        :return: returns a list of all legal moves for the king with the addition of castling
        """
        return_list = super().calculate_legal_moves(board, calculate_checks)
        if self.castle_king_side \
                and isinstance(board.board[self.position + 1], type(None)) \
                and isinstance(board.board[self.position + 2], type(None)) \
                and not board.king_in_check_after_move_ver_2_0(self.color, self.position, (self.position + 1, 0)) \
                and not board.king_in_check_after_move_ver_2_0(self.color, self.position, (self.position + 2, 0)) \
                and isinstance(board.board[self.position + 3], Rook.Rook):
            if board.board[self.position + 3].color == self.color:
                return_list.append((self.position + 2, 0))
        if self.castle_queen_side \
                and isinstance(board.board[self.position - 1], type(None)) \
                and isinstance(board.board[self.position - 2], type(None)) \
                and isinstance(board.board[self.position - 3], type(None)) \
                and not board.king_in_check_after_move_ver_2_0(self.color, self.position, (self.position - 1, 0)) \
                and not board.king_in_check_after_move_ver_2_0(self.color, self.position, (self.position - 2, 0)) \
                and isinstance(board.board[self.position - 4], Rook.Rook):
            if board.board[self.position - 4].color == self.color:
                return_list.append((self.position - 2, 0))
        return return_list

    def make_move(self, board, start_pos, move):
        """
        :param board: an object of type(Chess.Board.Board) the board on which the king is standing
        :param start_pos: the starting pos of the king to move
        :param move: (end_pos, promotion_type) the end pos of the move, and promotion flag
        :return: moves the king from [start_pos] to [end_pos] and moves the rook if castling
        """
        # king side castling
        if move[0] - start_pos == 2:
            board.board[start_pos + 1] = board.board[start_pos + 3]
            board.board[start_pos + 3] = None
        # queen side castling
        if move[0] - start_pos == -2:
            board.board[start_pos - 1] = board.board[start_pos - 4]
            board.board[start_pos - 4] = None

        board.king_pos[self.color] = move[0]

        self.castle_king_side = False
        self.castle_queen_side = False
        return super().make_move(board, start_pos, move)
