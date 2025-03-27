"""
1.  **Identify Leftmost Yellow Column:** Find the index of the leftmost column in the input grid that contains at least one yellow (4) pixel.
2.  **Identify Blue Column:** Find the index of the column containing *only* blue (1) pixels.
3.  **Create Subgrid:** Create a subgrid (output grid) from the input grid, using the full height of the input grid. The columns span from the leftmost yellow column (inclusive) up to, but not including, the blue column.
4.  **Replace Colors:** Within the created subgrid, replace all yellow (4) pixels with azure (8) pixels.
5. **Output:** return the subgrid
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
    """Finds the index of the column containing ONLY blue (1) pixels."""
    for j in range(grid.shape[1]):
        column = grid[:, j]
        if np.all(column == 1):
            return j
    return -1    

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)
    
    # Find the leftmost yellow column
    leftmost_yellow_column = find_leftmost_yellow_column(input_grid)
    
    # Find the blue column
    blue_column = find_blue_column(input_grid)

    # Create subgrid: Full height, columns from leftmost yellow to blue (exclusive)
    output_grid = input_grid[:, leftmost_yellow_column:blue_column].copy()

    # Replace yellow (4) with azure (8) within the subgrid
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            if output_grid[i, j] == 4:
                output_grid[i, j] = 8

    return output_grid.tolist()