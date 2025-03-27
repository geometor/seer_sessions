"""
1.  **Identify Background:** The background color is azure (8).
2.  **Find Isolated Pixel:** Locate the single white (0) pixel that is completely surrounded by the background color (8). A pixel is considered surrounded if all eight of its neighbors (horizontal, vertical, and diagonal) have the background color.
3.  **Transform:** Change the color of the isolated white pixel to green (3).
4.  **Output:** The output grid is identical to the input grid except for the single transformed pixel.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the 3x3 neighborhood around a pixel, including diagonals, handling edges."""
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

    # Identify Background: The background color is azure (8).
    background_color = 8

    # Find Isolated Pixel and Transform
    for i in range(rows):
        for j in range(cols):
            if output_grid[i, j] == 0 and is_isolated(output_grid, i, j, background_color):
                output_grid[i, j] = 3
                break  # Stop after finding and transforming the single isolated pixel
        else:
            continue
        break

    return output_grid.tolist()