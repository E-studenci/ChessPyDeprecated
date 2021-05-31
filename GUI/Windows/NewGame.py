import multiprocessing

if multiprocessing.current_process().name == 'MainProcess':
    import pygame

from GUI.Items.TextInputBox import TextInputBox
from GUI.Constants import Display, Font, Colors
from GUI.Items.DropDownMenu import DropDownMenu
from GUI.Items.MenuButton import MenuButton
from GUI.Windows import GameScreen
from GameManagerPackage.GameManager import GameManager
from GameManagerPackage.PlayerClock import PlayerClock
from GameManagerPackage.Players.PlayerConstructors import *

NUMBER_OF_DROP_DOWN_MENUS = 2
DROP_DOWN_MENUS_STARTING_POSITION = (Display.CENTER[0], Display.CENTER[1] - 150)
START_GAME_BUTTON_STARTING_POSITION = (Display.CENTER[0], Display.CENTER[1] + 100)

START_GAME_BUTTON_SIZE = (200, 50)
DROP_DOWN_MENU_SIZE = (200, 50)
OFFSET = DROP_DOWN_MENU_SIZE[1] + 5

PLAYERS_DICTIONARY = {"HUMAN":       constructors["human"],
                      "BOT RANDOM":  constructors["random_bot"],
                      "BOT WRITTEN": constructors["alpha_beta_handcrafted_bot"],
                      "BOT NEURAL":  constructors["alpha_beta_neural_bot"]}

CHOICES = list(PLAYERS_DICTIONARY.keys())
DROP_DOWN_MENUS_TEXT = [("PLAYER ONE", CHOICES),
                        ("PLAYER TWO", CHOICES)]


def start_new_game(args, fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
    """
    Starts the game

    :param args: (screen, clock, background)
    """
    screen = args[0]
    clock = args[1]
    background = args[2]
    background.render(screen)
    text_input_boxes_initial = ["PLAYER ONE NAME", "PLAYER TWO NAME"]
    text_input_boxes_functionality = [(None, (screen, clock, background))] * 2
    text_input_boxes = add_text_input_boxes(screen, text_input_boxes_functionality, text_input_boxes_initial, 11)
    drop_down_menus = add_drop_down_menus(screen, DROP_DOWN_MENUS_TEXT)
    start_game_button = MenuButton(START_GAME_BUTTON_STARTING_POSITION, start_game,
                                   (drop_down_menus, fen, screen, (screen, clock, background), text_input_boxes),
                                   START_GAME_BUTTON_SIZE, Colors.BUTTON_BACKGROUND_COLOR,
                                   Font.FONT, Font.FONT_COLOR,
                                   1.2, 5,
                                   "Start Game")
    running_loop(screen, clock, background, drop_down_menus, start_game_button, text_input_boxes)


def running_loop(screen, clock, background, drop_down_menus, start_game_button, text_input_boxes):
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
            for text_input_box in text_input_boxes:
                text_input_box.handle_event(event)
            for drop_down_menu in drop_down_menus:
                drop_down_menu.handle_event(event)
        background.render(screen)
        for drop_down_menu in drop_down_menus:
            drop_down_menu.render(screen)
        for text_input_box in text_input_boxes:
            text_input_box.render(screen)
        if can_start_game(drop_down_menus):
            start_game_button.render(screen, start_game_button.rect.collidepoint(pygame.mouse.get_pos()))
        clock.tick(Display.MAX_FPS)
        pygame.display.flip()


def add_text_input_boxes(screen, text_input_box_functionality, initial_messages, max_size):
    """
    :returns a list of text_input_boxes with selected functionality
    """
    text_input_boxes = []
    for index in range(len(text_input_box_functionality)):
        center = (DROP_DOWN_MENUS_STARTING_POSITION[0], DROP_DOWN_MENUS_STARTING_POSITION[1] + OFFSET * index * 2)
        center = (center[0], center[1] - 37)
        text_input_box = TextInputBox(center,
                                      *text_input_box_functionality[index],
                                      initial_messages[index],
                                      Colors.TEXT_INPUT_BOX_COLOR_ACTIVE,
                                      Colors.TEXT_INPUT_BOX_COLOR_INACTIVE,
                                      Colors.TEXT_INPUT_BOX_COLOR_INCORRECT,
                                      Font.FONT, Font.FONT_COLOR, max_size=max_size)
        text_input_box.render(screen)
        text_input_boxes.append(text_input_box)
    return text_input_boxes


def add_drop_down_menus(screen, text):
    drop_down_menus = []
    for index in range(NUMBER_OF_DROP_DOWN_MENUS):
        center = (DROP_DOWN_MENUS_STARTING_POSITION[0], DROP_DOWN_MENUS_STARTING_POSITION[1] + OFFSET * index * 2)
        menu = DropDownMenu(
            [Colors.DROP_DOWN_MENU_MAIN_INACTIVE, Colors.DROP_DOWN_MENU_MAIN_ACTIVE],
            [Colors.DROP_DOWN_MENU_OPTIONS_INACTIVE, Colors.DROP_DOWN_MENU_OPTIONS_ACTIVE],
            center, DROP_DOWN_MENU_SIZE,
            Font.FONT,
            *text[index],
            Font.FONT_COLOR)
        menu.render(screen)
        drop_down_menus.append(menu)
    return drop_down_menus


def can_start_game(drop_down_menus):
    """
    :param drop_down_menus: menus used to select players
    :returns True if both players have been selected in [drop_down_menus] else False
    """
    for index in range(len(drop_down_menus)):
        if drop_down_menus[index].main == DROP_DOWN_MENUS_TEXT[index][0]:
            return False
    return True


def start_game(args):
    """
    Invokes GameScreen.start_game(args) with a game created with iboth players
    """
    player_one_color = bool(random.randint(0, 1))
    players = []
    for i in range(len(args[0])):
        player_name = None if args[4][i].text == args[4][i].initial_text else args[4][i].text
        color = player_one_color if i == 0 else not player_one_color
        players.append(PLAYERS_DICTIONARY[args[0][i].main](name=player_name, color=color, player_clock=PlayerClock()))
    game = GameManager(players[0], players[1], args[1])
    args = args[3]
    GameScreen.start_game(args, game, player_one_color)
