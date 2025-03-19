"""
Iterate through each cell of the input grid.
If the cell's color is gray (5), change it to green (3) in the output grid.
If the cell's color is white (0), change it to yellow (4) in the output grid.
If a cell is any other color, keep the color unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with the same dimensions as the input grid.
    output_grid = np.copy(input_grid)  # Start with a copy to preserve original colors
    rows, cols = input_grid.shape

    # Iterate through each cell of the input grid.
    for i in range(rows):
        for j in range(cols):
            # Apply the color transformation rules.
            if input_grid[i, j] == 5:
                output_grid[i, j] = 3  # Change gray (5) to green (3)
            elif input_grid[i, j] == 0:
                output_grid[i, j] = 4  # Change white (0) to yellow (4)

    return output_grid