"""
Finds the non-zero color in the input grid, counts how many times they appear, and creates an output grid filled with that many instances of that color.
"""

import numpy as np

def get_nonzero_color(grid):
    # Flatten the grid and find unique colors
    unique_colors = np.unique(grid)
    # Return the non-zero color (assuming there's only one)
    for color in unique_colors:
        if color != 0:
            return color
    return 0

def count_color_instances(grid, color):
     #Count instances of the non-zero color
    return np.count_nonzero(grid == color)

def transform(input_grid):
    # Find the non-zero color in the input grid
    non_zero_color = get_nonzero_color(input_grid)

    # Count number of instances of non_zero_color
    color_count = count_color_instances(input_grid, non_zero_color)
    
    # Create output grid filled with the non-zero color
    output_grid = np.full((1, color_count), non_zero_color)

    return output_grid