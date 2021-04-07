from Chess.GameManager.GameStatus import GameStatus
from Chess.Board.Board import Board
from Chess.Board.Converters.FenEncoder import to_name_later
from Chess.Board.PrintMatrixToConsole import print_matrix_to_console


class GameManager:
    def __init__(self, player_one, player_two, fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        self.board: Board = Board()
        self.board.initialize_board(fen)
        self.player_one = player_one
        self.player_two = player_two
        self.history = []
        self.game_status = GameStatus.ONGOING

    def start_game(self):
        current_player = self.player_one if self.player_one.color == self.board.turn else self.player_two
        opposing_player = self.player_two if current_player == self.player_one else self.player_one
        self.game_loop(current_player, opposing_player)

    def game_loop(self, current, opposing):
        board = self.board
        current_player = current
        opposing_player = opposing
        current_player.moves = self.get_all_possible_moves_for_current_player()
        while self.game_status == GameStatus.ONGOING:
            current_player.make_move(board)
            current_player, opposing_player = opposing_player, current_player
            self.history.append(to_name_later(board.board, board.turn, board.fifty_move_rule, board.move_count))
            self.check_game_ending_conditions(current_player)
            print_matrix_to_console(board.board)
        print(self.game_status)

    def check_game_ending_conditions(self, player):
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
        return self.board.calculate_all_legal_moves()

    def insufficient_material(self):
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


if __name__ == '__main__':
    from Chess.GameManager.Players.BotRandom import BotRandom

    game = GameManager(BotRandom("alexei", True), BotRandom("Oleg", False))
    game.start_game()
