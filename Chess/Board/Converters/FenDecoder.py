from Chess.Pieces import Bishop, King, Knight, Pawn, Queen, Rook
from Chess.Board.Converters import ChessNotationConverter as Converter


def initialize_list_from_FEN(fen: str):
    """
    :param fen: string game to load in FEN
    :return: returns a tuple: (board in form of list of pieces, current turn, fifty_move_rule counter, move counter, king_pos)
    """

    piece_dictionary = {'p': lambda: Pawn.Pawn(False, 0), 'P': lambda: Pawn.Pawn(True, 0),
                        'n': lambda: Knight.Knight(False, 0), 'N': lambda: Knight.Knight(True, 0),
                        'b': lambda: Bishop.Bishop(False, 0), 'B': lambda: Bishop.Bishop(True, 0),
                        'r': lambda: Rook.Rook(False, 0), 'R': lambda: Rook.Rook(True, 0),
                        'q': lambda: Queen.Queen(False, 0), 'Q': lambda: Queen.Queen(True, 0),
                        'k': lambda: King.King(False, 0), 'K': lambda: King.King(True, 0)
                        }

    castle_dictionary = {'K': 0, 'Q': 1, 'k': 2, 'q': 3}

    fen_string_list: list = fen.split(' ')

    piece_positions: str = fen_string_list[0]

    side_to_move: bool = True if fen_string_list[1] == 'w' else False

    king_pos = {True: -1,
                False: -1}

    castling_ability = [False] * 4
    if fen_string_list[2] != '-':
        for char in fen_string_list[2]:
            castling_ability[castle_dictionary[char]] = True

    result_list = [None] * 64

    index: int = 56
    for char in piece_positions:
        if char != '/':
            if char.isnumeric() and 8 >= int(char) > 0:
                index += int(char)
            elif char.isalpha():
                result_list[index] = piece_dictionary[char]()
                result_list[index].position = index
                if char == 'k' or char == 'K':
                    add_castle_flags_to_king(result_list[index], char, castling_ability)
                    if char == 'k':
                        king_pos[False] = index
                    else:
                        king_pos[True] = index
                index += 1
            else:
                return [], True, 0, 0
        else:
            index -= 16

    if fen_string_list[3] != '-':
        add_en_passant_flag_to_pawn(result_list, fen_string_list[3])

    halfmove_clock: int = int(fen_string_list[4])

    fullmove_counter: int = int(fen_string_list[5])

    return result_list, side_to_move, halfmove_clock, fullmove_counter, king_pos


def add_castle_flags_to_king(king, char, castling_ability) -> None:
    """
    :param king: the king to set castling flags on
    :param char: the color of the king represented by lower or uppercase "k"
    :param castling_ability: flags representing castling in the form of a
       bool list: [black_king_side, black_queen_side, white_k_s, white_q_s]
    :return:sets the castling flags for the king according to castling_ability
    """
    if char == 'K':
        king.castle_king_side = castling_ability[0]
        king.castle_queen_side = castling_ability[1]
    elif char == 'k':
        king.castle_king_side = castling_ability[2]
        king.castle_queen_side = castling_ability[3]


def add_en_passant_flag_to_pawn(result_list, string) -> None:
    """
    :param result_list:
    :param string: position on the board in the form of a string: "column_letter + row_number"
    :return: sets the en_passant flag for the appropriate pawn to True
    """
    index: int = 0
    if string[1] == '3':
        index = Converter.convert_chess_notation_into_index(string) + 8
    elif string[1] == '6':
        index = Converter.convert_chess_notation_into_index(string) - 8

    if type(result_list[index]) is Pawn.Pawn:
        result_list[index].en_passant = True
