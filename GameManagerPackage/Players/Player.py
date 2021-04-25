from abc import ABC, abstractmethod


class Player(ABC):
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

    @abstractmethod
    def __init__(self, name: str, is_bot: bool, color: bool):
        self.name: str = name if name != "" else None
        self.is_bot: bool = is_bot
        self.color: bool = color
        self.moves = {}

    def make_move(self, board, args, move):
        """
        :param board: the board on which the game is played
        :param move: the move to be made
        :return: makes the move on the board
        """
        board.make_move(*move)

    def select_move(self, args):
        pass
