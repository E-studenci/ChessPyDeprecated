import multiprocessing

if multiprocessing.current_process().name == 'MainProcess':
    import pygame

from GUI.Items.TextInputBox import TextInputBox
from GUI.Constants import Display, Font, Colors
from GUI.Items.LeaderboardsList import LeaderboardsList
from Paths import FOLDER_PATHS

AMOUNT_OF_RECORDS = 5


def start_leaderboards(args):
    screen = args[0]
    clock = args[1]
    background = args[2]
    background.render(screen)
    leaderboards = LeaderboardsList(Display.CENTER, Font.FONT,
                                    Font.FONT_COLOR, Colors.BUTTON_BACKGROUND_COLOR, AMOUNT_OF_RECORDS,
                                    f"{FOLDER_PATHS['Leaderboards']}/Leaderboards.txt")

    text_input_boxes_functionality = [(None, None)]
    text_input_boxes = add_text_input_box(screen, text_input_boxes_functionality)
    running_loop(screen, clock, leaderboards, background, text_input_boxes)


def running_loop(screen, clock, leaderboards, background, text_input_boxes):
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
        leaderboards.render(screen, text_input_boxes[0].text)
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
        text_input_box = TextInputBox((Display.CENTER[0], Display.CENTER[1] - Display.DISPLAY_HEIGHT // 9),
                                      *text_input_box_functionality[index],
                                      "FILTER LEADERBOARDS",
                                      Colors.TEXT_INPUT_BOX_COLOR_ACTIVE,
                                      Colors.TEXT_INPUT_BOX_COLOR_INACTIVE,
                                      Colors.TEXT_INPUT_BOX_COLOR_INCORRECT,
                                      Font.FONT, Font.FONT_COLOR)
        text_input_box.render(screen)
        text_input_boxes.append(text_input_box)
    return text_input_boxes
