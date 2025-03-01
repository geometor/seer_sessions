"""
1.  **Identify** all pixels in the input grid that have the value 3 (green).
2.  **Check Adjacency:** For each green pixel, examine its immediate neighbors (up, down, left, and right).
3. **Conditional color change**: If a green pixel is directly adjacent to any pixel with value of 2 (red) on any of the four sides, change that green pixel's value to 8 (azure).
4.  **Preserve other pixels** All other pixels that are not a `3` adjacent to a `2` retain their original values.
5.  **Output:** Create the output grid with the modified pixel values.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    Returns a list of neighboring pixel values (up, down, left, right).
    """
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append(grid[row - 1, col])  # Up
    if row < rows - 1:
        neighbors.append(grid[row + 1, col])  # Down
    if col > 0:
        neighbors.append(grid[row, col - 1])  # Left
    if col < cols - 1:
        neighbors.append(grid[row, col + 1])  # Right
    return neighbors

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel of input grid
    for row in range(rows):
        for col in range(cols):
            # Identify green pixels (value 3)
            if input_grid[row, col] == 3:
                # Check Adjacency
                neighbors = get_neighbors(input_grid, row, col)
                # Conditional color change: if adjacent to red (2), change to azure (8)
                if 2 in neighbors:
                    output_grid[row, col] = 8

    return output_grid