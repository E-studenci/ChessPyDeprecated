from Chess.Pieces import Bishop, King, Knight, Pawn, Piece, Queen, Rook


class Board:
    def __init__(self):
        self.board: list
        self.turn: bool
        self.legal_moves = []
        self.fifty_move_rule = 0
        self.move_count = 0
    
    def get_board(self):
        return self.board

    def calculate_all_legal_moves(self):
        all_legal_moves = {}
        for piece in self.board:
            if piece is not None:
                if piece.get_color() == self.turn:
                    all_legal_moves[piece] = piece.calculate_legal_moves(self.board)
        return all_legal_moves