from Chess.Board.Converters.FenEncoder import piece_dictionary


def print_matrix_to_console(chess_board) -> None:
    """
    :param chess_board: list of Pieces: the chess board to print
    :return: prints a neat representation of the chess_board
    """

    chess_string = ["     0     1     2     3     4     5     6     7      ",
                    "  ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐   ",
                    "8 │     │     │     │     │     │     │     │     │ 56",
                    "  ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤   ",
                    "7 │     │     │     │     │     │     │     │     │ 48",
                    "  ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤   ",
                    "6 │     │     │     │     │     │     │     │     │ 40",
                    "  ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤   ",
                    "5 │     │     │     │     │     │     │     │     │ 32",
                    "  ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤   ",
                    "4 │     │     │     │     │     │     │     │     │ 24",
                    "  ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤   ",
                    "3 │     │     │     │     │     │     │     │     │ 16",
                    "  ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤   ",
                    "2 │     │     │     │     │     │     │     │     │ 8 ",
                    "  ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤   ",
                    "1 │     │     │     │     │     │     │     │     │ 0 ",
                    "  └─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┘   ",
                    "     A     B     C     D     E     F     G     H      "]

    for j in range(8):
        for i in range(8):
            obj = chess_board[(j * 8) + i]
            if obj is not None:
                chess_string[((7 - j) * 2) + 2] = chess_string[((7 - j) * 2) + 2][:((i + 1) * 6) - 1] + \
                                                  piece_dictionary[(type(obj), obj.color)] + \
                                                  chess_string[((7 - j) * 2) + 2][((i + 1) * 6):]
    print_chess_board(chess_string)


def print_chess_board(local_chess_board) -> None:
    """
    :param local_chess_board: a string of something, dunno
    :return: prints gut gut
    """
    for i in local_chess_board:
        print(i)
    print("------------------------------------------------------")