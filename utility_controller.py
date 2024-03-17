from utility import Utility
from state import State
from typing import List
import copy
import grid_constants, iteration_constants
from action import Action

class UtilityController:

    def __init__(self) -> None:
        pass

    @staticmethod
    def update_utility(source: List[List[Utility]], destination: List[List[Utility]]):
        # Copy the contents from the source array to the destination array
        destination = [[copy.deepcopy(item) for item in row] for row in source]
        return destination
    
    @staticmethod
    def move_right(row, col, current_utility_arr: List[List[Utility]], grid: List[List[State]]):
        # Attempt to move right
        if(col + 1 < grid_constants.TOTAL_COLS and not grid[row][col + 1].is_wall()):
            return current_utility_arr[row][col + 1].get_utility()
        # If the move is not possible, return the current utility
        return current_utility_arr[row][col].get_utility()
    
    @staticmethod
    def move_left(row, col, current_utility_arr: List[List[Utility]], grid: List[List[State]]):
        # Attempt to move left
        if(col - 1 >= 0 and not grid[row][col - 1].is_wall()):
            return current_utility_arr[row][col - 1].get_utility()
        # If the move is not possible, return the current utility
        return current_utility_arr[row][col].get_utility()
    
    @staticmethod
    def move_down(row, col, current_utility_arr: List[List[Utility]], grid: List[List[State]]):
        # Attempt to move down
        if(row + 1 < grid_constants.TOTAL_ROWS and not grid[row + 1][col].is_wall()):
            return current_utility_arr[row + 1][col].get_utility()
        # If the move is not possible, return the current utility
        return current_utility_arr[row][col].get_utility()
    
    @staticmethod
    def move_up(row, col, current_utility_arr: List[List[Utility]], grid: List[List[State]]):
        # Attempt to move up
        if(row - 1 >= 0 and not grid[row - 1][col].is_wall()):
            return current_utility_arr[row - 1][col].get_utility()
        # If the move is not possible, return the current utility
        return current_utility_arr[row][col].get_utility()
    
    # Calculate the utility of moving right
    @staticmethod
    def move_right_utility(row, col, current_utility_arr: List[List[Utility]], grid: List[List[State]]):
        right_utility = 0.0

        # Intends to move right
        right_utility += iteration_constants.INTENDED_PROBABILITY * UtilityController.move_right(row, col, current_utility_arr, grid)

        # Intends to move right, but moves down instead 
        right_utility += iteration_constants.RIGHT_PROBABILITY * UtilityController.move_down(row, col, current_utility_arr, grid)

        # Intends to move right, but moves up instead
        right_utility += iteration_constants.LEFT_PROBABILITY * UtilityController.move_up(row, col, current_utility_arr, grid)

        # Calculate the utility of moving right
        right_utility = grid[row][col].get_reward() + iteration_constants.DISCOUNT_FACTOR * right_utility

        return right_utility
    
    # Calculate the utility of moving left
    @staticmethod
    def move_left_utility(row, col, current_utility_arr: List[List[Utility]], grid: List[List[State]]):
        left_utility = 0.0

        # Intends to move left
        left_utility += iteration_constants.INTENDED_PROBABILITY * UtilityController.move_left(row, col, current_utility_arr, grid)

        # Intends to move left, but moves up instead
        left_utility += iteration_constants.RIGHT_PROBABILITY * UtilityController.move_up(row, col, current_utility_arr, grid)

        # Intends to move left, but moves down instead
        left_utility += iteration_constants.LEFT_PROBABILITY * UtilityController.move_down(row, col, current_utility_arr, grid)

        # Calculate the utility of moving left
        left_utility = grid[row][col].get_reward() + iteration_constants.DISCOUNT_FACTOR * left_utility

        return left_utility
    
    # Calculate the utility of moving down
    @staticmethod
    def move_down_utility(row, col, current_utility_arr: List[List[Utility]], grid: List[List[State]]):
        down_utility = 0.0

        # Intends to move down
        down_utility += iteration_constants.INTENDED_PROBABILITY * UtilityController.move_down(row, col, current_utility_arr, grid)

        # Intends to move down, but moves left instead
        down_utility += iteration_constants.LEFT_PROBABILITY * UtilityController.move_left(row, col, current_utility_arr, grid)

        # Intends to move down, but moves right instead
        down_utility += iteration_constants.RIGHT_PROBABILITY * UtilityController.move_right(row, col, current_utility_arr, grid)

        # Calculate the utility of moving down
        down_utility = grid[row][col].get_reward() + iteration_constants.DISCOUNT_FACTOR * down_utility

        return down_utility
    
    # Calculate the utility of moving up
    @staticmethod
    def move_up_utility(row, col, current_utility_arr: List[List[Utility]], grid: List[List[State]]):
        up_utility = 0.0

        # Intends to move up
        up_utility += iteration_constants.INTENDED_PROBABILITY * UtilityController.move_up(row, col, current_utility_arr, grid)

        # Intends to move up, but moves right instead
        up_utility += iteration_constants.RIGHT_PROBABILITY * UtilityController.move_right(row, col, current_utility_arr, grid)

        # Intends to move up, but moves left instead
        up_utility += iteration_constants.LEFT_PROBABILITY * UtilityController.move_left(row, col, current_utility_arr, grid)

        # Calculate the utility of moving up
        up_utility = grid[row][col].get_reward() + iteration_constants.DISCOUNT_FACTOR * up_utility

        return up_utility
    
    # Calculate the next utility values
    @staticmethod
    def calculate_next_utility(utils: List[List[Utility]], grid: List[List[State]]):
        current_utility_arr: List[List[Utility]] = [[Utility() for _ in range(grid_constants.TOTAL_COLS)] for _ in range(grid_constants.TOTAL_ROWS)]

        new_utility_arr: List[List[Utility]] = [[Utility(utils[i][j].get_action(), utils[i][j].get_utility()) for j in range(grid_constants.TOTAL_COLS)] for i in range(grid_constants.TOTAL_ROWS)]

        k = 0
        first_pass = True

        while(k < iteration_constants.K or first_pass):
            first_pass = False
            
            current_utility_arr = UtilityController.update_utility(new_utility_arr, current_utility_arr)

            for i in range(grid_constants.TOTAL_ROWS):
                for j in range(grid_constants.TOTAL_COLS):
                    if(not grid[i][j].is_wall()):
                        action = current_utility_arr[i][j].get_action()
                        new_utility_arr[i][j] = UtilityController.get_fixed_utility(action, i, j, current_utility_arr, grid)
            
            k += 1
        
        return new_utility_arr
    
    # Calculate the utility of a specific action
    @staticmethod
    def get_fixed_utility(action, row, col, current_utility_arr: List[List[Utility]], grid: List[List[State]]):
        fixed_action_utility: Utility = None

        if(action == Action.UP):
            fixed_action_utility = Utility(Action.UP, UtilityController.move_up_utility(row, col, current_utility_arr, grid))
        elif(action == Action.DOWN):
            fixed_action_utility = Utility(Action.DOWN, UtilityController.move_down_utility(row, col, current_utility_arr, grid))
        elif(action == Action.LEFT):
            fixed_action_utility = Utility(Action.LEFT, UtilityController.move_left_utility(row, col, current_utility_arr, grid))
        else:
            fixed_action_utility = Utility(Action.RIGHT, UtilityController.move_right_utility(row, col, current_utility_arr, grid))
        
        return fixed_action_utility
    
    # Calculates the utility for each possible action and returns the action with maximal utility
    @staticmethod
    def calculate_best_utility(row, col, current_utility_arr: List[List[Utility]], grid: List[List[State]]):
        utils: List[Utility] = []

        # Add the utilities for each possible action to the list
        utils.append(Utility(Action.UP, UtilityController.move_up_utility(row, col, current_utility_arr, grid)))
        utils.append(Utility(Action.DOWN, UtilityController.move_down_utility(row, col, current_utility_arr, grid)))
        utils.append(Utility(Action.LEFT, UtilityController.move_left_utility(row, col, current_utility_arr, grid)))
        utils.append(Utility(Action.RIGHT, UtilityController.move_right_utility(row, col, current_utility_arr, grid)))

        # Sort the list of utilities based on the utility value
        utils.sort(key=lambda x: x.get_utility(), reverse=True)

        # Return the Utility object with the maximum utility
        return utils[0]




























