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
    def __init__(self, position, command, args, width, height, text=None):
        self.rect = pygame.rect.Rect(*position, width, height)
        self.position_initial = position
        self.position = position
        self.command = command
        self.args = args
        self.size_initial = (width, height)
        self.size = (width, height)
        self.text = text
        self.font_size = FONT_SIZE
        self.center = (self.position_initial[0] + self.size_initial[0] / 2,
                       self.position_initial[1] + self.size_initial[1] / 2)

    def render(self, screen, hover=False):
        self.resize(hover)
        Shapes.draw_rect(screen, self.size, self.center, BACKGROUND_COLOR, )
        self.draw_text(screen)

    def resize(self, hover):
        size_comp = tuple(i * RESIZE_VALUE for i in self.size_initial)
        if hover and all(x < y if ENLARGE else x > y for x, y in zip(self.size, size_comp)):
            self.size = tuple(i * RESIZE_VALUE_2 for i in self.size)
            self.font_size *= RESIZE_VALUE_2
        elif not hover and all(x > y if ENLARGE else x < y for x, y in zip(self.size, self.size_initial)):
            self.size = tuple(i * 1 / RESIZE_VALUE_2 for i in self.size)
            self.font_size /= RESIZE_VALUE_2
        self.position = tuple(
            x - abs(y - z) / 2 for x, y, z in zip(self.position_initial, self.size_initial, self.size))

    def draw_text(self, screen):
        font = pygame.font.SysFont(FONT[0], int(self.font_size), FONT[2], FONT[3])
        text = font.render(self.text, True, FONT_COLOR)
        text_rect = text.get_rect()
        text_rect.center = self.center
        screen.blit(text, text_rect)

    def click_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.command(self.args)
