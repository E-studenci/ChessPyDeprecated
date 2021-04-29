from GameManagerPackage.Players.Player import Player


class Human(Player):
    """
    A class representing a human player
    Attributes:
        name: string
            name of the player (for leaderboards)
        color: bool
            - True if White
            - False if Black
        select_move_method: {} -> (start_pos, (end_pos, promotion_flag))
            a method used to select a move

    Methods:
        make_move:
            makes the selected move
        select_move:
            uses self.select_move_method to select a move
    """

    def __init__(self, name: str, color: bool, select_move_method):
        super().__init__(name, False, color)
        self.select_move_method = select_move_method

    def make_move(self, board, args, move="essa"):
        """
        Uses super().make_move() to make the move selected by self.select_move()

        :param board: the board on which the game is played
        :param args: args to be passed to self.select_move_method
        :param move: the move to be made
        """
        super().make_move(board, None, self.select_move(args))

    def select_move(self, args):
        """
        Uses self.select_move_method to select a move
        """
        return self.select_move_method(self.moves, args)
