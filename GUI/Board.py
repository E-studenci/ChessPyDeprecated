from Chess.Pieces import Bishop, King, Knight, Pawn, Queen, Rook
from Chess.Board.Board import Board
from GUI.Constants import *
import pygame
import os

CHESSBOARD_WIDTH = 800
CHESSBOARD_HEIGHT = 800
SQUARE_SIZE = CHESSBOARD_WIDTH / 8

WHITE_PAWN = pygame.image.load(os.path.join("Sprites", 'Pieces', 'white_pawn.png'))
WHITE_KNIGHT = pygame.image.load(os.path.join('Sprites', 'Pieces', 'white_knight.png'))
WHITE_BISHOP = pygame.image.load(os.path.join('Sprites', 'Pieces', 'white_bishop.png'))
WHITE_ROOK = pygame.image.load(os.path.join('Sprites', 'Pieces', 'white_rook.png'))
WHITE_QUEEN = pygame.image.load(os.path.join('Sprites', 'Pieces', 'white_queen.png'))
WHITE_KING = pygame.image.load(os.path.join('Sprites', 'Pieces', 'white_king.png'))
BLACK_PAWN = pygame.image.load(os.path.join('Sprites', 'Pieces', 'black_pawn.png'))
BLACK_KNIGHT = pygame.image.load(os.path.join('Sprites', 'Pieces', 'black_knight.png'))
BLACK_BISHOP = pygame.image.load(os.path.join('Sprites', 'Pieces', 'black_bishop.png'))
BLACK_ROOK = pygame.image.load(os.path.join('Sprites', 'Pieces', 'black_rook.png'))
BLACK_QUEEN = pygame.image.load(os.path.join('Sprites', 'Pieces', 'black_queen.png'))
BLACK_KING = pygame.image.load(os.path.join('Sprites', 'Pieces', 'black_king.png'))

piece_dictionary = {(Pawn.Pawn, False): BLACK_PAWN, (Pawn.Pawn, True): WHITE_PAWN,
                    (Knight.Knight, False): BLACK_KNIGHT, (Knight.Knight, True): WHITE_KNIGHT,
                    (Bishop.Bishop, False): BLACK_BISHOP, (Bishop.Bishop, True): WHITE_BISHOP,
                    (Rook.Rook, False): BLACK_ROOK, (Rook.Rook, True): WHITE_ROOK,
                    (Queen.Queen, False): BLACK_QUEEN, (Queen.Queen, True): WHITE_QUEEN,
                    (King.King, False): BLACK_KING, (King.King, True): WHITE_KING,
                    }

COLOR_F0D9B5 = (240, 217, 181)
COLOR_946F51 = (148, 111, 81)


def initialize_board(screen, clock):
    pygame.display.init()
    screen.fill(pygame.Color("white"))
    running_loop(screen, clock)


def running_loop(screen, clock):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        draw(screen)
        clock.tick(MAX_FPS)
        pygame.display.flip()


def draw(screen):
    draw_board(screen)
    draw_pieces(screen)


def draw_pieces(screen):
    # TEMP
    board = Board()
    board.initialize_board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    chess_board = board.board
    # TEMP
    piece_size = (int(SQUARE_SIZE), int(SQUARE_SIZE))
    for i in range(8):
        for j in range(8):
            index = (7 - i) * 8 + j
            if chess_board[index] is not None:
                current_piece = piece_dictionary[type(chess_board[index]), chess_board[index].color]
                current_image = pygame.transform.scale(current_piece, piece_size)
                screen.blit(current_image, (j * SQUARE_SIZE, i * SQUARE_SIZE))


def draw_board(screen):
    board_colors = [pygame.Color(COLOR_F0D9B5), pygame.Color(COLOR_946F51)]
    for i in range(8):
        for j in range(8):
            color = board_colors[(i + j) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(j * SQUARE_SIZE, i * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
