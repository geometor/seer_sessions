"""
1.  **Identify the Target Shape:** Locate the single contiguous region (object) of non-white pixels within the input grid.

2.  **Determine Bounding Box:** Find the smallest rectangle (the bounding box) that completely encloses the target shape. This is done by finding the minimum and maximum row and column indices of the non-white pixels.

3.  **Fill with Yellow:** Create a new grid, the same size as the input. All pixels within the bounding box determined in step 2 are colored yellow. All other pixels should remain unchanged.
"""

import numpy as np

def get_non_white_object(grid):
    # Find coordinates of all non-white pixels
    return np.where(grid != 0)

def get_bounding_box(coords):
    # get min and max of rows
    min_row = min(coords[0])
    max_row = max(coords[0])

    # get min and max of cols
    min_col = min(coords[1])
    max_col = max(coords[1])

    return min_row, max_row, min_col, max_col

def fill_bounding_box(grid, bbox):
  output_grid = np.zeros_like(grid)
  min_row, max_row, min_col, max_col = bbox

  # fill from top left
  for r in range(min_row, max_row + 1):
    for c in range(min_col, max_col + 1):
        output_grid[r, c] = 4  # Fill with yellow

  return output_grid

def transform(input_grid):
    # Initialize output grid as all white
    output_grid = np.zeros_like(input_grid)

    # Get coordinates of the non-white shape
    object_coords = get_non_white_object(input_grid)

    # get bounding box
    bbox = get_bounding_box(object_coords)

    # Fill the bounding box with yellow
    output_grid = fill_bounding_box(output_grid, bbox)

    return output_grid