"""
1.  **Identify Background:** The background color is maroon (9).
2.  **Identify Foreground:** The foreground objects are composed of blue (1) pixels.
3.  **Iterate Blue Pixels:** Examine each blue pixel in the input grid.
4.  **Check Connectivity:** Check if the blue pixel is part of a connected component (horizontal or vertical adjacency).
5.  **Replace Color:** If a blue pixel is part of connected set of 1 or more blue pixels (horizontal or vertical), change its color to azure (8).
6.  **Preserve Other Pixels:** Leave all maroon (9) pixels unchanged, and the blue (1) pixels unchanged if not adjacent to any other pixels.
"""

import numpy as np

def is_connected(grid, r, c):
    """Helper function to check for adjacent blue pixels."""
    rows, cols = grid.shape
    if grid[r,c] != 1:
        return False
    # Check adjacent cells (up, down, left, right)
    if r > 0 and grid[r-1, c] == 1:
        return True
    if r < rows - 1 and grid[r+1, c] == 1:
        return True
    if c > 0 and grid[r, c-1] == 1:
       return True
    if c < cols - 1 and grid[r, c+1] == 1:
        return True
    return False

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel
    for r in range(rows):
        for c in range(cols):
            # Check if the pixel is blue (1)
            if input_grid[r, c] == 1:
                # Check connectivity
                if is_connected(input_grid, r,c):
                     output_grid[r,c] = 8

    return output_grid