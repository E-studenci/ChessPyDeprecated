from Chess.Pieces import Bishop, King, Knight, Pawn, Piece, Queen, Rook
from Chess.Board import Converter as Converter


def initialize_list_from_FEN(fen: str):

    piece_dictionary = {'p': lambda: Pawn.Pawn(False, 0),     'P': lambda: Pawn.Pawn(True, 0),
                        'n': lambda: Knight.Knight(False, 0), 'N': lambda: Knight.Knight(True, 0),
                        'b': lambda: Bishop.Bishop(False, 0), 'B': lambda: Bishop.Bishop(True, 0),
                        'r': lambda: Rook.Rook(False, 0),     'R': lambda: Rook.Rook(True, 0),
                        'q': lambda: Queen.Queen(False, 0),   'Q': lambda: Queen.Queen(True, 0),
                        'k': lambda: King.King(False, 0),   'K': lambda: King.King(True, 0)
                        }

    castle_dictionary = {'K': 0, 'Q': 1, 'k': 2, 'q': 3}

    fen_string_list: list = fen.split(' ')

    piece_positions: str = fen_string_list[0]

    side_to_move: bool = True if fen_string_list[1] == 'w' else False

    castling_ability = [False] * 4
    if fen_string_list[3] != '-':
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
                index += 1
            else:
                return [], True
        else:
            index -= 16

    if fen_string_list[3] != '-':
        add_en_passant_flag_to_pawn(result_list, fen_string_list[3])

    halfmove_clock: int = int(fen_string_list[4])

    fullmove_counter: int = int(fen_string_list[5])

    return result_list, side_to_move, halfmove_clock, fullmove_counter


def add_castle_flags_to_king(king, char, castling_ability) -> None:
    if char == 'k':
        king.castle_king_side = castling_ability[0]
        king.castle_queen_side = castling_ability[1]
    elif char == 'K':
        king.castle_king_side = castling_ability[2]
        king.castle_queen_side = castling_ability[3]


def add_en_passant_flag_to_pawn(result_list, string) -> None:
    index: int = 0
    if string[1] == '3':
        index = Converter.convert_chess_notation_into_index(string) + 8
    elif string[1] == '6':
        index = Converter.convert_chess_notation_into_index(string) - 8

    if type(result_list[index]) is Pawn.Pawn:
        result_list[index].en_passant = True

