from Chess.Pieces import Bishop, King, Knight, Pawn, Piece, Queen, Rook


class Board:
    def __init__(self):
        self.board: list = [None] * 64
        self.turn: bool = False
        self.legal_moves = []
        self.fifty_move_rule = 0
        self.move_count = 0

    def calculate_all_legal_moves(self):
        all_legal_moves = {}
        for piece in self.board:
            if piece is not None:
                if piece.get_color() == self.turn:
                    all_legal_moves[piece] = piece.calculate_legal_moves(self.board)
        return all_legal_moves

    def take(self, pos):
        # add some functionality here
        self.board[pos] = None

    def find_piece(self, piece_to_find):
        index = 0
        for piece in self.board:
            if isinstance(piece, type(piece_to_find)) \
                    and piece.get_color() == piece_to_find.get_color():
                return index
            index += 1
        return -1

    def initialize_board(self, fen: str):
        from Chess.Board.Converters import FenDecoder as Fen
        self.board, self.turn, self.fifty_move_rule, self.move_count = Fen.initialize_list_from_FEN(fen)
