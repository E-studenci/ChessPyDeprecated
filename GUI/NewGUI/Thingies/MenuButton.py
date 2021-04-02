import pygame
import pygame.freetype
from GUI.NewGUI import Shapes

BACKGROUND_COLOR = (0, 0, 0, 150)
RESIZE_VALUE = 1.2
RESIZE_STEPS = 5
RESIZE_VALUE_2 = (RESIZE_VALUE - 1) / RESIZE_STEPS + 1
ENLARGE = True if RESIZE_VALUE_2 >= 1 else False
FONT_SIZE = 20
FONT = ('arial', FONT_SIZE, True, False)
FONT_COLOR = (255, 255, 255, 10)


class MenuButton:
    def __init__(self, center, command, args, width, height, text=None):
        self.top_left = (center[0] - width / 2,
                         center[1] - height / 2)
        self.rect = pygame.rect.Rect(*self.top_left, width, height)
        self.center = center
        self.command = command
        self.args = args
        self.size_initial = (width, height)
        self.size = (width, height)
        self.text = text
        self.font_size = FONT_SIZE

    def render(self, screen, hover=False):
        self.resize(hover)
        Shapes.draw_rect(screen, self.center, self.size, BACKGROUND_COLOR)
        Shapes.draw_text(screen, self.center, self.text, (FONT[0], int(self.font_size), FONT[2], FONT[3]), FONT_COLOR)

    def resize(self, hover):
        size_comp = tuple(i * RESIZE_VALUE for i in self.size_initial)
        if hover and all(x < y if ENLARGE else x > y for x, y in zip(self.size, size_comp)):
            self.size = tuple(i * RESIZE_VALUE_2 for i in self.size)
            self.font_size *= RESIZE_VALUE_2
        elif not hover and all(x > y if ENLARGE else x < y for x, y in zip(self.size, self.size_initial)):
            self.size = tuple(i * 1 / RESIZE_VALUE_2 for i in self.size)
            self.font_size /= RESIZE_VALUE_2

    def click_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.command(self.args)
                self.size = self.size_initial
                self.font_size = FONT_SIZE
