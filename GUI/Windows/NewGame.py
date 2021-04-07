from GUI import Constants
from GUI.Backgrounds.ChessBackground import ChessBackground
from GUI.Constants import *
import pygame


def start_new_game(args, FEN="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
    screen = args[0]
    clock = args[1]
    background = args[2]
    screen.fill(pygame.Color("white"))
    background.render(screen)
    running_loop(screen, clock, background)


def running_loop(screen, clock, background):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT \
                    or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                break
        background.render(screen)
        clock.tick(MAX_FPS)
        pygame.display.flip()
