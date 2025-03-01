"""
1.  **Identify the Initiator:** Locate the initial yellow pixel (value 4) within the input grid.
2.  **Vertical Extension:** Extend the yellow color vertically upwards and downwards from the initial yellow pixel's column.
3.  **Stopping Condition:** The extension stops when it encounters a black pixel (value 0) or reaches the boundary of the grid. The extension includes the starting pixel.
"""

import numpy as np

def find_initial_yellow(grid):
    # Find the coordinates of the initial yellow pixel (value 4).
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i][j] == 4:
                return (i, j)
    return None

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)
    
    # Find the initial yellow pixel.
    initial_yellow_pos = find_initial_yellow(input_grid)
    if initial_yellow_pos is None:
        return output_grid # Return original if no yellow pixel is found.

    row, col = initial_yellow_pos

    # Extend upwards.
    for i in range(row - 1, -1, -1):
        if output_grid[i, col] == 0:
            break  # Stop at black pixel
        output_grid[i, col] = 4

    # Extend downwards.
    for i in range(row + 1, output_grid.shape[0]):
        if output_grid[i, col] == 0:
            break  # Stop at black pixel
        output_grid[i, col] = 4

    # set initial position
    output_grid[row,col] = 4

    return output_grid