from Chess.Pieces import Bishop, King, Knight, Pawn, Piece, Queen, Rook
import PrintMatrixToConsole as PMC


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


if __name__ == "__main__":
    board = Board()
    board.board[9] = Bishop.Bishop(False, 9)
    board.board[48] = Pawn.Pawn(False, 48)
    board.board[36] = Queen.Queen(True, 36)
    # board.board[32] = Queen.Queen(False, 32)
    temp = King.King(False, 4)
    board.board[4] = temp
    board.board[0] = Rook.Rook(False, 0)
    board.board[7] = Rook.Rook(False, 7)

    board.board[26] = Pawn.Pawn(False, 26)
    board.board[25] = Pawn.Pawn(True, 25)
    board.board[18] = Pawn.Pawn(True, 18)
    board.board[11] = Pawn.Pawn(True, 11)
    board.board[33] = Pawn.Pawn(True, 33)

    # board.board[4].make_move(board, 4, 2)
    board.calculate_all_legal_moves()
    PMC.print_matrix_to_console(board.board)
    board.make_move(26, 17)
    PMC.print_matrix_to_console(board.board)
