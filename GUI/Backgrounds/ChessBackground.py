import threading
from queue import Queue

from GUI.Backgrounds import ChessBoard
import pygame
from PIL import Image, ImageFilter
from GameManagerPackage.GameManager import GameManager

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

    def __init__(self, size, bot_1, bot_2, bot_delay,
                 fen_init="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        self.size = size
        self.square_size = size[0] // 8
        self.image = None
        self.board_image = None
        self.__pause = False
        p_1 = bot_1("", True, delay=bot_delay)
        p_2 = bot_2("", False, delay=bot_delay)
        self.__q3 = Queue()
        self.game = GameManager(p_1, p_2)

        t = threading.Thread(target=self.game.start_game, args=(Queue(), Queue(), self.__q3))
        t.daemon = True
        t.start()

    def __update(self, screen):
        """
        Makes a move and updates self.image

        :param screen: the screen on which the board is to be rendered
        """
        ChessBoard.draw_board(screen, (0, 0))
        ChessBoard.draw_pieces(screen, self.game.board, True)
        image_string = pygame.image.tostring(screen, 'RGBA', False)
        image_blurred = Image.frombytes("RGBA", self.size, bytes(image_string)). \
            filter(ImageFilter.GaussianBlur(radius=3))
        self.image = pygame.image.fromstring(image_blurred.tobytes("raw", 'RGBA'), self.size, 'RGBA')

    def render(self, screen):
        """
        Renders self.image, and updates it every FRAMES_BETWEEN_MOVES frames

        :param screen: the screen on which the board is to be rendered
        """
        if self.image is None:
            self.__update(screen)
        if not self.pause:
            temp = self.__q3.get()
            if temp[2][0]:
                self.__update(screen)
            screen.blit(self.image, (0, 0))
            self.__q3.task_done()

    @property
    def pause(self):
        return self.__pause

    @pause.setter
    def pause(self, pause):
        self.__pause = pause
        self.game.pause = pause
