import random

from Chess.GameManager.Players.Player import Player


class BotRandom(Player):
    def __init__(self, name: str, color: bool):
        super().__init__(name, True, color)

    def make_move(self, board):
        board.make_move(*self.select_move())

    def select_move(self):
        start_pos = random.choice(list(self.moves.keys()))
        while not self.moves[start_pos]:
            start_pos = random.choice(list(self.moves.keys()))
        return (start_pos, random.choice(self.moves[start_pos]))
