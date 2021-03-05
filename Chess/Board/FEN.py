from Chess.Pieces import Bishop, King, Knight, Pawn, Piece, Queen, Rook


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
                if char is 'k' or char is 'K':
                    add_castle_flags_to_king(result_list[index], char, castling_ability)
                index += 1
            else:
                return [], True
        else:
            index -= 16

    return result_list, side_to_move


def add_castle_flags_to_king(king, char, castling_ability) -> None:
    if char is 'k':
        king.castle_king_side = castling_ability[0]
        king.castle_queen_side = castling_ability[1]
    elif char is 'K':
        king.castle_king_side = castling_ability[2]
        king.castle_queen_side = castling_ability[3]


def add_en_passant_flag_to_pawn(pawn, char) -> None:
    pass


# def show_list(result_list):
#     index = 0
#     for obj in result_list:
#         if index % 8 == 0:
#             print('')
#         if obj is not None:
#             print(obj.position, ' ', end='')
#         else:
#             print('    ', end='')
#         index += 1
