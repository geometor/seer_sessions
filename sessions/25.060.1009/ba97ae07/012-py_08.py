"""
Identify a horizontal stripe of blue pixels.
Identify a vertical stripe of magenta pixels (can be non-contiguous).
Find the intersection of the two stripes.
Change the color of the blue pixels within the intersection to magenta.
"""

import numpy as np

def find_horizontal_stripe(grid, color):
    # Find a contiguous horizontal stripe of a given color.
    for row_index in range(grid.shape[0]):
        if all(grid[row_index, :] == color):
            return row_index
    return None

def find_vertical_stripe(grid, color):
    # Find a vertical stripe of a given color, allowing for non-contiguous segments (one row gap).
    stripe_cols = []
    for col_index in range(grid.shape[1]):
        if all(grid[:, col_index] == color) or (all(grid[:3, col_index] == color) and all(grid[4:, col_index] == color)):
            stripe_cols.append(col_index)
    return stripe_cols

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find blue horizontal stripe
    blue_row = find_horizontal_stripe(output_grid, 1)

    # Find magenta vertical stripe
    magenta_cols = find_vertical_stripe(output_grid, 6)

    # Change blue cells to magenta at intersection
    if blue_row is not None and magenta_cols:
        for col in magenta_cols:
            if output_grid[blue_row, col] == 1:  # Check if it's blue before changing
                output_grid[blue_row, col] = 6

    return output_grid