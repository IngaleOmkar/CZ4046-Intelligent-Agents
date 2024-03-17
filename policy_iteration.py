from grid import Grid
from state import State
from utility_controller import UtilityController
from utility import Utility
from show_grid import ShowGrid
from write_output import WriteOutput
from typing import List
from action import Action
import grid_constants, iteration_constants
import sys

class PolicyIteration:

    grid_env: Grid = None
    utility_list : List[List[List[Utility]]] = None
    grid: List[List[State]] = None
    iterations: int = 0
    is_value_iteration: bool = False

    def __init__(self):
        PolicyIteration.grid_env = Grid()
        PolicyIteration.grid = PolicyIteration.grid_env.get_grid()

        PolicyIteration.run_policy_iteration(PolicyIteration.grid)

        PolicyIteration.display_results()

        WriteOutput.write_to_file(PolicyIteration.utility_list, "output/policy_iteration_list")

    @staticmethod
    def run_policy_iteration(grid: List[List[State]]):
        current_utility_array: List[List[Utility]] = []
        new_utility_array: List[List[Utility]] = [[Utility() for _ in range(grid_constants.TOTAL_COLS)] for _ in range(grid_constants.TOTAL_ROWS)]

        # Initialize default utilities and policies for all states 
        for i in range(grid_constants.TOTAL_ROWS):
            for j in range(grid_constants.TOTAL_COLS):
                if not grid[i][j].is_wall():
                    random_action = Action.get_random_action()
                    new_utility_array[i][j].set_action(random_action)
        
        # List to store all the utilities 
        
        PolicyIteration.utility_list = []

        # Check if current policy is optimal
        unchanged: bool = True

        first_pass: bool = True

        while first_pass or not unchanged:

            first_pass = False

            current_utility_array = UtilityController.update_utility(new_utility_array, current_utility_array)

            current_utility_array_cpy = []

            current_utility_array_cpy = UtilityController.update_utility(current_utility_array, current_utility_array_cpy)

            PolicyIteration.utility_list.append(current_utility_array_cpy)

            new_utility_array = UtilityController.calculate_next_utility(current_utility_array, grid)

            unchanged = True

            # Policy Improvement 

            for i in range(grid_constants.TOTAL_ROWS):
                for j in range(grid_constants.TOTAL_COLS):
                    if not grid[i][j].is_wall():
                        best_action_utility = UtilityController.calculate_best_utility(i, j, new_utility_array, grid)

                        policy_action: Action = new_utility_array[i][j].get_action()
                        policy_action_utility: Utility = UtilityController.get_fixed_utility(policy_action, i, j, new_utility_array, grid)

                        if best_action_utility.get_utility() > policy_action_utility.get_utility():
                            unchanged = False
                            new_utility_array[i][j].set_action(best_action_utility.get_action())
            
            PolicyIteration.iterations += 1
        
    @staticmethod
    def display_results():
        
        optimal_policy: List[List[Utility]] = PolicyIteration.utility_list[-1]

        ShowGrid.display_grid(PolicyIteration.grid)

        ShowGrid.display_setup(PolicyIteration.is_value_iteration, 0)

        ShowGrid.display_iteration_count(PolicyIteration.iterations)

        ShowGrid.display_utilities(PolicyIteration.grid, optimal_policy)

        ShowGrid.display_optimal_policy(optimal_policy)

        ShowGrid.display_utilities_on_grid(optimal_policy)

if __name__ == "__main__":
    PolicyIteration()