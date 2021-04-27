import pygame
from GUI.Constants import *
from GUI import Shapes

# Font
FONT_SIZE = 20
FONT_HEIGHT = 23
FONT_TUPLE = ('arial', FONT_SIZE, True, False)
FONT_COLOR = (255, 255, 255, 10)

# Starting Message
STARTING_MESSAGE_STRING = "INPUT FEN HERE"
FONT = pygame.font.SysFont(*FONT_TUPLE)
STARTING_MESSAGE = FONT.render(STARTING_MESSAGE_STRING, True, FONT_COLOR)
STARTING_MESSAGE_SIZE = STARTING_MESSAGE.get_size()

# General Info
CENTER = (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2)

# Background
BACKGROUND_COLOR = (80, 80, 80)
BUTTONS_BACKGROUND_COLOR = (0, 0, 0, 150)
BACKGROUND_STARTING_POS = CENTER
BACKGROUND_SIZE_INITIAL = STARTING_MESSAGE_SIZE


def start_load_game(args):
    """
    :param args: (screen, clock)
    :return: initialize the load game screen
    """
    screen = args[0]
    clock = args[1]
    background = args[2]
    text_input_boxes_functionality = [(start_game, (screen, clock, background))]
    text_input_boxes = add_text_input_box(screen, text_input_boxes_functionality)
    background.render(screen)
    Shapes.draw_rect(screen, BACKGROUND_STARTING_POS, BACKGROUND_SIZE_INITIAL, BUTTONS_BACKGROUND_COLOR)
    running_loop(screen, clock, text_input_boxes, background)


def running_loop(screen, clock, text_input_boxes, background):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT \
                    or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                break
            for text_input_box in text_input_boxes:
                text_input_box.handle_event(event)
        background.render(screen)
        for text_input_box in text_input_boxes:
            text_input_box.render(screen)
        clock.tick(MAX_FPS)
        pygame.display.flip()


def add_text_input_box(screen, text_input_box_functionality):
    """
    :param screen: the screen the switches should be rendered on
    :param text_input_box_functionality: a list of tuples (function, args)
    :return:creates a list of text input boxes with chosen functionality and renders them
    """
    from GUI.Items.TextInputBox import TextInputBox
    text_input_boxes = []
    for index in range(1):
        text_input_box = TextInputBox(CENTER,
                                      *text_input_box_functionality[index],
                                      STARTING_MESSAGE_STRING)
        text_input_box.render(screen)
        text_input_boxes.append(text_input_box)
    return text_input_boxes


def start_game(args, fen):
    """
    :param args: the args to be passed to start_new_game()
    :param fen: the fen to be passed to start_new_game()
    :return: starts a new game from the fen if it is correct, if the fen is incorrect, return False
    """
    from GUI.Windows.NewGame import start_new_game
    if fen == "True":
        start_new_game(args, fen)
        return True
    return False
