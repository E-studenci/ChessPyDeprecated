import pygame
import pygame.freetype
from GUI import Shapes


class MenuButton:
    """
    A simple button made of a text field and a semitransparent background under it
    It resizes upon hover, and executes a command when clicked

    Attributes
        center: (x,y)
            the center of the button in pixels
        command:
            the method to be executed upon clicking
        args:
            the arguments to pass to the method
        size: (width, height):
            the dimensions of the button in pixels
        font: (font_name, font_size, bold, italic)
            the font to be used
        font_color: (r,g,b,a)
            the font color to be used
        resize_value:
            the maximum value, the buttons size will be multiplied by
        resize_steps:
            how many steps to reach max size
        text: string
            the text that should be displayed on the button

    Methods
        render(screen, hover=False)
            renders the button on the screen
        handle_event(event)
            use this method to handle an event
    """

    def __init__(self, center, command, args, size, background_color, font, font_color, resize_value, resize_steps,
                 text=None):
        self.top_left = (center[0] - size[0] / 2,
                         center[1] - size[1] / 2)
        self.rect = pygame.rect.Rect(*self.top_left, *size)
        self.center = center
        self.command = command
        self.args = args
        self.size_initial = size
        self.size = size
        self.text = text
        self.background_color = background_color
        self.font = font
        self.font_size = font[1]
        self.font_initial = font
        self.font_color = font_color
        self.resize_value = resize_value
        self.resize_value_step = (resize_value - 1) / resize_steps + 1

    def render(self, screen, hover=False):
        """
        Updates the buttons size depending on hover, and draws the button on the screen

        :param screen: the screen the button should be drawn on
        :param hover: is the mouse hovering over the button
        """
        self.__resize(hover)
        Shapes.draw_rect(screen, self.center, self.size, self.background_color)
        Shapes.draw_text(screen, self.center, self.text,
                         (self.font[0], int(self.font[1]), self.font[2], self.font[3]), self.font_color)

    def __resize(self, hover):
        """
        Resizes the button if the mouse is hovering over it

        :param hover: is the mouse hovering over the button
        """
        enlarge = True if self.resize_value >= 1 else False
        size_comp = tuple(i * self.resize_value for i in self.size_initial)
        if hover and all(x < y if enlarge else x > y for x, y in zip(self.size, size_comp)):
            self.size = tuple(i * self.resize_value_step for i in self.size)
            font_size = self.font[1] * self.resize_value_step
            self.font = (self.font[0], font_size, self.font[2], self.font[3])
        elif not hover and all(x > y if enlarge else x < y for x, y in zip(self.size, self.size_initial)):
            self.size = tuple(i * 1 / self.resize_value_step for i in self.size)
            font_size = self.font[1] / self.resize_value_step
            self.font = (self.font[0], font_size, self.font[2], self.font[3])

    def handle_event(self, event):
        """
        If the button is clicked, execute self.command and reset size, and return True

        :param event: the pygame.event to be handled
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.command(self.args)
                self.size = self.size_initial
                self.font = self.font_initial
                return True
