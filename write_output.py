from typing import List
from utility import Utility
import grid_constants, iteration_constants
from decimal import Decimal

class WriteOutput:

    @staticmethod
    def write_to_file(lst_utilities: List[List[List['Utility']]], file_name: str):
        sb = []
        pattern = "{:.3f}"  # Format string to display 3 decimal places

        for row in range(grid_constants.TOTAL_ROWS):
            for col in range(grid_constants.TOTAL_COLS):
                for util in lst_utilities:
                    sb.append(str(util[row][col].get_utility())[0:6])
                    sb.append(",")
                # Remove the extra comma
                sb.pop()
                sb.append("\n")
        WriteOutput.write_to_file_content("".join(sb).strip(), file_name + ".csv")

    @staticmethod
    def write_to_file_content(content: str, file_name: str):
        try:
            with open(file_name, 'w') as fw:
                fw.write(content)
        except IOError as e:
            print("Error writing to file:", e)   