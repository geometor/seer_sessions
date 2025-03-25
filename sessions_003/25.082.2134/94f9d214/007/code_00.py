"""
Transforms green pixels in the top four rows of the input grid to red if they are adjacent to white pixels (in the input grid), otherwise to white. The output grid has the same width as the input, and its height is equal to the maximum of input and expected output heights. Rows beyond the fourth are filled with white.
"""

import numpy as np

def get_adjacent_pixels(grid, r, c):
    """Gets the values of adjacent pixels (including diagonals)."""
    rows, cols = grid.shape
    adjacent = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue  # Skip the cell itself
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                adjacent.append(grid[nr, nc])
    return adjacent

def transform(input_grid, expected_output=None):
    input_grid = np.array(input_grid)
    input_rows, cols = input_grid.shape
    
    # Determine output_rows based on expected_output if available, otherwise use input_rows
    if expected_output is not None:
        expected_output_grid = np.array(expected_output)
        expected_rows = expected_output_grid.shape[0]
        output_rows = max(input_rows, expected_rows)
    else:
        output_rows = input_rows


    # Create output grid with appropriate dimensions, initialized to white (0)
    output_grid = np.zeros((output_rows, cols), dtype=int)

    # Iterate through the top four rows of the input grid for transformation
    for r in range(min(4, input_rows)):
        for c in range(cols):
            if input_grid[r, c] == 3:  # If green
                adjacent_pixels = get_adjacent_pixels(input_grid, r, c)
                if 0 in adjacent_pixels:
                    output_grid[r, c] = 2  # Change to red
                else:
                    output_grid[r, c] = 0  # Change to white

    return output_grid.tolist()