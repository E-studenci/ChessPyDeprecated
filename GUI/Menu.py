import pygame
import os
from GUI.Item.Button import Button

DISPLAY_WIDTH = 1920
DISPLAY_HEIGHT = 1080
MAX_FPS = 15

try:
    PLAY_GAME_BUTTON = pygame.image.load(os.path.join("Sprites", "new_game_button.png"))
    HOVER_PLAY_GAME_BUTTON = pygame.image.load(os.path.join("Sprites", "new_game_button_hover.png"))
except FileNotFoundError:
    PLAY_GAME_BUTTON = None
    HOVER_PLAY_GAME_BUTTON = None

BUTTON_SIZE = PLAY_GAME_BUTTON.get_size()


def start_menu():
    pygame.display.init()
    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption('')
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
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
        for button in buttons:
            button.render(screen)
        clock.tick(MAX_FPS)
        pygame.display.flip()


def add_buttons(screen, clock):
    from GUI.NewGame import new_game
    buttons = []
    play_game_button = Button(((DISPLAY_WIDTH - BUTTON_SIZE[0]) / 2, (DISPLAY_HEIGHT - BUTTON_SIZE[1]) / 2),
                              [new_game, screen, clock],
                              PLAY_GAME_BUTTON,
                              HOVER_PLAY_GAME_BUTTON
                              )
    play_game_button.render(screen)
    buttons.append(play_game_button)
    return buttons
