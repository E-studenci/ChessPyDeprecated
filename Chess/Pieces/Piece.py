from abc import ABC, abstractmethod


class Piece(ABC):

    @abstractmethod
    def __init__(self, color: bool, position: int):
        self.color: bool = color
        self.position: int = position
        self.pinned: bool = False
        self.move_set: list = []
        self.possible_moves: list = []

