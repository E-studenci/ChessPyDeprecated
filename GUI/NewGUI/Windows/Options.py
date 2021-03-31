import pygame

from GUI import Constants
from GUI.Constants import *
from GUI.NewGUI import Shapes

SWITCH_GAP = 13
NUMBER_OF_SWITCHES = 2
SWITCH_STARTING_POSITIONS = (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2)
BACKGROUND_COLOR = (80, 80, 80)
BUTTONS_BACKGROUND_COLOR = (0, 0, 0, 150)
FONT_SIZE = 20
FONT = ('arial', FONT_SIZE, True, False)
FONT_COLOR = (255, 255, 255, 10)


def start_options(args):
    screen = args[0]
    clock = args[1]
    screen.fill(pygame.color.Color(*BACKGROUND_COLOR))
    Shapes.draw_rect(screen, (300, 400), SWITCH_STARTING_POSITIONS, BUTTONS_BACKGROUND_COLOR)
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
        Shapes.draw_rect(screen, (300, 400), SWITCH_STARTING_POSITIONS, BUTTONS_BACKGROUND_COLOR)
        for switch in switches:
            switch.render(screen)
        clock.tick(MAX_FPS)
        pygame.display.flip()


def add_buttons(screen, clock):
    return []


def add_switches(screen, clock):
    from GUI.NewGUI.Buttons.Switch import Switch
    from GUI.Item.Switch import SWITCH_SIZE
    switches = []
    offset = SWITCH_GAP + SWITCH_SIZE[0]
    functions = [mute_sound, mute_music]
    arguments = [Constants.SOUND, Constants.MUSIC]
    text = ["SOUND", "MUSIC"]
    for index in range(NUMBER_OF_SWITCHES):
        switch_position = (SWITCH_STARTING_POSITIONS[0], SWITCH_STARTING_POSITIONS[1] + offset * index)
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
