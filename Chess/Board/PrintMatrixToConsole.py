from Chess.Board.Converters.FenEncoder import piece_dictionary

chess_string = ["     A     B     C     D     E     F     G     H     ",
                "  ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐  ",
                "8 │     │     │     │     │     │     │     │     │ 8",
                "  ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤  ",
                "7 │     │     │     │     │     │     │     │     │ 7",
                "  ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤  ",
                "6 │     │     │     │     │     │     │     │     │ 6",
                "  ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤  ",
                "5 │     │     │     │     │     │     │     │     │ 5",
                "  ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤  ",
                "4 │     │     │     │     │     │     │     │     │ 4",
                "  ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤  ",
                "3 │     │     │     │     │     │     │     │     │ 3",
                "  ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤  ",
                "2 │     │     │     │     │     │     │     │     │ 2",
                "  ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤  ",
                "1 │     │     │     │     │     │     │     │     │ 1",
                "  └─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┘  ",
                "     A     B     C     D     E     F     G     H     "]


def print_matrix_to_console(chess_board) -> None:

    local_chess_board = chess_string
    for j in range(8):
        for i in range(8):
            obj = chess_board[(j * 8) + i]
            if obj is not None:
                local_chess_board[((7 - j) * 2) + 2] = local_chess_board[((7 - j) * 2) + 2][:((i + 1) * 6) - 1] +\
                                                       piece_dictionary[(type(obj), obj.color)] + \
                                                       local_chess_board[((7 - j) * 2) + 2][((i + 1) * 6):]
    print_chess_board(local_chess_board)


def print_chess_board(local_chess_board) -> None:
    for i in local_chess_board:
        for j in i:
            print(j, end='')
        print('')
