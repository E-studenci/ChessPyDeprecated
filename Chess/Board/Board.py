from Chess.Pieces import Bishop, King, Knight, Pawn, Piece, Queen, Rook


class Board:
    def __init__(self):
        self.board: list = [None] * 64
        self.turn: bool = False
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


if __name__ == "__main__":
    board = Board()
    board.get_board()[9] = Bishop.Bishop(False, 9)
    board.get_board()[43] = Pawn.Pawn(False, 43)
    board.get_board()[36] = Queen.Queen(True, 36)
    board.get_board()[5] = King.King(False, 5)
    board.get_board()[0] = Rook.Rook(False, 0)

    print(board.get_board()[5].castle_queen_side)
    board.get_board()[0].make_move(board, 0, 1)
    print(board.get_board()[5].castle_queen_side)
    board.calculate_all_legal_moves()
