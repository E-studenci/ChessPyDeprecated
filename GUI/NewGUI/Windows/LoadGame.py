import pygame
from GUI.Constants import *
from GUI.NewGUI import Shapes

# Font
FONT_SIZE = 20
FONT_HEIGHT = 23
FONT_TUPLE = ('arial', FONT_SIZE, True, False)
FONT_COLOR = (255, 255, 255, 10)

# Starting Message
STARTING_MESSAGE_STRING = "INPUT FEN HERE"
FONT = pygame.font.SysFont(FONT_TUPLE[0], FONT_TUPLE[1], FONT_TUPLE[2], FONT_TUPLE[3])
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
    screen = args[0]
    clock = args[1]
    text = STARTING_MESSAGE_STRING
    text_input_boxes = add_text_input_box(screen, clock)
    screen.fill(pygame.color.Color(*BACKGROUND_COLOR))
    Shapes.draw_rect(screen, BACKGROUND_STARTING_POS, BACKGROUND_SIZE_INITIAL, BUTTONS_BACKGROUND_COLOR)
    running_loop(screen, clock, text_input_boxes)


def running_loop(screen, clock, text_input_boxes):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for text_input_box in text_input_boxes:
                text_input_box.handle_event(event)
        screen.fill(pygame.color.Color(*BACKGROUND_COLOR))
        for text_input_box in text_input_boxes:
            text_input_box.render(screen)
        clock.tick(MAX_FPS)
        pygame.display.flip()


def add_text_input_box(screen, clock):
    from GUI.NewGUI.Thingies.TextInputBox import TextInputBox
    text_input_boxes = []
    functions = [start_game]
    arguments = [(screen, clock)]
    for index in range(1):
        text_input_box = TextInputBox(CENTER,
                                      functions[index],
                                      arguments[index],
                                      STARTING_MESSAGE_STRING)
        text_input_box.render(screen)
        text_input_boxes.append(text_input_box)
    return text_input_boxes


def start_game(args, fen):
    from GUI.NewGUI.Windows.NewGame import start_new_game
    if fen == "True":
        start_new_game(args, fen)
        return True
    else:
        return False
