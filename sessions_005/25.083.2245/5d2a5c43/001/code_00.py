"""
1.  **Identify Subgrid:** In the input grid find the borders made out of yellow, from the leftmost yellow vertically and horizontally.
2.  **Replace:** Within this subgrid, change all yellow (4) pixels to azure (8).
3.  **Output:** Return this subgrid of the same height as input, but using only columns delimited by the leftmost vertical yellow border, and the vertical line of 1s in the input.
"""

import numpy as np

def find_leftmost_yellow_column(grid):
    """Finds the index of the leftmost column containing a yellow (4) pixel."""
    for j in range(grid.shape[1]):
        for i in range(grid.shape[0]):
            if grid[i, j] == 4:
                return j
    return -1  # Should not happen in valid input

def find_blue_column(grid):
    """Find the column where blue(1) values are."""
    
    cols = np.where(grid == 1)[1]
    
    return int(np.mean(cols))

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    # Convert input to numpy array
    input_grid = np.array(input_grid)
    
    # Find the leftmost yellow column
    leftmost_yellow_column = find_leftmost_yellow_column(input_grid)
    
    
    # Find blue column
    blue_column = find_blue_column(input_grid)

    # Initialize output grid
    output_grid = np.copy(input_grid)
    
    # set output to only region of interest
    output_grid = output_grid[:, leftmost_yellow_column:blue_column]

    # Replace yellow (4) with azure (8) within the subgrid
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            if output_grid[i, j] == 4:
                output_grid[i, j] = 8

    return output_grid.tolist()