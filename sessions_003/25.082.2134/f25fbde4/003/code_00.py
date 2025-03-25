"""
1.  **Identify Yellow Shape:** Find all pixels with the value 4 (yellow) in the
    input grid. These form the `yellow_shape`.

2.  **Determine Bounding Box:** Calculate the minimum and maximum row and column
    indices of the `yellow_shape`. This defines the `bounding_box`.

3.  **Inflate Bounding Box:** Expand the `bounding_box` by one pixel in each
    direction (up, down, left, and right).  Crucially, ensure this inflation
    stays *within* the boundaries of the original input grid. This is the
    `inflated_box`.

4.  **Create Output Grid:** Create an output grid of the *same dimensions* as
    the *input grid*.

5.  **Fill the Output Grid:**

    -   Fill the area defined by the `inflated_box` within the output grid with
        yellow pixels (value 4).
    -   Fill the remaining area of the output grid (outside the `inflated_box`)
        with white pixels (value 0).
"""

import numpy as np

def _find_yellow_shape(grid):
    # Find coordinates of yellow pixels (value 4)
    yellow_pixels = np.argwhere(grid == 4)
    return yellow_pixels

def _bounding_box(coords):
    # Calculate min and max row/col indices
    min_row = np.min(coords[:, 0])
    max_row = np.max(coords[:, 0])
    min_col = np.min(coords[:, 1])
    max_col = np.max(coords[:, 1])
    return min_row, max_row, min_col, max_col

def _inflate_bounding_box(min_row, max_row, min_col, max_col, input_shape):
    # expand by one pixel in each direction within the original input shape
    min_row = max(0, min_row - 1)
    max_row = min(input_shape[0] - 1, max_row + 1)
    min_col = max(0, min_col - 1)
    max_col = min(input_shape[1] - 1, max_col + 1)
    
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    input_grid = np.array(input_grid)  # Ensure numpy array

    # Find yellow shape coordinates
    yellow_coords = _find_yellow_shape(input_grid)

    # Handle case where there are no yellow pixels
    if len(yellow_coords) == 0:
        return np.zeros_like(input_grid).tolist() # Return input grid sized 0s

    # Get bounding box
    min_row, max_row, min_col, max_col = _bounding_box(yellow_coords)
    
    # inflate
    min_row, max_row, min_col, max_col = _inflate_bounding_box(min_row, max_row, min_col, max_col, input_grid.shape)
    
    # Create output grid with same dimensions as input
    output_grid = np.zeros_like(input_grid)
    
    # fill bounding box with color 4
    output_grid[min_row:max_row+1, min_col:max_col+1] = 4

    return output_grid.tolist()