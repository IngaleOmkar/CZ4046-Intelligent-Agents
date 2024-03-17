from tabulate import tabulate
import grid_constants, iteration_constants
from typing import List
from state import State
from grid import Grid
from utility import Utility

class ShowGrid:

    def __init__(self) -> None:
        pass

    @staticmethod
    def display_grid(grid: List[List[State]]):
        print("GRID ENVIRONMENT")

        grid_str_list = []

        for i in range(grid_constants.TOTAL_ROWS):
            row = []
            for j in range(grid_constants.TOTAL_COLS):
                cell_str = " "
                if(grid[i][j].is_wall()):
                    cell_str = "Wall"
                elif(grid[i][j].get_reward() != iteration_constants.REWARD_WHITE):
                    cell_str = grid[i][j].get_reward()
                elif(i == grid_constants.AGENT_START_ROW and j == grid_constants.AGENT_START_COLUMN):
                    cell_str = "Start"
                row.append(cell_str)
            grid_str_list.append(row)
        
        print(tabulate(grid_str_list, tablefmt="grid"))
    
    @staticmethod
    def display_optimal_policy(utility_arr: List[List[Utility]]):
        # Displays the optimal policy, which is the action to be taken at each state, given a 2D array of utility values.
        print("OPTIMAL POLICY")

        str_arr = []

        for i in range(grid_constants.TOTAL_ROWS):
            row = []
            for j in range(grid_constants.TOTAL_COLS):
                row.append(utility_arr[i][j].get_action_str())
            str_arr.append(row)
        
        print(tabulate(str_arr, tablefmt="grid"))
    
    @staticmethod
    def display_utilities(grid: List[List[State]], utility_arr: List[List[Utility]]):
        print("UTILITY VALUE OF ALL STATES")
        for i in range(grid_constants.TOTAL_ROWS):
            for j in range(grid_constants.TOTAL_COLS):
                print(f"({i},{j}): {utility_arr[i][j].get_utility()}")
    
    @staticmethod
    def display_utilities_on_grid(utility_arr: List[List[Utility]]):
        print("UTILITY VALUE OF ALL STATES")
        grid_str_list = []

        for i in range(grid_constants.TOTAL_ROWS):
            row = []
            for j in range(grid_constants.TOTAL_COLS):
                row.append(utility_arr[i][j].get_utility())
            grid_str_list.append(row)
        
        print(tabulate(grid_str_list, tablefmt="grid"))
    
    @staticmethod
    def display_iteration_count(iteration_count: int):
        print(f"ITERATION COUNT: {iteration_count}")
    
    @staticmethod
    def display_setup(value_iteration: bool, converge_threshold: float):
        print("SETUP VALUES")
        values = []
        if(value_iteration):
            values.append(["DISCOUNT FACTOR", iteration_constants.DISCOUNT_FACTOR])
            values.append(["UPPER BOUND OF UTILITY", iteration_constants.UTILITY_UPPER_BOUND])
            values.append(["MAXIMUM REWARD", iteration_constants.MAX_REWARD])
            values.append(["CONSTANT 'c'", iteration_constants.MAX_ALLOWED_ERROR])
            values.append(["EPSILON", iteration_constants.MAX_DISCOUNTED_ERROR])
            values.append(["CONVERGE THRESHOLD", converge_threshold])
        else:
            values.append(["DISCOUNT FACTOR", iteration_constants.DISCOUNT_FACTOR])
            values.append(["K", iteration_constants.K])
        
        print(tabulate(values, tablefmt="fancy_grid"))


# TEST PRINT STATEMENTS
# ShowGrid.display_grid(Grid().get_grid())
# ShowGrid.display_setup(True, 0.01)



