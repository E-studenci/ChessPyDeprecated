from enum import Enum


class GameStatus(Enum):
    ONGOING = 0
    CHECKMATE = 1
    STALEMATE = 2
    FIFTY_MOVES = 3
    THREEFOLD_REPETITION = 4
    INSUFFICIENT_MATERIAL = 5

