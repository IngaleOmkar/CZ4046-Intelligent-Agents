from grid import Grid
from state import State
from utility_controller import UtilityController
from utility import Utility
from show_grid import ShowGrid
from write_output import WriteOutput
from typing import List
import grid_constants, iteration_constants
import sys

class ValueIteration:

    grid_env: Grid = None 
    grid: List[List[State]] = None
    utility_list : List[List[List[Utility]]] = None
    iterations: int = 0
    convergence_threshold:float= None
    is_value_iteration: bool = True

    def __init__(self):
        # Initialize environment
        ValueIteration.grid_env: Grid = Grid() 
        ValueIteration.grid: List[List[State]] = self.grid_env.get_grid() 
        
        # Execute Value Iteration
        ValueIteration.run_value_iteration(self.grid)

        # Demonstrate Results
        ValueIteration.display_results()
    
    @staticmethod
    def run_value_iteration(grid: List[List[State]]):
        new_utility_arr = [[Utility() for _ in range(grid_constants.TOTAL_COLS)] for _ in range(grid_constants.TOTAL_ROWS)]
        current_utility_arr = []

        ValueIteration.utility_list = []

        # Initialize delta to minimum double value first
        delta = sys.float_info.min

        ValueIteration.convergence_threshold = iteration_constants.MAX_DISCOUNTED_ERROR * ((1.000 - iteration_constants.DISCOUNT_FACTOR) / iteration_constants.DISCOUNT_FACTOR)

        first_pass = True

        while(first_pass or (delta >= ValueIteration.convergence_threshold)):
            first_pass = False

            current_utility_arr = UtilityController.update_utility(new_utility_arr, current_utility_arr)

            delta = sys.float_info.min

            curr_util_arr_cpy = []

            curr_util_arr_cpy = UtilityController.update_utility(current_utility_arr, curr_util_arr_cpy)

            ValueIteration.utility_list.append(curr_util_arr_cpy)

            for i in range(grid_constants.TOTAL_ROWS):
                for j in range(grid_constants.TOTAL_COLS):

                    if grid[i][j].is_wall():
                        continue

                    new_utility_arr[i][j] = UtilityController.calculate_best_utility(i, j, current_utility_arr, grid)

                    updated_util = new_utility_arr[i][j].get_utility()

                    current_util = current_utility_arr[i][j].get_utility()

                    updated_delta = abs(updated_util - current_util)

                    delta = max(delta, updated_delta)
            
            ValueIteration.iterations += 1
    
    @staticmethod
    def display_results():
        optimal_policy = ValueIteration.utility_list[-1]

        ShowGrid.display_grid(ValueIteration.grid)

        ShowGrid.display_setup(ValueIteration.is_value_iteration, ValueIteration.convergence_threshold)

        ShowGrid.display_iteration_count(ValueIteration.iterations)

        ShowGrid.display_utilities(ValueIteration.grid, optimal_policy)

        ShowGrid.display_optimal_policy(optimal_policy)

        ShowGrid.display_utilities_on_grid(optimal_policy)


if __name__ == "__main__":
    ValueIteration()