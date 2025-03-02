"""
The program identifies a yellow block, maintains the lower region of the image,
and places a yellow pixel in the top-right corner of the grid, mirroring its
original relative position by only using the top-right pixel of that position.
"""

import numpy as np

def find_object(grid, color):
    # Find the coordinates of all pixels of the given color.
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None, None, None, None
    # Calculate the bounding box.
    min_row, min_col = coords.min(axis=0)
    max_row, max_col = coords.max(axis=0)
    return min_row, min_col, max_row, max_col

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = input_grid.copy()
    
    # Find the yellow (4) object.
    min_row_y, min_col_y, max_row_y, max_col_y = find_object(input_grid, 4)

    if min_row_y is None:
        return output_grid

    # "Displacement"
    grid_height, grid_width = input_grid.shape

    new_x = grid_width - (max_col_y - min_col_y +1)  #+ min_col_y
    new_y = 0

    # Place the yellow pixel
    output_grid[:min_row_y, :] = 0
    if 0 <= new_x < grid_width and 0 <= new_y < grid_height:  # Ensure within bounds
      output_grid[new_y, new_x] = 4


    return output_grid