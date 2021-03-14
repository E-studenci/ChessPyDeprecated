from Chess.Pieces.Piece import Piece


class King(Piece):

    def __init__(self, color: bool, position: int):
        super().__init__(color, position)
        self.castle_king_side: bool = True
        self.castle_queen_side: bool = True
        self.move_set = [1, 1, 1, 1, 1, 1, 1, 1]

    def calculate_legal_moves(self, board):
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
