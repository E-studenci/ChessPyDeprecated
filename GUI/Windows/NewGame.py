import random

from GUI import Constants
from GUI.Backgrounds.ChessBackground import ChessBackground
from GUI.Constants import *
import pygame

from GUI.Items.DropDownMenu import DropDownMenu
from GUI.Items.MenuButton import MenuButton
from GameManagerPackage.GameManager import GameManager
from GameManagerPackage.Players.BotRandom import BotRandom
from GameManagerPackage.Players.Human import Human

CENTER = (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2)

NUMBER_OF_DROP_DOWN_MENUS = 2
DROP_DOWN_MENUS_STARTING_POSITION = (CENTER[0], CENTER[1] - 150)

DROP_DOWN_MENU_SIZE = (200, 50)
OFFSET = DROP_DOWN_MENU_SIZE[1] + 5

CHOICES = ["Human", "Bot Random"]
DROP_DOWN_MENUS_TEXT = [("Player One", CHOICES),
                        ("Player Two", CHOICES)]
PLAYERS_DICTIONARY = {"Human":      Human,
                      "Bot Random": BotRandom}


def start_new_game(args, fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
    screen = args[0]
    clock = args[1]
    background = args[2]
    screen.fill(pygame.Color("white"))
    background.render(screen)

    drop_down_menus = add_drop_down_menus(screen, DROP_DOWN_MENUS_TEXT)
    start_game_button = MenuButton(CENTER, start_game, (drop_down_menus, fen), (200, 50), "Start Game")
    running_loop(screen, clock, background, drop_down_menus, start_game_button)


def running_loop(screen, clock, background, drop_down_menus, start_game_button):
    running = True
    while running:
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT \
                    or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                break
            if can_start_game(drop_down_menus):
                start_game_button.handle_event(event)
        background.render(screen)
        for drop_down_menu in drop_down_menus:
            selected_option = drop_down_menu.update(event_list)
            if selected_option >= 0:
                drop_down_menu.main = drop_down_menu.options[selected_option]
            drop_down_menu.render(screen)
        if can_start_game(drop_down_menus):
            start_game_button.render(screen,
                                     True if start_game_button.rect.collidepoint(pygame.mouse.get_pos()) else False)
        clock.tick(MAX_FPS)
        pygame.display.flip()


def add_drop_down_menus(screen, text):
    drop_down_menus = []
    for index in range(NUMBER_OF_DROP_DOWN_MENUS):
        center = (DROP_DOWN_MENUS_STARTING_POSITION[0], DROP_DOWN_MENUS_STARTING_POSITION[1] + OFFSET * index)
        menu = DropDownMenu(
            [(0, 0, 0, 150), (0, 0, 0, 255)],
            [(0, 0, 0, 150), (0, 0, 0, 255)],
            center, DROP_DOWN_MENU_SIZE,
            ('arial', FONT_SIZE, True, False),
            *text[index])
        menu.render(screen)
        drop_down_menus.append(menu)
    return drop_down_menus


def can_start_game(drop_down_menus):
    for index in range(len(drop_down_menus)):
        if drop_down_menus[index].main == DROP_DOWN_MENUS_TEXT[index][0]:
            return False
    return True


def start_game(args):
    player_one_color = bool(random.randint(0, 1))
    players = []
    for i in range(len(args[0])):
        color = player_one_color if i == 0 else not player_one_color
        if args[0][i].main == CHOICES[0]:
            players.append(PLAYERS_DICTIONARY[args[0][i].main]("aaa",
                                                               color,
                                                               select_move))
        else:
            players.append(PLAYERS_DICTIONARY[args[0][i].main]("aaa",
                                                               color))
    game = GameManager(players[0], players[1], args[1])
    print(players)
    pass


def select_move():
    pass
