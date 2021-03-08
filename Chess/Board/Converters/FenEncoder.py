from Chess.Pieces import Bishop, King, Knight, Pawn, Queen, Rook, Piece
from Chess.Board.Converters import ChessNotationConverter as Converter
from Chess.Board.Converters import FenDecoder as Fn

piece_dictionary = {(Pawn.Pawn, False): 'p', (Pawn.Pawn, True): 'P',
                    (Knight.Knight, False): 'n', (Knight.Knight, True): 'N',
                    (Bishop.Bishop, False): 'b', (Bishop.Bishop, True): 'B',
                    (Rook.Rook, False): 'r', (Rook.Rook, True): 'R',
                    (Queen.Queen, False): 'q', (Queen.Queen, True): 'Q',
                    (King.King, False): 'k', (King.King, True): 'K',
                    }

castle_dictionary = {0: 'K', 1: 'Q', 2: 'k', 3: 'q'}

en_passant_square_index = -1
castling = [False, False, False, False]


def to_name_later(chess_board: list, turn: bool, fifty_move_rule: int, move_count: int) -> str:
    result_fen: str = ""

    # --------------------------PARSE_BOARD--------------------------
    temp_list: list = []
    for index in range(len(chess_board)):
        obj = chess_board[index]
        temp_list.append(obj)

        if index % 8 == 7:
            result_fen = parse_sublist(temp_list) + result_fen
            temp_list = []
    result_fen = result_fen[:-1]
    # --------------------------PARSE_TURN--------------------------

    result_fen += parse_turn(turn)

    # ------------------------PARSE_CASTLING------------------------

    result_fen += parse_castling()

    # -----------------------PARSE_EN_PASSANT-----------------------

    result_fen += ' ' + Converter.convert_index_into_chess_notation(en_passant_square_index)

    # ----------------------PARSE_50_MOVE_RULE----------------------

    result_fen += ' ' + str(fifty_move_rule)

    # -----------------------PARSE_MOVE_COUNT-----------------------

    result_fen += ' ' + str(move_count)

    print(result_fen)

    return result_fen


def parse_sublist(row: list) -> str:
    result_string: str = ""
    space: int = 0
    for index in range(len(row)):
        obj = row[index]
        if obj is not None:
            if space != 0:
                result_string += str(space)
            space = 0
            result_string += piece_dictionary[(type(obj), obj.color)]

            fulfill_conditions(obj)
        elif index + 1 == len(row):
            result_string += str(space + 1)
        else:
            space += 1
    result_string += '/'
    return result_string


def fulfill_conditions(obj):
    if type(obj) is Pawn.Pawn and check_for_en_passant(obj) != -1:
        global en_passant_square_index
        en_passant_square_index = check_for_en_passant(obj)

    if type(obj) is King.King:
        check_for_castling(obj)


def parse_turn(turn: bool) -> str:
    if turn:
        return " w"
    else:
        return " b"


def check_for_en_passant(pawn: Pawn.Pawn):
    if pawn.en_passant:
        result_index: int = pawn.position
        if pawn.color:
            return result_index - 8
        elif not pawn.color:
            return result_index + 8
    return -1


def check_for_castling(king: King.King):
    global castling
    if king.color:
        if king.castle_king_side:
            castling[0] = True
        if king.castle_queen_side:
            castling[1] = True
    elif not king.color:
        if king.castle_king_side:
            castling[2] = True
        if king.castle_queen_side:
            castling[3] = True


def parse_castling() -> str:
    global castling
    return_string: str = " "
    for index in range(len(castling)):
        if castling[index]:
            return_string += castle_dictionary[index]
    if return_string == " ":
        return_string += '-'
    return return_string


if __name__ == '__main__':
    arg1, arg2, arg3, arg4 = Fn.initialize_list_from_FEN("rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2")
    to_name_later(arg1, arg2, arg3, arg4)

