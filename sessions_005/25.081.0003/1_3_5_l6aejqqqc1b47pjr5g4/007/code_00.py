"""
1. Identify Yellow Regions: Find all contiguous regions of yellow (4) pixels in the input grid.
2. Fill to bottom: If any yellow exists in a column, fill that entire column with yellow from the highest yellow pixel in the input grid down to the bottom row.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate over each column
    for col in range(cols):
        # Check if any yellow exists in the column
        if 4 in input_grid[:, col]:
            # Find the highest row index with a yellow pixel in this column
            highest_yellow_row = 0
            for row in range(rows):
                if input_grid[row, col] == 4:
                  highest_yellow_row=row
                  break

            # Fill the column from the highest yellow row down to the bottom
            for row in range(highest_yellow_row, rows):
                output_grid[row, col] = 4

    return output_grid.tolist()