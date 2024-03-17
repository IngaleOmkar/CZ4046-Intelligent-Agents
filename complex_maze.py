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

class ComplexMaze:

    grid_env: Grid = None
    utility_list : List[List[List[Utility]]] = None
    grid: List[List[State]] = None
    iterations: int = 0
    converge_threshold: float = None
    is_value_iteration: bool = True

    def __init__(self):
        ComplexMaze.grid_env = Grid()
        ComplexMaze.grid = ComplexMaze.grid_env.get_grid()

        run_value_iteration(ComplexMaze.grid)

        display_results()

        WriteOutput.write_to_file(ComplexMaze.utility_list, "output/complex_maze_list")

        run_policy_iteration(ComplexMaze.grid)

        display_results()

        WriteOutput.write_to_file(ComplexMaze.utility_list, "output/complex_maze_list")