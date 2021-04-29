import pygame

from GUI import Shapes
from GUI.Constants import Font, Options, Colors, Display

# Switch
SWITCH_SIZE = (50, 40)
SWITCH_HEIGHT_TOTAL = SWITCH_SIZE[1] * 1.5 + Font.FONT_HEIGHT / 2
STEPS = 16

# General Info
NUMBER_OF_SWITCHES = 2
SWITCH_STARTING_CENTER = (Display.CENTER[0], Display.CENTER[1] + SWITCH_SIZE[1] / 2)
OFFSET_COUNT = NUMBER_OF_SWITCHES // 2 if NUMBER_OF_SWITCHES % 2 == 1 else \
    NUMBER_OF_SWITCHES // 3
OFFSET = 1.5 * SWITCH_HEIGHT_TOTAL
SWITCH_STARTING_POSITION = (SWITCH_STARTING_CENTER[0],
                            (SWITCH_STARTING_CENTER[1] - (SWITCH_HEIGHT_TOTAL * 1.5) * OFFSET_COUNT)
                            if NUMBER_OF_SWITCHES % 2 == 1 else
                            (SWITCH_STARTING_CENTER[1] - 0.75 * SWITCH_HEIGHT_TOTAL - OFFSET * OFFSET_COUNT))
SWITCH_GAP = 13

# Background
BACKGROUND_STARTING_POS = (Display.CENTER[0], Display.CENTER[1] + Font.FONT_HEIGHT / 3)
BACKGROUND_SIZE = (SWITCH_SIZE[0] * 2.5,
                   (SWITCH_HEIGHT_TOTAL * (1.5 * NUMBER_OF_SWITCHES)) if NUMBER_OF_SWITCHES % 2 == 1 else
                   (SWITCH_SIZE[1] + SWITCH_HEIGHT_TOTAL * 1.4 * NUMBER_OF_SWITCHES))


def start_options(args):
    """
    :param args: (screen, clock)
    :return: initialize the options screen
    """
    switch_functionality = [(mute_sound, Options.SOUND, "SOUND"),
                            (mute_music, Options.MUSIC, "MUSIC")]
    screen = args[0]
    clock = args[1]
    background = args[2]
    background.render(screen)
    Shapes.draw_rect(screen, BACKGROUND_STARTING_POS, BACKGROUND_SIZE, Colors.BUTTON_BACKGROUND_COLOR)
    switches = add_switches(screen, switch_functionality)
    running_loop(screen, clock, switches, background)


def running_loop(screen, clock, switches, background):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT \
                    or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                break
            for switch in switches:
                switch.handle_event(event)
        background.render(screen)
        Shapes.draw_rect(screen, BACKGROUND_STARTING_POS, BACKGROUND_SIZE, Colors.BUTTON_BACKGROUND_COLOR)
        for switch in switches:
            switch.render(screen)
        clock.tick(Display.MAX_FPS)
        pygame.display.flip()


def add_switches(screen, switch_functionality):
    """
    :param screen: the screen the switches should be rendered on
    :param switch_functionality: a list of tuples (function, args, text)
    :return: a list of NUMBER_OF_SWITCHES switches with chosen functionality and renders them
    """
    from GUI.Items.Switch import Switch
    switches = []
    for index in range(NUMBER_OF_SWITCHES):
        switch_position = (SWITCH_STARTING_POSITION[0], SWITCH_STARTING_POSITION[1] + OFFSET * index)
        switch = Switch(switch_position, SWITCH_SIZE,
                        Colors.SWITCH_COLOR_OFF, Colors.SWITCH_COLOR_ON, Colors.SWITCH_BUTTON_COLOR,
                        STEPS,
                        Font.FONT,
                        Font.FONT_COLOR,
                        *switch_functionality[index])
        switch.render(screen)
        switches.append(switch)
    return switches


def mute_sound(mute):
    """
    Sets Options.SOUND to True, or False depending on mute

    :param mute: True, if should mute, false if should turn on
    """
    Options.SOUND = not mute


def mute_music(mute):
    """
    Sets Options.MUSIC to True, or False depending on mute

    :param mute: True, if should mute, false if should turn on
    """
    Options.MUSIC = not mute
