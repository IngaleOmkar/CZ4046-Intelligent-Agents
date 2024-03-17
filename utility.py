from action import Action

class Utility:
    
    def __init__(self, action: Action = None, utility: float = 0.0) -> None:
        self.__action = action
        self.__utility = utility
    
    def get_action(self) -> Action:
        return self.__action
    
    def get_action_str(self) -> str:
        return "Wall" if self.__action is None else self.__action.get_string_rep()
    
    def set_action(self, action: Action) -> None:
        self.__action = action

    def get_utility(self) -> float:
        return self.__utility
    
    def set_utility(self, utility: float) -> None:
        self.__utility = utility
    
    def compare_untility_with(self, utility: 'Utility') -> int:
        if self.__utility > utility.get_utility():
            return 1
        elif self.__utility < utility.get_utility():
            return -1
        else:
            return 0
