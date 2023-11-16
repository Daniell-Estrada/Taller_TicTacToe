from components.minimax import MiniMaxTree


def main():
    board = [['X', 'O', 'O'],
             ['X', '#', '#'],
             ['#', 'X', '#']]
    player = 'X'
    MiniMaxTree(board, player)


if __name__ == "__main__":
    main()
