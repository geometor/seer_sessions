"""
Extracts the top four rows of the input grid and maps non-zero (non-white) colors to 3 (green), while 0 (white) remains 0.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an input grid to an output grid based on the observed rule.

    Args:
        input_grid (list of lists): A 2D array representing the input grid.

    Returns:
        list of lists: The transformed 2D array (output grid).
    """
    # Initialize output_grid with the dimensions of top section
    output_grid = np.zeros((4, 4), dtype=int)

    # Iterate through the top four rows of input and change output accordingly
    for i in range(4):
        for j in range(4):
            if input_grid[i][j] == 0:
                output_grid[i][j] = 0  # Keep white as white
            else:
                output_grid[i][j] = 3  # Change any other color to green

    return output_grid.tolist()