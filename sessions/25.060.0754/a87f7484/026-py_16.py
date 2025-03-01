"""
Examine the input grid.
Check for 3x3 area in the top-left corner of input.
If the area exists and is a uniform non-black color, output that 3x3 square.
if the area does not exists or is black, output a 3x3 black square
"""

import numpy as np

def _is_uniform_3x3_square(grid, start_row, start_col):
    """
    Checks if a 3x3 square starting at (start_row, start_col) is uniform in color.
    Returns the color if uniform, otherwise None.
    """
    if start_row + 3 > len(grid) or start_col + 3 > len(grid[0]):
        return None  # Not enough space for a 3x3 square

    first_color = grid[start_row][start_col]
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if grid[i][j] != first_color:
                return None
    return first_color

def transform(input_grid):
    """
    Transforms the input grid according to the rule.
    """
    input_array = np.array(input_grid)
    color = _is_uniform_3x3_square(input_array, 0, 0)

    if color is not None and color in [1, 2, 3, 4, 6, 7, 8, 9]: #check if the identified color is not black
        # Isolate the 3x3 square
        output_array = input_array[0:3, 0:3]
        output_grid = output_array.tolist()
    else:
        # Create a 3x3 black grid
        output_grid = [[0] * 3 for _ in range(3)]

    return output_grid