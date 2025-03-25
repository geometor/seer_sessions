"""
1.  **Create Output Grid:** Create a 4x4 output grid filled with white (0).
2.  **Input Region:** Consider the top-left 4x4 region of the input grid.
3.  **Locate Target Pixels:** Within this 4x4 input region, find the green (3) pixels that *touch* a blue (1) pixel (up, down, left, or right).
4.  **Place Red Pixels:** In the 4x4 *output* grid, place red (2) pixels at the *same* coordinates where the green pixels touching blue pixels were found in the *4x4 input region*.
5. **Fill**: The remaining pixels in the output are already white by initialization.
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
    # Create a 4x4 output grid filled with white (0)
    output_grid = np.zeros((4, 4), dtype=int)

    # Iterate through the top-left 4x4 region of the input grid
    for row in range(min(4, input_grid.shape[0])):
        for col in range(min(4, input_grid.shape[1])):
            # Check if the current pixel is green (3)
            if input_grid[row, col] == 3:
                # Get the neighbors of the current pixel
                neighbors = get_neighbors(input_grid, row, col)
                # Check if any of the neighbors are blue (1)
                if 1 in neighbors:
                    # If a green pixel touches a blue pixel, place a red pixel in the output grid at the same coordinates
                    output_grid[row, col] = 2

    return output_grid