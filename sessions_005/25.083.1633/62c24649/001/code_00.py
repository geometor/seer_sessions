"""
Creates a 2x2 tiled output grid from the input grid. The output grid is 
constructed by reflecting the input grid horizontally and vertically, 
resulting in four quadrants: original, horizontal mirror, vertical mirror, 
and combined horizontal and vertical mirror.
"""

import numpy as np

def reflect_horizontal(grid):
    return np.fliplr(grid)

def reflect_vertical(grid):
    return np.flipud(grid)

def transform(input_grid):
    # Convert input_grid to a NumPy array for easier manipulation
    input_grid = np.array(input_grid)

    # Get dimensions of the input grid
    rows, cols = input_grid.shape

    # Create mirrored versions of the input grid
    horizontal_mirror = reflect_horizontal(input_grid)
    vertical_mirror = reflect_vertical(input_grid)
    both_mirrors = reflect_horizontal(vertical_mirror)

    # Construct the top row by concatenating original and horizontal mirror
    top_row = np.concatenate((input_grid, horizontal_mirror), axis=1)

    # Construct the bottom row by concatenating vertical and combined mirrors
    bottom_row = np.concatenate((vertical_mirror, both_mirrors), axis=1)

    # Construct the output grid by stacking the top and bottom rows
    output_grid = np.concatenate((top_row, bottom_row), axis=0)

    return output_grid.tolist()