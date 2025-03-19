"""
The transformation rule identifies the blue object in the input grid and expands the grid downwards and to the right. The number of rows added is equal to the height of the original blue object, and the number of columns added is equal to the width of the original blue object. The original blue object's bottom row is extended downwards, and its right-most column is extended to the right, creating the expanded blue shape.
"""

import numpy as np

def find_blue_object(grid):
    # Find the coordinates of blue pixels (value 1).
    blue_pixels = np.argwhere(grid == 1)
    if len(blue_pixels) == 0:
        return None, None, None, None

    # Find the bounding box of the blue object.
    min_row, min_col = np.min(blue_pixels, axis=0)
    max_row, max_col = np.max(blue_pixels, axis=0)

    return min_row, max_row, min_col, max_col

def transform(input_grid):
    # Convert input grid to a NumPy array.
    input_grid = np.array(input_grid)

    # Find the bounding box of the blue object.
    min_row, max_row, min_col, max_col = find_blue_object(input_grid)
    if min_row is None:  # No blue object found, return original grid.
        return input_grid.tolist()

    # Calculate dimensions of blue shape
    height_shape = max_row-min_row + 1
    width_shape = max_col - min_col + 1

    # calculate expansion amounts
    rows_to_add = height_shape
    cols_to_add = width_shape

    # initialize the output
    output_grid = np.zeros((input_grid.shape[0] + rows_to_add, input_grid.shape[1] + cols_to_add), dtype=int)

    # copy input to output
    output_grid[:input_grid.shape[0], :input_grid.shape[1]] = input_grid

   # Expand downwards: extend the bottom row of the blue object.
    for i in range(rows_to_add):
        output_grid[max_row + 1 + i, min_col:max_col + 1] = output_grid[max_row, min_col:max_col + 1]

    # Expand to the right: extend the right-most column of the blue object.
    for j in range(cols_to_add):
        output_grid[min_row:max_row + rows_to_add + 1, max_col + 1 + j] = output_grid[min_row:max_row + rows_to_add + 1, max_col]

    return output_grid.tolist()