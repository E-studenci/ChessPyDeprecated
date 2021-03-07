from abc import ABC, abstractmethod

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

    def calculate_legal_moves(self, board):
        legal_moves = []
        for index in range (len(possible_moves)):
            temp = self.possible_moves[index]
            current_position = self.position
            currently_calculated_position = 0
            current_column = self.position%8
            currently_calculated_column = 0
            while temp > 0 \
                    & currently_calculated_position >= 0 \
                    & currently_calculated_position <= 63 \
                    & (board.get_board()[current_position] is not None & current_position != self.position ):
                currently_calculated_position = current_position + Constants.DIRECTION_MATH[index]
                currently_calculated_column = currently_calculated_position % 8
                if (currently_calculated_column - current_column) == Constants.COLUMN_CHANGE[index]:
                    # check if king will be in check
                    # if not:
                    legal_moves.append(currently_calculated_position)
                    current_position = currently_calculated_position
                    temp -= 1
        return legal_moves

