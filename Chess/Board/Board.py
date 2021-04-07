import copy
from numba import njit
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
        self.board: list = [None] * 64
        self.legal_moves = {}
        self.attacked_fields = [False] * 64
        self.attacked_lines = []

        self.turn: bool = True
        self.fifty_move_rule = 0
        self.move_count = 0
        self.king_pos = {True: -1,
                         False: -1}

    def calculate_all_legal_moves(self, turn):
        """
        :param turn: current turn
        :param calculate_checks: should the moves that will leave the [turn] player's king in check be removed
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

    def calculate_all_legal_moves_multiprocess(self, turn):
        from multiprocessing import Process
        import multiprocessing
        all_legal_moves = {}
        processes = []
        queue = multiprocessing.SimpleQueue()
        for piece in self.board:
            if piece is not None:
                if piece.color == turn:
                    process = Process(target=piece.calculate_legal_moves, args=(self, queue, False))
                    process.start()
                    processes.append(process)
                    # all_legal_moves[piece.position] = piece.calculate_legal_moves(self, calculate_checks)
        self.legal_moves = all_legal_moves

        for p in processes:
            p.join()

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
            if not self.turn:
                self.move_count += 1
            self.board[start_pos].make_move(self, start_pos, move)
            self.turn = not self.turn
            for piece in self.board:
                if isinstance(piece, Pawn.Pawn):
                    if piece.color == self.turn:
                        piece.en_passant = False

    def calculate_all_attacked_fields(self):
        self.attacked_lines = []
        self.attacked_fields = [False] * 64
        for piece in self.board:
            if piece is not None:
                if piece.color != self.turn:
                    piece.calculate_attacked_fields(self)
