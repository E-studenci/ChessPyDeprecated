from Chess.Pieces.Piece import Piece


class Bishop(Piece):
    """
        Sub class of Piece, it represents the bishop piece

        Nothing special here
    """

    def __init__(self, color: bool, position: int):
        super().__init__(color, position)
        self.move_set = [0,0,8,0,8,8,0,8]
