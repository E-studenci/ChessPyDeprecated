import pygame

from GUI.Constants import Display, Font, Colors
from GUI.Items.LeaderboardsList import LeaderboardsList

AMOUNT_OF_RECORDS = 5


def start_leaderboards(args):
    screen = args[0]
    clock = args[1]
    background = args[2]
    background.render(screen)
    leaderboards = LeaderboardsList(Display.CENTER, Font.FONT,
                                    Font.FONT_COLOR, Colors.BUTTON_BACKGROUND_COLOR, AMOUNT_OF_RECORDS,
                                    "Leaderboards.txt")
    running_loop(screen, clock, leaderboards, background)


def running_loop(screen, clock, leaderboards, background):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT \
                    or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                break
        background.render(screen)
        leaderboards.render(screen)
        clock.tick(Display.MAX_FPS)
        pygame.display.flip()
