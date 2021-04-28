import os
import threading
import time

from Chess.Board.Board import Board
from GameManagerPackage.GameStatus import GameStatus
from Chess.Board.Converters.FenEncoder import to_name_later, parse_board


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

    def __init__(self, player_one, player_two, fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
                 leaderboards="Leaderboards.txt"):
        self.board: Board = Board()
        self.board.initialize_board(fen)
        self.player_one = player_one
        self.player_two = player_two
        self.leaderboards = leaderboards
        self.current_player_is_bot = None
        self.history = []
        self.game_status: GameStatus = GameStatus.ONGOING
        self.kill = False
        self.pause = False

    def start_game(self, q1, q2, q3):
        """
        Starts the game

        :param q1: player will get the selected move from this queue
        :param q2: player will put legal moves into this queue
        :param q3: the current player's is_bot flag and current game status will be put here
        """
        current_player = self.player_one if self.player_one.color == self.board.turn else self.player_two
        opposing_player = self.player_two if current_player == self.player_one else self.player_one
        t = threading.Thread(target=self.__is_bot_notifier, args=(q3, self.board))
        t.daemon = True
        t.start()
        self.__game_loop(current_player, opposing_player, q1, q2)

    def __game_loop(self, current, opposing, q1, q2):
        """
        Handles turns and ends the game if necessary

        :param current: the first player to move
        :param opposing: the opposing player
        :param q1 player will get the selected move from this queue
        :param q2 player will put legal moves into this queue
        """
        current_player = current
        opposing_player = opposing
        self.current_player_is_bot = current_player.is_bot
        board = self.board
        current_player.moves = self.get_all_possible_moves_for_current_player()
        while self.game_status == GameStatus.ONGOING and not self.kill:
            while self.pause:
                time.sleep(1)
            current_player.make_move(board, (q1, q2))
            current_player, opposing_player = opposing_player, current_player
            self.current_player_is_bot = current_player.is_bot
            self.history.append(parse_board(board.board))
            self.__check_game_ending_conditions(current_player)
        self.__update_leaderboards(self.leaderboards, current_player, opposing_player)

    def __check_game_ending_conditions(self, player):
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

    def __is_bot_notifier(self, queue, board):
        """
        Puts current player's is_bot flag, current game status and if a move(take) occurred into the queue

        :param board: the board, on which the game is played
        :param queue: the queue to use
        """
        fst = (parse_board(board.board), self.__count_pieces())
        while True:
            snd = (parse_board(board.board), self.__count_pieces())
            made_move = True if fst[0] != snd[0] else False
            taken = True if fst[1] - snd[1] != 0 else False
            queue.put((self.current_player_is_bot, self.game_status, (made_move, taken)))
            fst = (parse_board(board.board), self.__count_pieces())
            queue.join()

    def __count_pieces(self):
        pieces = 0
        for piece in self.board.board:
            if piece is not None:
                pieces += 1
        return pieces

    def __update_leaderboards(self, file_path, current_player, opposing_player):
        """
        Appends the result of the game to the file

        :param file_path: the path to leaderboards
        :param current_player:
        :param opposing_player:
        :returns False if file not found
        """
        if os.path.isfile(file_path):
            altered_lines = []
            p_1_name = current_player.name
            p_2_name = opposing_player.name
            if p_1_name is not None and p_2_name is not None:
                with open(file_path) as f:
                    lines = f.read().splitlines()
                    found_match = False
                    for line in lines:
                        columns = line.split(" : ")
                        if (columns[0] == p_1_name and columns[1] == p_2_name) \
                                or (columns[1] == p_1_name and columns[0] == p_2_name):
                            if columns[1] == p_1_name and columns[0] == p_2_name:
                                columns[2], columns[3] = columns[3], columns[2]
                            updated_p_1_score = columns[2]
                            updated_p_2_score = int(columns[3]) + (
                                1 if (self.game_status == GameStatus.CHECKMATE) else 0)
                            updated_draws = int(columns[4]) + (1 if (self.game_status != GameStatus.CHECKMATE) else 0)
                            altered_lines.append(f"{p_1_name} : "
                                                 f"{p_2_name} : "
                                                 f"{updated_p_1_score} : "
                                                 f"{updated_p_2_score} : "
                                                 f"{updated_draws}")
                            found_match = True
                        else:
                            altered_lines.append(line)
                    if not found_match:
                        updated_p_2_score = 1 if (self.game_status == GameStatus.CHECKMATE) else 0
                        updated_draws = 1 if (self.game_status != GameStatus.CHECKMATE) else 0
                        altered_lines.append(f"{current_player.name} : "
                                             f"{opposing_player.name} : "
                                             f"0 : "
                                             f"{updated_p_2_score} : "
                                             f"{updated_draws}")
                with open(file_path, "w") as f:
                    f.write('\n'.join(altered_lines) + '\n')
                return True
        return False

