"""
The transformation identifies yellow, red, and blue rectangles in the input grid and stacks them vertically in that order (yellow on top, then red, then blue) at the top of the output grid. The rectangles maintain their original widths and heights. All background (white/0) pixels are removed.
"""

import numpy as np

def find_object(grid, color):
    """Finds the top-left and bottom-right coordinates of a colored object."""
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None
    top_left = (min(rows), min(cols))
    bottom_right = (max(rows), max(cols))
    return top_left, bottom_right

def get_object_shape(top_left, bottom_right):
    """Calculates the shape of the rectangle."""
    height = bottom_right[0] - top_left[0] + 1
    width = bottom_right[1] - top_left[1] + 1
    return height, width

def create_object(grid, top_left, bottom_right):
  """ create an object by copying the cells """
  color = grid[top_left[0],top_left[1]]
  height, width = get_object_shape(top_left, bottom_right)
  obj = np.full((height, width), color)
  return obj

def remove_empty_rows(grid):
    """Removes rows that are entirely filled with 0s."""
    non_empty_rows = np.any(grid != 0, axis=1)
    filtered_grid = grid[non_empty_rows]
    return filtered_grid


def transform(input_grid):
    # initialize output_grid with the correct dimensions, filled with 0s.
    # It is difficult to know the correct dimension before processing all the
    # objects so we will start large
    output_grid = np.zeros((30,30), dtype=int)
    # Find and stack objects
    current_row = 0
    for color in [4, 2, 1]:  # Yellow, Red, Blue
        object_coords = find_object(input_grid, color)
        if object_coords:
            top_left, bottom_right = object_coords
            obj = create_object(input_grid, top_left, bottom_right)
            height, width = obj.shape

            output_grid[current_row:current_row + height, 0:width] = obj
            current_row += height
    
    #remove white space
    output_grid = remove_empty_rows(output_grid)

    return output_grid