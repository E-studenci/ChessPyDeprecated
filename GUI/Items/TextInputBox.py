import pygame
from GUI import Shapes

# Font
FONT_SIZE = 30
FONT_HEIGHT = 23
FONT = ('arial', FONT_SIZE, True, False)
FONT_COLOR = (255, 255, 255, 10)

BACKGROUND_COLOR = (0, 0, 0, 150)


class TextInputBox:
    """
    A text input box it executes a command after clicking enter

    Attributes
        center: (x,y)
            the center of the button in pixels
        command:
            the method to be executed upon clicking enter
        args:
            the arguments to pass to the method
        initial_text:
            the string that should be displayed when the input box is empty

    Methods
        render(screen)
            renders the text input box on the screen
        handle_event(event)
            handles the passed event
    """

    def __init__(self, center, command, args, initial_text):
        self.center = center
        self.command = command
        self.args = args
        self.initial_text = initial_text
        self.text = ""
        self.font = pygame.font.SysFont(*FONT)
        self.text_rect = self.font.render(self.initial_text, True, FONT_COLOR)
        self.top_left = tuple(x - y // 2 for x, y in zip(self.center, self.text_rect.get_size()))
        self.rect = pygame.rect.Rect(*self.top_left, *self.text_rect.get_size())
        self.active = False
        self.correct = True

    def render(self, screen):
        """
        :param screen: the screen the input box should be drawn on
        :return: draws the input box on the screen, it glows red if the text is incorrect
        """
        if self.text == '':
            self.text_rect = self.font.render(self.initial_text, True, FONT_COLOR)
        else:
            self.text_rect = self.font.render(self.text, True, FONT_COLOR)
        Shapes.draw_rect(screen, self.center, self.text_rect.get_size(),
                         BACKGROUND_COLOR if self.correct else (255, 0, 0, 150))
        Shapes.draw_text(screen, self.center, self.initial_text if self.text == '' else self.text, FONT, FONT_COLOR)

    def handle_event(self, event):
        """
        :param event: the pygame.event to be handled
        :return: if the text input box is
            clicked on - it is ready to receive keyboard inputs
                if the key is backspace - it deletes the last character
                if the key is delete - it deletes the whole input
                if the key is enter - it executes the command, and sets itself to incorrect,
                                      if the method says that the text is incorrect
                if the key is any other - pass it to the string
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.correct = self.command(self.args, self.text)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                    self.correct = True
                elif event.key == pygame.K_DELETE:
                    self.text = ''
                    self.correct = True
                else:
                    self.text += event.unicode
                    self.correct = True
