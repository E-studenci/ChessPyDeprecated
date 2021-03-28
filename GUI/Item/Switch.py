import pygame
import os

pygame.display.init()
SWITCH_SIZE = (90, 40)
COLOR_CHANGE = pygame.color.Color(0, 7, 0)
COLOR_WHEN_OFF = pygame.color.Color(0, 0, 0)


class Switch:
    def __init__(self, position, command=None, args=None):
        self.rect = pygame.rect.Rect(position, SWITCH_SIZE)
        self.position = position
        self.command = command
        self.args = args
        self.is_on = False
        self.color = COLOR_WHEN_OFF
        self.offset = 0

    def render(self, screen):
        if self.is_on:
            self.color += COLOR_CHANGE
            if self.offset < SWITCH_SIZE[0] - SWITCH_SIZE[1]:
                self.offset += 2
        else:
            self.color -= COLOR_CHANGE
            if self.offset > 0:
                self.offset -= 2
        self.draw_circle(screen)
        self.draw_circle(screen, SWITCH_SIZE[0] - SWITCH_SIZE[1])
        self.draw_rect(screen)
        self.draw_button(screen, self.offset)

    def draw_circle(self, screen, offset=0):
        radius = int(SWITCH_SIZE[1] / 2)
        circle_position = (self.rect.bottomleft[0] + radius + offset, self.rect.bottomleft[1] - radius)
        pygame.draw.circle(screen, self.color, circle_position, radius)

    def draw_button(self, screen, offset=0):
        radius = int(SWITCH_SIZE[1] / 2) + 2
        circle_position = (self.rect.bottomleft[0] - 2 + radius + offset, self.rect.bottomleft[1] + 2 - radius)
        pygame.draw.circle(screen, (100, 100, 100), circle_position, radius)

    def draw_rect(self, screen):
        rect_position = (self.position[0] + int(SWITCH_SIZE[1] / 2), self.position[1])
        rect_size = (SWITCH_SIZE[0] - SWITCH_SIZE[1], SWITCH_SIZE[1])
        rect_to_draw = pygame.rect.Rect(rect_position, rect_size)
        pygame.draw.rect(screen, self.color, rect_to_draw)

    def click_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                if self.is_on:
                    self.is_on = False
                    if self.command is not None:
                        self.command(self.args)
                else:
                    self.is_on = True
                    if self.command is not None:
                        self.command(self.args)
