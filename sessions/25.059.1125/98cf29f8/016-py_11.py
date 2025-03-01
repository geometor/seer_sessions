"""
The input grid contains a composite object resembling a flower with a red top and a green base. The transformation moves the green base upwards to be adjacent to the red top.
"""

import numpy as np

def find_object(grid, color):
    """
    Finds the bounding box of an object of the specified color.

    Args:
      grid: The input grid (numpy array).
      color: The color of the object to find.

    Returns:
      A tuple (min_row, max_row, min_col, max_col) representing the bounding box,
      or None if the color is not found.
    """
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, max_row, min_col, max_col)

def transform(input_grid):
    """
    Transforms the input grid by moving the green base of the flower upwards.
    """
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Find the red top and green base
    red_bbox = find_object(input_grid, 2)
    green_bbox = find_object(input_grid, 3)
    
    if red_bbox is None or green_bbox is None:
      return output_grid

    # Calculate dimensions
    red_min_row, red_max_row, red_min_col, red_max_col = red_bbox
    green_min_row, green_max_row, green_min_col, green_max_col = green_bbox

    red_height = red_max_row - red_min_row + 1
    green_height = green_max_row - green_min_row + 1
    green_width = green_max_col - green_min_col + 1

    # Move green base up
    new_green_start_row = red_max_row + 1  # Directly below red

    # clear the old green area
    output_grid[green_min_row:green_max_row + 1, green_min_col:green_max_col + 1] = 0

    # fill in new green area
    output_grid[new_green_start_row:new_green_start_row+ (green_max_row-green_min_row)+1, green_min_col:green_max_col+1] = 3

    # remove single green cells below red
    for c in range(red_min_col, red_max_col + 1):
        for r in range(red_max_row + 1, input_grid.shape[0]):
            if output_grid[r,c] == 3:
               output_grid[r,c] = 0
            

    return output_grid