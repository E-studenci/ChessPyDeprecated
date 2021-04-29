import pygame


def draw_rect(screen, center, size, color):
    """
    Draws a rectangle on the screen

    :param screen: the screen the rectangle should be rendered on
    :param center: (x,y) the center of the rectangle in pixels
    :param size: (width, height) the size of the rectangle in pixels
    :param color: (r,g,b,a) the color of the rectangle
    """
    s = pygame.Surface(size)
    s.set_alpha(color[3])
    s.fill(color)
    s_rect = s.get_rect()
    s_rect.center = center
    screen.blit(s, s_rect)


def draw_circle(screen, center, radius, color, filled=True):
    """
    Draws a circle on the screen

    :param screen: the screen the rectangle should be rendered on
    :param center: (x,y) the center of the rectangle in pixels
    :param radius: the radius of the circle
    :param color: the color of the circle
    :param filled: should it be filled?
    """
    from pygame import gfxdraw
    gfxdraw.aacircle(screen, int(center[0]), int(center[1]), int(radius), color)
    if filled:
        gfxdraw.filled_circle(screen, int(center[0]), int(center[1]), int(radius), color)


def draw_text(screen, center, text, font, color):
    """
    Renders the text on the screen

    :param screen: the screen the text should be rendered on
    :param center: the center of the text
    :param text: string the content of the text
    :param font: (font_name, font_size, bold, italic) the font of the text
    :param color: (r,g,b) the color of the font
    """
    font = pygame.font.SysFont(*font)
    text = font.render(text, True, color)
    text_rect = text.get_rect()
    text_rect.center = center
    screen.blit(text, text_rect)
