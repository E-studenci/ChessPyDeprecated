from abc import ABC, abstractmethod


class Player(ABC):
    @abstractmethod
    def __init__(self, name: str, is_bot: bool, color: bool):
        self.name: str = name
        self.is_bot: bool = is_bot
        self.color: bool = color
        self.moves = {}

    def make_move(self, board):
        pass

    def select_move(self):
        pass
