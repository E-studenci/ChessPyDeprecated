import pygame
from pygame import gfxdraw

from GUI import Constants
from GUI.NewGUI import Shapes
from GUI.NewGUI.Buttons import MenuButton

pygame.display.init()
SWITCH_SIZE = (90, 40)
STEPS = 16
COLOR_WHEN_OFF = (0, 0, 0, 255)
COLOR_WHEN_ON = (0, 255, 0, 255)
COLOR_CHANGE = tuple((x - y) / STEPS for x, y in zip(COLOR_WHEN_ON, COLOR_WHEN_OFF))


class Switch:
    def __init__(self, center, width, height, command=None, args=None, text=None):
        self.center = center
        self.size = (width, height)
        self.rect = pygame.rect.Rect((self.center[0] - self.size[0] / 2, self.center[1] - self.size[1] / 2),
                                     self.size)
        self.command = command
        self.args = args
        self.is_on = args
        self.color = COLOR_WHEN_OFF if not self.is_on else COLOR_WHEN_ON
        self.color_float = self.color
        self.offset = 0 if not self.is_on else self.size[0]
        self.offset_step = self.size[0] / STEPS
        self.text = text
        self.radius = int(height / 2)

    def render(self, screen):
        self.update()
        pygame.draw.circle(screen, pygame.Color(*self.color),
                           (self.center[0] - self.size[0] / 2, self.center[1]),
                           self.radius)
        Shapes.draw_rect(screen, self.size, self.center, self.color)
        self.draw_circle(screen, (self.center[0] - self.size[0] / 2, self.center[1]), self.radius)
        self.draw_circle(screen, (self.center[0] + self.size[0] / 2, self.center[1]), self.radius)
        self.draw_button(screen,
                         (self.center[0] - self.size[0] / 2 + self.offset,
                          self.center[1]),
                         int(SWITCH_SIZE[1] / 2),
                         (100, 100, 100))
        if self.text is not None:
            self.draw_text_box(screen, (self.center[0], self.center[1] - self.size[1]))

    def update(self):
        if self.is_on:
            if any(x < y if z > 0 else x > y for x, y, z in zip(self.color_float, COLOR_WHEN_ON, COLOR_CHANGE)):
                if not any(x < 0 or x > 255 for x in tuple(x + y for x, y in zip(self.color_float, COLOR_CHANGE))):
                    self.color_float = tuple(x + y for x, y in zip(self.color_float, COLOR_CHANGE))
            if self.offset < self.size[0]:
                self.offset += self.offset_step
        else:
            if any(x > y if z > 0 else x < y for x, y, z in zip(self.color_float, COLOR_WHEN_OFF, COLOR_CHANGE)):
                if not any(x < 0 or x > 255 for x in tuple(x - y for x, y in zip(self.color_float, COLOR_CHANGE))):
                    self.color_float = tuple(x - y for x, y in zip(self.color_float, COLOR_CHANGE))
            if self.offset - self.offset_step >= 0:
                self.offset -= self.offset_step
        self.color = tuple(int(x) for x in self.color_float)

    def draw_circle(self, screen, center, radius):
        color = tuple(int(i) for i in self.color)
        pygame.draw.circle(screen, pygame.Color(*color), center, radius)

    def draw_button(self, screen, center, radius, color):
        pygame.draw.circle(screen, color, center, radius)

    def draw_text_box(self, screen, center):
        font = pygame.font.SysFont(MenuButton.FONT[0], MenuButton.FONT[1], MenuButton.FONT[2], MenuButton.FONT[3])
        text = font.render(self.text, True, MenuButton.FONT_COLOR)
        text_rect = text.get_rect()
        text_rect.center = center
        screen.blit(text, text_rect)

    def click_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                if self.is_on:
                    self.is_on = False
                    self.command(True)
                else:
                    self.is_on = True
                    self.command(False)
