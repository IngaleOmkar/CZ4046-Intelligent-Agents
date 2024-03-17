import grid_constants, iteration_constants
from state import State

class Grid:

    def __init__(self):
        # Set the grid with MAX_COLUMNS and MAX_ROWS
        self.__grid_env = []
        self.build_grid()

    def get_grid(self):
        return self.__grid_env
    
    def build_grid(self):
        # Set grid_env with states with rewards all initialized to -0.04
        for _ in range(grid_constants.TOTAL_ROWS):
            # Append a list of states (create new state) that denote the column in that row
            self.__grid_env.append([State(iteration_constants.REWARD_WHITE) for _ in range(grid_constants.TOTAL_COLS)])

        # Set the rewards for the green cells
        green_cells = grid_constants.GREEN_CELLS.split(grid_constants.CELL_DELIMETER)
        for cell in green_cells:
            col, row = cell.split(grid_constants.COORDINATE_DELIMER)
            self.__grid_env[int(row)][int(col)].set_reward(iteration_constants.REWARD_GREEN)
        
        # Set the rewards for the brown cells
        brown_cells = grid_constants.BROWN_CELLS.split(grid_constants.CELL_DELIMETER)
        for cell in brown_cells:
            col, row = cell.split(grid_constants.COORDINATE_DELIMER)
            self.__grid_env[int(row)][int(col)].set_reward(iteration_constants.REWARD_BROWN)
        
        # Set the rewards for the wall cells
        wall_cells = grid_constants.WALL_CELLS.split(grid_constants.CELL_DELIMETER)
        for cell in wall_cells:
            col, row = cell.split(grid_constants.COORDINATE_DELIMER)
            self.__grid_env[int(row)][int(col)].set_reward(iteration_constants.REWARD_WALL)
            self.__grid_env[int(row)][int(col)].set_wall(True)
    
    def duplicate_grid(self):
        for i in range(grid_constants.TOTAL_ROWS):
            for j in range(grid_constants.TOTAL_COLS):
                if(i >= 6 or j >= 6):
                    trueRow = i % 6
                    trueCol = j % 6

                    self.__grid_env[i][j].set_reward(self.__grid_env[trueRow][trueCol].get_reward())
                    self.__grid_env[i][j].set_wall(self.__grid_env[trueRow][trueCol].get_wall())

        
    
    
    
    
        
        



