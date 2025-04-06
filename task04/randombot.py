
from random import choice
from dots_and_boxes import State

class RandomAgent:
    
    def __init__(self, maxdepth=4):
        self.maxdepth = maxdepth
        self.nodes = 0
    
    def action(self, state : State):
        return choice(state.all_actions()), 0