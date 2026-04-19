from agent import Agent
from oxono import Game


class MyAgent(Agent):
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

    def global_score(self, state):
        score = 0

        for row in state.board:
            score += self.score_one_line(row)

        for col in range(6):
            column = []
            for row in range(6):
                column.append(state.board[row][col])
            score += self.score_one_line(column)

        return score

    def is_free_position(self, state, row, col):
        if not (0 <= row < 6 and 0 <= col < 6):
            return False
        if state.board[row][col] is not None:
            return False
        if (row, col) == state.totem_O or (row, col) == state.totem_X:
            return False
        return True

    def possible_placements(self, state, player):
        temp_state = state.copy()
        temp_state.current_player = player
        actions = Game.actions(temp_state)

        reachable_positions = set()
        for action in actions:
            reachable_positions.add(action[2])

        return reachable_positions

    def window_score(self, count):
        if count <= 0:
            return 0
        if count == 1:
            return 2
        if count == 2:
            return 15
        return 100

    def color_window_value(self, state, cells, positions, player, reachable_positions):
        count_player = 0
        count_other = 0
        empty_positions = []

        for i in range(4):
            cell = cells[i]
            if cell is None:
                empty_positions.append(positions[i])
            elif cell[1] == player:
                count_player += 1
            else:
                count_other += 1

        if count_player == 0 or count_other > 0:
            return 0

        points = self.window_score(count_player)
        can_fill_now = False
        for pos in empty_positions:
            if pos in reachable_positions:
                can_fill_now = True
                break

        if (
            count_player == 3
            and len(empty_positions) == 1
            and can_fill_now
            and state.current_player == player
        ):
            return 4 * points

        if can_fill_now:
            return 2 * points

        return points

    def window_evaluation(self, state, my_positions, opp_positions):
        score = 0

        for row in range(6):
            for start in range(3):
                cells = []
                positions = []
                for col in range(start, start + 4):
                    cells.append(state.board[row][col])
                    positions.append((row, col))

                score += self.color_window_value(
                    state, cells, positions, self.player, my_positions
                )
                score -= self.color_window_value(
                    state, cells, positions, 1 - self.player, opp_positions
                )

        for col in range(6):
            for start in range(3):
                cells = []
                positions = []
                for row in range(start, start + 4):
                    cells.append(state.board[row][col])
                    positions.append((row, col))

                score += self.color_window_value(
                    state, cells, positions, self.player, my_positions
                )
                score -= self.color_window_value(
                    state, cells, positions, 1 - self.player, opp_positions
                )

        return score

    def evaluate(self, state):
        if Game.is_terminal(state):
            return 100000 * Game.utility(state, self.player)

        my_positions = self.possible_placements(state, self.player)
        opp_positions = self.possible_placements(state, 1 - self.player)

        score = 1000 * self.global_score(state)
        score += self.window_evaluation(state, my_positions, opp_positions)

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
