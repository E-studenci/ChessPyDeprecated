from Chess.GameManager.Player import Player
from Chess.Board.Board import Board


class GameManager:
    starting_position: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    def __init__(self):
        self.player_one: Player is None
        self.player_two: Player is None
        self.board: Board = Board()

    def regular_new_game(self) -> bool:
        return self.board.initialize_board(self.starting_position)

    def add_players(self, name_one: str, is_bot_one: bool, color_one: bool,
                    name_two: str, is_bot_two: bool, color_two: bool):
        self.player_one = Player(name_one, is_bot_one, color_one)
        self.player_two = Player(name_two, is_bot_two, color_two)

    def get_possible_moves_from_piece(self, piece):
        # TODO Pobieranie ruchow dla poszczegulnych figur, jeszcze nie wiem czy tu czy w Player
        pass

    def get_all_possible_moves_for_player(self):
        # TODO Podobnie jak wyżej tylko dla wszystkich figur gracza
        pass

    def get_chess_board(self):
        return self.board.board
