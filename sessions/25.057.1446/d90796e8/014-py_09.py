"""
Finds red(2) pixels adjacent to green(3) or gray(5) pixels in the input grid and changes them to azure(8) in the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each cell in the grid
    for i in range(rows):
        for j in range(cols):
            # Check if the current cell is red (2)
            if input_grid[i, j] == 2:
                # Check for adjacent green (3) or gray (5) cells
                adjacent_cells = []
                if i > 0:
                    adjacent_cells.append(input_grid[i - 1, j])  # Up
                if i < rows - 1:
                    adjacent_cells.append(input_grid[i + 1, j])  # Down
                if j > 0:
                    adjacent_cells.append(input_grid[i, j - 1])  # Left
                if j < cols - 1:
                    adjacent_cells.append(input_grid[i, j + 1])  # Right

                # If any adjacent cell is green or gray, change the current cell to azure
                if 3 in adjacent_cells or 5 in adjacent_cells:
                    output_grid[i, j] = 8

    return output_grid