import pygame
import os

from GUI import Constants

pygame.display.init()
SWITCH_SIZE = (90, 40)
STEPS = 30
COLOR_WHEN_OFF = (0, 0, 0)
COLOR_WHEN_ON = (0, 255, 0)
COLOR_CHANGE = ((COLOR_WHEN_ON[0] - COLOR_WHEN_OFF[0]) // STEPS,
                (COLOR_WHEN_ON[1] - COLOR_WHEN_OFF[1]) // STEPS,
                (COLOR_WHEN_ON[2] - COLOR_WHEN_OFF[2]) // STEPS)


class Switch:
    def __init__(self, position, command=None, args=None, text=None):
        self.rect = pygame.rect.Rect(position, SWITCH_SIZE)
        self.position = position
        self.command = command
        self.args = args
        self.is_on = Constants.SOUND
        self.color = COLOR_WHEN_OFF if not self.is_on else COLOR_WHEN_ON
        self.offset = 0 if not self.is_on else SWITCH_SIZE[0] - SWITCH_SIZE[1]
        self.text = text

    def render(self, screen):
        if self.is_on:
            if not all(x == y for x, y in zip(self.color, COLOR_WHEN_ON)):
                self.color = (self.color[0] + COLOR_CHANGE[0],
                              self.color[1] + COLOR_CHANGE[1],
                              self.color[2] + COLOR_CHANGE[2])
            if self.offset < SWITCH_SIZE[0] - SWITCH_SIZE[1]:
                self.offset += 2
        else:
            if not all(x == y for x, y in zip(self.color, COLOR_WHEN_OFF)):
                self.color = (self.color[0] - COLOR_CHANGE[0],
                              self.color[1] - COLOR_CHANGE[1],
                              self.color[2] - COLOR_CHANGE[2])
            if self.offset > 0:
                self.offset -= 2
        self.draw_circle(screen)
        self.draw_circle(screen, SWITCH_SIZE[0] - SWITCH_SIZE[1])
        self.draw_rect(screen)
        self.draw_button(screen, self.offset)
        if self.text is not None:
            self.draw_text_box(screen)

    def draw_circle(self, screen, offset=0):
        radius = int(SWITCH_SIZE[1] / 2)
        circle_position = (self.rect.bottomleft[0] + radius + offset, self.rect.bottomleft[1] - radius)
        pygame.draw.circle(screen, pygame.Color(*self.color), circle_position, radius)

    def draw_button(self, screen, offset=0):
        radius = int(SWITCH_SIZE[1] / 2) + 2
        circle_position = (self.rect.bottomleft[0] - 2 + radius + offset, self.rect.bottomleft[1] + 2 - radius)
        pygame.draw.circle(screen, (100, 100, 100), circle_position, radius)

    def draw_rect(self, screen):
        rect_position = (self.position[0] + int(SWITCH_SIZE[1] / 2), self.position[1])
        rect_size = (SWITCH_SIZE[0] - SWITCH_SIZE[1], SWITCH_SIZE[1])
        rect_to_draw = pygame.rect.Rect(rect_position, rect_size)
        pygame.draw.rect(screen, pygame.Color(*self.color), rect_to_draw)

    def draw_text_box(self, screen):
        pygame.font.init()
        font = pygame.font.SysFont(Constants.FONT[0], Constants.FONT[1], Constants.FONT[2], Constants.FONT[3])
        text = font.render(self.text, False, (0, 0, 0))
        radius = int(SWITCH_SIZE[1] / 2)
        circle_position = (self.rect.bottomleft[0] - text.get_size()[0],
                           self.rect.bottomleft[1] - radius - text.get_size()[1] // 2)
        screen.blit(text, circle_position)

    def click_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                if self.is_on:
                    Constants.SOUND = False
                    self.is_on = False
                    if self.command is not None:
                        self.command(self.args)
                else:
                    Constants.SOUND = True
                    self.is_on = True
                    if self.command is not None:
                        self.command(self.args)
