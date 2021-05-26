import copy
import multiprocessing
import random

from Engine.Evaluation import order_moves


def select_move_human(moves, args):
    """
    :param moves: the legal moves to be put into args[1]
    :param args: (q1,q2) queues for storing moves
    :return: puts [moves] into q2, returns move from q1
    """
    args[1].put(moves)
    move = args[0].get()
    args[0].task_done()
    return move


def random_move(unused, all_legal_moves):
    """
    Finds a random move to make
    :param unused: unused
    :param all_legal_moves: all legal moves for current player
    :return: start_pos, move
    """
    start_pos = random.choice(list(all_legal_moves.keys()))
    while not all_legal_moves[start_pos]:
        start_pos = random.choice(list(all_legal_moves.keys()))
    return start_pos, random.choice(all_legal_moves[start_pos])


def __worker(queue: multiprocessing.Queue, result, lock):
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

        temp = current_task[0](current_task[1])
        lock.acquire()
        if temp < result[3]:
            result[0], result[1], result[2], result[3] = \
                current_task[2][0], current_task[2][1][0], current_task[2][1][1], temp
        lock.release()


def __add_starting_objects_to_queue(queue, board, all_legal_moves, eval_method):
    current_all_legal_moves = order_moves(board, all_legal_moves,
                                          True, False, -1, True)
    for move in current_all_legal_moves:
        chess_board_copy = copy.deepcopy(board)
        chess_board_copy.make_move(move[0], move[1])
        queue.put((eval_method, chess_board_copy, (move[0], move[1])))


def evaluated_move(board, all_legal_moves, evaluation_method, number_of_processes):
    """
    checks every possible move and selects the best one
    :param board: the board on which the game is played
    :param all_legal_moves: all legal moves for current player
    :param evaluation_method: method used to evaluate the board
    :return: start_pos, move
    """
    queue = multiprocessing.Queue(maxsize=0)
    lock = multiprocessing.Lock()
    result = multiprocessing.Array('f', [-1, -1, -1, 99999999999999])
    __add_starting_objects_to_queue(queue, board, all_legal_moves, evaluation_method)
    processes = []
    for i in range(number_of_processes):
        process = multiprocessing.Process(target=__worker, args=(queue, result, lock), name=f"Process {i}")
        processes.append(process)
        process.start()
    for p in processes:
        p.join()
    start_pos = int(result[0])
    move = (int(result[1]), int(result[2]))
    return start_pos, move
    # for piece in all_legal_moves.keys():
    #     for move in all_legal_moves[piece]:
    #         board_.make_move(piece, move)
    #         move_value = evaluation_method(board_)
    #         board_.unmake_move()
    #         if move_value < best_move[0]:
    #             best_move = (move_value, (piece, move))
    # return best_move[1]
