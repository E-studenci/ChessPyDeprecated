import multiprocessing

if multiprocessing.current_process().name == 'MainProcess':
    import pygame
from queue import Queue
from Chess.Pieces.Bishop import Bishop
from Chess.Pieces.Knight import Knight
from Chess.Pieces.Queen import Queen
from Chess.Pieces.Rook import Rook
from GUI import Shapes
from GUI.Backgrounds import ChessBoard
from GUI.Constants import Display, Font, Options, Colors
from GUI.Constants.BoardConst import *
import threading
from GUI.Backgrounds.SpritesLoaded import SPRITE_DICTIONARY
from GUI.Items.MenuButton import MenuButton
from GameManagerPackage.GameManager import GameManager

from GameManagerPackage.GameStatus import GameStatus
from Paths import FOLDER_PATHS

DISPLAY_WIDTH_EXTENSION = 200


def start_game(args, game, player_one_color):
    """
    Starts a game and the running_loop
    """
    screen = args[0]
    clock = args[1]
    args[2].pause = True

    ChessBoard.draw_board(screen, (0, 0))
    q1 = Queue(maxsize=0)
    q2 = Queue(maxsize=0)
    q3 = Queue(maxsize=0)
    t = threading.Thread(target=game.start_game, args=(q1, q2, q3))
    t.daemon = True
    t.start()
    screen = pygame.display.set_mode((Display.DISPLAY_WIDTH + DISPLAY_WIDTH_EXTENSION, Display.DISPLAY_HEIGHT))
    screen.fill(pygame.color.Color("#B27F54"))
    draw_button = MenuButton((Display.DISPLAY_WIDTH + DISPLAY_WIDTH_EXTENSION // 2, Display.CENTER[1]),
                             GameManager.draw, game, (100, 50), Colors.BUTTON_BACKGROUND_COLOR,
                             Font.FONT, Font.FONT_COLOR, 1.1, 5, "Draw")
    move_sounds = load_sounds(["Move.mp3", "Capture.mp3"])
    running_loop(screen, clock, args[2], q1, q2, q3, game, player_one_color, draw_button, move_sounds)


def load_sounds(file_names):
    ret_list = []
    for file in file_names:
        ret_list.append(pygame.mixer.Sound(f"{FOLDER_PATHS['Sounds']}/{file}"))
    return ret_list


def running_loop(screen, clock, background, q1, q2, q3, game, player_one_color, draw_button, sounds):
    running = True
    selecting_move = False
    game_ended = False
    do_select_move = False
    start_pos, move = -1, -1
    planning = []
    if game.player_one.is_bot and game.player_two.is_bot:
        do_select_move = False
    while running:
        # updating flags
        temp = q3.get()
        game_status = temp[1]
        if temp[0] is not None:
            do_select_move = not temp[0]
        if game_status != GameStatus.ONGOING:
            game_ended = True
        if do_select_move and not game_ended:
            if not selecting_move:
                moves = q2.get()
                if moves:
                    selecting_move = True
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT \
                    or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                background.pause = False
                game.kill = True
                screen = pygame.display.set_mode((Display.DISPLAY_WIDTH, Display.DISPLAY_HEIGHT))
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    index = get_square_index(pygame.mouse.get_pos())
                    if index in planning:
                        planning.remove(index)
                    else:
                        planning.append(index)
                    start_pos, move = -1, -1
                if event.button == 1:
                    planning.clear()
                    if do_select_move and not game_ended and selecting_move:
                        sq_index = get_square_index(pygame.mouse.get_pos())
                        if sq_index != start_pos:
                            if sq_index in moves.keys() and moves[sq_index]:
                                start_pos = sq_index
                                move = -1
                            elif start_pos != -1:
                                # choosing promotion
                                if move != -1 and move[1] == -1:
                                    move, start_pos = choose_promotion(move, sq_index, start_pos)
                                # choosing any legal move
                                else:
                                    move, start_pos = choose_move(moves, sq_index, start_pos)
                            else:
                                start_pos, move = -1, -1
            draw_button.handle_event(event)
        if do_select_move and not game_ended:
            if start_pos != -1 and move != -1:
                if move[1] != -1:
                    selecting_move = False
                    q1.put((start_pos, move))
                    q2.task_done()
                    start_pos, move = -1, -1
        screen.fill(pygame.color.Color("#B27F54"))
        ChessBoard.draw_board(screen, (0, 0))
        ChessBoard.draw_pieces(screen, game.board, True)
        draw_player_names(screen,
                          (game.player_one.name, game.player_two.name) if player_one_color else
                          (game.player_two.name, game.player_one.name),
                          (game.player_one.clock.get_time(), game.player_two.clock.get_time()) if player_one_color else
                          (game.player_two.clock.get_time(), game.player_one.clock.get_time()),
                          Font.FONT, Font.FONT_COLOR, Colors.BUTTON_BACKGROUND_COLOR)
        draw_button.render(screen, draw_button.rect.collidepoint(pygame.mouse.get_pos()))
        draw_planning(screen, planning)
        if start_pos != -1:
            if move == -1:
                # if chosen a start square, draw rectangles signalling possible moves
                draw_possible_moves(screen, moves[start_pos])
            else:
                # if chosen move leads to promotion, draw pieces depicting available promotions
                draw_promotions(screen, move[0])
        if game_ended:
            Shapes.draw_rect(screen, Display.CENTER,
                             pygame.font.SysFont(*Font.FONT).render(game_status.name, True, Font.FONT_COLOR).get_size(),
                             Colors.BUTTON_BACKGROUND_COLOR)
            Shapes.draw_text(screen, Display.CENTER, str(game_status.name), Font.FONT, Font.FONT_COLOR)
        if temp[2][0]:
            play_sound(sounds, temp[2][1])
        clock.tick(Display.MAX_FPS)
        q3.task_done()
        pygame.display.flip()


def draw_player_names(screen, player_names, player_timers, font, font_color, background_color):
    """
    :param screen: the screen the names should be rendered on
    :param player_names: (name of player one, name of player two)
    :param player_timers: [string]: the timers for each player
    :param font: (font_name, font_size, bold, italic) the font of the text
    :param font_color: (r,g,b) the color of the font
    :param background_color: color in the background of the name
    """
    for i in range(2):
        font_ = pygame.font.SysFont(*font)
        text_rect = font_.render(player_names[i], True, font_color)
        center = (BOARD_SIZE[0] + DISPLAY_WIDTH_EXTENSION // 2,
                  (Display.DISPLAY_HEIGHT - text_rect.get_size()[1]) * (1 - i) + text_rect.get_size()[1] // 2 * (
                      -1) ** (i + 1))
        if player_names[i]:
            Shapes.draw_text(screen, center, player_names[i], font, font_color)
        center = (center[0], center[1] + text_rect.get_size()[1])
        Shapes.draw_text(screen, center, player_timers[i], font, font_color)


