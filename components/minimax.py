import matplotlib.pyplot as plt
import networkx as nx

from .node import Node


class MiniMaxTree:
    def __init__(self, board: list, player: str, MAX_DEPTH=float('inf')):
        self.player = player
        self.MAX_DEPTH = MAX_DEPTH
        self.root = self.build_tree(board, player)
        self.BEST_MOVE = [self.root]
        self.propagate_score(self.root, True)
        [print(node) for node in self.BEST_MOVE]
        self.show_tree()

    def build_tree(self, board: list, player: str) -> Node:
        root = Node(board)
        self.generate_tree(root, player)
        return root

    def evaluate(self, board: list) -> int:
        if self.has_winner(board, self.player):
            return 10
        elif self.has_winner(board, self.get_opponent(self.player)):
            return -10
        elif self.has_possible_win(board, self.get_opponent(self.player)):
            return -5
        elif self.has_possible_win(board, self.player):
            return 5
        return 0

    def has_winner(self, board: list, player: str) -> bool:
        for i in range(3):
            if all(cell == player for cell in board[i]) \
                    or all(board[j][i] == player for j in range(3)):
                return True
        if all(board[i][i] == player for i in range(3)) \
                or all(board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def has_possible_win(self, board: list, player: str) -> bool:
        for i in range(3):
            if self.is_winning_move(board[i], player, '#') or \
                    self.is_winning_move([board[j][i] for j in range(3)], player, '#'):
                return True
        if self.is_winning_move([board[i][i] for i in range(3)], player, '#') or \
                self.is_winning_move([board[i][2 - i] for i in range(3)], player, '#'):
            return True
        return False

    def is_winning_move(self, line: list, player: str, empty_cell: str) -> bool:
        return line.count(player) == 2 and line.count(empty_cell) == 1

    def generate_tree(self, node: Node, player: str):
        if node.depth == self.MAX_DEPTH or self.has_winner(node.board, player) \
                or self.has_winner(node.board, self.get_opponent(player)):
            return

        moves = self.generate_moves(node.board, player)
        for move in moves:
            new_board = [row[:] for row in node.board]
            new_board[move[0]][move[1]] = move[2]
            score = self.evaluate(new_board)
            child = Node(new_board, score, node)
            child.depth = node.depth + 1
            node.add_child(child)
            self.generate_tree(child, self.get_opponent(player))

    def generate_moves(self, board, player):
        moves = [(i, j, player) for i in range(3)
                 for j in range(3) if board[i][j] == '#']
        return moves

    def get_opponent(self, player):
        return player == 'X' and 'O' or 'X'

    def minimax(self, node: Node, maximizing_player: bool) -> int:
        best_value = None

        if maximizing_player:
            for child in node.children:
                self.minimax(child, False)
                best_value = max(node.children, key=lambda x: x.score)
                node.score = best_value.score
        else:
            for child in node.children:
                self.minimax(child, True)
                best_value = min(node.children, key=lambda x: x.score)
                node.score = best_value.score

        return best_value

    def propagate_score(self, node: Node, turn):
        node = self.minimax(node, turn)

        if node:
            self.BEST_MOVE.append(node)
            self.propagate_score(node, turn=not turn)

    def show_tree(self):
        G = nx.Graph()

        def add_node(nodo_actual: Node, padre=None):
            if padre:
                G.add_edge(padre, nodo_actual)

            for hijo in nodo_actual.children:
                G.add_node(hijo, label=hijo)
                add_node(hijo, nodo_actual)

        G.add_node(self.root, label=self.root)
        add_node(self.root)
        pos = nx.nx_pydot.graphviz_layout(G, prog='dot', root=self.root)

        nx.draw(G, pos, with_labels=True, node_size=1500, node_color='lightblue',
                alpha=0.9, font_size=10, font_weight='bold', arrows=True)
        plt.show()
