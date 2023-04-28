from Tile import Tile

class Agent:

    MIN_VALUE = -1000000
    MAX_VALUE = 1000000

    def __init__(self, game, color, max_depth):
        self.game = game
        self.color = color
        self.max_depth = max_depth

    def do_min_max(self, current_board):
        move, value = self.max(current_board, self.color, 0, self.MIN_VALUE, self.MAX_VALUE)

        return move

    def max(self, current_board, current_color, depth, alpha, beta):
        best_move = None
        if self.game.check_terminal(current_board, current_color):
            return best_move, self.game.evaluate(current_board, current_color)

        if depth == self.max_depth:
            return best_move, self.game.evaluate(current_board, current_color)

        moves = self.game.generate_all_possible_moves(current_board, current_color)
        value = self.MIN_VALUE
        for move in moves:
            next_board = current_board.next_board(current_color, move)
            opponent_color = self.game.opponent(current_color)

            temp_move, min_value = self.min(next_board, opponent_color, depth+1, alpha, beta)

            if min_value > value:
                value = min_value
                best_move = move


            if value >= beta:
                return best_move, value
            alpha = max(alpha, value)

        return best_move, value

    def min(self, current_board, current_color, depth, alpha, beta):
        best_move = None
        if self.game.check_terminal(current_board, current_color):
            return best_move, self.game.evaluate(current_board, current_color)

        if depth == self.max_depth:
            return best_move, self.game.evaluate(current_board, current_color)

        moves = self.game.generate_all_possible_moves(current_board, current_color)
        value = self.MAX_VALUE

        for move in moves:
            next_board = current_board.next_board(current_color, move)
            opponent_color = self.game.opponent(current_color)

            temp_move, max_value = self.max(next_board, opponent_color, depth + 1, alpha, beta)
            if max_value < value:
                value = max_value
                best_move = move


            if value <= alpha:
                return best_move, value
            beta = min(beta, value)

        return best_move, value

