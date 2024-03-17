class State:

    def __init__(self, reward = 0.0):
        # The reward in the current state
        self.__reward = reward

        # Boolean flag to check if the state is a wall
        self.__is_wall = False

    def get_reward(self):
        return self.__reward
    
    def set_reward(self, reward):
        self.__reward = reward

    def is_wall(self):
        return self.__is_wall
    
    def set_wall(self, is_wall):
        self.__is_wall = is_wall