def play_sound(sounds, take):
    if Options.SOUND:
        if take:
            sounds[1].play()
        else:
            sounds[0].play()


def choose_move(moves, sq_index, start_pos):
    """
    :param moves: all legal moves
    :param sq_index: selected square
    :param start_pos: starting pos the piece
    :return: returns the selected move, if [sq_index] doesn't match any available move, returns -1,-1
    """
    amount_of_possible_moves = 0
    first_occurrence_index = -1
    for i in range(len(moves[start_pos])):
        if sq_index == moves[start_pos][i][0]:
            amount_of_possible_moves += 1
            if first_occurrence_index == -1:
                first_occurrence_index = i
    if amount_of_possible_moves == 1:
        move = moves[start_pos][first_occurrence_index]
    elif amount_of_possible_moves > 1:
        move = (moves[start_pos][first_occurrence_index][0], -1)
    # chosen a non legal move square
    else:
        start_pos, move = -1, -1
    return move, start_pos


def choose_promotion(move, sq_index, start_pos):
    """
    :param move: move of the pawn
    :param sq_index: selected piece to promote to
    :param start_pos: starting pos of the pawn
    :return: returns the selected promotion, if [sq_index] doesn't match any available promotion, returns -1,-1
    """
    for i in range(4):
        if sq_index == move[0] + i * 8 \
                or sq_index == move[0] - i * 8:
            move = (move[0], i + 1)
    if move[1] == -1:
        start_pos, move = -1, -1
    return move, start_pos


