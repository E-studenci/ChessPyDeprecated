import copy
from abc import ABC, abstractmethod
from Chess.Pieces import Constants


class Piece(ABC):
    """
        An abstract class representing chess pieces

        Attributes
            color: bool
                a flag representing the color of the piece
                                                - white - True
                                                - black - False
            position: int
                the current position of the piece on chess board
            pinned: bool
                a flag used to determine if the piece is pinned
            move_set: list
                a list representing the amount of steps the piece can take
                in the direction at matching index in Constants.DIRECTION_MATH
            possible_moves: list
                a list holding all the moves the piece can currently make

        methods
            calculate_legal_moves(chess_board)
                calculates all legal moves for the piece
            make_move(board, start_pos, end_pos)
                moves a piece [start_pos] to [end_pos]
    """

    @abstractmethod
    def __init__(self, color: bool, position: int):
        self.color: bool = color
        self.position: int = position
        self.pinned_squares = None
        self.move_set: list = []
        self.possible_moves: list = []

    def calculate_legal_moves(self, board):
        if len(board.attacked_lines) > 1:
            self.pinned_squares = None
            return []

        legal_moves = []

        from Chess.Pieces.Knight import Knight
        if isinstance(self, Knight):
            direction_math = Constants.KNIGHT_DIRECTION_MATH
            column_change = Constants.KNIGHT_COLUMN_CHANGE
        else:
            direction_math = Constants.NORMAL_DIRECTION_MATH
            column_change = Constants.NORMAL_COLUMN_CHANGE

        for direction_index in range(len(self.move_set)):
            interrupted = False
            maximum_move_length = self.move_set[direction_index]
            current_position = self.position
            while not interrupted and maximum_move_length > 0:
                currently_calculated_position = current_position + direction_math[direction_index]
                if currently_calculated_position % Constants.BOARD_SIZE - current_position % Constants.BOARD_SIZE == \
                   column_change[direction_index] \
                   and 0 <= currently_calculated_position <= len(board.board) - 1:
                    if currently_calculated_position in board.attacked_lines[0] if len(board.attacked_lines) == 1 else True:
                        if currently_calculated_position in self.pinned_squares if self.pinned_squares is not None else True:
                            if isinstance(board.board[currently_calculated_position], type(None)) \
                                    or board.board[currently_calculated_position].color != self.color:
                                legal_moves.append((currently_calculated_position, 0))
                    if not isinstance(board.board[currently_calculated_position], type(None)):
                        interrupted = True
                    current_position = currently_calculated_position
                    maximum_move_length -= 1
                else:
                    interrupted = True
        self.pinned_squares = None
        return legal_moves

    def make_move(self, board, start_pos, move):
        """
        :param board: an object of type(Chess.Board.Board) the board on which the pawn is standing
        :param start_pos: the starting pos of a piece to move
        :param move: (end_pos, promotion_type) the end pos of the move, and promotion flag
        :return: moves the piece from [start_pos] to [end_pos]
                uses board.take(end_pos) if the end_pos is occupied by opposing piece
        """
        # move piece from a to b
        # if b is occupied, take
        if not isinstance(board.board[move[0]], type(None)):
            board.take(move[0])
        self.position = move[0]
        board.board[start_pos] = None
        board.board[move[0]] = self
        return True
        # update all legal moves (to make check checking more optimised)

    def calculate_attacked_fields(self, board):
        from Chess.Pieces.King import King
        for index in range(len(self.move_set)):
            interrupted = False
            piece_in_way = False
            king_in_way = False
            add_pin_line = False
            maximum_move_length = self.move_set[index]
            current_position = self.position
            pin_line = set()
            pin_line.add(current_position)
            pinned_piece = None
            while not interrupted and maximum_move_length > 0:
                currently_calculated_position = current_position + Constants.NORMAL_DIRECTION_MATH[index]
                if currently_calculated_position % Constants.BOARD_SIZE - current_position % Constants.BOARD_SIZE == \
                   Constants.NORMAL_COLUMN_CHANGE[index] \
                   and 0 <= currently_calculated_position <= len(board.board) - 1:
                    if not piece_in_way or king_in_way:
                        board.attacked_fields[currently_calculated_position] = True
                    if not king_in_way:
                        pin_line.add(currently_calculated_position)
                    attacked_square = board.board[currently_calculated_position]
                    if not isinstance(attacked_square, type(None)):
                        if attacked_square.color is self.color:
                            interrupted = True
                        else:
                            if isinstance(attacked_square, King):
                                if piece_in_way:
                                    interrupted = True
                                    add_pin_line = True
                                else:
                                    king_in_way = True
                                    board.attacked_lines.append(pin_line)
                        if piece_in_way:
                            interrupted = True
                        else:
                            pinned_piece = attacked_square
                        piece_in_way = True
                    current_position = currently_calculated_position
                    maximum_move_length -= 1
                else:
                    interrupted = True
            if pinned_piece is not None:
                if add_pin_line:
                    pinned_piece.pinned_squares = pin_line
