
def count_legal_moves_recursive(chess_board, depth):
    """
    :param chess_board: Chess.Board.Board
    :param depth: a number that indicates how deep the search will be
    :return: returns a number of all possible positions that can happen for the given depth
    """
    all_legal_moves = 0
    if depth > 0:
        current_all_legal_moves = chess_board.calculate_all_legal_moves()
        for piece in current_all_legal_moves:
            for move in current_all_legal_moves[piece]:
                if depth == 1:
                    all_legal_moves += 1
                else:
                    chess_board.make_move(piece, move)
                    all_legal_moves += count_legal_moves_recursive(chess_board, depth - 1)
                    chess_board.unmake_move()
    return all_legal_moves
