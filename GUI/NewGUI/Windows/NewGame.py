from GUI.Constants import *
import pygame

def start_new_game(args, FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
    screen = args[0]
    clock = args[1]
    screen.fill(pygame.Color("white"))
    running_loop(screen, clock)
    print(FEN)


def running_loop(screen, clock):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        clock.tick(MAX_FPS)
        pygame.display.flip()
