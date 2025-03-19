"""
Extract the single non-zero value from the input grid and place it in a 1 x 1 grid.
"""

import numpy as np

def find_nonzero_pixel(grid):
    # Find the coordinates of the non-zero pixel.
    rows, cols = np.where(grid != 0)
    if len(rows) > 0:  # Check if a non-zero pixel was found
       return rows[0], cols[0]
    return None  # Or handle the case where no non-zero pixel exists differently


def transform(input_grid):
    """
    Transforms the input grid by extracting the non-zero value.
    """
    # Find the coordinates of non-zero pixel.
    coords = find_nonzero_pixel(np.array(input_grid))

    # Create a 1x1 output grid.
    output_grid = np.zeros((1, 1), dtype=int)

    # Set the value of the output grid to the non-zero pixel's value.
    if coords:
        row, col = coords
        output_grid[0, 0] = input_grid[row][col]

    return output_grid.tolist()