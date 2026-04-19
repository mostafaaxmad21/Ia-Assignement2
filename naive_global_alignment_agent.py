from agent import Agent
from oxono import Game


class NaiveGlobalAlignmentAgent(Agent):
    def __init__(self, player):
        super().__init__(player)

    def result(self, state, action):
        new_state = state.copy()
        Game.apply(new_state, action)
        return new_state

    def line_score(self, length):
        if length <= 0:
            return 0
        if length == 1:
            return 1
        if length == 2:
            return 10
        return 100

    def score_one_line(self, line):
        score = 0

        current_color = None
        color_length = 0
        for cell in line + [None]:
            color = None if cell is None else cell[1]

            if color is not None and color == current_color:
                color_length += 1
            else:
                if current_color is not None:
                    points = self.line_score(min(color_length, 3))
                    if current_color == self.player:
                        score += points
                    else:
                        score -= points

                if color is None:
                    current_color = None
                    color_length = 0
                else:
                    current_color = color
                    color_length = 1

        current_symbol = None
        symbol_length = 0
        my_pieces_in_run = 0
        opp_pieces_in_run = 0
        for cell in line + [None]:
            symbol = None if cell is None else cell[0]

            if symbol is not None and symbol == current_symbol:
                symbol_length += 1
                if cell[1] == self.player:
                    my_pieces_in_run += 1
                else:
                    opp_pieces_in_run += 1
            else:
                if current_symbol is not None:
                    points = self.line_score(min(symbol_length, 3))
                    if my_pieces_in_run > opp_pieces_in_run:
                        score += points
                    elif opp_pieces_in_run > my_pieces_in_run:
                        score -= points

                if symbol is None:
                    current_symbol = None
                    symbol_length = 0
                    my_pieces_in_run = 0
                    opp_pieces_in_run = 0
                else:
                    current_symbol = symbol
                    symbol_length = 1
                    if cell[1] == self.player:
                        my_pieces_in_run = 1
                        opp_pieces_in_run = 0
                    else:
                        my_pieces_in_run = 0
                        opp_pieces_in_run = 1

        return score

    def evaluate(self, state):
        if Game.is_terminal(state):
            return 100000 * Game.utility(state, self.player)

        score = 0
        board = state.board

        for row in board:
            score += self.score_one_line(row)

        for col in range(6):
            column = []
            for row in range(6):
                column.append(board[row][col])
            score += self.score_one_line(column)

        return score

    def alphabeta_value(self, state, depth_left, alpha, beta):
        if Game.is_terminal(state):
            return self.evaluate(state)

        if depth_left == 0:
            return self.evaluate(state)

        actions = Game.actions(state)

        if Game.to_move(state) == self.player:
            value = float("-inf")
            for action in actions:
                child = self.result(state, action)
                child_value = self.alphabeta_value(child, depth_left - 1, alpha, beta)
                if child_value > value:
                    value = child_value
                if value > alpha:
                    alpha = value
                if alpha >= beta:
                    break
            return value
        else:
            value = float("inf")
            for action in actions:
                child = self.result(state, action)
                child_value = self.alphabeta_value(child, depth_left - 1, alpha, beta)
                if child_value < value:
                    value = child_value
                if value < beta:
                    beta = value
                if alpha >= beta:
                    break
            return value

    def act(self, state, remaining_time):
        actions = Game.actions(state)
        best_action = actions[0]
        best_value = float("-inf")

        alpha = float("-inf")
        beta = float("inf")

        for action in actions:
            child = self.result(state, action)
            value = self.alphabeta_value(child, 1, alpha, beta)

            if value > best_value:
                best_value = value
                best_action = action

            if best_value > alpha:
                alpha = best_value

        return best_action
