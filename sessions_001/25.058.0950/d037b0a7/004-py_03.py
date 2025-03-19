"""
The transformation rule examines each column of the input grid. If a column contains any non-background (non-zero) pixels, the entire column is filled with the first encountered non-background color. If a column contains only background (zero) pixels, the entire column is filled with the background color (zero).
"""

import numpy as np

def get_column(grid, col_index):
    """Extracts a column from a 2D numpy array."""
    return grid[:, col_index]

def set_column(grid, col_index, color):
    """Sets all elements of a column in a 2D numpy array to a given color."""
    grid[:, col_index] = color
    return grid

def transform(input_grid):
    """
    Transforms the input grid according to the column-filling rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each column
    for j in range(cols):
        column = get_column(input_grid, j)
        
        # Find the first non-zero color in the column
        non_zero_pixels = column[column != 0]
        if non_zero_pixels.size > 0:
            fill_color = non_zero_pixels[0]  # Use the first non-zero color
        else:
            fill_color = 0  # Use the background color

        # Fill the entire column in the output grid
        output_grid = set_column(output_grid, j, fill_color)

    return output_grid