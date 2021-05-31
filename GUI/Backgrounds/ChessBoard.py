import pygame

from GUI.Backgrounds.SpritesLoaded import SPRITE_DICTIONARY
from GUI.Constants import Colors

CHESS_BOARD = None
PIECES = None
SQUARE_SIZE = None


def initialize(screen, size):
    global SQUARE_SIZE
    SQUARE_SIZE = size[0] // 8
    board_colors = [pygame.Color(Colors.BOARD_LIGHT), pygame.Color(Colors.BOARD_DARK)]
    for i in range(8):
        for j in range(8):
            color = board_colors[(i + j) % 2]
            pygame.draw.rect(screen, color,
                             pygame.Rect(j * SQUARE_SIZE, i * SQUARE_SIZE, SQUARE_SIZE,
                                         SQUARE_SIZE))
    image_string = pygame.image.tostring(screen, 'RGBA', False)
    image = pygame.image.fromstring(image_string, size, 'RGBA')
    global CHESS_BOARD
    CHESS_BOARD = image


def draw_board(screen, bottom_left):
    global CHESS_BOARD
    if CHESS_BOARD is None:
        return False
    else:
        screen.blit(CHESS_BOARD, bottom_left)


def draw_pieces(screen, board, update):
    global SQUARE_SIZE
    global PIECES
    if update:
        for i in range(8):
            for j in range(8):
                index = (7 - i) * 8 + j
                if board.board[index] is not None:
                    current_piece = SPRITE_DICTIONARY[type(board.board[index]), board.board[index].color]
                    screen.blit(current_piece, (j * SQUARE_SIZE, i * SQUARE_SIZE))
        image_string = pygame.image.tostring(screen, 'RGBA', False)
        image = pygame.image.fromstring(image_string, screen.get_size(), 'RGBA')
        PIECES = image
    screen.blit(PIECES, (0, 0))
