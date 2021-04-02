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
SWITCH_SIZE = (50, 40)
SWITCH_HEIGHT_TOTAL = SWITCH_SIZE[1] * 1.5 + FONT_HEIGHT / 2

# General Info
CENTER = (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2)
NUMBER_OF_SWITCHES = 2
SWITCH_STARTING_CENTER = (CENTER[0], CENTER[1] + SWITCH_SIZE[1] / 2)
OFFSET_COUNT = NUMBER_OF_SWITCHES // 2 if NUMBER_OF_SWITCHES % 2 == 1 else \
    NUMBER_OF_SWITCHES // 3
OFFSET = 1.5 * SWITCH_HEIGHT_TOTAL
SWITCH_STARTING_POSITION = (SWITCH_STARTING_CENTER[0],
                            (SWITCH_STARTING_CENTER[1] - (SWITCH_HEIGHT_TOTAL * 1.5) * OFFSET_COUNT)
                            if NUMBER_OF_SWITCHES % 2 == 1 else
                            (SWITCH_STARTING_CENTER[1] - 0.75 * SWITCH_HEIGHT_TOTAL - OFFSET * OFFSET_COUNT))
SWITCH_GAP = 13

# Background
BACKGROUND_COLOR = (80, 80, 80)
BUTTONS_BACKGROUND_COLOR = (0, 0, 0, 150)
BACKGROUND_STARTING_POS = (CENTER[0], CENTER[1] + FONT_HEIGHT / 3)
BACKGROUND_SIZE = (SWITCH_SIZE[0] * 2.5,
                   (SWITCH_HEIGHT_TOTAL * (1.5 * NUMBER_OF_SWITCHES)) if NUMBER_OF_SWITCHES % 2 == 1 else
                   (SWITCH_SIZE[1] + SWITCH_HEIGHT_TOTAL * 1.4 * NUMBER_OF_SWITCHES))


def start_options(args):
    screen = args[0]
    clock = args[1]
    screen.fill(pygame.color.Color(*BACKGROUND_COLOR))
    Shapes.draw_rect(screen, BACKGROUND_STARTING_POS, BACKGROUND_SIZE, BUTTONS_BACKGROUND_COLOR)
    switches = add_switches(screen)
    running_loop(screen, clock, switches)


def running_loop(screen, clock, switches):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for switch in switches:
                switch.click_event(event)
        screen.fill(pygame.color.Color(*BACKGROUND_COLOR))
        Shapes.draw_rect(screen, BACKGROUND_STARTING_POS, BACKGROUND_SIZE, BUTTONS_BACKGROUND_COLOR)
        for switch in switches:
            switch.render(screen)
        clock.tick(MAX_FPS)
        pygame.display.flip()


def add_switches(screen):
    from GUI.NewGUI.Thingies.Switch import Switch
    switches = []
    functions = [mute_sound, mute_music]
    arguments = [Constants.SOUND, Constants.MUSIC]
    text = ["SOUND", "MUSIC"]
    for index in range(NUMBER_OF_SWITCHES):
        switch_position = (SWITCH_STARTING_POSITION[0], SWITCH_STARTING_POSITION[1] + OFFSET * index)
        switch = Switch(switch_position, *SWITCH_SIZE, functions[index], arguments[index], text[index])
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
