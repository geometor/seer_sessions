"""
The transformation involves identifying all unique colors within the input grid, selecting the *largest* color value, and creating an output grid of the same dimensions as the input, filled entirely with the selected color.
"""

import numpy as np

def get_present_colors(grid):
    # Flatten the grid to a 1D array and get unique values
    unique_colors = np.unique(grid)
    return list(unique_colors)

def transform(input_grid):
    # Get the dimensions of the input grid
    rows, cols = input_grid.shape

    # Identify present colors in input
    present_colors = get_present_colors(input_grid)

    # select the largest color for the output
    output_color = max(present_colors)

    # Create an output grid of the same dimensions, filled with the selected color
    output_grid = np.full((rows, cols), output_color)

    return output_grid