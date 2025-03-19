"""
The transformation rule takes the connected blue shape and expands it downwards and to the right, creating extra space with the object stretched down and to the right.
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
    rows_to_add = int(np.ceil(height_shape * (2/3)))
    cols_to_add = int(np.ceil(width_shape * (2/3))) # edited from height

    # initialize the output
    output_grid = np.zeros((input_grid.shape[0] + rows_to_add, input_grid.shape[1] + cols_to_add), dtype=int)

    # copy input to output
    output_grid[:input_grid.shape[0], :input_grid.shape[1]] = input_grid

    # expand down
    for i in range(min_row, max_row+1):
        for j in range(rows_to_add):
            if output_grid[i, min_col:max_col+1].any():
                output_grid[i+j, min_col:max_col+1] = output_grid[i,min_col:max_col+1]

    # expand right
    for j in range(min_col,max_col +1):
      for i in range(cols_to_add):
        if output_grid[min_row:max_row+1, j].any():
            output_grid[min_row:max_row+1, j+i] = output_grid[min_row:max_row+1, j]


    return output_grid.tolist()