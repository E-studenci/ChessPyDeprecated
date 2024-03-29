import multiprocessing

if multiprocessing.current_process().name == 'MainProcess':
    import pygame

from GUI.Backgrounds.SpritesLoaded import LOGO
from GUI.Constants import Colors, Font, Display, BoardConst, Options
from GUI.Backgrounds.ChessBackground import ChessBackground
from GUI.Items.MenuButton import MenuButton
from GUI.Backgrounds import SpritesLoaded, ChessBoard
from GameManagerPackage.Players.PlayerConstructors import *

NUMBER_OF_BUTTONS = 5
BUTTON_SIZE = (240, 70)
BUTTON_GAP = 13
BUTTON_STARTING_POSITION = (Display.CENTER[0], Display.CENTER[1] - (3 * BUTTON_SIZE[1] + 3 * BUTTON_GAP) // 2)


def start_menu():
    """
    :return: initialize the menu screen
    """
    pygame.display.init()
    pygame.font.init()
    pygame.freetype.init()
    pygame.mixer.init()
    SpritesLoaded.initialize((BoardConst.SQUARE_SIZE, BoardConst.SQUARE_SIZE))
    from GUI.Windows.NewGame import start_new_game
    from GUI.Windows.LoadGame import start_load_game
    from GUI.Windows.Options import start_options
    from GUI.Windows.Leaderboards import start_leaderboards
    screen = pygame.display.set_mode((Display.DISPLAY_WIDTH, Display.DISPLAY_HEIGHT))
    pygame.display.set_icon(LOGO[0])
    ChessBoard.initialize(screen,
                          (Display.DISPLAY_WIDTH, Display.DISPLAY_HEIGHT))
    pygame.display.set_caption('')
    clock = pygame.time.Clock()
    background = ChessBackground((Display.DISPLAY_WIDTH, Display.DISPLAY_HEIGHT),
                                 constructors["random_bot"],
                                 constructors["alpha_beta_handcrafted_bot"],
                                 2)
    background.render(screen)
    button_functionality = [(start_new_game, (screen, clock, background), "START NEW GAME"),
                            (start_load_game, (screen, clock, background), "LOAD GAME"),
                            (start_leaderboards, (screen, clock, background), "LEADERBOARDS"),
                            (start_options, (screen, clock, background), "OPTIONS"),
                            (sys.exit, 0, "EXIT")]
    buttons = add_buttons(screen, button_functionality)
    load_music("music4.mp3")
    running_loop(screen, clock, buttons, background)


def running_loop(screen, clock, buttons, background):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            for button in buttons:
                if button.handle_event(event):
                    break
        background.render(screen)
        screen.blit(LOGO[0], LOGO[1])
        for button in buttons:
            button.render(screen, button.rect.collidepoint(pygame.mouse.get_pos()))
        clock.tick(Display.MAX_FPS)
        pygame.display.flip()


def add_buttons(screen, button_functionality):
    """
    :param screen: the screen the buttons should be rendered on
    :param button_functionality: a list of tuples (function, args, text)
    :return: a list of NUMBER_OF_BUTTONS buttons with chosen functionality and renders them
    """
    buttons = []
    offset = BUTTON_GAP + BUTTON_SIZE[1]

    for index in range(NUMBER_OF_BUTTONS):
        button_position = (BUTTON_STARTING_POSITION[0], BUTTON_STARTING_POSITION[1] + offset * index)
        button = MenuButton(button_position,
                            button_functionality[index][0],
                            button_functionality[index][1],
                            BUTTON_SIZE,
                            Colors.BUTTON_BACKGROUND_COLOR,
                            Font.FONT,
                            Font.FONT_COLOR,
                            1.2,
                            5,
                            button_functionality[index][2])
        button.render(screen)
        buttons.append(button)
    return buttons


def load_music(song):
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.load(f"{FOLDER_PATHS['Sounds']}/{song}")
    pygame.mixer.music.play(loops=-1)
    if not Options.MUSIC:
        pygame.mixer.music.pause()
