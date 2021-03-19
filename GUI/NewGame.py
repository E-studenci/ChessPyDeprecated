from GUI.Item.Button import Button
from GUI.Menu import MAX_FPS
import pygame
import sys
import os


def new_game(screen, clock):
    screen.fill(pygame.Color("white"))
    buttons = add_buttons(screen, clock)
    running_loop(screen, clock)


def running_loop(screen, clock):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # buttons(screen)
        clock.tick(MAX_FPS)
        pygame.display.flip()


def add_buttons(screen, clock):
    pass
