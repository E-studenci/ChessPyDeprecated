import copy

from Chess.Pieces import Bishop, King, Knight, Pawn, Piece, Queen, Rook, Constants


class Board:
    """
        Class representing our beautiful chessboard

        Attributes
            board: list
                a list of Pieces with 64 squares
            turn: bool
                a flag representing current turn
                                                - white - True
                                                - black - False
            legal_moves: list
                a list of all legal moves for the current player
            fifty_move_rule: int
                a counter representing the fifty move rule
            move_count: int
                a counter used for counting the number of turns since the start of a game

        methods
            calculate_all_legal_moves()
                calculates all legal moves for the current player
            take(pos)
                removes the piece at [pos] from the board, and does something
            find_piece(piece_to_find)
                Finds the index of the first piece that matches the class and color of piece_to_find
            make_move(start_pos, end_pos)
                moves a piece [start_pos] to [end_pos]
    """

    def __init__(self):
        self.king_pos = {True: -1,
                         False: -1}
        self.board: list = [None] * 64
        self.turn: bool = True
        self.legal_moves = []
        self.fifty_move_rule = 0
        self.move_count = 0

    def calculate_all_legal_moves(self, turn, calculate_checks=True):
        """
        :param turn: current turn
        :param calculate_checks: should the moves that will leave the [turn] player's king in check be removed
        :return:
            calculates all legal moves for the current player
            and returns them in the form of a dictionary where
            keys represent piece positions and values - all the squares, where the piece can move
        """
        all_legal_moves = {}
        for piece in self.board:
            if piece is not None:
                if piece.color == turn:
                    all_legal_moves[piece.position] = piece.calculate_legal_moves(self, calculate_checks)
        self.legal_moves = all_legal_moves
        return all_legal_moves

    def king_in_check_after_move(self, turn, start_pos, move):
        """
        :param turn: current turn
        :param start_pos: start_pos of the move to be checked
        :param move: (end_pos, promotion_type) the end pos of the move, and promotion flag
        :return: checks if the current player's king will be in check after the move
        """
        temp_board = copy.deepcopy(self)
        temp_board.make_move(start_pos, move)
        opposing_moves = temp_board.calculate_all_legal_moves(not turn, False)
        king_position = temp_board.king_pos[turn]
        for val in opposing_moves.values():
            if (king_position, 0) in val \
                    or (king_position, 1) in val:
                return True
        return False

    def king_in_check_after_move_ver_2_0(self, turn, start_pos, move):
        temp_board = copy.deepcopy(self)
        temp_board.make_move(start_pos, move)

        king_pos = temp_board.king_pos[turn]
        # check pawns
        direction = Pawn.direction_dictionary[temp_board.board[king_pos].color]
        if isinstance(temp_board.board[king_pos + 8 * direction + 1], Pawn.Pawn) \
                and not temp_board.board[king_pos + 8 * direction + 1].color == turn \
                or isinstance(temp_board.board[king_pos + 8 * direction - 1], Pawn.Pawn) \
                and not temp_board.board[king_pos + 8 * direction - 1].color == turn:
            return True

        # check knight
        def fun(pos):
            return isinstance(temp_board.board[pos], Knight.Knight)

        if self.helper(temp_board, [0] * 8 + [1] * 8, king_pos, turn, fun):
            return True

        # check rook and queen
        def fun2(pos):
            return isinstance(temp_board.board[pos], Rook.Rook) or isinstance(temp_board.board[pos], Queen.Queen)

        if self.helper(temp_board, [8, 8, 0, 8, 0, 0, 8, 0], king_pos, turn, fun2):
            return True

        # check bishop and queen
        def fun3(pos):
            return isinstance(temp_board.board[pos], Bishop.Bishop) or isinstance(temp_board.board[pos], Queen.Queen)

        if self.helper(temp_board, [0, 0, 8, 0, 8, 8, 0, 8], king_pos, turn, fun3):
            return True
        return False

    def helper(self, board, move_set, start_pos, turn, fun):
        for index in range(len(move_set)):
            interrupted = False
            temp = move_set[index]
            current_position = start_pos
            currently_calculated_position = 0
            while not interrupted \
                    and temp > 0:
                currently_calculated_position = current_position + Constants.DIRECTION_MATH[index]
                if (currently_calculated_position % Constants.BOARD_SIZE - current_position % Constants.BOARD_SIZE) == \
                        Constants.COLUMN_CHANGE[index] \
                        and 0 <= currently_calculated_position <= len(board.board) - 1:
                    current_position = currently_calculated_position
                    if not isinstance(board.board[currently_calculated_position], type(None)):
                        if fun(currently_calculated_position) \
                                and board.board[currently_calculated_position].color != turn:
                            return True
                        interrupted = True
                temp -= 1
        return False

    def take(self, pos):
        """
        :param pos: the position from which a piece should be removed
        :return: removes a piece at [pos]
        """
        # setting castling flags to false after taking a rook
        if isinstance(self.board[pos], type(Rook)):
            king_position = self.king_pos[self.turn]
            if pos == king_position + 3:
                self.board[king_position].castle_king_side = False
            elif pos == king_position - 4:
                self.board[king_position].castle_queen_side = False
        self.board[pos] = None

    def make_move(self, start_pos, move):
        """
        :param start_pos: the starting pos of a piece to move
        :param move: (end_pos, promotion_type) the end pos of the move, and promotion flag
        :return: moves the piece from [start_pos] to [end_pos]
                uses Board.take(end_pos) if the end_pos is occupied by opposing piece
        """
        if not isinstance(self.board[start_pos], type(None)):
            if not self.turn:
                self.move_count += 1
            self.board[start_pos].make_move(self, start_pos, move)
            self.turn = not self.turn
            for piece in self.board:
                if isinstance(piece, Pawn.Pawn):
                    if not piece.color == self.board[move[0]].color:
                        piece.en_passant = False
