import sys
from GUI.Windows.Menu import start_menu


def parse_args():
    args = sys.argv
    if len(args) > 1:
        if args[1] == "--help":
            print(f"Use ChessPy.exe without any additional parameters to enjoy the game \n"
                  f"Use ChessPy.exe -n [params] to use the neural network environment \n"
                  f"Use ChessPy.exe -n --help to find out more \n")
            sys.exit(0)
        elif args[1] == "-n":
            from NeuralNetwork import Executer
            sys.exit(Executer.main(args[2:]))


if __name__ == '__main__':
    parse_args()
    start_menu()
