import pygame as p


DISPLAY_WIDTH = 512
DISPLAY_HEIGHT = 512
SQUARE_SIZE = DISPLAY_HEIGHT / 8
MAX_FPS = 15


def initialize_board():
    p.display.init()
    screen = p.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    p.display.set_caption('')
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    running = True
    while running:
        for obj in p.event.get():
            if obj.type == p.QUIT:
                running = False
        draw_board(screen)
        clock.tick(MAX_FPS)
        p.display.flip()


def draw_board(screen):
    board_colors = [p.Color("white"), p.Color("grey")]
    for i in range(8):
        for j in range(8):
            color = board_colors[(i + j) % 2]
            p.draw.rect(screen, color, p.Rect(j * SQUARE_SIZE, i * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
