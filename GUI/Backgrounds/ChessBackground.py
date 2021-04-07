from Chess.Pieces import Bishop, King, Knight, Pawn, Queen, Rook
from Chess.Board.Board import Board
from GUI.Constants import *
import pygame
import os
from PIL import Image, ImageFilter

CHESSBOARD_WIDTH = 800
CHESSBOARD_HEIGHT = 800
SQUARE_SIZE = CHESSBOARD_WIDTH / 8

CHESSBOARD_SIZE = (800, 800)
SQUARE_SIZE_2 = (CHESSBOARD_SIZE[0] // 8, CHESSBOARD_SIZE[1] // 8)
COLOR_F0D9B5 = (240, 217, 181)
COLOR_946F51 = (148, 111, 81)

WHITE_PAWN = pygame.image.load(os.path.join('..', "Sprites", 'Pieces', 'white_pawn.png'))
WHITE_KNIGHT = pygame.image.load(os.path.join('..', 'Sprites', 'Pieces', 'white_knight.png'))
WHITE_BISHOP = pygame.image.load(os.path.join('..', 'Sprites', 'Pieces', 'white_bishop.png'))
WHITE_ROOK = pygame.image.load(os.path.join('..', 'Sprites', 'Pieces', 'white_rook.png'))
WHITE_QUEEN = pygame.image.load(os.path.join('..', 'Sprites', 'Pieces', 'white_queen.png'))
WHITE_KING = pygame.image.load(os.path.join('..', 'Sprites', 'Pieces', 'white_king.png'))
BLACK_PAWN = pygame.image.load(os.path.join('..', 'Sprites', 'Pieces', 'black_pawn.png'))
BLACK_KNIGHT = pygame.image.load(os.path.join('..', 'Sprites', 'Pieces', 'black_knight.png'))
BLACK_BISHOP = pygame.image.load(os.path.join('..', 'Sprites', 'Pieces', 'black_bishop.png'))
BLACK_ROOK = pygame.image.load(os.path.join('..', 'Sprites', 'Pieces', 'black_rook.png'))
BLACK_QUEEN = pygame.image.load(os.path.join('..', 'Sprites', 'Pieces', 'black_queen.png'))
BLACK_KING = pygame.image.load(os.path.join('..', 'Sprites', 'Pieces', 'black_king.png'))

piece_dictionary = {(Pawn.Pawn, False): BLACK_PAWN, (Pawn.Pawn, True): WHITE_PAWN,
                    (Knight.Knight, False): BLACK_KNIGHT, (Knight.Knight, True): WHITE_KNIGHT,
                    (Bishop.Bishop, False): BLACK_BISHOP, (Bishop.Bishop, True): WHITE_BISHOP,
                    (Rook.Rook, False): BLACK_ROOK, (Rook.Rook, True): WHITE_ROOK,
                    (Queen.Queen, False): BLACK_QUEEN, (Queen.Queen, True): WHITE_QUEEN,
                    (King.King, False): BLACK_KING, (King.King, True): WHITE_KING,
                    }


class ChessBackground:
    def __init__(self, size, fen_init):
        self.size = size
        self.square_size = (size[0]//2, size[1]//2)
        self.board = Board()
        self.board.initialize_board(fen_init)
        self.image_string = None

    def update(self, screen):
        self.draw_board(screen)
        self.draw_pieces(screen)
        ss = b'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'
        import codecs
        self.image_string = codecs.decode(codecs.decode(ss, "base64"), "zlib")
        # self.image_string = pygame.image.tostring(screen, 'RGB', True)

    def render(self, screen):
        pil_blurred = Image.frombytes("RGBA", self.size, bytes(self.image_string)).filter(ImageFilter.GaussianBlur(radius=3))
        other = pygame.image.fromstring(pil_blurred.tobytes("raw", "RGBA"), self.size, 'RGBA')
        screen.blit(other, (800,800))

    def draw_pieces(self, screen):
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

    def draw_board(self, screen):
        board_colors = [pygame.Color(COLOR_F0D9B5), pygame.Color(COLOR_946F51)]
        for i in range(8):
            for j in range(8):
                color = board_colors[(i + j) % 2]
                pygame.draw.rect(screen, color, pygame.Rect(j * SQUARE_SIZE, i * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
