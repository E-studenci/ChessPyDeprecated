from Chess.Board.Board import Board
from GUI.Backgrounds import ChessBoard
import pygame
from PIL import Image, ImageFilter
import random
from GUI.Backgrounds.Sprites_Loaded import SPRITE_DICTIONARY

COLOR_F0D9B5 = (240, 217, 181)
COLOR_946F51 = (148, 111, 81)

FRAMES_BETWEEN_MOVES = 100


class ChessBackground:
    """
            Class used to create a background with a blurred chess game

            Attributes
                size: (int,int)
                    size of the whole chess board
                fen_init: string
                    the initial position of the game in the background
            methods
                update(screen)
                    called automatically by render every FRAMES_BETWEEN_MOVES frames
                    makes a move, and saves the position to be rendered
                render(screen)
                    renders the saved position
                draw_pieces(screen)
                    draws pieces on the screen
                draw_board(screen)
                    draws board on the screen
        """

    def __init__(self, size, fen_init="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        self.size = size
        self.square_size = size[0] // 8
        self.board = Board()
        self.board.initialize_board(fen_init)
        self.image = None
        self.board_image = None
        self.counter: int = 0
        self.pause = False

    def update(self, screen):
        """
        :param screen: the screen on which the board is to be rendered
        :return: makes a move and updates self.image
        """
        moves = self.board.calculate_all_legal_moves(self.board.turn)
        start_pos = random.choice(list(moves.keys()))
        while not moves[start_pos]:
            start_pos = random.choice(list(moves.keys()))
        move = random.choice(moves[start_pos])
        self.board.make_move(start_pos, move)
        screen.blit(ChessBoard.CHESS_BOARD, (0, 0))
        ChessBoard.draw_pieces(screen, self.board, True)
        image_string = pygame.image.tostring(screen, 'RGBA', False)
        image_blurred = Image.frombytes("RGBA", self.size, bytes(image_string)). \
            filter(ImageFilter.GaussianBlur(radius=3))
        self.image = pygame.image.fromstring(image_blurred.tobytes("raw", 'RGBA'), self.size, 'RGBA')

    def render(self, screen):
        """
        :param screen: the screen on which the board is to be rendered
        :return: renders self.image, and updates it every FRAMES_BETWEEN_MOVES frames
        """
        if not self.pause:
            if self.counter % FRAMES_BETWEEN_MOVES == 0:
                self.update(screen)
                self.counter = 0
            screen.blit(self.image, (0, 0))
            self.counter += 1
