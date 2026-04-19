from agent import Agent
from oxono import Game


class MyAgent(Agent):
    def __init__(self, player):
        super().__init__(player)

    def result(self, state, action):
        new_state = state.copy()
        Game.apply(new_state, action)
        return new_state

    def window_score(self, count):
        if count <= 0:
            return 0
        if count == 1:
            return 1
        if count == 2:
            return 20
        return 500

    def playable_positions_by_symbol(self, state, player):
        temp_state = state.copy()
        temp_state.current_player = player

        positions = {"x": set(), "o": set()}
        for action in Game.actions(temp_state):
            symbol = "o" if action[0] == "O" else "x"
            positions[symbol].add(action[2])

        return positions

    def color_window_value(self, cells, player):
        count_player = 0

        for cell in cells:
            if cell is None:
                continue
            if cell[1] != player:
                return 0
            count_player += 1

        return self.window_score(count_player)

    def symbol_window_value(
        self,
        state,
        cells,
        positions,
        symbol,
        my_symbol_positions,
        opp_symbol_positions,
    ):
        count_symbol = 0
        my_count = 0
        opp_count = 0
        empty_positions = []

        for i in range(4):
            cell = cells[i]
            if cell is None:
                empty_positions.append(positions[i])
                continue

            cell_symbol, cell_player = cell
            if cell_symbol != symbol:
                return 0

            count_symbol += 1
            if cell_player == self.player:
                my_count += 1
            else:
                opp_count += 1

        if count_symbol == 0:
            return 0

        points = self.window_score(count_symbol)
        my_can_fill = False
        opp_can_fill = False

        for pos in empty_positions:
            if pos in my_symbol_positions[symbol]:
                my_can_fill = True
            if pos in opp_symbol_positions[symbol]:
                opp_can_fill = True

        if my_can_fill and not opp_can_fill:
            return points
        if opp_can_fill and not my_can_fill:
            return -points

        if my_can_fill and opp_can_fill:
            if state.current_player == self.player:
                return points
            return -points

        # If no one can complete the symbol window immediately, keep only a
        # smaller preference based on who contributed more pieces to it.
        if my_count > opp_count:
            return points // 2
        if opp_count > my_count:
            return -(points // 2)

        return 0

    def line_windows_score(self, state, line, positions, my_symbol_positions, opp_symbol_positions):
        score = 0

        for start in range(3):
            cells = line[start : start + 4]
            window_positions = positions[start : start + 4]

            score += self.color_window_value(cells, self.player)
            score -= self.color_window_value(cells, 1 - self.player)

            score += self.symbol_window_value(
                state,
                cells,
                window_positions,
                "x",
                my_symbol_positions,
                opp_symbol_positions,
            )
            score += self.symbol_window_value(
                state,
                cells,
                window_positions,
                "o",
                my_symbol_positions,
                opp_symbol_positions,
            )

        return score

    def evaluate(self, state):
        if Game.is_terminal(state):
            return 100000 * Game.utility(state, self.player)

        score = 0
        board = state.board
        my_symbol_positions = self.playable_positions_by_symbol(state, self.player)
        opp_symbol_positions = self.playable_positions_by_symbol(state, 1 - self.player)

        for row in range(6):
            line = board[row]
            positions = [(row, col) for col in range(6)]
            score += self.line_windows_score(
                state, line, positions, my_symbol_positions, opp_symbol_positions
            )

        for col in range(6):
            line = [board[row][col] for row in range(6)]
            positions = [(row, col) for row in range(6)]
            score += self.line_windows_score(
                state, line, positions, my_symbol_positions, opp_symbol_positions
            )

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
        if state.last_move is None and self.player == 0:
            opening_action = ("O", (4, 2), (3, 2))
            if opening_action in Game.actions(state):
                return opening_action

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
