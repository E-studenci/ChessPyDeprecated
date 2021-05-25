import time
from datetime import datetime

from GameManagerPackage.Players.Player import Player


class Bot(Player):
    """
    A class representing a bot making random moves
    Attributes:
        name: string
            name of the player (for leaderboards)
        color: bool
            - True if White
            - False if Black
        delay: int
            seconds between moves

    Methods:
        make_move:
            makes the selected move
        select_move:
            uses sheer luck to select a move
    """

    def __init__(self, name: str, color: bool, select_move_method, delay=1):
        super().__init__(name, True, color)
        self.delay = delay
        self.select_move_method = select_move_method

    def make_move(self, board, args, move="essa"):
        """
        Uses super().make_move() to make the move selected by self.select_move()

        :param board: the board on which the game is played
        :param args: unused
        :param move: the move to be made
        """
        super().make_move(board, None, self.select_move((board, board.calculate_all_legal_moves())))

    def select_move(self, args):
        """
        Selects a random legal move
        """
        start_time = datetime.now().microsecond
        start_pos, move = self.select_move_method(*args)
        elapsed = datetime.now().microsecond - start_time
        if elapsed < self.delay * 1000000:
            to_sleep = (self.delay * 1000000 - elapsed) / 1000000
            time.sleep(to_sleep)
        return start_pos, move
