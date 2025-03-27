"""
1.  **Determine Background:** The background color is typically azure (8).
2.  **Iterate:** Examine each pixel in the input grid.
3.  **Isolate Check:** For each pixel, check if it's "isolated." A pixel is isolated if *all* its immediate neighbors (up, down, left, right, and diagonals) have the background color.
4.  **Conditional transform:** If a pixel is isolated *and* is not already the background color, change its color to green (3).
5.  **Output:** The output grid is the modified input grid, with isolated non-background pixels changed to green.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the 3x3 neighborhood around a pixel, including diagonals."""
    rows, cols = grid.shape
    neighbors = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):
                neighbors.append(grid[i, j])
    return neighbors

def is_isolated(grid, row, col, background_color):
    """Checks if a pixel is surrounded by the background color."""
    neighbors = get_neighbors(grid, row, col)
    return all(neighbor == background_color for neighbor in neighbors)

def transform(input_grid):
    """Transforms the input grid according to the rules."""
    input_grid = np.array(input_grid)  # Ensure numpy array
    output_grid = input_grid.copy()
    rows, cols = output_grid.shape

    # Determine Background: Assume azure (8) for now.
    background_color = 8

    # Iterate through each pixel
    for i in range(rows):
        for j in range(cols):
            # Check if the pixel is isolated and not the background color
            if output_grid[i, j] != background_color and is_isolated(output_grid, i, j, background_color):
                # Transform isolated non-background pixels to green (3)
                output_grid[i, j] = 3

    return output_grid.tolist()