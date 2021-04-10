import pygame

from GUI import Shapes


class DropDownMenu:

    def __init__(self, color_menu, color_option, center, size, font, main, options):
        self.top_left = (center[0] - size[0] / 2,
                         center[1] - size[1] / 2)
        self.rect = pygame.rect.Rect(*self.top_left, *size)
        self.color_menu = color_menu
        self.color_option = color_option
        self.size = size
        self.center = center
        self.font = font
        self.main = main
        self.options = options
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1

    def render(self, screen):
        Shapes.draw_rect(screen, self.center, self.size, self.color_menu[self.menu_active])
        Shapes.draw_text(screen, self.center, self.main, self.font, (255, 255, 255))

        if self.draw_menu:
            for i, text in enumerate(self.options):
                center = (self.center[0] + self.size[0] + 2, self.center[1] + i * self.rect.height)
                Shapes.draw_rect(screen, center, self.size, self.color_option[1 if i == self.active_option else 0])
                Shapes.draw_text(screen, center, text, self.font, (255, 255, 255))

    def update(self, event_list):
        mpos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)

        self.active_option = -1
        for i in range(len(self.options)):
            rect = self.rect.copy()
            rect.x += self.size[0] + 2
            rect.y += i * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_active:
                    self.draw_menu = not self.draw_menu
                elif self.draw_menu and self.active_option >= 0:
                    self.draw_menu = False
                    return self.active_option
        return -1
