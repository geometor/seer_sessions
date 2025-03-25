"""
1.  **Locate Yellow Shape:** Find all yellow pixels (value 4) in the input grid. If no yellow pixels are found, return an empty grid.

2.  **Determine Bounding Box:** Calculate the bounding box of the yellow shape using the minimum and maximum row and column indices of the yellow pixels.

3.  **Inflate Bounding Box:** Expand the bounding box by one pixel in each direction (up, down, left, right).  Ensure the inflated bounding box stays within the original grid boundaries (0-29 for rows and columns).

4. **Create Output Grid:** Create a new output grid *with the same dimensions as the section of the input grid corresponding to the inflated bounding box*.

5.  **Copy and Populate:** Copy all pixels from the section of the original input that corresponds to the position and dimensions of the *inflated* bounding box. Then, iterate the output grid. For each pixel location that falls within the dimensions of the *original* (non-inflated) bounding box relative to the output grid's origin, set that pixel to yellow (value 4).
"""

import numpy as np

def _find_yellow_shape(grid):
    # Find coordinates of yellow pixels
    return np.argwhere(grid == 4)

def _bounding_box(coords):
    # Calculate min and max row/col
    min_row = np.min(coords[:, 0])
    max_row = np.max(coords[:, 0])
    min_col = np.min(coords[:, 1])
    max_col = np.max(coords[:, 1])
    return min_row, max_row, min_col, max_col

def _inflate_bounding_box(min_row, max_row, min_col, max_col, input_shape):
    # expand by one within valid bounds
    min_row = max(0, min_row - 1)
    max_row = min(input_shape[0] - 1, max_row + 1)
    min_col = max(0, min_col - 1)
    max_col = min(input_shape[1] - 1, max_col + 1)
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    input_grid = np.array(input_grid)

    # Find yellow shape
    yellow_coords = _find_yellow_shape(input_grid)

    # Handle no yellow pixels
    if len(yellow_coords) == 0:
        return []

    # Get bounding box
    min_row, max_row, min_col, max_col = _bounding_box(yellow_coords)

    # Inflate bounding box
    inf_min_row, inf_max_row, inf_min_col, inf_max_col = _inflate_bounding_box(min_row, max_row, min_col, max_col, input_grid.shape)

    # Create output - slice of input corresponding to inflated box
    output_grid = input_grid[inf_min_row:inf_max_row + 1, inf_min_col:inf_max_col + 1].copy()

    # Convert original bounding box region to yellow
    # adjust coordinates to be relative to the output grid
    rel_min_row = min_row - inf_min_row
    rel_max_row = max_row - inf_min_row
    rel_min_col = min_col - inf_min_col
    rel_max_col = max_col - inf_min_col

    output_grid[rel_min_row:rel_max_row+1, rel_min_col:rel_max_col+1] = 4


    return output_grid.tolist()