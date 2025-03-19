"""
Identify the color of the largest rectangular region at the bottom of the input grid and output it as a 1x1 grid.
"""

import numpy as np

def find_bottom_largest_rectangle_color(grid):
    """
    Finds the color of the largest rectangular region at the bottom of the grid.
    """
    rows, cols = grid.shape
    unique_colors = np.unique(grid)
    bottom_color = None
    max_height = 0

    for color in unique_colors:
        pixels = np.argwhere(grid == color)
        if pixels.size > 0:
            min_row, min_col = np.min(pixels, axis=0)
            max_row, max_col = np.max(pixels, axis=0)
            height = max_row - min_row + 1
            width = max_col - min_col + 1

            # Check if the region is at the bottom and is a rectangle
            if max_row == rows - 1 and np.all(grid[min_row:max_row+1, min_col:max_col+1] == color):
                if height > max_height:
                    max_height = height
                    bottom_color = color

    return bottom_color

def transform(input_grid):
    """
    Identifies the color of the largest rectangle at the bottom and outputs it as a 1x1 grid.
    """
    # Convert the input grid to a NumPy array.
    grid = np.array(input_grid)

    # Find the color of the bottom largest rectangle.
    bottom_color = find_bottom_largest_rectangle_color(grid)

    # Create a 1x1 output grid with the identified color.
    output_grid = np.array([[bottom_color]])

    return output_grid