"""
Copies the input grid to the output grid. Iterates through each pixel of the input grid.
If a pixel is white (0) and is adjacent (horizontally, vertically, or diagonally) to at least one grey pixel (5),
the corresponding pixel in the output grid is changed to red (2). Otherwise, the pixel remains unchanged.
"""

import numpy as np

def get_adjacent_pixels(grid, row, col):
    """Gets the values of adjacent pixels (up, down, left, right, and diagonals)."""
    rows, cols = grid.shape
    adjacent = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):  # Exclude the pixel itself
                adjacent.append((i, j, grid[i, j]))
    return adjacent

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel
    for row in range(rows):
        for col in range(cols):
            # Check if the pixel is white (0)
            if input_grid[row, col] == 0:
                # Get adjacent pixels (including diagonals)
                adjacent = get_adjacent_pixels(input_grid, row, col)
                
                # Check if any adjacent pixel is grey (5)
                for _, _, value in adjacent:
                    if value == 5:
                        # Change the corresponding pixel in output_grid to red (2)
                        output_grid[row, col] = 2
                        break  # Move to the next pixel after changing

    return output_grid