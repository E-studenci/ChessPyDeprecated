import pygame

from Chess.Board.Converters import FenDecoder
from GUI.Windows.NewGame import start_new_game
from GUI.Items.TextInputBox import TextInputBox

# Starting Message
from GUI.Constants import Font, Display, Colors

STARTING_MESSAGE_STRING = "INPUT FEN HERE"


def start_load_game(args):
    """
    Initialize the load game screen

    :param args: (screen, clock)
    """
    screen = args[0]
    clock = args[1]
    background = args[2]
    text_input_boxes_functionality = [(start_game, (screen, clock, background))]
    text_input_boxes = add_text_input_box(screen, text_input_boxes_functionality)
    background.render(screen)
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
        clock.tick(Display.MAX_FPS)
        pygame.display.flip()


def add_text_input_box(screen, text_input_box_functionality):
    """
    :param screen: the screen the switches should be rendered on
    :param text_input_box_functionality: a list of tuples (function, args)
    :return: a list of text input boxes with chosen functionality and renders them
    """
    text_input_boxes = []
    for index in range(1):
        text_input_box = TextInputBox(Display.CENTER,
                                      *text_input_box_functionality[index],
                                      STARTING_MESSAGE_STRING,
                                      Colors.TEXT_INPUT_BOX_COLOR_ACTIVE,
                                      Colors.TEXT_INPUT_BOX_COLOR_INACTIVE,
                                      Colors.TEXT_INPUT_BOX_COLOR_INCORRECT,
                                      Font.FONT, Font.FONT_COLOR)
        text_input_box.render(screen)
        text_input_boxes.append(text_input_box)
    return text_input_boxes


def start_game(args, fen):
    """
    :param args: the args to be passed to start_new_game()
    :param fen: the fen to be passed to start_new_game()
    :return: a new game from the fen if it is correct, if the fen is incorrect, return False
    """
    try:
        FenDecoder.initialize_list_from_FEN(fen)
        start_new_game(args, fen)
        return True
    except:
        return False