# class UtilityController:

#     def __init__(self) -> None:
#         pass

#     @staticmethod
#     def update_utility(src_utility: List[Utility], dst_utility: List[Utility]) -> None:
#         for i in range(len(src_utility)):
#             src_utility[i] = copy.deepcopy(dst_utility[i])
    
#     @staticmethod
#     def turn_right(col, row, cur_utils, grid):
#         if col + 1 < grid_constants.TOTAL_COLS and not grid[row][col + 1].is_wall():
#             return cur_utils[row][col + 1].get_utility()
        
#         return cur_utils[row][col].get_utility()
    
#     @staticmethod
#     def turn_left(col, row, cur_utils, grid):
#         if col - 1 >= 0 and not grid[row][col - 1].is_wall():
#             return cur_utils[row][col - 1].get_utility()
        
#         return cur_utils[row][col].get_utility()
    
#     @staticmethod
#     def go_down(col, row, cur_utils, grid):
#         if row + 1 < grid_constants.TOTAL_ROWS and not grid[row + 1][col].is_wall():
#             return cur_utils[row + 1][col].get_utility()
        
#         return cur_utils[row][col].get_utility()
    
#     @staticmethod
#     def go_up(col, row, cur_utils, grid):
#         if row - 1 >= 0 and not grid[row - 1][col].is_wall():
#             return cur_utils[row - 1][col].get_utility()
        
#         return cur_utils[row][col].get_utility()
    
#     @staticmethod
#     def move_right_utility(col, row, cur_utils, grid):
#         right_utility = 0.0

