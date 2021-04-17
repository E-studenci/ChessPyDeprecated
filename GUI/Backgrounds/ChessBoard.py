import pygame

from GUI.Backgrounds.Sprites_Loaded import SPRITE_DICTIONARY

COLOR_F0D9B5 = (240, 217, 181)
COLOR_946F51 = (148, 111, 81)

CHESS_BOARD = None
PIECES = None
SQUARE_SIZE = None


def initialize(screen, size):
    global SQUARE_SIZE
    SQUARE_SIZE = size[0] // 8
    board_colors = [pygame.Color(COLOR_F0D9B5), pygame.Color(COLOR_946F51)]
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
        size = (SQUARE_SIZE * 8, SQUARE_SIZE * 8)
        image_string = pygame.image.tostring(screen, 'RGBA', False)
        image = pygame.image.fromstring(image_string, size, 'RGBA')
        PIECES = image
    screen.blit(PIECES, (0, 0))
