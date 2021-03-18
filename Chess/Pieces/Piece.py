from abc import ABC, abstractmethod
from Chess.Pieces import Constants


class Piece(ABC):

    @abstractmethod
    def __init__(self, color: bool, position: int):
        self.color: bool = color
        self.position: int = position
        self.pinned: bool = True
        self.move_set: list = []
        self.possible_moves: list = []

    def get_color(self):
        return self.color

    def get_possible_moves(self):
        return self.possible_moves

    def calculate_legal_moves(self, board, calculate_checks=True):
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
                        if calculate_checks:
                            if not board.king_in_check_after_move(self.color, self.position,
                                                                  currently_calculated_position):
                                legal_moves.append(currently_calculated_position)
                        else:
                            legal_moves.append(currently_calculated_position)
                        current_position = currently_calculated_position
                    if not isinstance(board.board[currently_calculated_position], type(None)):
                        interrupted = True
                temp -= 1
        return legal_moves

    # TODO: usunac start_pos
    def make_move(self, board, start_pos, end_pos):
        # move piece from a to b
        # if b is occupied, take
        if not isinstance(board.board[end_pos], type(None)):
            board.take(end_pos)
        self.position = end_pos
        board.board[end_pos] = self
        board.board[start_pos] = None
        return True
        # update all legal moves (to make check checking more optimised)
