"""
Inspects a 3x3 input grid. Identifies if there's a row where all pixels are yellow (color 4).
If such a row is found, it's preserved in the output grid. All other cells in the output
grid are set to gray (color 5).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    output_grid = np.full(input_grid.shape, 5)  # Initialize output grid with gray (5)

    # Iterate through each row of the input grid
    for i, row in enumerate(input_grid):
        # Check if all elements in the row are the same and equal to 4 (yellow)
        if np.all(row == 4):
            output_grid[i, :] = 4  # Copy the row to the output grid

    return output_grid