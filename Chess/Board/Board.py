from Chess.Pieces import Bishop, King, Knight, Pawn, Piece, Queen, Rook


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
        self.turn: bool = True
        self.legal_moves = []
        self.fifty_move_rule = 0
        self.move_count = 0

    def calculate_all_legal_moves(self):
        """
        :return:
            calculates all legal moves for the current player
            and returns them in the form of a dictionary where
            keys represent pieces and values - all the squares, where the piece can move
        """
        all_legal_moves = {}
        for piece in self.board:
            if piece is not None:
                if piece.get_color() == self.turn:
                    all_legal_moves[piece] = piece.calculate_legal_moves(self.board)
        return all_legal_moves

    def take(self, pos):
        """
        :param pos: the position from which a piece should be removed
        :return: removes a piece at [pos]
        """
        # add some functionality here
        self.board[pos] = None

    def find_piece(self, piece_to_find):
        """
        :param piece_to_find:
        :return: returns the index of the first piece that matches the class and color of piece_to_find
        """
        index = 0
        for piece in self.board:
            if isinstance(piece, type(piece_to_find)) \
                    and piece.get_color() == piece_to_find.get_color():
                return index
            index += 1
        return -1

    def make_move(self, start_pos, end_pos):
        """
        :param start_pos: the starting pos of a piece to move
        :param end_pos: the destination of the move
        :return: moves the piece from [start_pos] to [end_pos]
                uses Board.take(end_pos) if the end_pos is occupied by opposing piece
        """
        if not isinstance(self.board[start_pos], type(None)):
            reset_en_passant_current_player = False
            temp_pawn = Pawn.Pawn(False, 11111)
            reset_en_passant_current_player = self.board[start_pos].make_move(self, start_pos, end_pos)
            for piece in self.board:
                if isinstance(piece, type(temp_pawn)):
                    if piece.color == self.board[end_pos].color:
                        if reset_en_passant_current_player:
                            piece.en_passant = False
                    else:
                        piece.en_passant = False


if __name__ == '__main__':
    board = Board()
    board.calculate_all_legal_moves()
    board.take()
    pawn = Pawn.Pawn()
