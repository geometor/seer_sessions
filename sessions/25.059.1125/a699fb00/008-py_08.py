"""
1.  **Identify Target Pixels:** Locate all blue (value 1) pixels within the input grid.
2.  **Count Adjacent Pixels:** For each identified blue pixel, count the number of adjacent pixels (up, down, left, and right) that have *any non-zero* color.
3.  **Conditional Color Change:** If a blue pixel has *more than one* adjacent pixel of any non-zero color , change its color to red (value 2).
4. **All other pixels:** are unchanged
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    Gets the values of the four immediate neighbors (up, down, left, right) of a given pixel.
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
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate over each pixel in the grid
    for row in range(rows):
        for col in range(cols):
            # Check if the current pixel is blue (1)
            if input_grid[row, col] == 1:
                # Get the values of the four immediate neighbors
                neighbors = get_neighbors(input_grid, row, col)
                # Count how many neighbors are non-zero
                non_zero_neighbors_count = sum(1 for neighbor in neighbors if neighbor != 0)
                # If more than one neighbor is non-zero, change the pixel to red (2)
                if non_zero_neighbors_count > 1:
                    output_grid[row, col] = 2

    return output_grid