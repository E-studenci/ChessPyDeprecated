from GUI.Windows.Menu import start_menu, initialize_player_constructors, multiprocessing
from Paths import initialize_paths


def parse_args():
    args = sys.argv
    if len(args) > 1:
        if args[1] == "-n":
            from NeuralNetwork import Executer
            sys.exit(Executer.main(args[2:]))
        else:
            print(f"Use ChessPy.exe without any additional parameters to enjoy the game \n"
                  f"Use ChessPy.exe -n [params] to use the neural network environment \n"
                  f"Use ChessPy.exe -n --help to find out more \n", file=sys.stdout)
            sys.exit(0)


if __name__ == '__main__':
    import io
    import sys
    import os

    multiprocessing.freeze_support()
    initialize_paths(getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))))
    initialize_player_constructors()
    parse_args()
    start_menu()
