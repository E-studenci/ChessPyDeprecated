import multiprocessing

if multiprocessing.current_process().name == 'MainProcess':
    import pygame
from GUI import Shapes


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
        background_color_active: (r,g,b,a)
            the color of the box if active
        background_color_inactive: (r,g,b,a)
            the color of the box if inactive
        background_color_incorrect: (r,g,b,a)
            the color of the box if incorrect as per [command]
        font: (font_name, font_size, bold, italic)
            the font to be used
        font_color: (r,g,b,a)
            the font color to be used
        max_size: int
            the maximum size of the entered string

    Methods
        render(screen)
            renders the text input box on the screen
        handle_event(event)
            handles the passed event
    """

    def __init__(self, center, command, args, initial_text, background_color_active, background_color_inactive,
                 background_color_incorrect, font, font_color, max_size=99999999):
        self.center = center
        self.command = command
        self.args = args
        self.initial_text = initial_text
        self.text = ""
        self.background_color_active = background_color_active
        self.background_color_inactive = background_color_inactive
        self.background_color_incorrect = background_color_incorrect
        self.font = font
        self.font_color = font_color
        self.text_rect = pygame.font.SysFont(*self.font).render(self.initial_text, True, self.font_color)
        self.top_left = tuple(x - y // 2 for x, y in zip(self.center, self.text_rect.get_size()))
        self.rect = pygame.rect.Rect(*self.top_left, *self.text_rect.get_size())
        self.active = False
        self.correct = True
        self.max_size = max_size

    def render(self, screen):
        """
        Draws the input box on the screen, it glows red if the text is incorrect

        :param screen: the screen the input box should be drawn on
        """
        font = pygame.font.SysFont(*self.font)
        if self.text == '':
            self.text_rect = font.render(self.initial_text, True, self.font_color)
        else:
            self.text_rect = font.render(self.text, True, self.font_color)
        Shapes.draw_rect(screen, self.center, self.text_rect.get_size(),
                         (self.background_color_active if self.active else self.background_color_inactive)
                         if self.correct else self.background_color_incorrect)
        Shapes.draw_text(screen, self.center,
                         self.initial_text if self.text == '' else self.text,
                         self.font, self.font_color)

    def handle_event(self, event):
        """
        If the text input box is
            clicked on - it is ready to receive keyboard inputs
                if the key is backspace - it deletes the last character
                if the key is delete - it deletes the whole input
                if the key is enter - it executes the command, and sets itself to incorrect,
                                      if the method says that the text is incorrect
                if the key is any other - pass it to the string

        :param event: the pygame.event to be handled
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.command is not None:
                        self.correct = self.command(self.args, self.text)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                    self.correct = True
                elif event.key == pygame.K_DELETE:
                    self.text = ''
                    self.correct = True
                else:
                    if len(self.text) < self.max_size:
                        self.text += event.unicode
                        self.correct = True
