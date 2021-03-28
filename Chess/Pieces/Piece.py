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
        self.pinned: bool = True
        self.move_set: list = []
        self.possible_moves: list = []

    def calculate_legal_moves(self, board, calculate_checks=True):
        """
        :param calculate_checks: should the moves that will leave the [self.color] player's king in check be removed
        :param board: Chess.Board.Board, the board on which the piece is standing
        :return: returns a list of all legal move for the piece
        """
        legal_moves = []
        for index in range(len(self.move_set)):
            interrupted = False
            temp = self.move_set[index]
            current_position = self.position
            currently_calculated_position = 0
            while not interrupted \
                    and temp > 0:
                currently_calculated_position = current_position + Constants.DIRECTION_MATH[index]
                if (currently_calculated_position % Constants.BOARD_SIZE - current_position % Constants.BOARD_SIZE) == \
                        Constants.COLUMN_CHANGE[index] \
                        and 0 <= currently_calculated_position <= len(board.board) - 1:
                    if isinstance(board.board[currently_calculated_position], type(None)) \
                            or board.board[currently_calculated_position].color != self.color:
                        legal_moves.append((currently_calculated_position, 0))
                    if not isinstance(board.board[currently_calculated_position], type(None)):
                        interrupted = True
                    current_position = currently_calculated_position
                temp -= 1

        if calculate_checks:
            for i in range(len(legal_moves) - 1, -1, -1):
                if board.king_in_check_after_move_ver_2_0(self.color, self.position, legal_moves[i]):
                    legal_moves.remove(legal_moves[i])
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
