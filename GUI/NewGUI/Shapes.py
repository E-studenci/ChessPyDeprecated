import pygame


def draw_rect(screen, size, center, color):
    s = pygame.Surface(size)
    s.set_alpha(color[3])
    s.fill(color)
    s_rect = s.get_rect()
    s_rect.center = center
    screen.blit(s, s_rect)


def draw_text(screen, center, text, font, color):
    font = pygame.font.SysFont(*font)
    text = font.render(text, True, color)
    text_rect = text.get_rect()
    text_rect.center = center
    screen.blit(text, text_rect)
