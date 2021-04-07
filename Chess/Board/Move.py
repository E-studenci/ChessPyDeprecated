import copy


class Move:
    def __init__(self, target_square, piece_moved, piece_captured):
        self.target_square = target_square
        self.piece_moved = copy.deepcopy(piece_moved)
        self.piece_captured = copy.deepcopy(piece_captured)
