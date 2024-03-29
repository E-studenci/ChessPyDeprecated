import os
import multiprocessing

if multiprocessing.current_process().name == 'MainProcess':
    import pygame
from Chess.Pieces import Bishop, King, Knight, Pawn, Queen, Rook
from PIL import Image, ImageFilter

from GUI.Constants import Display
from Paths import FOLDER_PATHS

SPRITE_DICTIONARY = {(Pawn.Pawn, False):     None, (Pawn.Pawn, True): None,
                     (Knight.Knight, False): None, (Knight.Knight, True): None,
                     (Bishop.Bishop, False): None, (Bishop.Bishop, True): None,
                     (Rook.Rook, False):     None, (Rook.Rook, True): None,
                     (Queen.Queen, False):   None, (Queen.Queen, True): None,
                     (King.King, False):     None, (King.King, True): None,
                     }

LOGO = [None, None]

def initialize(size):
    """
    Initializes SPRITE_DICTIONARY

    :param size: the final size of each piece sprite
    """
    paths = {(Pawn.Pawn, False):     'black_pawn.png', (Pawn.Pawn, True): 'white_pawn.png',
             (Knight.Knight, False): 'black_knight.png', (Knight.Knight, True): 'white_knight.png',
             (Bishop.Bishop, False): 'black_bishop.png', (Bishop.Bishop, True): 'white_bishop.png',
             (Rook.Rook, False):     'black_rook.png', (Rook.Rook, True): 'white_rook.png',
             (Queen.Queen, False):   'black_queen.png', (Queen.Queen, True): 'white_queen.png',
             (King.King, False):     'black_king.png', (King.King, True): 'white_king.png',
             }
    for key in paths:
        SPRITE_DICTIONARY[key] = load_sprite(os.path.join(FOLDER_PATHS['Pieces'], paths[key]), size)
    LOGO[0] = load_sprite(os.path.join(FOLDER_PATHS['Sprites'], 'Logo.png'), [int(size[0] * 2.5)] * 2)
    LOGO[1] = (Display.CENTER[0] - size[0] * 2.5 // 2, 0)


def load_sprite(path, size):
    """
    Loads a sprite, resizes it, and puts some sick antialiasing on it

    :param path: path to its sprite
    :param size: final size after resizing
    :return: returns the antialiased image
    """
    image = pygame.image.load(path)
    image_string = pygame.image.tostring(image, 'RGBA')
    enhanced = Image.frombytes("RGBA", image.get_size(), bytes(image_string)).filter(ImageFilter.SMOOTH)
    resized = enhanced.resize(size, resample=Image.ANTIALIAS)
    return pygame.image.fromstring(resized.tobytes("raw", 'RGBA'), size, 'RGBA')
