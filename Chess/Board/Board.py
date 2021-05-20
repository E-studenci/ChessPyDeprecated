from Chess.Pieces import Bishop, King, Knight, Pawn, Queen, Rook, Constants
from Chess.Board.Move import Move


class Board:
    """
        Class representing our beautiful chessboard

        Attributes
            board: list
                a list of Pieces with 64 squares
            legal_moves: dict
                a dict {piece: list} where piece is an object Piece
                and list is a list of all legal moves for that piece
            attacked_fields: list
                a list of all fields that the opposing player attacks
            attacked_lines: list
                a list of all lines that the opposing player attacks
            turn: bool
                a flag representing current turn
                                                - white - True
                                                - black - False
            fifty_move_rule: int
                a counter representing the fifty move rule
            move_count: int
                a counter used for counting the number of turns since the start of a game
            move_log: list
                a list of all moves that were made in the game
            king_pos: {True: int, False: int}
                a dictionary that keeps the positions of both kings

        methods
            calculate_all_legal_moves()
                calculates all legal moves for the current player
            take(pos)
                removes the piece at [pos] from the board, and does something
            make_move(start_pos, end_pos)
                moves a piece [start_pos] to [end_pos]
            unmake_move()
                unmake the previous move
            calculate_all_attacked_files()
                calculates all files the the opposing player attacks
            initialize_board(fen)
                initializes chess_board from the given string
    """

    def __init__(self):
        self.board: list = [None] * 64
        self.legal_moves = {}
        self.attacked_fields = [False] * 64
        self.attacked_lines = []

        self.turn: bool = True
        self.fifty_move_rule = 0
        self.move_count = 0
        self.move_log = []
        self.king_pos = {True: -1,
                         False: -1}

    def calculate_all_legal_moves(self):
        """
        :return:
            calculates all legal moves for the current player
            and returns them in the form of a dictionary where
            keys represent piece positions and values - all the squares, where the piece can move
        """
        self.calculate_all_attacked_fields()
        all_legal_moves = {}
        for piece in self.board:
            if piece is not None:
                if piece.color == self.turn:
                    all_legal_moves[piece.position] = piece.calculate_legal_moves(self)
        self.legal_moves = all_legal_moves
        return all_legal_moves

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
            king_castle = 0
            if isinstance(self.board[start_pos], King.King):
                if move[0] - start_pos == 2:
                    king_castle = 1
                elif move[0] - start_pos == -2:
                    king_castle = -1

            attacked_piece = move[0]
            if isinstance(self.board[start_pos], Pawn.Pawn) \
                    and (abs(start_pos - move[0]) == 7 or abs(start_pos - move[0]) == 9) \
                    and isinstance(self.board[move[0]], type(None)):
                if self.turn:
                    attacked_piece -= 8
                else:
                    attacked_piece += 8

            king = self.board[self.king_pos[self.turn]]

            self.move_log.append(Move(move[0], self.board[start_pos], self.board[attacked_piece],
                                      (king.castle_king_side, king.castle_queen_side), king_castle))
            if not self.turn:
                self.move_count += 1
            self.board[start_pos].make_move(self, start_pos, move)
            self.turn = not self.turn
            for piece in self.board:
                if isinstance(piece, Pawn.Pawn):
                    if piece.color == self.turn:
                        piece.en_passant = False

    def unmake_move(self):
        """
        :return: looks at the move_log and reverses the last move that was made
        """
        if len(self.move_log) > 0:
            move = self.move_log.pop()
            self.board[move.target_square] = None
            self.board[move.piece_moved.position] = move.piece_moved
            if move.piece_captured is not None:
                self.board[move.piece_captured.position] = move.piece_captured

            if move.king_castle == 1:
                rook = self.board[move.target_square - 1]
                self.board[move.piece_moved.position + 3] = rook
                self.board[move.target_square - 1] = None
                rook.position = move.piece_moved.position + 3
            if move.king_castle == -1:
                rook = self.board[move.target_square + 1]
                self.board[move.piece_moved.position - 4] = rook
                self.board[move.target_square + 1] = None
                rook.position = move.piece_moved.position - 4

            self.turn = not self.turn
            if isinstance(move.piece_moved, King.King):
                self.king_pos[move.piece_moved.color] = move.piece_moved.position

            king = self.board[self.king_pos[move.piece_moved.color]]
            king.castle_king_side = move.castle_flags[0]
            king.castle_queen_side = move.castle_flags[1]

    def calculate_all_attacked_fields(self):
        """
        :return:
            calculates all attacked fields for the opposing player
            and all of the pin lines for the current player and saves
            them into class attributes
        """
        self.attacked_lines = []
        self.attacked_fields = [False] * 64
        for piece in self.board:
            if piece is not None:
                if piece.color != self.turn:
                    piece.calculate_attacked_fields(self)

    def initialize_board(self, fen):
        """
        :param fen: a string that contains all necessary to initialize a chess board
        :return: initializes chess_board from the given string
        """
        from Chess.Board.Converters.FenDecoder import initialize_list_from_FEN
        x1, x2, x3, x4, x5 = initialize_list_from_FEN(fen)
        if x1 is None:
            return False
        self.board, self.turn, self.fifty_move_rule, self.move_count, self.king_pos = x1, x2, x3, x4, x5
        return True