def draw_planning(screen, planning):
    """
    :param screen: the screen the moves should be rendered on
    :param planning: planned squares
    :return: draws indicators on the squares passed in [planning]
    """
    if planning:
        for i in range(8):
            for j in range(8):
                index = i * 8 + j
                if any(index == index_ for index_ in planning):
                    top_left = get_top_left_from_index(index)
                    center = (top_left[0] + SQUARE_SIZE // 2, top_left[1] + SQUARE_SIZE // 2)
                    Shapes.draw_circle(screen, center, 20, (100, 0, 0, 150))


def draw_possible_moves(screen, moves):
    """
    :param screen: the screen the moves should be rendered on
    :param moves: legal moves square indexes
    :return: draws indicators on the squares passed in [moves]
    """
    mouse_pos_index = get_square_index(pygame.mouse.get_pos())
    for i in range(8):
        for j in range(8):
            index = i * 8 + j
            if any(index == move[0] for move in moves):
                top_left = (j * SQUARE_SIZE, (7 - i) * SQUARE_SIZE)
                center = (top_left[0] + SQUARE_SIZE // 2, top_left[1] + SQUARE_SIZE // 2)
                if mouse_pos_index != index:
                    Shapes.draw_circle(screen, center, 10, (0, 100, 0, 200))
                else:
                    Shapes.draw_rect(screen, center, (SQUARE_SIZE, SQUARE_SIZE), (0, 100, 0, 100))


def draw_promotions(screen, target_square_index):
    """
    :param screen: the screen the promotions should be rendered on
    :param target_square_index: the square from which the promotions should be drawn
    :return: draws possible promotions in a straight line from [target_square_index]
    """
    mouse_pos_index = get_square_index(pygame.mouse.get_pos())
    pieces = {0: SPRITE_DICTIONARY[(Knight, False)],
              1: SPRITE_DICTIONARY[(Bishop, False)],
              2: SPRITE_DICTIONARY[(Rook, False)],
              3: SPRITE_DICTIONARY[(Queen, False)],
              4: SPRITE_DICTIONARY[(Knight, True)],
              5: SPRITE_DICTIONARY[(Bishop, True)],
              6: SPRITE_DICTIONARY[(Rook, True)],
              7: SPRITE_DICTIONARY[(Queen, True)]}
    for i in range(4):
        square = target_square_index + i * 8 if target_square_index // 8 == 0 else target_square_index - i * 8
        top_left = get_top_left_from_index(square)
        Shapes.draw_rect(screen,
                         (top_left[0] + SQUARE_SIZE // 2, top_left[1] + SQUARE_SIZE // 2),
                         (SQUARE_SIZE, SQUARE_SIZE),
                         ((0, 0, 0, 150) if not (target_square_index // 8 == 0) else (255, 255, 255, 150))
                         if mouse_pos_index != square else (0, 100, 0, 150))
        screen.blit(pieces[i if target_square_index // 8 == 0 else i + 4], top_left)


def get_top_left_from_index(index):
    """
    :param index: square index
    :return: returns coordinates of the top left corner of the square
    """
    row = index // 8
    column = index % 8
    return column * SQUARE_SIZE, (7 - row) * SQUARE_SIZE


def get_square_index(mouse_pos):
    """
    :param mouse_pos: current mouse pos (x,y)
    :return: returns square index based on coordinates
    """
    x = mouse_pos[0]
    y = mouse_pos[1]
    column = x // SQUARE_SIZE
    row = (7 - y // SQUARE_SIZE) * 8
    index = row + column
    return index
