"""
Counts the number of 2x2 subgrids within the input grid that have the same color.
The count is represented as a 1x1 grid with the count value colored red.
"""

import numpy as np

def count_homogeneous_2x2(grid):
    """
    Counts the number of 2x2 subgrids within the input grid that have the same value.
    """
    count = 0
    for i in range(grid.shape[0] - 1):
        for j in range(grid.shape[1] - 1):
            subgrid = grid[i:i+2, j:j+2]
            if np.all(subgrid == subgrid[0,0]):
                count += 1
    return count

def transform(input_grid):
    """
    Transforms the input grid to a 1x1 output grid.
    The output grid's value represents the number of homogeneous 2x2 subgrids
    within the input grid, and colored red.
    """
    # Convert the input to a NumPy array for easier manipulation.
    input_grid = np.array(input_grid)

    # Count the number of homogeneous 2x2 subgrids.
    count = count_homogeneous_2x2(input_grid)

    # Create a 1x1 output grid with the count, colored red (2).
    output_grid = np.array([[2]])
    output_grid[0,0]=count
    return output_grid