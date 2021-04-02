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
        text: string
            the text that should be displayed on the button

    Methods
        render(screen, hoveer=False)
            renders the button on the screen
        handle_event(event)
            use this method to handle an event
    """
    def __init__(self, center, command, args, size, text=None):
        self.top_left = (center[0] - size[0] / 2,
                         center[1] - size[1] / 2)
        self.rect = pygame.rect.Rect(*self.top_left, *size)
        self.center = center
        self.command = command
        self.args = args
        self.size_initial = size
        self.size = size
        self.text = text
        self.font_size = FONT_SIZE

    def render(self, screen, hover=False):
        """
        :param screen: the screen the button should be drawn on
        :param hover: is the mouse hovering over the button
        :return: updates the buttons size depending on hover, and draws the button on the screen
        """
        self.resize(hover)
        Shapes.draw_rect(screen, self.center, self.size, BACKGROUND_COLOR)
        Shapes.draw_text(screen, self.center, self.text, (FONT[0], int(self.font_size), FONT[2], FONT[3]), FONT_COLOR)

    def resize(self, hover):
        """
        :param hover: is the mouse hovering over the button
        :return: resizes the button if the mouse is hovering over it
        """
        size_comp = tuple(i * RESIZE_VALUE for i in self.size_initial)
        if hover and all(x < y if ENLARGE else x > y for x, y in zip(self.size, size_comp)):
            self.size = tuple(i * RESIZE_VALUE_2 for i in self.size)
            self.font_size *= RESIZE_VALUE_2
        elif not hover and all(x > y if ENLARGE else x < y for x, y in zip(self.size, self.size_initial)):
            self.size = tuple(i * 1 / RESIZE_VALUE_2 for i in self.size)
            self.font_size /= RESIZE_VALUE_2

    def handle_event(self, event):
        """
        :param event: the pygame.event to be handled
        :return: if the button is clicked, execute self.command and reset size
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.command(self.args)
                self.size = self.size_initial
                self.font_size = FONT_SIZE
