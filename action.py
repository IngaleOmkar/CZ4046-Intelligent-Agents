import random
from enum import Enum

# Declare an enum of the actions that the agent can take
class Action(Enum):
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"

    def __init__(self, string_rep) -> None:
        super().__init__()
        self.action_string = string_rep
    
    def get_string_rep(self):
        return self.action_string

    @staticmethod
    def get_random_action():
        return random.choice(list(Action))










