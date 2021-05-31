
def convert_chess_notation_into_index(string: str) -> int:
    """
    :param string: position on the board in the form of a string: "column_letter + row_number"
    :return: returns the index of the column
    """
    letter_dictionary = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

    if len(string) != 2 or not string[0].isalpha() or not string[1].isnumeric():
        return -1

    return letter_dictionary[string[0]] + (int(string[1]) - 1) * 8


def convert_index_into_chess_notation(index: int) -> str:
    """
    :param index: index of a square on a chess board
    :return: position on the board in the form of a string: "column_letter + row_number"
    """
    letter_dictionary = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

    if index > 63 or index < 0:
        return '-'

    return letter_dictionary[index % 8] + str(int(index / 8) + 1)
