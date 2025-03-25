"""
Transforms green pixels in the top four rows of the input grid to red if they are adjacent to white pixels (in the input grid), otherwise to white.
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

def transform(input_grid):
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # Create output grid using the top four rows of input grid
    output_grid = np.copy(input_grid[:4,:])

    # Iterate through the top four rows for transformation
    for r in range(min(4,rows)): # to avoid error if the input height < 4
        for c in range(cols):
            if output_grid[r, c] == 3:  # If green
                adjacent_pixels = get_adjacent_pixels(input_grid, r, c)
                if 0 in adjacent_pixels:
                    output_grid[r, c] = 2  # Change to red
                else:
                    output_grid[r, c] = 0  # Change to white

    return output_grid.tolist()