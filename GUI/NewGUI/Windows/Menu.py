import sys
import pygame
from GUI.Constants import *
from GUI.NewGUI.Thingies.MenuButton import MenuButton

NUMBER_OF_BUTTONS = 4
BUTTON_SIZE = (200, 100)
BUTTON_GAP = 13
CENTER = (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2)
BUTTON_STARTING_POSITION = (CENTER[0], CENTER[1] - (4 * BUTTON_SIZE[1] - 3 * BUTTON_GAP) // 2)


def start_menu():
    pygame.display.init()
    pygame.font.init()
    pygame.freetype.init()
    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption('')
    clock = pygame.time.Clock()
    screen.fill(pygame.color.Color(*BACKGROUND_COLOR))
    buttons = add_buttons(screen, clock)
    running_loop(screen, clock, buttons)


def running_loop(screen, clock, buttons):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                print(pygame.mouse.get_pos())
            for button in buttons:
                button.click_event(event)
        screen.fill(pygame.color.Color(*BACKGROUND_COLOR))
        for button in buttons:
            button.render(screen, True if button.rect.collidepoint(pygame.mouse.get_pos()) else False)
        clock.tick(MAX_FPS)
        pygame.display.flip()


def add_buttons(screen, clock):
    from GUI.NewGame import start_new_game
    from GUI.NewGUI.Windows.LoadGame import start_load_game
    from GUI.NewGUI.Windows.Options import start_options
    buttons = []
    offset = BUTTON_GAP + BUTTON_SIZE[1]
    functions = [start_new_game, start_load_game, start_options, sys.exit]
    arguments = [(screen, clock), (screen, clock), (screen, clock), 0]
    text = ["START NEW GAME", "LOAD GAME", "OPTIONS", "EXIT"]

    for index in range(NUMBER_OF_BUTTONS):
        button_position = (BUTTON_STARTING_POSITION[0], BUTTON_STARTING_POSITION[1] + offset * index)
        button = MenuButton(button_position,
                            functions[index],
                            arguments[index],
                            200,
                            50,
                            text[index])
        button.render(screen)
        buttons.append(button)
    return buttons
