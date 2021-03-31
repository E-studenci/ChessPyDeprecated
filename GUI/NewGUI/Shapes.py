import pygame


def draw_rect(screen, size, center, color):
    s = pygame.Surface(size)
    s.set_alpha(color[3])
    s.fill(color)
    s_rect = s.get_rect()
    s_rect.center = center
    screen.blit(s, s_rect)
