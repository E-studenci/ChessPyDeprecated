import copy

from Chess.Pieces import Bishop, King, Knight, Piece, Queen, Rook, Constants

direction_dictionary = {True: +1,
                        False: -1}
second_row_dictionary = {True: 1,
                         False: 6}
last_row_dictionary = {True: 7,
                       False: 0}
promotion_dictionary = {1: Knight.Knight,
                        2: Bishop.Bishop,
                        3: Rook.Rook,
                        4: Queen.Queen}


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

    def make_move(self, board, start_pos, move):
        """
        :param board: an object of type(Chess.Board.Board) the board on which the pawn is standing
        :param start_pos: the starting pos of the move
        :param move: (end_pos, promotion_type) the end pos of the move, and promotion flag
        :return: it handles moving the pawn forward, on the diagonal to take, en passant, and promoting
        """
        direction = direction_dictionary[self.color]
        # Promotion
        if not move[1] == 0:
            board.take(move[0])
            board.board[move[0]] = promotion_dictionary[move[1]](self.color, move[0])
            board.board[start_pos] = None
            return True
        # first move
        elif abs(start_pos / 8 - move[0] / 8) == 2:
            self.en_passant = True
            self.position = move[0]
            return super().make_move(board, start_pos, move)
        # en passant
        elif not abs(start_pos - move[0]) == 8 \
                and isinstance(board.board[move[0]], type(None)):
            board.take(move[0] - 8 * direction)
            return super().make_move(board, start_pos, move)
        # normal move and taking
        else:
            return super().make_move(board, start_pos, move)

    def calculate_legal_moves(self, board, calculate_checks=True):
        """
        :param calculate_checks: should the moves that will leave the [self.color] player's king in check be removed
        :param board: Chess.Board.Board, the board on which the pawn is standing
        :return: returns a list of all legal moves for the pawn
        """
        return_list = []
        direction = direction_dictionary[self.color]
        second_row = second_row_dictionary[self.color]
        last_row = last_row_dictionary[self.color]
        # normal move
        currently_calculated_position = self.position + (Constants.DIRECTION_MATH[0] * direction)
        if isinstance(board.board[currently_calculated_position], type(None)):
            if last_row * 8 <= currently_calculated_position < (last_row + 1) * 8:
                for i in range(1, 5):
                    return_list.append((currently_calculated_position, i))
            else:
                return_list.append((currently_calculated_position, 0))
        # first move
        if second_row * 8 <= self.position < (second_row + 1) * 8 \
                and isinstance(board.board[self.position + 8 * direction], type(None)) \
                and isinstance(board.board[self.position + 16 * direction], type(None)):
            currently_calculated_position = self.position + 16 * direction
            return_list.append((currently_calculated_position, 0))
        # en passant
        for i in range(0, 2):
            currently_calculated_position = self.position \
                                            + 1 * direction * direction_dictionary[bool(i)]
            if abs(currently_calculated_position % 8 - self.position % 8) == 1:
                if isinstance(board.board[currently_calculated_position], type(self)):
                    if not board.board[currently_calculated_position].color == self.color \
                            and board.board[currently_calculated_position].en_passant:
                        currently_calculated_position += 8 * direction
                        if isinstance(board.board[currently_calculated_position], type(None)):
                            return_list.append((currently_calculated_position, 0))
        # taking
        for i in range(0, 2):
            currently_calculated_position = self.position \
                                            + Constants.DIRECTION_MATH[0] * direction \
                                            + 1 * direction_dictionary[bool(i)]
            if abs(currently_calculated_position % 8 - self.position % 8) == 1:
                if not isinstance(board.board[currently_calculated_position], type(None)):
                    if not board.board[currently_calculated_position].color == self.color:
                        if last_row * 8 <= currently_calculated_position < (last_row + 1) * 8:
                            for i in range(1, 5):
                                return_list.append((currently_calculated_position, i))
                        else:
                            return_list.append((currently_calculated_position, 0))

        temp_return_list = copy.deepcopy(return_list)
        if calculate_checks:
            for move in return_list:
                if board.king_in_check_after_move(self.color, self.position, move):
                    temp_return_list.remove(move)
        return_list = temp_return_list
        return return_list
