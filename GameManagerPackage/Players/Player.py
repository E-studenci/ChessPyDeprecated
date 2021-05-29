import threading
import time
from datetime import datetime


class Player:
    """
    An abstract class representing a player
    Attributes:
        name: string
            name of the player (for leaderboards)
        color: bool
            - True if White
            - False if Black
        is_bot: bool

    Methods:
        make_move: makes the selected move
        select_move:
    """

    def __init__(self, name: str, is_bot: bool, color: bool, select_move_method, delay=1, player_clock=None):
        self.name: str = name if name != "" else None
        self.is_bot: bool = is_bot
        self.color: bool = color
        self.moves = {}
        self.delay = delay
        self.select_move_method = select_move_method
        self.clock = player_clock
        if self.clock is not None:
            t = threading.Thread(target=self.clock.start)
            t.daemon = True
            t.start()

    def make_move(self, board, args):
        """
        Makes the move on the board

        :param board: the board on which the game is played
        :param move: the move to be made
        """
        if self.clock is not None:
            self.clock.pause = False
        move = self.select_move((board, self.moves, args))
        board.make_move(*move)
        if self.clock is not None:
            self.clock.pause = True

    def select_move(self, args):
        start_time = datetime.now().microsecond
        start_pos, move = self.select_move_method(*args)
        if self.is_bot:
            elapsed = datetime.now().microsecond - start_time
            if elapsed < self.delay * 1000000:
                to_sleep = (self.delay * 1000000 - elapsed) / 1000000
                time.sleep(to_sleep)
        return start_pos, move
