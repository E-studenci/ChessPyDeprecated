from Chess.Pieces import Bishop, King, Knight, Piece, Queen, Rook, Constants

direction_dictionary = {True: +1,
                        False: -1}
row_dictionary = {True: 1,
                  False: 6}


class Pawn(Piece.Piece):
    """
        Sub class of Piece, it represents the pawn piece

        Attributes
            en_passant: bool
                if true, the opposing, adjacent pawn will be able to make an absolutely outstanding move
                called "en passant".
                Read up on it, if you don't know what that is, honey.
                If you can't find it, in some countries it appears under an alias: "bicie w przelocie",
                don't mistake it for "bicie a popular chess piece", or at least not in working hours.

        methods
            calculate_legal_moves(chess_board)
                calculates all possible moves for a pawn
            make_move(board, start_pos, end_pos)
                moves the pawn
    """

    def __init__(self, color: bool, position: int):
        super().__init__(color, position)
        self.en_passant: bool = True
        self.move_set = [1]

    def make_move(self, board, start_pos, end_pos):
        """
        :param board: an object of type(Chess.Board.Board) the board on which the pawn is standing
        :param start_pos: the starting pos of the move
        :param end_pos: the end pos of the move
        :return: it handles moving the pawn forward, on the diagonal to take, en passant, and promoting
        """
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

    def calculate_legal_moves(self, board, calculate_checks=True):
        """
        :param chess_board: list, the board on which the pawn is standing
        :return: returns a list of all legal moves for the pawn
        """
        return_list = []
        direction = direction_dictionary[self.color]
        row = row_dictionary[self.color]
        # normal move
        currently_calculated_position = self.position + (Constants.DIRECTION_MATH[0] * direction)
        if isinstance(board.board[currently_calculated_position], type(None)):
            return_list.append(currently_calculated_position)
        # first move
        if row * 8 <= self.position < (row + 1) * 8 \
                and isinstance(board.board[self.position + 8 * direction], type(None)) \
                and isinstance(board.board[self.position + 16 * direction], type(None)):
            currently_calculated_position = self.position + 16 * direction
            return_list.append(currently_calculated_position)
        # en passant
        for i in range(0, 2):
            currently_calculated_position = self.position \
                                            + 1 * direction * direction_dictionary[bool(i)]
            if (currently_calculated_position % 8 - self.position % 8) == 1:
                if isinstance(board.board[currently_calculated_position], type(self)):
                    if not board.board[currently_calculated_position].color == self.color \
                            and board.board[currently_calculated_position].en_passant:
                        currently_calculated_position += 8 * direction
                        return_list.append(currently_calculated_position)
        # taking
        for i in range(0, 2):
            currently_calculated_position = self.position \
                                            + Constants.DIRECTION_MATH[0] * direction \
                                            + 1 * direction_dictionary[bool(i)]
            if (currently_calculated_position % 8 - self.position % 8) == 1:
                if not isinstance(board.board[currently_calculated_position], type(None)):
                    if not board.board[currently_calculated_position].color == self.color:
                        return_list.append(currently_calculated_position)
        if calculate_checks:
            for move in return_list:
                if board.king_in_check_after_move(self.color, self.position, move):
                    return_list.remove(move)
        return return_list
