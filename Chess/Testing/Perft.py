import copy
import multiprocessing
from Chess.Board.Board import Board


def count_legal_moves_recursive(chess_board, depth):
    """
    Performs a recursive perft operation for a given chess board.

    :param chess_board: Chess.Board.Board. A chess board that the computations are being performed at.
    :param depth: a number that indicates how deep the search will be.
    :return: returns a number of all possible positions that can happen for the given depth.
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


def worker(queue: multiprocessing.Queue, result, lock):
    """
    A function performed by a Process. It carries out the tasks until the queue is empty.

    :param queue: multiprocessing.Queue. Holds tasks performed by workers.
    :param result: multiprocessing.Value. An object that the results of all tasks are saved in.
    :param lock: multiprocessing.Lock. Standard monitor to protect the critical section.
    """
    while True:
        if queue.empty():
            return
        current_task = queue.get()

        temp = current_task[0](*current_task[1])
        lock.acquire()
        result.value += temp
        lock.release()


def add_starting_objects_to_queue(queue: multiprocessing.Queue, chess_board: Board, depth):
    """
    Adds all starting tasks to the queue.

    :param queue: multiprocessing.Queue. Holds tasks performed by workers.
    :param chess_board: Board. A chess board that the computations are being performed at.
    :param depth: a number that signifies how deep the search will be.
    """
    all_legal_moves = chess_board.calculate_all_legal_moves()
    for piece in all_legal_moves:
        for move in all_legal_moves[piece]:
            chess_board_copy = copy.deepcopy(chess_board)
            chess_board_copy.make_move(piece, move)
            queue.put((count_legal_moves_recursive, (chess_board_copy, depth - 1)))


def multiprocess_perft_starter(chess_board: Board, depth: int, number_of_processes: int):
    """
    Initializes all key components to perform a perft operation.

    :param chess_board: Board. A chess board that the computations are being performed at.
    :param depth: a number that signifies how deep the search will be.
    :param number_of_processes: a number of Processes that will perform a perft operation.
    :return: number of all possible positions positions for a given chess_board and depth.
    """
    queue = multiprocessing.Queue(maxsize=0)
    lock = multiprocessing.Lock()
    result = multiprocessing.Value('i', 0)
    add_starting_objects_to_queue(queue, chess_board, depth)

    processes = []
    for i in range(number_of_processes):
        process = multiprocessing.Process(target=worker, args=(queue, result, lock), name=f"Process {i}")
        processes.append(process)
        process.start()
    for p in processes:
        p.join()
    return result.value
