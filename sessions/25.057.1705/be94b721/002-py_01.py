"""
Identifies and extracts the red colored region from the input grid.
"""

import numpy as np

def find_object(grid, color_value):
    """
    Finds the bounding box of a contiguous region of a specific color.
    """
    rows, cols = np.where(grid == color_value)
    if len(rows) == 0:
        return None  # Object not found
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, min_col), (max_row, max_col)

def transform(input_grid):
    """
    Transforms the input grid by extracting the red region.
    """
    # Find the bounding box of the red region (color value 2).
    red_bounding_box = find_object(input_grid, 2)

    if red_bounding_box is None:
        return np.zeros((0, 0), dtype=int) #return empty grid if no object

    # Extract the red region using the bounding box.
    (min_row, min_col), (max_row, max_col) = red_bounding_box
    output_grid = input_grid[min_row:max_row+1, min_col:max_col+1]

    return output_grid