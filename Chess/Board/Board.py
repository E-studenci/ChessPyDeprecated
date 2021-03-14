from Chess.Pieces import Bishop, King, Knight, Pawn, Piece, Queen, Rook
import PrintMatrixToConsole as PMC


class Board:
    def __init__(self):
        self.board: list = [None] * 64
        self.turn: bool = True
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

    def make_move(self, start_pos, end_pos):
        if not isinstance(self.board[start_pos], type(None)):
            reset_en_passant_current_player = False
            temp_pawn = Pawn.Pawn(False, 11111)
            reset_en_passant_current_player = self.board[start_pos].make_move(self, start_pos, end_pos)
            print("AAA")
            for piece in self.board:
                if isinstance(piece, type(temp_pawn)):
                    if piece.color == self.board[end_pos].color:
                        if reset_en_passant_current_player:
                            piece.en_passant = False
                    else:
                        piece.en_passant = False
