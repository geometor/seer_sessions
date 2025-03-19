"""
1.  **Identify the Initiator:** Locate the initial yellow pixel (value 4) within the input grid.
2.  **Replicate with Constraints:** Starting from the row and column of the initial yellow pixel perform the following:
    *   From that initial position, and for every other row *above and below* the original, if the cell in the same column is not black (value 0), set it to yellow (value 4).
    * From that initial position, and for every other row *above and below* the original,
        *   if the cell one position to the left of the original is not black (value 0), set it to yellow (value 4).
        *   if the cell one position to the right of the original column is not black (value 0), and, set it to yellow (value 4).
3. **Boundary Condition.** The replication in any direction stops if it encounters a black pixel (value 0) or goes out of the grid boundary.
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

    # Replicate vertically and horizontally, both above and below.
    for i in range(output_grid.shape[0]):
        if (abs(i - row)) % 2 != 0 :  # every other row, above and below
            if output_grid[i, col] != 0:
                output_grid[i, col] = 4
            if col - 1 >= 0 and output_grid[i, col -1] != 0: #check if col is not out of range, and fill col to the left
                output_grid[i,col-1] = 4
            if col + 1 < output_grid.shape[1] and output_grid[i,col+1] != 0: #check if col is not out of range, and fill col to the right
                output_grid[i, col + 1] = 4

    return output_grid