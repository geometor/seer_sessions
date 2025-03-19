"""
The output is a 3x3 square subgrid extracted from the input grid. The subgrid
corresponds to the location of the single 3x3 colored square found in the
input.  The colors are prioritized in this order: green, yellow, blue.
"""

import numpy as np

def find_3x3_square(grid, color):
    """
    Finds the top-left coordinates of a 3x3 square of the given color.
    Returns None if no such square is found.
    """
    rows, cols = grid.shape
    for i in range(rows - 2):
        for j in range(cols - 2):
            if (grid[i:i+3, j:j+3] == color).all():
                return (i, j)
    return None

def transform(input_grid):
    """
    Extracts a 3x3 subgrid from the input, corresponding to the location
    of a 3x3 colored square (prioritizing green, then yellow, then blue).
    """
    input_array = np.array(input_grid)
    
    # Find the 3x3 square, prioritizing colors in order: green, yellow, blue
    for color in [3, 4, 1]:
        top_left = find_3x3_square(input_array, color)
        if top_left:
            break  # Exit the loop once a square of a prioritized color is found
    
    if top_left is None:
        return None # or perhaps raise an exception, depending on desired behavior if no square if found

    # Extract the 3x3 subgrid
    row_start, col_start = top_left
    output_array = input_array[row_start:row_start+3, col_start:col_start+3]

    output_grid = output_array.tolist()

    return output_grid