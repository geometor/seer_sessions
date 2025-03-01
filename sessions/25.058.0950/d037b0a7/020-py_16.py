"""
1. Identify all pixels that are yellow (4).
2. Copy the yellow color to all cells directly below it in the same column, extending down to the bottom row (row 2).
3. Identify all pixels that are red (2).
4. Copy the red color to all cells directly below it in the same column, down to the bottom row (row 2).
5. Leave white pixels unchanged.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid by extending yellow and red colors downwards."""
    output_grid = np.copy(input_grid)  # Initialize output_grid as a copy of the input_grid
    rows, cols = output_grid.shape

    # Iterate through each column
    for j in range(cols):
        # Iterate through each row in the column
        for i in range(rows):
            # Extend yellow color downwards
            if input_grid[i, j] == 4:  # Check for yellow pixel
                for k in range(i + 1, rows):  # Iterate downwards from current position
                    output_grid[k, j] = 4  # Set the pixel to yellow

            # Extend red color downwards
            elif input_grid[i, j] == 2:  # Check for red pixel
                for k in range(i + 1, rows): # Iterate downwards from current position
                    output_grid[k, j] = 2  # Set the pixel to red

    return output_grid