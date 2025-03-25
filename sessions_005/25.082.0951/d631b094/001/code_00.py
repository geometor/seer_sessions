"""
The transformation rule identifies the non-zero color in the input grid, counts the occurrences of that color, 
and creates a new grid filled with that color, with a size equal to count of non-zero colors in input.
"""

import numpy as np

def get_nonzero_color(grid):
    # Flatten the grid and remove zeros
    unique_colors = np.unique(grid[grid != 0])
    if unique_colors.size > 0:
      return unique_colors[0]
    return 0

def count_target_color(grid, target_color):
    # Count occurrences of the target color in the grid.
    count = np.sum(grid == target_color)
    return count

def transform(input_grid):
    # Find the non-zero color in the input grid.
    target_color = get_nonzero_color(input_grid)

    # If no non-zero color is found, return an empty grid (or handle as needed).
    if target_color == 0:
        return np.array([])

    # Count number of that color
    count = count_target_color(input_grid, target_color)
        
    # Create a new grid filled with the target color, dimensions are equal to the count.
    output_grid = np.full((1, count), target_color)

    return output_grid