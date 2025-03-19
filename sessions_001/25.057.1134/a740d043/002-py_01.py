"""
Extract a 3x3 subgrid centered around a region of interest (red and green pixels), preserving the relative positions of those colors and replacing others with white.
"""

import numpy as np

def find_object(grid, color):
    # Find coordinates of all pixels of the specified color.
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None
    return coords

def get_bounding_box(coords):
    # Get the bounding box of a set of coordinates.
    min_row = np.min(coords[:, 0])
    max_row = np.max(coords[:, 0])
    min_col = np.min(coords[:, 1])
    max_col = np.max(coords[:, 1])
    return (min_row, max_row, min_col, max_col)

def get_center(coords):
  """get center coordinate of a group of pixels"""
  return np.mean(coords, axis=0).astype(int)

def transform(input_grid):
    # Find red and green objects.
    red_coords = find_object(input_grid, 2)
    green_coords = find_object(input_grid, 3)

    # Initialize output grid with white.
    output_grid = np.zeros((3, 3), dtype=int)

    # use center of red object
    center = get_center(red_coords)

    # Calculate the offset for the 3x3 subgrid within the input grid.
    row_offset = center[0] - 1
    col_offset = center[1] - 1

    # Transfer red and green pixels to the output grid.
    for r in range(3):
        for c in range(3):
            input_row = row_offset + r
            input_col = col_offset + c

            # Check if the input coordinates are within the bounds of the input grid.
            if 0 <= input_row < input_grid.shape[0] and 0 <= input_col < input_grid.shape[1]:
              pixel = input_grid[input_row, input_col]
              if pixel == 2 or pixel == 3:  # red and green
                output_grid[r, c] = pixel

    return output_grid