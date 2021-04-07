import pygame


def draw_rect(screen, center, size, color):
    """
    :param screen: the screen the rectangle should be rendered on
    :param center: (x,y) the center of the rectangle in pixels
    :param size: (width, height) the size of the rectangle in pixels
    :param color: (r,g,b,a) the color of the rectangle
    :return: draws the rectangle on the screen
    """
    s = pygame.Surface(size)
    s.set_alpha(color[3])
    s.fill(color)
    s_rect = s.get_rect()
    s_rect.center = center
    screen.blit(s, s_rect)


def draw_text(screen, center, text, font, color):
    """
    :param screen: the screen the text should be rendered on
    :param center: the center of the text
    :param text: string the content of the text
    :param font: (font_name, font_size, bold, italic) the font of the text
    :param color: (r,g,b) the color of the font
    :return: renders the text on the screen
    """
    font = pygame.font.SysFont(*font)
    text = font.render(text, True, color)
    text_rect = text.get_rect()
    text_rect.center = center
    screen.blit(text, text_rect)