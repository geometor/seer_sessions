"""
1.  **Identify Target Pixels:** Examine the input grid. Find green (3) pixels that *touch* a blue (1) pixel. *Touch* is defined as up, down, left or right.
2.  **Create Output Grid**: create a new empty 4x4 grid
3.  **Place Red Pixels:** In the new 4x4 grid, place red (2) pixels in the locations that *correspond* to those of the green pixels *touching* blue pixels in the input grid.
4.  **Fill with White**: fill the remaining pixels with white (0).
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    Returns a list of the values of the neighbors of a given cell.
    """
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append(grid[row-1, col])  # Up
    if row < rows - 1:
        neighbors.append(grid[row+1, col])  # Down
    if col > 0:
        neighbors.append(grid[row, col-1])  # Left
    if col < cols - 1:
        neighbors.append(grid[row, col+1])  # Right
    return neighbors

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((4, 4), dtype=int)

    rows, cols = input_grid.shape
    
    # Iterate through input grid
    for row in range(rows):
      for col in range(cols):
        # change output pixels based on touching pixels
        if input_grid[row,col] == 3:
            neighbors = get_neighbors(input_grid, row, col)
            if 1 in neighbors:  # Check if any neighbor is blue (1)
                if row < 4 and col < 4: #prevent out of bounds for output
                  output_grid[row, col] = 2
        if input_grid[row,col] == 1:
            neighbors = get_neighbors(input_grid, row, col)
            if 3 in neighbors:  # Check if any neighbor is blue (1)
                if row < 4 and col < 4: #prevent out of bounds for output
                  output_grid[row, col] = 2

    return output_grid