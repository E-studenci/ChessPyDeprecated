from typing import List

from Chess.Pieces.Piece import Piece
from Chess.Pieces.King import King
from Chess.Pieces.Knight import Knight
#from Chess.Pieces.Bishop import Bishop
from Chess.Pieces import Bishop


class Board:


    def __init__(self):
        self.board: list = [None] * 64
        self.turn = False
        self.legal_moves = []



    def get_board(self):
        return self.board

    def calculate_all_legal_moves(self):
        all_legal_moves = {}
        for piece in self.board:
            if piece is not None:
                if piece.get_color() == self.turn:
                    all_legal_moves[piece] = piece.calculate_legal_moves(self.board)
        return all_legal_moves

if __name__ == '__main__':
    board = Board()
    board.board[9] = Bishop.Bishop(False, 9)
    board.board[27] = King(False, 27)
    board.calculate_all_legal_moves()
    pass
