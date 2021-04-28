import pygame

from GUI import Shapes


class Switch:
    """
    A simple switch it turns on/off and executes a command when clicked

    Attributes
        center: (x, y)
            the center of the switch in pixels
        size: (width, height):
            the dimensions of the switch in pixels
        color_off: (r,g,b,a)
            color when off
        color_on: (r,g,b,a)
            color when on
        switch_color: (r,g,b,a)
            color of the sliding circle
        steps:
            how many steps top change state
        font: (font_name, font_size, bold, italic)
            the font to be used
        font_color: (r,g,b,a)
            the font color to be used
        command:
            the method to be executed upon clicking
        arg:
            the initial position of the switch (on or off)
        text:
            the text that should be displayed above the switch

    Methods
        render(screen)
            renders the switch on the screen
        handle_event(event)
            use this method to handle an event
    """

    def __init__(self, center, size, color_off, color_on, switch_color, steps, font, font_color, command, arg,
                 text=None):
        self.center = center
        self.size = size
        self.rect = pygame.rect.Rect((self.center[0] - self.size[0] / 2, self.center[1] - self.size[1] / 2),
                                     self.size)
        self.command = command
        self.is_on = arg
        self.color_off = color_off
        self.color_on = color_on
        self.switch_color = switch_color
        self.steps = steps
        self.font = font
        self.font_color = font_color
        self.color = color_on if self.is_on else color_off
        self.color_float = self.color
        self.offset = 0 if not self.is_on else self.size[0]
        self.offset_step = self.size[0] / steps
        self.text = text
        self.color_change = tuple((x - y) / steps for x, y in zip(color_on, color_off))
        self.radius = int(size[1] / 2)

    def render(self, screen):
        """
        Updates the switch and draws it on the screen

        :param screen: the screen the button should be drawn on
        """
        self.__update()
        pygame.draw.circle(screen, pygame.Color(*self.color),
                           (self.center[0] - self.size[0] / 2, self.center[1]),
                           self.radius)
        Shapes.draw_rect(screen, self.center, self.size, self.color)
        self.__draw_circle(screen, (self.center[0] - self.size[0] / 2, self.center[1]), self.radius)
        self.__draw_circle(screen, (self.center[0] + self.size[0] / 2, self.center[1]), self.radius)
        self.__draw_button(screen,
                           (self.center[0] - self.size[0] / 2 + self.offset,
                            self.center[1]),
                           int(self.size[1] / 2),
                           self.switch_color)
        if self.text is not None:
            Shapes.draw_text(screen, (self.center[0], self.center[1] - self.size[1]),
                             self.text,
                             self.font, self.font_color)

    def __update(self):
        """
        Updates the color and position of the switch
        """
        if self.is_on:
            if any(x < y if z > 0 else x > y for x, y, z in zip(self.color_float, self.color_on, self.color_change)):
                if not any(x < 0 or x > 255 for x in tuple(x + y for x, y in zip(self.color_float, self.color_change))):
                    self.color_float = tuple(x + y for x, y in zip(self.color_float, self.color_change))
            if self.offset < self.size[0]:
                self.offset += self.offset_step
        else:
            if any(x > y if z > 0 else x < y for x, y, z in zip(self.color_float, self.color_off, self.color_change)):
                if not any(x < 0 or x > 255 for x in tuple(x - y for x, y in zip(self.color_float, self.color_change))):
                    self.color_float = tuple(x - y for x, y in zip(self.color_float, self.color_change))
            if self.offset - self.offset_step >= 0:
                self.offset -= self.offset_step
        self.color = tuple(int(x) for x in self.color_float)

    def __draw_circle(self, screen, center, radius):
        color = tuple(int(i) for i in self.color)
        # Shapes.draw_circle(screen, center, radius, color)
        pygame.draw.circle(screen, pygame.Color(*color), center, radius)

    def __draw_button(self, screen, center, radius, color):
        # Shapes.draw_circle(screen, center, radius, color)
        pygame.draw.circle(screen, color, center, radius)

    def handle_event(self, event):
        """
        Switches the switch and executes self.command upon clicking

        :param event: the pygame.event to be handled
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                if self.is_on:
                    self.is_on = False
                    self.command(True)
                else:
                    self.is_on = True
                    self.command(False)