#         right_utility += iteration_constants.INTENDED_PROBABILITY * UtilityController.turn_right(col, row, cur_utils, grid)

#         right_utility += iteration_constants.RIGHT_PROBABILITY * UtilityController.go_down(col, row, cur_utils, grid)

#         right_utility += iteration_constants.LEFT_PROBABILITY * UtilityController.go_up(col, row, cur_utils, grid)

#         right_utility = grid[row][col].get_reward() + iteration_constants.DISCOUNT_FACTOR * right_utility

#         return right_utility
    
#     @staticmethod
#     def move_left_utility(col, row, cur_utils, grid):
#         left_utility = 0.0

#         left_utility += iteration_constants.INTENDED_PROBABILITY * UtilityController.turn_left(col, row, cur_utils, grid)

#         left_utility += iteration_constants.RIGHT_PROBABILITY * UtilityController.go_up(col, row, cur_utils, grid)

#         left_utility += iteration_constants.LEFT_PROBABILITY * UtilityController.go_down(col, row, cur_utils, grid)

#         left_utility = grid[row][col].get_reward() + iteration_constants.DISCOUNT_FACTOR * left_utility

#         return left_utility
    
#     @staticmethod
#     def move_down_utility(col, row, cur_utils, grid):
#         down_utility = 0.0

#         down_utility += iteration_constants.INTENDED_PROBABILITY * UtilityController.go_down(col, row, cur_utils, grid)

#         down_utility += iteration_constants.LEFT_PROBABILITY * UtilityController.turn_left(col, row, cur_utils, grid)

#         down_utility += iteration_constants.RIGHT_PROBABILITY * UtilityController.turn_right(col, row, cur_utils, grid)

#         down_utility = grid[row][col].get_reward() + iteration_constants.DISCOUNT_FACTOR * down_utility

#         return down_utility
    
#     @staticmethod
#     def move_up_utility(col, row, cur_utils, grid):
#         up_utility = 0.0

#         up_utility += iteration_constants.INTENDED_PROBABILITY * UtilityController.go_up(col, row, cur_utils, grid)

#         up_utility += iteration_constants.RIGHT_PROBABILITY * UtilityController.turn_right(col, row, cur_utils, grid)

#         up_utility += iteration_constants.LEFT_PROBABILITY * UtilityController.turn_left(col, row, cur_utils, grid)

#         up_utility = grid[row][col].get_reward() + iteration_constants.DISCOUNT_FACTOR * up_utility

#         return up_utility
    
#     @staticmethod
#     def calculate_next_utility(utils, grid):
#         cur_utils = [[Utility() for _ in range(grid_constants.TOTAL_COLS)] for _ in range(grid_constants.TOTAL_ROWS)]

#         new_utils = [[Utility(utils[i][j].get_action(), utils[i][j].get_utility()) for j in range(grid_constants.TOTAL_COLS)] for i in range(grid_constants.TOTAL_ROWS)]

#         k = 0

#         while k < iteration_constants.K:
#             UtilityController.update_utility(new_utils, cur_utils)

#             # Updates the utility for each state based on the action stated in the policy

#             for i in range(grid_constants.TOTAL_ROWS):
#                 for j in range(grid_constants.TOTAL_COLS):
#                     if not grid[i][j].is_wall():
#                         new_utils[i][j] = UtilityController.calculate_action_util(cur_utils[i][j].get_action(), i, j, cur_utils, grid)
            
#             k += 1
        
#         return new_utils
    
#     @staticmethod
#     def calculate_action_util(action, row, col, cur_utils, grid):
#         action_util = None 

#         if(action == Action.UP):
#             action_util = Utility(Action.UP, UtilityController.move_up_utility(col, row, cur_utils, grid))
#         elif(action == Action.DOWN):
#             action_util = Utility(Action.DOWN, UtilityController.move_down_utility(col, row, cur_utils, grid))
#         elif(action == Action.LEFT):
#             action_util = Utility(Action.LEFT, UtilityController.move_left_utility(col, row, cur_utils, grid))
#         else:
#             action_util = Utility(Action.RIGHT, UtilityController.move_right_utility(col, row, cur_utils, grid))
        
#         return action_util
    
#     @staticmethod
#     def calculate_best_utility(row, col, cur_utils, grid):
#         utils = []

#         # Add the utilities for each possible action to the list
#         utils.append(Utility(Action.UP, UtilityController.move_up_utility(col, row, cur_utils, grid)))
#         utils.append(Utility(Action.DOWN, UtilityController.move_down_utility(col, row, cur_utils, grid)))
#         utils.append(Utility(Action.LEFT, UtilityController.move_left_utility(col, row, cur_utils, grid)))
#         utils.append(Utility(Action.RIGHT, UtilityController.move_right_utility(col, row, cur_utils, grid)))

#         # Sort the list of utilities based on the utility value
#         utils.sort(key=lambda x: x.get_utility(), reverse=True)

#         # Return the Utility object with the maximum utility
#         return utils[0]



           