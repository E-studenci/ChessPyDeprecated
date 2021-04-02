import sys
import pygame
from GUI.Constants import *
from GUI.Items.MenuButton import MenuButton

NUMBER_OF_BUTTONS = 4
BUTTON_SIZE = (200, 50)
BUTTON_GAP = 13
CENTER = (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2)
BUTTON_STARTING_POSITION = (CENTER[0], CENTER[1] - (4 * BUTTON_SIZE[1] - 3 * BUTTON_GAP) // 2)


def start_menu():
    """
    :return: initialize the menu screen
    """
    pygame.display.init()
    pygame.font.init()
    pygame.freetype.init()
    from OLDGUI.NewGame import start_new_game
    from GUI.Windows.LoadGame import start_load_game
    from GUI.Windows.Options import start_options
    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption('')
    clock = pygame.time.Clock()
    screen.fill(pygame.color.Color(*BACKGROUND_COLOR))
    button_functionality = [(start_new_game, (screen, clock), "START NEW GAME"),
                            (start_load_game, (screen, clock), "LOAD GAME"),
                            (start_options, (screen, clock), "OPTIONS"),
                            (sys.exit, (0), "EXIT")]
    buttons = add_buttons(screen, button_functionality)
    running_loop(screen, clock, buttons)


def running_loop(screen, clock, buttons):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for button in buttons:
                button.handle_event(event)
        screen.fill(pygame.color.Color(*BACKGROUND_COLOR))
        for button in buttons:
            button.render(screen, True if button.rect.collidepoint(pygame.mouse.get_pos()) else False)
        clock.tick(MAX_FPS)
        pygame.display.flip()


def add_buttons(screen, button_functionality):
    """
    :param screen: the screen the buttons should be rendered on
    :param button_functionality: a list of tuples (function, args, text)
    :return: creates a list of NUMBER_OF_BUTTONS buttons with chosen functionality and renders them
    """
    buttons = []
    offset = BUTTON_GAP + BUTTON_SIZE[1] * 1.5

    for index in range(NUMBER_OF_BUTTONS):
        button_position = (BUTTON_STARTING_POSITION[0], BUTTON_STARTING_POSITION[1] + offset * index)
        button = MenuButton(button_position,
                            button_functionality[index][0],
                            button_functionality[index][1],
                            BUTTON_SIZE,
                            button_functionality[index][2])
        button.render(screen)
        buttons.append(button)
    return buttons
