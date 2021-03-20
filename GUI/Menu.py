import pygame
import os
import sys
from GUI.Item.Button import Button

DISPLAY_WIDTH = 1920
DISPLAY_HEIGHT = 1080
MAX_FPS = 15

try:
    PLAY_GAME_BUTTON = pygame.image.load(os.path.join("Sprites", "Buttons", "new_game_button.png"))
    HOVER_PLAY_GAME_BUTTON = pygame.image.load(os.path.join("Sprites", "Buttons", "new_game_button_hover.png"))
    LOAD_GAME_BUTTON = pygame.image.load(os.path.join("Sprites", "Buttons", "load_game_button.png"))
    HOVER_LOAD_GAME_BUTTON = pygame.image.load(os.path.join("Sprites", "Buttons", "load_game_button_hover.png"))
    OPTIONS_BUTTON = pygame.image.load(os.path.join("Sprites", "Buttons", "options_button.png"))
    HOVER_OPTIONS_BUTTON = pygame.image.load(os.path.join("Sprites", "Buttons", "options_button_hover.png"))
    EXIT_GAME_BUTTON = pygame.image.load(os.path.join("Sprites", "Buttons", "exit_game_button.png"))
    HOVER_EXIT_GAME_BUTTON = pygame.image.load(os.path.join("Sprites", "Buttons", "exit_game_button_hover.png"))
    BACKGROUND_FOR_BUTTONS = pygame.image.load(os.path.join("Sprites", "Backgrounds", "button_background.png"))
except FileNotFoundError:
    PLAY_GAME_BUTTON = None
    HOVER_PLAY_GAME_BUTTON = None
    LOAD_GAME_BUTTON = None
    HOVER_LOAD_GAME_BUTTON = None
    OPTIONS_BUTTON = None
    HOVER_OPTIONS_BUTTON = None
    EXIT_GAME_BUTTON = None
    HOVER_EXIT_GAME_BUTTON = None
    BACKGROUND_FOR_BUTTONS = None

NUMBER_OF_BUTTONS = 4
BUTTON_SIZE = PLAY_GAME_BUTTON.get_size()
BUTTON_GAP = 30
BUTTON_STARTING_POSITION = ((DISPLAY_WIDTH - BUTTON_SIZE[0]) / 2, (DISPLAY_HEIGHT - 4 * BUTTON_SIZE[1] - 3 * BUTTON_GAP) / 2)


def start_menu():
    pygame.display.init()
    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption('')
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("grey"))
    buttons = add_buttons(screen, clock)
    running_loop(screen, clock, buttons)


def running_loop(screen, clock, buttons):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for button in buttons:
                button.click_event(event)
        screen.fill(pygame.Color("grey"))
        add_background_for_buttons(screen)
        for button in buttons:
            button.render(screen)
        clock.tick(MAX_FPS)
        pygame.display.flip()


def add_buttons(screen, clock):
    from GUI.NewGame import start_new_game
    from GUI.LoadGame import start_load_game
    from GUI.Options import start_options
    buttons = []
    offset = BUTTON_GAP + BUTTON_SIZE[1]
    functions = [start_new_game, start_load_game, start_options, sys.exit]
    arguments = [(screen, clock), (screen, clock), (screen, clock), 0]
    button_image = [PLAY_GAME_BUTTON, LOAD_GAME_BUTTON, OPTIONS_BUTTON, EXIT_GAME_BUTTON]
    hover_button_image = [HOVER_PLAY_GAME_BUTTON, HOVER_LOAD_GAME_BUTTON, HOVER_OPTIONS_BUTTON, HOVER_EXIT_GAME_BUTTON]

    for index in range(NUMBER_OF_BUTTONS):
        button_position = (BUTTON_STARTING_POSITION[0], BUTTON_STARTING_POSITION[1] + offset * index)
        button = Button(button_position,
                        functions[index],
                        arguments[index],
                        button_image[index],
                        hover_button_image[index]
                        )
        button.render(screen)
        buttons.append(button)
    return buttons


def add_background_for_buttons(screen):
    button_background_position = ((DISPLAY_WIDTH - BACKGROUND_FOR_BUTTONS.get_width()) / 2,
                                  (DISPLAY_HEIGHT - BACKGROUND_FOR_BUTTONS.get_height()) / 2)
    screen.blit(BACKGROUND_FOR_BUTTONS, button_background_position)


if __name__ == '__main__':
    start_menu()
