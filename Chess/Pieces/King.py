from Chess.Pieces.Piece import Piece
from Chess.Board.Board import Board


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

    def calculate_legal_moves(self, board):
        """
        :param board: list the board on which the pawn is standing
        :return: returns a list of all legal moves for the king with the addition of castling
        """
        return_list = super().calculate_legal_moves(board)
        if self.castle_king_side \
                and isinstance(board[self.position + 1], type(None)) \
                and isinstance(board[self.position + 2], type(None)):
            return_list.append(self.position + 2)
        if self.castle_queen_side \
                and isinstance(board[self.position - 1], type(None)) \
                and isinstance(board[self.position - 2], type(None)) \
                and isinstance(board[self.position - 3], type(None)):
            return_list.append(self.position - 2)
        return return_list

    def make_move(self, board, start_pos, end_pos):
        """
        :param board: an object of type(Chess.Board.Board) the board on which the king is standing
        :param start_pos: the starting pos of the king to move
        :param end_pos: the destination of the move
        :return: moves the king from [start_pos] to [end_pos] and moves the rook if castling
        """
        # king side castling
        if end_pos - start_pos == 2:
            board.board[start_pos + 1] = board.board[start_pos + 3]
            board.board[start_pos + 3] = None
        # queen side castling
        if end_pos - start_pos == -2:
            board.board[start_pos - 1] = board.board[start_pos - 4]
            board.board[start_pos - 4] = None

        self.castle_king_side = False
        self.castle_queen_side = False
        return super().make_move(board, start_pos, end_pos)
