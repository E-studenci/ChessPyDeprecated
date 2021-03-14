from Chess.Pieces import Bishop, King, Knight, Piece, Queen, Rook, Constants


class Pawn(Piece.Piece):

    def __init__(self, color: bool, position: int):
        super().__init__(color, position)
        self.en_passant: bool = True
        self.move_set = [1]

    def make_move(self, board, start_pos, end_pos):
        # Promotion, for now it is hard coded for queen
        if 56 <= end_pos <= 63 \
                or 0 <= end_pos <= 7:
            board.board[end_pos] = None
            board.board[end_pos] = Queen.Queen(self.color, end_pos)
            board.board[start_pos] = None
            return True
        # first move
        elif abs(start_pos / 8 - end_pos / 8) == 2:
            self.en_passant = True
            self.position = end_pos
            return super().make_move(board, start_pos, end_pos)
            return False
        # en passant
        elif not abs(start_pos - end_pos) == 8 \
                and isinstance(board.board[end_pos], type(None)):
            if end_pos > start_pos:
                board.take(end_pos - 8)
            else:
                board.take(end_pos + 8)
            return super().make_move(board, start_pos, end_pos)
        # normal move and taking
        else:
            return super().make_move(board, start_pos, end_pos)

    def calculate_legal_moves(self, chess_board):
        return_list = []
        # normal move
        if self.color:
            if isinstance(chess_board[self.position + Constants.DIRECTION_MATH[0]], type(None)):
                return_list.append(self.position + Constants.DIRECTION_MATH[0])
        else:
            if isinstance(chess_board[self.position - Constants.DIRECTION_MATH[0]], type(None)):
                return_list.append(self.position - Constants.DIRECTION_MATH[0])
        # first move
        if self.color \
                and 1 <= self.position / 8 < 2 \
                and isinstance(chess_board[self.position + 8], type(None)) \
                and isinstance(chess_board[self.position + 16], type(None)):
            return_list.append(self.position + 16)
        else:
            if 6 <= self.position / 8 < 7 \
                    and isinstance(chess_board[self.position - 8], type(None)) \
                    and isinstance(chess_board[self.position - 16], type(None)):
                return_list.append(self.position - 16)
        # en passant to the right
        if isinstance(chess_board[self.position + 1], type(self)):
            if not chess_board[self.position + 1].color == self.color \
                    and chess_board[self.position + 1].en_passant:
                if self.color:
                    return_list.append(self.position + Constants.DIRECTION_MATH[2])
                else:
                    return_list.append(self.position + Constants.DIRECTION_MATH[4])
        # en passant to the left
        if isinstance(chess_board[self.position - 1], type(self)):
            if not chess_board[self.position - 1].color == self.color \
                    and chess_board[self.position - 1].en_passant:
                if self.color:
                    return_list.append(self.position + Constants.DIRECTION_MATH[5])
                else:
                    return_list.append(self.position + Constants.DIRECTION_MATH[7])
        # taking
        if self.color:
            if not isinstance(chess_board[self.position + Constants.DIRECTION_MATH[0] + 1], type(None)):
                if not chess_board[self.position + Constants.DIRECTION_MATH[0] + 1].color == self.color:
                    return_list.append(self.position + Constants.DIRECTION_MATH[0] + 1)
            if not isinstance(chess_board[self.position + Constants.DIRECTION_MATH[0] - 1], type(None)):
                if not chess_board[self.position + Constants.DIRECTION_MATH[0] - 1].color == self.color:
                    return_list.append(self.position + Constants.DIRECTION_MATH[0] - 1)
        else:
            if not isinstance(chess_board[self.position - Constants.DIRECTION_MATH[0] + 1], type(None)):
                if not chess_board[self.position - Constants.DIRECTION_MATH[0] + 1].color == self.color:
                    return_list.append(self.position - Constants.DIRECTION_MATH[0] + 1)
            if not isinstance(chess_board[self.position - Constants.DIRECTION_MATH[0] - 1], type(None)):
                if not chess_board[self.position - Constants.DIRECTION_MATH[0] - 1].color == self.color:
                    return_list.append(self.position - Constants.DIRECTION_MATH[0] - 1)
        return return_list
