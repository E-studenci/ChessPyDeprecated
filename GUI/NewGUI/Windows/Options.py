import pygame

from GUI import Constants
from GUI.Constants import *
from GUI.NewGUI import Shapes

# Font
FONT_SIZE = 20
FONT_HEIGHT = 23
FONT = ('arial', FONT_SIZE, True, False)
FONT_COLOR = (255, 255, 255, 10)

# Switch
SWITCH_SIZE = (90, 40)
SWITCH_HEIGHT_TOTAL = SWITCH_SIZE[1] * 1.5 + FONT_HEIGHT / 2

# General Info
NUMBER_OF_SWITCHES = 2
CENTER = (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2)
SWITCH_STARTING_CENTER = (CENTER[0], CENTER[1] + SWITCH_SIZE[1] / 2)
OFFSET_COUNT = NUMBER_OF_SWITCHES // 2 if NUMBER_OF_SWITCHES % 2 == 1 else \
    NUMBER_OF_SWITCHES // 3
SWITCH_STARTING_POSITION = \
     (SWITCH_STARTING_CENTER[0],
     (SWITCH_STARTING_CENTER[1] - (SWITCH_HEIGHT_TOTAL * 1.5) * OFFSET_COUNT)
     if NUMBER_OF_SWITCHES % 2 == 1 else
     (SWITCH_STARTING_CENTER[1] - 0.75 * SWITCH_HEIGHT_TOTAL - 1.5 * SWITCH_HEIGHT_TOTAL * OFFSET_COUNT))

SWITCH_GAP = 13

# Background
BACKGROUND_COLOR = (80, 80, 80)
BUTTONS_BACKGROUND_COLOR = (0, 0, 0, 150)
BACKGROUND_STARTING_POS = (CENTER[0], CENTER[1] + FONT_HEIGHT / 3)
BACKGROUND_SIZE = (SWITCH_SIZE[0] * 1.8, (SWITCH_HEIGHT_TOTAL * (1.5 * NUMBER_OF_SWITCHES))
     if NUMBER_OF_SWITCHES % 2 == 1 else (SWITCH_SIZE[1] + SWITCH_HEIGHT_TOTAL * 1.4 * NUMBER_OF_SWITCHES))


def start_options(args):
    screen = args[0]
    clock = args[1]
    screen.fill(pygame.color.Color(*BACKGROUND_COLOR))
    Shapes.draw_rect(screen,
                     BACKGROUND_SIZE,
                     BACKGROUND_STARTING_POS,
                     BUTTONS_BACKGROUND_COLOR)
    switches = add_switches(screen, clock)
    buttons = add_buttons(screen, clock)
    running_loop(screen, clock, switches)


def running_loop(screen, clock, switches):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                print(pygame.mouse.get_pos())
            for switch in switches:
                switch.click_event(event)
        # buttons(screen)
        screen.fill(pygame.color.Color(*BACKGROUND_COLOR))
        Shapes.draw_rect(screen,
                         BACKGROUND_SIZE,
                         BACKGROUND_STARTING_POS,
                         BUTTONS_BACKGROUND_COLOR)
        for switch in switches:
            switch.render(screen)
        clock.tick(MAX_FPS)
        pygame.display.flip()


def add_buttons(screen, clock):
    return []


def add_switches(screen, clock):
    from GUI.NewGUI.Buttons.Switch import Switch
    switches = []
    offset = SWITCH_HEIGHT_TOTAL * 1.5
    functions = [mute_sound, mute_music]
    arguments = [Constants.SOUND, Constants.MUSIC]
    text = ["SOUND", "MUSIC"]
    for index in range(NUMBER_OF_SWITCHES):
        switch_position = (SWITCH_STARTING_POSITION[0], SWITCH_STARTING_POSITION[1] + offset * index)
        switch = Switch(switch_position, 50, 40, functions[index], arguments[index], text[index])
        switch.render(screen)
        switches.append(switch)
    return switches


def mute_sound(mute):
    if mute:
        Constants.SOUND = False
    else:
        Constants.SOUND = True


def mute_music(mute):
    if mute:
        Constants.MUSIC = False
    else:
        Constants.MUSIC = True
