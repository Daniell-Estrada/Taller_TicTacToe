class Node:
    def __init__(self, board: list, score: int = 0, parent=None):
        self.board: list = board
        self.score: int = score
        self.parent: Node = parent
        self.depth: int = 0
        self.children: list = []

    def add_child(self, node):
        self.children.append(node)
        return self

    def __str__(self):
        string = f'Score {self.score}\n'

        for row in self.board:
            string += '|'.join(row) + '\n'

        return string
