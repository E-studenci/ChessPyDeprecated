from Chess.Pieces.Piece import Piece
from Chess.Pieces import Constants
from Chess.Pieces.King import King


class Knight(Piece):
    """
        Sub class of Piece, it represents the bishop piece

        Nothing special here
    """

    def __init__(self, color: bool, position: int):
        super().__init__(color, position)
        self.move_set = [1, 1, 1, 1, 1, 1, 1, 1]

    def calculate_attacked_fields(self, board):
        """
        :param board: Chess.Board.Board, the board on which the knight is standing
        :return: returns the list of all the fields attacked by a knight
        """
        for index in range(len(self.move_set)):
            maximum_move_length = self.move_set[index]
            current_position = self.position
            while maximum_move_length > 0:
                currently_calculated_position = current_position + Constants.KNIGHT_DIRECTION_MATH[index]
                if currently_calculated_position % Constants.BOARD_SIZE - current_position % Constants.BOARD_SIZE == \
                   Constants.KNIGHT_COLUMN_CHANGE[index] \
                   and 0 <= currently_calculated_position <= len(board.board) - 1:
                    board.attacked_fields[currently_calculated_position] = True
                    if isinstance(board.board[currently_calculated_position], King):
                        if board.board[currently_calculated_position].color != self.color:
                            board.attacked_lines.append({self.position})
                maximum_move_length -= 1
