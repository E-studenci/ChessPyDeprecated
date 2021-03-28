from GUI.Item.Button import Button
from GUI.Constants import *
import pygame
import sys
import os

SWITCH_GAP = 13
NUMBER_OF_SWITCHES = 1
SWITCH_STARTING_POSITIONS = (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2)


def start_options(args):
    screen = args[0]
    clock = args[1]
    screen.fill(pygame.Color(BACKGROUND_COLOR))
    # buttons = add_buttons(screen, clock)
    buttons = add_buttons(screen, clock)
    switches = add_switches(screen, clock)
    running_loop(screen, clock, buttons, switches)


def running_loop(screen, clock, buttons, switches):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for button in buttons:
                button.click_event(event)
            for switch in switches:
                switch.click_event(event)
        screen.fill(pygame.Color(BACKGROUND_COLOR))
        # buttons(screen)
        for switch in switches:
            switch.render(screen)
        clock.tick(MAX_FPS)
        pygame.display.flip()


def add_buttons(screen, clock):
    return []


def add_switches(screen, clock):
    from GUI.Item.Switch import Switch
    from GUI.Item.Switch import SWITCH_SIZE
    switches = []
    offset = SWITCH_GAP + SWITCH_SIZE[0]
    functions = [None]
    arguments = [None]
    for index in range(NUMBER_OF_SWITCHES):
        switch_position = (SWITCH_STARTING_POSITIONS[0], SWITCH_STARTING_POSITIONS[1] + offset * index)
        switch = Switch(switch_position, functions[index], arguments[index])
        switch.render(screen)
        switches.append(switch)
    return switches
