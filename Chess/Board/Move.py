import copy


class Move:
    """
    Class that stores information about a move for future action

    Attributes
        target_square: int
            an index of the square a piece was moved to
        piece_moved: Piece
            a deepcopy of moved piece
        piece_captured: Piece
            a deepcopy of captured piece (if there was one)
        castle_flags: Tuple(bool, bool)
            an information about possible castling moves for King
        king_castle: int
            an indicator if a move was castling
    """
    def __init__(self, target_square, piece_moved, piece_captured, castle_flags, king_castle):
        self.target_square = target_square
        self.piece_moved = copy.deepcopy(piece_moved)
        self.piece_captured = copy.deepcopy(piece_captured)
        self.castle_flags = castle_flags
        self.king_castle = king_castle
