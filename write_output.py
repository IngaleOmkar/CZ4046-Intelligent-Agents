from typing import List
from utility import Utility
import grid_constants, iteration_constants

class WriteOutput:

    @staticmethod
    def write_to_file(lst_utilities: List[List[List['Utility']]], file_name: str):
        pattern = "00.000"
        decimal_format = "{:.3f}"

        with open(file_name + ".csv", 'w') as file:
            for row in range(len(lst_utilities[0])):
                for col in range(len(lst_utilities[0][0])):
                    for action_utils in lst_utilities:
                        action_util = action_utils[row][col]
                        file.write(decimal_format.format(action_util.get_util())[:6])
                        if action_utils != lst_utilities[-1]:
                            file.write(",")
                    file.write("\n")


                    