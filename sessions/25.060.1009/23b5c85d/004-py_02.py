"""
Extracts the inner azure square region from the input grid.
"""

import numpy as np

def find_inner_square(grid, color):
    # Find all pixels of the specified color.
    coords = np.argwhere(grid == color)
    if coords.size == 0:
      return None, None, None
    # Find the bounding box of these pixels.
    min_row = np.min(coords[:, 0])
    max_row = np.max(coords[:, 0])
    min_col = np.min(coords[:, 1])
    max_col = np.max(coords[:, 1])
    
    # Calculate dimensions
    height = max_row - min_row + 1
    width = max_col - min_col + 1

    return (min_row, min_col), height, width

def transform(input_grid):
    """
    Transforms the input grid by extracting the inner azure square.
    """
    # Find the inner azure (8) square.
    top_left, height, width = find_inner_square(input_grid, 8)

    # Check if valid object - otherwise return an empty array
    if top_left == None:
      return np.array([[]])

    # if the identified object is not square, return an empty array -
    # it is required to be square
    if height != width:
      return np.array([[]])

    # Create an output grid of the correct dimensions.
    output_grid = np.full((height, width), 8, dtype=int)

    return output_grid