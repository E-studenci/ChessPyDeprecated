import pygame
import os

pygame.init()


class Button:
    def __init__(self, position, command, normal_image, hover_image):
        self.normal_image = normal_image
        self.hover_image = hover_image
        self.rect = pygame.rect.Rect(position, self.normal_image.get_size())
        self.position = position
        self.command = command

    def render(self, screen):
        if not self.rect.collidepoint(pygame.mouse.get_pos()):
            screen.blit(self.normal_image, self.position)
        else:
            screen.blit(self.hover_image, self.position)

    def click_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.command[0](self.command[1], self.command[2])
