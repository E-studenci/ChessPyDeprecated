import threading

from Chess.Board.Board import Board
from GameManagerPackage.GameStatus import GameStatus
from Chess.Board.Converters.FenEncoder import to_name_later
from Chess.Board.PrintMatrixToConsole import print_matrix_to_console


class GameManager:
    """
    Wanna play a game? Say no more, just use this class to create one of chess

    Attributes:
            player_one: GameManagerPackage.Players.Player
                the first player
            player_two: GameManagerPackage.Players.Player
                the second player
            fen: str
                optional, if you want to start a game from a certain position

    Methods:
            start_game:
                start the game_loop
            game_loop:
                handles turns and ending the game
            check game conditions:
                checks if the game should be ended
            get_all_possible_moves_for_current_player:
                gets legal moves for the player from self.board
            insufficient_material:
                helper method to check_game_ending_conditions
    """

    def __init__(self, player_one, player_two, fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        self.board: Board = Board()
        self.board.initialize_board(fen)
        self.player_one = player_one
        self.player_two = player_two
        self.current_player_is_bot = None
        self.history = []
        self.game_status = GameStatus.ONGOING

    def start_game(self, q1, q2, q3):
        """
        :return: starts the game
        """
        current_player = self.player_one if self.player_one.color == self.board.turn else self.player_two
        opposing_player = self.player_two if current_player == self.player_one else self.player_one
        t = threading.Thread(target=self.is_bot_notifier, args=(q3,))
        t.daemon = True
        t.start()
        self.game_loop(current_player, opposing_player, q1, q2)

    def game_loop(self, current, opposing, q1, q2):
        """
        :param current: the first player to move
        :param opposing: the opposing player
        :return:  handles turns and ends the game if necessary
        """
        current_player = current
        opposing_player = opposing
        self.current_player_is_bot = current_player.is_bot
        board = self.board
        current_player.moves = self.get_all_possible_moves_for_current_player()
        while self.game_status == GameStatus.ONGOING:
            current_player.make_move(board, (q1, q2))
            current_player, opposing_player = opposing_player, current_player
            self.current_player_is_bot = current_player.is_bot
            self.history.append(to_name_later(board.board, board.turn, board.fifty_move_rule, board.move_count))
            self.check_game_ending_conditions(current_player)
        print(self.game_status)

    def check_game_ending_conditions(self, player):
        """
        :param player: current player
        :return: returns:
                GameStatus.FIFTY_MOVES            : if the fifty move rule has been broken;
                GameStatus.CHECKMATE              : if the current player is in mate;
                GameStatus.THREEFOLD_REPETITION   : if the threefold repetition rule has been broken;
                GameStatus.INSUFFICIENT_MATERIAL  : if neither player can possibly mate the opposing player;
                GameStatus.ONGOING                : otherwise
        """
        player.moves = self.get_all_possible_moves_for_current_player()
        if self.board.fifty_move_rule == 50:
            self.game_status = GameStatus.FIFTY_MOVES
        elif sum(len(val) for val in player.moves.values()) == 0:
            if self.board.attacked_fields[self.board.king_pos[self.board.turn]]:
                self.game_status = GameStatus.CHECKMATE
            else:
                self.game_status = GameStatus.STALEMATE
        elif self.history.count(self.history[-1]) == 3:
            self.game_status = GameStatus.THREEFOLD_REPETITION
        elif self.insufficient_material():
            self.game_status = GameStatus.INSUFFICIENT_MATERIAL
        else:
            self.game_status = GameStatus.ONGOING

    def get_all_possible_moves_for_current_player(self):
        """
        :return: returns legal moves for the player from self.board
        """
        return self.board.calculate_all_legal_moves(self.board.turn)

    def insufficient_material(self):
        """
        :return: True if: KN vs K, or KB vs K, or K vs K;
                 False: otherwise
        """
        from Chess.Pieces import Knight, Bishop
        piece_count_white = 0
        piece_count_black = 0
        for piece in self.board.board:
            if not isinstance(piece, type(None)):
                if piece.color:
                    piece_count_white += 1
                else:
                    piece_count_black += 1
        if piece_count_white == 1 and piece_count_black == 1:
            return True
        if piece_count_white == 1 and piece_count_black == 2:
            if any(isinstance(x, Knight.Knight) or isinstance(x, Bishop.Bishop) for x in self.board.board):
                return True
        if piece_count_black == 1 and piece_count_white == 2:
            if any(isinstance(x, Knight.Knight) or isinstance(x, Bishop.Bishop) for x in self.board.board):
                return True
        return False

    def is_bot_notifier(self, q3):
        from GUI.Constants.Constant import MAX_FPS
        import time
        while self.game_status == GameStatus.ONGOING:
            q3.put((self.current_player_is_bot, None))
            q3.join()
        q3.put((-1, self.game_status))
