from Chess.Pieces import Bishop, King, Knight, Pawn, Queen, Rook, Piece
from Chess.Board.Converters import ChessNotationConverter as Converter

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
    """
    :param chess_board: the board to parse into FEN
    :param turn: current turn: white: True, black: False
    :param fifty_move_rule: fifty move rule counter status
    :param move_count: moves since the beginning of the game
    :return: returns the state of the game in FEN
    """
    # --------------------------PARSE_BOARD--------------------------
    result_fen = parse_board(chess_board)
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

    return result_fen


def parse_board(chess_board):
    temp_list: list = []
    result_fen = ""
    for index in range(len(chess_board)):
        obj = chess_board[index]
        temp_list.append(obj)

        if index % 8 == 7:
            result_fen = parse_sublist(temp_list) + result_fen
            temp_list = []
    result_fen = result_fen[:-1]
    return result_fen


def parse_sublist(row: list) -> str:
    """
    :param row: list, a list of pieces representing a row
    :return: converts row to string using FEN
    """
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
    """
    :param obj: A piece to check
    :return: if the piece is a pawn, or a king, it sets en_passant, and castling flags accordingly
    """
    if type(obj) is Pawn.Pawn and check_for_en_passant(obj) != -1:
        global en_passant_square_index
        en_passant_square_index = check_for_en_passant(obj)

    if type(obj) is King.King:
        check_for_castling(obj)


def parse_turn(turn: bool) -> str:
    """
    :param turn: bool, current turn
    :return: converts current turn to FEN
    """
    if turn:
        return " w"
    else:
        return " b"


def check_for_en_passant(pawn: Pawn.Pawn):
    """
    :param pawn: a pawn to check
    :return: if the pawn's en_passant flag is true, the method retuns the index of the target square
    """
    if pawn.en_passant:
        result_index: int = pawn.position
        if pawn.color:
            return result_index - 8
        elif not pawn.color:
            return result_index + 8
    return -1


def check_for_castling(king: King.King):
    """
    :param king: a king to check
    :return: sets castling flags based on the king's ability to castle
    """
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
    """
    :return: Converts castling flags to FEN
    """
    global castling
    return_string: str = " "
    for index in range(len(castling)):
        if castling[index]:
            return_string += castle_dictionary[index]
    if return_string == " ":
        return_string += '-'
    return return_string

