from GUI.Backgrounds.ChessBackground import ChessBackground
from GUI.Constants import *
import pygame


def start_new_game(args, FEN="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
    screen = args[0]
    clock = args[1]
    screen.fill(pygame.Color("white"))
    background = ChessBackground((400,400), FEN)
    background.update(screen)
    background.render(screen)
    running_loop(screen, clock, background)

def running_loop(screen, clock, background):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        background.render(screen)
        clock.tick(MAX_FPS)
        pygame.display.flip()
