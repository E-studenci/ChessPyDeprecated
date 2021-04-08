from GameManagerPackage.Players.Player import Player


class Human(Player):
    def __init__(self, name: str, color: bool, select_move_method):
        super().__init__(name, False, color)
        self.select_move_method = select_move_method

    def make_move(self, board):
        board.make_move(*self.select_move())

    def select_move(self):
        return self.select_move_method(self.moves)
