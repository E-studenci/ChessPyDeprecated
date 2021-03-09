from abc import ABC, abstractmethod
from Chess.Pieces import Constants


class Piece(ABC):

    @abstractmethod
    def __init__(self, color: bool, position: int):
        self.color: bool = color
        self.position: int = position
        self.pinned: bool = False
        self.move_set: list = []
        self.possible_moves: list = []

    def get_color(self):
        return self.color

    def get_possible_moves(self):
        return self.possible_moves

    def calculate_legal_moves(self, chess_board):
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
                        and 0 <= currently_calculated_position <= len(chess_board) - 1:
                    if isinstance(chess_board[currently_calculated_position], type(None)) \
                            or chess_board[currently_calculated_position].color != self.color:
                        # check if king will be in check
                        # if not:
                        legal_moves.append(currently_calculated_position)
                        current_position = currently_calculated_position
                    if not isinstance(chess_board[currently_calculated_position], type(None)):
                        interrupted = True
                temp -= 1
        return legal_moves

    def make_move(self, board, start_pos, end_pos):
        # move piece from a to b
        # if b is occupied, take
        if not isinstance(board.get_board()[end_pos], type(None)):
            board.take(end_pos)
        self.position = end_pos
        board.get_board()[end_pos] = self
        board.get_board()[start_pos] = None
        # update all legal moves (to make check checking more optimised)

