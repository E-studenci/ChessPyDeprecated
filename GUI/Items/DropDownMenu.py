import pygame

from GUI import Shapes


class DropDownMenu:
    """
    A dropdown menu that appears after clicking the main button

    Attributes
        color_menu: ((r,g,b,a), (r,g,b,a)))
            the color of the main button when inactive, active
        color_option: ((r,g,b,a), (r,g,b,a)))
            the color of the option buttons when inactive, active
        center: (x,y)
            the center position of the main button
        size: (width, height)
            the size of every button
        main: string
            what should appear on the main button
        options: list(string)
            what are the options
        font: (font_name, font_size, bold, italic)
            the font to be used
        font_color: (r,g,b,a)
            the font color to be used

    Methods
        render(screen)
            renders the menu on the screen
        handle_event(event)
            use this method whenever an event is detected
    """

    def __init__(self, color_menu, color_option, center, size, font, main, options, font_color):
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
        self.font_color = font_color

    def render(self, screen):
        """
        Renders the dropdown menu on the screen

        :param screen: the screen the menu should be drawn on
        """
        Shapes.draw_rect(screen, self.center, self.size, self.color_menu[self.menu_active])
        Shapes.draw_text(screen, self.center, self.main, self.font, self.font_color)

        if self.draw_menu:
            for i, text in enumerate(self.options):
                center = (self.center[0] + self.size[0] + 2, self.center[1] + i * self.rect.height)
                Shapes.draw_rect(screen, center, self.size, self.color_option[[0, 1][i == self.active_option]])
                Shapes.draw_text(screen, center, text, self.font, self.font_color)

    def handle_event(self, event):
        """
        Handles the event

        :param event: the pygame.event to be handled
        """
        mpos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)

        hovering_over_any = False
        for i in range(len(self.options)):
            rect = self.rect.copy()
            rect.x += self.size[0] + 2
            rect.y += i * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                hovering_over_any = True
        if not hovering_over_any:
            self.active_option = -1

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.menu_active:
                self.draw_menu = not self.draw_menu
            elif self.draw_menu and self.active_option >= 0:
                self.draw_menu = False
                self.main = self.options[self.active_option]
            if not self.menu_active and self.active_option == -1:
                self.draw_menu = False
