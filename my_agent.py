from agent import Agent
from oxono import Game
from oxono import State


class MyAgent(Agent):
    def act(self, state, remaining_time):
        print(Game.actions(state)[0])
        return Game.actions(state)[0]

    def action_result(self, state, action):
        new_state = state.copy()
        Game.apply(new_state, action)
        return new_state
