import sys

import pygame

from GUI.Constants import Colors, Font, Display, Board
from GUI.Backgrounds.ChessBackground import ChessBackground
from GUI.Items.MenuButton import MenuButton
from GUI.Backgrounds import Sprites_Loaded, ChessBoard
from GameManagerPackage.Players.BotRandom import BotRandom

NUMBER_OF_BUTTONS = 5
BUTTON_SIZE = (240, 70)
BUTTON_GAP = 13
BUTTON_STARTING_POSITION = (Display.CENTER[0], Display.CENTER[1] - (3 * BUTTON_SIZE[1] + 3 * BUTTON_GAP) // 2)


def start_menu():
    """
    :return: initialize the menu screen
    """
    pygame.display.init()
    pygame.font.init()
    pygame.freetype.init()
    pygame.mixer.init()
    Sprites_Loaded.initialize((Board.SQUARE_SIZE, Board.SQUARE_SIZE))
    from GUI.Windows.NewGame import start_new_game
    from GUI.Windows.LoadGame import start_load_game
    from GUI.Windows.Options import start_options
    from GUI.Windows.Leaderboards import start_leaderboards
    screen = pygame.display.set_mode((Display.DISPLAY_WIDTH, Display.DISPLAY_HEIGHT))
    ChessBoard.initialize(screen,
                          (Display.DISPLAY_WIDTH, Display.DISPLAY_HEIGHT))
    pygame.display.set_caption('')
    clock = pygame.time.Clock()
    background = ChessBackground((Display.DISPLAY_WIDTH, Display.DISPLAY_HEIGHT), BotRandom, BotRandom, 2)
    background.render(screen)
    button_functionality = [(start_new_game, (screen, clock, background), "START NEW GAME"),
                            (start_load_game, (screen, clock, background), "LOAD GAME"),
                            (start_leaderboards, (screen, clock, background), "LEADERBOARDS"),
                            (start_options, (screen, clock, background), "OPTIONS"),
                            (sys.exit, 0, "EXIT")]
    buttons = add_buttons(screen, button_functionality)
    running_loop(screen, clock, buttons, background)


def running_loop(screen, clock, buttons, background):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            for button in buttons:
                if button.handle_event(event):
                    break
        background.render(screen)
        for button in buttons:
            button.render(screen, True if button.rect.collidepoint(pygame.mouse.get_pos()) else False)
        clock.tick(Display.MAX_FPS)
        pygame.display.flip()


def add_buttons(screen, button_functionality):
    """
    :param screen: the screen the buttons should be rendered on
    :param button_functionality: a list of tuples (function, args, text)
    :return: a list of NUMBER_OF_BUTTONS buttons with chosen functionality and renders them
    """
    buttons = []
    offset = BUTTON_GAP + BUTTON_SIZE[1]

    for index in range(NUMBER_OF_BUTTONS):
        button_position = (BUTTON_STARTING_POSITION[0], BUTTON_STARTING_POSITION[1] + offset * index)
        button = MenuButton(button_position,
                            button_functionality[index][0],
                            button_functionality[index][1],
                            BUTTON_SIZE,
                            Colors.BUTTON_BACKGROUND_COLOR,
                            Font.FONT,
                            Font.FONT_COLOR,
                            1.2,
                            5,
                            button_functionality[index][2])
        button.render(screen)
        buttons.append(button)
    return buttons
