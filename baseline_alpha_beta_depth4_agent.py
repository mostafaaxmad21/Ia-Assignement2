from agent import Agent
from oxono import Game


class BaselineAlphaBetaDepth4Agent(Agent):
    def __init__(self, player):
        super().__init__(player)

    def result(self, state, action):
        new_state = state.copy()
        Game.apply(new_state, action)
        return new_state

    def evaluate(self, state):
        if Game.is_terminal(state):
            return Game.utility(state, self.player)
        return 0

    def alphabeta_value(self, state, depth_left, alpha, beta):
        if Game.is_terminal(state):
            return Game.utility(state, self.player)

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
            value = self.alphabeta_value(child, 3, alpha, beta)

            if value > best_value:
                best_value = value
                best_action = action

            if best_value > alpha:
                alpha = best_value

        return best_action
