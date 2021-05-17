import time
import random

from GameManagerPackage.Players.Player import Player


class BotRandom(Player):
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

    def __init__(self, name: str, color: bool, delay=1):
        super().__init__(name, True, color)
        self.delay = delay

    def make_move(self, board, args, move="essa"):
        """
        Uses super().make_move() to make the move selected by self.select_move()

        :param board: the board on which the game is played
        :param args: unused
        :param move: the move to be made
        """
        super().make_move(board, None, self.select_move(args))

    def select_move(self, args):
        """
        Selects a random legal move
        """
        start_pos = random.choice(list(self.moves.keys()))
        while not self.moves[start_pos]:
            start_pos = random.choice(list(self.moves.keys()))
        time.sleep(self.delay)
        return start_pos, random.choice(self.moves[start_pos])
